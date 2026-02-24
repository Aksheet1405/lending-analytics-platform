with src as (
    select * from raw_payments
)
select
  cast(application_id as bigint) as application_id,
  cast(payment_month as int) as payment_month,
  cast(due_date as date) as due_date,
  cast(paid as int) as paid,
  cast(amount_paid as double) as amount_paid,
  cast(ending_balance_est as double) as ending_balance_est
from src
