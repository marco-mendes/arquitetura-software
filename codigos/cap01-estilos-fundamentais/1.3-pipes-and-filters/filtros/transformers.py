"""Transformers — transformam dados sem descartar registros."""

from framework import Filtro
from dominio import Curriculo, Vaga, ResultadoTriagem


class NormalizadorDeCampos(Filtro):
    """
    Transformer: normaliza habilidades (lowercase) e nome (title case).
    Não descarta — apenas padroniza os dados para processamento posterior.
    """

    def processar(self, curriculos: list[Curriculo]) -> list[Curriculo]:
        for c in curriculos:
            c.candidato_nome = c.candidato_nome.strip().title()
            c.habilidades = [h.lower().strip() for h in c.habilidades]
        return curriculos


class CalculadorDeScore(Filtro):
    """
    Transformer: calcula score de aderência baseado na interseção de habilidades
    e converte Curriculo em ResultadoTriagem com o score calculado.
    """

    def __init__(self, vaga: Vaga):
        self._requeridas = {h.lower() for h in vaga.habilidades_requeridas}

    def processar(self, curriculos: list[Curriculo]) -> list[ResultadoTriagem]:
        resultados = []
        for c in curriculos:
            compativeis = list(set(c.habilidades) & self._requeridas)
            score = len(compativeis) / len(self._requeridas) if self._requeridas else 0.0
            resultados.append(ResultadoTriagem(
                curriculo=c,
                aprovado=True,
                score=round(score, 2),
                habilidades_compativeis=compativeis,
            ))
        return resultados
