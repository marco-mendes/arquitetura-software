from pathlib import Path
import re

import yaml

from scripts.validate_content import PAGES, bloom_sections


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def _nav_paths(node) -> tuple[str, ...]:
    if isinstance(node, str):
        return (node,)
    if isinstance(node, list):
        return tuple(path for item in node for path in _nav_paths(item))
    if isinstance(node, dict):
        return tuple(path for item in node.values() for path in _nav_paths(item))
    return ()


def navigation_section_paths(title: str) -> tuple[str, ...]:
    """Retorna caminhos da seção MkDocs pelo YAML, sem depender de recortes de texto."""

    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    for item in config["nav"]:
        if isinstance(item, dict) and title in item:
            return _nav_paths(item[title])
    raise AssertionError(f"Seção de navegação ausente: {title}")


def assert_module_contract(
    testcase, slug: str, required_terms: tuple[str, ...]
) -> None:
    module = DOCS / slug
    navigation = _nav_paths(
        yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))["nav"]
    )
    for page in PAGES:
        testcase.assertTrue((module / page).is_file(), f"{slug}/{page}")
        testcase.assertIn(f"{slug}/{page}", navigation)
    corpus = "\n".join(
        (module / page).read_text(encoding="utf-8") for page in PAGES
    )
    testcase.assertIn("## Equivalências em Java e .NET", corpus)
    for term in required_terms:
        testcase.assertIn(term.casefold(), corpus.casefold(), term)
    workshop = (module / "oficina-de-ferramentas.md").read_text(encoding="utf-8")
    for heading in (
        "## Ferramenta",
        "## Pré-requisitos",
        "## Instalação",
        "## Preparação do laboratório",
        "## Execução",
        "## Resultado esperado",
        "## Interpretação",
        "## Limpeza e contingência",
        "## Evidência a entregar",
    ):
        testcase.assertIn(heading, workshop)
    for platform in ("### Windows", "### macOS", "### Linux"):
        testcase.assertIn(platform, workshop)
    for label in ("Essencial em aula", "Exploração em dupla", "Extensão"):
        testcase.assertIn(label, workshop)
    for prompt in (
        "**Objetivo**",
        "**Pré-requisito**",
        "**Execute**",
        "**Observe**",
        "**Compare**",
        "Questões exploratórias",
    ):
        testcase.assertIn(prompt, workshop)
    exercises = (module / "exercicios.md").read_text(encoding="utf-8")
    sections = bloom_sections(exercises)
    testcase.assertEqual(
        {"Recordar", "Compreender", "Aplicar", "Analisar", "Avaliar", "Criar"},
        set(sections),
    )
    legacy_markers = (
        "**Situação**",
        "**Seu papel**",
        "**Insumos disponíveis**",
        "**Como conduzir**",
        "**Entrega esperada**",
        "**Critérios de avaliação**",
    )
    self_contained_markers = (
        "**Objetivo**",
        "**Situação**",
        "**Seu papel**",
        "**Artefato que você irá usar**",
        "**Antes de executar**",
        "**O que fazer**",
        "**Evidência esperada**",
        "**Entrega esperada**",
        "**Critérios de avaliação**",
    )
    for level in ("Aplicar", "Analisar", "Avaliar"):
        markers = (
            self_contained_markers
            if all(marker in sections[level] for marker in self_contained_markers)
            else legacy_markers
        )
        for marker in markers:
            testcase.assertIn(marker, sections[level])
        testcase.assertRegex(sections[level], r"\|[^\n]*\|\s*\d+%\s*\|")
