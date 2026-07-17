"""MkDocs hook that adds course-specific semantic classes to rendered HTML."""

from __future__ import annotations

import re


_CLASS_ATTRIBUTE = re.compile(r"\bclass=(?P<quote>['\"])(?P<classes>.*?)(?P=quote)", re.IGNORECASE)


def _add_class(tag: str, class_name: str) -> str:
    """Add ``class_name`` to an opening tag without discarding existing classes."""
    class_attribute = _CLASS_ATTRIBUTE.search(tag)
    if class_attribute:
        classes = class_attribute.group("classes").split()
        if class_name in classes:
            return tag
        classes.append(class_name)
        quote = class_attribute.group("quote")
        replacement = f"class={quote}{' '.join(classes)}{quote}"
        return _CLASS_ATTRIBUTE.sub(replacement, tag, count=1)

    return f'{tag[:-1]} class="{class_name}">'


def _class_tags(html: str, pattern: str, class_name: str) -> str:
    return re.sub(
        pattern,
        lambda match: _add_class(match.group(0), class_name),
        html,
        flags=re.IGNORECASE,
    )


def on_page_content(html: str, **_kwargs: object) -> str:
    """Enrich rendered course content with stable, accessible component classes."""
    html = _class_tags(html, r"<h1(?:\s[^>]*)?>", "module-opening")
    html = _class_tags(html, r"<table(?:\s[^>]*)?>", "comparison-table")
    html = _class_tags(
        html,
        r'<h2\b[^>]*\bid="(?:recordar|compreender|aplicar|analisar|avaliar|criar)"[^>]*>',
        "bloom-label",
    )
    html = _class_tags(
        html,
        r"<p(?:\s[^>]*)?>(?=\s*<strong>Critérios de avaliação)",
        "criteria",
    )
    return html
