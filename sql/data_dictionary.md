# BlueStock Mutual Fund - Data Dictionary

## Dimension Tables

### `dim_fund`
Stores static information and categorizations for each mutual fund.
* **amfi_code** (INTEGER): Primary Key. The unique identifier for the mutual fund.
* **fund_house** (TEXT): The AMC (Asset Management Company) managing the fund.
* **scheme_name** (TEXT): The full name of the mutual fund scheme.
* **category** (TEXT): High-level classification (e.g., Equity, Debt).
* **sub_category** (TEXT): Specific classification (e.g., Large Cap, Liquid).
* **plan** (TEXT): Regular or Direct plan.
* **risk_grade** (TEXT): The risk classification assigned to the fund.

### `dim_date`
Calendar dimension used for time-series analytics.
* **date** (TEXT): Primary Key. Format YYYY-MM-DD.
* **year** (INTEGER): The year of the date.
* **month** (INTEGER): The month of the date (1-12).
* **day** (INTEGER): The day of the month.
* **quarter** (INTEGER): The fiscal quarter (1-4).
* **is_weekend** (BOOLEAN): True if the date falls on a Saturday or Sunday.

## Fact Tables

### `fact_nav`
Daily Net Asset Value (NAV) pricing for the funds.
* **amfi_code** (INTEGER): Foreign Key mapping to `dim_fund`.
* **date** (TEXT): Foreign Key mapping to `dim_date`.
* **nav** (REAL): The Net Asset Value price on that specific date.

### `fact_transactions`
Individual investor transactions (SIPs, Lumpsums, Redemptions).
* **investor_id** (TEXT): Unique ID for the investor executing the trade.
* **transaction_date** (TEXT): Foreign Key mapping to `dim_date`.
* **amfi_code** (INTEGER): Foreign Key mapping to `dim_fund`.
* **transaction_type** (TEXT): Type of trade (SIP, LUMPSUM, REDEMPTION).
* **amount_inr** (REAL): Transaction volume in Indian Rupees.
* **state / city / city_tier** (TEXT): Geographical data of the investor.
* **age_group / gender / annual_income_lakh** (TEXT/REAL): Demographic data.
* **payment_mode** (TEXT): Method of payment (UPI, Net Banking, etc.).
* **kyc_status** (TEXT): Verification status of the investor.

### `fact_performance`
Long-term performance metrics and risk ratios.
* **amfi_code** (INTEGER): Primary Key. Foreign Key mapping to `dim_fund`.
* **return_1yr_pct / 3yr / 5yr** (REAL): Historical percentage returns.
* **benchmark_3yr_pct** (REAL): The 3-year return of the fund's benchmark index.
* **alpha / beta** (REAL): Market volatility and performance metrics.
* **expense_ratio_pct** (REAL): The annual fee charged by the fund (validated 0.1 - 2.5).

### `fact_aum`
Assets Under Management for each fund.
* **amfi_code** (INTEGER): Primary Key. Foreign Key mapping to `dim_fund`.
* **aum_crore** (REAL): Total assets managed by the fund, measured in Crores.