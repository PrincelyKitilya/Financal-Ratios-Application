import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Financial Ratios Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark mode compatible CSS
st.markdown("""
<style>
    /* Main title */
    .main-header {
        font-size: 2.5rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    /* Company header - dark mode compatible */
    .company-header {
        background: linear-gradient(90deg, #2c3e50, #34495e);
        color: #ecf0f1;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-weight: 600;
        border-left: 4px solid #3498db;
    }

    /* Warning box for alerts - visible on dark background */
    .warning-box {
        background-color: rgba(255, 193, 7, 0.2);
        border: 1px solid #ffc107;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #ffd54f;
    }

    /* Insight box - visible on dark background */
    .insight-box {
        background-color: rgba(23, 162, 184, 0.2);
        border: 1px solid #17a2b8;
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #4dd0e1;
    }

    /* Success box */
    .success-box {
        background-color: rgba(40, 167, 69, 0.2);
        border: 1px solid #28a745;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #6fcf97;
    }

    /* Metric card */
    .metric-card {
        background-color: rgba(52, 58, 64, 0.5);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #2c3e50;
        border-radius: 5px 5px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #3498db !important;
        color: white !important;
    }

    /* Dataframe styling */
    .stDataFrame {
        background-color: rgba(0,0,0,0.1);
    }

    /* Make text more readable on dark background */
    .stMarkdown, .stText, .stMetric {
        color: #ecf0f1 !important;
    }
    
    #background-color: #2c3e50;
    /* Streamlit widget styling */
    .stSelectbox, .stMultiselect, .stSlider, .stNumberInput {
        color: white;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }

    /* Plotly chart background fix */
    .js-plotly-plot .plotly {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown('<h1 class="main-header">Financial Ratios Dashboard - 3 Company Comparison</h1>', unsafe_allow_html=True)


@st.cache_data
def load_and_clean_data():
    """Load and clean the financial data"""
    try:
        # Load data
        master_df = pd.read_excel("./pipeline/master_ratios.xlsx")
        master_inputs_df = pd.read_excel("./pipeline/master_inputs.xlsx")

        # Clean column names
        master_df.columns = master_df.columns.str.strip()
        master_inputs_df.columns = master_inputs_df.columns.str.strip()

        # Clean master_inputs - remove duplicate depreciation entries
        master_inputs_df = master_inputs_df.drop_duplicates(subset=['item', 'company', '2023', '2024'], keep='first')

        # Add some calculated metrics
        # Calculate Cash Conversion Cycle
        for company in master_df['company'].unique():
            try:
                dso = master_df.loc[(master_df['company'] == company) & 
                                    (master_df['ratio_name'] == 'Days Sales Outstanding'), '2024'].values[0]
                inventory_days = master_df.loc[(master_df['company'] == company) & 
                                                (master_df['ratio_name'] == 'Days to Sell Inventory'), '2024'].values[0]
                dpo = master_df.loc[(master_df['company'] == company) & 
                                    (master_df['ratio_name'] == 'Days Payable Outstanding'), '2024'].values[0]
                cash_cycle = dso + inventory_days - dpo

                # Add to master_df
                new_row = pd.DataFrame({
                    'company': [company],
                    'category': ['activity'],
                    'ratio_name': ['Cash Conversion Cycle'],
                    '2023': [np.nan],
                    '2024': [cash_cycle]
                })
                master_df = pd.concat([master_df, new_row], ignore_index=True)
            except:
                pass
        return master_df, master_inputs_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None


# Load data
master_df, master_inputs_df = load_and_clean_data()

if master_df is None or master_inputs_df is None:
    st.stop()

# Sidebar controls
with st.sidebar:
    st.header("Dashboard Controls")

    # Company selection
    all_companies = sorted(master_df['company'].unique())
    selected_companies = st.multiselect(
        "Select Companies",
        all_companies,
        default=all_companies  # Show all by default
    )

    # Year selection
    years = ['2023', '2024']
    selected_years = st.multiselect(
        "Select Years",
        years,
        default=years
    )

    # Ratio category filter
    ratio_categories = sorted(master_df['category'].unique())
    selected_category = st.selectbox(
        "Filter by Category",
        ["All Categories"] + ratio_categories
    )

    # Display options
    st.subheader("Display Options")
    show_raw_data = st.checkbox("Show Raw Data", value=False)
    show_insights = st.checkbox("Show Insights", value=True)

    # Color scheme selection
    color_scheme = st.selectbox(
        "Color Scheme",
        ["Corporate", "Bright", "Pastel", "Monochrome"]
    )

    # Color mapping based on selection
    if color_scheme == "Corporate":
        company_colors = {'BORYSZEW': '#1f77b4', 'FASING': '#ff7f0e', 'FEERUM': '#2ca02c'}
    elif color_scheme == "Bright":
        company_colors = {'BORYSZEW': '#e41a1c', 'FASING': '#377eb8', 'FEERUM': '#4daf4a'}
    elif color_scheme == "Pastel":
        company_colors = {'BORYSZEW': '#a6cee3', 'FASING': '#b2df8a', 'FEERUM': '#fb9a99'}
    else:
        company_colors = {'BORYSZEW': '#636363', 'FASING': '#969696', 'FEERUM': '#cccccc'}

# Main dashboard content

# Row 1: Executive Summary with Alerts
st.header("Executive Summary & Alerts")

# Calculate alerts for each company
alerts = []
for company in selected_companies:
    company_data = master_df[master_df['company'] == company]

    # Check for negative interest coverage
    interest_coverage = company_data[company_data['ratio_name'] == 'Interest Coverage Ratio']['2024'].values[0]
    if interest_coverage < 0:
        alerts.append(f"{company}: Negative Interest Coverage ({interest_coverage:.2f})")

    # Check for low liquidity
    current_ratio = company_data[company_data['ratio_name'] == 'Current Ratio']['2024'].values[0]
    if current_ratio < 1.2:
        alerts.append(f"{company}: Low Current Ratio ({current_ratio:.2f})")

    # Check for negative margins
    net_margin = company_data[company_data['ratio_name'] == 'Net Profit Margin']['2024'].values[0]
    if net_margin < 0:
        alerts.append(f"{company}: Negative Net Margin ({net_margin:.1%})")

if alerts:
    with st.expander("Critical Alerts", expanded=True):
        for alert in alerts:
            st.markdown(f'<div class="warning-box">{alert}</div>', unsafe_allow_html=True)

# Row 2: Key Financial Metrics
st.header("Key Financial Metrics")

# Create 4 columns for KPIs
kpi_cols = st.columns(4)


# Helper function to safely get ratio values
def get_ratio_value(company, ratio_name, year):
    try:
        value = master_df.loc[
            (master_df['company'] == company) &
            (master_df['ratio_name'] == ratio_name),
            year
        ].values[0]
        return value
    except:
        return None


# Display KPIs for first selected company
if selected_companies:
    ref_company = selected_companies[0]

    # Current Ratio KPI
    with kpi_cols[0]:
        cr_2024 = get_ratio_value(ref_company, "Current Ratio", "2024")
        cr_2023 = get_ratio_value(ref_company, "Current Ratio", "2023")
        delta_cr = (cr_2024 - cr_2023) if (cr_2024 and cr_2023) else None
        st.metric(
            "Current Ratio",
            f"{cr_2024:.2f}" if cr_2024 else "N/A",
            f"{delta_cr:+.2f}" if delta_cr is not None else None,
            delta_color="inverse" if delta_cr and delta_cr < 0 else "normal"
        )

    # Debt to Equity KPI
    with kpi_cols[1]:
        dte_2024 = get_ratio_value(ref_company, "Debt to Equity Ratio", "2024")
        dte_2023 = get_ratio_value(ref_company, "Debt to Equity Ratio", "2023")
        delta_dte = (dte_2024 - dte_2023) if (dte_2024 and dte_2023) else None
        st.metric(
            "Debt to Equity",
            f"{dte_2024:.2f}" if dte_2024 else "N/A",
            f"{delta_dte:+.2f}" if delta_dte is not None else None,
            delta_color="inverse" if delta_dte and delta_dte > 0 else "normal"
        )

    # Net Profit Margin KPI
    with kpi_cols[2]:
        npm_2024 = get_ratio_value(ref_company, "Net Profit Margin", "2024")
        npm_2023 = get_ratio_value(ref_company, "Net Profit Margin", "2023")
        delta_npm = (npm_2024 - npm_2023) if (npm_2024 and npm_2023) else None
        st.metric(
            "Net Profit Margin",
            f"{npm_2024:.1%}" if npm_2024 else "N/A",
            f"{delta_npm:+.1%}" if delta_npm is not None else None,
            delta_color="inverse" if delta_npm and delta_npm < 0 else "normal"
        )

    # Asset Turnover KPI
    with kpi_cols[3]:
        at_2024 = get_ratio_value(ref_company, "Asset Turnover Ratio", "2024")
        at_2023 = get_ratio_value(ref_company, "Asset Turnover Ratio", "2023")
        delta_at = (at_2024 - at_2023) if (at_2024 and at_2023) else None
        st.metric(
            "Asset Turnover",
            f"{at_2024:.2f}" if at_2024 else "N/A",
            f"{delta_at:+.2f}" if delta_at is not None else None,
            delta_color="inverse" if delta_at and delta_at < 0 else "normal"
        )

# Row 3: Main Visualizations - Tabs
st.header("Financial Analysis")

# Create tabs for different analyses
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Profitability",
    "Liquidity & Leverage",
    "Efficiency",
    "Structure",
    "All Data"
])

with tab1:
    # Profitability Analysis
    st.subheader("Profitability Margins Comparison")

    # Filter profitability ratios
    profit_ratios = ["Gross Margin", "Operating Margin", "EBIT Margin", "Net Profit Margin"]
    profit_data = []

    for company in selected_companies:
        for ratio in profit_ratios:
            val_2024 = get_ratio_value(company, ratio, "2024")
            val_2023 = get_ratio_value(company, ratio, "2023")

            if val_2024 is not None:
                profit_data.append({
                    'Company': company,
                    'Ratio': ratio,
                    'Year': '2024',
                    'Value': val_2024,
                    'Color': company_colors[company]
                })
            if val_2023 is not None:
                profit_data.append({
                    'Company': company,
                    'Ratio': ratio,
                    'Year': '2023',
                    'Value': val_2023,
                    'Color': company_colors[company]
                })

    if profit_data:
        profit_df = pd.DataFrame(profit_data)

        # Create grouped bar chart
        fig_profit = px.bar(
            profit_df,
            x='Ratio',
            y='Value',
            color='Company',
            facet_col='Year',
            barmode='group',
            color_discrete_map=company_colors,
            title="Profitability Margins Comparison"
        )
        fig_profit.update_yaxes(tickformat=".1%")
        fig_profit.update_layout(height=500, showlegend=True)
        st.plotly_chart(fig_profit, use_container_width=True)

        # Profitability insights
        if show_insights:
            with st.expander("📝 Profitability Insights"):
                insights = []
                for company in selected_companies:
                    npm = get_ratio_value(company, "Net Profit Margin", "2024")
                    opm = get_ratio_value(company, "Operating Margin", "2024")
                    if npm and opm:
                        tax_efficiency = npm / opm if opm != 0 else 0
                        insights.append(f"{company}: Net margin is {npm:.1%} of operating margin (tax/interest efficiency: {tax_efficiency:.1%})")
                for insight in insights:
                    st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

with tab2:
    # Liquidity & Leverage Analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Liquidity Ratios")

        liquidity_data = []
        for company in selected_companies:
            cr = get_ratio_value(company, "Current Ratio", "2024")
            qr = get_ratio_value(company, "Quick Ratio", "2024")

            if cr and qr:
                liquidity_data.append({
                    'Company': company,
                    'Current Ratio': cr,
                    'Quick Ratio': qr
                })

        if liquidity_data:
            liquidity_df = pd.DataFrame(liquidity_data)

            # Create scatter plot for liquidity
            fig_liquidity = px.scatter(
                liquidity_df,
                x='Current Ratio',
                y='Quick Ratio',
                color='Company',
                size=[100] * len(liquidity_df),
                hover_name='Company',
                color_discrete_map=company_colors,
                title="Current vs Quick Ratio (2024)"
            )

            # Add reference lines
            fig_liquidity.add_hline(y=1, line_dash="dash", line_color="gray")
            fig_liquidity.add_vline(x=1.5, line_dash="dash", line_color="gray")

            # Add quadrant labels
            fig_liquidity.add_annotation(
                x=0.5, y=2,
                text="High Quality Liquidity",
                showarrow=False
                )
            fig_liquidity.add_annotation(
                x=2.5,
                y=0.5,
                text="Inventory Dependent",
                showarrow=False
                )

            fig_liquidity.update_layout(height=400)
            st.plotly_chart(fig_liquidity, use_container_width=True)

    with col2:
        st.subheader("Leverage Ratios")

        leverage_data = []
        for company in selected_companies:
            dte = get_ratio_value(company, "Debt to Equity Ratio", "2024")
            eq_ratio = get_ratio_value(company, "Equity Ratio", "2024")

            if dte and eq_ratio:
                leverage_data.append({
                    'Company': company,
                    'Debt to Equity': dte,
                    'Equity Ratio': eq_ratio
                })

        if leverage_data:
            leverage_df = pd.DataFrame(leverage_data)

            # Create bar chart for leverage
            fig_leverage = go.Figure()

            for i, company in enumerate(selected_companies):
                company_data = leverage_df[leverage_df['Company'] == company]
                if not company_data.empty:
                    fig_leverage.add_trace(go.Bar(
                        name=company,
                        x=['Debt/Equity', 'Equity Ratio'],
                        y=[company_data['Debt to Equity'].values[0],
                            company_data['Equity Ratio'].values[0]],
                        marker_color=company_colors[company]
                    ))

            fig_leverage.update_layout(
                title="Leverage Analysis (2024)",
                barmode='group',
                height=400,
                yaxis_tickformat=".2f"
            )
            st.plotly_chart(fig_leverage, use_container_width=True)

with tab3:
    # Efficiency Analysis
    st.subheader("Efficiency Metrics")
    
    # Create gauge charts for efficiency metrics (keeping your original design)
    efficiency_ratios = [
        ("Days Sales Outstanding", "DSO", "days"),
        ("Days to Sell Inventory", "Inventory Days", "days"),
        ("Days Payable Outstanding", "DPO", "days"),
        ("Asset Turnover Ratio", "Asset Turnover", "ratio"),
        ("Cash Conversion Cycle", "Cash Cycle", "days")
    ]
    
    # Create columns for each company
    company_cols = st.columns(len(selected_companies))
    
    for idx, company in enumerate(selected_companies):
        with company_cols[idx]:
            st.markdown(
                f'<div class="company-header">{company}</div>',
                unsafe_allow_html=True
                )

            for ratio_fullname, short_name, unit in efficiency_ratios:
                val_2024 = get_ratio_value(company, ratio_fullname, "2024")
                val_2023 = get_ratio_value(company, ratio_fullname, "2023")

                if val_2024 is None:
                    continue

                # Determine gauge settings based on metric type
                if unit == "days":
                    gauge_max = max(150, val_2024 * 1.5)
                    ranges = [
                        {'range': [0, 30], 'color': "lightgreen"},
                        {'range': [30, 60], 'color': "yellow"},
                        {'range': [60, gauge_max], 'color': "red"}
                    ]
                else:
                    gauge_max = max(2.0, val_2024 * 1.5)
                    ranges = [
                        {'range': [0, 0.5], 'color': "red"},
                        {'range': [0.5, 1.0], 'color': "yellow"},
                        {'range': [1.0, gauge_max], 'color': "lightgreen"}
                    ]

                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=val_2024,
                    title={'text': f"{short_name}", 'font': {'size': 14}},
                    delta={'reference': val_2023 if val_2023 else 0,
                            'increasing': {'color': "red"},
                            'decreasing': {'color': "green"}},
                    gauge={
                        'axis': {'range': [0, gauge_max]},
                        'steps': ranges,
                        'threshold': {
                            'line': {'color': "black", 'width': 3},
                            'thickness': 0.8,
                            'value': val_2024
                        }
                    }
                ))
                fig.update_layout(width=300, height=200, margin=dict(t=50, b=10, l=10, r=10))
                st.plotly_chart(fig, use_container_width=True)

with tab4:
    # Financial Structure Analysis
    st.subheader("Financial Structure Composition")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Asset Structure (2024)")

        asset_data = []
        for company in selected_companies:
            nc_assets = get_ratio_value(company, "Non-current Assets Ratio", "2024")
            c_assets = get_ratio_value(company, "Current Assets Ratio", "2024")

            if nc_assets and c_assets:
                asset_data.append({
                    'Company': company,
                    'Type': 'Non-current Assets',
                    'Value': nc_assets
                })
                asset_data.append({
                    'Company': company,
                    'Type': 'Current Assets',
                    'Value': c_assets
                })

        if asset_data:
            asset_df = pd.DataFrame(asset_data)

            fig_assets = px.bar(
                asset_df,
                x='Company',
                y='Value',
                color='Type',
                barmode='stack',
                color_discrete_sequence=['#1f77b4', '#ff7f0e'],
                title="Asset Composition"
            )
            fig_assets.update_yaxes(tickformat=".0%")
            fig_assets.update_layout(height=400)
            st.plotly_chart(fig_assets, use_container_width=True)

    with col2:
        st.markdown("#### Financing Structure (2024)")

        financing_data = []
        for company in selected_companies:
            equity = get_ratio_value(company, "Equity Ratio", "2024")
            nc_liab = get_ratio_value(company, "Non-current Liabilities Ratio", "2024")
            c_liab = get_ratio_value(company, "Current Liabilities Ratio", "2024")

            if equity and nc_liab and c_liab:
                financing_data.append({
                    'Company': company,
                    'Type': 'Equity',
                    'Value': equity
                })
                financing_data.append({
                    'Company': company,
                    'Type': 'Non-current Liabilities',
                    'Value': nc_liab
                })
                financing_data.append({
                    'Company': company,
                    'Type': 'Current Liabilities',
                    'Value': c_liab
                })

        if financing_data:
            financing_df = pd.DataFrame(financing_data)
            
            fig_financing = px.bar(
                financing_df,
                x='Company',
                y='Value',
                color='Type',
                barmode='stack',
                color_discrete_sequence=['#2ca02c', '#d62728', '#9467bd'],
                title="Financing Structure"
            )
            fig_financing.update_yaxes(tickformat=".0%")
            fig_financing.update_layout(height=400)
            st.plotly_chart(fig_financing, use_container_width=True)

with tab5:
    # All Data tab
    st.subheader("Complete Ratio Data")

    # Filter data based on selections
    display_df = master_df.copy()

    if selected_companies:
        display_df = display_df[display_df['company'].isin(selected_companies)]

    if selected_category != "All Categories":
        display_df = display_df[display_df['category'] == selected_category]

    # Format the display
    formatted_df = display_df.copy()

    # Format percentage columns for specific ratios
    percent_ratios = ['Margin', 'Ratio', 'Holdings']
    for idx, row in formatted_df.iterrows():
        for year in ['2023', '2024']:
            if year in formatted_df.columns:
                if any(term in row['ratio_name'] for term in percent_ratios):
                    try:
                        formatted_df.at[idx, year] = f"{float(row[year]):.1%}"
                    except:
                        pass
                elif 'Days' in row['ratio_name'] or 'Working Capital' in row['ratio_name']:
                    try:
                        formatted_df.at[idx, year] = f"{float(row[year]):,.0f}"
                    except:
                        pass
                else:
                    try:
                        formatted_df.at[idx, year] = f"{float(row[year]):.2f}"
                    except:
                        pass

    st.dataframe(
        formatted_df,
        use_container_width=True,
        height=600
    )

# Row 4: Cash Flow Analysis (using master_inputs)
st.header("Cash Flow Analysis")

if len(selected_companies) > 0:
    # Get cash flow items
    cash_flow_items = ['operating_cash_flow', 'investing_cash_flow', 'financing_cash_flow', 'net_cash_flow']

    # Prepare cash flow data
    cash_data = []
    for company in selected_companies[:3]:  # Limit to 3 for space
        company_cash = master_inputs_df[master_inputs_df['company'] == company]
        company_cash = company_cash[company_cash['item'].isin(cash_flow_items)]

        for _, row in company_cash.iterrows():
            cash_data.append({
                'Company': company,
                'Cash Flow Type': row['item'].replace('_', ' ').title(),
                '2023': row['2023'],
                '2024': row['2024']
            })

    if cash_data:
        cash_df = pd.DataFrame(cash_data)

        # Create waterfall charts for each company
        st.subheader("Cash Flow Components")

        for company in selected_companies[:2]:  # Show first 2 companies
            st.markdown(f"{company}")

            company_cash = cash_df[cash_df['Company'] == company]
            company_cash_2024 = company_cash[['Cash Flow Type', '2024']].copy()

            # Sort for logical waterfall order
            order = ['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow', 'Net Cash Flow']
            company_cash_2024['Cash Flow Type'] = pd.Categorical(
                company_cash_2024['Cash Flow Type'], 
                categories=order, 
                ordered=True
            )
            company_cash_2024 = company_cash_2024.sort_values('Cash Flow Type')

            # Create waterfall
            fig_waterfall = go.Figure(go.Waterfall(
                name=f"{company} 2024",
                orientation="v",
                measure=["relative", "relative", "relative", "total"],
                x=company_cash_2024['Cash Flow Type'],
                y=company_cash_2024['2024'],
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                decreasing={"marker": {"color": "#d62728"}},
                increasing={"marker": {"color": "#2ca02c"}},
                totals={"marker": {"color": "#1f77b4"}}
            ))
            
            fig_waterfall.update_layout(
                title=f"Cash Flow Waterfall - {company} (2024)",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_waterfall, use_container_width=True)

# Row 5: Overall Insights
if show_insights:
    st.header("Overall Insights & Recommendations")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("### Strengths")
        strengths = []
        
        # Check each company for strengths
        for company in selected_companies:
            company_data = master_df[master_df['company'] == company]
            
            # Check equity ratio
            equity_ratio = get_ratio_value(company, "Equity Ratio", "2024")
            if equity_ratio and equity_ratio > 0.5:
                strengths.append(f"{company}: Strong equity position ({equity_ratio:.1%})")
            
            # Check current ratio
            current_ratio = get_ratio_value(company, "Current Ratio", "2024")
            if current_ratio and current_ratio > 2.0:
                strengths.append(f"{company}: Excellent liquidity (Current Ratio: {current_ratio:.2f})")
            
            # Check positive interest coverage
            interest_coverage = get_ratio_value(company, "Interest Coverage Ratio", "2024")
            if interest_coverage and interest_coverage > 2:
                strengths.append(f"{company}: Strong interest coverage ({interest_coverage:.2f})")
        
        if strengths:
            for strength in strengths:
                st.markdown(f'<div class="insight-box">{strength}</div>', unsafe_allow_html=True)
        else:
            st.info("No significant strengths identified for selected companies.")
    
    with insights_col2:
        st.markdown("### Areas for Improvement")
        improvements = []
        
        # Check each company for improvements needed
        for company in selected_companies:
            company_data = master_df[master_df['company'] == company]
            
            # Check negative interest coverage
            interest_coverage = get_ratio_value(company, "Interest Coverage Ratio", "2024")
            if interest_coverage and interest_coverage < 0:
                improvements.append(f"{company}: Negative interest coverage indicates financial distress")
            
            # Check low cash holdings
            cash_ratio = get_ratio_value(company, "Cash Holdings Ratio", "2024")
            if cash_ratio and cash_ratio < 0.05:
                improvements.append(f"{company}: Low cash reserves ({cash_ratio:.1%})")
            
            # Check negative margins
            net_margin = get_ratio_value(company, "Net Profit Margin", "2024")
            if net_margin and net_margin < 0:
                improvements.append(f"{company}: Operating at a loss ({net_margin:.1%} net margin)")
        
        if improvements:
            for improvement in improvements:
                st.markdown(f'<div class="warning-box">{improvement}</div>', unsafe_allow_html=True)
        else:
            st.success("No critical issues identified for selected companies.")

# Row 6: Raw Data (if requested)
if show_raw_data:
    with st.expander("📄 Raw Data Preview"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Master Ratios Data")
            st.dataframe(master_df.head(30))
        
        with col2:
            st.write("### Master Inputs Data")
            st.dataframe(master_inputs_df.head(30))

# Footer
st.markdown("---")
st.markdown("*Dashboard created with Streamlit & Plotly | Data updated: 2024*")

# Add download button for filtered data
if len(selected_companies) > 0:
    filtered_data = master_df[master_df['company'].isin(selected_companies)]
    csv = filtered_data.to_csv(index=False)
    
    st.sidebar.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name=f"financial_ratios_{'_'.join(selected_companies)}.csv",
        mime="text/csv"
    )