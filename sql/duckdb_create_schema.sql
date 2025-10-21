-- Carregar extensão Delta
LOAD delta;

-- Criar schemas
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Mapear tabelas Delta na camada Silver
CREATE OR REPLACE VIEW bronze.raw_cotahist AS
SELECT * FROM delta_scan('D:/Projetos/Jornada_financas_pessoais/data/delta/bronze/raw_cotahist');

-- Mapear tabelas Delta na camada Silver
CREATE OR REPLACE VIEW silver.stg_cotacao_historica AS
SELECT * FROM delta_scan('D:/Projetos/Jornada_financas_pessoais/data/delta/silver/stg_cotacao_historica');

-- Mapear tabelas Delta na camada Gold
CREATE OR REPLACE VIEW gold.dim_ativo_financeiro AS
SELECT * FROM delta_scan('D:/Projetos/Jornada_financas_pessoais/data/delta/gold/dim_ativo_financeiro');

-- Mapear tabelas Delta na camada Gold
CREATE OR REPLACE VIEW gold.fato_cotacao AS
SELECT 
    t1.sk_ativo,
    t2.cd_ativo,
    t2.nm_empresa,
    t2.ds_ativo,
    t2.cd_tipo_mercado,
    t2.ds_tipo_mercado,
    t2.ds_tipo_ativo,
    dt_pregao,
    vl_abertura,
    vl_minimo,
    vl_maximo,
    vl_medio,
    vl_ultimo_negocio,
    qt_negocios,
    qt_titulos,
    vl_volume,
    t1.ts_insercao
FROM delta_scan('D:/Projetos/Jornada_financas_pessoais/data/delta/gold/fato_cotacao') t1
LEFT JOIN delta_scan('D:/Projetos/Jornada_financas_pessoais/data/delta/gold/dim_ativo_financeiro') t2
ON t1.sk_ativo = t2.sk_ativo



-- Ver todos os schemas
SELECT * FROM information_schema.schemata;

-- Ver todas as views em um schema
SELECT * FROM information_schema.tables WHERE table_schema = 'silver';