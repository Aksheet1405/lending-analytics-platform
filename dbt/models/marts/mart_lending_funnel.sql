with a as (
  select * from {{ ref('stg_applications') }}
),
m as (
  select
    channel,
    application_id,
    count(*) filter (where event_type = 'click') as clicks,
    count(*) filter (where event_type = 'impression') as impressions
  from {{ ref('stg_marketing_events') }}
  group by 1,2
)
select
  a.application_id,
  a.application_date,
  a.channel,
  a.state,
  a.risk_tier,
  a.annual_income,
  a.dti,
  a.fico_score,
  a.requested_amount,
  a.approved,
  a.apr,
  a.term_months,
  coalesce(m.clicks, 0) as clicks,
  coalesce(m.impressions, 0) as impressions
from a
left join m using (application_id, channel)
