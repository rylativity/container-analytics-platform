WITH raw AS (
    SELECT SUM(CAST(CostPerItem AS FLOAT)*CAST(NumberOfItemsPurchased AS INT)) AS total
    FROM minio.test."transaction_data.csv"
),
bronze as (
    SELECT SUM(CAST(CostPerItem AS FLOAT)*CAST(NumberOfItemsPurchased AS INT)) AS total
    -- FROM minio.warehouse.bronze.transaction_data
    FROM {{ ref("transactions_bronze") }}
)
SELECT * from raw
LEFT JOIN bronze
ON raw.total = bronze.total
WHERE bronze.total != raw.total