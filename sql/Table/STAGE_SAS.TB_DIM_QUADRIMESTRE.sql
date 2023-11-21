CREATE TABLE stage_sas.tb_dim_quadrimestre (
    id_quadrimestre              NUMBER(6) NOT NULL,
    ds_quadrimestre              VARCHAR2(15 BYTE) NOT NULL,
    id_quadrimestre_anterior_1   NUMBER(6) NOT NULL,
    id_quadrimestre_anterior_2   NUMBER(6) NOT NULL,
    id_quadrimestre_ano_anterior NUMBER(6) NOT NULL,
    id_ano                       NUMBER(4) NOT NULL,
    nr_quadrimestre              NUMBER(1) NOT NULL,
    dt_insr                      DATE DEFAULT sysdate
);

COMMENT ON TABLE stage_sas.tb_dim_quadrimestre IS
    'Dimensão de tempo - QUADRIMESTRE';

COMMENT ON COLUMN stage_sas.tb_dim_quadrimestre.id_quadrimestre IS
    'Surrogate key da dimensão';

COMMENT ON COLUMN stage_sas.tb_dim_quadrimestre.ds_quadrimestre IS
    'Semestre no formato Q/AAAA';

COMMENT ON COLUMN stage_sas.tb_dim_quadrimestre.id_quadrimestre_anterior_1 IS
    'Surrogate key da própria dimensão de quadrimestre para recuperar o quadrimestre Q-1';

COMMENT ON COLUMN stage_sas.tb_dim_quadrimestre.id_quadrimestre_anterior_2 IS
    'Surrogate key da própria dimensão de quadrimestre para recuperar o quadrimestre Q-2';

COMMENT ON COLUMN stage_sas.tb_dim_quadrimestre.id_quadrimestre_ano_anterior IS
    'Surrogate key da própria dimensão de quadrimestre para recuperar o quadrimestre similar no ano anterior (Q-3)';

COMMENT ON COLUMN stage_sas.tb_dim_quadrimestre.id_ano IS
    'Surrogate key da dimensão de ano';

COMMENT ON COLUMN stage_sas.tb_dim_quadrimestre.nr_quadrimestre IS
    'Número do quadrimestre (sem o ano). Valores possíveis: 1, 2, 3';

COMMENT ON COLUMN stage_sas.tb_dim_quadrimestre.dt_insr IS
    'Data de inserção do registro na tabela';

CREATE UNIQUE INDEX stage_sas.pk_dim_quadrimestre ON
    stage_sas.tb_dim_quadrimestre (
        id_quadrimestre
    ASC );