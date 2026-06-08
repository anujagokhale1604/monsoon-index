# 🌧️ The Monsoon Index
### Live Global Inflation Transmission Tracker

> *Where is the next inflation surge coming from?*

A live dashboard tracking inflation transmission dynamics across 15 economies using rolling Granger causality analysis. Built on the empirical framework from [Gokhale (2026)](https://ssrn.com/abstract=6514338), which documents an asymmetric India → Singapore → UK inflation transmission chain.

**Live app:** [monsoon-index.streamlit.app](https://monsoon-index.streamlit.app/)

## What it does
- Tracks CPI dynamics across 15 economies (upstream EM, relay, downstream DM)
- Runs rolling 36-month Granger causality tests across all 210 country pairs
- Generates a real-time "Monsoon Regime" signal — Active / Marginal / Quiet
- Answers the question: *where is upstream inflation pressure building right now?*

## Data sources
- FRED (Federal Reserve) — USA, UK, Germany, France, Japan, India
- Eurostat — Germany, France (monthly HICP)
- SingStat — Singapore CPI (seasonally adjusted, 2024 base)
- World Bank — all 15 economies (annual, calibrated to monthly)

## Technical stack
- Python (Pandas, Statsmodels, Plotly, Streamlit)
- Rolling VAR(4) Granger causality engine
- Deployed on Streamlit Cloud

## Research basis
Gokhale, A.A. (2026). *Cross-Country Macroeconomic Dynamics: Inflation, Growth, and Monetary Policy — India, Singapore, and the United Kingdom.* SSRN Working Paper. [ssrn.com/abstract=6514338](https://ssrn.com/abstract=6514338)

---
*Anuja A. Gokhale · MA Applied Economics, NUS (Merit Scholar) · anujagokhale1604@gmail.com*
