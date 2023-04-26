{{ config(materialized = "view") }}

select * from {{ ref('stg_sandy_data') }}