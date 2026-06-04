"""
2026 大型IPO与泡沫风险模拟器 - Streamlit版
部署: streamlit run app.py
"""

import math
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── 页面配置 ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="2026 IPO泡沫模拟器",
    page_icon="📈",
    layout="wide",
)

# ── 数据 ──────────────────────────────────────────────────────────────────────
IPOS = [
    {"name": "SpaceX",       "sector": "太空科技", "val_b": 1750, "rev_b": 12.4,
     "profitable": True,  "float_pct": 4,  "exp_pop": 22, "bubble_risk": 45, "date": "2026年6月",
     "desc": "S-1已于5月20日提交，预计6月定价。唯一盈利的超级IPO，收入$124亿，自由现金流为正。流通比例仅4-5%，流通量极度受限。"},
    {"name": "OpenAI",       "sector": "人工智能", "val_b": 1000, "rev_b": 3.4,
     "profitable": False, "float_pct": 5,  "exp_pop": 35, "bubble_risk": 78, "date": "2026年Q4",
     "desc": "ChatGPT母公司，月活超5亿，年收入约$34亿但仍大幅亏损。内部治理复杂，从非营利转向营利结构存在法律不确定性。"},
    {"name": "Anthropic",    "sector": "人工智能", "val_b": 965,  "rev_b": 1.8,
     "profitable": False, "float_pct": 5,  "exp_pop": 40, "bubble_risk": 82, "date": "2026年Q4",
     "desc": "Claude系列模型公司，Series H估值$965亿。亚马逊和谷歌为主要战略投资方，AI安全定位差异化。"},
    {"name": "Databricks",   "sector": "企业AI",   "val_b": 134,  "rev_b": 2.8,
     "profitable": True,  "float_pct": 8,  "exp_pop": 18, "bubble_risk": 38, "date": "2026年H1",
     "desc": "数据+AI平台，年收入$28亿，正自由现金流。2026年IPO中基本面最扎实的AI公司，估值约47x收入。"},
    {"name": "Shein",        "sector": "电商",     "val_b": 66,   "rev_b": 38.0,
     "profitable": True,  "float_pct": 10, "exp_pop": 12, "bubble_risk": 52, "date": "2026年H1",
     "desc": "快时尚电商巨头，GMV超$380亿，盈利。主要风险：关税政策、ESG压力和地缘政治风险。"},
    {"name": "Reliance Jio", "sector": "电信",     "val_b": 137,  "rev_b": 22.0,
     "profitable": True,  "float_pct": 8,  "exp_pop": 15, "bubble_risk": 35, "date": "2026年H1",
     "desc": "印度最大电信运营商，5亿+用户，市占率42%。估值$1200-1540亿区间，基本面稳健。"},
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
    "2026 AI(预测)": [100, 130, 180, 240, None, None, None, None, None],
}

COLORS = ["#185FA5","#534AB7","#7F77DD","#1D9E75","#D85A30","#0F6E56"]

# ── 计算函数 ──────────────────────────────────────────────────────────────────
def simulate(sentiment, rate, ai_speed, retail):
    pop   = round(5 + sentiment*0.4 + ai_speed*0.2 - rate*2 + retail*0.15)
    six_m = round((sentiment-50)*0.3 + (ai_speed-50)*0.2 - (rate-4)*8 + (retail-50)*0.1)
    burst = max(5, min(95, round(100 - sentiment*0.4 - ai_speed*0.2 + rate*6 - retail*0.05)))
    temp  = max(0, min(100, round(sentiment*0.4 + ai_speed*0.3 + retail*0.2 + (100-rate*8)*0.1)))
    labels = ["极度乐观","温和上行","基准预期","高度警觉","泡沫破裂风险"]
    descs  = [
        "AI商业化超预期叠加宽松流动性，各IPO首日均大幅上涨。散户FOMO情绪驱动短期溢价，但基本面支撑不足，需警惕6-12个月后的回调。",
        "市场情绪良好，优质标的（SpaceX、Databricks）表现稳健。AI概念公司获适度溢价，但盈利能力将成为分化关键指标。",
        "基于当前参数，市场处于可控高估值区间。锁定期到期（约180天）后预计出现首次较大波动。",
        "高利率+高估值形成压力，AI商业化不及预期将触发大幅回调。类比2000年3月，纳斯达克可能在6个月内下跌30%+。",
        "多重风险共振：流动性枯竭+盈利预期落空+锁定期抛售。历史类比：2000年互联网崩盘。",
    ]
    idx = min(4, burst // 20)
    return {"pop": pop, "six_m": six_m, "burst": burst, "temp": temp,
            "label": labels[idx], "desc": descs[idx]}

# ── 标题 ──────────────────────────────────────────────────────────────────────
st.title("📈 2026 大型IPO与泡沫风险模拟器")
st.caption("数据基于2026年Q1公开市场信息 · 仅供研究参考，不构成投资建议")

tab1, tab2, tab3, tab4 = st.tabs(["🏠 市场概览", "🔍 IPO详情", "🎛️ 泡沫模拟", "📜 历史对比"])

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
    fig_bar.update_layout(height=350, margin=dict(t=20,b=20),
                          yaxis_title="估值 ($B)", showlegend=False,
                          plot_bgcolor="#fafafa")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("市场集中度风险")
    risks = {"AI估值集中": 88, "流动性压力": 79, "盈利能力缺口": 72,
             "锁定期后抛压": 65, "市场吸收能力": 42}
    for label, val in risks.items():
        color = "normal" if val < 50 else "inverse"
        st.progress(val/100, text=f"{label}：**{val}%**")

# ── Tab 2: IPO详情 ─────────────────────────────────────────────────────────────
with tab2:
    selected = st.selectbox("选择公司", [c["name"] for c in IPOS])
    company = next(c for c in IPOS if c["name"] == selected)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader(company["name"])
        st.caption(company["sector"] + " · " + company["date"])
        st.write(company["desc"])

    with col2:
        ps = round(company["val_b"] / company["rev_b"])
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
    sc_cols = st.columns(4)
    chosen_sc = None
    for i, (name, vals) in enumerate(SCENARIOS.items()):
        if sc_cols[i].button(name, use_container_width=True):
            chosen_sc = vals

    st.subheader("手动调节参数")
    col_l, col_r = st.columns(2)
    with col_l:
        sentiment = st.slider("市场情绪（0=恐慌，100=狂热）", 0, 100,
                              int(chosen_sc[0]) if chosen_sc else 65)
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

    st.subheader("泡沫温度计")
    temp_label = ("极度过热" if sim["temp"]>80 else "中度过热" if sim["temp"]>60
                  else "温和偏高" if sim["temp"]>40 else "相对理性")
    st.progress(sim["temp"]/100, text=f"**{sim['temp']}/100 — {temp_label}**")

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
    nodes = HISTORICAL["节点"]
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
                           plot_bgcolor="#fafafa", legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("三大泡沫对比")
    col1, col2, col3 = st.columns(3)
    col1.error("**2000 互联网泡沫**\n\n纳斯达克峰值5,048点，随后暴跌78%。1500+科技公司破产。市值蒸发约$5万亿。")
    col2.warning("**2021 SPAC狂热**\n\n600+ SPAC上市，多数较峰值下跌70%+。利率上升刺破泡沫，散户损失惨重。")
    col3.info("**2026 AI IPO浪潮**\n\n三巨头合计估值$3T，AI占风投80%。部分公司确有营收，但P/S倍数同样极端。")
