with src as (
    select * from raw_applications
)
select
  cast(application_id as bigint) as application_id,
  cast(application_date as date) as application_date,
  channel,
  state,
  risk_tier,
  cast(annual_income as bigint) as annual_income,
  cast(dti as double) as dti,
  cast(fico_score as int) as fico_score,
  cast(requested_amount as bigint) as requested_amount,
  cast(approved as int) as approved,
  cast(apr as double) as apr,
  cast(term_months as int) as term_months
from src
