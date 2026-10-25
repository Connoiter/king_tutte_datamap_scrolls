"""Format a document the way EmbeddingGemma 2 expects for documents.

Model card (google/embeddinggemma-2, "Task Instruction Prefixes"):
documents with a real title are `title: {title} | text: {content}`;
use `title: none` when no title is available.
"""


def format_document(text: str, title: str | None = None) -> str:
    title = (title or "").strip() or "none"
    return f"title: {title} | text: {text}"
