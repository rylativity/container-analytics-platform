WITH silver as (
    SELECT *, NumberOfItemsPurchased * CostPerItem as TransactionTotal
    FROM {{ ref("transactions_silver") }}
)
SELECT 
    UserId,
    SUM(TransactionTotal) as total_spend,
    AVG(TransactionTotal) as avg_spend_per_transaction,
    SUM(NumberOfItemsPurchased) as total_items_purchased,
    COUNT(DISTINCT(ItemCode)) as distinct_items_purchased
FROM silver
GROUP BY UserId