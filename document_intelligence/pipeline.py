from __future__ import annotations

from pathlib import Path
from typing import Any

from .extraction import LandRecordExtractor, LayoutDetector, OCRBackend
from .models import DocumentResult
from .normalization import normalize_area
from .quality import assess_quality
from .restoration import restore_image


class DocumentIntelligencePipeline:
    """Phase 2 orchestration: quality -> restoration -> layout -> OCR/HTR -> IE -> normalization."""

    def __init__(self, layout=None, ocr=None, extractor=None):
        self.layout = layout or LayoutDetector()
        self.ocr = ocr or OCRBackend()
        self.extractor = extractor or LandRecordExtractor()

    def process(self, input_path: str | Path, output_dir: str | Path = "artifacts",
                jurisdiction: str | None = None, super_resolution: bool = False,
                entities: list[dict[str, Any]] | None = None) -> DocumentResult:
        input_path = Path(input_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        quality = assess_quality(input_path)
        clean_path = output_dir / f"{input_path.stem}.clean.png"
        restore_image(input_path, clean_path, quality,
                      use_super_resolution=super_resolution)

        regions = self.layout.detect(str(clean_path), page=1)
        ocr_items = self.ocr.extract(str(clean_path), page=1)
        fields = self.extractor.extract(entities or [])

        normalized = None
        area_field = next((f for f in fields if f.name == "area" and f.value), None)
        if area_field:
            area_text = str(area_field.value)
            try:
                normalized_data = normalize_area(area_text, jurisdiction)
                from .models import NormalizedArea
                normalized = NormalizedArea(**{k: normalized_data[k] for k in NormalizedArea.__dataclass_fields__})
            except ValueError:
                normalized = None

        return DocumentResult(
            quality=quality,
            regions=regions,
            fields=fields,
            normalized_area=normalized,
            artifacts={"original": str(input_path), "clean": str(clean_path),
                       "ocr_items": str(len(ocr_items))},
        )
