from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import markdown
import yaml

from scripts.validate_content import (
    BLOOM,
    MODULES,
    PAGES,
    bloom_sections,
    validate_all,
    validate_document,
    validate_module,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class ContentContractTest(unittest.TestCase):
    def test_course_has_six_modules_and_eight_page_contract(self):
        expected_modules = (
            ("modulo-1-visao-geral", "Visão geral de estilos"),
            ("modulo-2-apis", "Arquitetura de APIs"),
            ("modulo-3-servicos", "Arquitetura de Serviços"),
            ("modulo-4-governanca", "Governança de Serviços"),
            ("modulo-5-eventos", "Arquiteturas de Eventos"),
            ("modulo-6-nuvem", "Arquiteturas de Nuvens"),
        )
        self.assertEqual(expected_modules, tuple(MODULES.items()))
        self.assertEqual(
            (
                "index.md",
                "conceitos.md",
                "padroes-e-decisoes.md",
                "exemplo-arquitetural.md",
                "estudo-de-caso.md",
                "oficina-de-ferramentas.md",
                "exercicios.md",
                "sintese-e-referencias.md",
            ),
            PAGES,
        )
        self.assertEqual(
            ("Recordar", "Compreender", "Aplicar", "Analisar", "Avaliar", "Criar"),
            BLOOM,
        )

    def test_mkdocs_excludes_internal_planning_documents(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))

        excluded = config.get("exclude_docs", ())
        self.assertIn("superpowers/**", excluded)
        self.assertNotIn("superpowers", yaml.safe_dump(config.get("nav", ())))

    def test_public_pages_use_assessment_criteria_vocabulary(self):
        for path in DOCS.rglob("*.md"):
            if path.relative_to(DOCS).parts[0] == "superpowers":
                continue
            text = path.read_text(encoding="utf-8").casefold()
            self.assertNotRegex(
                text,
                r"\brubricas?\b|\bpontua(?:ção|cao)\b|\b\d+\s+pontos?\b",
            )

    def test_bloom_sections_extracts_each_level_without_subheadings(self):
        text = "\n".join(
            f"## {level}\n\nAtividade de {level}.\n\n### Apoio\n\nDetalhe."
            for level in BLOOM
        )

        sections = bloom_sections(text)

        self.assertEqual(set(BLOOM), set(sections))
        self.assertIn("### Apoio", sections["Aplicar"])
        self.assertNotIn("## Analisar", sections["Aplicar"])

    def test_bloom_sections_ignore_headings_in_fenced_examples(self):
        text = (
            "## Recordar\n\nDefina o conceito.\n\n"
            "```markdown\n"
            "## Aplicar\n\n"
            "**Resposta:** este é apenas um exemplo de sintaxe.\n"
            "```\n\n"
            "## Compreender\n\nExplique a diferença.\n"
        )

        sections = bloom_sections(text)

        self.assertEqual({"Recordar", "Compreender"}, set(sections))
        self.assertNotIn("Resposta", sections["Recordar"])

    def test_mkdocs_renders_explicit_anchors_accepted_by_validator(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        extension_names: list[str] = []
        extension_configs: dict[str, dict] = {}
        for extension in config["markdown_extensions"]:
            if isinstance(extension, str):
                extension_names.append(extension)
            else:
                name, settings = next(iter(extension.items()))
                extension_names.append(name)
                extension_configs[name] = settings or {}

        self.assertIn("attr_list", extension_names)
        rendered = markdown.markdown(
            "## Seção explícita {#anchor-explicito}",
            extensions=extension_names,
            extension_configs=extension_configs,
        )
        self.assertIn('id="anchor-explicito"', rendered)

        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            (docs / "destino.md").write_text(
                "# Destino\n\n## Seção explícita {#anchor-explicito}\n",
                encoding="utf-8",
            )
            source = docs / "origem.md"
            source.write_text(
                "# Origem\n\n[Seção](destino.md#anchor-explicito)\n",
                encoding="utf-8",
            )
            self.assertFalse(
                any("âncora local ausente" in e for e in validate_document(source, docs))
            )

    def test_validator_rejects_placeholders_and_public_policy_vocabulary(self):
        samples = {
            "TODO: completar": "marcador provisório",
            "Use a rubrica publicada.": "vocabulário público proibido",
            "A atividade vale dez pontos.": "vocabulário público proibido",
            "Consulte a pontuação.": "vocabulário público proibido",
            "A ferramenta exige cartão para acesso.": "classificação de acesso",
            "O acesso depende de crédito.": "classificação de acesso",
            "Há cobrança para usar a ferramenta.": "classificação de acesso",
            "Acesso à ferramenta:\n- cadastro com cobranca.": "classificação de acesso",
        }
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            page = docs / "pagina.md"
            for text, expected in samples.items():
                with self.subTest(text=text):
                    page.write_text(f"# Título\n\n{text}\n", encoding="utf-8")
                    self.assertTrue(
                        any(expected in error for error in validate_document(page, docs))
                    )

    def test_access_classification_spans_sections_without_matching_hospital_domain(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            page = docs / "pagina.md"
            for heading in ("Acesso à ferramenta", "Instalação"):
                with self.subTest(heading=heading):
                    page.write_text(
                        "# Ferramenta\n\n"
                        f"## {heading}\n\n"
                        "Antes da oficina, prepare o ambiente.\n\n"
                        "Requer cartão.\n",
                        encoding="utf-8",
                    )
                    self.assertTrue(
                        any(
                            "classificação de acesso" in error
                            for error in validate_document(page, docs)
                        )
                    )

            workshop = docs / "oficina-de-ferramentas.md"
            workshop.write_text(
                "# Oficina\n\n## Pré-requisitos\n\nRequer cartão.\n",
                encoding="utf-8",
            )
            self.assertTrue(
                any(
                    "classificação de acesso" in error
                    for error in validate_document(workshop, docs)
                )
            )

            page.write_text(
                "# Caso hospitalar\n\n"
                "## Requisitos do caso hospitalar\n\n"
                "A cobrança hospitalar gera crédito no prontuário.\n\n"
                "Use a ferramenta para simular a cobrança hospitalar.\n",
                encoding="utf-8",
            )
            self.assertFalse(
                any(
                    "classificação de acesso" in error
                    for error in validate_document(page, docs)
                )
            )

    def test_validator_checks_local_links_anchors_and_figure_accessibility(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            (docs / "figura.png").write_bytes(b"png")
            (docs / "destino.md").write_text(
                "# Destino\n\n## Âncora existente\n", encoding="utf-8"
            )
            page = docs / "pagina.md"
            page.write_text(
                "# Página\n\n"
                "[Arquivo ausente](ausente.md)\n\n"
                "[Âncora ausente](destino.md#nao-existe)\n\n"
                "![](figura.png)\n\n"
                "![Fluxo do exemplo](figura.png)\n\n"
                "Parágrafo sem equivalência.\n",
                encoding="utf-8",
            )

            errors = validate_document(page, docs)

            for expected in (
                "arquivo local ausente",
                "âncora local ausente",
                "imagem sem texto alternativo",
                "figura sem leitura textual",
            ):
                self.assertTrue(any(expected in error for error in errors), expected)

    def test_resource_parser_supports_reference_html_and_ignores_fenced_examples(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            (docs / "figura.png").write_bytes(b"png")
            (docs / "destino.md").write_text(
                "# Destino\n\n## Alvo\n", encoding="utf-8"
            )
            page = docs / "pagina.md"
            page.write_text(
                "# Recursos\n\n"
                "[Inline](destino.md#alvo)\n\n"
                "[Referência][destino]\n\n"
                "[Guia]\n\n"
                '<a href="destino.md#alvo">HTML</a>\n\n'
                "![Mapa por referência][figura]\n\n"
                "**Leitura textual da figura:** O mapa conecta origem e destino.\n\n"
                "![Mapa]\n\n"
                "**Leitura textual da figura:** O atalho mostra o mesmo mapa.\n\n"
                '<img src="figura.png" alt="Mapa em HTML">\n\n'
                "**Leitura textual da figura:** O mapa HTML repete a relação.\n\n"
                "```markdown\n"
                "[Exemplo não ativo](ausente.md)\n"
                "![Imagem não ativa](ausente.png)\n"
                '<a href="ausente-html.md">Exemplo</a>\n'
                "```\n\n"
                "    ```markdown\n"
                "    [Exemplo aninhado](ausente-aninhado.md)\n"
                "    ![Imagem aninhada](ausente-aninhado.png)\n"
                "    ```\n\n"
                "[destino]: destino.md#alvo\n"
                "[figura]: figura.png\n"
                "[Guia]: destino.md#alvo\n"
                "[Mapa]: figura.png\n",
                encoding="utf-8",
            )

            self.assertEqual([], validate_document(page, docs))

    def test_reference_and_html_resources_are_actively_validated(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            page = docs / "pagina.md"
            page.write_text(
                "# Recursos\n\n"
                "[Referência ausente][destino]\n\n"
                "[Guia ausente]\n\n"
                '<a href="ausente-html.md">HTML ausente</a>\n\n'
                "![Figura ausente][figura]\n\n"
                "**Leitura textual da figura:** Figura de teste.\n\n"
                "![Mapa ausente]\n\n"
                "**Leitura textual da figura:** Atalho de imagem.\n\n"
                '<img src="ausente-html.png" alt="">\n\n'
                "**Leitura textual da figura:** Figura HTML de teste.\n\n"
                "[destino]: ausente-referencia.md\n"
                "[figura]: ausente-referencia.png\n"
                "[Guia ausente]: ausente-atalho.md\n"
                "[Mapa ausente]: ausente-atalho.png\n",
                encoding="utf-8",
            )

            errors = validate_document(page, docs)

            for target in (
                "ausente-referencia.md",
                "ausente-html.md",
                "ausente-referencia.png",
                "ausente-html.png",
                "ausente-atalho.md",
                "ausente-atalho.png",
            ):
                self.assertTrue(any(target in error for error in errors), target)
                if "atalho" in target:
                    self.assertEqual(1, sum(target in error for error in errors), target)
            self.assertTrue(any("imagem sem texto alternativo" in e for e in errors))

    def test_figure_equivalence_must_be_the_next_block_after_optional_caption(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            (docs / "figura.png").write_bytes(b"png")
            page = docs / "pagina.md"
            valid_followings = (
                "**Leitura textual da figura:** Origem leva ao destino.",
                "*Figura 1 — Mapa do fluxo.*\n\n"
                "**Leitura textual da figura:** Origem leva ao destino.",
            )
            for following in valid_followings:
                with self.subTest(valid=following):
                    page.write_text(
                        f"# Figura\n\n![Mapa](figura.png)\n\n{following}\n",
                        encoding="utf-8",
                    )
                    self.assertFalse(
                        any(
                            "figura sem leitura textual" in error
                            for error in validate_document(page, docs)
                        )
                    )

            invalid_followings = (
                "Parágrafo interveniente.\n\n**Leitura textual da figura:** Tardia.",
                "## Outra seção\n\n**Leitura textual da figura:** Tardia.",
                "![Outra](figura.png)\n\n**Leitura textual da figura:** Só a segunda.",
                "**Equivalente textual:** Marcador incorreto.",
                "**Leitura textual da figura:**",
            )
            for following in invalid_followings:
                with self.subTest(following=following):
                    page.write_text(
                        f"# Figura\n\n![Mapa](figura.png)\n\n{following}\n",
                        encoding="utf-8",
                    )
                    self.assertTrue(
                        any(
                            "figura sem leitura textual" in error
                            for error in validate_document(page, docs)
                        )
                    )

            for source in (
                "# Figura\n\n![Mapa](figura.png) "
                "**Leitura textual da figura:** Mesma linha.\n",
                "# Figura\n\n![Mapa](figura.png)\n"
                "**Leitura textual da figura:** Mesmo bloco.\n",
            ):
                with self.subTest(source=source):
                    page.write_text(source, encoding="utf-8")
                    self.assertTrue(
                        any(
                            "figura sem leitura textual" in error
                            for error in validate_document(page, docs)
                        )
                    )

    def test_procedural_bold_labels_are_isolated_as_paragraphs(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            page = docs / "oficina-de-ferramentas.md"
            page.write_text(
                "# Oficina\n\n"
                "**Execute** rode o comando.\n\n"
                "**Observe**\n"
                "Leia a saída.\n\n"
                "**Prepare** crie o diretório.\n\n"
                "**Instale:** execute o instalador.\n\n"
                "**Verifique** confira a versão.\n\n"
                "**Interpretação** compare a saída.\n\n"
                "**Limpeza** remova os recursos.\n",
                encoding="utf-8",
            )
            errors = validate_document(page, docs)
            self.assertEqual(
                7,
                sum("rótulo procedimental aglutinado" in error for error in errors),
            )

            page.write_text(
                "# Oficina\n\n**Execute**\n\nRode o comando.\n",
                encoding="utf-8",
            )
            self.assertFalse(
                any(
                    "rótulo procedimental aglutinado" in error
                    for error in validate_document(page, docs)
                )
            )

            page.write_text(
                "# Oficina\n\n"
                "```markdown\n"
                "**Execute** rode o comando apenas como exemplo.\n"
                "```\n",
                encoding="utf-8",
            )
            self.assertFalse(
                any(
                    "rótulo procedimental aglutinado" in error
                    for error in validate_document(page, docs)
                )
            )

    def test_module_validator_enforces_bloom_answers_criteria_and_percentages(self):
        complete_markers = "\n\n".join(
            (
                "**Situação**\n\nCenário.",
                "**Seu papel**\n\nArquiteto.",
                "**Insumos disponíveis**\n\nEvidências.",
                "**Como conduzir**\n\nCompare.",
                "**Entrega esperada**\n\nADR.",
                "**Critérios de avaliação**\n\nCritérios.",
            )
        )
        exercises = (
            "# Exercícios\n\n"
            "## Recordar\n\n**Resposta:** conceito.\n\n"
            "## Compreender\n\nExplique.\n\n"
            "## Aplicar\n\n**Resposta:** execução.\n\n"
            "## Analisar\n\n"
            f"{complete_markers}\n\n"
            "| Critério | Percentual |\n| --- | ---: |\n"
            "| Evidência | 40% |\n| Decisão | 50% |\n\n"
            "## Avaliar\n\n"
            f"{complete_markers}\n\n"
            "| Critério | Percentual |\n| --- | ---: |\n| Recomendação | 100% |\n\n"
            "## Criar\n\nProduza um incremento.\n\n"
            "## Recordar\n\nRepetição indevida.\n"
        )
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            slug = next(iter(MODULES))
            module = docs / slug
            module.mkdir()
            for page_name in PAGES:
                (module / page_name).write_text(
                    exercises if page_name == "exercicios.md" else "# Página\n",
                    encoding="utf-8",
                )

            errors = validate_module(slug, docs)

            for expected in (
                "bloco de resposta fora de Recordar/Compreender",
                "Aplicar: marcador obrigatório ausente",
                "percentuais do instrumento somam 90%",
                "seção Bloom duplicada: Recordar",
                "fora da faixa de 5.000–8.500 palavras",
            ):
                self.assertTrue(any(expected in error for error in errors), expected)

    def test_percentages_are_scoped_to_assessment_criteria_blocks(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            page = docs / "avaliacao.md"
            page.write_text(
                "# Avaliação\n\n"
                "| Entrada | SLA |\n| --- | ---: |\n| Agendamento | 99,9% |\n\n"
                "## Instrumento com tabela\n\n"
                "**Critérios de avaliação**\n\n"
                "| Critério | Percentual |\n| --- | ---: |\n"
                "| Evidência | 40% |\n| Decisão | 50% |\n\n"
                "## Instrumento com lista\n\n"
                "**Critérios de avaliação**\n\n"
                "- Clareza — 60%\n- Consequências — 40%\n\n"
                "## Instrumento sem valores\n\n"
                "**Critérios de avaliação**\n\n"
                "A entrega será observada pela coerência.\n",
                encoding="utf-8",
            )

            errors = validate_document(page, docs)

            self.assertEqual(
                1, sum("percentuais do instrumento somam 90%" in e for e in errors)
            )
            self.assertEqual(
                1, sum("instrumento sem percentuais" in e for e in errors)
            )
            self.assertFalse(any("99.9" in error or "99,9" in error for error in errors))

    def test_criteria_tables_require_evidence_and_insufficiency_per_row(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            slug = next(iter(MODULES))
            module = docs / slug
            module.mkdir()
            incomplete = (
                "# Exercícios\n\n"
                "## Aplicar\n\n"
                "**Critérios de avaliação**\n\n"
                "| Critério | Percentual | Evidência e insuficiência |\n"
                "| --- | ---: | --- |\n"
                "| Decisão | 100% | Evidência: contexto declarado. |\n"
            )
            for page_name in PAGES:
                (module / page_name).write_text(
                    incomplete if page_name == "exercicios.md" else "# Página\n",
                    encoding="utf-8",
                )

            errors = validate_module(slug, docs)

            self.assertTrue(
                any("critério sem insuficiência explícita" in error for error in errors)
            )

            complete = incomplete.replace(
                "Evidência: contexto declarado.",
                "Evidência: contexto declarado. Insuficiente: falta de contexto.",
            )
            (module / "exercicios.md").write_text(complete, encoding="utf-8")
            errors = validate_module(slug, docs)
            self.assertFalse(
                any("critério sem insuficiência explícita" in error for error in errors)
            )

    def test_all_validation_skips_internal_superpowers_documents(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            internal = docs / "superpowers"
            internal.mkdir()
            (internal / "plano.md").write_text(
                "# Plano\n\nTODO: material interno.\n", encoding="utf-8"
            )
            (docs / "publica.md").write_text("# Página pública\n", encoding="utf-8")
            nested_public = docs / "comecar" / "superpowers"
            nested_public.mkdir(parents=True)
            (nested_public / "pagina.md").write_text(
                "# Página pública\n\nTODO: validar esta página.\n", encoding="utf-8"
            )

            errors = validate_all(docs)

            self.assertFalse(any("superpowers/plano.md" in error for error in errors))
            self.assertTrue(
                any("comecar/superpowers/pagina.md" in error for error in errors)
            )
            self.assertTrue(any("32.000–51.000 palavras" in error for error in errors))
