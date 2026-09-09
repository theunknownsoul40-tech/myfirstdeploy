from __future__ import annotations

from typing import Any

from .models import ExtractedField, LayoutRegion, Provenance


class LayoutDetector:
    """Adapter boundary for LayoutLMv3/Table Transformer.

    Production inference can be injected without changing the pipeline API.
    """

    model_name = "layoutlmv3/table-transformer"

    def detect(self, page_image: str, page: int = 1) -> list[LayoutRegion]:
        # TODO: load trained layout model and return detected regions.
        return []


class OCRBackend:
    """Adapter boundary for PaddleOCR + TrOCR/Sarvam HTR."""

    model_name = "paddleocr-trocr"

    def extract(self, image_path: str, page: int = 1) -> list[Provenance]:
        # TODO: wire model inference. Returning an empty list is intentional:
        # fake OCR must never be presented as extracted land-record evidence.
        return []


class LandRecordExtractor:
    """Schema mapper for OCR/NER output with provenance preserved."""

    FIELD_ALIASES = {
        "owner": "owner",
        "owner_name": "owner",
        "survey": "survey_no",
        "survey_no": "survey_no",
        "khata": "khata_no",
        "khata_no": "khata_no",
        "area": "area",
        "village": "village",
        "tehsil": "tehsil",
        "district": "district",
        "land_class": "land_class",
        "mutation": "mutation_id",
        "mutation_id": "mutation_id",
    }

    def extract(self, entities: list[dict[str, Any]]) -> list[ExtractedField]:
        fields: list[ExtractedField] = []
        for entity in entities:
            raw_name = str(entity.get("label", entity.get("name", ""))).lower()
            name = self.FIELD_ALIASES.get(raw_name)
            if not name:
                continue
            provenance = Provenance(
                page=int(entity.get("page", 1)),
                bbox=entity.get("bbox"),
                model=str(entity.get("model", "land-record-ner")),
                confidence=float(entity.get("confidence", 0.0)),
                source_image=str(entity.get("source_image", "")),
                value=None if entity.get("value") is None else str(entity["value"]),
                language=entity.get("language"),
                script=entity.get("script"),
            )
            fields.append(ExtractedField(name=name, value=entity.get("value"),
                                         confidence=provenance.confidence,
                                         provenance=provenance))
        return fields
