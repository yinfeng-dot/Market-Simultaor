import math
import streamlit as st
import plotly.graph_objects as go
import pandas as pd     # 必须添加
import numpy as np      # 必须添加
import yfinance as yf   # 必须添加

st.set_page_config(page_title="2026 IPO泡沫模拟器", layout="wide")

# ... (保留你原有的 IPOS, SCENARIOS, HISTORICAL, MARKET_TICKERS 数据字典) ...

# ── 统一的标签页定义 ──────────────────────────────────────────
# 为了避免 NameError，必须在这里定义好所有 tab
tabs = st.tabs(["🏠 市场概览", "🔍 IPO详情", "🎛️ 泡沫模拟", "📜 历史对比", "📡 实时市场", "📈 趋势预测"])

# ── 依次实现每个 Tab (使用 tabs[0], tabs[1]...) ────────────────
with tabs[0]:
    # 原 Tab 1 内容...

with tabs[5]: # 这里对应 "趋势预测"
    st.subheader("🔮 资产多情景演化路径")
    # 确保在这里使用 pd.DataFrame 或其他逻辑时，导入语句在文件最顶部
    # ... (你的趋势预测代码) ...
