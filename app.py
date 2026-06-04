import math
import streamlit as st
import plotly.graph_objects as go
import pandas as pd  # 必须导入
import numpy as np   # 数学计算
import yfinance as yf # 实时数据获取

st.set_page_config(
    page_title="2026 IPO泡沫模拟器",
    page_icon="📈",
    layout="wide",
)

# ── 数据定义 ──────────────────────────────────────────────────────────────────
IPOS = [
    {"name": "SpaceX", "sector": "太空科技", "val_b": 1750, "rev_b": 12.4, "profitable": True, "float_pct": 4, "exp_pop": 22, "bubble_risk": 45, "date": "2026年6月", "desc": "S-1已于5月20日提交，唯一盈利的超级IPO。"},
    {"name": "OpenAI", "sector": "人工智能", "val_b": 1000, "rev_b": 3.4, "profitable": False, "float_pct": 5, "exp_pop": 35, "bubble_risk": 78, "date": "2026年Q4", "desc": "ChatGPT母公司，年收入约$34亿但仍大幅亏损。"},
    {"name": "Anthropic", "sector": "人工智能", "val_b": 965, "rev_b": 1.8, "profitable": False, "float_pct": 5, "exp_pop": 40, "bubble_risk": 82, "date": "2026年Q4", "desc": "Claude系列模型公司，主要受战略投资方支持。"},
]

# ── 核心函数 ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_and_calc_params(ticker):
    try:
        data = yf.download(ticker, period="1y", progress=False)
        if data.empty: return None, "未找到数据"
        
        # 处理可能的 MultiIndex
        if isinstance(data.columns, pd.MultiIndex):
            close = data['Close'][ticker].dropna()
        else:
            close = data['Close'].dropna()
            
        s0 = float(close.iloc[-1])
        daily_returns = close.pct_change().dropna()
        hist_sigma = float(daily_returns.std() * np.sqrt(252))
        hist_mu = float((close.iloc[-1] / close.iloc[0]) - 1)
        
        return {"s0": s0, "mu": hist_mu, "sigma": hist_sigma}, None
    except Exception as e:
        return None, str(e)

def generate_gbm_paths(S0, mu, sigma, T_months, n_paths):
    dt = 1 / 12
    paths = np.zeros((T_months + 1, n_paths))
    paths[0] = S0
    for t in range(1, T_months + 1):
        Z = np.random.standard_normal(n_paths)
        paths[t] = paths[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
    return paths

# ── 页面布局 ──────────────────────────────────────────────────────────────────
st.title("📈 2026 大型IPO与泡沫风险模拟器")
tabs = st.tabs(["🏠 市场概览", "📡 实时市场", "📈 趋势预测"])

with tabs[0]:
    st.write("欢迎使用IPO泡沫模拟器。")

with tabs[1]:
    st.subheader("实时市场数据")
    # 此处放置你的 Tab 5 逻辑

with tabs[2]:
    st.subheader("🔮 资产多情景演化路径")
    col1, col2 = st.columns(2)
    ticker = col1.text_input("输入代码", "NVDA")
    horizon = col2.slider("周期(月)", 6, 36, 12)
    
    if st.button("计算预测"):
        params, err = fetch_and_calc_params(ticker)
        if err:
            st.error(err)
        else:
            paths = generate_gbm_paths(params["s0"], params["mu"], params["sigma"], horizon, 10)
            fig = go.Figure()
            for i in range(10):
                fig.add_trace(go.Scatter(y=paths[:, i], mode='lines', opacity=0.3))
            st.plotly_chart(fig)
