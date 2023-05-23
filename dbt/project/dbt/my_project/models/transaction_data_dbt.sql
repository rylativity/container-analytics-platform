with transaction_data_dbt as (

    select *
    from minio.test."transaction_data.csv"

)
select * from transaction_data_dbt