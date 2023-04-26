{{ config(
        materialized = "view",  
        partition_by = {
            "field": "Album_type",
            "data_type": "string",
        },
        cluster_by = "Artist"
    ) 
}}

select
    -- identifiers
    {{ dbt_utils.surrogate_key(['Artist', 'Track']) }} as id,
    cast(Artist as string) as artist,
    cast(Track as string) as track,    
    cast(Album as string) as album,
    cast(Album_type as string) as album_type,
    cast(Danceability as numeric) as danceability,
    cast(Acousticness as numeric) as energy,
    cast(Tempo as numeric) as tempo,
    cast(Views as integer) as views,
    cast(Likes as integer) as likes,
    cast(Comments as integer) as comments,
    cast(Stream as integer) as stream,
    cast(dur_min as numeric) as dur_min
from {{ source("staging", "ingested")}}

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=false) %}
  limit 100
{% endif %}