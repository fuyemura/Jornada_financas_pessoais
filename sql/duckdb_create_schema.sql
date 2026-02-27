-- Carregar extensão Delta
LOAD delta;

-- Criar schemas
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Mapear tabelas Delta na camada Bronze
CREATE OR REPLACE VIEW bronze.raw_cotahist AS
SELECT * FROM delta_scan('D:/Projetos/jornada_financas_pessoais/data/bronze/raw_cotahist');

CREATE OR REPLACE VIEW bronze.raw_cadcliente AS
SELECT * FROM delta_scan('D:/Projetos/jornada_financas_pessoais/data/delta/bronze/raw_cadcliente');

CREATE OR REPLACE VIEW bronze.raw_controleativo AS
SELECT * FROM delta_scan('D:/Projetos/jornada_financas_pessoais/data/delta/bronze/raw_controleativo');

-- Mapear tabelas Delta na camada Silver
CREATE OR REPLACE VIEW silver.stg_cotacao_historica AS
SELECT * FROM delta_scan('D:/Projetos/jornada_financas_pessoais/data/silver/stg_cotacao_historica');

CREATE OR REPLACE VIEW silver.stg_controle_ativo AS
SELECT * FROM delta_scan('D:/Projetos/jornada_financas_pessoais/data/delta/silver/stg_controle_ativo');

-- Mapear tabelas Delta na camada Gold
CREATE OR REPLACE VIEW gold.dim_tempo AS
SELECT * FROM delta_scan('D:/Projetos/jornada_financas_pessoais/data/delta/gold/dim_tempo');

CREATE OR REPLACE VIEW gold.dim_ativo_financeiro AS
SELECT * FROM delta_scan('D:/Projetos/jornada_financas_pessoais/data/delta/gold/dim_ativo_financeiro');

CREATE OR REPLACE VIEW gold.dim_cliente AS
SELECT * FROM delta_scan('D:/Projetos/jornada_financas_pessoais/data/delta/gold/dim_cliente');

CREATE OR REPLACE VIEW gold.fato_cotacao AS
SELECT 
    data_pregao,
    t1.id_ativo_financeiro,
    t2.codigo_ativo,
    t2.nome_empresa,
    t2.descricao_ativo,
    preco_abertura,
    preco_minimo,
    preco_maximo,
    preco_medio,
    preco_ultimo_negocio,
    quantidade_negocio,
    quantidade_titulo,
    volume_financeiro,
    t1.criado_em
FROM delta_scan('D:/Projetos/jornada_financas_pessoais/data/gold/fato_cotacao') t1
LEFT JOIN delta_scan('D:/Projetos/jornada_financas_pessoais/data/gold/dim_ativo_financeiro') t2
ON t1.id_ativo_financeiro = t2.id_ativo_financeiro

CREATE OR REPLACE VIEW gold.fato_carteira AS
SELECT 
    dt_carteira,
    t1.sk_cliente,
    t2.cd_cpf_pessoa,
    t2.nm_cliente,
    t1.sk_ativo,
    t3.cd_ativo,
    t3.nm_empresa,
    t3.ds_ativo,
    qt_ativo,
    vl_ativo,
    vl_pmedio,
    vl_investido,
    vl_carteira,
    t1.ts_insercao
FROM delta_scan('D:/Projetos/jornada_financas_pessoais/data/delta/gold/fato_carteira') t1
LEFT JOIN delta_scan('D:/Projetos/jornada_financas_pessoais/data/delta/gold/dim_cliente') t2
ON t1.sk_cliente = t2.sk_cliente
LEFT JOIN delta_scan('D:/Projetos/jornada_financas_pessoais/data/delta/gold/dim_ativo_financeiro') t3
ON t1.sk_ativo = t3.sk_ativo

-- Ver todos os schemas
SELECT * FROM information_schema.schemata;

-- Ver todas as views em um schema
SELECT * FROM information_schema.tables WHERE table_schema = 'silver';