WITH tmp_base AS (
    SELECT 
        data_pregao,
        codigo_ativo,
        preco_medio,
        DATE_TRUNC('month', data_pregao) AS mes
    FROM gold.fato_cotacao
    WHERE codigo_ativo = 'BBDC4'
),
tmp_marcos AS (
    SELECT
        mes,
        MIN(data_pregao) AS primeiro_dia,
        MAX(data_pregao) AS ultimo_dia,
        MIN(data_pregao) 
            + (CAST((julian(MAX(data_pregao)) - julian(MIN(data_pregao))) / 2 AS INTEGER)) * INTERVAL 1 DAY 
            AS meio_dia
    FROM tmp_base
    GROUP BY mes
)
SELECT 
    b.data_pregao, 
    b.codigo_ativo, 
    b.preco_medio,
    CASE
        WHEN b.data_pregao = m.primeiro_dia THEN 'Primeiro dia'
        WHEN b.data_pregao = m.meio_dia THEN 'Meio do mês'
        WHEN b.data_pregao = m.ultimo_dia THEN 'Último dia'
    END AS tipo_dia
FROM tmp_base b
JOIN tmp_marcos m
  ON b.data_pregao IN (m.primeiro_dia, m.meio_dia, m.ultimo_dia)
ORDER BY b.data_pregao;



WITH tmp_max_cotacao AS
(
SELECT MAX(dt_pregao) max_dt_pregao
, cd_ativo
FROM gold.fato_cotacao
GROUP BY cd_ativo
)
SELECT t1.dt_pregao
, t1.cd_ativo
, t1.nm_empresa
, t1.vl_medio
FROM gold.fato_cotacao t1
INNER JOIN tmp_max_cotacao t2
ON t1.cd_ativo = t2.cd_ativo
AND t1.dt_pregao = t2.max_dt_pregao
WHERE t1.cd_ativo IN ('TRXF11', 'BTLG11', 'TRBL11', 'ALZR11', 'XPML11', 'KNSC11', 'IRDM11', 'AFHI11', 'VGIR11', 'RZTR11', 'VGIA11', 'CPTI11')
ORDER BY t1.cd_ativo
;