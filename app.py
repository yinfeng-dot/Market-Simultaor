"""
2026 大型IPO与泡沫风险模拟器 - Streamlit版（含实时数据+趋势预测+股票分析器）
"""

import math
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="2026 IPO泡沫模拟器",
    page_icon="📈",
    layout="wide",
)

# ── 数据 ──────────────────────────────────────────────────────────────────────
IPOS = [
    {"name": "SpaceX",       "sector": "太空科技", "val_b": 1750, "rev_b": 12.4,
     "profitable": True,  "float_pct": 4,  "exp_pop": 22, "bubble_risk": 45, "date": "2026年6月",
     "desc": "S-1已于5月20日提交，预计6月定价。唯一盈利的超级IPO，收入$124亿，自由现金流为正。流通比例仅4-5%，极度受限。"},
    {"name": "OpenAI",       "sector": "人工智能", "val_b": 1000, "rev_b": 3.4,
     "profitable": False, "float_pct": 5,  "exp_pop": 35, "bubble_risk": 78, "date": "2026年Q4",
     "desc": "ChatGPT母公司，月活超5亿，年收入约$34亿但仍大幅亏损。内部治理复杂，存在法律不确定性。"},
    {"name": "Anthropic",    "sector": "人工智能", "val_b": 965,  "rev_b": 1.8,
     "profitable": False, "float_pct": 5,  "exp_pop": 40, "bubble_risk": 82, "date": "2026年Q4",
     "desc": "Claude系列模型公司，Series H估值$965亿。亚马逊和谷歌为主要战略投资方。"},
    {"name": "Databricks",   "sector": "企业AI",   "val_b": 134,  "rev_b": 2.8,
     "profitable": True,  "float_pct": 8,  "exp_pop": 18, "bubble_risk": 38, "date": "2026年H1",
     "desc": "数据+AI平台，年收入$28亿，正自由现金流。2026年IPO中基本面最扎实的AI公司。"},
    {"name": "Shein",        "sector": "电商",     "val_b": 66,   "rev_b": 38.0,
     "profitable": True,  "float_pct": 10, "exp_pop": 12, "bubble_risk": 52, "date": "2026年H1",
     "desc": "快时尚电商巨头，GMV超$380亿，盈利。主要风险：关税政策、ESG压力和地缘政治风险。"},
    {"name": "Reliance Jio", "sector": "电信",     "val_b": 137,  "rev_b": 22.0,
     "profitable": True,  "float_pct": 8,  "exp_pop": 15, "bubble_risk": 35, "date": "2026年H1",
     "desc": "印度最大电信运营商，5亿+用户，市占率42%。基本面稳健，盈利能力强。"},
]

SCENARIOS = {
    "🚀 牛市顺风":  (85, 3.5, 80, 85),
    "📊 基准预期":  (65, 4.5, 60, 70),
    "🐻 泡沫破裂":  (35, 6.0, 40, 45),
    "💥 系统崩溃":  (15, 7.5, 20, 25),
}

HISTORICAL = {
    "节点": ["T-24m","T-18m","T-12m","T-6m","峰值","T+6m","T+12m","T+18m","T+24m"],
    "2000互联网": [100, 180, 320, 480, 500, 240, 140, 100, 95],
    "2021 SPAC":  [100, 150, 220, 310, 350, 200, 140, 110, 105],
}

COLORS = ["#185FA5","#534AB7","#7F77DD","#1D9E75","#D85A30","#0F6E56"]

MARKET_TICKERS = {
    "^IXIC":  "纳斯达克",
    "^VIX":   "恐慌指数(VIX)",
    "NVDA":   "英伟达",
    "MSFT":   "微软",
    "GOOGL":  "谷歌",
    "META":   "Meta",
    "AMZN":   "亚马逊",
    "^GSPC":  "标普500",
}

POPULAR_STOCKS = {
    "科技": ["AAPL","MSFT","NVDA","GOOGL","META","AMZN","TSLA","AMD","INTC","ORCL"],
    "AI":   ["NVDA","AMD","SMCI","PLTR","AI","SOUN","BBAI","KULR"],
    "中概股":["BABA","JD","PDD","BIDU","NIO","XPEV","LI"],
    "ETF":  ["QQQ","SPY","ARKK","SOXX","VGT"],
}

# ── 工具函数 ──────────────────────────────────────────────────────────────────
def simulate(sentiment, rate, ai_speed, retail):
    pop   = round(5 + sentiment*0.4 + ai_speed*0.2 - rate*2 + retail*0.15)
    six_m = round((sentiment-50)*0.3 + (ai_speed-50)*0.2 - (rate-4)*8 + (retail-50)*0.1)
    burst = max(5, min(95, round(100 - sentiment*0.4 - ai_speed*0.2 + rate*6 - retail*0.05)))
    temp  = max(0, min(100, round(sentiment*0.4 + ai_speed*0.3 + retail*0.2 + (100-rate*8)*0.1)))
    labels = ["极度乐观","温和上行","基准预期","高度警觉","泡沫破裂风险"]
    descs  = [
        "AI商业化超预期叠加宽松流动性，各IPO首日均大幅上涨。散户FOMO情绪驱动短期溢价，需警惕6-12个月后回调。",
        "市场情绪良好，优质标的（SpaceX、Databricks）表现稳健。盈利能力将成为分化关键指标。",
        "市场处于可控高估值区间。锁定期到期（约180天）后预计出现首次较大波动。",
        "高利率+高估值形成压力，AI商业化不及预期将触发大幅回调。类比2000年3月。",
        "多重风险共振：流动性枯竭+盈利预期落空+锁定期抛售。历史类比：2000年互联网崩盘。",
    ]
    idx = min(4, burst // 20)
    return {"pop": pop, "six_m": six_m, "burst": burst, "temp": temp,
            "label": labels[idx], "desc": descs[idx]}

@st.cache_data(ttl=300)
def fetch_market_data():
    try:
        import yfinance as yf
        results = {}
        for ticker, name in MARKET_TICKERS.items():
            try:
                t    = yf.Ticker(ticker)
                hist = t.history(period="2d")
                if len(hist) >= 2:
                    price      = hist["Close"].iloc[-1]
                    prev       = hist["Close"].iloc[-2]
                    change_pct = (price - prev) / prev * 100
                    results[ticker] = {
                        "name": name,
                        "price": round(float(price), 2),
                        "change": round(float(price - prev), 2),
                        "change_pct": round(float(change_pct), 2),
                    }
            except Exception:
                pass
        return results
    except ImportError:
        return {}

def market_to_sentiment(data):
    if not data:
        return 65
    score = 50
    if "^VIX" in data:
        vix = data["^VIX"]["price"]
        if vix < 15:   score += 20
        elif vix < 20: score += 10
        elif vix < 30: score -= 10
        else:          score -= 25
    if "^IXIC" in data:
        score += data["^IXIC"]["change_pct"] * 3
    if "NVDA" in data:
        score += data["NVDA"]["change_pct"] * 2
    return max(0, min(100, round(score)))

def generate_gbm_paths(S0, mu, sigma, T_months, n_paths, seed=None):
    if seed is not None:
        np.random.seed(seed)
    dt    = 1 / 12
    paths = np.zeros((T_months + 1, n_paths))
    paths[0] = S0
    for t in range(1, T_months + 1):
        Z = np.random.standard_normal(n_paths)
        paths[t] = paths[t-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)
    return paths

# ── 股票分析核心函数 ───────────────────────────────────────────────────────────
@st.cache_data(ttl=180)
def fetch_stock_analysis(ticker: str):
    try:
        import yfinance as yf
        t    = yf.Ticker(ticker)
        hist = t.history(period="6mo")
        if hist.empty or len(hist) < 20:
            return None

        close  = hist["Close"]
        volume = hist["Volume"]

        # ── 技术指标计算 ──
        # RSI (14)
        delta  = close.diff()
        gain   = delta.clip(lower=0).rolling(14).mean()
        loss   = (-delta.clip(upper=0)).rolling(14).mean()
        rs     = gain / loss.replace(0, 1e-9)
        rsi    = float((100 - 100 / (1 + rs)).iloc[-1])

        # MACD
        ema12  = close.ewm(span=12).mean()
        ema26  = close.ewm(span=26).mean()
        macd   = ema12 - ema26
        signal = macd.ewm(span=9).mean()
        macd_val    = float(macd.iloc[-1])
        signal_val  = float(signal.iloc[-1])
        macd_hist   = macd_val - signal_val

        # 均线
        ma20  = float(close.rolling(20).mean().iloc[-1])
        ma50  = float(close.rolling(50).mean().iloc[-1]) if len(close) >= 50 else ma20
        ma200 = float(close.rolling(200).mean().iloc[-1]) if len(close) >= 200 else ma20

        # 布林带
        bb_mid = float(close.rolling(20).mean().iloc[-1])
        bb_std = float(close.rolling(20).std().iloc[-1])
        bb_up  = bb_mid + 2 * bb_std
        bb_low = bb_mid - 2 * bb_std

        # 成交量趋势
        vol_avg = float(volume.rolling(20).mean().iloc[-1])
        vol_now = float(volume.iloc[-1])
        vol_ratio = vol_now / vol_avg if vol_avg > 0 else 1.0

        # 价格位置
        price_now = float(close.iloc[-1])
        price_52w_high = float(close.rolling(min(252, len(close))).max().iloc[-1])
        price_52w_low  = float(close.rolling(min(252, len(close))).min().iloc[-1])
        price_from_high = (price_now - price_52w_high) / price_52w_high * 100
        price_from_low  = (price_now - price_52w_low)  / price_52w_low  * 100

        # 动量
        mom_1m  = float((close.iloc[-1] / close.iloc[-22] - 1) * 100) if len(close) >= 22 else 0
        mom_3m  = float((close.iloc[-1] / close.iloc[-66] - 1) * 100) if len(close) >= 66 else 0

        # 基本面（若有）
        info = {}
        try:
            info = t.info
        except Exception:
            pass

        pe     = info.get("trailingPE",  None)
        fwd_pe = info.get("forwardPE",   None)
        pb     = info.get("priceToBook", None)
        beta   = info.get("beta",        None)
        name   = info.get("longName",    ticker)
        sector = info.get("sector",      "未知")
        mktcap = info.get("marketCap",   None)
        target = info.get("targetMeanPrice", None)

        # ── 评分系统（总分 100） ──
        score = 50  # 中性起点
        signals = []

        # RSI 信号 (±15分)
        if rsi < 30:
            score += 15
            signals.append(("✅", "RSI超卖", f"RSI={rsi:.1f}，技术面严重超卖，反弹概率高"))
        elif rsi < 45:
            score += 8
            signals.append(("✅", "RSI偏低", f"RSI={rsi:.1f}，存在买入机会"))
        elif rsi > 75:
            score -= 15
            signals.append(("🔴", "RSI超买", f"RSI={rsi:.1f}，短期获利回吐压力大"))
        elif rsi > 60:
            score -= 5
            signals.append(("🟡", "RSI偏高", f"RSI={rsi:.1f}，上涨动能趋弱"))
        else:
            signals.append(("⚪", "RSI中性", f"RSI={rsi:.1f}，无明显超买超卖信号"))

        # MACD 信号 (±12分)
        if macd_hist > 0 and macd_val > signal_val:
            score += 12
            signals.append(("✅", "MACD金叉", f"MACD柱={macd_hist:.3f}，多头趋势确认"))
        elif macd_hist < 0 and macd_val < signal_val:
            score -= 12
            signals.append(("🔴", "MACD死叉", f"MACD柱={macd_hist:.3f}，空头趋势确认"))
        else:
            signals.append(("🟡", "MACD待确认", "MACD信号模糊，等待方向选择"))

        # 均线系统 (±10分)
        if price_now > ma20 > ma50:
            score += 10
            signals.append(("✅", "多头排列", f"价格>${ma20:.2f}(MA20)>${ma50:.2f}(MA50)"))
        elif price_now < ma20 < ma50:
            score -= 10
            signals.append(("🔴", "空头排列", f"价格<MA20<MA50，下行趋势明确"))
        elif price_now > ma20:
            score += 5
            signals.append(("🟡", "价格站上MA20", f"短期趋势向好"))

        # 布林带 (±8分)
        if price_now < bb_low:
            score += 8
            signals.append(("✅", "触及布林下轨", f"价格${price_now:.2f}低于下轨${bb_low:.2f}，超卖区间"))
        elif price_now > bb_up:
            score -= 8
            signals.append(("🔴", "突破布林上轨", f"价格${price_now:.2f}高于上轨${bb_up:.2f}，超买区间"))

        # 成交量 (±5分)
        if vol_ratio > 1.5 and mom_1m > 0:
            score += 5
            signals.append(("✅", "放量上涨", f"成交量是均值的{vol_ratio:.1f}倍，资金流入确认"))
        elif vol_ratio > 1.5 and mom_1m < 0:
            score -= 5
            signals.append(("🔴", "放量下跌", f"成交量是均值的{vol_ratio:.1f}倍，资金出逃信号"))

        # 动量 (±10分)
        if mom_1m > 10:
            score += 10
            signals.append(("✅", "强势动量", f"1个月涨幅+{mom_1m:.1f}%，趋势强劲"))
        elif mom_1m < -15:
            score -= 10
            signals.append(("🔴", "弱势动量", f"1个月跌幅{mom_1m:.1f}%，下行压力大"))

        # 基本面 PE (±5分)
        if pe and pe > 0:
            if pe < 15:
                score += 5
                signals.append(("✅", "估值便宜", f"P/E={pe:.1f}x，低于市场平均"))
            elif pe > 50:
                score -= 5
                signals.append(("🔴", "估值偏贵", f"P/E={pe:.1f}x，溢价明显需要高增长支撑"))

        # 分析师目标价 (±5分)
        if target and target > 0:
            upside = (target - price_now) / price_now * 100
            if upside > 20:
                score += 5
                signals.append(("✅", "分析师看多", f"目标价${target:.2f}，较现价上行空间{upside:.1f}%"))
            elif upside < -10:
                score -= 5
                signals.append(("🔴", "分析师看空", f"目标价${target:.2f}，较现价下行风险{abs(upside):.1f}%"))

        score = max(0, min(100, score))

        # ── 评级逻辑 ──
        if score >= 80:
            rating = "强力买入"; rating_color = "#0F6E56"; rating_emoji = "🚀"
            price_target_pct = round(mom_3m * 0.5 + 15 + (100 - rsi) * 0.3, 1)
        elif score >= 65:
            rating = "买入";     rating_color = "#1D9E75"; rating_emoji = "📈"
            price_target_pct = round(mom_3m * 0.3 + 8 + (60 - rsi) * 0.1, 1)
        elif score >= 45:
            rating = "持有";     rating_color = "#BA7517"; rating_emoji = "⚖️"
            price_target_pct = round(mom_3m * 0.1, 1)
        elif score >= 30:
            rating = "卖出";     rating_color = "#D85A30"; rating_emoji = "📉"
            price_target_pct = round(mom_3m * 0.3 - 8, 1)
        else:
            rating = "强力卖出"; rating_color = "#A32D2D"; rating_emoji = "💥"
            price_target_pct = round(mom_3m * 0.5 - 18, 1)

        price_target_pct = max(-50, min(100, price_target_pct))
        price_target = price_now * (1 + price_target_pct / 100)

        return {
            "ticker": ticker.upper(),
            "name": name,
            "sector": sector,
            "price_now": price_now,
            "price_target": price_target,
            "price_target_pct": price_target_pct,
            "price_52w_high": price_52w_high,
            "price_52w_low": price_52w_low,
            "price_from_high": price_from_high,
            "rsi": rsi,
            "macd_hist": macd_hist,
            "ma20": ma20, "ma50": ma50, "ma200": ma200,
            "bb_up": bb_up, "bb_low": bb_low,
            "vol_ratio": vol_ratio,
            "mom_1m": mom_1m, "mom_3m": mom_3m,
            "pe": pe, "fwd_pe": fwd_pe, "pb": pb,
            "beta": beta, "mktcap": mktcap,
            "target_analyst": target,
            "score": score,
            "rating": rating,
            "rating_color": rating_color,
            "rating_emoji": rating_emoji,
            "signals": signals,
            "hist": hist,
        }
    except Exception as e:
        return {"error": str(e)}

# ── 标题 ──────────────────────────────────────────────────────────────────────
st.title("📈 2026 大型IPO与泡沫风险模拟器")
st.caption("数据基于2026年Q1公开市场信息 · 仅供研究参考，不构成投资建议")

tabs = st.tabs(["🏠 市场概览","🔍 IPO详情","🎛️ 泡沫模拟","📜 历史对比","📡 实时市场","📈 趋势预测","🔬 股票分析器"])

# ── Tab 1 ──────────────────────────────────────────────────────────────────────
with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("预期总市值", "$3.12T", "12大待上市公司")
    c2.metric("Q1 2026 融资额", "$42.6B", "同比 +45%")
    c3.metric("AI占风投比例", "80%", "泡沫风险高", delta_color="inverse")
    c4.metric("泡沫综合指数", "74/100", "⚠ 高度警戒", delta_color="inverse")

    st.subheader("核心IPO估值分布")
    names = [c["name"] for c in IPOS]
    vals  = [c["val_b"] for c in IPOS]
    fig_bar = go.Figure(go.Bar(
        x=names, y=vals, marker_color=COLORS,
        text=[f"${v/1000:.2f}T" if v>=1000 else f"${v}B" for v in vals],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>估值: $%{y}B<extra></extra>",
    ))
    fig_bar.update_layout(height=350, margin=dict(t=30,b=20),
                          yaxis_title="估值 ($B)", showlegend=False, plot_bgcolor="#fafafa")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("市场集中度风险")
    for label, val in {"AI估值集中":88,"流动性压力":79,"盈利能力缺口":72,"锁定期后抛压":65,"市场吸收能力":42}.items():
        st.progress(val/100, text=f"{label}：**{val}%**")

# ── Tab 2 ──────────────────────────────────────────────────────────────────────
with tabs[1]:
    selected = st.selectbox("选择公司", [c["name"] for c in IPOS])
    company  = next(c for c in IPOS if c["name"] == selected)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(company["name"])
        st.caption(company["sector"] + " · " + company["date"])
        st.write(company["desc"])
    with col2:
        ps      = round(company["val_b"] / company["rev_b"])
        val_str = f"${company['val_b']/1000:.2f}T" if company["val_b"] >= 1000 else f"${company['val_b']}B"
        m1,m2,m3 = st.columns(3)
        m1.metric("预期估值", val_str)
        m2.metric("年收入", f"${company['rev_b']}B")
        m3.metric("P/S倍数", f"{ps}x")
        m4,m5,m6 = st.columns(3)
        m4.metric("盈利状态", "✓ 盈利" if company["profitable"] else "✗ 亏损")
        m5.metric("首日预期涨幅", f"+{company['exp_pop']}%")
        m6.metric("泡沫风险", f"{company['bubble_risk']}%",
                  delta_color="inverse" if company["bubble_risk"]>60 else "normal")

    st.subheader("所有公司对比")
    fig_bubble = go.Figure(go.Scatter(
        x=[c["bubble_risk"] for c in IPOS], y=[c["exp_pop"] for c in IPOS],
        mode="markers+text", text=[c["name"] for c in IPOS], textposition="top center",
        marker=dict(size=[max(14,math.log(c["val_b"]+1)*4) for c in IPOS],
                    color=[c["bubble_risk"] for c in IPOS], colorscale="RdYlGn_r",
                    showscale=True, colorbar=dict(title="泡沫风险%"),
                    line=dict(width=1, color="white")),
        hovertemplate="<b>%{text}</b><br>泡沫风险: %{x}%<br>首日预期: +%{y}%<extra></extra>",
    ))
    fig_bubble.update_layout(height=380, xaxis_title="泡沫风险 (%)",
                             yaxis_title="首日预期涨幅 (%)", plot_bgcolor="#fafafa", margin=dict(t=10))
    st.plotly_chart(fig_bubble, use_container_width=True)

# ── Tab 3 ──────────────────────────────────────────────────────────────────────
with tabs[2]:
    st.subheader("情景预设")
    sc_cols=st.columns(4); chosen_sc=None
    for i,(name,vals) in enumerate(SCENARIOS.items()):
        if sc_cols[i].button(name, use_container_width=True): chosen_sc=vals

    live_data=fetch_market_data(); auto_sentiment=market_to_sentiment(live_data)
    if live_data:
        st.caption(f"📡 实时市场情绪估算：**{auto_sentiment}/100**（基于纳斯达克+VIX+英伟达）")

    col_l,col_r=st.columns(2)
    with col_l:
        sentiment=st.slider("市场情绪（0=恐慌，100=狂热）",0,100,int(chosen_sc[0]) if chosen_sc else auto_sentiment)
        rate=st.slider("利率环境（%）",1.0,8.0,float(chosen_sc[1]) if chosen_sc else 4.5,step=0.1)
    with col_r:
        ai_speed=st.slider("AI商业化速度（0=慢，100=快）",0,100,int(chosen_sc[2]) if chosen_sc else 60)
        retail=st.slider("散户参与度（0=低，100=高）",0,100,int(chosen_sc[3]) if chosen_sc else 70)

    sim=simulate(sentiment,rate,ai_speed,retail)
    r1,r2,r3=st.columns(3)
    r1.metric("首日预期涨幅",f"+{sim['pop']}%")
    r2.metric("6个月后收益",f"{'+' if sim['six_m']>=0 else ''}{sim['six_m']}%")
    r3.metric("泡沫破裂概率",f"{sim['burst']}%","未来18个月内",delta_color="inverse")

    temp_label=("极度过热" if sim["temp"]>80 else "中度过热" if sim["temp"]>60 else "温和偏高" if sim["temp"]>40 else "相对理性")
    st.progress(sim["temp"]/100, text=f"泡沫温度计：**{sim['temp']}/100 — {temp_label}**")
    st.info(f"**{sim['label']}**\n\n{sim['desc']}")

    fig_gauge=go.Figure(go.Indicator(
        mode="gauge+number", value=sim["burst"], title={"text":"泡沫破裂概率 (%)"},
        gauge={"axis":{"range":[0,100]},
               "bar":{"color":"#A32D2D" if sim["burst"]>65 else "#BA7517" if sim["burst"]>40 else "#1D9E75"},
               "steps":[{"range":[0,40],"color":"#E1F5EE"},{"range":[40,70],"color":"#FAEEDA"},{"range":[70,100],"color":"#FCEBEB"}]},
    ))
    fig_gauge.update_layout(height=280,margin=dict(t=40,b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

# ── Tab 4 ──────────────────────────────────────────────────────────────────────
with tabs[3]:
    st.subheader("历史泡沫周期对比")
    nodes=HISTORICAL["节点"]; fig_hist=go.Figure()
    fig_hist.add_trace(go.Scatter(x=nodes,y=HISTORICAL["2000互联网"],name="2000互联网",
        line=dict(color="#E24B4A",dash="dash",width=2),mode="lines+markers"))
    fig_hist.add_trace(go.Scatter(x=nodes,y=HISTORICAL["2021 SPAC"],name="2021 SPAC",
        line=dict(color="#BA7517",dash="dot",width=2),mode="lines+markers"))
    fig_hist.add_trace(go.Scatter(x=nodes[:4],y=[100,130,180,240],name="2026 AI IPO(预测)",
        line=dict(color="#534AB7",width=3),mode="lines+markers"))
    fig_hist.update_layout(height=380,yaxis_title="指数 (基准=100)",
                           plot_bgcolor="#fafafa",legend=dict(orientation="h",y=-0.2))
    st.plotly_chart(fig_hist, use_container_width=True)
    col1,col2,col3=st.columns(3)
    col1.error("**2000 互联网泡沫**\n\n纳斯达克峰值5,048点，随后暴跌78%。1500+科技公司破产，市值蒸发约$5万亿。")
    col2.warning("**2021 SPAC狂热**\n\n600+ SPAC上市，多数较峰值下跌70%+。利率上升刺破泡沫，散户损失惨重。")
    col3.info("**2026 AI IPO浪潮**\n\n三巨头合计估值$3T，AI占风投80%。部分公司确有营收，但P/S倍数同样极端。")

# ── Tab 5 ──────────────────────────────────────────────────────────────────────
with tabs[4]:
    st.subheader("📡 实时AI相关市场数据")
    st.caption("数据来自雅虎财经，每5分钟自动刷新")
    if st.button("🔄 手动刷新"):
        st.cache_data.clear(); st.rerun()

    live_data=fetch_market_data()
    if not live_data:
        st.warning("无法获取实时数据，请检查网络连接。")
    else:
        cols=st.columns(4)
        for i,(ticker,info) in enumerate(live_data.items()):
            cols[i%4].metric(label=info["name"], value=f"{info['price']:,.2f}",
                delta=f"{info['change_pct']:+.2f}%",
                delta_color="inverse" if ticker=="^VIX" else "normal")
        st.subheader("今日涨跌幅")
        tl=[v["name"] for v in live_data.values()]; ch=[v["change_pct"] for v in live_data.values()]
        fig_live=go.Figure(go.Bar(x=tl,y=ch,marker_color=["#A32D2D" if c<0 else "#0F6E56" for c in ch],
            text=[f"{c:+.2f}%" for c in ch],textposition="outside"))
        fig_live.update_layout(height=320,yaxis_title="涨跌幅 (%)",plot_bgcolor="#fafafa",
                               showlegend=False,margin=dict(t=20,b=20),
                               yaxis=dict(zeroline=True,zerolinecolor="#cccccc"))
        st.plotly_chart(fig_live, use_container_width=True)
        sentiment_score=market_to_sentiment(live_data)
        label=("极度恐慌" if sentiment_score<20 else "恐慌" if sentiment_score<40
               else "中性" if sentiment_score<60 else "乐观" if sentiment_score<80 else "极度狂热")
        st.subheader(f"当前市场情绪：{label}（{sentiment_score}/100）")
        st.progress(sentiment_score/100)

# ── Tab 6 ──────────────────────────────────────────────────────────────────────
with tabs[5]:
    st.subheader("🔮 核心资产 24 个月多情景价格趋势模拟")
    col1,col2,col3=st.columns(3)
    with col1:
        s0=st.number_input("初始资产价格 ($)",min_value=10.0,value=100.0,step=5.0)
        time_horizon=st.slider("预测周期 (月)",6,36,24)
    with col2:
        base_mu=st.slider("基准年化预期收益率 (μ)",-0.5,1.0,0.15,step=0.05)
        base_sigma=st.slider("基准年化波动率 (σ)",0.1,1.5,0.40,step=0.05)
    with col3:
        macro_shock=st.slider("宏观情绪冲击因子",-5.0,5.0,0.0,step=0.5)
        simulations=st.selectbox("每情景模拟路径数",[5,10,20],index=0)
    st.divider()

    mu_base=base_mu+(macro_shock*0.02); mu_bull=base_mu+0.30+(macro_shock*0.05); mu_bear=base_mu-0.40+(macro_shock*0.05)
    sig_base=base_sigma; sig_bull=max(0.1,base_sigma-0.10); sig_bear=base_sigma+0.30
    paths_base=generate_gbm_paths(s0,mu_base,sig_base,time_horizon,simulations,seed=42)
    paths_bull=generate_gbm_paths(s0,mu_bull,sig_bull,time_horizon,simulations,seed=42)
    paths_bear=generate_gbm_paths(s0,mu_bear,sig_bear,time_horizon,simulations,seed=42)

    fig_trend=go.Figure(); time_axis=np.arange(0,time_horizon+1)
    for lbl,paths,color in [("📊 基准",paths_base,"#534AB7"),("🚀 乐观",paths_bull,"#1D9E75"),("🐻 悲观",paths_bear,"#D85A30")]:
        for i in range(paths.shape[1]):
            fig_trend.add_trace(go.Scatter(x=time_axis,y=paths[:,i],mode="lines",
                line=dict(color=color,width=2 if i==0 else 1,dash="solid" if i==0 else "dot"),
                opacity=0.9 if i==0 else 0.3,name=f"{lbl} 情景",showlegend=(i==0)))
    fig_trend.update_layout(height=500,title=f"未来{time_horizon}个月多情景价格演化路径(GBM蒙特卡洛)",
        xaxis_title="时间 (月)",yaxis_title="预测资产价格 ($)",plot_bgcolor="#fafafa",
        hovermode="x unified",legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    st.plotly_chart(fig_trend, use_container_width=True)

    c1,c2,c3=st.columns(3)
    c1.metric("🚀 乐观情景均值",f"${np.mean(paths_bull[-1]):.2f}",f"{(np.mean(paths_bull[-1])/s0-1)*100:.1f}%")
    c2.metric("📊 基准情景均值",f"${np.mean(paths_base[-1]):.2f}",f"{(np.mean(paths_base[-1])/s0-1)*100:.1f}%",delta_color="off")
    c3.metric("🐻 悲观情景均值",f"${np.mean(paths_bear[-1]):.2f}",f"{(np.mean(paths_bear[-1])/s0-1)*100:.1f}%",delta_color="inverse")

# ── Tab 7: 股票分析器 ──────────────────────────────────────────────────────────
with tabs[6]:
    st.subheader("🔬 股票智能分析器")
    st.caption("输入任意股票代码，自动分析技术面+基本面，给出评级与价格目标")

    # 快捷选股
    st.write("**快捷选择热门股票：**")
    qcols = st.columns(len(POPULAR_STOCKS))
    quick_pick = None
    for i, (group, tickers) in enumerate(POPULAR_STOCKS.items()):
        with qcols[i]:
            st.caption(group)
            for tk in tickers:
                if st.button(tk, key=f"q_{group}_{tk}", use_container_width=True):
                    quick_pick = tk

    st.divider()

    # 股票代码输入
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        ticker_input = st.text_input(
            "输入股票代码（如 AAPL、TSLA、0700.HK）",
            value=quick_pick if quick_pick else "",
            placeholder="AAPL",
        ).strip().upper()
    with col_btn:
        st.write("")
        st.write("")
        analyze_btn = st.button("🔍 开始分析", use_container_width=True, type="primary")

    if ticker_input and (analyze_btn or quick_pick):
        with st.spinner(f"正在分析 {ticker_input}..."):
            result = fetch_stock_analysis(ticker_input)

        if result is None:
            st.error("数据不足，请检查股票代码是否正确。")
        elif "error" in result:
            st.error(f"获取数据失败：{result['error']}")
        else:
            # ── 评级横幅 ──
            st.markdown(f"""
            <div style="background:{result['rating_color']};color:white;padding:20px 24px;
                        border-radius:12px;margin:12px 0;display:flex;align-items:center;gap:16px">
                <span style="font-size:48px">{result['rating_emoji']}</span>
                <div>
                    <div style="font-size:28px;font-weight:700">{result['rating']}</div>
                    <div style="font-size:14px;opacity:0.9">{result['name']} · {result['sector']}</div>
                </div>
                <div style="margin-left:auto;text-align:right">
                    <div style="font-size:32px;font-weight:700">${result['price_now']:.2f}</div>
                    <div style="font-size:13px;opacity:0.9">综合评分：{result['score']}/100</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── 核心指标 ──
            m1,m2,m3,m4,m5 = st.columns(5)
            pct = result["price_target_pct"]
            m1.metric("📍 当前价格", f"${result['price_now']:.2f}")
            m2.metric("🎯 价格目标", f"${result['price_target']:.2f}",
                      f"{'+' if pct>=0 else ''}{pct:.1f}%",
                      delta_color="normal" if pct>=0 else "inverse")
            m3.metric("52周最高", f"${result['price_52w_high']:.2f}",
                      f"{result['price_from_high']:.1f}%", delta_color="inverse")
            m4.metric("RSI (14)", f"{result['rsi']:.1f}",
                      "超卖" if result['rsi']<30 else "超买" if result['rsi']>70 else "正常")
            m5.metric("综合评分", f"{result['score']}/100")

            # ── 价格图表 + 技术指标 ──
            hist = result["hist"]
            close = hist["Close"]
            ma20_s  = close.rolling(20).mean()
            ma50_s  = close.rolling(50).mean()
            bb_mid_s = close.rolling(20).mean()
            bb_std_s = close.rolling(20).std()

            fig_price = make_subplots(
                rows=3, cols=1, shared_xaxes=True,
                row_heights=[0.6, 0.2, 0.2],
                subplot_titles=("价格走势 + 均线 + 布林带", "RSI (14)", "成交量"),
                vertical_spacing=0.06,
            )

            # K线
            fig_price.add_trace(go.Candlestick(
                x=hist.index, open=hist["Open"], high=hist["High"],
                low=hist["Low"], close=hist["Close"],
                name="K线", increasing_line_color="#1D9E75", decreasing_line_color="#A32D2D",
            ), row=1, col=1)
            fig_price.add_trace(go.Scatter(x=hist.index,y=ma20_s,name="MA20",
                line=dict(color="#534AB7",width=1.5)),row=1,col=1)
            fig_price.add_trace(go.Scatter(x=hist.index,y=ma50_s,name="MA50",
                line=dict(color="#D85A30",width=1.5)),row=1,col=1)
            fig_price.add_trace(go.Scatter(x=hist.index,y=bb_mid_s+2*bb_std_s,name="布林上轨",
                line=dict(color="gray",width=1,dash="dot"),showlegend=False),row=1,col=1)
            fig_price.add_trace(go.Scatter(x=hist.index,y=bb_mid_s-2*bb_std_s,name="布林下轨",
                line=dict(color="gray",width=1,dash="dot"),
                fill="tonexty",fillcolor="rgba(128,128,128,0.05)",showlegend=False),row=1,col=1)

            # RSI
            delta_s = close.diff()
            gain_s  = delta_s.clip(lower=0).rolling(14).mean()
            loss_s  = (-delta_s.clip(upper=0)).rolling(14).mean()
            rsi_s   = 100 - 100/(1+gain_s/loss_s.replace(0,1e-9))
            fig_price.add_trace(go.Scatter(x=hist.index,y=rsi_s,name="RSI",
                line=dict(color="#534AB7",width=1.5)),row=2,col=1)
            fig_price.add_hline(y=70,line_dash="dot",line_color="red",row=2,col=1)
            fig_price.add_hline(y=30,line_dash="dot",line_color="green",row=2,col=1)

            # 成交量
            fig_price.add_trace(go.Bar(x=hist.index,y=hist["Volume"],name="成交量",
                marker_color=["#1D9E75" if c>=o else "#A32D2D"
                              for c,o in zip(hist["Close"],hist["Open"])]),row=3,col=1)

            fig_price.update_layout(height=620,plot_bgcolor="#fafafa",
                xaxis_rangeslider_visible=False,showlegend=True,
                legend=dict(orientation="h",y=-0.08))
            st.plotly_chart(fig_price, use_container_width=True)

            # ── 信号列表 ──
            st.subheader("📋 技术信号详情")
            sig_col1, sig_col2 = st.columns(2)
            for i, (icon, title, desc) in enumerate(result["signals"]):
                col = sig_col1 if i % 2 == 0 else sig_col2
                col.markdown(f"**{icon} {title}**  \n{desc}")

            # ── 基本面 ──
            st.subheader("📊 基本面数据")
            f1,f2,f3,f4 = st.columns(4)
            f1.metric("P/E (TTM)", f"{result['pe']:.1f}x" if result['pe'] else "N/A")
            f2.metric("Forward P/E", f"{result['fwd_pe']:.1f}x" if result['fwd_pe'] else "N/A")
            f3.metric("P/B", f"{result['pb']:.2f}x" if result['pb'] else "N/A")
            f4.metric("Beta", f"{result['beta']:.2f}" if result['beta'] else "N/A")

            if result["target_analyst"]:
                upside = (result["target_analyst"] - result["price_now"]) / result["price_now"] * 100
                st.info(f"**华尔街分析师目标价：${result['target_analyst']:.2f}**  较现价 {'+' if upside>=0 else ''}{upside:.1f}%")

            # ── 评级说明 ──
            st.subheader("💡 评级说明")
            rating_guide = {
                "🚀 强力买入 (80-100分)": "多项技术指标同时发出买入信号，趋势强劲，建议积极布局",
                "📈 买入 (65-79分)": "技术面偏多，建议逢低分批买入，控制仓位",
                "⚖️ 持有 (45-64分)": "信号中性，建议持有观望，等待更明确方向",
                "📉 卖出 (30-44分)": "技术面偏空，建议减仓或止损，控制风险",
                "💥 强力卖出 (0-29分)": "多项指标同时发出警告，建议清仓规避风险",
            }
            for r, d in rating_guide.items():
                st.caption(f"**{r}**：{d}")

            st.warning("⚠️ 以上分析基于技术指标，仅供参考，不构成投资建议。投资有风险，入市需谨慎。")
