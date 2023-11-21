-- CREATE TABLE
CREATE TABLE gold.tb_dim_semana (
    id_semana              INT NOT NULL COMMENT 'Surrogate key da dimensão',
    ds_semana              VARCHAR(25) NOT NULL COMMENT 'Período de dias equivalente a semana no formato <dd-mm> a <dd-mm>',
    id_semana_anterior_1   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de semana para recuperar a semana S-1',
    id_semana_anterior_2   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de semana para recuperar a semana S-2',
    id_semana_anterior_3   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de semana para recuperar a semana s-3',
    id_semana_anterior_4   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de semana para recuperar a semana S-4',
    id_semana_ano_anterior INT NOT NULL COMMENT 'Surrogate key da própria dimensão de semana para recuperar a semana similar no ano anterior',
    nr_semana              TINYINT NOT NULL COMMENT 'Número da semana (sem o ano). Valores possíveis: de 1 a 52',
    dt_insr                DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de inserção do registro na tabela'
);

ALTER TABLE gold.tb_dim_semana COMMENT
    'Dimensão de tempo - SEMANA';

ALTER TABLE gold.tb_dim_semana ADD CONSTRAINT pk_dim_semana PRIMARY KEY ( id_semana ); 