-- CREATE TABLE
CREATE TABLE gold.tb_dim_ano (
    id_ano            SMALLINT NOT NULL COMMENT 'Surrogate key da dimensão',
    ds_ano            VARCHAR(4) NOT NULL COMMENT 'Ano no formato AAAA',
    id_ano_anterior_1 SMALLINT NOT NULL COMMENT 'Surrogate key da própria dimensão de ano para recuperar o ano A-1',
    id_ano_anterior_2 SMALLINT NOT NULL COMMENT 'Surrogate key da própria dimensão de ano para recuperar o ano A-2',
    fl_ano_bissexto   TINYINT NOT NULL COMMENT 'Flag que indica se o ano é bissexto (0=não; 1=sim)',
    dt_insr           DATETIME DEFAULT CURRENT_TIMESTAMP comment 'Data de inserção do registro na tabela'
);

ALTER TABLE gold.tb_dim_ano COMMENT 'Dimensão de tempo - ANO';

CREATE UNIQUE INDEX pk_dim_ano ON gold.tb_dim_ano ( id_ano ASC );

ALTER TABLE gold.tb_dim_ano ADD CONSTRAINT pk_dim_ano PRIMARY KEY ( id_ano );