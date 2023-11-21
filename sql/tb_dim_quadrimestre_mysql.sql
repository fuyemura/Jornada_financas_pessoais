-- CREATE TABLE
CREATE TABLE gold.tb_dim_quadrimestre (
    id_quadrimestre              INT NOT NULL COMMENT 'Surrogate key da dimensão',
    ds_quadrimestre              VARCHAR(15) NOT NULL COMMENT 'Semestre no formato Q/AAAA',
    id_quadrimestre_anterior_1   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de quadrimestre para recuperar o quadrimestre Q-1',
    id_quadrimestre_anterior_2   INT NOT NULL COMMENT 'Surrogate key da própria dimensão de quadrimestre para recuperar o quadrimestre Q-2',
    id_quadrimestre_ano_anterior INT NOT NULL COMMENT 'Surrogate key da própria dimensão de quadrimestre para recuperar o quadrimestre similar no ano anterior (Q-3)',
    id_ano                       SMALLINT NOT NULL COMMENT 'Surrogate key da dimensão de ano',
    nr_quadrimestre              TINYINT NOT NULL COMMENT 'Número do quadrimestre (sem o ano). Valores possíveis: 1, 2, 3',
    dt_insr                      DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT  'Data de inserção do registro na tabela'
);

ALTER TABLE gold.tb_dim_quadrimestre COMMENT
    'Dimensão de tempo - QUADRIMESTRE';

ALTER TABLE gold.tb_dim_quadrimestre ADD CONSTRAINT pk_dim_quadrimestre PRIMARY KEY ( id_quadrimestre );