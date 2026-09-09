# Phase 2 — Document Intelligence

This package implements the land-record document intelligence foundation:

1. Scan quality assessment
2. Conditional image restoration (deskew, border crop, denoise, Sauvola, CLAHE)
3. Optional Real-ESRGAN super-resolution
4. Layout detection adapter for LayoutLMv3/Table Transformer
5. OCR/HTR adapter boundary for PaddleOCR/TrOCR/Sarvam
6. Provenance-aware land-record field extraction
7. Jurisdiction-aware area normalization while preserving original values

## Quick start

```python
from document_intelligence import DocumentIntelligencePipeline

pipeline = DocumentIntelligencePipeline()
result = pipeline.process(
    "data/scan.jpg",
    output_dir="artifacts",
    jurisdiction="Maharashtra",
    super_resolution=False,
)
print(result.to_dict())
```

Model adapters intentionally return no fabricated OCR/layout data until real model inference is configured. This keeps the system auditable and prevents placeholder text from becoming land-record evidence.
