SELECT current_database() = 'elegibilidade' AS is_elegibilidade \gset
SELECT current_database() = 'exames' AS is_exames \gset

\if :is_elegibilidade
CREATE SCHEMA elegibilidade;
CREATE TABLE elegibilidade.beneficiarios (
    id text PRIMARY KEY,
    elegivel boolean NOT NULL
);
INSERT INTO elegibilidade.beneficiarios (id, elegivel)
VALUES ('paciente-001', true), ('paciente-002', false);
\elif :is_exames
CREATE SCHEMA exames;
CREATE TABLE exames.solicitacoes (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    beneficiario_id text NOT NULL,
    codigo_exame text NOT NULL,
    criado_em timestamptz NOT NULL DEFAULT now()
);
\else
\echo 'O banco deve se chamar elegibilidade ou exames'
\quit
\endif
