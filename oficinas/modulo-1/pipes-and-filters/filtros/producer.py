"""Produtor: entrega os dados brutos ao fluxo."""

from dominio import Curriculo


class LeitorDeCurriculos:
    """Na vida real leria um arquivo ou uma fila. Aqui devolve dados fixos."""

    def ler(self) -> list[Curriculo]:
        return [
            Curriculo(1, "Ana Lima", 5, 14000, ["Python", "PostgreSQL", "REST", "Docker"], "São Paulo"),
            Curriculo(2, "Bruno Rocha", 1, 9000, ["Python", "REST"], "Recife"),
            Curriculo(3, None, 4, 15000, ["Python"], "Curitiba"),
            Curriculo(4, "Clara Mendes", 6, 22000, ["Python", "Docker"], "Belo Horizonte"),
            Curriculo(5, "Elena Souza", 7, 17000, ["python", "postgresql", "rest", "docker"], "Porto Alegre"),
            Curriculo(6, "Felipe Nunes", 3, 16000, ["Python", "REST"], "Salvador"),
        ]
