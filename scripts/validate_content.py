#!/usr/bin/env python3
"""Valida o contrato editorial do conteúdo público da disciplina."""

import argparse
import re
import sys
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown.extensions.toc import slugify


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

MODULES = {
    "modulo-1-visao-geral": "Visão geral de estilos",
    "modulo-2-apis": "Arquitetura de APIs",
    "modulo-3-servicos": "Arquitetura de Serviços",
    "modulo-4-governanca": "Governança de Serviços",
    "modulo-5-eventos": "Arquiteturas de Eventos",
    "modulo-6-nuvem": "Arquiteturas de Nuvens",
}

PAGES = (
    "index.md",
    "conceitos.md",
    "padroes-e-decisoes.md",
    "exemplo-arquitetural.md",
    "estudo-de-caso.md",
    "oficina-de-ferramentas.md",
    "exercicios.md",
    "sintese-e-referencias.md",
)

BLOOM = ("Recordar", "Compreender", "Aplicar", "Analisar", "Avaliar", "Criar")

_PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|PLACEHOLDER|PREENCHER)\b", re.IGNORECASE)
_ASSESSMENT_VOCABULARY = re.compile(
    r"\brubricas?\b|\bpontua(?:ção|cao)\b|\bpontos?\b", re.IGNORECASE
)
_ACCESS_CLASSIFICATION = re.compile(
    r"\b(?:cart(?:ão|ao)|cr[eé]dito|cobran(?:ça|ca))\b"
)
_ACCESS_CONTEXT = re.compile(
    r"\b(?:acesso|assinatura|cadastro|conta|ferramenta|pagamento|plano|uso|usar)\w*\b"
)
_MARKDOWN_LINK = re.compile(
    r"(?P<image>!)?\[(?P<label>[^\]]*)\]"
    r"\((?P<target><[^>]+>|[^\s)]+)(?:\s+[\"'][^\"']*[\"'])?\)"
)
_HEADING = re.compile(r"^#{1,6}[ \t]+(?P<title>.+?)[ \t]*#*[ \t]*$", re.MULTILINE)
_EXPLICIT_ANCHOR = re.compile(r"\{[ \t]*#(?P<anchor>[A-Za-z][\w:.-]*)[^}]*\}")
_TEXTUAL_EQUIVALENT = "**Leitura textual da figura:**"
_PROCEDURAL_LABEL = re.compile(
    r"^[ \t]*(?:[-*+]|\d+\.)?[ \t]*\*\*(?:"
    r"Objetivo|Pré-requisitos?|Execute|Observe|Compare|Situação|Seu papel|"
    r"Insumos disponíveis|Como conduzir|Entrega esperada|Critérios de avaliação|"
    r"Resultado esperado|Evidência a entregar"
    r"):?[ \t]*\*\*(?P<tail>.*)$",
    re.IGNORECASE,
)
_ADVANCED_MARKERS = (
    "**Situação**",
    "**Seu papel**",
    "**Insumos disponíveis**",
    "**Como conduzir**",
    "**Entrega esperada**",
    "**Critérios de avaliação**",
)
_ANSWER_BLOCK = re.compile(
    r"^(?:#{1,6}[ \t]+|\*\*|!!![ \t]+\w+[ \t]+[\"']?|"
    r"\?\?\?[ \t]+\w+[ \t]+[\"']?|<summary>)"
    r"(?:resposta|gabarito|solução esperada)\b",
    re.IGNORECASE | re.MULTILINE,
)
_TABLE = re.compile(r"(?:^[ \t]*\|.*\|[ \t]*(?:\n|$)){2,}", re.MULTILINE)
_PERCENTAGE = re.compile(r"(?<!\w)(\d+(?:[.,]\d+)?)[ \t]*%")
_WORD = re.compile(r"\b[^\W_]+(?:[-'][^\W_]+)*\b", re.UNICODE)


def bloom_sections(text: str) -> dict[str, str]:
    """Retorna o conteúdo delimitado pelos títulos de segundo nível de Bloom."""

    levels = "|".join(map(re.escape, BLOOM))
    heading = re.compile(
        rf"^##[ \t]+(?P<level>{levels})[ \t]*#*[ \t]*$", re.MULTILINE
    )
    matches = list(heading.finditer(text))
    return {
        match.group("level"): text[
            match.end() : matches[index + 1].start()
            if index + 1 < len(matches)
            else len(text)
        ].strip()
        for index, match in enumerate(matches)
    }


def _location(path: Path, docs_root: Path) -> str:
    try:
        return path.relative_to(docs_root).as_posix()
    except ValueError:
        return path.as_posix()


def _anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for match in _HEADING.finditer(text):
        title = match.group("title")
        explicit = _EXPLICIT_ANCHOR.search(title)
        if explicit:
            anchors.add(explicit.group("anchor"))
            title = _EXPLICIT_ANCHOR.sub("", title)
        title = re.sub(r"[*_`~\[\]]", "", title).strip()
        base = slugify(title, "-")
        occurrence = counts.get(base, 0)
        counts[base] = occurrence + 1
        anchors.add(base if occurrence == 0 else f"{base}_{occurrence}")
    return anchors


def _local_target(source: Path, docs_root: Path, target: str) -> tuple[Path, str]:
    target = target[1:-1] if target.startswith("<") and target.endswith(">") else target
    parsed = urlsplit(unquote(target))
    raw_path = parsed.path
    if not raw_path:
        destination = source
    elif raw_path.startswith("/"):
        destination = docs_root / raw_path.lstrip("/")
    else:
        destination = source.parent / raw_path
    if destination.is_dir():
        destination /= "index.md"
    return destination.resolve(), parsed.fragment


def _validate_links_and_figures(path: Path, docs_root: Path, text: str) -> list[str]:
    location = _location(path, docs_root)
    errors: list[str] = []
    matches = list(_MARKDOWN_LINK.finditer(text))
    image_matches = [match for match in matches if match.group("image")]
    for match in matches:
        raw_target = match.group("target")
        target = raw_target[1:-1] if raw_target.startswith("<") else raw_target
        parsed = urlsplit(unquote(target))
        if parsed.scheme or target.startswith("//"):
            continue
        destination, fragment = _local_target(path, docs_root, raw_target)
        if not destination.is_file():
            errors.append(f"{location}: arquivo local ausente: {target}")
        elif fragment and destination.suffix.casefold() in {".md", ".markdown"}:
            destination_text = destination.read_text(encoding="utf-8")
            if fragment not in _anchors(destination_text):
                errors.append(f"{location}: âncora local ausente: {target}")
        if match.group("image") and not match.group("label").strip():
            errors.append(f"{location}: imagem sem texto alternativo: {target}")

    for index, match in enumerate(image_matches):
        end = image_matches[index + 1].start() if index + 1 < len(image_matches) else len(text)
        following = text[match.end() : end]
        next_section = re.search(r"^##[ \t]", following, re.MULTILINE)
        if next_section:
            following = following[: next_section.start()]
        if _TEXTUAL_EQUIVALENT not in following:
            target = match.group("target")
            errors.append(f"{location}: figura sem leitura textual: {target}")
    return errors


def _validate_procedural_labels(path: Path, docs_root: Path, text: str) -> list[str]:
    if path.name not in {"oficina-de-ferramentas.md", "exercicios.md"} and not any(
        part.casefold() in {"laboratorio", "laboratorios", "laboratórios"}
        for part in path.parts
    ):
        return []
    location = _location(path, docs_root)
    lines = text.splitlines()
    errors: list[str] = []
    for index, line in enumerate(lines):
        match = _PROCEDURAL_LABEL.match(line)
        if not match:
            continue
        followed_by_blank = index + 1 < len(lines) and not lines[index + 1].strip()
        if match.group("tail").strip() or not followed_by_blank:
            errors.append(
                f"{location}:{index + 1}: rótulo procedimental aglutinado; "
                "termine o parágrafo e insira uma linha em branco"
            )
    return errors


def _percentage_errors(text: str, location: str, context: str = "") -> list[str]:
    errors: list[str] = []
    for instrument, table in enumerate(_TABLE.finditer(text), start=1):
        values = [
            Decimal(value.replace(",", "."))
            for value in _PERCENTAGE.findall(table.group(0))
        ]
        if not values:
            continue
        total = sum(values, Decimal(0))
        if total != Decimal(100):
            rendered = format(total.normalize(), "f")
            prefix = f"{context}: " if context else ""
            errors.append(
                f"{location}: {prefix}percentuais do instrumento somam {rendered}% "
                f"(instrumento {instrument}; esperado: 100%)"
            )
    return errors


def _word_count(text: str) -> int:
    without_code = re.sub(r"```.*?```|~~~.*?~~~", " ", text, flags=re.DOTALL)
    without_links = re.sub(r"https?://\S+", " ", without_code)
    return len(_WORD.findall(without_links))


def _validate_exercises(path: Path, docs_root: Path) -> list[str]:
    location = _location(path, docs_root)
    text = path.read_text(encoding="utf-8")
    sections = bloom_sections(text)
    errors: list[str] = []
    for level in BLOOM:
        occurrences = len(
            re.findall(
                rf"^##[ \t]+{re.escape(level)}[ \t]*#*[ \t]*$",
                text,
                re.MULTILINE,
            )
        )
        if occurrences == 0:
            errors.append(f"{location}: seção Bloom ausente: {level}")
        elif occurrences > 1:
            errors.append(f"{location}: seção Bloom duplicada: {level}")
    for level, section in sections.items():
        if level not in {"Recordar", "Compreender"} and _ANSWER_BLOCK.search(section):
            errors.append(
                f"{location}: {level}: bloco de resposta fora de Recordar/Compreender"
            )
    for level in ("Aplicar", "Analisar", "Avaliar"):
        section = sections.get(level, "")
        for marker in _ADVANCED_MARKERS:
            if marker not in section:
                errors.append(
                    f"{location}: {level}: marcador obrigatório ausente: {marker}"
                )
        errors.extend(_percentage_errors(section, location, level))
        if section and not _PERCENTAGE.search(section):
            errors.append(f"{location}: {level}: critérios sem percentuais")
    return errors


def validate_document(path: Path, docs_root: Path) -> list[str]:
    """Valida regras editoriais aplicáveis a um documento Markdown público."""

    text = path.read_text(encoding="utf-8")
    location = _location(path, docs_root)
    errors: list[str] = []
    if _PLACEHOLDER.search(text):
        errors.append(f"{location}: marcador provisório")
    if _ASSESSMENT_VOCABULARY.search(text):
        errors.append(f"{location}: vocabulário público proibido")
    folded = text.casefold()
    for block in re.split(r"\n[ \t]*\n", folded):
        if _ACCESS_CLASSIFICATION.search(block) and _ACCESS_CONTEXT.search(block):
            errors.append(
                f"{location}: classificação de acesso com linguagem comercial"
            )
    errors.extend(_validate_links_and_figures(path, docs_root, text))
    errors.extend(_validate_procedural_labels(path, docs_root, text))
    if path.name != "exercicios.md":
        errors.extend(_percentage_errors(text, location))
    return errors


def validate_module(slug: str, docs_root: Path) -> list[str]:
    """Valida um módulo completo, inclusive exercícios e extensão editorial."""

    module = docs_root / slug
    errors: list[str] = []
    if slug not in MODULES:
        return [f"módulo desconhecido: {slug}"]
    texts: list[str] = []
    for page_name in PAGES:
        path = module / page_name
        if not path.is_file():
            errors.append(f"{slug}/{page_name}: arquivo obrigatório ausente")
            continue
        text = path.read_text(encoding="utf-8")
        texts.append(text)
        errors.extend(validate_document(path, docs_root))
        if page_name == "exercicios.md":
            errors.extend(_validate_exercises(path, docs_root))
    count = _word_count("\n".join(texts))
    if not 5_000 <= count <= 8_500:
        errors.append(
            f"{slug}: fora da faixa de 5.000–8.500 palavras ({count} palavras)"
        )
    return errors


def validate_all(docs_root: Path) -> list[str]:
    """Valida todas as páginas públicas e os limites globais de extensão."""

    errors: list[str] = []
    for path in sorted(docs_root.rglob("*.md")):
        relative_parts = path.relative_to(docs_root).parts
        if "superpowers" in relative_parts:
            continue
        if relative_parts and relative_parts[0] in MODULES:
            continue
        errors.extend(validate_document(path, docs_root))

    module_texts: list[str] = []
    for slug in MODULES:
        errors.extend(validate_module(slug, docs_root))
        for page_name in PAGES:
            page = docs_root / slug / page_name
            if page.is_file():
                module_texts.append(page.read_text(encoding="utf-8"))
    total = _word_count("\n".join(module_texts))
    if not 32_000 <= total <= 51_000:
        errors.append(
            "curso: fora da faixa de 32.000–51.000 palavras nos módulos "
            f"({total} palavras)"
        )
    return errors


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--module", choices=tuple(MODULES), metavar="SLUG")
    selection.add_argument("--all", action="store_true", dest="validate_all")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    errors = (
        validate_all(DOCS)
        if args.validate_all
        else validate_module(args.module, DOCS)
    )
    if errors:
        for error in errors:
            print(f"ERRO: {error}", file=sys.stderr)
        return 1
    print("Validação concluída sem erros")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
