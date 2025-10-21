WITH tmp_base AS (
    SELECT 
        dt_pregao,
        cd_ativo,
        vl_medio,
        DATE_TRUNC('month', dt_pregao) AS mes
    FROM gold.fato_cotacao
    WHERE cd_ativo = 'ITSA4'
),
tmp_marcos AS (
    SELECT
        mes,
        MIN(dt_pregao) AS primeiro_dia,
        MAX(dt_pregao) AS ultimo_dia,
        MIN(dt_pregao) 
            + (CAST((julian(MAX(dt_pregao)) - julian(MIN(dt_pregao))) / 2 AS INTEGER)) * INTERVAL 1 DAY 
            AS meio_dia
    FROM tmp_base
    GROUP BY mes
)
SELECT 
    b.dt_pregao, 
    b.cd_ativo, 
    b.vl_medio,
    CASE
        WHEN b.dt_pregao = m.primeiro_dia THEN 'Primeiro dia'
        WHEN b.dt_pregao = m.meio_dia THEN 'Meio do mês'
        WHEN b.dt_pregao = m.ultimo_dia THEN 'Último dia'
    END AS tipo_dia
FROM tmp_base b
JOIN tmp_marcos m
  ON b.dt_pregao IN (m.primeiro_dia, m.meio_dia, m.ultimo_dia)
ORDER BY b.dt_pregao
;




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