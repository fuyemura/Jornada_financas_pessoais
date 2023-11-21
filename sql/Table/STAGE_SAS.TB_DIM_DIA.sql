CREATE TABLE stage_sas.tb_dim_dia (
    id_dia              NUMBER(8) NOT NULL,
    dt_dia              DATE NOT NULL,
    ds_dia              VARCHAR2(10) NOT NULL,
    id_dia_semana       NUMBER(6) NOT NULL,
    id_semana           NUMBER(6) NOT NULL,
    id_mes              NUMBER(6) NOT NULL,
    id_bimestre         NUMBER(5) NOT NULL,
    id_trimestre        NUMBER(5) NOT NULL,
    id_quadrimestre     NUMBER(6) NOT NULL,
    id_semestre         NUMBER(5) NOT NULL,
    id_ano              NUMBER(4) NOT NULL,
    id_dia_anterior     NUMBER(8) NOT NULL,
    id_dia_ano_anterior NUMBER(8) NOT NULL,
    nr_dia              NUMBER(2) NOT NULL,
    nr_dia_ano          NUMBER(3) NOT NULL,
    fl_dia_util         NUMBER(1) NOT NULL,
    ds_estacao_ano      VARCHAR2(20) NOT NULL,
    dt_insr             DATE DEFAULT sysdate,
    nr_semana_no_mes    NUMBER(*, 0)
);

COMMENT ON TABLE stage_sas.tb_dim_dia IS
    'Dimensão de tempo - DIA';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_dia IS
    'Surrogate key da dimensão';

COMMENT ON COLUMN stage_sas.tb_dim_dia.dt_dia IS
    'Data no formato DD/MM/YYYY';

COMMENT ON COLUMN stage_sas.tb_dim_dia.ds_dia IS
    'Data no formato YYYY-MM-DD';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_dia_semana IS
    'Surrogate key da dimensão de dia da semana';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_semana IS
    'Surrogate key da dimensão de semana';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_mes IS
    'Surrogate key da dimensão de mês';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_bimestre IS
    'Surrogate key da dimensão de bimestre';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_trimestre IS
    'Surrogate key da dimensão de trimestre';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_quadrimestre IS
    'Surrogate key da dimensão de quadrimestre';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_semestre IS
    'Surrogate key da dimensão de semestre';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_ano IS
    'Surrogate key da dimensão de ano';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_dia_anterior IS
    'Surrogate key da própria dimensão de dia para recuperar o dia D-1';

COMMENT ON COLUMN stage_sas.tb_dim_dia.id_dia_ano_anterior IS
    'Surrogate key da própria dimensão de dia para recuperar o dia D-365';

COMMENT ON COLUMN stage_sas.tb_dim_dia.nr_dia IS
    'Número do dia (sem o mês, e sem o ano). Valores possíveis: 1 à 31';

COMMENT ON COLUMN stage_sas.tb_dim_dia.nr_dia_ano IS
    'Número do dia no ano. Valores possíveis: 1 à 365 (366 no caso de anos bissextos)';

COMMENT ON COLUMN stage_sas.tb_dim_dia.fl_dia_util IS
    'Flag que indica se a data corresponde a um dia útil (0 - não, 1 - sim). Foram considerados dias não úteis sábados e domingos. Também são considerados dias não úteis os feriados nacionais e municipais (de São Paulo) a partir de 2001'
    ;

COMMENT ON COLUMN stage_sas.tb_dim_dia.ds_estacao_ano IS
    'Estação do ano conforme calendário brasileiro. Valores possíveis: primavera, verão, outono e inverno';

COMMENT ON COLUMN stage_sas.tb_dim_dia.dt_insr IS
    'Data de inserção do registro na tabela';

COMMENT ON COLUMN stage_sas.tb_dim_dia.nr_semana_no_mes IS
    'Número da semana dentro do mês (de 1 a 5)';

CREATE INDEX stage_sas.idx_dim_dia_dt_dia ON
    stage_sas.tb_dim_dia (
        dt_dia
    ASC );

CREATE INDEX stage_sas.idx_dim_dia_reports ON
    stage_sas.tb_dim_dia (
        id_dia
    ASC,
        dt_dia
    ASC );

CREATE UNIQUE INDEX stage_sas.pk_dim_dia ON
    stage_sas.tb_dim_dia (
        id_dia
    ASC );