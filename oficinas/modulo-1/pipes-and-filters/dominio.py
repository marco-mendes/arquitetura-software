"""O dado que atravessa o fluxo, e nada mais."""

from dataclasses import dataclass, field


@dataclass
class Curriculo:
    id: int
    nome: str | None
    anos_experiencia: int
    pretensao: int
    habilidades: list[str] = field(default_factory=list)
    cidade: str = ""
    score: int = 0
    compativeis: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Vaga:
    titulo: str
    anos_minimos: int
    teto_salarial: int
    habilidades: tuple[str, ...]
