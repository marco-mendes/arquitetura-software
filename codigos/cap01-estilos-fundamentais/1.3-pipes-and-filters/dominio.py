"""
Domínio — Pipeline de Triagem de Currículos
Objetos de dados simples usados pelos filtros.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Curriculo:
    id: int
    candidato_nome: str
    email: str
    anos_experiencia: int
    habilidades: list[str]
    pretensao_salarial: float
    cidade: str


@dataclass
class Vaga:
    id: int
    titulo: str
    experiencia_minima: int
    habilidades_requeridas: list[str]
    salario_maximo: float


@dataclass
class ResultadoTriagem:
    curriculo: Curriculo
    aprovado: bool = True
    score: float = 0.0
    motivo_rejeicao: str = ""
    habilidades_compativeis: list[str] = field(default_factory=list)
