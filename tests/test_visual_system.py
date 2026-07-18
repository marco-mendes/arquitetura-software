from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AcademiaVisualSystemTest(unittest.TestCase):
    def test_tokens_typography_and_components(self):
        css = (ROOT / "docs/assets/stylesheets/extra.css").read_text(encoding="utf-8")
        for value in ("#16243A", "#254DB8", "#5FC0D1", "#F2F6FB", "#FFFFFF", "#F2B84B"):
            self.assertIn(value, css)
        for value in ("Charter", "Georgia", "Inter", "Segoe UI", "IBM Plex Mono", "Consolas"):
            self.assertIn(value, css)
        for selector in (
            ".module-opening",
            ".objective-card",
            ".decision-callout",
            ".risk-callout",
            ".bloom-label",
            ".architecture-figure",
            ".comparison-table",
            ".adr-block",
            ".criteria",
        ):
            self.assertIn(selector, css)

    def test_accessibility_rules(self):
        css = (ROOT / "docs/assets/stylesheets/extra.css").read_text(encoding="utf-8")
        for marker in (":focus-visible", "prefers-reduced-motion", "overflow-x: auto", "max-width: 100%"):
            self.assertIn(marker, css)
        self.assertNotIn("outline: none", css)

    def test_public_mermaid_render_is_responsive_in_material_content(self):
        css = (ROOT / "docs/assets/stylesheets/extra.css").read_text(encoding="utf-8")

        self.assertRegex(css, r"\.md-typeset\s+\.mermaid\s*\{")
        self.assertRegex(
            css,
            r"\.md-typeset\s+\.mermaid\s*>\s*svg\s*\{[^}]*max-width:\s*100%[^}]*height:\s*auto",
        )
        self.assertRegex(
            css,
            r"\.md-typeset\s+\.mermaid\s*\{[^}]*overflow-x:\s*auto",
        )

    def test_semantic_hook_exposes_expected_interface(self):
        from course_semantics import on_page_content

        html = on_page_content("<h1>Título</h1><table><tr><td>x</td></tr></table>")
        self.assertIn("module-opening", html)
        self.assertIn("comparison-table", html)

    def test_semantic_hook_does_not_treat_data_class_as_class(self):
        from course_semantics import on_page_content

        html = on_page_content('<h1 data-class="legacy">Título</h1>')
        self.assertIn('data-class="legacy"', html)
        self.assertIn(' class="module-opening"', html)


class VisualSystemTest(unittest.TestCase):
    def test_right_toc_can_be_collapsed_accessibly_on_desktop(self):
        navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        css = (ROOT / "docs/assets/stylesheets/extra.css").read_text(encoding="utf-8")
        script = (ROOT / "docs/assets/javascripts/toc-toggle.mjs").read_text(
            encoding="utf-8"
        )

        self.assertIn("assets/javascripts/toc-toggle.mjs", navigation)
        self.assertIn("html.toc-collapsed .md-sidebar--secondary", css)
        self.assertIn("@media (min-width: 76.25em)", css)
        self.assertRegex(
            css,
            r"\.academia-toc-toggle\s*\{[^}]*display:\s*none;",
        )
        self.assertRegex(
            css,
            r"(?s)@media \(min-width: 76\.25em\)\s*\{.*?\.academia-toc-toggle\s*\{[^}]*display:\s*inline-flex;[^}]*position:\s*fixed;",
        )
        self.assertNotRegex(
            css,
            r"html\.toc-collapsed \.academia-toc-toggle\s*\{[^}]*position:\s*fixed;",
        )
        self.assertIn("academia-toc-toggle", script)
        self.assertIn('querySelector(".md-content")', script)
        self.assertIn('matchMedia("(min-width: 76.25em)")', script)
        self.assertIn("aria-expanded", script)
        self.assertIn("localStorage", script)
        self.assertIn("document$.subscribe", script)
        self.assertNotIn("html.toc-collapsed .md-grid", css)
