-- Carregar extensão Delta
LOAD delta;

-- Criar schemas
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Mapear tabelas Delta na camada Silver
CREATE OR REPLACE VIEW bronze.cotahist AS
SELECT * FROM delta_scan('D:/Projetos/Jornada_financas_pessoais/data/delta/bronze/cotahist');

-- Mapear tabelas Delta na camada Silver
CREATE OR REPLACE VIEW silver.cotacao_historica AS
SELECT * FROM delta_scan('D:/Projetos/Jornada_financas_pessoais/data/delta/silver/cotacao_historica');

-- Ver todos os schemas
SELECT * FROM information_schema.schemata;

-- Ver todas as views em um schema
SELECT * FROM information_schema.tables WHERE table_schema = 'silver';