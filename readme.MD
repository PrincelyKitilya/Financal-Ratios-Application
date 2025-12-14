# Financial Ratio Analysis Dashboard

## Overview
A comprehensive Streamlit application that automates financial ratio analysis for multiple companies. The app processes financial statements, calculates key ratios, identifies financial health warnings, and provides interactive visualizations for comparative analysis.

## Workflow Process

### 1. Data Ingestion & Processing
- **Input:** Raw financial statements in Excel format (`*_inputs.xlsx`)
- **Processing:** Automated extraction and cleaning of financial data
- **Companies Supported:** BORYSZEW, FASING, FEERUM (extensible to others)

### 2. Financial Ratio Calculation
The application calculates **four main categories** of financial ratios:

#### Liquidity Ratios (Short-term solvency)
- **Current Ratio** = Current Assets / Current Liabilities
- **Quick Ratio** = (Current Assets - Inventory) / Current Liabilities
- **Cash Ratio** = Cash & Equivalents / Current Liabilities
- **Operating Cash Flow Ratio** = Operating Cash Flow / Current Liabilities

#### Solvency/Leverage Ratios (Long-term stability)
- **Debt-to-Equity Ratio** = Total Debt / Total Equity
- **Debt-to-Assets Ratio** = Total Debt / Total Assets
- **Interest Coverage Ratio** = EBIT / Interest Expense
- **Equity Multiplier** = Total Assets / Total Equity

#### Profitability Ratios (Earning capacity)
- **Gross Profit Margin** = Gross Profit / Revenue
- **Operating Profit Margin** = Operating Income / Revenue
- **Net Profit Margin** = Net Income / Revenue
- **Return on Assets (ROA)** = Net Income / Total Assets
- **Return on Equity (ROE)** = Net Income / Total Equity
- **Return on Invested Capital (ROIC)** = NOPAT / Invested Capital

#### Efficiency/Activity Ratios (Asset utilization)
- **Asset Turnover** = Revenue / Total Assets
- **Inventory Turnover** = COGS / Average Inventory
- **Receivables Turnover** = Revenue / Average Receivables
- **Days Sales Outstanding (DSO)** = 365 / Receivables Turnover
- **Days Inventory Outstanding (DIO)** = 365 / Inventory Turnover

### 3. Warning System & Financial Health Assessment
The app automatically generates **color-coded warnings** based on industry benchmarks:

#### Critical Warnings (Require Immediate Attention)
- Current Ratio < 1.0 (Potential liquidity crisis)
- Quick Ratio < 0.5 (Severe liquidity problems)
- Debt-to-Equity > 2.0 (Excessive leverage)
- Interest Coverage < 1.5 (Difficulty covering interest)
- Negative Profit Margins (Operating at a loss)

#### Caution Warnings (Monitor Closely)
- Current Ratio 1.0-1.5 (Below optimal liquidity)
- Debt-to-Equity 1.5-2.0 (High leverage)
- ROE < Cost of Equity (Destroying shareholder value)
- DSO > 60 days (Poor receivables management)
- Inventory Turnover < industry average

#### Healthy Indicators
- Current Ratio 1.5-3.0 (Strong liquidity)
- Debt-to-Equity < 1.0 (Conservative leverage)
- ROE > 15% (Excellent profitability)
- Positive trending ratios quarter-over-quarter

### 4. Data Consolidation & Master Analysis
- **Automatic Combination:** Merges ratios from all companies into `master_ratios.xlsx`
- **Comparative Analysis:** Side-by-side company comparisons
- **Trend Analysis:** Historical performance tracking (if multi-period data available)

## Streamlit Dashboard Features

### Main Dashboard Sections:

#### 1. Company Overview Panel
- Quick financial health snapshot for each company
- Color-coded status indicators (Green/Yellow/Red)
- Key ratio highlights with trend arrows

#### 2. Ratio Explorer
- Interactive dropdown to select specific ratios
- Side-by-side company comparisons
- Historical trends visualization (line charts)

#### 3. Warning & Alerts Center
- Consolidated list of all financial warnings
- Filterable by company and severity
- Recommended actions for each warning

#### 4. Comparative Analysis
- Radar charts for multi-ratio comparison
- Peer benchmarking against industry averages
- Performance scoring system

#### 5. Export & Reporting
- One-click export of all ratios to Excel
- Generate PDF summary reports
- Customizable analysis timeframes

### Technical Features:
- **Real-time Processing:** Upload new financial statements for instant analysis
- **Custom Thresholds:** Adjust warning thresholds based on industry
- **Data Validation:** Automatic checks for data consistency and completeness
- **Multi-currency Support:** Handle different currency units
- **Scalable Architecture:** Easy to add new companies or industries

## Getting Started

## deployed application
https://financal-ratios-application-jmkwsmten7txwh7ykbgs9d.streamlit.app

### Quick Launch:
```bash
streamlit run app.py

