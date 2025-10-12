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

