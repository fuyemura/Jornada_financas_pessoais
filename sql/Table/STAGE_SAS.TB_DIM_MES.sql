CREATE TABLE stage_sas.tb_dim_mes (
    id_mes              NUMBER(6) NOT NULL,
    id_bimestre         NUMBER(5) NOT NULL,
    id_trimestre        NUMBER(5) NOT NULL,
    id_quadrimestre     NUMBER(5) NOT NULL,
    id_semestre         NUMBER(5) NOT NULL,
    id_ano              NUMBER(4) NOT NULL,
    nr_mes              NUMBER(2) NOT NULL,
    ds_mes_ano          VARCHAR2(40 BYTE) NOT NULL,
    ds_mes_ano_abrev    VARCHAR2(10 BYTE) NOT NULL,
    ds_mes_abrev        VARCHAR2(3 BYTE) NOT NULL,
    ds_sigla_mes        VARCHAR2(1 BYTE) NOT NULL,
    id_mes_anterior_1   NUMBER(6) NOT NULL,
    id_mes_anterior_2   NUMBER(6) NOT NULL,
    id_mes_anterior_3   NUMBER(6) NOT NULL,
    id_mes_anterior_4   NUMBER(6) NOT NULL,
    id_mes_anterior_5   NUMBER(6) NOT NULL,
    id_mes_anterior_6   NUMBER(6) NOT NULL,
    id_mes_ano_anterior NUMBER(6) NOT NULL,
    dt_insr             DATE DEFAULT sysdate
);

COMMENT ON TABLE stage_sas.tb_dim_mes IS
    'Dimensão de tempo - MÊS';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_mes IS
    'Surrogate key da dimensão';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_bimestre IS
    'Surrogate key da dimensão de bimestre';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_trimestre IS
    'Surrogate key da dimensão de trimestre';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_quadrimestre IS
    'Surrogate key da dimensão de quadrimestre';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_semestre IS
    'Surrogate key da dimensão de semestre';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_ano IS
    'Surrogate key da dimensão de ano';

COMMENT ON COLUMN stage_sas.tb_dim_mes.nr_mes IS
    'Número do mês (sem o ano). Valores possíveis: 1,2,3,4,5,6,7,8,9,10,11,12';

COMMENT ON COLUMN stage_sas.tb_dim_mes.ds_mes_ano IS
    'Mês ano por extenso no formato <nome do mês> de <ano>. Exemplo: janeiro de 2020';

COMMENT ON COLUMN stage_sas.tb_dim_mes.ds_mes_ano_abrev IS
    'Mês/ano abreviado no formato Mmm/AAAA. Exemplo: jan/2020';

COMMENT ON COLUMN stage_sas.tb_dim_mes.ds_mes_abrev IS
    'Mês abreviado no formato Mmm. Exemplo: Jan';

COMMENT ON COLUMN stage_sas.tb_dim_mes.ds_sigla_mes IS
    'Sigla inicial do mês no formato M. Exemplo: J para janeiro, F para fevereiro';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_mes_anterior_1 IS
    'Surrogate key da própria dimensão de mês para recuperar o mês M-1';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_mes_anterior_2 IS
    'Surrogate key da própria dimensão de mês para recuperar o mês M-2';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_mes_anterior_3 IS
    'Surrogate key da própria dimensão de mês para recuperar o mês M-3';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_mes_anterior_4 IS
    'Surrogate key da própria dimensão de mês para recuperar o mês M-4';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_mes_anterior_5 IS
    'Surrogate key da própria dimensão de mês para recuperar o mês M-5';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_mes_anterior_6 IS
    'Surrogate key da própria dimensão de mês para recuperar o mês M-6';

COMMENT ON COLUMN stage_sas.tb_dim_mes.id_mes_ano_anterior IS
    'Surrogate key da própria dimensão de mês para recuperar o mês similar no ano anterior';

COMMENT ON COLUMN stage_sas.tb_dim_mes.dt_insr IS
    'Data de inserção do registro na tabela';

CREATE UNIQUE INDEX stage_sas.pk_dim_mes ON
    stage_sas.tb_dim_mes (
        id_mes
    ASC );