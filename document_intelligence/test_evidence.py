from .evidence import EvidenceGraph, evidence_from_extraction


def test_evidence_lifecycle_and_location():
    graph = EvidenceGraph()
    node = graph.add(evidence_from_extraction(
        field="owner",
        value="Ramesh Kumar",
        document_id="LR-1842",
        document_name="LR_1842.pdf",
        page=3,
        region_id="B4",
        bbox=[100, 200, 420, 260],
        ocr_confidence=0.96,
        ner_confidence=0.91,
        source_text="Ramesh Kumar",
        extraction_model="land-record-ner-v1",
    ))

    assert node.combined_confidence == 0.935
    assert graph.for_field("owner")[0].value == "Ramesh Kumar"

    graph.validate(node.evidence_id, True)
    graph.verify(node.evidence_id, True)

    assert node.validation == "PASS"
    assert node.human_verification == "APPROVED"
    assert node.location.page == 3
    assert node.location.region_id == "B4"
    assert node.location.bbox == [100, 200, 420, 260]


def test_search_finds_value_and_document():
    graph = EvidenceGraph()
    graph.add(evidence_from_extraction(
        field="owner",
        value="Ramesh Kumar",
        document_id="LR-1842",
        document_name="LR_1842.pdf",
        page=3,
        region_id="B4",
        bbox=[0, 0, 1, 1],
    ))

    assert len(graph.search("Ramesh")) == 1
    assert len(graph.search("LR_1842")) == 1
