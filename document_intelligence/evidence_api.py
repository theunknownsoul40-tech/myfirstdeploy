from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .evidence import EvidenceGraph, EvidenceNode


def evidence_response(graph: EvidenceGraph, field_name: str) -> dict[str, Any]:
    """API-ready payload for the UI's 'Show Evidence' action."""
    items = graph.for_field(field_name)
    return {
        "field": field_name,
        "count": len(items),
        "evidence": [item.to_dict() for item in items],
    }


def highlight_payload(evidence: EvidenceNode) -> dict[str, Any]:
    """Coordinates required to open the source page and highlight the evidence."""
    return {
        "document_id": evidence.location.document_id,
        "document_name": evidence.location.document_name,
        "page": evidence.location.page,
        "region_id": evidence.location.region_id,
        "bbox": evidence.location.bbox,
        "evidence_id": evidence.evidence_id,
    }
