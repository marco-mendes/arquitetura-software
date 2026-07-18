#!/usr/bin/env python3
"""Valida o contrato editorial do conteúdo público da disciplina."""

import argparse
import re
import sys
from dataclasses import dataclass
from decimal import Decimal
from html import unescape
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
    r"\b(?:acesso|assinatura|cadastro|conta|pagamento)\w*\b"
)
_TOOL_ACCESS_HEADING = re.compile(
    r"\b(?:acesso|ferramentas?|instala(?:ção|cao))\b"
)
_PREREQUISITE_HEADING = re.compile(r"\bpr[eé]-?requisitos?\b")
_TOOL_REQUIREMENT = re.compile(
    r"\bferramenta\b.{0,80}\b(?:exige|requer|depende|necessita|solicita)\w*\b",
    re.DOTALL,
)
_COMMERCIAL_REQUIREMENT = re.compile(
    r"\b(?:cart(?:ão|ao)|cr[eé]dito|cobran(?:ça|ca))\b.{0,80}"
    r"\b(?:para|ao)\s+(?:acessar|instalar|cadastrar|usar)\w*\b",
    re.DOTALL,
)
_MARKDOWN_LINK = re.compile(
    r"(?P<image>!)?\[(?P<label>[^\]]*)\]"
    r"\((?P<target><[^>]+>|[^\s)]+)(?:\s+[\"'][^\"']*[\"'])?\)"
)
_REFERENCE_LINK = re.compile(
    r"(?P<image>!)?\[(?P<label>[^\]]+)\]\[(?P<reference>[^\]]*)\]"
)
_SHORTCUT_REFERENCE = re.compile(
    r"(?P<image>!)?\[(?P<label>[^\]\n]+)\](?![\[(])"
)
_REFERENCE_DEFINITION = re.compile(
    r"^[ \t]{0,3}\[(?P<reference>[^\]]+)\]:[ \t]*"
    r"(?P<target><[^>]+>|\S+)(?:[ \t]+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?[ \t]*$",
    re.MULTILINE,
)
_HTML_RESOURCE = re.compile(r"<(?P<tag>a|img)\b[^>]*>", re.IGNORECASE)
_HTML_ATTRIBUTE = re.compile(
    r"\b(?P<name>href|src|alt)[ \t]*=[ \t]*"
    r"(?:\"(?P<double>[^\"]*)\"|'(?P<single>[^']*)'|(?P<bare>[^\s>]+))",
    re.IGNORECASE,
)
_HEADING = re.compile(r"^#{1,6}[ \t]+(?P<title>.+?)[ \t]*#*[ \t]*$", re.MULTILINE)
_EXPLICIT_ANCHOR = re.compile(r"\{[ \t]*#(?P<anchor>[A-Za-z][\w:.-]*)[^}]*\}")
_TEXTUAL_EQUIVALENT = "**Leitura textual da figura:**"
_FIGURE_CAPTION = re.compile(
    r"^(?:\*(?:Figura|Fonte)\b[^\n]*\*|_(?:Figura|Fonte)\b[^\n]*_|"
    r"<figcaption\b[^>]*>.*?</figcaption>)",
    re.IGNORECASE | re.DOTALL,
)
_PROCEDURAL_LABEL = re.compile(
    r"^[ \t]*(?:(?:[-*+]|\d+\.)[ \t]+)?"
    r"\*\*(?P<label>[^*\n]+)\*\*(?P<tail>.*)$"
)
_SELF_CONTAINED_LABELS = (
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
_ACTIVITY_PATH = re.compile(
    r"(?:<raiz-do-clone>/|(?:\.\.?/|[A-Za-z0-9_.-]+/)[A-Za-z0-9_./-]+)"
)
_ACTIVITY_INITIAL_STATE = re.compile(
    r"\b(?:estado|inicial|existe|parad[oa]s?|confirm\w*|verifi\w*|"
    r"instalad[oa]s?)\b",
    re.IGNORECASE,
)
_ACTIVITY_ACTION = re.compile(r"(?m)^\s*(?:\d+\.|[-*+])\s+\S+")
_ACTIVITY_EVIDENCE = re.compile(
    r"\b(?:sa[ií]da|resposta|status|registro|arquivo|resultado|observ\w*|"
    r"mensagem|teste|log|m[eé]trica|tabela|diagrama|parecer|cadeia|pol[ií]tica|"
    r"artefato|linha)\b",
    re.IGNORECASE,
)
_ACTIVITY_CONTINGENCY = re.compile(
    r"\b(?:se|caso|conting[êe]ncia|falha|erro|indispon\w*|"
    r"n[aã]o\s+funcion\w*|retorn\w*)\b",
    re.IGNORECASE,
)
_ANSWER_BLOCK = re.compile(
    r"^(?:#{1,6}[ \t]+|\*\*|!!![ \t]+\w+[ \t]+[\"']?|"
    r"\?\?\?[ \t]+\w+[ \t]+[\"']?|<summary>)"
    r"(?:resposta|gabarito|solução esperada)\b",
    re.IGNORECASE | re.MULTILINE,
)
_TABLE = re.compile(r"(?:^[ \t]*\|.*\|[ \t]*(?:\n|$)){2,}", re.MULTILINE)
_LIST_ITEM = re.compile(r"^[ \t]*(?:[-*+]|\d+\.)[ \t]+.*$", re.MULTILINE)
_PERCENTAGE = re.compile(r"(?<!\w)(\d+(?:[.,]\d+)?)[ \t]*%")
_CRITERIA_LABEL = re.compile(
    r"^[ \t]*\*\*Critérios de avaliação:?\*\*[ \t]*$",
    re.IGNORECASE | re.MULTILINE,
)
_BOLD_LABEL = re.compile(r"^[ \t]*\*\*[^*\n]+\*\*[ \t]*$", re.MULTILINE)
_WORD = re.compile(r"\b[^\W_]+(?:[-'][^\W_]+)*\b", re.UNICODE)


@dataclass(frozen=True)
class _Resource:
    kind: str
    target: str | None
    label: str
    start: int
    end: int
    reference: str | None = None


def bloom_sections(text: str) -> dict[str, str]:
    """Retorna seções Bloom, ignorando títulos presentes em exemplos cercados."""

    text = _mask_fenced_code(text)
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


def expandable_feedback_errors(text: str, location: str) -> list[str]:
    """Exige uma resposta expansível para cada pergunta inicial de Bloom."""

    errors: list[str] = []
    for level in ("Recordar", "Compreender"):
        section = bloom_sections(text).get(level, "")
        items = re.split(r"(?m)(?=^\d+\.\s)", section)
        for item in (item for item in items if re.match(r"^\d+\.\s", item)):
            if not re.search(
                r"<details>\s*<summary>Ver resposta</summary>.*?</details>",
                item,
                re.DOTALL,
            ):
                errors.append(
                    f"{location}: {level}: pergunta sem resposta expansível"
                )
    return errors


def self_contained_activity_errors(text: str, location: str) -> list[str]:
    """Exige o roteiro contextual completo nas atividades avançadas de Bloom."""

    errors: list[str] = []
    for level in ("Aplicar", "Analisar", "Avaliar", "Criar"):
        section = bloom_sections(text).get(level, "")
        if not section:
            continue
        previous = -1
        positions: dict[str, int] = {}
        for label in _SELF_CONTAINED_LABELS:
            current = section.find(label)
            if current == -1:
                errors.append(
                    f"{location}: {level}: marcador obrigatório ausente: {label}"
                )
            elif current < previous:
                errors.append(
                    f"{location}: {level}: marcador fora da ordem: {label}"
                )
            previous = max(previous, current)
            positions[label] = current

        if len(positions) != len(_SELF_CONTAINED_LABELS):
            continue

        fields = {
            label: section[
                positions[label] + len(label) :
                positions[_SELF_CONTAINED_LABELS[index + 1]]
                if index + 1 < len(_SELF_CONTAINED_LABELS)
                else len(section)
            ].strip()
            for index, label in enumerate(_SELF_CONTAINED_LABELS)
        }
        for label, content in fields.items():
            content_without_comments = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
            if not content_without_comments.strip():
                errors.append(
                    f"{location}: {level}: campo obrigatório sem conteúdo: {label}"
                )

        artifact = fields["**Artefato que você irá usar**"]
        preparation = fields["**Antes de executar**"]
        action = fields["**O que fazer**"]
        evidence = fields["**Evidência esperada**"]
        if not _ACTIVITY_PATH.search(artifact):
            errors.append(
                f"{location}: {level}: artefato deve identificar um caminho"
            )
        if not _ACTIVITY_INITIAL_STATE.search(preparation):
            errors.append(
                f"{location}: {level}: preparação deve declarar um estado inicial verificável"
            )
        if not _ACTIVITY_ACTION.search(action):
            errors.append(
                f"{location}: {level}: ação deve listar uma manipulação ou execução concreta"
            )
        if not _ACTIVITY_EVIDENCE.search(evidence):
            errors.append(
                f"{location}: {level}: evidência deve indicar uma saída ou observação verificável"
            )
        if not _ACTIVITY_CONTINGENCY.search("\n".join(fields.values())):
            errors.append(
                f"{location}: {level}: atividade deve informar uma contingência"
            )
    return errors


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


def _mask_fenced_code(text: str) -> str:
    """Substitui cercas e seu conteúdo por espaços, preservando offsets e linhas."""

    masked: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        content = line.lstrip(" ")
        opening = re.match(r"(?P<fence>`{3,}|~{3,})", content)
        inside_fence = fence_character is not None
        if inside_fence:
            stripped = content.rstrip("\r\n")
            if re.fullmatch(
                rf"{re.escape(fence_character)}{{{fence_length},}}[ \t]*", stripped
            ):
                fence_character = None
                fence_length = 0
            masked.append("".join(char if char in "\r\n" else " " for char in line))
            continue
        if opening:
            fence = opening.group("fence")
            fence_character = fence[0]
            fence_length = len(fence)
            masked.append("".join(char if char in "\r\n" else " " for char in line))
            continue
        masked.append(line)
    return "".join(masked)


def _reference_key(value: str) -> str:
    return " ".join(value.split()).casefold()


def _html_attributes(tag: str) -> dict[str, str]:
    attributes: dict[str, str] = {}
    for match in _HTML_ATTRIBUTE.finditer(tag):
        value = match.group("double") or match.group("single") or match.group("bare") or ""
        attributes[match.group("name").casefold()] = unescape(value)
    return attributes


def _resources(text: str) -> tuple[str, list[_Resource]]:
    masked = _mask_fenced_code(text)
    definition_matches = list(_REFERENCE_DEFINITION.finditer(masked))
    definitions = {
        _reference_key(match.group("reference")): match.group("target")
        for match in definition_matches
    }
    resources: list[_Resource] = []
    for match in _MARKDOWN_LINK.finditer(masked):
        resources.append(
            _Resource(
                "image" if match.group("image") else "link",
                match.group("target"),
                match.group("label"),
                match.start(),
                match.end(),
            )
        )
    for match in _REFERENCE_LINK.finditer(masked):
        reference = match.group("reference") or match.group("label")
        resources.append(
            _Resource(
                "image" if match.group("image") else "link",
                definitions.get(_reference_key(reference)),
                match.group("label"),
                match.start(),
                match.end(),
                reference,
            )
        )
    for match in _SHORTCUT_REFERENCE.finditer(masked):
        if any(
            definition.start() <= match.start() < definition.end()
            for definition in definition_matches
        ):
            continue
        target = definitions.get(_reference_key(match.group("label")))
        if target is None:
            continue
        resources.append(
            _Resource(
                "image" if match.group("image") else "link",
                target,
                match.group("label"),
                match.start(),
                match.end(),
                match.group("label"),
            )
        )
    for match in _HTML_RESOURCE.finditer(masked):
        attributes = _html_attributes(match.group(0))
        is_image = match.group("tag").casefold() == "img"
        resources.append(
            _Resource(
                "image" if is_image else "link",
                attributes.get("src" if is_image else "href"),
                attributes.get("alt", ""),
                match.start(),
                match.end(),
            )
        )
    return masked, sorted(resources, key=lambda resource: resource.start)


def _has_proximal_textual_equivalent(masked: str, image: _Resource) -> bool:
    line_start = masked.rfind("\n", 0, image.start) + 1
    line_end = masked.find("\n", image.end)
    if line_end == -1:
        line_end = len(masked)
    if (
        masked[line_start : image.start].strip()
        or masked[image.end : line_end].strip()
        or line_end == len(masked)
    ):
        return False

    following_lines = masked[line_end + 1 :]
    separator = re.match(r"(?:[ \t]*\r?\n)+", following_lines)
    if not separator:
        return False
    following = following_lines[separator.end() :]

    caption = _FIGURE_CAPTION.match(following)
    if caption:
        after_caption = following[caption.end() :]
        caption_separator = re.match(
            r"[ \t]*\r?\n(?:[ \t]*\r?\n)+", after_caption
        )
        if not caption_separator:
            return False
        following = after_caption[caption_separator.end() :]

    if not following.startswith(_TEXTUAL_EQUIVALENT):
        return False
    paragraph_end = re.search(r"\r?\n[ \t]*\r?\n|\Z", following)
    paragraph = following[: paragraph_end.start()] if paragraph_end else following
    description = paragraph[len(_TEXTUAL_EQUIVALENT) :].strip()
    return bool(description)


def _validate_links_and_figures(path: Path, docs_root: Path, text: str) -> list[str]:
    location = _location(path, docs_root)
    errors: list[str] = []
    masked, resources = _resources(text)
    for resource in resources:
        raw_target = resource.target
        if raw_target is None:
            reference = resource.reference or resource.label
            errors.append(f"{location}: referência Markdown ausente: {reference}")
            continue
        target = raw_target[1:-1] if raw_target.startswith("<") else raw_target
        parsed = urlsplit(unquote(target))
        if not parsed.scheme and not target.startswith("//"):
            destination, fragment = _local_target(path, docs_root, raw_target)
            if not destination.is_file():
                errors.append(f"{location}: arquivo local ausente: {target}")
            elif fragment and destination.suffix.casefold() in {".md", ".markdown"}:
                destination_text = destination.read_text(encoding="utf-8")
                if fragment not in _anchors(destination_text):
                    errors.append(f"{location}: âncora local ausente: {target}")
        if resource.kind == "image" and not resource.label.strip():
            errors.append(f"{location}: imagem sem texto alternativo: {target}")
        if resource.kind == "image" and not _has_proximal_textual_equivalent(
            masked, resource
        ):
            errors.append(f"{location}: figura sem leitura textual: {target}")
    return errors


def _validate_procedural_labels(path: Path, docs_root: Path, text: str) -> list[str]:
    if path.name not in {"oficina-de-ferramentas.md", "exercicios.md"} and not any(
        part.casefold() in {"laboratorio", "laboratorios", "laboratórios"}
        for part in path.parts
    ):
        return []
    location = _location(path, docs_root)
    lines = _mask_fenced_code(text).splitlines()
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


def _access_classification_errors(
    text: str, location: str, path: Path
) -> list[str]:
    folded = text.casefold()
    candidates = list(re.split(r"\n[ \t]*\n", folded))
    scoped_sections: list[str] = []
    is_tool_page = path.name in {
        "oficina-de-ferramentas.md",
        "guia-de-ferramentas.md",
    }
    headings = list(_HEADING.finditer(folded))
    for index, heading in enumerate(headings):
        title = heading.group("title")
        if not _TOOL_ACCESS_HEADING.search(title) and not (
            is_tool_page and _PREREQUISITE_HEADING.search(title)
        ):
            continue
        level = len(heading.group(0)) - len(heading.group(0).lstrip("#"))
        end = len(folded)
        for following in headings[index + 1 :]:
            following_level = len(following.group(0)) - len(
                following.group(0).lstrip("#")
            )
            if following_level <= level:
                end = following.start()
                break
        scoped_sections.append(folded[heading.start() : end])

    if any(_ACCESS_CLASSIFICATION.search(section) for section in scoped_sections):
        return [f"{location}: classificação de acesso com linguagem comercial"]

    for candidate in candidates:
        has_commercial_language = _ACCESS_CLASSIFICATION.search(candidate)
        has_access_classification = (
            _ACCESS_CONTEXT.search(candidate)
            or _TOOL_REQUIREMENT.search(candidate)
            or _COMMERCIAL_REQUIREMENT.search(candidate)
        )
        if has_commercial_language and has_access_classification:
            return [f"{location}: classificação de acesso com linguagem comercial"]
    return []


def _criteria_blocks(text: str) -> list[str]:
    markers = list(_CRITERIA_LABEL.finditer(text))
    blocks: list[str] = []
    for index, marker in enumerate(markers):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        for boundary in (_HEADING.search(text, marker.end()), _BOLD_LABEL.search(text, marker.end())):
            if boundary and boundary.start() < end:
                end = boundary.start()
        blocks.append(text[marker.end() : end])
    return blocks


def _percentage_errors(text: str, location: str, context: str = "") -> list[str]:
    errors: list[str] = []
    for instrument, block in enumerate(_criteria_blocks(text), start=1):
        assessment_rows = [match.group(0) for match in _TABLE.finditer(block)]
        assessment_rows.extend(match.group(0) for match in _LIST_ITEM.finditer(block))
        values = [
            Decimal(value.replace(",", "."))
            for row in assessment_rows
            for value in _PERCENTAGE.findall(row)
        ]
        if not values:
            prefix = f"{context}: " if context else ""
            errors.append(
                f"{location}: {prefix}instrumento sem percentuais "
                f"(instrumento {instrument}; esperado: 100%)"
            )
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


def _criteria_table_evidence_errors(text: str, location: str) -> list[str]:
    """Exige evidência e insuficiência explícitas em cada linha de critérios."""

    errors: list[str] = []
    for instrument, block in enumerate(_criteria_blocks(text), start=1):
        for table in _TABLE.finditer(block):
            rows = [line for line in table.group(0).splitlines() if line.strip()]
            if len(rows) < 3:
                continue
            header = [cell.strip().casefold() for cell in rows[0].strip().strip("|").split("|")]
            if len(header) < 3 or not any(
                "evid" in cell and "insufici" in cell for cell in header
            ):
                errors.append(
                    f"{location}: instrumento {instrument}: tabela de critérios "
                    "sem coluna de evidência e insuficiência"
                )
                continue
            for row_number, row in enumerate(rows[2:], start=1):
                cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
                description = " ".join(cells[2:]).casefold()
                if "evid" not in description:
                    errors.append(
                        f"{location}: instrumento {instrument}, critério {row_number}: "
                        "critério sem evidência explícita"
                    )
                if "insufici" not in description:
                    errors.append(
                        f"{location}: instrumento {instrument}, critério {row_number}: "
                        "critério sem insuficiência explícita"
                    )
    return errors


def _word_count(text: str) -> int:
    without_code = re.sub(r"```.*?```|~~~.*?~~~", " ", text, flags=re.DOTALL)
    without_links = re.sub(r"https?://\S+", " ", without_code)
    return len(_WORD.findall(without_links))


def _validate_exercises(path: Path, docs_root: Path) -> list[str]:
    location = _location(path, docs_root)
    text = path.read_text(encoding="utf-8")
    masked = _mask_fenced_code(text)
    sections = bloom_sections(masked)
    errors: list[str] = []
    for level in BLOOM:
        occurrences = len(
            re.findall(
                rf"^##[ \t]+{re.escape(level)}[ \t]*#*[ \t]*$",
                masked,
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
        errors.extend(_percentage_errors(section, location, level))
    errors.extend(_criteria_table_evidence_errors(text, location))
    errors.extend(expandable_feedback_errors(text, location))
    errors.extend(self_contained_activity_errors(text, location))
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
    errors.extend(_access_classification_errors(text, location, path))
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
        if relative_parts and relative_parts[0] == "superpowers":
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
