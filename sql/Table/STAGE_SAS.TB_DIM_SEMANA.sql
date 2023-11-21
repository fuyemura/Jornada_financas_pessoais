CREATE TABLE stage_sas.tb_dim_semana (
    id_semana              NUMBER(6) NOT NULL,
    ds_semana              VARCHAR2(25 BYTE) NOT NULL,
    id_semana_anterior_1   NUMBER(6) NOT NULL,
    id_semana_anterior_2   NUMBER(6) NOT NULL,
    id_semana_anterior_3   NUMBER(6) NOT NULL,
    id_semana_anterior_4   NUMBER(6) NOT NULL,
    id_semana_ano_anterior NUMBER(6) NOT NULL,
    nr_semana              NUMBER(2) NOT NULL,
    dt_insr                DATE DEFAULT sysdate
);

COMMENT ON TABLE stage_sas.tb_dim_semana IS
    'Dimensão de tempo - SEMANA';

COMMENT ON COLUMN stage_sas.tb_dim_semana.id_semana IS
    'Surrogate key da dimensão';

COMMENT ON COLUMN stage_sas.tb_dim_semana.ds_semana IS
    'Período de dias equivalente a semana no formato <dd-mm> a <dd-mm>';

COMMENT ON COLUMN stage_sas.tb_dim_semana.id_semana_anterior_1 IS
    'Surrogate key da própria dimensão de semana para recuperar a semana S-1';

COMMENT ON COLUMN stage_sas.tb_dim_semana.id_semana_anterior_2 IS
    'Surrogate key da própria dimensão de semana para recuperar a semana S-2';

COMMENT ON COLUMN stage_sas.tb_dim_semana.id_semana_anterior_3 IS
    'Surrogate key da própria dimensão de semana para recuperar a semana s-3';

COMMENT ON COLUMN stage_sas.tb_dim_semana.id_semana_anterior_4 IS
    'Surrogate key da própria dimensão de semana para recuperar a semana S-4';

COMMENT ON COLUMN stage_sas.tb_dim_semana.id_semana_ano_anterior IS
    'Surrogate key da própria dimensão de semana para recuperar a semana similar no ano anterior';

COMMENT ON COLUMN stage_sas.tb_dim_semana.nr_semana IS
    'Número da semana (sem o ano). Valores possíveis: de 1 a 52';

COMMENT ON COLUMN stage_sas.tb_dim_semana.dt_insr IS
    'Data de inserção do registro na tabela';

CREATE UNIQUE INDEX stage_sas.pk_dim_semana ON
    stage_sas.tb_dim_semana (
        id_semana
    ASC );