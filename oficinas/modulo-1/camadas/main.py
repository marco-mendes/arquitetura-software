"""Cenário que exercita as quatro camadas da agenda clínica."""

from apresentacao import ApresentacaoHTTP
from repositorios import RepositorioDeConsultas
from servicos import ServicoDeAgenda


def main() -> None:
    api = ApresentacaoHTTP(ServicoDeAgenda(RepositorioDeConsultas()))

    print("== Agendamentos válidos ==")
    api.post_consultas("Dra. Ana Silva", "Maria Santos", "09:00", "09:30")
    api.post_consultas("Dra. Ana Silva", "João Lima", "10:00", "10:30")
    api.post_consultas("Dr. Paulo Reis", "Ana Costa", "09:00", "09:30")

    print("\n== Conflito de horário ==")
    api.post_consultas("Dra. Ana Silva", "Carlos Dias", "09:15", "09:45")

    print("\n== Realizar e cancelar ==")
    api.post_realizacao(1)
    api.delete_consulta(2)

    print("\n== Agenda final ==")
    api.get_agenda()


if __name__ == "__main__":
    main()
