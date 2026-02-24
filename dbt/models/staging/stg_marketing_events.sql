with src as (
    select * from raw_marketing_events
)
select
  cast(event_id as bigint) as event_id,
  cast(event_date as date) as event_date,
  channel,
  event_type,
  cast(application_id as bigint) as application_id
from src
