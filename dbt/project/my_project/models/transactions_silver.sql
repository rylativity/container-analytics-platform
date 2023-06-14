{{
    config(
        materialized='incremental',
        unique_key='TransactionId'
    )
}}

WITH transactions_silver as (
  SELECT 
      CASE
          WHEN UserId = '-1' THEN 'Unknown'
          ELSE UserId
      END AS UserId,
      TransactionId,
      TO_TIMESTAMP(TransactionTime, 'YYYY-MM-DD HH24:MI:SS') as TransactionTime,
      ItemCode,
      ItemDescription,
      CAST(NumberOfItemsPurchased AS INTEGER) as NumberOfItemsPurchased,
      CAST(CostPerItem AS FLOAT) as CostPerItem,
      Country

  FROM {{ ref("transactions_bronze") }}
  
  -- Intentional Failure to trigger DBT Test Failure
  WHERE UserId != '364791'
)

SELECT * FROM transactions_silver
{% if is_incremental() %}
  -- this filter will only be applied on an incremental run
  WHERE TransactionId NOT IN (SELECT TransactionId FROM {{ this }})
{% endif %}
