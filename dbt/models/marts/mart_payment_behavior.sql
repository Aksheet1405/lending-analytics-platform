select
  application_id,
  payment_month,
  due_date,
  paid,
  amount_paid,
  ending_balance_est
from {{ ref('stg_payments') }}
