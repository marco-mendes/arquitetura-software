import os
from pathlib import Path
import subprocess

import pytest


LAB = Path(__file__).resolve().parents[1]
COMPOSE = "infra/compose.servicos.yml"


@pytest.mark.skipif(
    os.getenv("COMPOSE_LIVE") != "1",
    reason="execute com COMPOSE_LIVE=1 após docker compose up --wait",
)
def test_exames_cannot_resolve_or_connect_to_eligibility_database_network():
    probe = """
import psycopg

try:
    connection = psycopg.connect(
        'postgresql://elegibilidade:elegibilidade@elegibilidade-db:5432/elegibilidade',
        connect_timeout=2,
    )
    connection.execute('SELECT 1')
except psycopg.Error as error:
    print(type(error).__name__)
else:
    raise SystemExit('Exames alcançou indevidamente o banco de Elegibilidade')
"""
    result = subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            COMPOSE,
            "exec",
            "-T",
            "exames",
            "python",
            "-c",
            probe,
        ],
        cwd=LAB,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "OperationalError" in result.stdout
