CREATE TABLE stage_sas.tb_dim_ano (
    id_ano            NUMBER(4) NOT NULL,
    ds_ano            VARCHAR2(4 BYTE) NOT NULL,
    id_ano_anterior_1 NUMBER(4) NOT NULL,
    id_ano_anterior_2 NUMBER(4) NOT NULL,
    fl_ano_bissexto   NUMBER(1) NOT NULL,
    dt_insr           DATE DEFAULT sysdate
);

COMMENT ON TABLE stage_sas.tb_dim_ano IS
    'Dimensão de tempo - ANO';

COMMENT ON COLUMN stage_sas.tb_dim_ano.id_ano IS
    'Surrogate key da dimensão';

COMMENT ON COLUMN stage_sas.tb_dim_ano.ds_ano IS
    'Ano no formato AAAA';

COMMENT ON COLUMN stage_sas.tb_dim_ano.id_ano_anterior_1 IS
    'Surrogate key da própria dimensão de ano para recuperar o ano A-1';

COMMENT ON COLUMN stage_sas.tb_dim_ano.id_ano_anterior_2 IS
    'Surrogate key da própria dimensão de ano para recuperar o ano A-2';

COMMENT ON COLUMN stage_sas.tb_dim_ano.fl_ano_bissexto IS
    'Flag que indica se o ano é bissexto (0=não; 1=sim)';

COMMENT ON COLUMN stage_sas.tb_dim_ano.dt_insr IS
    'Data de inserção do registro na tabela';

CREATE UNIQUE INDEX stage_sas.pk_dim_ano ON
    stage_sas.tb_dim_ano (
        id_ano
    ASC );