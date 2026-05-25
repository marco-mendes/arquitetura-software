"""Testers — filtram e descartam currículos que não atendem critérios."""

from framework import Filtro
from dominio import Curriculo, Vaga


class ValidadorDeCurriculo(Filtro):
    """
    Tester: descarta currículos com dados obrigatórios ausentes ou inválidos.
    Não transforma — apenas aprova ou descarta.
    """

    def processar(self, curriculos: list[Curriculo]) -> list[Curriculo]:
        validos = []
        for c in curriculos:
            if not c.candidato_nome.strip():
                print(f"  [DESCARTADO] Currículo id={c.id}: nome ausente")
                continue
            if "@" not in c.email:
                print(f"  [DESCARTADO] {c.candidato_nome}: e-mail inválido")
                continue
            if c.anos_experiencia < 0:
                print(f"  [DESCARTADO] {c.candidato_nome}: experiência negativa")
                continue
            validos.append(c)
        return validos


class FiltroPorExperienciaMinima(Filtro):
    """
    Tester: descarta candidatos abaixo do mínimo de experiência da vaga.
    """

    def __init__(self, vaga: Vaga):
        self._minimo = vaga.experiencia_minima
        self._titulo = vaga.titulo

    def processar(self, curriculos: list[Curriculo]) -> list[Curriculo]:
        aprovados = []
        for c in curriculos:
            if c.anos_experiencia < self._minimo:
                print(
                    f"  [REPROVADO] {c.candidato_nome}: "
                    f"{c.anos_experiencia} ano(s) < mínimo {self._minimo}"
                )
                continue
            aprovados.append(c)
        return aprovados


class FiltroPorPretensaoSalarial(Filtro):
    """
    Tester: descarta candidatos com pretensão acima do orçamento da vaga.
    """

    def __init__(self, vaga: Vaga):
        self._maximo = vaga.salario_maximo

    def processar(self, curriculos: list[Curriculo]) -> list[Curriculo]:
        aprovados = []
        for c in curriculos:
            if c.pretensao_salarial > self._maximo:
                print(
                    f"  [REPROVADO] {c.candidato_nome}: "
                    f"pretensão R${c.pretensao_salarial:,.0f} "
                    f"> máximo R${self._maximo:,.0f}"
                )
                continue
            aprovados.append(c)
        return aprovados
