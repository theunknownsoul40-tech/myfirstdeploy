from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import uuid


@dataclass(frozen=True)
class EvidenceLocation:
    document_id: str
    document_name: str
    page: int
    region_id: str
    bbox: list[float]


@dataclass
class EvidenceNode:
    """Auditable evidence for one extracted field/value."""

    field: str
    value: Any
    location: EvidenceLocation
    ocr_confidence: Optional[float] = None
    ner_confidence: Optional[float] = None
    validation: str = "PENDING"
    human_verification: str = "PENDING"
    source_text: Optional[str] = None
    extraction_model: Optional[str] = None
    evidence_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def combined_confidence(self) -> Optional[float]:
        values = [v for v in (self.ocr_confidence, self.ner_confidence) if v is not None]
        return round(sum(values) / len(values), 4) if values else None

    def approve(self) -> None:
        self.human_verification = "APPROVED"

    def reject(self) -> None:
        self.human_verification = "REJECTED"

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["combined_confidence"] = self.combined_confidence
        return result


class EvidenceGraph:
    """Small dependency-free evidence graph suitable for API/database adapters."""

    def __init__(self) -> None:
        self._nodes: dict[str, EvidenceNode] = {}
        self._field_index: dict[str, list[str]] = {}

    def add(self, evidence: EvidenceNode) -> EvidenceNode:
        self._nodes[evidence.evidence_id] = evidence
        self._field_index.setdefault(evidence.field, []).append(evidence.evidence_id)
        return evidence

    def get(self, evidence_id: str) -> EvidenceNode:
        return self._nodes[evidence_id]

    def for_field(self, field_name: str) -> list[EvidenceNode]:
        return [self._nodes[i] for i in self._field_index.get(field_name, [])]

    def verify(self, evidence_id: str, approved: bool) -> EvidenceNode:
        evidence = self.get(evidence_id)
        evidence.human_verification = "APPROVED" if approved else "REJECTED"
        return evidence

    def validate(self, evidence_id: str, passed: bool) -> EvidenceNode:
        evidence = self.get(evidence_id)
        evidence.validation = "PASS" if passed else "FAIL"
        return evidence

    def search(self, query: str) -> list[EvidenceNode]:
        query = query.lower().strip()
        return [
            node for node in self._nodes.values()
            if query in node.field.lower()
            or query in str(node.value).lower()
            or query in node.location.document_name.lower()
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [node.to_dict() for node in self._nodes.values()],
            "fields": {
                key: list(ids) for key, ids in self._field_index.items()
            },
        }


def evidence_from_extraction(
    *,
    field: str,
    value: Any,
    document_id: str,
    document_name: str,
    page: int,
    region_id: str,
    bbox: list[float],
    ocr_confidence: float | None = None,
    ner_confidence: float | None = None,
    source_text: str | None = None,
    extraction_model: str | None = None,
) -> EvidenceNode:
    return EvidenceNode(
        field=field,
        value=value,
        location=EvidenceLocation(
            document_id=document_id,
            document_name=document_name,
            page=page,
            region_id=region_id,
            bbox=bbox,
        ),
        ocr_confidence=ocr_confidence,
        ner_confidence=ner_confidence,
        source_text=source_text,
        extraction_model=extraction_model,
    )
