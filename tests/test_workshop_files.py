"""As oficinas entregam arquivos, e a página precisa mostrar o arquivo real.

Cada bloco de código de uma oficina vem precedido por um link para o arquivo
correspondente em `oficinas/`. Este teste compara os dois: o que o aluno copia
da página e o que ele baixa pelo link têm de ser idênticos, byte a byte.
"""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OFICINAS = ROOT / "oficinas"
BLOB = "https://github.com/marco-mendes/arquitetura-software/blob/main/"

# Bloco entregue: link para o arquivo canônico, linha em branco e o código.
ENTREGA = re.compile(
    r"\[`(?P<rotulo>[^`]+)`\]\("
    + re.escape(BLOB)
    + r"(?P<caminho>oficinas/[^)]+)\)\n\n"
    r"```(?P<lingua>[a-z]*)\n(?P<corpo>.*?)```",
    re.DOTALL,
)


# Módulos já convertidos para o formato "pasta vazia, arquivos entregues um a um".
# A lista cresce conforme cada oficina é convertida, e o que não está aqui ainda
# pede o repositório clonado. Converter um módulo é acrescentá-lo a esta tupla.
CONVERTIDOS = ("modulo-1-visao-geral", "modulo-2-apis", "modulo-3-servicos", "modulo-4-governanca", "modulo-6-nuvem")


def _oficinas_publicadas() -> list[Path]:
    return [DOCS / modulo / "oficina-de-ferramentas.md" for modulo in CONVERTIDOS]


class WorkshopFilesTest(unittest.TestCase):
    def test_every_delivered_block_matches_its_file_on_disk(self):
        entregues = 0
        for pagina in _oficinas_publicadas():
            texto = pagina.read_text(encoding="utf-8")
            for bloco in ENTREGA.finditer(texto):
                caminho = ROOT / bloco.group("caminho")
                rotulo = bloco.group("rotulo")
                with self.subTest(pagina=pagina.name, arquivo=bloco.group("caminho")):
                    self.assertTrue(caminho.is_file(), caminho)
                    self.assertTrue(
                        bloco.group("caminho").endswith(rotulo),
                        f"o rótulo {rotulo!r} não corresponde ao caminho do link",
                    )
                    esperado = caminho.read_text(encoding="utf-8").rstrip("\n")
                    self.assertEqual(
                        esperado,
                        bloco.group("corpo").rstrip("\n"),
                        f"{caminho} divergiu do bloco publicado",
                    )
                entregues += 1
        self.assertGreater(entregues, 0, "nenhuma oficina entrega arquivos")

    def test_no_workshop_asks_the_student_to_clone_the_repository(self):
        proibidos = ("raiz-do-clone", "raiz do clone", "git clone", "repositório clonado")
        for pagina in _oficinas_publicadas():
            texto = pagina.read_text(encoding="utf-8").casefold()
            for termo in proibidos:
                with self.subTest(pagina=pagina.name, termo=termo):
                    self.assertNotIn(termo, texto)

    def test_delivered_files_live_under_the_module_they_belong_to(self):
        for pagina in _oficinas_publicadas():
            modulo = pagina.parent.name.split("-")[1]
            texto = pagina.read_text(encoding="utf-8")
            for bloco in ENTREGA.finditer(texto):
                with self.subTest(pagina=pagina.name):
                    self.assertTrue(
                        bloco.group("caminho").startswith(f"oficinas/modulo-{modulo}/"),
                        bloco.group("caminho"),
                    )

    def test_the_conversion_backlog_is_explicit(self):
        """O que ainda não foi convertido precisa estar visível, e não esquecido."""

        todas = {p.parent.name for p in DOCS.glob("modulo-*/oficina-de-ferramentas.md")}
        pendentes = sorted(todas - set(CONVERTIDOS))
        self.assertEqual(
            ["modulo-5-eventos"],
            pendentes,
            "atualize CONVERTIDOS ao converter uma oficina",
        )

    def test_every_file_under_oficinas_is_published_by_some_workshop(self):
        publicados = set()
        for pagina in _oficinas_publicadas():
            texto = pagina.read_text(encoding="utf-8")
            publicados.update(b.group("caminho") for b in ENTREGA.finditer(texto))
        no_disco = {
            str(caminho.relative_to(ROOT))
            for caminho in OFICINAS.rglob("*")
            if caminho.is_file() and "__pycache__" not in caminho.parts
        }
        self.assertEqual(set(), no_disco - publicados, "arquivo sem bloco correspondente")


if __name__ == "__main__":
    unittest.main()
