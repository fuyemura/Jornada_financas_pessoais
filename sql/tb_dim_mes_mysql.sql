-- CREATE TABLE
CREATE TABLE gold.tb_dim_mes (
    id_mes              INT NOT NULL COMMENT 'Surrogate key da dimensão',
    id_bimestre         INT NOT NULL COMMENT 'Surrogate key da dimensão de bimestre',
    id_trimestre        INT NOT NULL COMMENT 'Surrogate key da dimensão de trimestre',
    id_quadrimestre     INT NOT NULL COMMENT 'Surrogate key da dimensão de quadrimestre',
    id_semestre         INT NOT NULL COMMENT 'Surrogate key da dimensão de semestre',
    id_ano              SMALLINT NOT NULL COMMENT 'Surrogate key da dimensão de ano',
    nr_mes              TINYINT NOT NULL COMMENT 'Número do mês (sem o ano). Valores possíveis: 1,2,3,4,5,6,7,8,9,10,11,12',
    ds_mes_ano          VARCHAR(40) NOT NULL COMMENT 'Mês ano por extenso no formato <nome do mês> de <ano>. Exemplo: janeiro de 2020',
    ds_mes_ano_abrev    VARCHAR(10) NOT NULL COMMENT 'Mês/ano abreviado no formato Mmm/AAAA. Exemplo: jan/2020',
    ds_mes_abrev        VARCHAR(3) NOT NULL COMMENT 'Mês abreviado no formato Mmm. Exemplo: Jan',
    ds_sigla_mes        VARCHAR(1) NOT NULL COMMENT 'Sigla inicial do mês no formato M. Exemplo: J para janeiro, F para fevereiro',
    id_mes_anterior_1   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de mês para recuperar o mês M-1',
    id_mes_anterior_2   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de mês para recuperar o mês M-2',
    id_mes_anterior_3   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de mês para recuperar o mês M-3',
    id_mes_anterior_4   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de mês para recuperar o mês M-4',
    id_mes_anterior_5   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de mês para recuperar o mês M-5',
    id_mes_anterior_6   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de mês para recuperar o mês M-6',
    id_mes_ano_anterior INT NOT NULL COMMENT 'Surrogate key da própria dimensão de mês para recuperar o mês similar no ano anterior',
    dt_insr             DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de inserção do registro na tabela'
);

ALTER TABLE gold.tb_dim_mes COMMENT 'Dimensão de tempo - MÊS';

ALTER TABLE gold.tb_dim_mes ADD CONSTRAINT pk_dim_mes PRIMARY KEY ( id_mes );