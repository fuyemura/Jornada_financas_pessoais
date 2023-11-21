-- CREATE TABLE
CREATE TABLE gold.tb_dim_dia_semana (
    id_dia_semana       INT NOT NULL COMMENT 'Surrogate key da dimensão',
    ds_dia_semana       VARCHAR(20) NOT NULL COMMENT 'Dia da semana por extenso',
    ds_dia_semana_abrev VARCHAR(3) NOT NULL COMMENT 'Dia da semana abreviado no formato. Exemplo: dom, seg',
    ds_sigla_dia_semana VARCHAR(3) NOT NULL COMMENT 'Sigla inicial do dia da semana. Exemplo: D para domingo, S para segunda',
    dt_insr             DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de inserção do registro na tabela'
);

ALTER TABLE gold.tb_dim_dia_semana COMMENT 'Dimensão de tempo - DIA DA SEMANA';

ALTER TABLE gold.tb_dim_dia_semana ADD CONSTRAINT pk_dim_dia_semana PRIMARY KEY ( id_dia_semana );