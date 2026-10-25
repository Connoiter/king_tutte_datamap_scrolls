"""Document format EmbeddingGemma 2 expects (model card, "Task Instruction Prefixes")."""

from embedding_format import format_document


def test_titled_document_combines_title_and_text():
    assert (
        format_document("We study graphs.", title="Graph Neural Nets")
        == "title: Graph Neural Nets | text: We study graphs."
    )


def test_untitled_document_uses_title_none():
    # Matches the model's own "Document" prompt: "title: none | text: "
    assert format_document("We study graphs.") == "title: none | text: We study graphs."


def test_blank_title_counts_as_no_title():
    assert format_document("We study graphs.", title="  ") == "title: none | text: We study graphs."
