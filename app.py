
"""
2026 大型IPO与泡沫风险模拟器 - Streamlit版（含实时数据）
"""

import math
import streamlit as st
import plotly.graph_objects as go

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

# AI相关已上市股票（作为市场情绪代理指标）
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

# ── 计算函数 ──────────────────────────────────────────────────────────────────
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

@st.cache_data(ttl=300)  # 缓存5分钟，避免频繁请求
def fetch_market_data():
    try:
        import yfinance as yf
        results = {}
        for ticker, name in MARKET_TICKERS.items():
            try:
                t = yf.Ticker(ticker)
                hist = t.history(period="2d")
                if len(hist) >= 2:
                    price     = hist["Close"].iloc[-1]
                    prev      = hist["Close"].iloc[-2]
                    change    = price - prev
                    change_pct = (change / prev) * 100
                    results[ticker] = {
                        "name": name,
                        "price": round(price, 2),
                        "change": round(change, 2),
                        "change_pct": round(change_pct, 2),
                    }
            except Exception:
                pass
        return results
    except ImportError:
        return {}

def market_to_sentiment(data):
    """根据实时市场数据估算市场情绪分"""
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
        chg = data["^IXIC"]["change_pct"]
        score += chg * 3
    if "NVDA" in data:
        chg = data["NVDA"]["change_pct"]
        score += chg * 2
    return max(0, min(100, round(score)))

# ── 标题 ──────────────────────────────────────────────────────────────────────
st.title("📈 2026 大型IPO与泡沫风险模拟器")
st.caption("数据基于2026年Q1公开市场信息 · 仅供研究参考，不构成投资建议")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 市场概览", "🔍 IPO详情", "🎛️ 泡沫模拟", "📜 历史对比", "📡 实时市场", "📈 趋势预测"
])

# ── Tab 1: 市场概览 ────────────────────────────────────────────────────────────
with tab1:
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
                          yaxis_title="估值 ($B)", showlegend=False,
                          plot_bgcolor="#fafafa")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("市场集中度风险")
    risks = {"AI估值集中": 88, "流动性压力": 79, "盈利能力缺口": 72,
             "锁定期后抛压": 65, "市场吸收能力": 42}
    for label, val in risks.items():
        st.progress(val/100, text=f"{label}：**{val}%**")

# ── Tab 2: IPO详情 ─────────────────────────────────────────────────────────────
with tab2:
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
        m1, m2, m3 = st.columns(3)
        m1.metric("预期估值", val_str)
        m2.metric("年收入", f"${company['rev_b']}B")
        m3.metric("P/S倍数", f"{ps}x")
        m4, m5, m6 = st.columns(3)
        m4.metric("盈利状态", "✓ 盈利" if company["profitable"] else "✗ 亏损")
        m5.metric("首日预期涨幅", f"+{company['exp_pop']}%")
        m6.metric("泡沫风险", f"{company['bubble_risk']}%",
                  delta_color="inverse" if company["bubble_risk"] > 60 else "normal")

    st.subheader("所有公司对比")
    fig_bubble = go.Figure(go.Scatter(
        x=[c["bubble_risk"] for c in IPOS],
        y=[c["exp_pop"] for c in IPOS],
        mode="markers+text",
        text=[c["name"] for c in IPOS],
        textposition="top center",
        marker=dict(
            size=[max(14, math.log(c["val_b"]+1)*4) for c in IPOS],
            color=[c["bubble_risk"] for c in IPOS],
            colorscale="RdYlGn_r", showscale=True,
            colorbar=dict(title="泡沫风险%"),
            line=dict(width=1, color="white"),
        ),
        hovertemplate="<b>%{text}</b><br>泡沫风险: %{x}%<br>首日预期: +%{y}%<extra></extra>",
    ))
    fig_bubble.update_layout(height=380, xaxis_title="泡沫风险 (%)",
                             yaxis_title="首日预期涨幅 (%)",
                             plot_bgcolor="#fafafa", margin=dict(t=10))
    st.plotly_chart(fig_bubble, use_container_width=True)

# ── Tab 3: 泡沫模拟 ────────────────────────────────────────────────────────────
with tab3:
    st.subheader("情景预设")
    sc_cols   = st.columns(4)
    chosen_sc = None
    for i, (name, vals) in enumerate(SCENARIOS.items()):
        if sc_cols[i].button(name, use_container_width=True):
            chosen_sc = vals

    # 尝试从实时数据自动填充情绪
    live_data = fetch_market_data()
    auto_sentiment = market_to_sentiment(live_data)
    if live_data:
        st.caption(f"📡 实时市场情绪估算：**{auto_sentiment}/100**（基于纳斯达克+VIX+英伟达）")

    st.subheader("手动调节参数")
    col_l, col_r = st.columns(2)
    with col_l:
        sentiment = st.slider("市场情绪（0=恐慌，100=狂热）", 0, 100,
                              int(chosen_sc[0]) if chosen_sc else auto_sentiment)
        rate      = st.slider("利率环境（%）", 1.0, 8.0,
                              float(chosen_sc[1]) if chosen_sc else 4.5, step=0.1)
    with col_r:
        ai_speed  = st.slider("AI商业化速度（0=慢，100=快）", 0, 100,
                              int(chosen_sc[2]) if chosen_sc else 60)
        retail    = st.slider("散户参与度（0=低，100=高）", 0, 100,
                              int(chosen_sc[3]) if chosen_sc else 70)

    sim = simulate(sentiment, rate, ai_speed, retail)

    st.subheader("模拟结果")
    r1, r2, r3 = st.columns(3)
    r1.metric("首日预期涨幅", f"+{sim['pop']}%")
    r2.metric("6个月后收益", f"{'+' if sim['six_m']>=0 else ''}{sim['six_m']}%")
    r3.metric("泡沫破裂概率", f"{sim['burst']}%", "未来18个月内", delta_color="inverse")

    temp_label = ("极度过热" if sim["temp"]>80 else "中度过热" if sim["temp"]>60
                  else "温和偏高" if sim["temp"]>40 else "相对理性")
    st.progress(sim["temp"]/100, text=f"泡沫温度计：**{sim['temp']}/100 — {temp_label}**")
    st.info(f"**{sim['label']}**\n\n{sim['desc']}")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=sim["burst"],
        title={"text": "泡沫破裂概率 (%)"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#A32D2D" if sim["burst"]>65 else "#BA7517" if sim["burst"]>40 else "#1D9E75"},
            "steps": [
                {"range": [0,  40], "color": "#E1F5EE"},
                {"range": [40, 70], "color": "#FAEEDA"},
                {"range": [70,100], "color": "#FCEBEB"},
            ],
        },
    ))
    fig_gauge.update_layout(height=280, margin=dict(t=40,b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

# ── Tab 4: 历史对比 ────────────────────────────────────────────────────────────
with tab4:
    st.subheader("历史泡沫周期对比")
    nodes    = HISTORICAL["节点"]
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(
        x=nodes, y=HISTORICAL["2000互联网"], name="2000互联网",
        line=dict(color="#E24B4A", dash="dash", width=2), mode="lines+markers"))
    fig_hist.add_trace(go.Scatter(
        x=nodes, y=HISTORICAL["2021 SPAC"], name="2021 SPAC",
        line=dict(color="#BA7517", dash="dot", width=2), mode="lines+markers"))
    fig_hist.add_trace(go.Scatter(
        x=nodes[:4], y=[100,130,180,240], name="2026 AI IPO(预测)",
        line=dict(color="#534AB7", width=3), mode="lines+markers"))
    fig_hist.update_layout(height=380, yaxis_title="指数 (基准=100)",
                           plot_bgcolor="#fafafa",
                           legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig_hist, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.error("**2000 互联网泡沫**\n\n纳斯达克峰值5,048点，随后暴跌78%。1500+科技公司破产，市值蒸发约$5万亿。")
    col2.warning("**2021 SPAC狂热**\n\n600+ SPAC上市，多数较峰值下跌70%+。利率上升刺破泡沫，散户损失惨重。")
    col3.info("**2026 AI IPO浪潮**\n\n三巨头合计估值$3T，AI占风投80%。部分公司确有营收，但P/S倍数同样极端。")

# ── Tab 5: 实时市场 ────────────────────────────────────────────────────────────
with tab5:
    st.subheader("📡 实时AI相关市场数据")
    st.caption("数据来自雅虎财经，每5分钟自动刷新 · 用于判断当前市场情绪")

    if st.button("🔄 手动刷新"):
        st.cache_data.clear()
        st.rerun()

    live_data = fetch_market_data()

    if not live_data:
        st.warning("无法获取实时数据，请检查网络连接。模拟器仍可正常使用。")
    else:
        # 显示各股票指标
        cols = st.columns(4)
        for i, (ticker, info) in enumerate(live_data.items()):
            col = cols[i % 4]
            delta_color = "inverse" if ticker == "^VIX" else "normal"
            col.metric(
                label=info["name"],
                value=f"{info['price']:,.2f}",
                delta=f"{info['change_pct']:+.2f}%",
                delta_color=delta_color,
            )

        # 涨跌柱状图
        st.subheader("今日涨跌幅")
        tickers_list = [v["name"] for v in live_data.values()]
        changes      = [v["change_pct"] for v in live_data.values()]
        bar_colors   = ["#A32D2D" if c < 0 else "#0F6E56" for c in changes]
        fig_live = go.Figure(go.Bar(
            x=tickers_list, y=changes,
            marker_color=bar_colors,
            text=[f"{c:+.2f}%" for c in changes],
            textposition="outside",
        ))
        fig_live.update_layout(
            height=320, yaxis_title="涨跌幅 (%)",
            plot_bgcolor="#fafafa", showlegend=False,
            margin=dict(t=20, b=20),
            yaxis=dict(zeroline=True, zerolinecolor="#cccccc"),
        )
        st.plotly_chart(fig_live, use_container_width=True)

        # 市场情绪解读
        sentiment_score = market_to_sentiment(live_data)
        label = ("极度恐慌" if sentiment_score < 20 else "恐慌" if sentiment_score < 40
                 else "中性" if sentiment_score < 60 else "乐观" if sentiment_score < 80 else "极度狂热")
        st.subheader(f"当前市场情绪：{label}（{sentiment_score}/100）")
        st.progress(sentiment_score / 100)
        st.caption("基于纳斯达克涨跌幅、VIX恐慌指数、英伟达股价综合计算 · 可直接用于泡沫模拟Tab的情绪参数")
import numpy as np
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ── 资产情景与参数字典 (核心逻辑库) ───────────────────────────────────────────
# 结构：资产名称 -> {"s0": 默认价格, "mu": 默认基准收益, "sigma": 默认基准波动, "scenarios": {具体故事}}
ASSET_SCENARIOS = {
    "个股：英伟达 (NVDA) - AI算力核心": {
        "s0": 130.0, "mu": 0.25, "sigma": 0.45,
        "scenarios": {
            "bull": "🚀 乐观情景 (超预期)：B200等下一代芯片产能瓶颈突破，大型云厂商（微软、亚马逊等）资本支出（CapEx）无衰退迹象，且未出现地缘政治黑天鹅。",
            "base": "📊 基准情景 (符合预期)：芯片按计划交付，供应链保持稳定，市场估值随着实际业绩的增长被逐步且健康地消化。",
            "bear": "🐻 悲观情景 (逻辑破坏)：下游AI应用迟迟缺乏‘杀手级’产品，导致云厂商削减资本开支；或台积电（TSMC）面临严重的地缘冲突与断供危机。"
        }
    },
    "指数：纳斯达克100 (^NDX) - 科技大盘": {
        "s0": 18000.0, "mu": 0.12, "sigma": 0.22, # 指数的波动率显著低于个股
        "scenarios": {
            "bull": "🚀 乐观情景 (金发姑娘经济)：美联储（Fed）开启连续降息周期，宏观经济实现完美‘软着陆’，同时AI技术实质性提升了标普企业的整体生产率。",
            "base": "📊 基准情景 (温和增长)：利率维持中性区间，美国宏观经济未见显著衰退，大型科技股盈利基本符合华尔街的一致预期。",
            "bear": "🐻 悲观情景 (滞胀或硬着陆)：通胀意外反弹迫使美联储重新加息（资金面收紧），或者美国经济数据恶化陷入深度衰退，引发系统性估值杀跌。"
        }
    },
    "IPO标的：SpaceX - 太空科技龙头": {
        "s0": 100.0, "mu": 0.30, "sigma": 0.60, # 一级/刚上市资产波动率极高
        "scenarios": {
            "bull": "🚀 乐观情景 (商业化爆发)：星舰（Starship）全面实现常态化商业发射，星链（Starlink）垄断全球卫星互联网并产生巨额自由现金流，IPO遭机构疯抢。",
            "base": "📊 基准情景 (稳步推进)：各项发射任务按部就班，市场愿意为马斯克的愿景和其在航天领域的绝对垄断地位支付较高的估值溢价。",
            "bear": "🐻 悲观情景 (重大挫折)：核心火箭在关键载人或大额商业任务中遭遇灾难性失败；或者NASA等政府大额合同被竞争对手大幅分食。"
        }
    },
    "期货：VIX 恐慌指数期货": {
        "s0": 15.0, "mu": 0.0, "sigma": 0.80, # VIX具有均值回归特性，且波动极大
        "scenarios": {
            "bull": "🚀 乐观情景 (系统崩溃)：这是VIX的‘多头’情景。全球爆发黑天鹅事件（如突发战争、大型金融机构倒闭），市场流动性瞬间枯竭，期权对冲需求井喷。",
            "base": "📊 基准情景 (市场平静)：宏观无重大消息，VIX在13-18的历史低位区间震荡，由于期货升水（Contango），多头面临展期损耗。",
            "bear": "🐻 悲观情景 (极度贪婪)：AI泡沫持续膨胀且无任何利空阻力，散户与机构一致看多，市场波动率被极度压缩至个位数。"
        }
    }
}
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
import datetime

# ── Tab 6: 趋势预测 (接入实时市场数据版) ──────────────────────────────────────────
with tab6:
    st.subheader("🔮 资产多情景演化路径 (实时数据驱动版)")
    st.caption("基于雅虎财经实时数据自动计算历史波动率与收益率，驱动 GBM 蒙特卡洛模拟")

    # 1. 控制面板：数据源与资产选择
    col_mode, col_ticker, col_horizon = st.columns([1, 1, 1])
    with col_mode:
        use_live_data = st.toggle("📡 开启实时市场数据抓取", value=True, help="开启后将自动计算该资产过去一年的真实波动率和收益率")
    with col_ticker:
        # 支持用户输入任意美股代码或指数代码
        ticker_symbol = st.text_input("输入资产代码 (如 NVDA, ^NDX, MSFT, TSLA)", value="NVDA")
    with col_horizon:
        time_horizon = st.slider("预测周期 (月)", 6, 36, 24)

    st.divider()

    # 2. 数据获取与参数推导模块
    @st.cache_data(ttl=3600) # 缓存1小时，避免API请求超限
    def fetch_and_calc_params(ticker):
        try:
            # 获取过去 1 年的数据
            data = yf.download(ticker, period="1y", progress=False)
            if data.empty:
                return None, "未找到该资产数据，请检查代码。"
            
            # 提取收盘价 (处理多重索引问题)
            if isinstance(data.columns, pd.MultiIndex):
                close_prices = data['Close'][ticker].dropna()
            else:
                close_prices = data['Close'].dropna()

            if len(close_prices) < 50:
                return None, "有效交易数据不足，无法计算可靠的波动率。"

            s0 = float(close_prices.iloc[-1]) # 最新收盘价
            
            # 计算每日收益率
            daily_returns = close_prices.pct_change().dropna()
            
            # 年化历史波动率 = 日波动率 * sqrt(252)
            hist_sigma = float(daily_returns.std() * np.sqrt(252))
            
            # 年化历史收益率 = (最新价 / 一年前价格) - 1  (使用过去一年的实际表现作为基准漂移率)
            hist_mu = float((close_prices.iloc[-1] / close_prices.iloc[0]) - 1)
            
            # 加上风控熔断：限制极大极小值，防止图表崩溃
            hist_mu = max(-0.8, min(1.5, hist_mu)) 
            hist_sigma = max(0.05, min(1.2, hist_sigma))
            
            return {"s0": s0, "mu": hist_mu, "sigma": hist_sigma}, None
        except Exception as e:
            return None, str(e)

    # 3. 初始化核心参数
    s0, base_mu, base_sigma = 100.0, 0.15, 0.40 # 默认兜底参数
    
    if use_live_data and ticker_symbol:
        with st.spinner(f"正在从市场抓取 {ticker_symbol} 的量化特征..."):
            live_params, err = fetch_and_calc_params(ticker_symbol)
            if err:
                st.error(f"数据获取失败: {err}")
            elif live_params:
                s0 = live_params["s0"]
                base_mu = live_params["mu"]
                base_sigma = live_params["sigma"]
                st.success(f"✅ 成功同步实时数据！最新价: **${s0:,.2f}** | 历史年化收益: **{base_mu*100:.1f}%** | 历史年化波动率: **{base_sigma*100:.1f}%**")

    # 允许用户在实时数据基础上进一步手动微调
    st.markdown("#### ⚙️ 参数微调与外力冲击")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        s0 = st.number_input("起始价格 ($)", value=s0, step=5.0)
    with c2:
        base_mu = st.number_input("基准年化收益 (μ)", value=float(base_mu), step=0.05)
    with c3:
        base_sigma = st.number_input("基准年化波动率 (σ)", value=float(base_sigma), step=0.05)
    with c4:
        macro_shock = st.slider("宏观情绪冲击因子", -5.0, 5.0, 0.0, step=0.5, help="外生变量：模拟突发利好或利空")

    # 4. 几何布朗运动 (GBM) 核心模型
    def generate_gbm_paths(S0, mu, sigma, T_months, n_paths):
        dt = 1 / 12
        N_steps = T_months
        paths = np.zeros((N_steps + 1, n_paths))
        paths[0] = S0
        for t in range(1, N_steps + 1):
            Z = np.random.standard_normal(n_paths) 
            paths[t] = paths[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
        return paths

    # 情景参数设定 (加入冲击因子)
    mu_base = base_mu + (macro_shock * 0.02)
    sigma_base = base_sigma

    mu_bull = base_mu + 0.25 + (macro_shock * 0.05)
    sigma_bull = max(0.1, base_sigma - 0.10) # 牛市波动通常较低

    mu_bear = base_mu - 0.40 + (macro_shock * 0.05)
    sigma_bear = min(1.5, base_sigma + 0.30) # 熊市恐慌波动飙升

    simulations = 10 # 默认跑10条路径保持界面清爽
    np.random.seed(42)
    paths_base = generate_gbm_paths(s0, mu_base, sigma_base, time_horizon, simulations)
    paths_bull = generate_gbm_paths(s0, mu_bull, sigma_bull, time_horizon, simulations)
    paths_bear = generate_gbm_paths(s0, mu_bear, sigma_bear, time_horizon, simulations)

    # 5. 图表渲染
    fig_trend = go.Figure()
    time_axis = np.arange(0, time_horizon + 1)

    def add_paths(fig, paths, color, name_prefix):
        for i in range(paths.shape[1]):
            show_leg = True if i == 0 else False
            fig.add_trace(go.Scatter(
                x=time_axis, y=paths[:, i], mode='lines',
                line=dict(color=color, width=1.5, dash='solid' if i==0 else 'dot'),
                opacity=0.8 if i==0 else 0.2,
                name=f"{name_prefix}", showlegend=show_leg
            ))

    add_paths(fig_trend, paths_base, "#534AB7", "📊 基准情景")
    add_paths(fig_trend, paths_bull, "#1D9E75", "🚀 乐观情景")
    add_paths(fig_trend, paths_bear, "#D85A30", "🐻 悲观情景")

    fig_trend.update_layout(
        height=450, margin=dict(t=30, b=10),
        xaxis_title="未来月份", yaxis_title="预测价格 ($)",
        plot_bgcolor="#fafafa", hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # 6. 数据统计面板
    r1, r2, r3 = st.columns(3)
    r1.metric("🚀 乐观预期均价 (T+"+str(time_horizon)+")", f"${np.mean(paths_bull[-1]):,.2f}", f"{(np.mean(paths_bull[-1])/s0 - 1)*100:+.1f}%")
    r2.metric("📊 基准预期均价 (T+"+str(time_horizon)+")", f"${np.mean(paths_base[-1]):,.2f}", f"{(np.mean(paths_base[-1])/s0 - 1)*100:+.1f}%", delta_color="off")
    r3.metric("🐻 悲观预期均价 (T+"+str(time_horizon)+")", f"${np.mean(paths_bear[-1]):,.2f}", f"{(np.mean(paths_bear[-1])/s0 - 1)*100:+.1f}%", delta_color="inverse")
    
    
