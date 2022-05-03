from typing import Tuple

from markdownify import markdownify
from readability import Document


def html_to_flat_markdown(html: str) -> Tuple[str, str]:
    doc = Document(html)
    title = doc.title()
    md = markdownify(doc.summary())
    return title, md
