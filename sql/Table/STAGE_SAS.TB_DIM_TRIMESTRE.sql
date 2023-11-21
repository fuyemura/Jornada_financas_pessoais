CREATE TABLE stage_sas.tb_dim_trimestre (
    id_trimestre              NUMBER(5) NOT NULL,
    ds_trimestre              VARCHAR2(20 BYTE) NOT NULL,
    id_trimestre_anterior_1   NUMBER(5) NOT NULL,
    id_trimestre_anterior_2   NUMBER(5) NOT NULL,
    id_trimestre_anterior_3   NUMBER(5) NOT NULL,
    id_trimestre_ano_anterior NUMBER(5) NOT NULL,
    id_ano                    NUMBER(4) NOT NULL,
    id_semestre               NUMBER(5) NOT NULL,
    nr_trimestre              NUMBER(1) NOT NULL,
    dt_insr                   DATE DEFAULT sysdate
);

COMMENT ON TABLE stage_sas.tb_dim_trimestre IS
    'Dimensão de tempo - TRIMESTRE';

COMMENT ON COLUMN stage_sas.tb_dim_trimestre.id_trimestre IS
    'Surrogate key da dimensão';

COMMENT ON COLUMN stage_sas.tb_dim_trimestre.ds_trimestre IS
    'Trimestre no formato T/AAAA';

COMMENT ON COLUMN stage_sas.tb_dim_trimestre.id_trimestre_anterior_1 IS
    'Surrogate key da própria dimensão de trimestre para recuperar o trimestre t-1';

COMMENT ON COLUMN stage_sas.tb_dim_trimestre.id_trimestre_anterior_2 IS
    'Surrogate key da própria dimensão de trimestre para recuperar o trimestre T-2';

COMMENT ON COLUMN stage_sas.tb_dim_trimestre.id_trimestre_anterior_3 IS
    'Surrogate key da própria dimensão de trimestre para recuperar o trimestre T-3';

COMMENT ON COLUMN stage_sas.tb_dim_trimestre.id_trimestre_ano_anterior IS
    'Surrogate key da própria dimensão de trimestre para recuperar o trimestre similar no ano anterior (T-4)';

COMMENT ON COLUMN stage_sas.tb_dim_trimestre.id_ano IS
    'Surrogate key da dimensão de ano';

COMMENT ON COLUMN stage_sas.tb_dim_trimestre.id_semestre IS
    'Surrogate key da dimensão de semestre';

COMMENT ON COLUMN stage_sas.tb_dim_trimestre.nr_trimestre IS
    'Número do trimestre (sem o ano). Valores possíveis: 1,2,3,4';

COMMENT ON COLUMN stage_sas.tb_dim_trimestre.dt_insr IS
    'Data de inserção do registro na tabela';

CREATE UNIQUE INDEX stage_sas.pk_dim_trimestre ON
    stage_sas.tb_dim_trimestre (
        id_trimestre
    ASC );