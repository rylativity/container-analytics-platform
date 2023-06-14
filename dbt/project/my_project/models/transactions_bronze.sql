{{
    config(
        materialized='incremental',
        unique_key='TransactionId'
    )
}}

WITH transactions_raw as (SELECT *
FROM minio.test."transaction_data.csv")

SELECT * FROM transactions_raw

{% if is_incremental() %}
  -- this filter will only be applied on an incremental run
  WHERE TransactionId NOT IN (SELECT TransactionId FROM {{ this }})
{% endif %}