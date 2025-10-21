WITH base AS (
    SELECT 
        data_pregao,
        codigo_negociacao,
        preco_medio_papel,
        DATE_TRUNC('month', data_pregao) AS mes
    FROM silver.cotacao_historica
    WHERE codigo_negociacao = 'ITSA4'
),
marcos AS (
    SELECT
        mes,
        MIN(data_pregao) AS primeiro_dia,
        MAX(data_pregao) AS ultimo_dia,
        MIN(data_pregao) 
            + (CAST((julian(MAX(data_pregao)) - julian(MIN(data_pregao))) / 2 AS INTEGER)) * INTERVAL 1 DAY 
            AS meio_dia
    FROM base
    GROUP BY mes
)
SELECT 
    b.data_pregao, 
    b.codigo_negociacao, 
    b.preco_medio_papel,
    CASE
        WHEN b.data_pregao = m.primeiro_dia THEN 'Primeiro dia'
        WHEN b.data_pregao = m.meio_dia THEN 'Meio do mês'
        WHEN b.data_pregao = m.ultimo_dia THEN 'Último dia'
    END AS tipo_dia
FROM base b
JOIN marcos m
  ON b.data_pregao IN (m.primeiro_dia, m.meio_dia, m.ultimo_dia)
ORDER BY b.data_pregao;




WITH tmp_max_cotacao AS
(
SELECT MAX(dt_pregao) max_dt_pregao
, cd_negociacao
FROM silver.stg_cotacao_historica
GROUP BY cd_negociacao
)
SELECT t1.dt_pregao
, t1.cd_negociacao
, t1.nm_empresa
, t1.vl_medio
FROM silver.stg_cotacao_historica t1
INNER JOIN tmp_max_cotacao t2
ON t1.cd_negociacao = t2.cd_negociacao 
AND t1.dt_pregao = t2.max_dt_pregao
WHERE t1.cd_negociacao IN ('TRXF11', 'BTLG11', 'TRBL11', 'ALZR11', 'XPML11', 'KNSC11', 'IRDM11', 'AFHI11', 'VGIR11', 'RZTR11', 'VGIA11', 'CPTI11')
ORDER BY t1.cd_negociacao