SELECT current_database() = 'elegibilidade' AS is_elegibilidade \gset
SELECT current_database() = 'exames' AS is_exames \gset

\if :is_elegibilidade
CREATE ROLE elegibilidade LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD 'elegibilidade';
CREATE SCHEMA AUTHORIZATION elegibilidade;
SET ROLE elegibilidade;
CREATE TABLE elegibilidade.beneficiarios (
    id text PRIMARY KEY,
    elegivel boolean NOT NULL
);
INSERT INTO elegibilidade.beneficiarios (id, elegivel)
VALUES ('paciente-001', true), ('paciente-002', false);
RESET ROLE;
\elif :is_exames
CREATE ROLE exames LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD 'exames';
CREATE SCHEMA AUTHORIZATION exames;
SET ROLE exames;
CREATE TABLE exames.solicitacoes (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    beneficiario_id text NOT NULL,
    codigo_exame text NOT NULL,
    criado_em timestamptz NOT NULL DEFAULT now()
);
RESET ROLE;
\else
\echo 'O banco deve se chamar elegibilidade ou exames'
\quit
\endif
