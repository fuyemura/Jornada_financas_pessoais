CREATE TABLE stage_sas.tb_dim_dia_semana (
    id_dia_semana       NUMBER(6) NOT NULL,
    ds_dia_semana       VARCHAR2(20 BYTE) NOT NULL,
    ds_dia_semana_abrev VARCHAR2(3 BYTE) NOT NULL,
    ds_sigla_dia_semana VARCHAR2(3 BYTE) NOT NULL,
    dt_insr             DATE DEFAULT sysdate
);

COMMENT ON TABLE stage_sas.tb_dim_dia_semana IS
    'Dimensão de tempo - DIA DA SEMANA';

COMMENT ON COLUMN stage_sas.tb_dim_dia_semana.id_dia_semana IS
    'Surrogate key da dimensão';

COMMENT ON COLUMN stage_sas.tb_dim_dia_semana.ds_dia_semana IS
    'Dia da semana por extenso';

COMMENT ON COLUMN stage_sas.tb_dim_dia_semana.ds_dia_semana_abrev IS
    'Dia da semana abreviado no formato. Exemplo: dom, seg';

COMMENT ON COLUMN stage_sas.tb_dim_dia_semana.ds_sigla_dia_semana IS
    'Sigla inicial do dia da semana. Exemplo: D para domingo, S para segunda';

COMMENT ON COLUMN stage_sas.tb_dim_dia_semana.dt_insr IS
    'Data de inserção do registro na tabela';

CREATE UNIQUE INDEX stage_sas.pk_dim_dia_semana ON
    stage_sas.tb_dim_dia_semana (
        id_dia_semana
    ASC );