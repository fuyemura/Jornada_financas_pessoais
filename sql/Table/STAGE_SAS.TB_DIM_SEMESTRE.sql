CREATE TABLE stage_sas.tb_dim_semestre (
    id_semestre              NUMBER(5) NOT NULL,
    ds_semestre              VARCHAR2(20 BYTE) NOT NULL,
    id_semestre_anterior_1   NUMBER(5) NOT NULL,
    id_semestre_ano_anterior NUMBER(5) NOT NULL,
    id_ano                   NUMBER(4) NOT NULL,
    nr_semestre              NUMBER(1) NOT NULL,
    dt_insr                  DATE DEFAULT sysdate
);

COMMENT ON TABLE stage_sas.tb_dim_semestre IS
    'Dimensão de tempo - SEMESTRE';

COMMENT ON COLUMN stage_sas.tb_dim_semestre.id_semestre IS
    'Surrogate key da dimensão';

COMMENT ON COLUMN stage_sas.tb_dim_semestre.ds_semestre IS
    'Semestre no formato S/AAAA';

COMMENT ON COLUMN stage_sas.tb_dim_semestre.id_semestre_anterior_1 IS
    'Surrogate key da própria dimensão de semestre para recuperar o semestre S-1';

COMMENT ON COLUMN stage_sas.tb_dim_semestre.id_semestre_ano_anterior IS
    'Surrogate key da própria dimensão de semestre para recuperar o semestre similar no ano anterior (S-2)';

COMMENT ON COLUMN stage_sas.tb_dim_semestre.id_ano IS
    'Surrogate key da dimensão de ano';

COMMENT ON COLUMN stage_sas.tb_dim_semestre.nr_semestre IS
    'Número do semestre (sem o ano). Valores possíveis: 1,2';

COMMENT ON COLUMN stage_sas.tb_dim_semestre.dt_insr IS
    'Data de inserção do registro na tabela';

CREATE UNIQUE INDEX stage_sas.pk_dim_semestre ON
    stage_sas.tb_dim_semestre (
        id_semestre
    ASC );