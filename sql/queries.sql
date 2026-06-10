-- 1. Top 5 funds by AUM
SELECT f.scheme_name, a.aum_crore
FROM dim_fund f
JOIN fact_aum a ON f.amfi_code = a.amfi_code
ORDER BY a.aum_crore DESC
LIMIT 5;

-- 2. Transactions by State
SELECT state, COUNT(investor_id) as total_transactions, SUM(amount_inr) as total_volume_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_volume_inr DESC;

-- 3. Funds with expense ratio less than 1%
SELECT f.scheme_name, f.category, p.expense_ratio_pct
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct ASC;

-- 4. Average NAV per month for each fund
SELECT 
    f.scheme_name, 
    d.year, 
    d.month, 
    ROUND(AVG(n.nav), 2) as avg_nav
FROM fact_nav n
JOIN dim_date d ON n.date = d.date
JOIN dim_fund f ON n.amfi_code = f.amfi_code
GROUP BY f.scheme_name, d.year, d.month
ORDER BY f.scheme_name, d.year DESC, d.month DESC;

-- 5. SIP Year-over-Year (YoY) Growth
WITH yearly_sip AS (
    SELECT 
        d.year, 
        SUM(t.amount_inr) as total_sip_volume
    FROM fact_transactions t
    JOIN dim_date d ON t.transaction_date = d.date
    WHERE t.transaction_type = 'SIP'
    GROUP BY d.year
)
SELECT 
    year, 
    total_sip_volume,
    LAG(total_sip_volume) OVER (ORDER BY year) as prev_year_volume,
    ROUND(((total_sip_volume - LAG(total_sip_volume) OVER (ORDER BY year)) / LAG(total_sip_volume) OVER (ORDER BY year)) * 100, 2) as yoy_growth_pct
FROM yearly_sip;

-- 6. Total AUM by Mutual Fund House
SELECT 
    f.fund_house, 
    SUM(a.aum_crore) as total_aum_crore
FROM dim_fund f
JOIN fact_aum a ON f.amfi_code = a.amfi_code
GROUP BY f.fund_house
ORDER BY total_aum_crore DESC;

-- 7. Average Return by Risk Grade
SELECT 
    f.risk_grade, 
    ROUND(AVG(p.return_3yr_pct), 2) as avg_3yr_return, 
    ROUND(AVG(p.return_5yr_pct), 2) as avg_5yr_return
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
GROUP BY f.risk_grade
ORDER BY avg_5yr_return DESC;

-- 8. Transaction Volume by Age Group
SELECT 
    age_group, 
    COUNT(investor_id) as total_transactions, 
    SUM(amount_inr) as total_volume_inr
FROM fact_transactions
GROUP BY age_group
ORDER BY total_volume_inr DESC;

-- 9. Most Popular Payment Modes
SELECT 
    transaction_type, 
    payment_mode, 
    COUNT(*) as usage_count
FROM fact_transactions
GROUP BY transaction_type, payment_mode
ORDER BY transaction_type, usage_count DESC;

-- 10. Top 5 Funds Generating the Best "Alpha"
SELECT 
    f.scheme_name, 
    f.category, 
    p.alpha, 
    p.beta
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
ORDER BY p.alpha DESC
LIMIT 5;