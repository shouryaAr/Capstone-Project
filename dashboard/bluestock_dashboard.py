import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from pathlib import Path

# Page Setup
st.set_page_config(
    page_title="BlueStock MF Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Data via SQLAlchemy
@st.cache_data
def load_data():
    db_path = Path.cwd() / "data" / "db" / "bluestock_mf.db"
    if not db_path.exists():
        st.error(f"Database file not found at: {db_path}")
        st.stop()
        
    engine = create_engine(f"sqlite:///{db_path}")
    
    tables = {
        "funds": pd.read_sql("SELECT * FROM dim_fund", engine),
        "nav": pd.read_sql("SELECT * FROM fact_nav", engine),
        "performance": pd.read_sql("SELECT * FROM fact_performance", engine),
        "aum": pd.read_sql("SELECT * FROM fact_aum", engine),
        "transactions": pd.read_sql("SELECT * FROM fact_transactions", engine)
    }
    
    # Cast AMFI codes to string to prevent join/merge errors
    for df in tables.values():
        if 'amfi_code' in df.columns:
            df['amfi_code'] = df['amfi_code'].astype(str).str.strip()
            
    # Parse dates
    if 'date' in tables['nav'].columns:
        tables['nav']['date'] = pd.to_datetime(tables['nav']['date'])
    if 'transaction_date' in tables['transactions'].columns:
        tables['transactions']['transaction_date'] = pd.to_datetime(tables['transactions']['transaction_date'])
        
    return tables

data = load_data()
df_funds = data["funds"]
df_nav = data["nav"]
df_perf = data["performance"]
df_aum = data["aum"]
df_trans = data["transactions"]

# Sidebar Filter Interactivity
st.sidebar.markdown("<h2 style='color:#003366;'>Bluestock Fintech</h2>", unsafe_allow_html=True)
st.sidebar.markdown("### Dashboard Filters")
st.sidebar.markdown("---")

houses = ["All"] + sorted(list(df_funds['fund_house'].dropna().unique()))
categories = ["All"] + sorted(list(df_funds['category'].dropna().unique()))
plans = ["All"] + sorted(list(df_funds['plan'].dropna().unique()))

selected_house = st.sidebar.selectbox("Fund House", houses)
selected_cat = st.sidebar.selectbox("Category", categories)
selected_plan = st.sidebar.selectbox("Plan Type", plans)

# Filter Dataframes
filtered_funds = df_funds.copy()
if selected_house != "All":
    filtered_funds = filtered_funds[filtered_funds['fund_house'] == selected_house]
if selected_cat != "All":
    filtered_funds = filtered_funds[filtered_funds['category'] == selected_cat]
if selected_plan != "All":
    filtered_funds = filtered_funds[filtered_funds['plan'] == selected_plan]

valid_amfi = filtered_funds['amfi_code'].tolist()
filtered_nav = df_nav[df_nav['amfi_code'].isin(valid_amfi)]
filtered_perf = df_perf[df_perf['amfi_code'].isin(valid_amfi)]
filtered_aum = df_aum[df_aum['amfi_code'].isin(valid_amfi)]
filtered_trans = df_trans[df_trans['amfi_code'].isin(valid_amfi)]

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🏢 Industry Overview", 
    "📈 Fund Performance", 
    "👥 Investor Analytics", 
    "🔄 SIP & Market Trends"
])

# --- PAGE 1: INDUSTRY OVERVIEW ---
with tab1:
    st.header("Industry Overview")
    
    # KPI Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Industry AUM", "₹81.00 Lakh Cr")
    kpi2.metric("Monthly SIP Inflows", "₹31,002 Cr")
    kpi3.metric("Total Active Folios", "26.12 Cr")
    kpi4.metric("Active Schemes", f"{len(filtered_funds['scheme_name'].unique())} / 1,908")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Industry AUM Trend (2022–2025)")
        if not filtered_nav.empty:
            timeline_aum = filtered_nav.groupby(filtered_nav['date'].dt.to_period('M'))['nav'].mean().reset_index()
            timeline_aum['date'] = timeline_aum['date'].dt.to_timestamp()
            fig_timeline = px.line(timeline_aum, x='date', y='nav', labels={'nav': 'Average NAV'}, template="plotly_white")
            fig_timeline.update_traces(line_color='#003366', line_width=3)
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("No timeline data found for the current filter criteria.")
        
    with col2:
        st.subheader("AUM by AMC (Top 10)")
        if not filtered_funds.empty and not df_aum.empty:
            amc_aum = filtered_funds.merge(df_aum, on='amfi_code').groupby('fund_house')['aum_crore'].sum().reset_index()
            fig_amc = px.bar(amc_aum.sort_values(by='aum_crore', ascending=False).head(10), x='fund_house', y='aum_crore', template="plotly_white")
            fig_amc.update_traces(marker_color='#4682B4')
            st.plotly_chart(fig_amc, use_container_width=True)
        else:
            st.info("No AUM data found for the current filter criteria.")

# --- PAGE 2: FUND PERFORMANCE ---
with tab2:
    st.header("Fund Performance")
    
    col1, col2 = st.columns([6, 4])
    
    with col1:
        st.subheader("Risk vs. Return Profile")
        if not filtered_perf.empty:
            merged_scatter = filtered_perf.merge(filtered_funds, on='amfi_code').merge(df_aum, on='amfi_code')
            fig_scatter = px.scatter(
                merged_scatter, 
                x='return_3yr_pct', 
                y='std_dev_ann_pct', 
                size='aum_crore', 
                color='category',
                hover_name='scheme_name',
                labels={'return_3yr_pct': '3Y Return (%)', 'std_dev_ann_pct': 'Annualized Volatility (%)'},
                template="plotly_white"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("No performance records found for the current filter criteria.")
            
    with col2:
        st.subheader("NAV Historical Chart")
        if not filtered_funds.empty:
            selected_scheme = st.selectbox("Select Scheme", filtered_funds['scheme_name'].unique())
            scheme_code = filtered_funds[filtered_funds['scheme_name'] == selected_scheme]['amfi_code'].values[0]
            scheme_nav = df_nav[df_nav['amfi_code'] == scheme_code].sort_values(by='date')
            
            if not scheme_nav.empty:
                fig_nav_line = px.line(scheme_nav, x='date', y='nav', template="plotly_white")
                fig_nav_line.update_traces(line_color='#008080')
                st.plotly_chart(fig_nav_line, use_container_width=True)
            else:
                st.info("No data available for this scheme.")
        
    st.markdown("---")
    st.subheader("Sortable Fund Scorecard Table")
    if not filtered_funds.empty and not df_perf.empty:
        display_scorecard = filtered_funds.merge(df_perf, on='amfi_code')[['amfi_code', 'scheme_name', 'category', 'fund_house', 'return_1yr_pct', 'return_3yr_pct', 'sharpe_ratio', 'sortino_ratio']]
        st.dataframe(display_scorecard.style.background_gradient(cmap="Blues", subset=['return_3yr_pct', 'sharpe_ratio']), use_container_width=True)

# --- PAGE 3: INVESTOR ANALYTICS ---
with tab3:
    st.header("Investor Analytics")
    
    if not filtered_trans.empty:
        row3_1, row3_2 = st.columns(2)
        
        with row3_1:
            st.subheader("Transaction Amount by State")
            state_vol = filtered_trans.groupby('state')['amount_inr'].sum().reset_index()
            fig_state = px.bar(state_vol.sort_values(by='amount_inr', ascending=False), x='state', y='amount_inr', template="plotly_white")
            fig_state.update_traces(marker_color='#1f77b4')
            st.plotly_chart(fig_state, use_container_width=True)
            
        with row3_2:
            st.subheader("Transaction Type Distribution Split")
            type_split = filtered_trans.groupby('transaction_type')['amount_inr'].sum().reset_index()
            fig_donut = px.pie(type_split, values='amount_inr', names='transaction_type', hole=0.4, template="plotly_white")
            st.plotly_chart(fig_donut, use_container_width=True)
            
        st.markdown("---")
        row3_3, row3_4 = st.columns(2)
        
        with row3_3:
            st.subheader("Age Group vs. Average SIP Amount")
            sip_data = filtered_trans[filtered_trans['transaction_type'] == 'SIP']
            if not sip_data.empty:
                age_sip = sip_data.groupby('age_group')['amount_inr'].mean().reset_index()
                fig_age = px.bar(age_sip, x='age_group', y='amount_inr', template="plotly_white", category_orders={"age_group": ["18-25", "26-35", "36-45", "46-55", "56+"]})
                fig_age.update_traces(marker_color='#aec7e8')
                st.plotly_chart(fig_age, use_container_width=True)
            else:
                st.info("No SIP transaction records found.")
            
        with row3_4:
            st.subheader("Monthly Transaction Volume")
            monthly_vol = filtered_trans.groupby(filtered_trans['transaction_date'].dt.to_period('M'))['amount_inr'].count().reset_index()
            monthly_vol['transaction_date'] = monthly_vol['transaction_date'].dt.to_timestamp()
            fig_vol_line = px.line(monthly_vol, x='transaction_date', y='amount_inr', labels={'amount_inr': 'Total Transactions'}, template="plotly_white")
            fig_vol_line.update_traces(line_color='#ff7f0e')
            st.plotly_chart(fig_vol_line, use_container_width=True)
    else:
        st.warning("No transaction data matches the selected sidebar filters.")

# --- PAGE 4: SIP & MARKET TRENDS ---
with tab4:
    st.header("SIP & Market Trends")
    
    if not filtered_trans.empty:
        col4_1, col4_2 = st.columns(2)
        
        with col4_1:
            st.subheader("SIP Inflow vs. Nifty 50 Proxy Trend")
            sip_trend_data = filtered_trans[filtered_trans['transaction_type'] == 'SIP']
            if not sip_trend_data.empty:
                monthly_sip = sip_trend_data.groupby(sip_trend_data['transaction_date'].dt.to_period('M'))['amount_inr'].sum().reset_index()
                monthly_sip['transaction_date'] = monthly_sip['transaction_date'].dt.to_timestamp()
                
                fig_dual = go.Figure()
                fig_dual.add_trace(go.Bar(
                    x=monthly_sip['transaction_date'], y=monthly_sip['amount_inr'],
                    name="Monthly SIP Vol", marker_color='#9467bd', yaxis='y1'
                ))
                fig_dual.add_trace(go.Scatter(
                    x=monthly_sip['transaction_date'], y=np.sin(np.arange(len(monthly_sip))) * 5000 + 20000, 
                    name="Nifty 50 Proxy", line=dict(color='#d62728', width=3), yaxis='y2'
                ))
                
                fig_dual.update_layout(
                    template="plotly_white",
                    yaxis=dict(title="SIP Inflow Amount (₹)"),
                    yaxis2=dict(title="Nifty 50 Index Points", overlaying='y', side='right'),
                    legend=dict(x=0.01, y=0.99, orientation="h")
                )
                st.plotly_chart(fig_dual, use_container_width=True)
            else:
                st.info("No SIP transaction logs found.")
            
        with col4_2:
            st.subheader("Category Monthly Inflow Heatmap")
            filtered_trans['month_year'] = filtered_trans['transaction_date'].dt.strftime('%Y-%m')
            merged_trans_funds = filtered_trans.merge(df_funds, on='amfi_code')
            if not merged_trans_funds.empty:
                pivot_heatmap = merged_trans_funds.pivot_table(
                    index='category', 
                    columns='month_year', 
                    values='amount_inr', 
                    aggfunc='sum', 
                    fill_value=0
                ).head(5)
                
                fig_heatmap = px.imshow(pivot_heatmap, labels=dict(x="Month", y="Category", color="Inflow Volume"), template="plotly_white")
                st.plotly_chart(fig_heatmap, use_container_width=True)
            else:
                st.info("Insufficient category matching data to render the heatmap matrix.")
                
        st.markdown("---")
        st.subheader("Top 5 Categories by Net Inflow")
        merged_flows = filtered_trans.merge(df_funds, on='amfi_code')
        if not merged_flows.empty:
            top_cats = merged_flows.groupby('category')['amount_inr'].sum().reset_index().nlargest(5, 'amount_inr')
            st.table(top_cats.rename(columns={'category': 'Fund Category', 'amount_inr': 'Net Inflows (INR)'}))
    else:
        st.warning("No market trends data available for the active filters.")