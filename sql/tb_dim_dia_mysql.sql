-- CREATE TABLE
CREATE TABLE gold.tb_dim_dia (
    id_dia              INT NOT NULL COMMENT 'Surrogate key da dimensão',
    dt_dia              DATETIME NOT NULL COMMENT 'Data no formato DD/MM/YYYY',
    ds_dia              VARCHAR(10) NOT NULL COMMENT 'Data no formato YYYY-MM-DD',
    id_dia_semana       INT NOT NULL COMMENT 'Surrogate key da dimensão de dia da semana',
    id_semana           INT NOT NULL COMMENT 'Surrogate key da dimensão de semana',
    id_mes              INT NOT NULL COMMENT 'Surrogate key da dimensão de mês',
    id_bimestre         INT NOT NULL COMMENT 'Surrogate key da dimensão de bimestre',
    id_trimestre        INT NOT NULL COMMENT 'Surrogate key da dimensão de trimestre',
    id_quadrimestre     INT NOT NULL COMMENT 'Surrogate key da dimensão de quadrimestre',
    id_semestre         INT NOT NULL COMMENT 'Surrogate key da dimensão de semestre',
    id_ano              SMALLINT NOT NULL COMMENT 'Surrogate key da dimensão de ano',
    id_dia_anterior     INT NOT NULL COMMENT 'Surrogate key da própria dimensão de dia para recuperar o dia D-1',
    id_dia_ano_anterior INT NOT NULL COMMENT 'Surrogate key da própria dimensão de dia para recuperar o dia D-365',
    nr_dia              TINYINT NOT NULL COMMENT 'Número do dia (sem o mês, e sem o ano). Valores possíveis: 1 à 31',
    nr_dia_ano          SMALLINT NOT NULL COMMENT 'Número do dia no ano. Valores possíveis: 1 à 365 (366 no caso de anos bissextos)',
    fl_dia_util         TINYINT NOT NULL COMMENT 'Flag que indica se a data corresponde a um dia útil (0 - não, 1 - sim). Foram considerados dias não úteis sábados e domingos. Também são considerados dias não úteis os feriados nacionais e municipais (de São Paulo) a partir de 2001',
    ds_estacao_ano      VARCHAR(20) NOT NULL COMMENT 'Estação do ano conforme calendário brasileiro. Valores possíveis: primavera, verão, outono e inverno',
    dt_insr             DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de inserção do registro na tabela',
    nr_semana_no_mes    DECIMAL(38, 0) COMMENT 'Número da semana dentro do mês (de 1 a 5)'
);

ALTER TABLE gold.tb_dim_dia COMMENT 'Dimensão de tempo - DIA';

CREATE INDEX idx_dim_dia_dt_dia ON gold.tb_dim_dia (dt_dia ASC );

CREATE INDEX idx_dim_dia_reports ON gold.tb_dim_dia (id_dia ASC, dt_dia ASC );

CREATE UNIQUE INDEX pk_dim_dia ON gold.tb_dim_dia (id_dia ASC );

ALTER TABLE gold.tb_dim_dia ADD CONSTRAINT pk_dim_dia PRIMARY KEY ( id_dia );