"""
Demonstração completa — Estilo Arquitetural em Camadas
Sistema de Agendamento de Clínica Médica

Execução: python main.py
Sem dependências externas — apenas stdlib Python 3.10+
"""

from datetime import datetime

from dominio import CPF, Medico, Paciente
from repositorios import (
    InMemoriaRepositorioConsulta,
    InMemoriaRepositorioPaciente,
    InMemoriaRepositorioMedico,
)
from servicos import AgendamentoServico, RelatorioServico
from apresentacao import AgendaController


def secao(titulo: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {titulo}")
    print(f"{'─' * 60}")


def main():
    print("=" * 60)
    print("  SISTEMA DE AGENDAMENTO DE CLÍNICA MÉDICA")
    print("  Demonstração — Estilo Arquitetural em Camadas")
    print("=" * 60)

    # ── Camada de Dados (repositórios em memória) ──────────────
    repo_consulta  = InMemoriaRepositorioConsulta()
    repo_paciente  = InMemoriaRepositorioPaciente()
    repo_medico    = InMemoriaRepositorioMedico()

    # ── Dados iniciais ─────────────────────────────────────────
    dra_ana   = Medico(1, "Dra. Ana Silva",   "CRM/SP 12345", "Cardiologia")
    dr_joao   = Medico(2, "Dr. João Costa",   "CRM/SP 67890", "Clínica Geral")
    repo_medico.salvar(dra_ana)
    repo_medico.salvar(dr_joao)

    maria   = Paciente(1, "Maria Santos",   CPF("123.456.789-09"), "(11) 99999-1111")
    carlos  = Paciente(2, "Carlos Oliveira", CPF("987.654.321-00"), "(11) 99999-2222")
    lucia   = Paciente(3, "Lúcia Ferreira",  CPF("111.222.333-44"), "(11) 99999-3333")
    repo_paciente.salvar(maria)
    repo_paciente.salvar(carlos)
    repo_paciente.salvar(lucia)

    # ── Camada de Negócios ─────────────────────────────────────
    agendamento = AgendamentoServico(repo_consulta, repo_paciente, repo_medico)
    relatorio   = RelatorioServico(repo_consulta)

    # ── Camada de Apresentação ─────────────────────────────────
    controller = AgendaController(agendamento, relatorio)

    # ── Cenários de demonstração ───────────────────────────────

    secao("1. Agendando consultas válidas")
    print(controller.post_consulta({
        "paciente_id": 1, "medico_id": 1,
        "inicio": "2025-06-10T09:00:00", "fim": "2025-06-10T09:30:00",
    }))
    print(controller.post_consulta({
        "paciente_id": 2, "medico_id": 1,
        "inicio": "2025-06-10T10:00:00", "fim": "2025-06-10T10:30:00",
    }))
    print(controller.post_consulta({
        "paciente_id": 3, "medico_id": 2,
        "inicio": "2025-06-10T14:00:00", "fim": "2025-06-10T14:20:00",
    }))

    secao("2. Tentando agendar com CONFLITO de horário (esperado: HTTP 409)")
    print(controller.post_consulta({
        "paciente_id": 3, "medico_id": 1,
        "inicio": "2025-06-10T09:15:00", "fim": "2025-06-10T09:45:00",
    }))

    secao("3. Agenda do dia — Dra. Ana em 10/06/2025")
    print(controller.get_agenda(medico_id=1, data="2025-06-10"))

    secao("4. Realizando a consulta #1")
    print(controller.patch_consulta_realizar(1, "Paciente sem alterações. Retorno em 6 meses."))

    secao("5. Cancelando a consulta #2")
    print(controller.delete_consulta(2))

    secao("6. Tentando cancelar consulta já cancelada (esperado: HTTP 400)")
    print(controller.delete_consulta(2))

    secao("7. Agenda após alterações")
    print(controller.get_agenda(medico_id=1, data="2025-06-10"))

    secao("8. Histórico da paciente Maria")
    print(controller.get_historico_paciente(paciente_id=1))

    secao("9. OCP em ação — trocando implementação de repositório")
    print("   A camada de negócios (AgendamentoServico) não muda.")
    print("   Em produção, InMemoria* seria substituído por Postgres*.")
    print("   O contrato (ABC RepositorioConsulta) garante a troca sem impacto.")


if __name__ == "__main__":
    main()
