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

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 苹果风毛玻璃主题（Glassmorphism）
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── 页面底色：网格 + 噪点 + 多层光晕（为毛玻璃提供可虚化的底纹）── */
.stApp {
    background-color: #EAF0F8;
    background-image:
        /* 1. 极细噪点，消除渐变色带、增加质感 */
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E"),
        /* 2. 淡淡的行情网格（透过毛玻璃会被柔化，正是玻璃质感的来源）*/
        repeating-linear-gradient(0deg,  rgba(15,23,42,0.035) 0 1px, transparent 1px 44px),
        repeating-linear-gradient(90deg, rgba(15,23,42,0.035) 0 1px, transparent 1px 44px),
        /* 3. 四周暗角，把视线收拢到内容区 */
        radial-gradient(115% 95% at 50% 45%, transparent 52%, rgba(15,23,42,0.07) 100%),
        /* 4. 顶部高光，让标题区域更透亮 */
        radial-gradient(1250px 560px at 50% -12%, rgba(255,255,255,0.92), transparent 72%),
        /* 5. 四角柔光晕 */
        radial-gradient(860px 600px at 2% -4%,   rgba(96,132,255,0.26), transparent 62%),
        radial-gradient(780px 540px at 99% 2%,   rgba(255,122,170,0.20), transparent 60%),
        radial-gradient(940px 640px at 8% 102%,  rgba(72,214,186,0.22), transparent 62%),
        radial-gradient(840px 580px at 96% 98%,  rgba(158,124,255,0.19), transparent 60%),
        /* 6. 基础渐变 */
        linear-gradient(172deg, #F8FAFD 0%, #EDF2F9 48%, #E5ECF7 100%);
    background-size: 220px 220px, auto, auto, auto, auto, auto, auto, auto, auto, auto;
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: transparent; }

/* ── 强制浅色外观：本应用整体为浅色设计，避免系统深色模式下文字看不清 ── */
html, body, .stApp { color-scheme: light; }
.stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stWidgetLabel"] { color: #0f172a; }
.stApp [data-testid="stCaptionContainer"], .stApp small { color: #5b6678 !important; }
/* 输入控件在深色模式下也保持浅色 */
.stApp input, .stApp textarea,
.stApp [data-baseweb="input"] > div, .stApp [data-baseweb="base-input"],
.stApp [data-baseweb="select"] > div, .stApp [data-baseweb="popover"] li {
    background: rgba(255,255,255,0.80) !important;
    color: #0f172a !important;
}
.stApp [data-baseweb="popover"] ul { background: #ffffff !important; }
.stApp [data-testid="stNumberInputStepUp"],
.stApp [data-testid="stNumberInputStepDown"] {
    background: rgba(255,255,255,0.88) !important;
    color: #0f172a !important;
    border-left: 1px solid rgba(15,23,42,0.07) !important;
}
.stApp [data-testid="stNumberInputStepUp"] svg,
.stApp [data-testid="stNumberInputStepDown"] svg { fill: #0f172a !important; }
.stApp [data-testid="stExpander"] details,
.stApp [data-testid="stExpander"] summary { background: transparent !important; }

/* ── 指标卡：毛玻璃 ── */
div[data-testid="stMetric"], div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.55);
    -webkit-backdrop-filter: blur(22px) saturate(180%);
    backdrop-filter: blur(22px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.75);
    border-radius: 18px;
    padding: 14px 16px !important;
    box-shadow: 0 6px 22px rgba(15,23,42,0.07);
    transition: transform .18s ease, box-shadow .18s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(15,23,42,0.13);
}

/* ── 图表容器：毛玻璃相框 ── */
div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.48);
    -webkit-backdrop-filter: blur(20px) saturate(170%);
    backdrop-filter: blur(20px) saturate(170%);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 22px;
    padding: 12px 10px 14px;
    box-shadow: 0 8px 28px rgba(15,23,42,0.07);
}

/* ── 隐藏 Plotly 工具栏（下载图片/缩放等按钮）── */
.js-plotly-plot .modebar, .modebar-container, .modebar { display: none !important; }

/* ── 数值解读条：告诉用户"为什么是这个结果" ── */
.whybox {
    font-size: 11.8px; line-height: 1.7; color: #334155;
    padding: 8px 12px; border-radius: 10px; margin: -6px 0 14px;
}
.stApp .whybox, .stApp .whybox span { color: #334155; }
.whybox .wt { font-weight: 700; }
.whybox .calc {
    display: block; margin-top: 4px; font-size: 11px; color: #5b6678;
    font-variant-numeric: tabular-nums;
}

/* ── 折叠面板 / 提示框 ── */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.52);
    -webkit-backdrop-filter: blur(20px) saturate(175%);
    backdrop-filter: blur(20px) saturate(175%);
    border: 1px solid rgba(255,255,255,0.72) !important;
    border-radius: 18px !important;
    box-shadow: 0 6px 22px rgba(15,23,42,0.06);
    overflow: hidden;
}
div[data-testid="stAlert"] {
    -webkit-backdrop-filter: blur(16px) saturate(160%);
    backdrop-filter: blur(16px) saturate(160%);
    border-radius: 14px;
}

/* ── 顶部页签：苹果分段控件 ── */
div[data-testid="stTabs"] div[role="tablist"] {
    gap: 4px;
    background: rgba(255,255,255,0.45);
    -webkit-backdrop-filter: blur(18px) saturate(180%);
    backdrop-filter: blur(18px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 16px;
    padding: 5px;
    box-shadow: 0 4px 16px rgba(15,23,42,0.06);
}
div[data-testid="stTabs"] button[role="tab"] {
    border-radius: 12px;
    padding: 6px 14px;
    transition: background .18s ease, box-shadow .18s ease;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: rgba(255,255,255,0.92);
    box-shadow: 0 2px 8px rgba(15,23,42,0.10);
}
div[data-testid="stTabs"] div[role="tablist"] + div [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none; }

/* ── 按钮 / 输入框 ── */
div[data-testid="stButton"] > button {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.8);
    background: rgba(255,255,255,0.62);
    -webkit-backdrop-filter: blur(14px);
    backdrop-filter: blur(14px);
    box-shadow: 0 2px 10px rgba(15,23,42,0.06);
    transition: transform .15s ease, box-shadow .15s ease;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(15,23,42,0.12);
}
div[data-testid="stProgress"] > div > div {
    border-radius: 99px;
    background: rgba(15,23,42,0.10) !important;
}
div[data-testid="stProgress"] > div > div > div {
    border-radius: 99px;
    background: linear-gradient(90deg, #6C8BFF 0%, #534AB7 100%) !important;
}

/* ══ 资产卡片（Logo 水印 + 毛玻璃） ══ */
.ac-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(var(--acmin, 220px), 1fr));
    gap: 14px;
    margin: 8px 0 10px;
}
.ac {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    min-height: 132px;
    background: linear-gradient(135deg, #ffffff 0%, #eef2f8 100%);
    box-shadow: 0 8px 26px rgba(15,23,42,0.10);
    transition: transform .2s ease, box-shadow .2s ease;
}
.ac:hover { transform: translateY(-3px); box-shadow: 0 16px 36px rgba(15,23,42,0.16); }
/* 背景大 Logo 水印——被上层毛玻璃虚化 */
.ac-wm {
    position: absolute; right: -6%; top: 50%;
    transform: translateY(-50%);
    width: 70%; height: 104%;
    object-fit: contain; object-position: right center;
    opacity: .30; pointer-events: none;
}
.ac-wm-txt {
    position: absolute; right: -6px; top: 50%;
    transform: translateY(-50%);
    font-size: 84px; font-weight: 800; letter-spacing: -3px;
    opacity: .18; pointer-events: none; line-height: 1;
}
.ac-glass {
    position: relative; height: 100%;
    padding: 13px 15px;
    display: flex; flex-direction: column; justify-content: space-between;
    background: rgba(255,255,255,0.52);
    -webkit-backdrop-filter: blur(13px) saturate(185%);
    backdrop-filter: blur(13px) saturate(185%);
    border: 1px solid rgba(255,255,255,0.72);
    border-radius: 20px;
}
.ac-top { display: flex; align-items: center; gap: 9px; }
.ac-chip {
    width: 34px; height: 34px; border-radius: 11px; flex: 0 0 34px;
    background: rgba(255,255,255,0.92);
    box-shadow: 0 2px 8px rgba(15,23,42,0.13);
    display: flex; align-items: center; justify-content: center;
    overflow: hidden;
}
.ac-chip img { width: 26px; height: 26px; object-fit: contain; }
.ac-chip span { font-size: 13px; font-weight: 800; letter-spacing: -.5px; }
.ac-name { font-size: 13.5px; font-weight: 700; color: #0f172a; line-height: 1.25; }
.ac-sub  { font-size: 10.5px; color: #64748b; margin-top: 1px; letter-spacing: .3px; }
.ac-val  { font-size: 25px; font-weight: 750; color: #0f172a; letter-spacing: -.6px; margin-top: 6px; }
.ac-chg  { font-size: 12.5px; font-weight: 700; display: inline-flex; align-items: center;
           gap: 4px; padding: 2px 9px; border-radius: 99px; width: fit-content; margin-top: 4px; }
.ac-up   { color: #0F6E56; background: rgba(29,158,117,0.14); }
.ac-down { color: #A32D2D; background: rgba(226,75,74,0.14); }
.ac-flat { color: #64748b; background: rgba(100,116,139,0.13); }
.ac-note { font-size: 10.5px; color: #64748b; margin-top: 4px; }

/* ══ 资产主视觉横幅（分析页顶部） ══ */
.ahero {
    position: relative; border-radius: 24px; overflow: hidden;
    margin: 12px 0 16px; min-height: 132px;
    box-shadow: 0 14px 40px rgba(15,23,42,0.16);
}
.ahero-wm {
    position: absolute; right: 1.5%; top: 50%; transform: translateY(-50%);
    width: 34%; height: 165%;
    object-fit: contain; object-position: right center;
    opacity: .40; pointer-events: none;
}
.ahero-wm-txt {
    position: absolute; right: 3%; top: 50%; transform: translateY(-50%);
    font-size: 120px; font-weight: 800; color: #fff; opacity: .16; line-height: 1;
    letter-spacing: -4px; pointer-events: none;
}
.ahero-glass {
    position: relative; padding: 20px 24px;
    display: flex; align-items: center; gap: 16px;
    background: rgba(255,255,255,0.16);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.28);
    border-radius: 24px; color: #fff;
}
.ahero-chip {
    width: 58px; height: 58px; border-radius: 17px; flex: 0 0 58px;
    background: rgba(255,255,255,0.95);
    box-shadow: 0 4px 14px rgba(0,0,0,0.18);
    display: flex; align-items: center; justify-content: center; overflow: hidden;
}
.ahero-chip img { width: 44px; height: 44px; object-fit: contain; }
.ahero-chip span { font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: -.6px; }

/* ══ 持仓紧凑行 ══ */
.arow {
    position: relative; display: flex; align-items: center; gap: 11px;
    border-radius: 15px; overflow: hidden; margin-bottom: 8px;
    padding: 9px 14px;
    background: rgba(255,255,255,0.55);
    -webkit-backdrop-filter: blur(18px) saturate(180%);
    backdrop-filter: blur(18px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.72);
    box-shadow: 0 4px 16px rgba(15,23,42,0.07);
    transition: transform .16s ease, box-shadow .16s ease;
}
.arow:hover { transform: translateX(2px); box-shadow: 0 8px 22px rgba(15,23,42,0.12); }
.arow-chip {
    width: 30px; height: 30px; border-radius: 10px; flex: 0 0 30px;
    background: rgba(255,255,255,0.95); box-shadow: 0 2px 7px rgba(15,23,42,0.13);
    display: flex; align-items: center; justify-content: center; overflow: hidden;
}
.arow-chip img { width: 23px; height: 23px; object-fit: contain; }
.arow-chip span { font-size: 11px; font-weight: 800; letter-spacing: -.4px; }

/* ── 组件配色复位（优先级高于上面的"强制浅色"规则）── */
.stApp .ac-name { color: #0f172a; }
.stApp .ac-sub, .stApp .ac-note { color: #64748b; }
.stApp .ac-val { color: #0f172a; }
.stApp .ac-chg.ac-up   { color: #0F6E56; }
.stApp .ac-chg.ac-down { color: #A32D2D; }
.stApp .ac-chg.ac-flat { color: #64748b; }
/* 深色横幅内：未自带颜色的文字保持白色，自带颜色的（涨跌标签）不动 */
.stApp .ahero-glass,
.stApp .ahero-glass div:not([style*="color"]),
.stApp .ahero-glass span:not([style*="color"]) { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 👀 盯盘模式：只在你盯盘的这段时间里自动刷新，时间一到自动停止
# ══════════════════════════════════════════════════════════════════════════════
def watch_status():
    """返回 (是否盯盘中, 刷新间隔秒, 剩余秒)，并处理会话到期"""
    from datetime import datetime as _dtn
    ss = st.session_state
    until = ss.get("watch_until")
    if until:
        left = (until - _dtn.now()).total_seconds()
        if left <= 0:
            ss["watch_until"] = None
            ss["watch_expired"] = True
            return False, ss.get("watch_iv", 60), 0
        return True, ss.get("watch_iv", 60), int(left)
    return False, ss.get("watch_iv", 60), 0

def start_watch(minutes=None, interval=None):
    from datetime import datetime as _dtn, timedelta as _td
    import time as _t
    ss = st.session_state
    ss["watch_iv"] = interval or ss.get("watch_iv", 60)
    ss["watch_min"] = minutes or ss.get("watch_min", 15)
    ss["watch_until"] = _dtn.now() + _td(minutes=ss["watch_min"])
    ss["watch_count"] = 0
    ss["watch_last"] = _t.time()      # 时间闸门起点，防止启动瞬间连环重跑
    ss.pop("watch_expired", None)

def stop_watch():
    st.session_state["watch_until"] = None
    st.session_state.pop("watch_expired", None)

def setup_auto_refresh():
    from datetime import datetime as _dtn
    ss = st.session_state
    active, iv, left = watch_status()
    with st.sidebar:
        st.markdown("### 👀 盯盘模式")
        st.caption(f"本次数据更新于 **{_dtn.now().strftime('%H:%M:%S')}**")
        if active:
            st.success(f"🟢 盯盘中 · 每 {iv} 秒自动刷新\n\n"
                       f"⏳ 剩余 {left//60:02d}:{left%60:02d}　·　已刷新 {ss.get('watch_count', 0)} 次")
            b1, b2 = st.columns(2)
            if b1.button("⏹ 结束盯盘", use_container_width=True, key="watch_stop"):
                stop_watch(); st.rerun()
            if b2.button("⏱ 再延长", use_container_width=True, key="watch_extend",
                         help=f"再延长 {ss.get('watch_min', 15)} 分钟"):
                start_watch(); st.rerun()
        else:
            if ss.pop("watch_expired", False):
                st.info("⏸️ 盯盘时段已结束，自动刷新已停止（避免你离开后继续空转）。需要时再点开始。")
            c1, c2 = st.columns(2)
            _iv = c1.selectbox("刷新间隔", [30, 60, 120, 300],
                               index=[30, 60, 120, 300].index(ss.get("watch_iv", 60)),
                               key="watch_iv_sel",
                               format_func=lambda s: f"{s} 秒" if s < 60 else f"{s // 60} 分钟")
            _mn = c2.selectbox("盯盘时长", [5, 15, 30, 60],
                               index=[5, 15, 30, 60].index(ss.get("watch_min", 15)),
                               key="watch_min_sel", format_func=lambda m: f"{m} 分钟")
            if st.button("▶️ 开始盯盘", use_container_width=True, type="primary", key="watch_start"):
                start_watch(minutes=_mn, interval=_iv); st.rerun()
            st.caption("⚪ 当前为手动模式：只有你操作页面或点刷新时才会取新数据，不消耗后台资源。")
        st.caption("行情来自雅虎财经，美股约延迟15分钟；加密货币 24 小时连续报价。")
        if st.button("🔄 立即强制刷新全部数据", use_container_width=True, key="force_refresh_all"):
            st.cache_data.clear()
            st.rerun()
    return active, iv

_auto_on, _auto_interval = setup_auto_refresh()

if _auto_on and hasattr(st, "fragment"):
    try:
        # 心跳片段本身很轻（只重跑自己），真正的整页刷新由下面的时间闸门控制，
        # 否则「片段启动即重跑整页 → 整页重跑又重建片段」会变成死循环。
        _tick_every = max(3, min(_auto_interval, 10))

        @st.fragment(run_every=_tick_every)
        def _auto_refresh_ticker():
            import time as _t
            from datetime import datetime as _d
            ss = st.session_state
            if not ss.get("watch_until"):
                return
            def _do_rerun():
                try:
                    st.rerun(scope="app")
                except TypeError:      # 老版本 st.rerun 不支持 scope
                    st.rerun()
            if _d.now() >= ss["watch_until"]:          # 盯盘时段结束，自动停
                ss["watch_until"] = None
                ss["watch_expired"] = True
                _do_rerun()
                return
            _now = _t.time()
            if _now - ss.get("watch_last", 0) >= ss.get("watch_iv", 60):
                ss["watch_last"] = _now
                ss["watch_count"] = ss.get("watch_count", 0) + 1
                _do_rerun()
        _auto_refresh_ticker()
    except Exception:
        st.sidebar.caption("⚠️ 当前 Streamlit 版本不支持自动刷新，请使用手动刷新按钮。")

# ── Logo 资源（指数/交易所用官方标识，个股与加密货币走公开 Logo CDN）──
LOGO_OVERRIDES = {
    "^IXIC": "https://upload.wikimedia.org/wikipedia/commons/8/87/NASDAQ_Logo.svg",
    "^GSPC": "https://upload.wikimedia.org/wikipedia/commons/e/ee/S%26P_Global_logo.svg",
    "^VIX":  "https://upload.wikimedia.org/wikipedia/commons/8/8a/Cboe_Global_Markets_Logo.svg",
    "^DJI":  "https://upload.wikimedia.org/wikipedia/commons/9/99/NYSE_logo.svg",
}
# 没有 Logo 的标的用 emoji / 文字徽标兜底
LOGO_EMOJI = {
    "^TNX": "🏛️", "GC=F": "🥇", "SI=F": "🥈", "HG=F": "🟠",
    "CL=F": "🛢️", "SPCX": "🚀",
    "^GSPC": "S&P", "^IXIC": "NDQ", "^VIX": "VIX", "^DJI": "DJI",
}
ACCENT_PALETTE = ["#185FA5", "#534AB7", "#1D9E75", "#D85A30", "#0F6E56", "#BA7517", "#7F77DD"]

@st.cache_data(ttl=21600, show_spinner=False)
def fetch_logo_data_uri(ticker: str):
    """抓取标的 Logo 并内联为 data URI（失败返回 None，由字母/emoji 徽标兜底）"""
    import base64, urllib.request
    t = (ticker or "").upper().strip()
    if not t:
        return None
    cands = []
    if t in LOGO_OVERRIDES:
        cands.append(LOGO_OVERRIDES[t])
    elif t.endswith("-USD"):                      # 加密货币
        sym = t[:-4].lower()
        cands.append(f"https://assets.coincap.io/assets/icons/{sym}@2x.png")
    elif not t.startswith("^") and "=" not in t:  # 个股 / ETF
        cands.append(f"https://images.financialmodelingprep.com/symbol/{t}.png")
        cands.append(f"https://assets.parqet.com/logos/symbol/{t}?format=png&size=200")
    for url in cands:
        for _attempt in range(2):                 # 单次超时会重试一次，避免偶发抖动
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = resp.read()
                    if len(data) < 200:           # 过小多半是占位图
                        break
                    ctype = (resp.headers.get("Content-Type") or "image/png").split(";")[0]
                    if "svg" in ctype:
                        ctype = "image/svg+xml"
                    elif "image" not in ctype:
                        ctype = "image/png"
                    return f"data:{ctype};base64," + base64.b64encode(data).decode("ascii")
            except Exception:
                continue
    return None

def _accent_for(ticker: str) -> str:
    return ACCENT_PALETTE[sum(ord(c) for c in (ticker or "X")) % len(ACCENT_PALETTE)]

def _mono(ticker: str) -> str:
    """字母/emoji 徽标文本"""
    t = (ticker or "").upper()
    if t in LOGO_EMOJI:
        return LOGO_EMOJI[t]
    t = t.split("-")[0].split("=")[0].lstrip("^")
    return (t[:2] or "?")

def logo_chip_html(ticker: str, cls: str = "ac-chip") -> str:
    """小尺寸清晰 Logo 徽标"""
    uri = fetch_logo_data_uri(ticker)
    inner = (f'<img src="{uri}" alt="">' if uri
             else f'<span style="color:{_accent_for(ticker)} !important">{_mono(ticker)}</span>')
    return f'<div class="{cls}">{inner}</div>'

def logo_watermark_html(ticker: str, hero: bool = False) -> str:
    """背景大 Logo 水印（会被上层毛玻璃虚化）"""
    uri = fetch_logo_data_uri(ticker)
    if uri:
        return f'<img class="{"ahero-wm" if hero else "ac-wm"}" src="{uri}" alt="">'
    cls = "ahero-wm-txt" if hero else "ac-wm-txt"
    style = "" if hero else f' style="color:{_accent_for(ticker)}"'
    return f'<div class="{cls}"{style}>{_mono(ticker)}</div>'

def asset_card_html(ticker, name, subtitle="", value="", change_pct=None,
                    invert_color=False, note=""):
    """单个资产毛玻璃卡片 HTML（Logo 水印打底）"""
    if change_pct is None:
        chg_html = ""
    else:
        good = (change_pct < 0) if invert_color else (change_pct > 0)
        bad  = (change_pct > 0) if invert_color else (change_pct < 0)
        cls  = "ac-up" if good else "ac-down" if bad else "ac-flat"
        arrow = "▲" if change_pct > 0 else "▼" if change_pct < 0 else "＝"
        chg_html = f'<div class="ac-chg {cls}">{arrow} {change_pct:+.2f}%</div>'
    note_html = f'<div class="ac-note">{note}</div>' if note else ""
    return (
        '<div class="ac">'
        f'{logo_watermark_html(ticker)}'
        '<div class="ac-glass">'
        f'<div class="ac-top">{logo_chip_html(ticker)}'
        f'<div><div class="ac-name">{name}</div>'
        f'<div class="ac-sub">{subtitle or ticker}</div></div></div>'
        f'<div><div class="ac-val">{value}</div>{chg_html}{note_html}</div>'
        '</div></div>'
    )

def render_asset_grid(cards, min_width=220):
    """把若干资产卡片排成自适应网格"""
    st.markdown(
        f'<div class="ac-grid" style="--acmin:{min_width}px">{"".join(cards)}</div>',
        unsafe_allow_html=True,
    )

def glass_chart(fig, **kwargs):
    """统一图表风格：透明背景 + 浅色文字，融入毛玻璃相框"""
    try:
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.30)",
            font=dict(color="#334155"),
            legend=dict(font=dict(color="#334155")),
        )
        fig.update_xaxes(tickfont=dict(color="#475569"), title_font=dict(color="#475569"))
        fig.update_yaxes(tickfont=dict(color="#475569"), title_font=dict(color="#475569"))
        for ann in (fig.layout.annotations or ()):      # 子图标题等
            if ann.font is None or ann.font.color is None:
                ann.font.color = "#334155"
    except Exception:
        pass
    kwargs.setdefault("use_container_width", True)
    kwargs.setdefault("theme", None)   # 不套用 Streamlit 深色图表模板
    kwargs.setdefault("config", {"displayModeBar": False, "displaylogo": False,
                                 "scrollZoom": False})
    try:
        return st.plotly_chart(fig, **kwargs)
    except TypeError:                  # 老版本 Streamlit 不支持 config 参数
        kwargs.pop("config", None)
        return st.plotly_chart(fig, **kwargs)

# ══════════════════════════════════════════════════════════════════════════════
# 📖 数值解读引擎：每个指标都告诉用户"这个数字为什么是这样、意味着什么"
# ══════════════════════════════════════════════════════════════════════════════
_WHY_C  = {"good": "#0F6E56", "bad": "#A32D2D", "warn": "#BA7517", "neutral": "#475569"}
_WHY_BG = {"good": "rgba(29,158,117,.10)", "bad": "rgba(226,75,74,.10)",
           "warn": "rgba(186,117,23,.10)", "neutral": "rgba(100,116,139,.09)"}

def why_html(text, tone="neutral", calc=None, title="为什么是这个结果"):
    import re
    c, bg = _WHY_C.get(tone, "#475569"), _WHY_BG.get(tone, "rgba(100,116,139,.09)")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)   # HTML 块内不会解析 markdown 粗体
    calc_html = f'<span class="calc">{calc}</span>' if calc else ""
    return (f'<div class="whybox" style="border-left:3px solid {c};background:{bg}">'
            f'<span class="wt" style="color:{c}">{title}：</span>{text}{calc_html}</div>')

def why(text, tone="neutral", calc=None, title="为什么是这个结果", target=None):
    """在指标下方渲染一条解读"""
    (target or st).markdown(why_html(text, tone, calc, title), unsafe_allow_html=True)

def interpret_market(ticker, info):
    """解读市场概览里的每个标的：(解读文字, 语气)"""
    p, chg = info["price"], info["change_pct"]
    name = info["name"]

    if ticker == "^VIX":
        if p < 13:
            base, tone = (f"VIX 现在 {p:.2f}，处在**极低区间（低于13）**。它衡量的是标普500未来30天的预期波动，"
                          f"这么低说明几乎没人花钱买下跌保险、市场偏自满——historically 这种时候一旦有利空，回调反而更猛。"), "warn"
        elif p < 20:
            base, tone = (f"VIX 现在 {p:.2f}，属于**平静区间（13–20）**。市场预期未来一个月不会有大波动，"
                          f"风险偏好正常，资金愿意待在股票等风险资产里，这对高估值的AI和IPO标的是有利环境。"), "good"
        elif p < 30:
            base, tone = (f"VIX 现在 {p:.2f}，已进入**紧张区间（20–30）**。投资者正在为下跌买保险，"
                          f"避险需求上升时，最先被卖掉的通常就是没有盈利支撑的高估值成长股。"), "warn"
        else:
            base, tone = (f"VIX 现在 {p:.2f}，处于**恐慌区间（高于30）**。历史上这种水平只在系统性风险事件中出现"
                          f"（如2008、2020年3月），此时泡沫类资产的抛压最集中。"), "bad"
        move = ("今日**大幅回落**，说明恐慌情绪在快速消退、风险偏好回升" if chg < -5 else
                "今日**明显上升**，说明市场正在加速买入下跌保护、担忧升温" if chg > 5 else
                "今日变化不大，情绪维持现状")
        return base + f" {move}（{chg:+.2f}%）。", tone

    if ticker == "^TNX":
        if p < 3:
            body, tone = (f"10年期美债收益率 {p:.2f}%，处于**低位**。它是全球资产定价的「无风险利率」基准，"
                          f"越低意味着未来现金流折现回来越值钱，对靠远期故事支撑的成长股最有利。"), "good"
        elif p < 4.5:
            body, tone = (f"10年期美债收益率 {p:.2f}%，处于**中性偏紧区间**。股票相对债券的吸引力被削弱，"
                          f"但还不至于压垮估值，市场会更看重公司能不能真正赚钱。"), "warn"
        else:
            body, tone = (f"10年期美债收益率 {p:.2f}%，**偏高**。无风险利率越高，折现率就越高，"
                          f"没有当期盈利、只靠远期增长故事的AI股和新股受到的估值压制最大——这也是泡沫风险模型里利率权重很重的原因。"), "bad"
        return body + f" 今日{chg:+.2f}%。", tone

    if ticker in ("^IXIC", "^GSPC"):
        idx = "纳斯达克（科技股集中）" if ticker == "^IXIC" else "标普500（宽基大盘）"
        if chg > 1.5:
            return f"{idx}今日上涨 {chg:+.2f}%，属于**明显放量的风险偏好回升**，通常伴随资金从防御性板块流向成长股。", "good"
        if chg > 0:
            return f"{idx}今日小幅收涨 {chg:+.2f}%，市场情绪偏稳，没有出现方向性突破。", "good"
        if chg > -1.5:
            return f"{idx}今日小幅回落 {chg:+.2f}%，属于正常波动区间，暂时看不出趋势反转。", "neutral"
        return f"{idx}今日下跌 {chg:+.2f}%，跌幅偏大，需要留意是否有宏观利空（利率、通胀或财报）在发酵。", "bad"

    if ticker == "SPCX":
        return (f"SpaceX 现价 ${p:.2f}，今日{chg:+.2f}%。作为2026年最大的IPO，它的走势是市场对"
                f"「高估值、未盈利、故事驱动」这一类资产风险偏好的直接体温计。"), ("good" if chg >= 0 else "bad")

    # 个股
    if chg > 3:
        return f"{name}今日大涨 {chg:+.2f}%，明显强于大盘，多半有个股层面的催化（财报、订单或行业消息）在推动。", "good"
    if chg > 0:
        return f"{name}今日收涨 {chg:+.2f}%，跟随大盘小幅走强，属于常规波动。", "good"
    if chg > -3:
        return f"{name}今日回落 {chg:+.2f}%，幅度不大，更像是随大盘整理而非个股利空。", "neutral"
    return f"{name}今日下跌 {chg:+.2f}%，跌幅偏大，建议结合「股票分析器」看是技术面破位还是基本面出了问题。", "bad"

def interpret_crypto(ticker, info):
    chg, name, p = info["change_pct"], info["name"], info["price"]
    role = {
        "BTC-USD": "比特币是整个加密市场的风险偏好温度计，与纳斯达克的相关性近年明显上升，流动性宽松时涨得最凶",
        "ETH-USD": "以太坊的价格绑定链上活跃度（DeFi、Layer2、RWA），比比特币多一层「生态使用率」的基本面",
        "SOL-USD": "Solana 属于高贝塔品种，牛市涨幅通常超过主流币，回撤也更深",
        "BNB-USD": "币安币与交易所交易量和销毁机制挂钩，受监管消息影响特别大",
        "XRP-USD": "瑞波的价格主要由监管进展和跨境支付采用消息驱动，技术面之外的事件风险高",
        "DOGE-USD": "狗狗币没有现金流和技术护城河，价格几乎完全由社区情绪和名人效应驱动",
    }.get(ticker, "该币种价格主要由市场情绪和流动性驱动")
    if chg > 3:
        return f"现价 ${p:,.2f}，24小时{chg:+.2f}%，**涨势明显**。{role}。", "good"
    if chg > 0:
        return f"现价 ${p:,.2f}，24小时{chg:+.2f}%，小幅走强。{role}。", "good"
    if chg > -3:
        return f"现价 ${p:,.2f}，24小时{chg:+.2f}%，小幅回落，属于加密市场的日常波动。{role}。", "neutral"
    return f"现价 ${p:,.2f}，24小时{chg:+.2f}%，**跌幅较大**。{role}。", "bad"

def interpret_metal(ticker, info):
    chg, p = info["change_pct"], info["price"]
    logic = {
        "GC=F": "黄金涨跌主要看**实际利率和避险需求**：实际利率下行或地缘风险升温时黄金走强",
        "SI=F": "白银是**贵金属+工业金属**双重属性，除了避险，还受光伏和电子需求影响，弹性比黄金大",
        "HG=F": "铜被称为「铜博士」，是**全球经济需求的领先指标**，电动车、电网和数据中心建设是长期需求来源",
        "GDX": "金矿股相对金价有**杠杆效应**，金价涨1%时矿股往往涨2-3%，但也多了矿山成本和运营风险",
        "SLV": "白银ETF跟踪银价，走势同时受避险情绪和工业（光伏）需求影响",
        "FCX": "自由港是全球最大上市铜生产商之一，业绩与铜价高度绑定，可视为**铜价的放大器**",
    }.get(ticker, "该品种主要受大宗商品供需和美元汇率影响")
    if chg > 2:
        return f"现价 ${p:,.2f}，今日{chg:+.2f}%，**涨幅明显**。{logic}。", "good"
    if chg > 0:
        return f"现价 ${p:,.2f}，今日{chg:+.2f}%，小幅走强。{logic}。", "good"
    if chg > -2:
        return f"现价 ${p:,.2f}，今日{chg:+.2f}%，小幅回落。{logic}。", "neutral"
    return f"现价 ${p:,.2f}，今日{chg:+.2f}%，**跌幅较大**。{logic}。", "bad"

def explain_sentiment(data, score):
    """拆解市场情绪分是怎么算出来的"""
    terms, notes = ["中性起点 50"], []
    if "^VIX" in data:
        v = data["^VIX"]["price"]
        pts = 20 if v < 15 else 10 if v < 20 else -10 if v < 30 else -25
        terms.append(f"VIX {v:.1f} → {pts:+d}")
        notes.append(f"VIX {v:.1f}（{'低波动加分' if pts > 0 else '波动升高扣分'}）")
    if "^IXIC" in data:
        c = data["^IXIC"]["change_pct"]
        terms.append(f"纳指 {c:+.2f}% × 3 → {c*3:+.1f}")
        notes.append(f"纳指今日{c:+.2f}%")
    if "NVDA" in data:
        c = data["NVDA"]["change_pct"]
        terms.append(f"英伟达 {c:+.2f}% × 2 → {c*2:+.1f}")
        notes.append(f"英伟达（AI风向标）{c:+.2f}%")
    label = ("极度恐慌" if score < 20 else "恐慌" if score < 40 else
             "中性" if score < 60 else "乐观" if score < 80 else "极度狂热")
    tone = "bad" if score < 40 else "neutral" if score < 60 else "good" if score < 80 else "warn"
    text = (f"这个 **{score}/100（{label}）** 不是拍脑袋来的，而是由三个实时数据加权算出来的："
            + "、".join(notes) + "。三者共同决定了当前风险偏好水平，分数越高说明市场越愿意为高估值资产买单。")
    return text, tone, "计算过程：" + "　".join(terms) + f"　=　{score}"

def explain_simulate(sentiment, rate, ai_speed, retail, sim):
    """拆解泡沫模拟器的四个输出分别是怎么算出来的"""
    def fmt(terms, total, unit="%"):
        return "　".join(terms) + f"　=　{total}{unit}"

    pop_terms = [f"基础 5", f"情绪 {sentiment}×0.4={sentiment*0.4:+.1f}",
                 f"AI速度 {ai_speed}×0.2={ai_speed*0.2:+.1f}",
                 f"利率 {rate}%×2={-rate*2:+.1f}", f"散户 {retail}×0.15={retail*0.15:+.1f}"]
    six_terms = [f"(情绪{sentiment}-50)×0.3={(sentiment-50)*0.3:+.1f}",
                 f"(AI{ai_speed}-50)×0.2={(ai_speed-50)*0.2:+.1f}",
                 f"(利率{rate}-4)×8={-(rate-4)*8:+.1f}",
                 f"(散户{retail}-50)×0.1={(retail-50)*0.1:+.1f}"]
    burst_terms = [f"基础 100", f"情绪 {sentiment}×0.4={-sentiment*0.4:+.1f}",
                   f"AI速度 {ai_speed}×0.2={-ai_speed*0.2:+.1f}",
                   f"利率 {rate}%×6={rate*6:+.1f}", f"散户 {retail}×0.05={-retail*0.05:+.1f}"]

    # 找出影响最大的驱动因素
    drivers = {"市场情绪": sentiment*0.4, "AI商业化速度": ai_speed*0.2,
               "利率环境": -rate*2, "散户参与度": retail*0.15}
    top = max(drivers.items(), key=lambda kv: abs(kv[1]))
    drag = min(drivers.items(), key=lambda kv: kv[1])

    return {
        "pop": (f"首日涨幅是四个输入的加权和：情绪和散户热度推高发行日溢价，利率则是唯一的拖累项。"
                f"当前**{top[0]}贡献最大（{top[1]:+.1f}）**，"
                f"而**{drag[0]}拖累最多（{drag[1]:+.1f}）**。",
                "good" if sim["pop"] > 20 else "neutral",
                fmt(pop_terms, sim["pop"])),
        "six_m": (f"6个月收益衡量的是「上市热度退潮后还剩多少」。它以中性值（情绪50、AI50、散户50、利率4%）为基准，"
                  f"只看偏离量，所以数值通常远小于首日涨幅。利率每高出基准1个百分点就直接扣8个点，是四项里权重最重的。",
                  "good" if sim["six_m"] > 0 else "bad",
                  fmt(six_terms, sim["six_m"])),
        "burst": (f"泡沫破裂概率从100分往下扣：情绪越乐观、AI落地越快、散户越活跃，破裂概率越低；"
                  f"而利率是唯一的**加分项（权重最高，×6）**，因为历史上刺破泡沫的通常都是利率上行"
                  f"（2000年互联网、2021年SPAC都是如此）。当前利率 {rate}% 贡献了 {rate*6:+.1f} 的破裂概率。",
                  "bad" if sim["burst"] > 65 else "warn" if sim["burst"] > 40 else "good",
                  fmt(burst_terms, sim["burst"])),
        "temp": (f"泡沫温度计是情绪(40%)、AI速度(30%)、散户参与(20%)和低利率红利(10%)的综合打分，"
                 f"越接近100说明市场越亢奋。它和破裂概率是一体两面：温度越高，一旦流动性收紧，回撤空间也越大。",
                 "warn" if sim["temp"] > 60 else "neutral",
                 f"情绪 {sentiment}×0.4　AI {ai_speed}×0.3　散户 {retail}×0.2　"
                 f"低利率红利 (100-{rate}×8)×0.1　=　{sim['temp']}/100"),
    }

# ══════════════════════════════════════════════════════════════════════════════
# 🔍 标的搜索库（输入首字母即可联想，如输入 T 会列出所有 T 开头的标的）
# ══════════════════════════════════════════════════════════════════════════════
TICKER_UNIVERSE = {
    # 科技巨头
    "AAPL":"苹果 Apple", "MSFT":"微软 Microsoft", "NVDA":"英伟达 NVIDIA", "GOOGL":"谷歌 Alphabet",
    "GOOG":"谷歌 Alphabet C", "AMZN":"亚马逊 Amazon", "META":"Meta 脸书", "TSLA":"特斯拉 Tesla",
    "AVGO":"博通 Broadcom", "ORCL":"甲骨文 Oracle", "CRM":"Salesforce", "ADBE":"Adobe",
    "AMD":"超微半导体 AMD", "INTC":"英特尔 Intel", "QCOM":"高通 Qualcomm", "TXN":"德州仪器",
    "MU":"美光科技 Micron", "AMAT":"应用材料", "LRCX":"泛林集团", "KLAC":"科磊",
    "TSM":"台积电 TSMC", "ASML":"阿斯麦 ASML", "ARM":"ARM控股", "SMCI":"超微电脑",
    "PLTR":"Palantir", "SNOW":"Snowflake", "NOW":"ServiceNow", "PANW":"Palo Alto",
    "CRWD":"CrowdStrike", "DDOG":"Datadog", "NET":"Cloudflare", "MDB":"MongoDB",
    "SHOP":"Shopify", "XYZ":"Block(原SQ)", "PYPL":"PayPal", "UBER":"优步 Uber", "ABNB":"爱彼迎 Airbnb",
    "COIN":"Coinbase", "HOOD":"Robinhood", "MSTR":"MicroStrategy", "RBLX":"Roblox",
    "SPOT":"Spotify", "NFLX":"奈飞 Netflix", "DIS":"迪士尼 Disney", "TTD":"The Trade Desk",
    "TEAM":"Atlassian", "TWLO":"Twilio", "TOST":"Toast", "ZM":"Zoom", "DOCU":"DocuSign",
    "SOUN":"SoundHound AI", "BBAI":"BigBear.ai", "AI":"C3.ai", "KULR":"KULR Technology",
    "IONQ":"IonQ 量子计算", "RGTI":"Rigetti 量子计算", "QBTS":"D-Wave 量子计算",
    # 金融
    "JPM":"摩根大通", "BAC":"美国银行", "WFC":"富国银行", "GS":"高盛", "MS":"摩根士丹利",
    "C":"花旗集团", "SCHW":"嘉信理财", "BLK":"贝莱德", "V":"Visa", "MA":"万事达 Mastercard",
    "AXP":"美国运通", "BRK-B":"伯克希尔 B", "TFC":"Truist Financial", "TRV":"旅行者保险",
    # 医疗消费工业
    "UNH":"联合健康", "JNJ":"强生", "LLY":"礼来", "PFE":"辉瑞", "MRK":"默沙东",
    "ABBV":"艾伯维", "TMO":"赛默飞世尔", "ABT":"雅培", "DHR":"丹纳赫", "AMGN":"安进",
    "TDOC":"Teladoc 远程医疗", "MRNA":"Moderna", "NVO":"诺和诺德",
    "WMT":"沃尔玛", "COST":"好市多 Costco", "PG":"宝洁", "KO":"可口可乐", "PEP":"百事",
    "MCD":"麦当劳", "NKE":"耐克", "SBUX":"星巴克", "TGT":"塔吉特 Target", "TJX":"TJX公司",
    "HD":"家得宝", "LOW":"劳氏", "BA":"波音", "CAT":"卡特彼勒", "GE":"通用电气",
    "LMT":"洛克希德马丁", "RTX":"雷神技术", "HON":"霍尼韦尔", "UPS":"联合包裹", "FDX":"联邦快递",
    "T":"AT&T 电信", "TMUS":"T-Mobile", "VZ":"威瑞森 Verizon", "CMCSA":"康卡斯特",
    "XOM":"埃克森美孚", "CVX":"雪佛龙", "COP":"康菲石油", "OXY":"西方石油",
    "F":"福特汽车", "GM":"通用汽车", "RIVN":"Rivian", "LCID":"Lucid",
    # 中概股
    "BABA":"阿里巴巴", "JD":"京东", "PDD":"拼多多", "BIDU":"百度", "NTES":"网易",
    "TCOM":"携程 Trip.com", "NIO":"蔚来", "XPEV":"小鹏汽车", "LI":"理想汽车", "BEKE":"贝壳",
    "TME":"腾讯音乐", "YUMC":"百胜中国", "ZTO":"中通快递",
    # 宽基与行业ETF
    "SPY":"标普500 ETF", "QQQ":"纳斯达克100 ETF", "DIA":"道指 ETF", "IWM":"罗素2000 ETF",
    "VTI":"全美股市 ETF", "VOO":"先锋标普500", "VUG":"成长股 ETF", "VTV":"价值股 ETF",
    "ARKK":"ARK创新 ETF", "SOXX":"半导体 ETF", "SMH":"半导体 ETF", "XLK":"科技板块 ETF",
    "XLF":"金融板块 ETF", "XLE":"能源板块 ETF", "XLV":"医疗板块 ETF", "XLI":"工业板块 ETF",
    "XLP":"必需消费 ETF", "XLY":"可选消费 ETF", "XLU":"公用事业 ETF", "XLRE":"房地产 ETF",
    "VGT":"信息科技 ETF", "VNQ":"REITs房地产 ETF", "TQQQ":"纳指三倍做多", "SQQQ":"纳指三倍做空",
    "XLC":"通讯服务 ETF", "XLB":"原材料 ETF", "XBI":"生物科技 ETF", "XHB":"住宅建筑 ETF",
    # 海外与新兴市场
    "EFA":"发达市场(除美) ETF", "VEA":"发达市场 ETF", "VWO":"新兴市场 ETF", "EEM":"新兴市场 ETF",
    "FXI":"中国大盘 ETF", "MCHI":"MSCI中国 ETF", "KWEB":"中概互联 ETF", "EWJ":"日本 ETF",
    "INDA":"印度 ETF", "EWZ":"巴西 ETF", "IEFA":"核心发达市场", "IEMG":"核心新兴市场",
    # 债券
    "TLT":"20年+长期美债 ETF", "IEF":"7-10年美债 ETF", "SHY":"1-3年短债 ETF",
    "BND":"综合债券 ETF", "AGG":"综合债券 ETF", "TIP":"抗通胀债券 ETF", "LQD":"投资级公司债",
    "HYG":"高收益债 ETF", "EDV":"超长久期美债", "ZROZ":"零息长债",
    # 黄金/有色/大宗
    "GLD":"黄金 ETF", "IAU":"黄金 ETF(低费率)", "SLV":"白银 ETF", "GDX":"金矿股 ETF",
    "GDXJ":"初级金矿股 ETF", "PPLT":"铂金 ETF", "DBC":"大宗商品 ETF", "PDBC":"免K1大宗商品",
    "USO":"原油 ETF", "UNG":"天然气 ETF", "NEM":"纽蒙特矿业", "FCX":"自由港麦克莫兰",
    "SCCO":"南方铜业", "AA":"美国铝业", "CLF":"克利夫兰克里夫斯", "XME":"金属采矿 ETF",
    "GC=F":"黄金期货", "SI=F":"白银期货", "HG=F":"铜期货", "CL=F":"原油期货", "NG=F":"天然气期货",
    # 加密货币
    "BTC-USD":"比特币 Bitcoin", "ETH-USD":"以太坊 Ethereum", "SOL-USD":"Solana",
    "BNB-USD":"币安币 BNB", "XRP-USD":"瑞波币 XRP", "DOGE-USD":"狗狗币 Dogecoin",
    "ADA-USD":"艾达币 Cardano", "AVAX-USD":"雪崩 Avalanche", "LINK-USD":"Chainlink",
    "DOT-USD":"波卡 Polkadot", "LTC-USD":"莱特币 Litecoin",
    # 指数
    "^IXIC":"纳斯达克综合指数", "^GSPC":"标普500指数", "^DJI":"道琼斯指数",
    "^VIX":"VIX恐慌指数", "^TNX":"10年期美债收益率", "^RUT":"罗素2000指数",
    "^HSI":"恒生指数", "^N225":"日经225", "^FTSE":"英国富时100",
    # 2026 IPO
    "SPCX":"SpaceX 太空探索",
}

def search_tickers(query, limit=12):
    """代码前缀优先，其次匹配代码包含或公司名包含"""
    q = (query or "").strip()
    if not q:
        return []
    qu = q.upper()
    starts, contains = [], []
    for tk, nm in TICKER_UNIVERSE.items():
        if tk.startswith(qu):
            starts.append((tk, nm))
        elif qu in tk or q.lower() in nm.lower():
            contains.append((tk, nm))
    starts.sort(key=lambda x: (len(x[0]), x[0]))
    return (starts + contains)[:limit]

def _uni_label(tk):
    nm = TICKER_UNIVERSE.get(tk)
    return f"{tk} — {nm}" if nm else tk

def ticker_autocomplete(key, default=None, label="股票代码（边打边出提示）", label_visibility="visible",
                        help_text="输入首字母即可联想，如 X → XOM / XLK / XRP-USD；库里没有的代码也可以直接输入，如 0700.HK"):
    """可搜索下拉框：输入即过滤候选，同时允许输入库里没有的任意代码"""
    opts = list(TICKER_UNIVERSE.keys())
    default = (default or "").strip().upper()
    if default and default not in opts:
        opts = [default] + opts
    idx = opts.index(default) if default in opts else None
    try:
        val = st.selectbox(label, opts, index=idx, key=key, format_func=_uni_label,
                           placeholder="输入代码或名称搜索，如 X、TSLA、特斯拉、比特币",
                           accept_new_options=True, help=help_text,
                           label_visibility=label_visibility)
    except TypeError:
        # 老版本 Streamlit 不支持 accept_new_options：退回「下拉 + 手填」双通道
        val = st.selectbox(label, ["（手动输入其它代码）"] + opts,
                           index=(opts.index(default) + 1) if default in opts else 0,
                           key=key, label_visibility=label_visibility,
                           format_func=lambda x: x if x.startswith("（") else _uni_label(x),
                           help=help_text)
        if val.startswith("（"):
            val = st.text_input("手动输入代码", value=default, key=f"{key}_manual",
                                label_visibility="collapsed")
    return (val or "").strip().upper()

def render_asset_grid_clickable(items, key_prefix, cols=4, btn_label="📊 查看分析与走势"):
    """items: [(ticker, card_html)]；每张卡下方带一个跳转按钮"""
    for start in range(0, len(items), cols):
        chunk = items[start:start + cols]
        cc = st.columns(cols)
        for i, (tk, html) in enumerate(chunk):
            with cc[i]:
                st.markdown(f'<div class="ac-grid" style="--acmin:100%;margin-bottom:6px">{html}</div>',
                            unsafe_allow_html=True)
                if st.button(btn_label, key=f"{key_prefix}_{tk}", use_container_width=True):
                    st.session_state["quick_view_ticker"] = tk
                    st.session_state["selected_ticker"] = tk      # 同步给「股票分析器」
                    st.session_state["analysis_result"] = None
                    st.rerun()

def render_quick_analysis(ticker):
    """点击标的后就地展开：评级横幅 + 关键指标 + K线走势图"""
    r = fetch_stock_analysis(ticker)
    if not r or "error" in r:
        st.error(f"无法获取 {ticker} 的分析数据：{(r or {}).get('error', '数据不足')}")
        return
    _rc = r["rating_color"]
    st.markdown(
        f'<div class="ahero" style="min-height:110px;'
        f'background:linear-gradient(120deg,{_rc} 0%,{_rc}cc 55%,{_rc}99 100%)">'
        f'{logo_watermark_html(r["ticker"], hero=True)}'
        f'<div class="ahero-glass" style="padding:16px 20px">'
        f'{logo_chip_html(r["ticker"], cls="ahero-chip")}'
        f'<span style="font-size:34px;line-height:1">{r["rating_emoji"]}</span>'
        f'<div><div style="font-size:23px;font-weight:750">{r["rating"]}</div>'
        f'<div style="font-size:13px;opacity:.92">{r["name"]} · {r["sector"]}</div></div>'
        f'<div style="margin-left:auto;text-align:right">'
        f'<div style="font-size:28px;font-weight:750">${r["price_now"]:.2f}</div>'
        f'<div style="font-size:12.5px;opacity:.92">综合评分：{r["score"]}/100</div>'
        f'</div></div></div>', unsafe_allow_html=True)

    q1, q2, q3, q4, q5 = st.columns(5)
    q1.metric("现价", f"${r['price_now']:.2f}")
    q2.metric("1个月动量", f"{r['mom_1m']:+.1f}%", delta_color="normal" if r['mom_1m'] >= 0 else "inverse")
    q3.metric("RSI(14)", f"{r['rsi']:.1f}",
              "超卖" if r['rsi'] < 30 else "超买" if r['rsi'] > 70 else "正常")
    q4.metric("52周区间", f"${r['price_52w_low']:.0f}–${r['price_52w_high']:.0f}",
              f"距高点{r['price_from_high']:.1f}%", delta_color="inverse")
    q5.metric("长期评分", f"{r['lt_score']}/100", r["lt_rating"], delta_color="off")

    hist = r.get("hist")
    if hist is None or len(hist) < 5:
        st.info("该标的暂无足够的历史数据绘制走势图。")
    else:
        close = hist["Close"]
        fig_q = go.Figure()
        fig_q.add_trace(go.Candlestick(
            x=hist.index, open=hist["Open"], high=hist["High"],
            low=hist["Low"], close=hist["Close"], name="K线",
            increasing_line_color="#1D9E75", decreasing_line_color="#E24B4A", showlegend=False))
        fig_q.add_trace(go.Scatter(x=hist.index, y=close.rolling(20).mean(), mode="lines",
                                   line=dict(color="#F5A623", width=1.6), name="MA20"))
        fig_q.add_trace(go.Scatter(x=hist.index, y=close.rolling(min(50, len(close))).mean(),
                                   mode="lines", line=dict(color="#534AB7", width=1.6), name="MA50"))
        fig_q.add_hline(y=r["price_now"], line_color="#0F6E56", line_width=1.8,
                        annotation_text=f" 现价 ${r['price_now']:.2f}",
                        annotation_position="right", annotation_font=dict(color="#0F6E56", size=11))
        fig_q.update_layout(
            height=420, title=dict(text=f"{r['ticker']} · 价格走势", font=dict(size=14)),
            xaxis=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                       rangeslider=dict(visible=True, thickness=0.05)),
            yaxis=dict(title="价格 ($)", showgrid=True, gridcolor="#eeeeee"),
            legend=dict(orientation="h", y=1.1, x=0), margin=dict(t=60, b=40, l=60, r=110))
        glass_chart(fig_q)

    st.markdown("**📋 关键技术信号**")
    sc1, sc2 = st.columns(2)
    for i, (icon, title, desc) in enumerate(r.get("signals", [])[:6]):
        (sc1 if i % 2 == 0 else sc2).markdown(f"**{icon} {title}** — {desc}")
    st.caption("想看完整分析（财报、斐波那契、量化面板、宏观联动）请前往「🔬 股票分析器」，代码已自动填好。")

def add_range_tools(fig, range_buttons=True, slider=True, height_add=0):
    """给任意Plotly图表加上时间轴范围按钮和可拖动滑条"""
    rb = []
    if range_buttons:
        rb = [
            dict(count=1,  label="1个月", step="month", stepmode="backward"),
            dict(count=3,  label="3个月", step="month", stepmode="backward"),
            dict(count=6,  label="6个月", step="month", stepmode="backward"),
            dict(count=1,  label="1年",   step="year",  stepmode="backward"),
            dict(count=2,  label="2年",   step="year",  stepmode="backward"),
            dict(step="all", label="全部"),
        ]
    fig.update_xaxes(
        rangeselector=dict(
            buttons=rb,
            bgcolor="#f0f0f0",
            activecolor="#534AB7",
            font=dict(size=11),
            x=0, y=1.02, xanchor="left", yanchor="bottom",
        ) if range_buttons else dict(),
        rangeslider=dict(
            visible=slider,
            thickness=0.06,
            bgcolor="#fafafa",
        ),
        type="date" if range_buttons else None,
    )
    if slider:
        fig.update_layout(height=fig.layout.height + height_add if fig.layout.height else 400 + height_add)
    return fig

def add_year_range_tools(fig, start_year, end_year):
    """给年份轴图表加范围选择按钮（用于趋势预测/蒙地卡罗）"""
    total_years = end_year - start_year
    buttons = []
    for label, years in [("5年",5),("10年",10),("全部",total_years)]:
        if years <= total_years:
            buttons.append(dict(
                label=label,
                method="relayout",
                args=[{"xaxis.range": [end_year-years, end_year]}]
            ))
    buttons.append(dict(label="全部", method="relayout",
                        args=[{"xaxis.range": [start_year, end_year]}]))
    fig.update_layout(
        updatemenus=[dict(
            type="buttons", direction="right",
            x=0, y=1.08, xanchor="left", yanchor="bottom",
            bgcolor="#f0f0f0", bordercolor="#ddd",
            font=dict(size=11),
            buttons=buttons,
        )]
    )
    fig.update_xaxes(
        rangeslider=dict(visible=True, thickness=0.05, bgcolor="#fafafa"),
    )
    return fig

# ── 数据 ──────────────────────────────────────────────────────────────────────
IPOS = [
    {"name": "SpaceX",       "sector": "太空科技", "val_b": 1770, "rev_b": 18.7,
     "profitable": False, "float_pct": 4,  "exp_pop": 19, "bubble_risk": 45,
     "date": "2026年6月12日 ✅已上市", "ticker": "SPCX",
     "price_now": 206.19, "ipo_price": 135.0,
     "desc": "2026年6月12日纳斯达克上市，发行价$135，首日收盘$161（+19%），史上最大IPO。2025年全年营收$187亿（同比+33%），EBITDA $66亿，但GAAP净亏损$49亿。已收购xAI，整合Grok AI和X（Twitter）。累计亏损$413亿。"},
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
    "^TNX":   "10年期国债收益率",
    "NVDA":   "英伟达",
    "MSFT":   "微软",
    "GOOGL":  "谷歌",
    "META":   "Meta",
    "AMZN":   "亚马逊",
    "^GSPC":  "标普500",
    "SPCX":   "SpaceX 🚀",
}

POPULAR_STOCKS = {
    "科技": ["AAPL","MSFT","NVDA","GOOGL","META","AMZN","TSLA","AMD","INTC","ORCL"],
    "AI":   ["NVDA","AMD","SMCI","PLTR","AI","SOUN","BBAI","KULR"],
    "中概股":["BABA","JD","PDD","BIDU","NIO","XPEV","LI"],
    "ETF":  ["QQQ","SPY","ARKK","SOXX","VGT"],
    "加密货币": ["BTC-USD","ETH-USD","SOL-USD","BNB-USD","XRP-USD","DOGE-USD"],
    "有色金属/矿业": ["GLD","SLV","GDX","FCX","NEM","SCCO"],
}

# 加密货币 / 有色金属实时行情用的代码表（Tab1 市场概览）
CRYPTO_TICKERS = {
    "BTC-USD": "比特币",
    "ETH-USD": "以太坊",
    "SOL-USD": "Solana",
    "BNB-USD": "币安币",
    "XRP-USD": "瑞波币",
    "DOGE-USD":"狗狗币",
}
METALS_TICKERS = {
    "GC=F": "黄金期货",
    "SI=F": "白银期货",
    "HG=F": "铜期货",
    "GDX":  "金矿股ETF",
    "SLV":  "白银ETF",
    "FCX":  "自由港矿业(铜)",
}

# 赛道潜力叙事：优先按具体代码匹配，其次按行业(sector)匹配
TRACK_POTENTIAL = {
    "BTC-USD": ("数字黄金 / 价值存储", "#F5A623",
                "比特币的核心叙事是稀缺性（总量2100万枚）+ 机构采用（现货ETF、企业资产负债表配置）。长期潜力取决于能否持续被主流金融体系接纳为价值存储资产；减半周期后的供给收缩是历史上主要的上涨催化剂，但监管政策和宏观流动性仍是最大变量。"),
    "ETH-USD": ("智能合约平台 / Layer2 + DeFi生态", "#534AB7",
                "以太坊是最大的智能合约与DeFi结算层，潜力绑定于Layer2扩容、质押收益（PoS）和现实世界资产（RWA）上链叙事。竞争风险来自Solana等高性能公链的分流，长期表现取决于生态开发者活跃度和费率优化。"),
    "SOL-USD": ("高性能公链", "#1D9E75",
                "Solana主打高吞吐低费率，叙事集中在链上交易（DeFi/meme币/支付）和机构级应用尝试。生态增长速度快是优势，但历史上出现过网络宕机问题，长期能否稳定承载更大规模应用是核心变量。"),
    "BNB-USD": ("交易所生态币", "#BA7517",
                "币安币的价值支撑主要来自全球最大加密交易所的手续费折扣、销毁机制和BNB Chain生态。潜力与交易所监管风险、交易量周期高度相关，天花板受限于中心化交易所模式本身的监管不确定性。"),
    "XRP-USD": ("跨境支付", "#185FA5",
                "瑞波定位跨境支付清算网络，潜力取决于传统金融机构的实际采用率。长期看点在于监管明朗后能否切入传统清算体系的市场份额，但目前实际企业采用规模仍有限。"),
    "DOGE-USD":("Meme币 / 社区驱动", "#D85A30",
                "狗狗币缺乏实质技术护城河，价格主要由社区热度、名人效应和市场投机情绪驱动，没有现金流或基本面支撑，长期赛道潜力评级最低，更接近投机品而非资产配置标的。"),
    "GC=F": ("避险资产 / 抗通胀", "#F5A623", "黄金的长期需求锚定在央行购金、地缘政治避险和抗通胀属性上。潜力相对稳定但增长空间有限，更适合作为组合的\"压舱石\"而非成长型配置，长期收益通常跑输股票类资产。"),
    "GLD":  ("避险资产 / 抗通胀", "#F5A623", "黄金ETF跟踪金价，逻辑同黄金期货：央行购金、地缘避险和抗通胀是长期支撑，适合作为组合的防御性配置而非成长型标的。"),
    "SI=F": ("工业+贵金属双属性", "#999999", "白银兼具贵金属避险属性和光伏/电子工业需求，近年受益于新能源（光伏银浆）需求增长，波动性高于黄金，价格弹性更大但风险也更高。"),
    "SLV":  ("工业+贵金属双属性", "#999999", "白银ETF跟踪银价，兼具避险和工业（光伏、电子）双重需求驱动，波动性高于黄金类资产。"),
    "HG=F": ("电气化 / 新能源基建金属", "#D85A30", "铜被称为\"新能源金属之王\"，核心逻辑是电动车、电网升级和数据中心建设带来的结构性需求增长，叠加全球矿山资本开支不足导致的供给约束，长期潜力被广泛看好，但短期高度受宏观周期（尤其中国需求）影响。"),
    "GDX":  ("黄金矿业股（金价的杠杆敞口）", "#F5A623", "金矿股相对金价通常有杠杆效应（金价上涨时涨幅更大，下跌时跌幅也更大），额外叠加了矿山运营成本、产量和管理层资本配置能力等公司层面风险。"),
    "FCX":  ("铜矿开采（新能源金属敞口）", "#D85A30", "自由港是全球最大的上市铜生产商之一，业绩与铜价高度挂钩，长期受益于电气化和新能源基建需求，但需关注矿山所在地（印尼等）的政治/税收风险。"),
    "NEM":  ("黄金开采", "#F5A623", "全球最大黄金生产商之一，是获取金价敞口同时博取运营杠杆的方式，长期表现取决于金价走势和自身成本控制/矿山寿命。"),
    "SCCO": ("铜矿开采（新能源金属敞口）", "#D85A30", "南方铜业是全球成本最低的铜生产商之一，长期受益于电气化需求增长和高股息率，但同样面临大宗商品价格周期性波动风险。"),
}
SECTOR_TRACK_MAP = {
    "Technology":          ("科技 / AI基础设施", "AI算力、云计算和软件平台的长期增长驱动力强，但估值普遍较高，需警惕AI资本开支周期见顶的风险。"),
    "Financial Services":  ("金融服务", "受益于净息差和资本市场活跃度，长期增长相对稳健但弹性有限，衰退期需警惕信贷质量恶化。"),
    "Consumer Cyclical":   ("可选消费", "增长与居民收入和信心高度相关，潜力取决于消费升级/降级周期，波动性较大。"),
    "Healthcare":          ("医疗健康", "人口老龄化提供长期结构性需求，创新药和器械是主要增长点，防御属性强，适合长期配置。"),
    "Energy":              ("能源", "传统能源受地缘政治和OPEC+产量政策影响大，长期面临能源转型压力，但短期现金流和分红能力强。"),
    "Real Estate":         ("房地产 / REITs", "对利率极度敏感，长期潜力取决于城镇化和资产证券化程度，高利率环境下承压明显。"),
    "Communication Services":("传媒 / 互联网", "广告和订阅收入受经济周期影响，长期看点在于内容/流量变现效率和AI应用落地。"),
    "Industrials":         ("工业 / 制造", "受益于基建投资和供应链本土化趋势，长期增长稳健但对全球贸易环境敏感。"),
    "Consumer Defensive":  ("必需消费", "需求刚性强，防御属性突出，长期增长天花板较低但现金流稳定，适合稳健配置。"),
    "Utilities":           ("公用事业", "现金流极其稳定，但成长性有限，主要作为高股息防御性资产配置。"),
    "Basic Materials":     ("原材料 / 大宗商品", "受益于全球工业化和新能源转型带来的结构性需求，周期性强，供给端约束是核心逻辑。"),
}

def get_track_info(ticker, sector=None):
    """返回 (赛道名称, 主题色, 潜力叙述)，优先按代码匹配，其次按行业匹配"""
    if ticker in TRACK_POTENTIAL:
        return TRACK_POTENTIAL[ticker]
    if sector in SECTOR_TRACK_MAP:
        name, desc = SECTOR_TRACK_MAP[sector]
        return (name, "#534AB7", desc)
    return ("综合板块", "#666666", "暂无该行业的专项赛道分析，建议结合公司基本面和所处行业竞争格局自行评估长期成长空间。")

# 多币种支持（成本价可用非美元货币录入，自动换算为美元用于盈亏计算）
CURRENCY_LIST = [
    "USD 🇺🇸", "EUR 🇪🇺", "GBP 🇬🇧", "CNY 🇨🇳",
    "JPY 🇯🇵", "HKD 🇭🇰", "SGD 🇸🇬", "KRW 🇰🇷",
    "AUD 🇦🇺", "CAD 🇨🇦", "CHF 🇨🇭", "INR 🇮🇳",
    "MXN 🇲🇽", "BRL 🇧🇷", "SEK 🇸🇪", "NOK 🇳🇴",
]
CURRENCY_SYMBOLS = {
    "USD":"$","EUR":"€","GBP":"£","CNY":"¥","JPY":"¥",
    "HKD":"HK$","SGD":"S$","KRW":"₩","AUD":"A$",
    "CAD":"C$","CHF":"Fr","INR":"₹","MXN":"MX$",
    "BRL":"R$","SEK":"kr","NOK":"kr",
}

@st.cache_data(ttl=3600)
def get_fx_rate(currency_code: str) -> float:
    """返回 1单位该货币 = 多少美元"""
    if currency_code == "USD":
        return 1.0
    try:
        import yfinance as yf
        ticker_map = {
            "EUR":"EURUSD=X","GBP":"GBPUSD=X","CNY":"CNY=X",
            "JPY":"JPY=X","HKD":"HKD=X","SGD":"SGD=X",
            "KRW":"KRW=X","AUD":"AUDUSD=X","CAD":"CAD=X",
            "CHF":"CHF=X","INR":"INR=X","MXN":"MXN=X",
            "BRL":"BRL=X","SEK":"SEK=X","NOK":"NOK=X",
        }
        sym = ticker_map.get(currency_code)
        if not sym:
            return 1.0
        hist = yf.Ticker(sym).history(period="2d")
        if hist.empty:
            return 1.0
        rate = float(hist["Close"].iloc[-1])
        # EUR/GBP/AUD 是"1单位=X美元"的直接报价，其余是"1美元=X单位"的间接报价需取倒数
        direct = ["EUR", "GBP", "AUD"]
        return rate if currency_code in direct else 1.0 / rate
    except Exception:
        fallback = {
            "EUR":1.08,"GBP":1.27,"CNY":0.138,"JPY":0.0067,
            "HKD":0.128,"SGD":0.74,"KRW":0.00072,"AUD":0.65,
            "CAD":0.73,"CHF":1.10,"INR":0.012,"MXN":0.052,
            "BRL":0.18,"SEK":0.093,"NOK":0.092,
        }
        return fallback.get(currency_code, 1.0)

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

@st.cache_data(ttl=60)
def fetch_market_data():
    try:
        import yfinance as yf, math
        results = {}
        for ticker, name in MARKET_TICKERS.items():
            try:
                t    = yf.Ticker(ticker)
                hist = t.history(period="5d")
                hist = hist.dropna(subset=["Close"])
                if len(hist) >= 2:
                    price = float(hist["Close"].iloc[-1])
                    prev  = float(hist["Close"].iloc[-2])
                    if math.isnan(price) or math.isnan(prev) or prev == 0:
                        continue
                    change_pct = (price - prev) / prev * 100
                    if math.isnan(change_pct) or math.isinf(change_pct):
                        change_pct = 0.0
                    results[ticker] = {
                        "name":       name,
                        "price":      round(price, 2),
                        "change":     round(price - prev, 2),
                        "change_pct": round(change_pct, 2),
                    }
            except Exception:
                pass
        return results
    except ImportError:
        return {}

def market_to_sentiment(data):
    if not data:
        return 65
    import math
    score = 50.0
    try:
        def safe_val(v, default=0.0):
            try:
                f = float(v)
                return default if (math.isnan(f) or math.isinf(f)) else f
            except Exception:
                return default

        if "^VIX" in data:
            vix = safe_val(data["^VIX"]["price"], 20)
            if vix < 15:   score += 20
            elif vix < 20: score += 10
            elif vix < 30: score -= 10
            else:          score -= 25
        if "^IXIC" in data:
            score += safe_val(data["^IXIC"]["change_pct"]) * 3
        if "NVDA" in data:
            score += safe_val(data["NVDA"]["change_pct"]) * 2
        if math.isnan(score) or math.isinf(score):
            score = 50.0
    except Exception:
        score = 50.0
    return max(0, min(100, int(score)))

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
# 静态备用数据（yfinance未同步的新上市股票）
STATIC_STOCK_DATA = {
    "SPCX": {
        "ticker": "SPCX", "name": "Space Exploration Technologies Corp",
        "sector": "Industrials", "price_now": 206.19, "price_target": 227.0,
        "price_target_pct": 10.1, "price_52w_high": 225.64, "price_52w_low": 135.0,
        "price_from_high": -8.7, "rsi": 62.0, "macd_hist": 0.85,
        "ma20": 185.0, "ma50": 170.0, "ma200": 170.0,
        "bb_up": 220.0, "bb_low": 150.0, "vol_ratio": 2.1,
        "mom_1m": 52.7, "mom_3m": 52.7, "pe": None, "fwd_pe": None,
        "pb": None, "beta": 1.5, "mktcap": 2730000000000,
        "target_analyst": 196.0, "score": 68, "rating": "买入",
        "rating_color": "#1D9E75", "rating_emoji": "📈",
        "signals": [
            ("✅","上市首周强势",f"上市价$135，当前$206.19，涨幅+52.7%，资金持续流入"),
            ("✅","MA多头排列",f"价格$206.19站于MA20($185.00)和MA50($170.00)之上"),
            ("🟡","RSI偏高",f"RSI=62.0，接近超买区间，短期注意回调风险"),
            ("✅","成交量放大",f"成交量是均值的2.1倍，机构资金积极参与"),
            ("🔴","估值极高",f"P/S倍数约145x，需要极高增长预期支撑"),
            ("⚪","新上市股票",f"上市仅4天，历史数据有限，技术分析仅供参考"),
        ],
        "hist": None, "static": True,
        "atr": 8.5, "atr_pct": 4.1, "stop_loss": 193.4, "stop_loss_pct": -6.2,
        "obv_trend": "上升", "obv_pct": 45.0,
        "fib_levels": {"0.236":176.3,"0.382":163.6,"0.500":153.8,"0.618":144.0,"0.786":130.5},
        "nearest_support": 176.3, "nearest_resistance": 225.64,
        "slope_pct": 2.1, "sharpe": 1.2,
        "lt_score": 62, "lt_rating": "适合长期投资", "lt_color": "#1D9E75",
    }
}

@st.cache_data(ttl=120)
def fetch_stock_analysis(ticker: str):
    # 检查是否有静态备用数据
    if ticker.upper() in STATIC_STOCK_DATA:
        return STATIC_STOCK_DATA[ticker.upper()]

    try:
        import yfinance as yf
        t    = yf.Ticker(ticker)
        # 尝试1年数据，不足则用6个月
        hist = t.history(period="1y")
        if hist.empty or len(hist) < 10:
            hist = t.history(period="6mo")
        if hist.empty or len(hist) < 10:
            return None
        # 清理 NaN
        hist = hist.dropna(subset=["Close","Open","High","Low","Volume"])
        if len(hist) < 10:
            return None

        close  = hist["Close"].dropna()
        volume = hist["Volume"].fillna(0)

        def safe_float(val, default=0.0):
            """Convert to float, return default if NaN/None/inf"""
            import math
            try:
                v = float(val)
                return default if (math.isnan(v) or math.isinf(v)) else v
            except Exception:
                return default

        # ── 技术指标计算 ──
        # RSI (14)
        delta  = close.diff()
        gain   = delta.clip(lower=0).rolling(14).mean()
        loss   = (-delta.clip(upper=0)).rolling(14).mean()
        rs     = gain / loss.replace(0, 1e-9)
        rsi    = safe_float((100 - 100 / (1 + rs)).iloc[-1], 50.0)

        # MACD
        ema12  = close.ewm(span=12).mean()
        ema26  = close.ewm(span=26).mean()
        macd   = ema12 - ema26
        signal = macd.ewm(span=9).mean()
        macd_val    = safe_float(macd.iloc[-1])
        signal_val  = safe_float(signal.iloc[-1])
        macd_hist   = macd_val - signal_val

        # 价格位置（必须最先计算，其他指标依赖 price_now）
        price_now = safe_float(close.iloc[-1])
        if price_now == 0: return None
        price_52w_high = safe_float(close.rolling(min(252, len(close))).max().iloc[-1], price_now)
        price_52w_low  = safe_float(close.rolling(min(252, len(close))).min().iloc[-1], price_now)
        price_from_high = (price_now - price_52w_high) / price_52w_high * 100
        price_from_low  = (price_now - price_52w_low)  / price_52w_low  * 100

        # 均线
        ma20  = safe_float(close.rolling(20).mean().iloc[-1], price_now)
        ma50  = safe_float(close.rolling(min(50,len(close))).mean().iloc[-1], ma20)
        ma200 = safe_float(close.rolling(min(200,len(close))).mean().iloc[-1], ma20)

        # 布林带
        bb_mid = safe_float(close.rolling(min(20,len(close))).mean().iloc[-1], price_now)
        bb_std = safe_float(close.rolling(min(20,len(close))).std().iloc[-1], price_now*0.02)
        bb_up  = bb_mid + 2 * bb_std
        bb_low = bb_mid - 2 * bb_std

        # 成交量趋势
        vol_avg = safe_float(volume.rolling(min(20,len(volume))).mean().iloc[-1], 1.0)
        vol_now = safe_float(volume.iloc[-1], vol_avg)
        vol_ratio = vol_now / vol_avg if vol_avg > 0 else 1.0

        # 动量
        mom_1m  = safe_float((close.iloc[-1] / close.iloc[max(0,len(close)-22)] - 1) * 100)
        mom_3m  = safe_float((close.iloc[-1] / close.iloc[max(0,len(close)-66)] - 1) * 100)

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

        # ── 新增指标 ──────────────────────────────────────────────────
        # ATR (14) — 平均真实波幅，用于止损计算
        high_low   = hist["High"] - hist["Low"]
        high_close = (hist["High"] - hist["Close"].shift()).abs()
        low_close  = (hist["Low"]  - hist["Close"].shift()).abs()
        true_range = high_low.combine(high_close, max).combine(low_close, max)
        atr        = safe_float(true_range.rolling(min(14,len(true_range))).mean().iloc[-1], price_now*0.02)
        atr_pct    = atr / price_now * 100

        # 止损建议（1.5x ATR below current price）
        stop_loss       = price_now - 1.5 * atr
        stop_loss_pct   = (stop_loss - price_now) / price_now * 100

        # OBV — 能量潮（On-Balance Volume）
        obv = []
        for i in range(len(close)):
            if i == 0:
                obv.append(float(volume.iloc[i]))
            else:
                if close.iloc[i] > close.iloc[i-1]:
                    obv.append(obv[-1] + float(volume.iloc[i]))
                elif close.iloc[i] < close.iloc[i-1]:
                    obv.append(obv[-1] - float(volume.iloc[i]))
                else:
                    obv.append(obv[-1])
        import pandas as pd
        obv_series    = pd.Series(obv, index=close.index)
        obv_ma20      = safe_float(obv_series.rolling(min(20,len(obv_series))).mean().iloc[-1])
        obv_now       = safe_float(obv_series.iloc[-1])
        obv_trend     = "上升" if obv_now > obv_ma20 else "下降"
        obv_pct       = (obv_now - obv_ma20) / abs(obv_ma20) * 100 if obv_ma20 != 0 else 0

        # 斐波那契回撤位
        fib_high = price_52w_high
        fib_low  = price_52w_low
        fib_range = fib_high - fib_low
        fib_levels = {
            "0.236": round(fib_high - 0.236 * fib_range, 2),
            "0.382": round(fib_high - 0.382 * fib_range, 2),
            "0.500": round(fib_high - 0.500 * fib_range, 2),
            "0.618": round(fib_high - 0.618 * fib_range, 2),
            "0.786": round(fib_high - 0.786 * fib_range, 2),
        }
        # 找最近的支撑和阻力
        nearest_support    = max([v for v in fib_levels.values() if v <= price_now], default=fib_low)
        nearest_resistance = min([v for v in fib_levels.values() if v >= price_now], default=fib_high)

        # 线性回归斜率（20日）
        import numpy as np_inner
        x_lr  = np_inner.arange(20)
        y_lr  = close.iloc[-20:].values if len(close) >= 20 else close.values
        if len(y_lr) >= 2:
            slope_norm = float(np_inner.polyfit(np_inner.arange(len(y_lr)), y_lr, 1)[0])
            slope_pct  = slope_norm / price_now * 100  # 每日涨跌%
        else:
            slope_norm = 0.0
            slope_pct  = 0.0

        # 夏普比率（年化，使用6个月日收益率）
        daily_returns = close.pct_change().dropna()
        if len(daily_returns) > 5:
            sharpe = float((daily_returns.mean() / daily_returns.std()) * (252 ** 0.5))
        else:
            sharpe = 0.0

        # 长期投资综合评分（0-100，独立于短线评分）
        lt_score = 50
        # 趋势稳定性：线性回归斜率正负
        if slope_pct > 0.1:   lt_score += 10
        elif slope_pct < -0.1: lt_score -= 10
        # OBV趋势：资金长期流向
        if obv_trend == "上升": lt_score += 10
        else:                   lt_score -= 10
        # 夏普比率：风险调整后收益
        if sharpe > 1.5:   lt_score += 15
        elif sharpe > 0.5: lt_score += 8
        elif sharpe < 0:   lt_score -= 15
        elif sharpe < 0.5: lt_score -= 5
        # 价格与MA200关系（若有）
        if price_now > ma200: lt_score += 10
        else:                 lt_score -= 10
        # P/E基本面
        if pe and pe > 0:
            if pe < 20:   lt_score += 10
            elif pe > 60: lt_score -= 10
        # Beta波动性
        if beta:
            if beta < 1.2: lt_score += 5
            elif beta > 2:  lt_score -= 5
        lt_score = max(0, min(100, lt_score))

        # 长期投资评级
        if lt_score >= 75:
            lt_rating = "强烈推荐长期持有"; lt_color = "#0F6E56"
        elif lt_score >= 60:
            lt_rating = "适合长期投资";     lt_color = "#1D9E75"
        elif lt_score >= 45:
            lt_rating = "中性，谨慎长持";   lt_color = "#BA7517"
        elif lt_score >= 30:
            lt_rating = "不建议长期持有";   lt_color = "#D85A30"
        else:
            lt_rating = "规避，高风险资产"; lt_color = "#A32D2D"

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

        # OBV 信号 (±8分)
        if obv_trend == "上升" and obv_pct > 5:
            score += 8
            signals.append(("✅", "OBV资金流入", f"能量潮高于均线{obv_pct:.1f}%，机构资金持续买入"))
        elif obv_trend == "下降" and obv_pct < -5:
            score -= 8
            signals.append(("🔴", "OBV资金流出", f"能量潮低于均线{abs(obv_pct):.1f}%，资金持续流出"))
        else:
            signals.append(("⚪", "OBV中性", f"资金流向尚不明确，趋势待确认"))

        # 线性回归斜率信号 (±6分)
        if slope_pct > 0.15:
            score += 6
            signals.append(("✅", "上升趋势", f"20日线性回归斜率 +{slope_pct:.2f}%/日，价格趋势向上"))
        elif slope_pct < -0.15:
            score -= 6
            signals.append(("🔴", "下降趋势", f"20日线性回归斜率 {slope_pct:.2f}%/日，价格趋势向下"))
        else:
            signals.append(("⚪", "趋势平坦", f"20日线性回归斜率接近0（{slope_pct:.2f}%/日），横盘整理中"))

        # 斐波那契位置信号 (±5分)
        fib_position = (price_now - fib_low) / fib_range * 100 if fib_range > 0 else 50
        if abs(price_now - nearest_support) / price_now < 0.02:
            score += 5
            signals.append(("✅", "斐波那契支撑", f"价格${price_now:.2f}接近支撑位${nearest_support:.2f}（Fib回撤）"))
        elif abs(price_now - nearest_resistance) / price_now < 0.02:
            score -= 5
            signals.append(("🔴", "斐波那契阻力", f"价格${price_now:.2f}接近阻力位${nearest_resistance:.2f}（Fib回撤）"))
        else:
            signals.append(("⚪", "斐波那契中性", f"支撑${nearest_support:.2f} → 当前${price_now:.2f} → 阻力${nearest_resistance:.2f}"))

        # 夏普比率信号 (±5分)
        if sharpe > 1.5:
            score += 5
            signals.append(("✅", "夏普比率优秀", f"夏普={sharpe:.2f}，风险调整后收益极佳"))
        elif sharpe > 0.5:
            score += 2
            signals.append(("🟡", "夏普比率良好", f"夏普={sharpe:.2f}，风险收益比尚可"))
        elif sharpe < 0:
            score -= 5
            signals.append(("🔴", "夏普比率为负", f"夏普={sharpe:.2f}，持有该股不如持有现金"))

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
            "atr": atr, "atr_pct": atr_pct,
            "stop_loss": stop_loss, "stop_loss_pct": stop_loss_pct,
            "obv_trend": obv_trend, "obv_pct": obv_pct,
            "fib_levels": fib_levels,
            "nearest_support": nearest_support,
            "nearest_resistance": nearest_resistance,
            "slope_pct": slope_pct,
            "sharpe": sharpe,
            "lt_score": lt_score,
            "lt_rating": lt_rating,
            "lt_color": lt_color,
        }
    except Exception as e:
        return {"error": str(e)}

# ── 标题 ──────────────────────────────────────────────────────────────────────
st.title("📈 2026 大型IPO与泡沫风险模拟器")
st.caption("数据基于2026年Q1公开市场信息 · 仅供研究参考，不构成投资建议")

tabs = st.tabs(["🏠 市场概览","🔍 IPO详情","📜 历史对比","📈 趋势预测 + 泡沫模拟","🌐 宏观分析","🔬 股票分析器","💰 我的持仓","🏆 投资圣杯"])

# ── Tab 1: 市场概览 + 实时市场 ──────────────────────────────────────────────────
with tabs[0]:
    st.subheader("📊 市场实时动态")

    live_data_t1 = fetch_market_data()
    if live_data_t1:
        _w_on, _w_iv, _w_left = watch_status()
        _wc1, _wc2, _wc3 = st.columns([1.1, 1.3, 3.6])
        if _wc1.button("🔄 刷新实时数据", key="refresh_t1", use_container_width=True):
            st.cache_data.clear(); st.rerun()
        if _w_on:
            if _wc2.button("⏹ 结束盯盘", key="watch_stop_t1", use_container_width=True):
                stop_watch(); st.rerun()
            _wc3.markdown(
                f'<div class="arow" style="margin-top:2px;background:rgba(29,158,117,.14);'
                f'border:1px solid rgba(29,158,117,.35)">'
                f'<span style="font-size:13px;color:#0F6E56;font-weight:600">'
                f'🟢 盯盘中 · 每 {_w_iv} 秒自动刷新 · 剩余 {_w_left//60:02d}:{_w_left%60:02d} · '
                f'已刷新 {st.session_state.get("watch_count", 0)} 次</span></div>',
                unsafe_allow_html=True)
        else:
            if _wc2.button("👀 开始盯盘", key="watch_start_t1", use_container_width=True, type="primary"):
                start_watch(); st.rerun()
            _wc3.markdown(
                f'<div class="arow" style="margin-top:2px">'
                f'<span style="font-size:12.5px;color:#64748b">'
                f'⚪ 手动模式：数据只在你操作时更新。点「开始盯盘」后会每 '
                f'{st.session_state.get("watch_iv", 60)} 秒自动刷新一次，'
                f'{st.session_state.get("watch_min", 15)} 分钟后自动停止（可在左侧边栏调整）。</span></div>',
                unsafe_allow_html=True)

        cards_t1 = []
        for ticker, info in live_data_t1.items():
            if ticker == "^TNX":
                val = f"{info['price']:.2f}%"
            elif ticker.startswith("^"):
                val = f"{info['price']:,.2f}"
            else:
                val = f"${info['price']:,.2f}"
            sub = {"^IXIC": "NASDAQ 综合指数", "^GSPC": "S&P 500 指数",
                   "^VIX": "CBOE 波动率指数", "^TNX": "US 10Y Treasury"}.get(ticker, ticker)
            cards_t1.append((ticker, asset_card_html(
                ticker, info["name"], sub, val, info["change_pct"],
                invert_color=(ticker == "^VIX"),
            )))
        render_asset_grid_clickable(cards_t1, key_prefix="t1card", cols=4)

        # ── 点击任意标的后就地展开分析与走势 ──
        _qv = st.session_state.get("quick_view_ticker")
        if _qv:
            st.divider()
            _qc1, _qc2 = st.columns([5, 1])
            _qc1.markdown(f"#### 🔎 {_qv} 快速分析")
            if _qc2.button("✕ 关闭", key="qv_close", use_container_width=True):
                st.session_state["quick_view_ticker"] = None
                st.rerun()
            with st.spinner(f"正在分析 {_qv}..."):
                render_quick_analysis(_qv)
            st.divider()

        with st.expander("📖 每个指标怎么读？（点开看每个数字为什么是这样）", expanded=True):
            for ticker, info in live_data_t1.items():
                txt, tone = interpret_market(ticker, info)
                why(txt, tone, title=f"{info['name']}")

        st.subheader("今日涨跌幅")
        tl_t1 = [v["name"] for v in live_data_t1.values()]
        ch_t1 = [v["change_pct"] for v in live_data_t1.values()]
        fig_live_t1 = go.Figure(go.Bar(
            x=tl_t1, y=ch_t1,
            marker_color=["#A32D2D" if c < 0 else "#0F6E56" for c in ch_t1],
            text=[f"{c:+.2f}%" for c in ch_t1], textposition="outside",
        ))
        fig_live_t1.update_layout(
            height=300, yaxis_title="涨跌幅 (%)", plot_bgcolor="#fafafa",
            showlegend=False, margin=dict(t=20, b=20),
            yaxis=dict(zeroline=True, zerolinecolor="#cccccc"),
        )
        glass_chart(fig_live_t1, use_container_width=True)

        sentiment_t1 = market_to_sentiment(live_data_t1)
        label_t1 = ("极度恐慌" if sentiment_t1 < 20 else "恐慌" if sentiment_t1 < 40
                    else "中性" if sentiment_t1 < 60 else "乐观" if sentiment_t1 < 80 else "极度狂热")
        st.subheader(f"当前市场情绪：{label_t1}（{sentiment_t1}/100）")
        st.progress(sentiment_t1 / 100)
        _s_txt, _s_tone, _s_calc = explain_sentiment(live_data_t1, sentiment_t1)
        why(_s_txt, _s_tone, calc=_s_calc, title="这个分数怎么来的")
    else:
        st.warning("无法获取实时数据，请检查网络连接。")

    st.divider()
    st.subheader("💎 加密货币 & 有色金属/矿业")

    @st.cache_data(ttl=60)
    def fetch_crypto_metals_data(tickers_dict):
        try:
            import yfinance as yf, math
            results = {}
            for ticker, name in tickers_dict.items():
                try:
                    t    = yf.Ticker(ticker)
                    hist = t.history(period="5d")
                    hist = hist.dropna(subset=["Close"])
                    if len(hist) >= 2:
                        price = float(hist["Close"].iloc[-1])
                        prev  = float(hist["Close"].iloc[-2])
                        if math.isnan(price) or math.isnan(prev) or prev == 0:
                            continue
                        change_pct = (price - prev) / prev * 100
                        if math.isnan(change_pct) or math.isinf(change_pct):
                            change_pct = 0.0
                        results[ticker] = {
                            "name": name, "price": round(price, 2),
                            "change_pct": round(change_pct, 2),
                        }
                except Exception:
                    pass
            return results
        except ImportError:
            return {}

    cm_tab1, cm_tab2 = st.tabs(["🪙 加密货币", "⛏️ 有色金属/矿业"])
    with cm_tab1:
        crypto_data = fetch_crypto_metals_data(CRYPTO_TICKERS)
        if crypto_data:
            render_asset_grid_clickable([
                (tk, asset_card_html(tk, info["name"], tk.replace("-USD", " / USD"),
                                     f"${info['price']:,.2f}", info["change_pct"],
                                     note=get_track_info(tk)[0]))
                for tk, info in crypto_data.items()
            ], key_prefix="cryptocard", cols=3)
            fig_crypto = go.Figure(go.Bar(
                x=[v["name"] for v in crypto_data.values()],
                y=[v["change_pct"] for v in crypto_data.values()],
                marker_color=["#A32D2D" if v["change_pct"] < 0 else "#0F6E56" for v in crypto_data.values()],
                text=[f"{v['change_pct']:+.2f}%" for v in crypto_data.values()], textposition="outside",
            ))
            fig_crypto.update_layout(height=280, yaxis_title="24h涨跌幅 (%)", plot_bgcolor="#fafafa",
                                     showlegend=False, margin=dict(t=20, b=20),
                                     yaxis=dict(zeroline=True, zerolinecolor="#cccccc"))
            glass_chart(fig_crypto, use_container_width=True)
            avg_chg = sum(v["change_pct"] for v in crypto_data.values()) / len(crypto_data)
            crypto_mood = ("🔥 普遍上涨，风险偏好回升" if avg_chg > 2 else
                           "📉 普遍下跌，避险情绪升温" if avg_chg < -2 else "⚖️ 涨跌互现，方向不明")
            why(f"加密市场整体 **{crypto_mood}**，平均涨跌 {avg_chg:+.2f}%。加密资产没有现金流估值锚，"
                f"价格几乎完全由流动性和风险偏好驱动，所以它常常是市场情绪的**放大版**——"
                f"美联储宽松时涨得比纳斯达克更凶，收紧时也跌得更深。",
                "good" if avg_chg > 0 else "bad", title="整体怎么看")
            with st.expander("📖 每个币怎么读？", expanded=False):
                for tk, info in crypto_data.items():
                    txt, tone = interpret_crypto(tk, info)
                    why(txt, tone, title=info["name"])
            st.caption("可在「🔬 股票分析器」或「💰 我的持仓」输入 BTC-USD / ETH-USD 等代码查看详细技术面分析")
        else:
            st.warning("无法获取加密货币实时数据。")

    with cm_tab2:
        metals_data = fetch_crypto_metals_data(METALS_TICKERS)
        if metals_data:
            render_asset_grid_clickable([
                (tk, asset_card_html(tk, info["name"],
                                     "期货合约" if "=" in tk else tk,
                                     f"${info['price']:,.2f}", info["change_pct"],
                                     note=get_track_info(tk)[0]))
                for tk, info in metals_data.items()
            ], key_prefix="metalcard", cols=3)
            fig_metals = go.Figure(go.Bar(
                x=[v["name"] for v in metals_data.values()],
                y=[v["change_pct"] for v in metals_data.values()],
                marker_color=["#A32D2D" if v["change_pct"] < 0 else "#0F6E56" for v in metals_data.values()],
                text=[f"{v['change_pct']:+.2f}%" for v in metals_data.values()], textposition="outside",
            ))
            fig_metals.update_layout(height=280, yaxis_title="今日涨跌幅 (%)", plot_bgcolor="#fafafa",
                                     showlegend=False, margin=dict(t=20, b=20),
                                     yaxis=dict(zeroline=True, zerolinecolor="#cccccc"))
            glass_chart(fig_metals, use_container_width=True)
            _m_avg = sum(v["change_pct"] for v in metals_data.values()) / len(metals_data)
            why(f"板块平均 {_m_avg:+.2f}%。有色金属有两条独立的定价逻辑："
                f"**贵金属（金/银）看实际利率和避险需求**——实际利率下行或地缘冲突升温时走强；"
                f"**工业金属（铜）看全球经济需求**——电动车、电网升级和数据中心建设是长期需求来源。"
                f"所以金涨铜跌通常意味着市场在担心衰退，金铜齐涨则多半是通胀预期在升温。",
                "good" if _m_avg > 0 else "neutral", title="整体怎么看")
            with st.expander("📖 每个品种怎么读？", expanded=False):
                for tk, info in metals_data.items():
                    txt, tone = interpret_metal(tk, info)
                    why(txt, tone, title=info["name"])
        else:
            st.warning("无法获取有色金属数据。")

    st.divider()
    st.subheader("📈 2026 IPO市场总览")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("预期总市值", "$3.12T", "12大待上市公司")
    c2.metric("Q1 2026 融资额", "$42.6B", "同比 +45%")
    c3.metric("AI占风投比例", "80%", "泡沫风险高", delta_color="inverse")
    c4.metric("泡沫综合指数", "74/100", "⚠ 高度警戒", delta_color="inverse")

    _ipo_why = [
        ("预期总市值 $3.12T",
         "把2026年12家待上市公司的最新一轮估值加总得到。$3.12万亿这个体量本身就是信号——"
         "相当于一次性要市场消化掉一个「英伟达级别」的市值，而这些公司绝大多数还没有稳定盈利。", "warn"),
        ("Q1融资额 $42.6B 同比+45%",
         "一级市场融资额同比大增45%，说明资金正在加速涌入Pre-IPO阶段。融资越容易，公司上市时的"
         "估值起点就越高，留给二级市场投资者的安全边际也就越薄。", "warn"),
        ("AI占风投比例 80%",
         "每100元风险投资里有80元投向AI。这个集中度在历史上只有2000年的互联网和2021年的SPAC可比——"
         "**赛道越拥挤，一旦叙事证伪，资金同时撤离造成的踩踏就越严重**。", "bad"),
        ("泡沫综合指数 74/100",
         "由估值倍数（P/S）、盈利覆盖率、资金集中度和锁定期抛压四项加权得到。74分落在「高度警戒」区间"
         "（70以上），意味着当前定价已经把很多乐观假设提前兑现了。", "bad"),
    ]
    with st.expander("📖 这四个数字分别说明什么？", expanded=False):
        for t, d, tone in _ipo_why:
            why(d, tone, title=t)

    st.subheader("市场集中度风险")
    _conc_why = {
        "AI估值集中": "衡量市值有多少集中在少数AI标的上。88%意味着整个板块的涨跌几乎由几家公司决定，分散投资在这里失效了。",
        "流动性压力": "衡量市场有没有足够的资金接住这些新股。79%说明在高利率环境下，能承接$3万亿新增供给的增量资金并不充裕。",
        "盈利能力缺口": "待上市公司中亏损企业的占比与亏损幅度。72%说明大部分标的的估值靠的是远期预期，而不是当期利润。",
        "锁定期后抛压": "IPO后约180天锁定期到期时，早期投资者和员工可抛售的股份占比。65%属于偏高水平，通常对应解禁后的一波明显回调。",
        "市场吸收能力": "市场实际能消化多少新增供给。42%是唯一的低分项——**分数越低越危险**，说明供给远超需求承接力。",
    }
    for label, val in {"AI估值集中":88,"流动性压力":79,"盈利能力缺口":72,"锁定期后抛压":65,"市场吸收能力":42}.items():
        st.progress(val/100, text=f"{label}：**{val}%**")
        why(_conc_why[label], "bad" if val >= 70 or label == "市场吸收能力" else "warn", title=label)

# ── Tab 2: IPO详情（含估值总览） ────────────────────────────────────────────────
with tabs[1]:

    # 自动抓取已上市IPO的实时价格
    @st.cache_data(ttl=120)
    def fetch_ipo_live_prices():
        """抓取已上市IPO的实时股价"""
        try:
            import yfinance as yf, math
            live = {}
            # SpaceX上市代码候选（上市初期代码可能不稳定）
            spacex_candidates = ["SPCX","SPACX","SX"]  # SPCE=Virgin Galactic 不是SpaceX
            found = False
            for ticker in spacex_candidates:
                try:
                    t    = yf.Ticker(ticker)
                    hist = t.history(period="5d")
                    hist = hist.dropna(subset=["Close"])
                    if len(hist) >= 1:
                        price = float(hist["Close"].iloc[-1])
                        prev  = float(hist["Close"].iloc[-2]) if len(hist)>1 else price
                        if math.isnan(price) or price <= 1.0:
                            continue
                        chg = (price-prev)/prev*100 if prev>0 else 0
                        live[ticker] = {
                            "name":       "SpaceX",
                            "price":      round(price,2),
                            "change_pct": round(chg,2),
                            "ipo_price":  135.0,
                            "from_ipo":   round((price-135.0)/135.0*100,1),
                        }
                        found = True
                        break
                except Exception:
                    continue
            # 如果yfinance还未同步SPCX，使用静态备用数据
            if not found:
                live["SPCX"] = {
                    "name":       "SpaceX",
                    "price":      206.19,
                    "change_pct": 7.12,
                    "ipo_price":  135.0,
                    "from_ipo":   round((206.19-135.0)/135.0*100,1),
                    "static":     True,
                }
            return live
        except Exception:
            return {}

    live_ipo = fetch_ipo_live_prices()

    # 已上市公司实时价格横幅
    if live_ipo:
        st.subheader("📡 已上市IPO实时行情")
        for ticker, d in live_ipo.items():
            clr = "#0F6E56" if d["change_pct"] >= 0 else "#A32D2D"
            from_ipo_clr = "#0F6E56" if d["from_ipo"] >= 0 else "#A32D2D"
            st.markdown(
                f'<div class="ahero" style="background:linear-gradient(120deg,#1a1a2e 0%,#16213e 60%,#243b6b 100%)">'
                f'{logo_watermark_html("^IXIC", hero=True)}'
                f'<div class="ahero-glass">'
                f'{logo_chip_html(ticker, cls="ahero-chip")}'
                f'<div style="flex:1">'
                f'<div style="font-size:19px;font-weight:750">{d["name"]} ({ticker})</div>'
                f'<div style="font-size:12px;opacity:.8;margin-top:2px">🚀 纳斯达克上市 · 发行价 $135.00</div>'
                f'</div>'
                f'<div style="text-align:right">'
                f'<div style="font-size:31px;font-weight:750;letter-spacing:-.5px">${d["price"]:.2f}</div>'
                f'<div style="font-size:13.5px;color:{clr};font-weight:700;'
                f'background:rgba(255,255,255,.9);border-radius:99px;padding:1px 10px;display:inline-block;margin-top:3px">'
                f'{"+"+str(round(d["change_pct"],2))+"%" if d["change_pct"]>=0 else str(round(d["change_pct"],2))+"%"} 今日</div>'
                f'<div style="font-size:11.5px;opacity:.9;margin-top:4px">'
                f'较发行价 {"+"+str(round(d["from_ipo"],1))+"%" if d["from_ipo"]>=0 else str(round(d["from_ipo"],1))+"%"}</div>'
                f'</div></div></div>',
                unsafe_allow_html=True
            )
        if st.button("🔄 刷新实时价格", key="refresh_ipo_live"):
            st.cache_data.clear(); st.rerun()

    # 估值分布图（从原市场概览移过来）
    st.subheader("核心IPO估值分布")
    names = [c["name"] for c in IPOS]
    vals  = [c["val_b"] for c in IPOS]  # SpaceX已更新为上市后实际市值$1770B
    fig_bar = go.Figure(go.Bar(
        x=names, y=vals, marker_color=COLORS,
        text=[f"${v/1000:.2f}T" if v>=1000 else f"${v}B" for v in vals],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>估值: $%{y}B<extra></extra>",
    ))
    fig_bar.update_layout(height=320, margin=dict(t=30,b=20),
                          yaxis_title="估值 ($B)", showlegend=False,
                          plot_bgcolor="#fafafa")
    glass_chart(fig_bar, use_container_width=True)

    st.divider()
    st.subheader("公司深度分析")
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

    # ── 点进公司看真实走势与技术分析（已上市的才有行情）──
    _co_ticker = company.get("ticker")
    if _co_ticker:
        if st.button(f"📈 查看 {company['name']}（{_co_ticker}）的走势图与完整技术分析",
                     key=f"ipo_analyze_{_co_ticker}", use_container_width=True, type="primary"):
            st.session_state["ipo_quick_view"] = _co_ticker
            st.session_state["selected_ticker"] = _co_ticker
            st.session_state["analysis_result"] = None
            st.rerun()
    else:
        st.info(f"🔒 {company['name']} 尚未上市（预计 {company['date']}），还没有可交易的股票代码，"
                f"因此无法显示K线走势。上市后这里会自动出现走势图入口。"
                f"你可以先在「📈 趋势预测」里用同板块的已上市标的做情景推演。")

    if st.session_state.get("ipo_quick_view"):
        _iv = st.session_state["ipo_quick_view"]
        st.divider()
        _ic1, _ic2 = st.columns([5, 1])
        _ic1.markdown(f"#### 🔎 {_iv} 走势与技术分析")
        if _ic2.button("✕ 关闭", key="ipo_qv_close", use_container_width=True):
            st.session_state["ipo_quick_view"] = None
            st.rerun()
        with st.spinner(f"正在分析 {_iv}..."):
            render_quick_analysis(_iv)
        st.divider()

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
    glass_chart(fig_bubble, use_container_width=True)

# ── Tab 3: 历史对比 ─────────────────────────────────────────────────────────────
with tabs[2]:
    st.subheader("历史泡沫周期对比")
    nodes=HISTORICAL["节点"]; fig_hist=go.Figure()
    fig_hist.add_trace(go.Scatter(x=nodes,y=HISTORICAL["2000互联网"],name="2000互联网",
        line=dict(color="#E24B4A",dash="dash",width=2),mode="lines+markers"))
    fig_hist.add_trace(go.Scatter(x=nodes,y=HISTORICAL["2021 SPAC"],name="2021 SPAC",
        line=dict(color="#BA7517",dash="dot",width=2),mode="lines+markers"))
    fig_hist.add_trace(go.Scatter(x=nodes[:4],y=[100,130,180,240],name="2026 AI IPO(预测)",
        line=dict(color="#534AB7",width=3),mode="lines+markers"))
    fig_hist.update_layout(height=420,yaxis_title="指数 (基准=100)",
                           plot_bgcolor="#fafafa",legend=dict(orientation="h",y=-0.2))
    glass_chart(fig_hist, use_container_width=True)
    col1,col2,col3=st.columns(3)
    col1.error("**2000 互联网泡沫**\n\n纳斯达克峰值5,048点，随后暴跌78%。1500+科技公司破产，市值蒸发约$5万亿。")
    col2.warning("**2021 SPAC狂热**\n\n600+ SPAC上市，多数较峰值下跌70%+。利率上升刺破泡沫，散户损失惨重。")
    col3.info("**2026 AI IPO浪潮**\n\n三巨头合计估值$3T，AI占风投80%。部分公司确有营收，但P/S倍数同样极端。")

# ── (实时市场已合并到Tab1) ──────────────────────────────────────────────────────

# ── Tab 4: 趋势预测 + 泡沫模拟 ────────────────────────────────────────────────────
with tabs[3]:

    # ══════════════════════════════════════════════════════════════════════
    # 🎛️ 泡沫模拟（已整合至趋势预测）
    # ══════════════════════════════════════════════════════════════════════
    with st.expander("🎛️ 泡沫风险模拟器", expanded=False):
        
        live_data_sim  = fetch_market_data()
        auto_sentiment = market_to_sentiment(live_data_sim)
        auto_rate = 4.5
        if live_data_sim and "^TNX" in live_data_sim:
            auto_rate = round(live_data_sim["^TNX"]["price"], 2)
        auto_retail = 70
        if live_data_sim and "^VIX" in live_data_sim:
            vix = live_data_sim["^VIX"]["price"]
            auto_retail = max(20, min(90, int(100 - vix * 2)))
        
        mode_col1, mode_col2 = st.columns([1, 2])
        with mode_col1:
            auto_mode = st.toggle("🤖 自动驾驶模式", value=False,
                                  help="开启后从实时市场数据自动计算所有参数")
        with mode_col2:
            if auto_mode:
                st.success(f"✅ 已接入实时数据 · 情绪={auto_sentiment} · 利率={auto_rate}% · 散户={auto_retail}")
                if st.button("🔄 刷新实时参数", key="refresh_sim"):
                    st.cache_data.clear()
                    st.rerun()
            else:
                st.caption("💡 手动模式：拖动滑块或选择情景预设")
        
        st.divider()
        
        if auto_mode:
            sentiment = auto_sentiment
            rate      = auto_rate
            ai_speed  = 60
            retail    = auto_retail
        
            # ── 股票/ETF选择器 ──────────────────────────────────────────────
            st.subheader("🔍 选择分析标的")
            sc_presets = {
                "大盘ETF": ["SPY","QQQ","DIA","IWM","VTI"],
                "AI科技":  ["NVDA","MSFT","GOOGL","META","AMZN","SPCX"],
                "中概股":  ["BABA","JD","PDD","BIDU","NIO"],
                "防御型":  ["JNJ","PG","KO","WMT","GLD"],
                "高风险":  ["TSLA","AMD","PLTR","ARKK","MSTR"],
            }
            sc_row1, sc_row2 = st.columns([1,3])
            with sc_row1:
                sc_group = st.selectbox("板块", list(sc_presets.keys()), key="sc_group")
            with sc_row2:
                sc_ticker_cols = st.columns(len(sc_presets[sc_group]))
                sc_picked = None
                for i, tk in enumerate(sc_presets[sc_group]):
                    is_sel = st.session_state.get("sc_ticker") == tk
                    if sc_ticker_cols[i].button(
                        tk, key=f"sc_btn_{tk}",
                        use_container_width=True,
                        type="primary" if is_sel else "secondary"
                    ):
                        st.session_state["sc_ticker"] = tk
                        sc_picked = tk
        
            custom_col, _ = st.columns([2,3])
            with custom_col:
                custom_tk = ticker_autocomplete(
                    "sc_custom_input", default=st.session_state.get("sc_ticker", "SPY"),
                    label="🔍 或搜索其它标的（边打边出提示，如 X、GO、黄金）")
                if custom_tk:
                    st.session_state["sc_ticker"] = custom_tk

            sc_ticker = st.session_state.get("sc_ticker", "SPY")
            st.markdown(
                f'<div class="arow">{logo_chip_html(sc_ticker, cls="arow-chip")}'
                f'<span style="font-size:13px;color:#0f172a">当前分析标的：<b>{sc_ticker}</b>'
                f'　<span style="font-size:11px;color:#64748b">'
                f'{TICKER_UNIVERSE.get(sc_ticker, "自定义代码")}</span></span></div>',
                unsafe_allow_html=True)
        
            # ── 抓取该股实时数据 ──────────────────────────────────────────────
            @st.cache_data(ttl=300)
            def fetch_sc_data(ticker):
                try:
                    import yfinance as yf, numpy as np_sc
                    t    = yf.Ticker(ticker)
                    hist = t.history(period="1y")
                    if hist.empty or len(hist) < 20:
                        return None
                    close = hist["Close"].dropna()
                    price = float(close.iloc[-1])
                    rets  = close.pct_change().dropna()
                    mu    = float(rets.mean() * 252)
                    sigma = float(rets.std() * (252**0.5))
                    info  = {}
                    try: info = t.info
                    except: pass
                    beta    = float(info.get("beta", 1.0) or 1.0)
                    name    = info.get("longName", ticker)
                    sector  = info.get("sector", "未知")
                    pe      = info.get("trailingPE")
                    mktcap  = info.get("marketCap")
                    prev    = float(close.iloc[-2]) if len(close)>1 else price
                    chg_pct = (price-prev)/prev*100
                    return {
                        "ticker": ticker, "name": name, "sector": sector,
                        "price": price, "chg_pct": chg_pct,
                        "mu": mu, "sigma": sigma, "beta": beta,
                        "pe": pe, "mktcap": mktcap,
                    }
                except Exception as e:
                    return {"error": str(e)}
        
            with st.spinner(f"正在获取 {sc_ticker} 实时数据..."):
                sc_data = fetch_sc_data(sc_ticker)
        
            if sc_data is None or "error" in (sc_data or {}):
                st.warning(f"无法获取 {sc_ticker} 数据，请检查代码是否正确。")
                sc_data = None
        
            st.divider()
        
            if sc_data:
                # 股票信息横幅
                chg_clr = "#0F6E56" if sc_data["chg_pct"] >= 0 else "#A32D2D"
                cap_str = f"${sc_data['mktcap']/1e12:.2f}T" if sc_data.get("mktcap") and sc_data["mktcap"]>1e12 else                       f"${sc_data['mktcap']/1e9:.1f}B" if sc_data.get("mktcap") else "N/A"
                st.markdown(
                    f'<div class="ahero" style="min-height:96px;'
                    f'background:linear-gradient(120deg,#1a1a2e 0%,#243b6b 100%)">'
                    f'{logo_watermark_html(sc_ticker, hero=True)}'
                    f'<div class="ahero-glass" style="padding:14px 20px;gap:14px">'
                    f'{logo_chip_html(sc_ticker, cls="ahero-chip")}'
                    f'<div style="flex:1">'
                    f'<div style="font-size:16px;font-weight:750">{sc_data["name"]} ({sc_ticker})</div>'
                    f'<div style="font-size:12px;opacity:0.75">{sc_data["sector"]}</div>'
                    f'</div>'
                    f'<div style="text-align:center;padding:0 16px;border-left:1px solid rgba(255,255,255,0.2)">'
                    f'<div style="font-size:26px;font-weight:700">${sc_data["price"]:.2f}</div>'
                    f'<div style="color:{chg_clr};font-size:13px;font-weight:600">{sc_data["chg_pct"]:+.2f}% 今日</div>'
                    f'</div>'
                    f'<div style="text-align:center;padding:0 16px;border-left:1px solid rgba(255,255,255,0.2)">'
                    f'<div style="font-size:12px;opacity:0.6">Beta</div>'
                    f'<div style="font-size:20px;font-weight:700">{sc_data["beta"]:.2f}</div>'
                    f'</div>'
                    f'<div style="text-align:center;padding:0 16px;border-left:1px solid rgba(255,255,255,0.2)">'
                    f'<div style="font-size:12px;opacity:0.6">市值</div>'
                    f'<div style="font-size:20px;font-weight:700">{cap_str}</div>'
                    f'</div>'
                    f'<div style="text-align:center;padding:0 16px;border-left:1px solid rgba(255,255,255,0.2)">'
                    f'<div style="font-size:12px;opacity:0.6">年化波动</div>'
                    f'<div style="font-size:20px;font-weight:700">{sc_data["sigma"]*100:.1f}%</div>'
                    f'</div>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )
        
                # ── 预测时间选择 ──────────────────────────────────────────────
                st.markdown("**⏱️ 预测时间范围**")
                time_cols = st.columns([3, 2])
                with time_cols[0]:
                    sc_months = st.select_slider(
                        "预测周期",
                        options=[1, 2, 3, 6, 9, 12, 15, 18],
                        value=6,
                        format_func=lambda x: f"{x}个月" if x < 12 else f"{x//12}年" + (f"{x%12}个月" if x%12 else ""),
                        key="sc_months_slider",
                    )
                with time_cols[1]:
                    st.markdown(f"<br><span style='font-size:28px;font-weight:700;color:#534AB7'>{sc_months}个月</span>", unsafe_allow_html=True)
        
                # ── 根据Beta和Sigma调整四情景的个股影响 ──────────────────────
                beta  = sc_data["beta"]
                sigma = sc_data["sigma"]
                price = sc_data["price"]
        
                def stock_scenario(base_mkt_annual: float, beta: float, sigma: float,
                                   idio_annual: float = 0, months: int = 6) -> dict:
                    """计算个股在给定市场情景、指定月数下的预期表现"""
                    # 将年化收益率转换为指定月数的收益率
                    t_frac       = months / 12
                    stock_annual = base_mkt_annual * beta + idio_annual
                    stock_ret    = (1 + stock_annual) ** t_frac - 1  # 复利
                    risk         = min(95, max(5, int(50 + sigma*50 - stock_annual*30)))
                    temp         = min(100, max(0, int(50 + stock_annual*25)))
                    return {
                        "pop":    round(stock_ret * 100, 1),
                        "six_m":  round(stock_ret * 100, 1),
                        "burst":  risk,
                        "temp":   temp,
                        "label":  "",
                        "desc":   "",
                    }
        
                # 四情景下市场预期年化收益率（基于宏观参数）
                sc_bull_mkt  = (sentiment+20)/100 * 0.15  - (rate-4)*0.02
                sc_base_mkt  = sentiment/100 * 0.10       - (rate-4)*0.015
                sc_bear_mkt  = (sentiment-20)/100 * 0.05  - (rate-3.5)*0.025
                sc_crash_mkt = (sentiment-40)/100 * (-0.05) - (rate-3)*0.04
        
                scenarios_stock = {
                    "🚀 牛市顺风": stock_scenario(sc_bull_mkt,  beta, sigma, +0.05, sc_months),
                    "📊 当前基准": stock_scenario(sc_base_mkt,  beta, sigma,  0.00, sc_months),
                    "🐻 泡沫破裂": stock_scenario(sc_bear_mkt,  beta, sigma, -0.05, sc_months),
                    "💥 系统崩溃": stock_scenario(sc_crash_mkt, beta, sigma, -0.15, sc_months),
                }
        
                period_label = f"{sc_months}个月" if sc_months < 12 else f"{sc_months//12}年" + (f"{sc_months%12}个月" if sc_months%12 else "")
                st.subheader(f"📡 {sc_ticker} · 四情景影响分析（{period_label}预测）")
                st.caption(f"Beta={beta:.2f} · 年化波动={sigma*100:.1f}% · 市场情绪={sentiment}/100 · 利率={rate}%")
        
                colors_sc = ["#1D9E75","#534AB7","#D85A30","#A32D2D"]
                sc_cols4  = st.columns(4)
                for i, (sc_name, sc_sim) in enumerate(scenarios_stock.items()):
                    with sc_cols4[i]:
                        c = colors_sc[i]
                        pop_str = f"+{sc_sim['pop']}%" if sc_sim['pop']>=0 else f"{sc_sim['pop']}%"
                        st.markdown(
                            f'<div style="background:{c};color:white;border-radius:10px;'
                            f'padding:14px 12px;text-align:center;margin-bottom:8px">'
                            f'<div style="font-size:14px;font-weight:700">{sc_name}</div>'
                            f'<div style="font-size:26px;font-weight:700;margin:6px 0">{pop_str}</div>'
                            f'<div style="font-size:11px;opacity:0.85">预期涨跌幅</div></div>',
                            unsafe_allow_html=True
                        )
                        six_str = f"+{sc_sim['six_m']}%" if sc_sim['six_m']>=0 else f"{sc_sim['six_m']}%"
                        st.metric(f"{period_label}收益", six_str)
                        # 计算价格目标
                        target_price = price * (1 + sc_sim["six_m"]/100)
                        st.metric(f"{period_label}目标价", f"${target_price:.2f}")
                        st.progress(sc_sim["temp"]/100, text=f"情景强度 {sc_sim['temp']}/100")
        
                # ── Beta影响说明 ──────────────────────────────────────────────
                st.divider()
                bc1, bc2 = st.columns(2)
                with bc1:
                    st.markdown("**⚡ Beta影响解读**")
                    if beta > 1.5:
                        beta_msg = f"Beta={beta:.2f}，高波动股，市场上涨时放大{beta:.1f}倍收益，下跌时也放大{beta:.1f}倍损失。"
                        beta_color = "#D85A30"
                    elif beta > 1.0:
                        beta_msg = f"Beta={beta:.2f}，略高于市场，走势与大盘高度相关但波动稍大。"
                        beta_color = "#BA7517"
                    elif beta > 0.5:
                        beta_msg = f"Beta={beta:.2f}，防御性股票，市场剧烈波动时相对稳定。"
                        beta_color = "#1D9E75"
                    else:
                        beta_msg = f"Beta={beta:.2f}，极低相关性，几乎独立于大盘走势。"
                        beta_color = "#0F6E56"
                    st.markdown(
                        f'<div style="background:#F8F9FA;border-left:4px solid {beta_color};'
                        f'padding:12px 14px;border-radius:6px;font-size:13px">{beta_msg}</div>',
                        unsafe_allow_html=True
                    )
        
                with bc2:
                    st.markdown("**📋 情景参数来源**")
                    vix_val = live_data_sim.get("^VIX",{}).get("price","N/A") if live_data_sim else "N/A"
                    for label, val, clr in [
                        ("市场情绪",  f"{sentiment}/100", "#534AB7"),
                        ("利率环境",  f"{rate}%",         "#D85A30"),
                        ("VIX恐慌",   f"{vix_val}",       "#A32D2D"),
                        ("个股Beta",  f"{beta:.2f}",      "#185FA5"),
                        ("年化波动率",f"{sigma*100:.1f}%", "#BA7517"),
                    ]:
                        st.markdown(
                            f'<div style="display:flex;justify-content:space-between;'
                            f'padding:6px 10px;background:#F8F9FA;border-radius:5px;'
                            f'margin-bottom:4px;font-size:12px">'
                            f'<span style="color:#666">{label}</span>'
                            f'<span style="font-weight:700;color:{clr}">{val}</span></div>',
                            unsafe_allow_html=True
                        )
            else:
                # 无股票数据时退回大盘分析
                st.subheader("📡 实时数据驱动 · 大盘四情景分析")
                st.caption(f"基于当前市场：情绪={sentiment}/100 · 利率={rate}%")
                scenarios_auto = {
                    "🚀 牛市顺风": simulate(min(sentiment+20,100), max(rate-0.5,1.0), min(ai_speed+20,100), min(retail+15,100)),
                    "📊 当前基准": simulate(sentiment, rate, ai_speed, retail),
                    "🐻 泡沫破裂": simulate(max(sentiment-20,0), rate+1.0, max(ai_speed-20,0), max(retail-20,0)),
                    "💥 系统崩溃": simulate(max(sentiment-40,0), rate+2.5, max(ai_speed-40,0), max(retail-40,0)),
                }
                colors_sc = ["#1D9E75","#534AB7","#D85A30","#A32D2D"]
                sc_cols4  = st.columns(4)
                for i, (sc_name, sc_sim) in enumerate(scenarios_auto.items()):
                    with sc_cols4[i]:
                        c = colors_sc[i]
                        pop_str = f"+{sc_sim['pop']}%" if sc_sim['pop']>=0 else f"{sc_sim['pop']}%"
                        st.markdown(
                            f'<div style="background:{c};color:white;border-radius:10px;'
                            f'padding:14px 12px;text-align:center;margin-bottom:8px">'
                            f'<div style="font-size:14px;font-weight:700">{sc_name}</div>'
                            f'<div style="font-size:26px;font-weight:700;margin:6px 0">{pop_str}</div>'
                            f'<div style="font-size:11px;opacity:0.85">首日预期涨幅</div></div>',
                            unsafe_allow_html=True
                        )
                        six_str = f"+{sc_sim['six_m']}%" if sc_sim['six_m']>=0 else f"{sc_sim['six_m']}%"
                        st.metric("6个月收益", six_str)
                        st.metric("泡沫破裂概率", f"{sc_sim['burst']}%", delta_color="inverse")
                        st.progress(sc_sim["temp"]/100, text=f"温度 {sc_sim['temp']}/100")
        
        else:
            st.subheader("情景预设")
            sc_cols = st.columns(4)
            chosen_sc = None
            for i, (name, vals) in enumerate(SCENARIOS.items()):
                if sc_cols[i].button(name, use_container_width=True):
                    chosen_sc = vals
        
            if live_data_sim:
                st.caption(f"📡 实时市场情绪估算：**{auto_sentiment}/100**（基于纳斯达克+VIX+英伟达）")
        
            col_l, col_r = st.columns(2)
            with col_l:
                sentiment = st.slider("市场情绪（0=恐慌，100=狂热）", 0, 100,
                                      int(chosen_sc[0]) if chosen_sc else auto_sentiment)
                rate      = st.slider("利率环境（%）", 1.0, 8.0,
                                      float(chosen_sc[1]) if chosen_sc else auto_rate, step=0.1)
            with col_r:
                ai_speed  = st.slider("AI商业化速度（0=慢，100=快）", 0, 100,
                                      int(chosen_sc[2]) if chosen_sc else 60)
                retail    = st.slider("散户参与度（0=低，100=高）", 0, 100,
                                      int(chosen_sc[3]) if chosen_sc else auto_retail)
        
            sim = simulate(sentiment, rate, ai_speed, retail)
            _ex = explain_simulate(sentiment, rate, ai_speed, retail, sim)
            r1, r2, r3 = st.columns(3)
            r1.metric("首日预期涨幅", f"+{sim['pop']}%")
            r2.metric("6个月后收益", f"{'+' if sim['six_m']>=0 else ''}{sim['six_m']}%")
            r3.metric("泡沫破裂概率", f"{sim['burst']}%", "未来18个月内", delta_color="inverse")

            why(_ex["pop"][0],   _ex["pop"][1],   calc=_ex["pop"][2],   title="首日预期涨幅",   target=r1)
            why(_ex["six_m"][0], _ex["six_m"][1], calc=_ex["six_m"][2], title="6个月后收益",   target=r2)
            why(_ex["burst"][0], _ex["burst"][1], calc=_ex["burst"][2], title="泡沫破裂概率", target=r3)

            temp_label = ("极度过热" if sim["temp"]>80 else "中度过热"
                          if sim["temp"]>60 else "温和偏高" if sim["temp"]>40 else "相对理性")
            st.progress(sim["temp"]/100, text=f"泡沫温度计：**{sim['temp']}/100 — {temp_label}**")
            why(_ex["temp"][0], _ex["temp"][1], calc=_ex["temp"][2], title=f"温度计 {sim['temp']}/100（{temp_label}）")
            st.info(f"**{sim['label']}** — {sim['desc']}")
            why(f"这句结论对应的是破裂概率 {sim['burst']}% 所落在的区间："
                f"0–19%→极度乐观、20–39%→温和上行、40–59%→基准预期、60–79%→高度警觉、80%以上→泡沫破裂风险。"
                f"所以你调动滑块让破裂概率跨过某个整二十的门槛时，这段文字才会换。",
                "neutral", title="这段结论怎么选出来的")
        
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=sim["burst"],
                title={"text":"泡沫破裂概率 (%)"},
                gauge={
                    "axis":{"range":[0,100]},
                    "bar":{"color":"#A32D2D" if sim["burst"]>65 else "#BA7517" if sim["burst"]>40 else "#1D9E75"},
                    "steps":[{"range":[0,40],"color":"#E1F5EE"},
                              {"range":[40,70],"color":"#FAEEDA"},
                              {"range":[70,100],"color":"#FCEBEB"}],
                },
            ))
            fig_gauge.update_layout(height=280, margin=dict(t=40,b=10))
            glass_chart(fig_gauge, use_container_width=True)


    # ══════════════════════════════════════════════════════════════════════
    # 💼 投资组合构建器
    # ══════════════════════════════════════════════════════════════════════
    with st.expander("💼 投资组合构建器 + 组合预测", expanded=True):
        st.markdown("#### 构建你的投资组合")
        st.caption("添加股票/ETF并设置投入金额，系统将自动分析组合风险并预测未来表现")

        if "portfolio" not in st.session_state:
            st.session_state["portfolio"] = [
                {"ticker":"SPY",  "amount":5000.0},
                {"ticker":"NVDA", "amount":3000.0},
                {"ticker":"QQQ",  "amount":2000.0},
            ]

        # 快捷预设
        st.markdown("**快捷预设**")
        preset_btns = st.columns(4)
        presets = {
            "🛡️ 稳健型": [("SPY",5000),("BND",3000),("GLD",2000)],
            "🚀 成长型": [("QQQ",4000),("NVDA",3000),("MSFT",2000),("TSLA",1000)],
            "🌏 全球型": [("VTI",3000),("VXUS",2000),("GLD",1000),("BND",2000),("BABA",1000)],
            "🤖 AI主题": [("NVDA",4000),("MSFT",2000),("GOOGL",2000),("SPCX",2000)],
        }
        for i,(pname,ptickers) in enumerate(presets.items()):
            if preset_btns[i].button(pname, key=f"preset_{i}", use_container_width=True):
                st.session_state["portfolio"] = [{"ticker":tk,"amount":float(amt)} for tk,amt in ptickers]
                st.rerun()

        st.divider()

        # 组合编辑器
        portfolio = st.session_state["portfolio"]
        total_invest = sum(p["amount"] for p in portfolio)

        hc = st.columns([2,2,1,1])
        hc[0].markdown("**股票代码**")
        hc[1].markdown("**投入金额 ($)**")
        hc[2].markdown("**占比**")
        hc[3].markdown("**删除**")

        to_remove = []
        for idx, pos in enumerate(portfolio):
            rc = st.columns([2,2,1,1])
            new_ticker = rc[0].text_input("", value=pos["ticker"], key=f"pf_t_{idx}",
                                           label_visibility="collapsed").strip().upper()
            new_amount = rc[1].number_input("", value=float(pos["amount"]), min_value=0.0,
                                             step=500.0, key=f"pf_a_{idx}",
                                             label_visibility="collapsed")
            pct = new_amount/total_invest*100 if total_invest>0 else 0
            rc[2].markdown(f"<br><b>{pct:.0f}%</b>", unsafe_allow_html=True)
            if rc[3].button("🗑️", key=f"pf_d_{idx}"):
                to_remove.append(idx)
            portfolio[idx]["ticker"] = new_ticker
            portfolio[idx]["amount"] = new_amount

        for i in sorted(to_remove, reverse=True):
            portfolio.pop(i)
        if to_remove:
            st.rerun()

        # 添加新股票
        ac = st.columns([2,2,1,1])
        new_tk = ac[0].text_input("", placeholder="代码如 AAPL", key="pf_ntk",
                                   label_visibility="collapsed").strip().upper()
        new_amt = ac[1].number_input("", value=1000.0, min_value=0.0, step=500.0,
                                      key="pf_namt", label_visibility="collapsed")
        if ac[3].button("➕", key="pf_add", use_container_width=True):
            if new_tk:
                portfolio.append({"ticker":new_tk,"amount":new_amt})
                st.rerun()

        st.session_state["portfolio"] = portfolio
        total_invest = sum(p["amount"] for p in portfolio)

        st.divider()

        if portfolio and total_invest > 0:
            pf_c1, pf_c2, pf_c3 = st.columns(3)
            pf_horizon_map = {"6个月":6,"1年":12,"3年":36,"5年":60,"10年":120,"20年":240}
            pf_hl = pf_c1.selectbox("预测周期", list(pf_horizon_map.keys()), index=1, key="pf_hl")
            pf_months = pf_horizon_map[pf_hl]
            pf_mc_n   = pf_c2.selectbox("模拟路径数", [200,500,1000], index=1, key="pf_mcn")
            pf_c3.metric("总投资额", f"${total_invest:,.0f}")

            @st.cache_data(ttl=300)
            def fetch_pf_data(tickers_tuple):
                import yfinance as yf, numpy as _np
                result = {}
                for tk in tickers_tuple:
                    try:
                        hist = yf.Ticker(tk).history(period="2y")
                        if hist.empty or len(hist)<30: continue
                        close = hist["Close"].dropna()
                        rets  = close.pct_change().dropna()
                        info  = {}
                        try: info = yf.Ticker(tk).info
                        except: pass
                        result[tk] = {
                            "price": float(close.iloc[-1]),
                            "mu":    float(rets.mean()*252),
                            "sigma": float(rets.std()*(252**0.5)),
                            "beta":  float(info.get("beta",1.0) or 1.0),
                            "name":  info.get("longName",tk)[:18],
                        }
                    except: pass
                return result

            with st.spinner("正在获取组合数据..."):
                pf_data = fetch_pf_data(tuple(p["ticker"] for p in portfolio))

            valid_pf = [p for p in portfolio if p["ticker"] in pf_data]
            if not valid_pf:
                st.error("无法获取任何股票数据，请检查代码是否正确。")
            else:
                valid_total = sum(p["amount"] for p in valid_pf)
                weights = [p["amount"]/valid_total for p in valid_pf]

                # 饼图 + 组合指标
                pc1, pc2 = st.columns([1,1])
                with pc1:
                    pie_colors = ["#185FA5","#534AB7","#1D9E75","#D85A30",
                                  "#F5A623","#A32D2D","#0F6E56","#BA7517"]
                    fig_pie = go.Figure(go.Pie(
                        labels=[p["ticker"] for p in valid_pf],
                        values=[p["amount"] for p in valid_pf],
                        marker=dict(colors=pie_colors[:len(valid_pf)]),
                        hole=0.4, textinfo="label+percent",
                        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
                    ))
                    fig_pie.update_layout(height=260, margin=dict(t=10,b=10,l=10,r=10),
                                          showlegend=False,
                                          annotations=[dict(text=f"${valid_total:,.0f}",
                                                            x=0.5, y=0.5, font_size=13, showarrow=False)])
                    glass_chart(fig_pie, use_container_width=True)

                with pc2:
                    pf_mu    = sum(w*pf_data[p["ticker"]]["mu"]    for w,p in zip(weights,valid_pf))
                    pf_sigma = sum(w*pf_data[p["ticker"]]["sigma"] for w,p in zip(weights,valid_pf))
                    pf_beta  = sum(w*pf_data[p["ticker"]]["beta"]  for w,p in zip(weights,valid_pf))
                    sharpe   = pf_mu/pf_sigma if pf_sigma>0 else 0
                    st.markdown("**组合风险指标**")
                    for lbl, val, clr in [
                        ("年化预期收益", f"{pf_mu*100:+.1f}%",  "#0F6E56" if pf_mu>0 else "#A32D2D"),
                        ("年化波动率",   f"{pf_sigma*100:.1f}%","#BA7517"),
                        ("夏普比率",     f"{sharpe:.2f}",        "#0F6E56" if sharpe>1 else "#BA7517" if sharpe>0.5 else "#A32D2D"),
                        ("加权Beta",     f"{pf_beta:.2f}",       "#534AB7"),
                        ("持仓数量",     f"{len(valid_pf)}支",   "#185FA5"),
                    ]:
                        st.markdown(
                            f'<div style="display:flex;justify-content:space-between;padding:6px 10px;'
                            f'background:#F8F9FA;border-radius:6px;margin-bottom:4px;font-size:13px">'
                            f'<span style="color:#666">{lbl}</span>'
                            f'<span style="font-weight:700;color:{clr}">{val}</span></div>',
                            unsafe_allow_html=True
                        )

                # 蒙地卡罗
                import numpy as _np2
                _np2.random.seed(42)
                dt = 1/12
                pf_paths = _np2.zeros((pf_months+1, pf_mc_n))
                pf_paths[0] = valid_total
                for step in range(1, pf_months+1):
                    port_ret = _np2.zeros(pf_mc_n)
                    for w, pos in zip(weights, valid_pf):
                        d   = pf_data[pos["ticker"]]
                        Z   = _np2.random.standard_normal(pf_mc_n)
                        r   = _np2.exp((d["mu"]-0.5*d["sigma"]**2)*dt + d["sigma"]*_np2.sqrt(dt)*Z) - 1
                        port_ret += w * r
                    pf_paths[step] = pf_paths[step-1] * (1 + port_ret)

                from datetime import datetime as _dt_pf
                _cy = _dt_pf.now().year
                if pf_months >= 12:
                    _xpf = [_cy+i/12 for i in range(pf_months+1)]
                    _tpf = list(range(_cy, _cy+pf_months//12+1, max(1,pf_months//12//6)))
                    _xt  = "年份"
                else:
                    _xpf = list(range(pf_months+1))
                    _tpf = _xpf
                    _xt  = "月份"

                pp5  = _np2.percentile(pf_paths, 5,  axis=1)
                pp25 = _np2.percentile(pf_paths, 25, axis=1)
                pp50 = _np2.percentile(pf_paths, 50, axis=1)
                pp75 = _np2.percentile(pf_paths, 75, axis=1)
                pp95 = _np2.percentile(pf_paths, 95, axis=1)

                fig_pf = go.Figure()
                fig_pf.add_trace(go.Scatter(x=_xpf+_xpf[::-1], y=list(pp95)+list(pp5[::-1]),
                    fill="toself", fillcolor="rgba(83,74,183,0.08)",
                    line=dict(width=0), name="90%置信区间", hoverinfo="skip"))
                fig_pf.add_trace(go.Scatter(x=_xpf+_xpf[::-1], y=list(pp75)+list(pp25[::-1]),
                    fill="toself", fillcolor="rgba(83,74,183,0.18)",
                    line=dict(width=0), name="50%置信区间", hoverinfo="skip"))
                fig_pf.add_trace(go.Scatter(x=_xpf, y=pp95, mode="lines", name="P95乐观",
                    line=dict(color="#1D9E75", width=1.5, dash="dot")))
                fig_pf.add_trace(go.Scatter(x=_xpf, y=pp5,  mode="lines", name="P5悲观",
                    line=dict(color="#E24B4A", width=1.5, dash="dot")))
                fig_pf.add_trace(go.Scatter(x=_xpf, y=pp50, mode="lines", name="中位数",
                    line=dict(color="#534AB7", width=2.5)))
                fig_pf.add_hline(y=valid_total, line_dash="dash", line_color="#888",
                                 annotation_text=f" 初始 ${valid_total:,.0f}",
                                 annotation_position="right",
                                 annotation_font=dict(size=11))
                fig_pf.update_layout(
                    height=400,
                    title=dict(text=f"投资组合 · {pf_mc_n}条蒙地卡罗 · {pf_hl}", font=dict(size=14)),
                    xaxis=dict(title=_xt, tickmode="array", tickvals=_tpf,
                               ticktext=[str(y) for y in _tpf],
                               showgrid=True, gridcolor="#eeeeee"),
                    yaxis=dict(title="组合价值 ($)", showgrid=True, gridcolor="#eeeeee"),
                    plot_bgcolor="#fafafa", hovermode="x unified",
                    legend=dict(orientation="h", y=1.08, x=0),
                    margin=dict(t=60,b=50,l=70,r=110),
                )
                glass_chart(fig_pf, use_container_width=True)

                # 期末结果
                final_vals = pf_paths[-1]
                pct_profit = (final_vals>valid_total).mean()*100
                pct_double = (final_vals>valid_total*2).mean()*100
                pct_loss50 = (final_vals<valid_total*0.5).mean()*100

                st.markdown(f"#### 📈 {pf_hl}后预测结果")
                rc1,rc2,rc3,rc4,rc5 = st.columns(5)
                rc1.metric("P95 乐观", f"${float(pp95[-1]):,.0f}", f"{(float(pp95[-1])/valid_total-1)*100:+.0f}%")
                rc2.metric("P75 较好", f"${float(pp75[-1]):,.0f}", f"{(float(pp75[-1])/valid_total-1)*100:+.0f}%")
                rc3.metric("P50 中位", f"${float(pp50[-1]):,.0f}", f"{(float(pp50[-1])/valid_total-1)*100:+.0f}%", delta_color="off")
                rc4.metric("P25 较差", f"${float(pp25[-1]):,.0f}", f"{(float(pp25[-1])/valid_total-1)*100:+.0f}%", delta_color="inverse")
                rc5.metric("P5 悲观",  f"${float(pp5[-1]):,.0f}",  f"{(float(pp5[-1])/valid_total-1)*100:+.0f}%",  delta_color="inverse")

                st.markdown(
                    f'<div style="background:#F0F4FF;border-radius:10px;padding:14px 18px;'
                    f'font-size:13px;line-height:2.2;margin-top:8px">'
                    f'🟢 盈利概率：<b style="color:#0F6E56">{pct_profit:.1f}%</b> &nbsp;|&nbsp; '
                    f'🚀 翻倍概率：<b style="color:#1D9E75">{pct_double:.1f}%</b> &nbsp;|&nbsp; '
                    f'🔴 腰斩概率：<b style="color:#A32D2D">{pct_loss50:.1f}%</b> &nbsp;|&nbsp; '
                    f'中位年化：<b>{((float(pp50[-1])/valid_total)**(12/pf_months)-1)*100:+.1f}%/年</b>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # 个股贡献
                st.markdown("#### 🔍 个股贡献分析")
                cc = st.columns(len(valid_pf))
                colors_pf = ["#185FA5","#534AB7","#1D9E75","#D85A30","#F5A623","#A32D2D","#0F6E56","#BA7517"]
                for i,(pos,w) in enumerate(zip(valid_pf,weights)):
                    d   = pf_data[pos["ticker"]]
                    clr = colors_pf[i % len(colors_pf)]
                    mu_clr = "#0F6E56" if d["mu"]>0 else "#A32D2D"
                    cc[i].markdown(
                        f'<div style="background:#F8F9FA;border-radius:8px;padding:10px 8px;'
                        f'text-align:center;border-top:3px solid {clr}">'
                        f'<div style="font-weight:700;font-size:14px">{pos["ticker"]}</div>'
                        f'<div style="font-size:10px;color:#888">{d["name"][:12]}</div>'
                        f'<div style="font-size:11px;color:#666;margin:3px 0">{w*100:.0f}% · ${pos["amount"]:,.0f}</div>'
                        f'<div style="color:{mu_clr};font-weight:700;font-size:13px">{d["mu"]*100:+.1f}%/年</div>'
                        f'<div style="font-size:11px;color:#888">波动 {d["sigma"]*100:.0f}%</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

    st.divider()
    st.subheader("🔮 核心资产多情景价格趋势模拟")

    # ── 自动/手动模式切换 ──
    t5_col1, t5_col2 = st.columns([1, 2])
    with t5_col1:
        auto_trend = st.toggle("🤖 自动填充市场数据", value=False,
                               help="从实时市场数据自动推算股票价格、波动率和预期收益率")
    with t5_col2:
        if auto_trend:
            st.info("请在下方选择一支股票，系统将自动从雅虎财经获取实时数据填充参数")

    st.divider()

    if auto_trend:
        # ── 标的选择：联想搜索 + 快捷预设 ──
        if "t5_ticker" not in st.session_state:
            st.session_state["t5_ticker"] = "QQQ"

        t5_ticker_presets = {
            "纳斯达克ETF": "QQQ", "标普500ETF": "SPY",
            "英伟达": "NVDA", "苹果": "AAPL", "微软": "MSFT",
            "特斯拉": "TSLA", "谷歌": "GOOGL", "亚马逊": "AMZN",
        }
        _t5pc = st.columns(len(t5_ticker_presets))
        for _i, (_pn, _pt) in enumerate(t5_ticker_presets.items()):
            with _t5pc[_i]:
                st.markdown(
                    f'<div class="arow" style="margin-bottom:4px;justify-content:center">'
                    f'{logo_chip_html(_pt, cls="arow-chip")}'
                    f'<span style="font-size:11.5px;font-weight:700;color:#0f172a">{_pn}</span></div>',
                    unsafe_allow_html=True)
                if st.button("选择", key=f"t5_preset_{_pt}", use_container_width=True):
                    st.session_state["t5_ticker"] = _pt
                    st.rerun()

        t5c1, t5c2 = st.columns([2, 2])
        with t5c1:
            auto_ticker = ticker_autocomplete(
                "t5_ticker_input", default=st.session_state["t5_ticker"],
                label="🔍 要预测的标的（边打边出提示，如 X、NVD、英伟达、比特币）")
            st.session_state["t5_ticker"] = auto_ticker
        with t5c2:
            st.markdown(
                f'<div class="arow" style="margin-top:26px">{logo_chip_html(auto_ticker, cls="arow-chip")}'
                f'<span style="font-size:13px;color:#0f172a">已选择 <b>{auto_ticker}</b>'
                f'<br><span style="font-size:11px;color:#64748b">'
                f'{TICKER_UNIVERSE.get(auto_ticker, "自定义代码")}</span></span></div>',
                unsafe_allow_html=True)

        horizon_map  = {"1年": 12, "5年": 60, "10年": 120, "20年": 240}
        horizon_sel  = st.selectbox("预测周期", list(horizon_map.keys()), index=1)
        time_horizon = horizon_map[horizon_sel]
        simulations  = st.selectbox("每情景路径数", [5, 10, 20], index=0)

        @st.cache_data(ttl=300)
        def fetch_ticker_params(ticker: str):
            try:
                import yfinance as yf, numpy as np_t
                t    = yf.Ticker(ticker)
                hist = t.history(period="1y")
                if hist.empty or len(hist) < 20:
                    return None
                close  = hist["Close"].dropna()
                price  = float(close.iloc[-1])
                rets   = close.pct_change().dropna()
                mu_ann = float(rets.mean() * 252)
                sig_ann= float(rets.std() * (252**0.5))
                sharpe = mu_ann / sig_ann if sig_ann > 0 else 0
                info   = {}
                try: info = t.info
                except: pass
                name   = info.get("longName", ticker)
                sector = info.get("sector", "")
                beta   = info.get("beta", 1.0) or 1.0
                return {
                    "ticker": ticker, "name": name, "sector": sector,
                    "price": price, "mu": round(mu_ann, 3),
                    "sigma": round(sig_ann, 3), "sharpe": round(sharpe, 2),
                    "beta": beta,
                }
            except Exception as e:
                return {"error": str(e)}

        with st.spinner(f"正在从雅虎财经获取 {auto_ticker} 数据..."):
            params = fetch_ticker_params(auto_ticker)

        if params is None:
            st.error("数据不足，请尝试其他股票代码。")
        elif "error" in params:
            st.error(f"获取失败：{params['error']}")
        else:
            # 展示自动填充的参数
            st.success(f"✅ 已自动获取 {params['name']} ({params['ticker']}) 实时数据")

            # ── 投资金额设置 ──────────────────────────────────────────────
            st.subheader("💰 投资金额设置")
            inv_c1, inv_c2, inv_c3 = st.columns([2, 1, 2])
            with inv_c1:
                invest_amount = st.number_input(
                    "投资金额", min_value=0.0, value=10000.0, step=1000.0,
                    format="%.2f", help="输入你计划投入的金额"
                )
            with inv_c2:
                currency = st.selectbox("货币", [
                    "USD 🇺🇸", "EUR 🇪🇺", "GBP 🇬🇧", "CNY 🇨🇳",
                    "JPY 🇯🇵", "HKD 🇭🇰", "SGD 🇸🇬", "KRW 🇰🇷",
                    "AUD 🇦🇺", "CAD 🇨🇦", "CHF 🇨🇭", "INR 🇮🇳",
                    "MXN 🇲🇽", "BRL 🇧🇷", "SEK 🇸🇪", "NOK 🇳🇴",
                ])

            # 实时汇率（用yfinance抓取）
            @st.cache_data(ttl=3600)
            def get_fx_rate(currency_code: str) -> float:
                if currency_code == "USD": return 1.0
                try:
                    import yfinance as yf
                    ticker_map = {
                        "EUR":"EURUSD=X","GBP":"GBPUSD=X","CNY":"CNY=X",
                        "JPY":"JPY=X","HKD":"HKD=X","SGD":"SGD=X",
                        "KRW":"KRW=X","AUD":"AUDUSD=X","CAD":"CAD=X",
                        "CHF":"CHF=X","INR":"INR=X","MXN":"MXN=X",
                        "BRL":"BRL=X","SEK":"SEK=X","NOK":"NOK=X",
                    }
                    sym  = ticker_map.get(currency_code)
                    if not sym: return 1.0
                    hist = yf.Ticker(sym).history(period="2d")
                    if hist.empty: return 1.0
                    rate = float(hist["Close"].iloc[-1])
                    # For XXX/USD pairs (EUR, GBP, AUD, CAD) rate is already USD per unit
                    # For USD/XXX pairs (JPY, CNY, HKD etc.) rate is units per USD → invert
                    direct = ["EUR","GBP","AUD"]
                    return rate if currency_code in direct else 1.0/rate
                except:
                    # Fallback static rates
                    fallback = {
                        "EUR":1.08,"GBP":1.27,"CNY":0.138,"JPY":0.0067,
                        "HKD":0.128,"SGD":0.74,"KRW":0.00072,"AUD":0.65,
                        "CAD":0.73,"CHF":1.10,"INR":0.012,"MXN":0.052,
                        "BRL":0.18,"SEK":0.093,"NOK":0.092,
                    }
                    return fallback.get(currency_code, 1.0)

            curr_code = currency.split()[0]
            fx_rate   = get_fx_rate(curr_code)
            invest_usd = invest_amount * fx_rate

            with inv_c3:
                st.markdown("<br>", unsafe_allow_html=True)
                if curr_code != "USD":
                    st.info(f"≈ **${invest_usd:,.2f} USD** | 汇率: 1 {curr_code} = {fx_rate:.4f} USD")
                else:
                    st.info(f"投资金额：**${invest_usd:,.2f} USD**")

            # 计算可购买股数
            shares = invest_usd / params["price"] if params["price"] > 0 else 0
            st.caption(f"📊 以当前价格 ${params['price']:.2f} 可购入约 **{shares:.2f} 股** {params['ticker']}")

            st.divider()

            p1, p2, p3, p4, p5 = st.columns(5)
            p1.metric("当前价格",    f"${params['price']:.2f}")
            p2.metric("年化预期收益", f"{params['mu']*100:+.1f}%",
                      "历史均值", delta_color="normal" if params["mu"]>0 else "inverse")
            p3.metric("年化波动率",   f"{params['sigma']*100:.1f}%",
                      "历史标准差", delta_color="off")
            p4.metric("夏普比率",     f"{params['sharpe']:.2f}",
                      "风险调整收益", delta_color="normal" if params["sharpe"]>0.5 else "inverse")
            p5.metric("Beta",        f"{params['beta']:.2f}")

            # 宏观冲击因子（根据VIX自动调整）
            live_t5   = fetch_market_data()
            vix_t5    = live_t5.get("^VIX", {}).get("price", 20) if live_t5 else 20
            macro_t5  = round((20 - vix_t5) * 0.1, 1)  # VIX低=正向冲击
            st.caption(f"📡 宏观冲击因子已根据当前VIX（{vix_t5:.1f}）自动设为 {macro_t5:+.1f}")

            s0         = params["price"]
            base_mu    = params["mu"]
            base_sigma = params["sigma"]
            macro_shock = macro_t5

            mu_base  = base_mu + (macro_shock * 0.02)
            mu_bull  = base_mu + 0.25 + (macro_shock * 0.05)
            mu_bear  = base_mu - 0.30 + (macro_shock * 0.05)
            sig_base = base_sigma
            sig_bull = max(0.05, base_sigma - 0.08)
            sig_bear = base_sigma + 0.20

            paths_base = generate_gbm_paths(s0, mu_base, sig_base, time_horizon, simulations, seed=42)
            paths_bull = generate_gbm_paths(s0, mu_bull, sig_bull, time_horizon, simulations, seed=42)
            paths_bear = generate_gbm_paths(s0, mu_bear, sig_bear, time_horizon, simulations, seed=42)

            # 将价格路径转换为投资组合价值
            port_base = paths_base * shares
            port_bull = paths_bull * shares
            port_bear = paths_bear * shares

            from datetime import datetime
            import pandas as _pd3
            current_year = datetime.now().year
            # X轴用实际年份
            if time_horizon >= 12:
                # 按年显示
                step       = time_horizon // 12
                time_years = [current_year + i/12 for i in range(time_horizon + 1)]
                x_labels   = [current_year + i/12 for i in range(time_horizon + 1)]
                x_title    = "年份"
            else:
                time_years = list(range(time_horizon + 1))
                x_labels   = time_years
                x_title    = "月份"

            fig_trend = go.Figure()
            for lbl, paths, color in [
                ("📊 基准", paths_base, "#534AB7"),
                ("🚀 乐观", paths_bull, "#1D9E75"),
                ("🐻 悲观", paths_bear, "#D85A30"),
            ]:
                for i in range(paths.shape[1]):
                    fig_trend.add_trace(go.Scatter(
                        x=x_labels, y=paths[:, i], mode="lines",
                        line=dict(color=color, width=2.5 if i==0 else 1,
                                  dash="solid" if i==0 else "dot"),
                        opacity=0.9 if i==0 else 0.25,
                        name=f"{lbl} 情景", showlegend=(i==0),
                    ))

            # 当前价格基准线
            fig_trend.add_hline(y=s0, line_dash="dash", line_color="#888",
                                line_width=1,
                                annotation_text=f" 当前价格 ${s0:.2f}",
                                annotation_position="right",
                                annotation_font=dict(size=11))

            # X轴刻度：整数年份
            tick_years  = list(range(current_year, current_year + time_horizon//12 + 1,
                                     max(1, time_horizon//12//8)))
            tick_vals   = [y for y in tick_years]

            fig_trend.update_layout(
                height=520,
                title=dict(text=f"{params['name']} ({auto_ticker}) · {horizon_sel}多情景GBM预测",
                           font=dict(size=14)),
                xaxis=dict(
                    title=x_title,
                    tickmode="array",
                    tickvals=tick_vals,
                    ticktext=[str(y) for y in tick_vals],
                    showgrid=True, gridcolor="#eeeeee",
                ),
                yaxis_title="价格 ($)",
                plot_bgcolor="#fafafa",
                hovermode="x unified",
                legend=dict(orientation="h", y=1.08, x=0),
                margin=dict(t=70, b=50, l=60, r=100),
            )
            from datetime import datetime as _dt_tr
            _sy_tr = _dt_tr.now().year
            fig_trend = add_year_range_tools(fig_trend, _sy_tr, _sy_tr + time_horizon//12)
            glass_chart(fig_trend, use_container_width=True)

            # ── 期末汇总：股价 + 投资组合价值 ──
            bull_end_p = np.mean(paths_bull[-1])
            base_end_p = np.mean(paths_base[-1])
            bear_end_p = np.mean(paths_bear[-1])
            bull_port  = np.mean(port_bull[-1])
            base_port  = np.mean(port_base[-1])
            bear_port  = np.mean(port_bear[-1])

            def fmt_val(v_usd, code, rate):
                v_local = v_usd / rate if rate > 0 else v_usd
                sym = {"USD":"$","EUR":"€","GBP":"£","CNY":"¥","JPY":"¥",
                       "HKD":"HK$","SGD":"S$","KRW":"₩","AUD":"A$",
                       "CAD":"C$","CHF":"Fr","INR":"₹","MXN":"MX$",
                       "BRL":"R$","SEK":"kr","NOK":"kr"}.get(code,"$")
                if v_local >= 1e9:   return f"{sym}{v_local/1e9:.2f}B"
                elif v_local >= 1e6: return f"{sym}{v_local/1e6:.2f}M"
                elif v_local >= 1e3: return f"{sym}{v_local/1e3:.2f}K"
                else:                return f"{sym}{v_local:.2f}"

            st.subheader(f"📈 {horizon_sel}后投资组合预测（初始投入 {fmt_val(invest_usd, curr_code, fx_rate)}）")
            c1, c2, c3 = st.columns(3)
            if invest_usd > 0:
                c1.metric(
                    "🚀 乐观情景",
                    fmt_val(bull_port, curr_code, fx_rate),
                    f"股价 ${bull_end_p:.2f}  |  回报 {(bull_port/invest_usd-1)*100:+.1f}%"
                )
                c2.metric(
                    "📊 基准情景",
                    fmt_val(base_port, curr_code, fx_rate),
                    f"股价 ${base_end_p:.2f}  |  回报 {(base_port/invest_usd-1)*100:+.1f}%",
                    delta_color="off"
                )
                c3.metric(
                    "🐻 悲观情景",
                    fmt_val(bear_port, curr_code, fx_rate),
                    f"股价 ${bear_end_p:.2f}  |  回报 {(bear_port/invest_usd-1)*100:+.1f}%",
                    delta_color="inverse"
                )
            else:
                st.info("💡 投资金额为0，仅展示股价预测，不计算回报率（回报率需要非零投资金额才有意义）。")
                c1.metric("🚀 乐观情景股价", f"${bull_end_p:.2f}")
                c2.metric("📊 基准情景股价", f"${base_end_p:.2f}")
                c3.metric("🐻 悲观情景股价", f"${bear_end_p:.2f}")

            if invest_usd > 0:
                st.markdown(
                    f'<div style="background:#F8F9FA;border-radius:8px;padding:12px 16px;'
                    f'font-size:13px;line-height:2;margin-top:8px">'
                    f'💡 <b>投资回报摘要</b>（初始投入 {fmt_val(invest_usd,curr_code,fx_rate)} · {shares:.2f}股）<br>'
                    f'🚀 乐观：{fmt_val(invest_usd,curr_code,fx_rate)} → <b>{fmt_val(bull_port,curr_code,fx_rate)}</b>'
                    f'（{(bull_port/invest_usd-1)*100:+.1f}%，年化约{((bull_port/invest_usd)**(12/time_horizon)-1)*100:+.1f}%）<br>'
                    f'📊 基准：{fmt_val(invest_usd,curr_code,fx_rate)} → <b>{fmt_val(base_port,curr_code,fx_rate)}</b>'
                    f'（{(base_port/invest_usd-1)*100:+.1f}%，年化约{((base_port/invest_usd)**(12/time_horizon)-1)*100:+.1f}%）<br>'
                    f'🐻 悲观：{fmt_val(invest_usd,curr_code,fx_rate)} → <b>{fmt_val(bear_port,curr_code,fx_rate)}</b>'
                    f'（{(bear_port/invest_usd-1)*100:+.1f}%，年化约{((bear_port/invest_usd)**(12/time_horizon)-1)*100:+.1f}%）'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # ── 蒙地卡罗完整模拟 ────────────────────────────────────────────
            st.divider()
            st.subheader("🎲 蒙地卡罗完整模拟")
            st.caption("使用大量随机路径模拟，展示价格分布的置信区间和概率分析")

            mc_n = st.select_slider("模拟路径数量", options=[100, 500, 1000, 5000], value=500)

            with st.spinner(f"正在运行 {mc_n} 条蒙地卡罗路径..."):
                mc_paths = generate_gbm_paths(s0, mu_base, sig_base, time_horizon, mc_n, seed=None)
                mc_port  = mc_paths * shares if invest_usd > 0 else mc_paths

            # 每个时间点的百分位数
            p5   = np.percentile(mc_paths, 5,  axis=1)
            p25  = np.percentile(mc_paths, 25, axis=1)
            p50  = np.percentile(mc_paths, 50, axis=1)
            p75  = np.percentile(mc_paths, 75, axis=1)
            p95  = np.percentile(mc_paths, 95, axis=1)

            from datetime import datetime as _dt2
            _cy2 = _dt2.now().year
            if time_horizon >= 12:
                _x2 = [_cy2 + i/12 for i in range(time_horizon + 1)]
                _ticks2 = list(range(_cy2, _cy2 + time_horizon//12 + 1,
                                     max(1, time_horizon//12//8)))
                _xtitle2 = "年份"
            else:
                _x2 = list(range(time_horizon + 1))
                _ticks2 = _x2
                _xtitle2 = "月份"

            fig_mc = go.Figure()

            # 90% 置信区间填充（浅蓝）
            fig_mc.add_trace(go.Scatter(
                x=_x2 + _x2[::-1], y=list(p95) + list(p5[::-1]),
                fill="toself", fillcolor="rgba(83,74,183,0.08)",
                line=dict(width=0), name="90% 置信区间",
                hoverinfo="skip",
            ))
            # 50% 置信区间填充（中蓝）
            fig_mc.add_trace(go.Scatter(
                x=_x2 + _x2[::-1], y=list(p75) + list(p25[::-1]),
                fill="toself", fillcolor="rgba(83,74,183,0.18)",
                line=dict(width=0), name="50% 置信区间",
                hoverinfo="skip",
            ))
            # P5/P95 边界线
            fig_mc.add_trace(go.Scatter(
                x=_x2, y=p95, mode="lines", name="P95（乐观95%）",
                line=dict(color="#1D9E75", width=1.5, dash="dot"),
            ))
            fig_mc.add_trace(go.Scatter(
                x=_x2, y=p5, mode="lines", name="P5（悲观5%）",
                line=dict(color="#E24B4A", width=1.5, dash="dot"),
            ))
            # P25/P75
            fig_mc.add_trace(go.Scatter(
                x=_x2, y=p75, mode="lines", name="P75",
                line=dict(color="#1D9E75", width=1, dash="dash"),
            ))
            fig_mc.add_trace(go.Scatter(
                x=_x2, y=p25, mode="lines", name="P25",
                line=dict(color="#E24B4A", width=1, dash="dash"),
            ))
            # 中位数（P50）
            fig_mc.add_trace(go.Scatter(
                x=_x2, y=p50, mode="lines", name="中位数（P50）",
                line=dict(color="#534AB7", width=2.5),
            ))
            # 当前价格线
            fig_mc.add_hline(
                y=s0, line_dash="dash", line_color="#888", line_width=1,
                annotation_text=f" 当前价格 ${s0:.2f}",
                annotation_position="right",
                annotation_font=dict(size=11),
            )

            fig_mc.update_layout(
                height=540,
                title=dict(
                    text=f"{auto_ticker} · {mc_n}条路径蒙地卡罗模拟 · {horizon_sel}",
                    font=dict(size=14)
                ),
                xaxis=dict(
                    title=_xtitle2,
                    tickmode="array",
                    tickvals=_ticks2,
                    ticktext=[str(y) for y in _ticks2],
                    showgrid=True, gridcolor="#eeeeee",
                    rangeslider=dict(visible=True, thickness=0.05, bgcolor="#fafafa"),
                ),
                yaxis=dict(title="价格 ($)", showgrid=True, gridcolor="#eeeeee"),
                plot_bgcolor="#fafafa",
                hovermode="x unified",
                legend=dict(orientation="h", y=1.08, x=0),
                margin=dict(t=70, b=60, l=60, r=100),
            )
            from datetime import datetime as _dt_mc
            _sy_mc = _dt_mc.now().year
            fig_mc = add_year_range_tools(fig_mc, _sy_mc, _sy_mc + time_horizon//12)
            glass_chart(fig_mc, use_container_width=True)

            # ── 期末概率分布直方图 ──
            st.subheader("📊 期末价格概率分布")
            final_prices = mc_paths[-1]
            final_ports  = mc_port[-1]

            mc_c1, mc_c2 = st.columns(2)

            with mc_c1:
                fig_hist_mc = go.Figure()
                fig_hist_mc.add_trace(go.Histogram(
                    x=final_prices,
                    nbinsx=50,
                    marker_color="#534AB7",
                    opacity=0.7,
                    name="期末价格分布",
                ))
                fig_hist_mc.add_vline(x=s0, line_dash="dash", line_color="#888",
                                      annotation_text=f" 现价 ${s0:.2f}",
                                      annotation_font=dict(size=11))
                fig_hist_mc.add_vline(x=float(p50[-1]), line_color="#0F6E56", line_width=2,
                                      annotation_text=f" 中位 ${float(p50[-1]):.2f}",
                                      annotation_font=dict(color="#0F6E56", size=11))
                fig_hist_mc.update_layout(
                    height=320, title=f"期末股价分布（{horizon_sel}后）",
                    xaxis_title="价格 ($)", yaxis_title="频次",
                    plot_bgcolor="#fafafa", showlegend=False,
                    margin=dict(t=50,b=40,l=50,r=20),
                )
                glass_chart(fig_hist_mc, use_container_width=True)

            with mc_c2:
                # 概率统计表
                pct_above = (final_prices > s0).mean() * 100
                pct_double = (final_prices > s0*2).mean() * 100
                pct_half   = (final_prices < s0*0.5).mean() * 100
                st.markdown("**📋 概率统计**")
                stats_data = [
                    ("高于现价概率",      f"{pct_above:.1f}%",
                     "#0F6E56" if pct_above>50 else "#A32D2D"),
                    ("翻倍概率（>2x）",   f"{pct_double:.1f}%", "#1D9E75"),
                    ("腰斩概率（<0.5x）", f"{pct_half:.1f}%",   "#E24B4A"),
                    ("P5  最坏5%结果",    f"${float(p5[-1]):.2f}", "#E24B4A"),
                    ("P25 较差25%结果",   f"${float(p25[-1]):.2f}","#D85A30"),
                    ("P50 中位数结果",    f"${float(p50[-1]):.2f}","#534AB7"),
                    ("P75 较好75%结果",   f"${float(p75[-1]):.2f}","#1D9E75"),
                    ("P95 最佳5%结果",    f"${float(p95[-1]):.2f}","#0F6E56"),
                ]
                for label, val, color in stats_data:
                    st.markdown(
                        f'<div style="display:flex;justify-content:space-between;'
                        f'padding:7px 12px;background:#F8F9FA;border-radius:6px;'
                        f'margin-bottom:4px;font-size:13px">'
                        f'<span>{label}</span>'
                        f'<span style="font-weight:700;color:{color}">{val}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                if invest_usd > 0:
                    st.markdown("**💰 投资组合概率统计**")
                    port_above  = (final_ports > invest_usd).mean() * 100
                    port_double = (final_ports > invest_usd*2).mean() * 100
                    port_p50    = float(np.percentile(final_ports, 50))
                    st.markdown(
                        f'<div style="background:#E1F5EE;border-radius:8px;padding:12px 14px;font-size:13px;line-height:2">'
                        f'盈利概率：<b style="color:#0F6E56">{port_above:.1f}%</b><br>'
                        f'翻倍概率：<b style="color:#1D9E75">{port_double:.1f}%</b><br>'
                        f'中位数结果：<b>{fmt_val(port_p50, curr_code, fx_rate)}</b>'
                        f'（回报 {(port_p50/invest_usd-1)*100:+.1f}%）'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            # 参数来源说明
            st.subheader("📋 参数来源说明")
            for label, val, source in [
                ("初始价格",    f"${s0:.2f}",               "雅虎财经实时收盘价"),
                ("年化收益率μ", f"{base_mu*100:+.1f}%",     "过去1年日收益率均值×252（年化）"),
                ("年化波动率σ", f"{base_sigma*100:.1f}%",   "过去1年日收益率标准差×√252（年化）"),
                ("宏观冲击",    f"{macro_shock:+.1f}",       f"根据当前VIX={vix_t5:.1f}自动计算"),
                ("乐观μ调整",   f"{mu_bull*100:+.1f}%",     "历史均值 + 25%乐观溢价 + 宏观冲击"),
                ("悲观μ调整",   f"{mu_bear*100:+.1f}%",     "历史均值 - 30%悲观折扣 + 宏观冲击"),
            ]:
                st.markdown(
                    f'<div style="display:flex;gap:16px;align-items:center;padding:8px 12px;'
                    f'background:#F8F9FA;border-radius:6px;margin-bottom:5px;font-size:13px">'
                    f'<b style="min-width:120px;color:#534AB7">{label}</b>'
                    f'<span style="min-width:70px;font-weight:700">{val}</span>'
                    f'<span style="color:#666">{source}</span></div>',
                    unsafe_allow_html=True
                )

    else:
        # ── 手动模式（原来的交互界面）──
        col1, col2, col3 = st.columns(3)
        with col1:
            s0              = st.number_input("初始资产价格 ($)", min_value=10.0, value=100.0, step=5.0)
            horizon_map_m   = {"1年": 12, "5年": 60, "10年": 120, "20年": 240}
            horizon_sel_m   = st.selectbox("预测周期", list(horizon_map_m.keys()), index=1)
            time_horizon    = horizon_map_m[horizon_sel_m]
        with col2:
            base_mu    = st.slider("基准年化预期收益率 (μ)", -0.5, 1.0, 0.15, step=0.05)
            base_sigma = st.slider("基准年化波动率 (σ)",     0.1, 1.5, 0.40, step=0.05)
        with col3:
            macro_shock  = st.slider("宏观情绪冲击因子", -5.0, 5.0, 0.0, step=0.5)
            simulations  = st.selectbox("每情景模拟路径数", [5, 10, 20], index=0)
        st.divider()

        mu_base  = base_mu + (macro_shock * 0.02)
        mu_bull  = base_mu + 0.30 + (macro_shock * 0.05)
        mu_bear  = base_mu - 0.40 + (macro_shock * 0.05)
        sig_base = base_sigma
        sig_bull = max(0.1, base_sigma - 0.10)
        sig_bear = base_sigma + 0.30
        paths_base = generate_gbm_paths(s0, mu_base, sig_base, time_horizon, simulations, seed=42)
        paths_bull = generate_gbm_paths(s0, mu_bull, sig_bull, time_horizon, simulations, seed=42)
        paths_bear = generate_gbm_paths(s0, mu_bear, sig_bear, time_horizon, simulations, seed=42)

        from datetime import datetime as _dt
        _cur_year = _dt.now().year
        if time_horizon >= 12:
            _x_labels = [_cur_year + i/12 for i in range(time_horizon + 1)]
            _tick_yrs = list(range(_cur_year, _cur_year + time_horizon//12 + 1,
                                   max(1, time_horizon//12//8)))
            _x_title  = "年份"
        else:
            _x_labels = list(range(time_horizon + 1))
            _tick_yrs = _x_labels
            _x_title  = "月份"

        fig_trend = go.Figure()
        for lbl, paths, color in [
            ("📊 基准", paths_base, "#534AB7"),
            ("🚀 乐观", paths_bull, "#1D9E75"),
            ("🐻 悲观", paths_bear, "#D85A30"),
        ]:
            for i in range(paths.shape[1]):
                fig_trend.add_trace(go.Scatter(
                    x=_x_labels, y=paths[:, i], mode="lines",
                    line=dict(color=color, width=2 if i==0 else 1,
                              dash="solid" if i==0 else "dot"),
                    opacity=0.9 if i==0 else 0.3,
                    name=f"{lbl} 情景", showlegend=(i==0),
                ))
        fig_trend.update_layout(
            height=500,
            title=f"未来{horizon_sel_m}多情景价格演化路径（GBM蒙特卡洛）",
            xaxis=dict(
                title=_x_title,
                tickmode="array",
                tickvals=_tick_yrs,
                ticktext=[str(y) for y in _tick_yrs],
                showgrid=True, gridcolor="#eeeeee",
            ),
            yaxis_title="价格 ($)",
            plot_bgcolor="#fafafa", hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        from datetime import datetime as _dt_tr2
        _sy_tr2 = _dt_tr2.now().year
        fig_trend = add_year_range_tools(fig_trend, _sy_tr2, _sy_tr2 + time_horizon//12)
        glass_chart(fig_trend, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("🚀 乐观情景均值", f"${np.mean(paths_bull[-1]):.2f}",
                  f"{(np.mean(paths_bull[-1])/s0-1)*100:.1f}%")
        c2.metric("📊 基准情景均值", f"${np.mean(paths_base[-1]):.2f}",
                  f"{(np.mean(paths_base[-1])/s0-1)*100:.1f}%", delta_color="off")
        c3.metric("🐻 悲观情景均值", f"${np.mean(paths_bear[-1]):.2f}",
                  f"{(np.mean(paths_bear[-1])/s0-1)*100:.1f}%", delta_color="inverse")

# ── Tab 5: 宏观分析 ──────────────────────────────────────────────────────────────
with tabs[4]:
    st.subheader("🌐 宏观经济指标与股市影响分析")
    st.caption("数据来自 FRED (美联储经济数据库) · 自动分析最新数据并预测对股市的影响")

    @st.cache_data(ttl=3600)
    def fetch_macro_data():
        """从 yfinance 抓取宏观代理数据（备用：静态近期数据）"""
        results = {}

        # 用 yfinance 抓取宏观代理指标
        try:
            import yfinance as yf
            proxies = {
                "^TNX":   ("DGS10",   "10年期国债收益率", "%",    "daily"),
                "^VIX":   ("VIXCLS",  "波动率指数VIX",   "指数", "daily"),
                "GLD":    ("GOLD",    "黄金ETF价格",     "$",    "daily"),
                "TIP":    ("T10YIE",  "通胀保值债券",    "$",    "daily"),
            }
            for ticker, (sid, name, unit, freq) in proxies.items():
                try:
                    t = yf.Ticker(ticker)
                    hist = t.history(period="3mo")
                    if not hist.empty:
                        vals  = [round(float(v), 2) for v in hist["Close"].dropna().values[-12:]]
                        dates = [str(d)[:10] for d in hist.index[-12:]]
                        if vals:
                            results[sid] = {
                                "name": name, "unit": unit, "freq": freq,
                                "dates": dates, "values": vals,
                                "latest": vals[-1],
                                "prev": vals[-2] if len(vals)>=2 else vals[-1],
                                "change": vals[-1]-vals[-2] if len(vals)>=2 else 0,
                            }
                except Exception:
                    pass
        except ImportError:
            pass

        # 静态备用数据（2026年6月最新公开数据）
        static = {
            "FEDFUNDS": ("联邦基金利率", "%",    "monthly",
                         ["2025-12","2026-01","2026-02","2026-03","2026-04","2026-05"],
                         [4.33, 4.33, 4.33, 4.33, 4.33, 4.33]),
            "CPIAUCSL": ("CPI通胀率",    "%",    "monthly",
                         ["2025-11","2025-12","2026-01","2026-02","2026-03","2026-04"],
                         [315.5, 316.4, 317.1, 317.8, 318.2, 318.9]),
            "UNRATE":   ("失业率",       "%",    "monthly",
                         ["2025-11","2025-12","2026-01","2026-02","2026-03","2026-04"],
                         [4.2, 4.1, 4.1, 4.0, 4.1, 4.2]),
            "PAYEMS":   ("非农就业变化", "K",    "monthly",
                         ["2025-11","2025-12","2026-01","2026-02","2026-03","2026-04"],
                         [212, 307, 111, 151, 228, 177]),
            "UMCSENT":  ("密歇根消费者信心","指数","monthly",
                         ["2025-11","2025-12","2026-01","2026-02","2026-03","2026-04"],
                         [71.8, 74.0, 71.1, 67.8, 57.0, 52.2]),
        }
        for sid, (name, unit, freq, dates, vals) in static.items():
            if sid not in results:
                results[sid] = {
                    "name": name, "unit": unit, "freq": freq,
                    "dates": dates, "values": vals,
                    "latest": vals[-1], "prev": vals[-2],
                    "change": vals[-1]-vals[-2],
                    "static": True,
                }
        return results

    def analyze_macro_impact(macro):
        """根据宏观数据自动生成股市影响分析"""
        signals = []
        score = 0  # 正=利多，负=利空

        # CPI分析
        if "CPIAUCSL" in macro and "error" not in macro["CPIAUCSL"]:
            cpi = macro["CPIAUCSL"]
            # YoY: compare latest vs 12 months ago; fallback to MoM change * 12
            if len(cpi["values"]) >= 13:
                cpi_yoy = ((cpi["latest"] / cpi["values"][-13]) - 1) * 100
            elif len(cpi["values"]) >= 2:
                cpi_yoy = cpi["change"] / cpi["prev"] * 100 * 12  # annualize MoM
            else:
                cpi_yoy = 3.0  # neutral default
            if cpi_yoy < 2.5:
                score += 15
                signals.append(("🟢", "CPI通胀受控", f"同比+{cpi_yoy:.1f}%，低于美联储2%目标附近，降息预期上升，利多股市。"))
            elif cpi_yoy < 3.5:
                score += 5
                signals.append(("🟡", "CPI温和", f"同比+{cpi_yoy:.1f}%，通胀温和，美联储维持中性政策。"))
            elif cpi_yoy < 5.0:
                score -= 10
                signals.append(("🟠", "CPI偏高", f"同比+{cpi_yoy:.1f}%，通胀压力上升，加息预期压制估值。"))
            else:
                score -= 20
                signals.append(("🔴", "CPI过热", f"同比+{cpi_yoy:.1f}%，高通胀环境，历史上对成长股杀伤力大。"))

        # 非农就业
        if "PAYEMS" in macro and "error" not in macro["PAYEMS"]:
            nfp = macro["PAYEMS"]
            mom_change = nfp["change"]  # 千人
            if mom_change > 200:
                score += 10
                signals.append(("🟢", "非农强劲", f"新增{mom_change:.0f}K就业，劳动市场健康，消费支撑股市。"))
            elif mom_change > 100:
                score += 5
                signals.append(("🟡", "非农温和", f"新增{mom_change:.0f}K就业，劳动市场稳定，对股市中性。"))
            elif mom_change > 0:
                score -= 5
                signals.append(("🟠", "非农偏弱", f"新增{mom_change:.0f}K就业，就业放缓，可能触发衰退担忧。"))
            else:
                score -= 15
                signals.append(("🔴", "非农负增长", f"减少{abs(mom_change):.0f}K就业，衰退信号，历史上大幅利空。"))

        # 联邦基金利率
        if "FEDFUNDS" in macro and "error" not in macro["FEDFUNDS"]:
            rate = macro["FEDFUNDS"]["latest"]
            change = macro["FEDFUNDS"]["change"]
            if rate < 2.0:
                score += 20
                signals.append(("🟢", "超低利率", f"联邦基金利率{rate:.2f}%，宽松周期利好成长股和科技股。"))
            elif rate < 3.5:
                score += 8
                signals.append(("🟢", "利率适中", f"联邦基金利率{rate:.2f}%，对股市影响中性偏正。"))
            elif rate < 5.0:
                score -= 8
                signals.append(("🟠", "利率偏高", f"联邦基金利率{rate:.2f}%，高利率压制高估值成长股。"))
            else:
                score -= 15
                signals.append(("🔴", "高利率环境", f"联邦基金利率{rate:.2f}%，高利率显著提升折现率，压制股票估值。"))
            if change < -0.1:
                score += 10
                signals.append(("🟢", "降息周期", f"利率下降{abs(change):.2f}%，降息周期历史上平均推动标普500上涨20%+。"))
            elif change > 0.1:
                score -= 10
                signals.append(("🔴", "加息周期", f"利率上升{change:.2f}%，加息周期初期通常对成长股造成压力。"))

        # 10年期国债
        if "DGS10" in macro and "error" not in macro["DGS10"]:
            t10 = macro["DGS10"]["latest"]
            if t10 < 3.0:
                score += 10
                signals.append(("🟢", "10年债收益率低", f"{t10:.2f}%，股票相对债券更有吸引力（TINA效应）。"))
            elif t10 < 4.5:
                score += 2
                signals.append(("🟡", "10年债收益率适中", f"{t10:.2f}%，股债竞争加剧，高估值股承压。"))
            else:
                score -= 12
                signals.append(("🔴", "10年债收益率高", f"{t10:.2f}%，债券吸引力增加，资金流出股市，P/E压缩。"))

        # 失业率
        if "UNRATE" in macro and "error" not in macro["UNRATE"]:
            unrate = macro["UNRATE"]["latest"]
            change = macro["UNRATE"]["change"]
            if unrate < 4.0:
                score += 8
                signals.append(("🟢", "就业市场强健", f"失业率{unrate:.1f}%，历史低位，消费能力强。"))
            elif unrate < 5.5:
                score += 3
                signals.append(("🟡", "就业市场正常", f"失业率{unrate:.1f}%，处于正常区间。"))
            else:
                score -= 12
                signals.append(("🔴", "失业率偏高", f"失业率{unrate:.1f}%，经济承压，消费需求走弱。"))

        # 消费者信心
        if "UMCSENT" in macro and "error" not in macro["UMCSENT"]:
            sentiment = macro["UMCSENT"]["latest"]
            if sentiment > 85:
                score += 8
                signals.append(("🟢", "消费者信心强", f"密歇根指数{sentiment:.1f}，消费预期乐观。"))
            elif sentiment > 65:
                score += 2
                signals.append(("🟡", "消费者信心中性", f"密歇根指数{sentiment:.1f}，消费预期平稳。"))
            else:
                score -= 8
                signals.append(("🔴", "消费者信心弱", f"密歇根指数{sentiment:.1f}，消费预期低迷，零售和消费股承压。"))

        # 综合判断
        if score >= 30:
            outlook = "🚀 强烈看涨"; outlook_color = "#0F6E56"
            summary = "宏观环境整体利多股市，低通胀+宽松货币政策+强就业三重利好共振，建议增加风险资产配置。"
        elif score >= 15:
            outlook = "📈 温和看涨"; outlook_color = "#1D9E75"
            summary = "宏观环境偏正面，主要风险指标可控，可维持正常股票仓位，重点关注成长股和科技股。"
        elif score >= 0:
            outlook = "⚖️ 中性"; outlook_color = "#BA7517"
            summary = "宏观信号混杂，正负因素并存，建议均衡配置，避免过度集中于高估值板块。"
        elif score >= -15:
            outlook = "📉 温和看空"; outlook_color = "#D85A30"
            summary = "宏观环境存在逆风，高利率或高通胀压制估值，建议降低仓位，增加防御性资产比重。"
        else:
            outlook = "💥 强烈看空"; outlook_color = "#A32D2D"
            summary = "多项宏观指标同时发出警告，历史上此类组合往往伴随较大市场回调，建议显著降低风险敞口。"

        return signals, score, outlook, outlook_color, summary

    if st.button("🔄 刷新宏观数据", key="refresh_macro"):
        st.cache_data.clear(); st.rerun()

    with st.spinner("正在从美联储数据库获取最新宏观数据..."):
        macro_data = fetch_macro_data()

    # 宏观指标总览
    st.subheader("📊 核心宏观指标（最新值）")
    macro_display = {
        "FEDFUNDS": ("🏦 联邦基金利率", "%",  "美联储政策利率",    True),
        "CPIAUCSL": ("📈 CPI指数",      "",   "消费者价格指数",    True),
        "UNRATE":   ("📉 失业率",       "%",  "劳动市场健康度",    True),
        "PAYEMS":   ("👷 非农就业变化", "K",  "月度新增就业（千）",False),
        "DGS10":    ("📜 10年期国债",   "%",  "长端无风险利率",    True),
        "T10YIE":   ("🌡️ 通胀保值债",  "$",  "通胀预期代理指标",  True),
        "UMCSENT":  ("😊 消费者信心",   "",   "密歇根大学消费信心",False),
        "VIXCLS":   ("⚡ VIX波动率",   "指数","市场恐慌程度",      True),
    }
    # 数据来源标注
    has_static = any(macro_data.get(sid,{}).get("static") for sid in macro_display)
    if has_static:
        st.caption("📋 部分数据为2026年5月最新公开数据（静态），实时代理指标来自市场价格")

    mcols = st.columns(4)
    shown = 0
    for sid, (label, unit, desc, is_bad_up) in macro_display.items():
        if sid in macro_data and "error" not in macro_data[sid]:
            d = macro_data[sid]
            chg = d["change"]
            chg_str = f"{'+' if chg>=0 else ''}{chg:.2f}{unit}"
            delta_color = ("inverse" if is_bad_up else "normal") if chg != 0 else "off"
            mcols[shown % 4].metric(
                label=label, value=f"{d['latest']:.2f}{unit}",
                delta=chg_str, delta_color=delta_color, help=desc,
            )
            shown += 1
    # Fill empty slots
    for _ in range(shown, 8):
        mcols[_ % 4].metric(label="获取中...", value="—")

    st.divider()

    # 股市影响分析
    signals, score, outlook, outlook_color, summary = analyze_macro_impact(macro_data)

    st.subheader("🎯 宏观环境对股市综合影响")
    st.markdown(
        f'<div style="background:{outlook_color};color:white;padding:16px 20px;'
        f'border-radius:10px;margin-bottom:12px">'
        f'<span style="font-size:22px;font-weight:700">{outlook}</span>'
        f'<span style="margin-left:16px;opacity:0.9;font-size:14px">综合评分：{score:+d}分</span><br>'
        f'<span style="font-size:13px;opacity:0.9;margin-top:6px;display:block">{summary}</span>'
        f'</div>', unsafe_allow_html=True
    )

    # 各指标信号
    st.subheader("📋 逐项指标分析")
    sig_c1, sig_c2 = st.columns(2)
    for i, (icon, title, desc) in enumerate(signals):
        col = sig_c1 if i % 2 == 0 else sig_c2
        bg = {"🟢":"#E1F5EE","🟡":"#FAEEDA","🟠":"#FDF0EC","🔴":"#FCEBEB"}.get(icon, "#F5F5F5")
        border = {"🟢":"#0F6E56","🟡":"#BA7517","🟠":"#D85A30","🔴":"#A32D2D"}.get(icon, "#999")
        col.markdown(
            f'<div style="background:{bg};border-left:4px solid {border};'
            f'padding:10px 14px;border-radius:6px;margin-bottom:8px;font-size:13px;line-height:1.7">'
            f'<b>{icon} {title}</b><br>{desc}</div>',
            unsafe_allow_html=True
        )

    st.divider()

    # 历史趋势图
    st.subheader("📈 关键指标历史走势")
    chart_tabs = st.tabs(["非农就业", "CPI通胀", "联邦基金利率", "10年期国债", "失业率", "消费者信心"])
    chart_map = [
        ("PAYEMS",  "非农新增就业（千人）", "#185FA5"),
        ("CPIAUCSL","消费者价格指数",       "#D85A30"),
        ("FEDFUNDS","联邦基金利率 (%)",      "#534AB7"),
        ("DGS10",   "10年期国债收益率 (%)", "#1D9E75"),
        ("UNRATE",  "失业率 (%)",           "#E24B4A"),
        ("UMCSENT", "密歇根消费者信心指数", "#F5A623"),
    ]
    for ct, (sid, ylabel, color) in zip(chart_tabs, chart_map):
        with ct:
            if sid in macro_data and "error" not in macro_data[sid]:
                d = macro_data[sid]
                fig_m = go.Figure()
                fig_m.add_trace(go.Scatter(
                    x=d["dates"], y=d["values"],
                    mode="lines+markers",
                    line=dict(color=color, width=2.5),
                    marker=dict(size=6, color=color,
                                line=dict(color="white", width=1.5)),
                    fill="tozeroy",
                    fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.08)",
                    hovertemplate=f"<b>%{{x}}</b><br>{ylabel}: %{{y:.2f}}<extra></extra>",
                ))
                # 最新值标注
                fig_m.add_annotation(
                    x=d["dates"][-1], y=d["values"][-1],
                    text=f"  最新: {d['values'][-1]:.2f}",
                    showarrow=False, xanchor="left",
                    font=dict(color=color, size=12, family="Arial Black"),
                )
                fig_m.update_layout(
                    height=320, plot_bgcolor="#fafafa",
                    yaxis_title=ylabel,
                    xaxis=dict(showgrid=True, gridcolor="#eeeeee"),
                    yaxis=dict(showgrid=True, gridcolor="#eeeeee"),
                    margin=dict(t=20, b=40, l=60, r=40),
                    showlegend=False,
                )
                glass_chart(fig_m, use_container_width=True)

                # 数据解读
                latest = d["values"][-1]
                chg    = d["change"]
                interp = {
                    "PAYEMS":  f"本月新增就业 {latest:.0f}K，环比{'增加' if chg>0 else '减少'} {abs(chg):.0f}K。{'就业市场强劲，支撑消费和企业盈利。' if latest>150 else '就业增速放缓，需警惕经济降温。'}",
                    "CPIAUCSL":f"CPI指数 {latest:.2f}，环比{'上升' if chg>0 else '下降'} {abs(chg):.2f}。{'通胀压力较大，加息预期升温。' if chg>0.3 else '通胀温和，货币政策压力减轻。'}",
                    "FEDFUNDS":f"政策利率 {latest:.2f}%，{'高利率压制估值，资金成本上升。' if latest>4 else '低利率环境支持股票估值扩张。'}",
                    "DGS10":   f"10年债收益率 {latest:.2f}%，{'与股票股息率竞争加剧，资金或从股市流向债市。' if latest>4 else '股票相对债券仍有吸引力。'}",
                    "UNRATE":  f"失业率 {latest:.1f}%，{'就业市场偏紧，消费韧性强。' if latest<4 else '失业率上升，消费和企业盈利面临压力。'}",
                    "UMCSENT": f"消费者信心 {latest:.1f}，{'消费者对经济前景乐观，有利于零售和消费板块。' if latest>80 else '消费者信心不足，消费支出可能走弱。'}",
                }.get(sid, "")
                if interp:
                    st.caption(interp)
            else:
                err = macro_data.get(sid, {}).get("error", "未知错误")
                st.info(f"暂无数据：{err}")

    st.divider()
    st.subheader("🔮 宏观情景对不同板块的影响预测")
    
    sectors = {
        "科技/成长股": {"high_rate": -20, "low_rate": +25, "high_cpi": -15, "low_cpi": +10, "strong_job": +10, "weak_job": -5},
        "金融股":      {"high_rate": +15, "low_rate": -10, "high_cpi": +5,  "low_cpi": -5,  "strong_job": +8,  "weak_job": -8},
        "消费股":      {"high_rate": -5,  "low_rate": +8,  "high_cpi": -10, "low_cpi": +5,  "strong_job": +15, "weak_job": -15},
        "能源股":      {"high_rate": -3,  "low_rate": +3,  "high_cpi": +20, "low_cpi": -10, "strong_job": +5,  "weak_job": -3},
        "医疗股":      {"high_rate": -5,  "low_rate": +5,  "high_cpi": -3,  "low_cpi": +3,  "strong_job": +5,  "weak_job": +3},
        "公用事业":    {"high_rate": -15, "low_rate": +15, "high_cpi": -5,  "low_cpi": +5,  "strong_job": +2,  "weak_job": +5},
    }

    # 判断当前环境
    rate_env  = "high_rate" if macro_data.get("FEDFUNDS",{}).get("latest",0) > 4 else "low_rate"
    cpi_env   = "high_cpi"  if macro_data.get("CPIAUCSL",{}).get("change",0) > 0.3 else "low_cpi"
    job_env   = "strong_job" if macro_data.get("PAYEMS",{}).get("change",0) > 100 else "weak_job"

    sector_scores = {}
    for sector, impacts in sectors.items():
        s = impacts[rate_env] + impacts[cpi_env] + impacts[job_env]
        sector_scores[sector] = s

    sorted_sectors = sorted(sector_scores.items(), key=lambda x: x[1], reverse=True)
    s_names = [s[0] for s in sorted_sectors]
    s_scores = [s[1] for s in sorted_sectors]
    s_colors = ["#0F6E56" if v > 10 else "#1D9E75" if v > 0 else "#D85A30" if v > -10 else "#A32D2D" for v in s_scores]

    fig_sec = go.Figure(go.Bar(
        x=s_scores, y=s_names, orientation="h",
        marker_color=s_colors,
        text=[f"{'+' if v>=0 else ''}{v}" for v in s_scores],
        textposition="outside",
    ))
    fig_sec.update_layout(
        height=320, plot_bgcolor="#fafafa",
        xaxis_title="宏观影响评分（正=利多，负=利空）",
        xaxis=dict(zeroline=True, zerolinecolor="#888", showgrid=True, gridcolor="#eeeeee"),
        yaxis=dict(showgrid=False),
        margin=dict(t=20, b=40, l=120, r=60),
        showlegend=False,
    )
    glass_chart(fig_sec, use_container_width=True)
    st.caption(f"基于当前：{'高利率' if rate_env=='high_rate' else '低利率'} + {'高通胀' if cpi_env=='high_cpi' else '低通胀'} + {'强就业' if job_env=='strong_job' else '弱就业'} 环境自动计算")

    st.divider()
    # ── 实时财经新闻 ─────────────────────────────────────────────────────────
    st.subheader("📰 实时财经新闻与地缘政治分析")

    @st.cache_data(ttl=1800)
    def fetch_financial_news():
        import urllib.request, xml.etree.ElementTree as ET
        feeds = [
            ("https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US", "市场"),
            ("https://feeds.finance.yahoo.com/rss/2.0/headline?s=NVDA,AAPL,MSFT&region=US&lang=en-US", "科技"),
        ]
        all_news = []
        for url, category in feeds:
            try:
                req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=8) as r:
                    tree = ET.parse(r)
                root = tree.getroot()
                for item in root.findall(".//item")[:8]:
                    title = item.findtext("title","")
                    pub   = item.findtext("pubDate","")[:22]
                    if title:
                        all_news.append({"title":title,"pub":pub,"category":category})
            except Exception:
                pass
        return all_news[:15]

    def classify_news(title):
        t = title.lower()
        geo = ["war","conflict","sanction","military","russia","ukraine","china","taiwan",
               "iran","missile","attack","invasion","tariff","trade war"]
        bull = ["rate cut","fed cut","rally","surge","beat","strong","record","ai boost",
                "upgrade","profit","earnings beat"]
        bear = ["recession","inflation","rate hike","selloff","crash","miss","weak",
                "layoff","bankruptcy","downgrade","warning"]
        if any(k in t for k in geo):
            return ("🌍","地缘政治","#534AB7","#EEEDFE",
                    "地缘风险短期利空，推升避险需求，压制科技股和周期股。")
        elif any(k in t for k in bull) and not any(k in t for k in bear):
            return ("🟢","利多信号","#0F6E56","#E1F5EE",
                    "正面消息，可能推动相关板块上涨，成长股和科技股受益。")
        elif any(k in t for k in bear) and not any(k in t for k in bull):
            return ("🔴","利空信号","#A32D2D","#FCEBEB",
                    "负面消息，可能引发回调，防御性资产相对受益。")
        return ("⚪","中性","#555","#F5F5F5","对市场整体影响中性。")

    news_list = fetch_financial_news()
    bull_c = bear_c = geo_c = 0
    for n in news_list:
        icon,_,_,_,_ = classify_news(n["title"])
        if icon=="🟢": bull_c+=1
        elif icon=="🔴": bear_c+=1
        elif icon=="🌍": geo_c+=1

    total_n = max(len(news_list),1)
    nc1,nc2,nc3,nc4 = st.columns(4)
    nc1.metric("📰 新闻数", len(news_list))
    nc2.metric("🟢 利多", bull_c, f"{bull_c/total_n*100:.0f}%", delta_color="normal")
    nc3.metric("🔴 利空", bear_c, f"{bear_c/total_n*100:.0f}%", delta_color="inverse")
    nc4.metric("🌍 地缘", geo_c, f"{geo_c/total_n*100:.0f}%", delta_color="off")

    news_score = (bull_c - bear_c - geo_c*0.5) / total_n
    if news_score > 0.2:
        nb,nc2c = "📰 新闻面整体正面，短线情绪偏多","#1D9E75"
    elif news_score < -0.2:
        nb,nc2c = "📰 新闻面整体负面，注意短线风险","#A32D2D"
    else:
        nb,nc2c = "📰 新闻面中性，市场由基本面主导","#BA7517"
    st.markdown(f'<div style="background:{nc2c};color:white;padding:10px 16px;border-radius:8px;'
                f'font-size:14px;font-weight:500;margin-bottom:12px">{nb}</div>',
                unsafe_allow_html=True)

    for n in news_list:
        icon,label,tc,bg,impact = classify_news(n["title"])
        st.markdown(
            f'<div style="background:{bg};border-left:4px solid {tc};padding:10px 14px;'
            f'border-radius:6px;margin-bottom:8px">'
            f'<div style="font-size:13px;font-weight:600;color:{tc}">{icon} [{label}] {n["title"]}</div>'
            f'<div style="font-size:11px;color:#666;margin-top:4px">📅 {n["pub"]} &nbsp;|&nbsp; '
            f'<span style="color:{tc}">影响：{impact}</span></div></div>',
            unsafe_allow_html=True)

    # 保存宏观状态供股票分析器使用
    st.session_state["macro_signals"] = signals
    st.session_state["macro_score"]   = score
    st.session_state["macro_outlook"] = outlook
    st.session_state["macro_summary"] = summary
    st.session_state["news_score"]    = news_score
    st.session_state["news_list"]     = news_list



# ── Tab 6: 股票分析器 ──────────────────────────────────────────────────────────
with tabs[5]:
    st.subheader("🔬 股票智能分析器")
    st.caption("输入任意股票代码，自动分析技术面+基本面，给出评级与价格目标")

    # ── 全局 session_state 初始化 ──
    if "selected_ticker" not in st.session_state:
        st.session_state["selected_ticker"] = ""
    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = None
    if "chart_type" not in st.session_state:
        st.session_state["chart_type"] = "📈 K线 + 斐波那契"

    # 快捷选股（带 Logo，点击后存入 session_state）
    st.write("**快捷选择热门标的：**")
    _grp_tabs = st.tabs(list(POPULAR_STOCKS.keys()))
    for _gt, (group, tickers) in zip(_grp_tabs, POPULAR_STOCKS.items()):
        with _gt:
            _qc = st.columns(min(len(tickers), 6))
            for i, tk in enumerate(tickers):
                with _qc[i % len(_qc)]:
                    st.markdown(
                        f'<div class="arow" style="margin-bottom:4px;justify-content:center">'
                        f'{logo_chip_html(tk, cls="arow-chip")}'
                        f'<span style="font-size:12.5px;font-weight:700;color:#0f172a">{tk}</span></div>',
                        unsafe_allow_html=True)
                    if st.button("分析", key=f"q_{group}_{tk}", use_container_width=True):
                        st.session_state["selected_ticker"] = tk
                        st.session_state["analysis_result"] = None
                        st.rerun()

    st.divider()

    # 股票代码输入框：边打边联想（输入 X 会列出 XOM / XLK / XRP-USD 等）
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        ticker_input = ticker_autocomplete(
            "analyzer_pick",
            default=st.session_state.get("selected_ticker") or "",
            label="🔍 输入股票代码或名称（边打边出提示，如 X、TSLA、特斯拉、比特币）")
    with col_btn:
        st.write("")
        st.write("")
        analyze_btn = st.button("🔍 开始分析", use_container_width=True, type="primary")

    # 触发分析：点击开始分析 或 输入框里有内容且与上次不同
    if analyze_btn and ticker_input:
        st.session_state["selected_ticker"] = ticker_input
        st.session_state["analysis_result"] = None  # 强制重新分析

    if st.session_state["selected_ticker"] and st.session_state["analysis_result"] is None:
        with st.spinner(f"正在分析 {st.session_state['selected_ticker']}..."):
            st.session_state["analysis_result"] = fetch_stock_analysis(
                st.session_state["selected_ticker"]
            )

    result = st.session_state["analysis_result"]
    ticker_input = st.session_state["selected_ticker"]

    if ticker_input and result is not None:
        if "error" in result:
            st.error(f"获取数据失败：{result['error']}")
        else:
            # ── 评级横幅（Logo 水印 + 毛玻璃）──
            _rc = result["rating_color"]
            st.markdown(
                f'<div class="ahero" style="background:linear-gradient(120deg,{_rc} 0%,{_rc}cc 55%,{_rc}99 100%)">'
                f'{logo_watermark_html(result["ticker"], hero=True)}'
                f'<div class="ahero-glass">'
                f'{logo_chip_html(result["ticker"], cls="ahero-chip")}'
                f'<span style="font-size:40px;line-height:1">{result["rating_emoji"]}</span>'
                f'<div>'
                f'<div style="font-size:27px;font-weight:750;letter-spacing:-.5px">{result["rating"]}</div>'
                f'<div style="font-size:13.5px;opacity:.92">{result["name"]} · {result["sector"]}</div>'
                f'</div>'
                f'<div style="margin-left:auto;text-align:right">'
                f'<div style="font-size:31px;font-weight:750;letter-spacing:-.5px">${result["price_now"]:.2f}</div>'
                f'<div style="font-size:12.5px;opacity:.92">综合评分：{result["score"]}/100</div>'
                f'</div></div></div>',
                unsafe_allow_html=True
            )

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

            # ── 逐项解释这五个数字 ──
            _sig = result.get("signals", [])
            _pos = sum(1 for s in _sig if s[0] == "✅")
            _neg = sum(1 for s in _sig if s[0] == "🔴")
            _neu = len(_sig) - _pos - _neg
            _p, _ma20, _ma50 = result["price_now"], result["ma20"], result["ma50"]
            _pos_desc = ("同时站上MA20和MA50，均线呈多头排列" if _p > _ma20 > _ma50 else
                         "跌破MA20和MA50，均线呈空头排列" if _p < _ma20 < _ma50 else
                         "在均线之间反复，方向尚未确认")
            why(f"现价是最近一个交易日的收盘价。相对均线看，它{_pos_desc}"
                f"（MA20=${_ma20:.2f}，MA50=${_ma50:.2f}）——均线位置决定了下面所有技术信号的基调。",
                "good" if _p > _ma20 else "bad", title="当前价格", target=m1)
            why(f"目标价不是分析师给的，是本模型按「综合评分档位 + 3个月动量 + RSI 修正」算出来的。"
                f"当前评分 {result['score']} 落在「{result['rating']}」档，再叠加3个月动量 {result['mom_3m']:+.1f}%，"
                f"得到 {result['price_target_pct']:+.1f}% 的空间。**它反映的是技术面延续性，不是基本面估值。**",
                "good" if result["price_target_pct"] >= 0 else "bad", title="价格目标", target=m2)
            why(f"当前价距52周最高价 ${result['price_52w_high']:.2f} 还有 {result['price_from_high']:.1f}%。"
                + ("离高点很近，说明趋势强势，但也意味着上方没有套牢盘做参照，回调时缺乏支撑位。"
                   if result["price_from_high"] > -5 else
                   "距离高点有明显回撤空间，说明股价已经历过一轮调整，上方存在套牢抛压。"),
                "good" if result["price_from_high"] > -10 else "warn", title="52周最高", target=m3)
            why(f"RSI 用过去14天的涨跌幅算出来：涨得多、跌得少，数值就高。"
                + (f"现在 {result['rsi']:.1f} **超过70属于超买**，说明短期买盘透支，回调风险上升。"
                   if result["rsi"] > 70 else
                   f"现在 {result['rsi']:.1f} **低于30属于超卖**，短期抛压释放较充分，反弹概率偏高。"
                   if result["rsi"] < 30 else
                   f"现在 {result['rsi']:.1f} 在30–70的中性区间，没有明显的超买或超卖信号。"),
                "bad" if result["rsi"] > 70 else "good" if result["rsi"] < 30 else "neutral",
                title="RSI (14)", target=m4)
            why(f"评分从 **50分中性起点** 出发，由下方「技术信号详情」里的每一条信号加减而来："
                f"本次共 **{_pos} 条利多信号加分、{_neg} 条利空信号减分、{_neu} 条中性**，最终得到 {result['score']} 分，"
                f"对应「{result['rating']}」评级（80+强力买入／65+买入／45+持有／30+卖出／30以下强力卖出）。",
                "good" if result["score"] >= 65 else "bad" if result["score"] < 45 else "neutral",
                title="综合评分", target=m5)

            # ── 买입/卖출理由 ──
            st.subheader("🧠 分析师意见")

            def gen_reason(r):
                lines = []
                p = r["price_now"]
                if r["rating"] in ("强力买入", "买入"):
                    lines.append(f"**{r['ticker']} 目前技术面偏多，综合评分 {r['score']}/100，给予「{r['rating']}」评级。**")
                elif r["rating"] == "持有":
                    lines.append(f"**{r['ticker']} 技术信号中性，综合评分 {r['score']}/100，建议「持有」观望。**")
                else:
                    lines.append(f"**{r['ticker']} 技术面偏空，综合评分 {r['score']}/100，给予「{r['rating']}」评级。**")

                if r["rsi"] < 30:
                    lines.append(f"RSI 仅 {r['rsi']:.1f}，处于严重超卖区间，历史上此位置出现反弹的概率较高，短线存在较好的买点。")
                elif r["rsi"] > 70:
                    lines.append(f"RSI 高达 {r['rsi']:.1f}，进入超买区间，短期获利盘压力较大，追高风险显著。")
                else:
                    lines.append(f"RSI 为 {r['rsi']:.1f}，处于中性区间，无明显超买超卖信号。")

                if r["macd_hist"] > 0:
                    lines.append(f"MACD 柱状图为正（{r['macd_hist']:.3f}），多头动能持续，金叉形态支撑上涨趋势。")
                else:
                    lines.append(f"MACD 柱状图为负（{r['macd_hist']:.3f}），空头动能占主导，死叉形态需警惕进一步下行。")

                if p > r["ma20"] and r["ma20"] > r["ma50"]:
                    lines.append(f"价格 ${p:.2f} 站于 MA20（${r['ma20']:.2f}）和 MA50（${r['ma50']:.2f}）之上，均线多头排列，中期趋势向好。")
                elif p < r["ma20"] and r["ma20"] < r["ma50"]:
                    lines.append(f"价格 ${p:.2f} 跌破 MA20（${r['ma20']:.2f}）和 MA50（${r['ma50']:.2f}），均线空头排列，中期趋势偏弱。")
                else:
                    lines.append(f"价格与均线关系中性（MA20: ${r['ma20']:.2f}，MA50: ${r['ma50']:.2f}），方向待确认。")

                if p < r["bb_low"]:
                    lines.append(f"价格触及布林带下轨（${r['bb_low']:.2f}），处于统计超卖区间，均值回归概率较高。")
                elif p > r["bb_up"]:
                    lines.append(f"价格突破布林带上轨（${r['bb_up']:.2f}），短期过度拉伸，需警惕回调。")

                if r["vol_ratio"] > 1.5 and r["mom_1m"] > 0:
                    lines.append(f"近期成交量是20日均量的 {r['vol_ratio']:.1f} 倍，放量上涨说明资金积极介入，信号可信度高。")
                elif r["vol_ratio"] > 1.5 and r["mom_1m"] < 0:
                    lines.append(f"近期成交量是20日均量的 {r['vol_ratio']:.1f} 倍，但伴随价格下跌，放量下跌为明显出逃信号。")
                else:
                    lines.append(f"成交量接近均值（{r['vol_ratio']:.1f}x），没有明显的资金异动。")

                if r["mom_1m"] > 10:
                    lines.append(f"过去1个月涨幅达 +{r['mom_1m']:.1f}%，3个月涨幅 {r['mom_3m']:+.1f}%，动量强劲，趋势追随者可考虑顺势参与。")
                elif r["mom_1m"] < -10:
                    lines.append(f"过去1个月跌幅 {r['mom_1m']:.1f}%，3个月跌幅 {r['mom_3m']:.1f}%，下行压力持续，建议等待趋势企稳。")

                if r["pe"] and r["pe"] > 0:
                    if r["pe"] < 15:
                        lines.append(f"基本面方面，P/E 仅 {r['pe']:.1f}x，估值处于低位，具备安全边际。")
                    elif r["pe"] > 50:
                        lines.append(f"基本面方面，P/E 高达 {r['pe']:.1f}x，估值偏贵，需要高增长持续兑现才能支撑当前股价。")

                if r["target_analyst"] and r["target_analyst"] > 0:
                    upside = (r["target_analyst"] - p) / p * 100
                    agree = "与本模型判断一致。" if (upside > 0) == (r["score"] >= 50) else "与本模型判断存在分歧，建议综合参考。"
                    lines.append(f"华尔街分析师平均目标价为 ${r['target_analyst']:.2f}，较现价 {'+' if upside>=0 else ''}{upside:.1f}%，{agree}")

                direction = "上行" if r["price_target_pct"] >= 0 else "下行"
                lines.append(f"综合以上因素，模型预测未来3个月价格目标为 ${r['price_target']:.2f}，{direction}空间约 {abs(r['price_target_pct']):.1f}%。")

                if r["rating"] in ("强力买入", "买入"):
                    lines.append("建议逢低分批建仓，严格设置止损位（建议设于近期低点下方3-5%）。")
                elif r["rating"] == "持有":
                    lines.append("建议持仓观望，等待更明确的方向性信号后再做决策。")
                else:
                    lines.append("建议减仓或设置严格止损，控制下行风险，等待技术面好转后再考虑重新介入。")

                return lines

            box_colors = {
                "强力买入": ("#E1F5EE", "#0F6E56"),
                "买入":     ("#F0FAF5", "#1D9E75"),
                "持有":     ("#FAEEDA", "#BA7517"),
                "卖出":     ("#FDF0EC", "#D85A30"),
                "强力卖出": ("#FCEBEB", "#A32D2D"),
            }
            bg, border = box_colors.get(result["rating"], ("#F5F5F5", "#cccccc"))
            reason_lines = gen_reason(result)
            for line in reason_lines:
                st.markdown(
                    f'<div style="background:{bg};border-left:4px solid {border};'
                    f'padding:10px 16px;border-radius:6px;margin-bottom:8px;'
                    f'font-size:14px;line-height:1.7">{line}</div>',
                    unsafe_allow_html=True
                )

            # ── 新增指标面板 ──
            st.subheader("📐 量化指标面板")
            qi1, qi2, qi3, qi4 = st.columns(4)
            qi1.metric("ATR波幅", f"${result['atr']:.2f}", f"占价格{result['atr_pct']:.1f}%")
            qi2.metric("建议止损位", f"${result['stop_loss']:.2f}", f"{result['stop_loss_pct']:.1f}%", delta_color="inverse")
            qi3.metric("夏普比率(年化)", f"{result['sharpe']:.2f}",
                       "优秀" if result['sharpe']>1.5 else "良好" if result['sharpe']>0.5 else "偏低")
            qi4.metric("趋势斜率(日)", f"{result['slope_pct']:+.2f}%",
                       "上升趋势" if result['slope_pct']>0.1 else "下降趋势" if result['slope_pct']<-0.1 else "横盘")

            qi5, qi6, qi7, qi8 = st.columns(4)
            qi5.metric("OBV资金趋势", result['obv_trend'],
                       f"{'高于' if result['obv_pct']>0 else '低于'}均线{abs(result['obv_pct']):.1f}%",
                       delta_color="normal" if result['obv_trend']=="上升" else "inverse")
            qi6.metric("斐波那契支撑", f"${result['nearest_support']:.2f}")
            qi7.metric("斐波那契阻力", f"${result['nearest_resistance']:.2f}")
            qi8.metric("MA200趋势", f"${result['ma200']:.2f}",
                       "价格在上方✓" if result['price_now']>result['ma200'] else "价格在下方✗",
                       delta_color="normal" if result['price_now']>result['ma200'] else "inverse")

            # ── 逐项解释这八个量化指标 ──
            why(f"ATR 是过去14天「每天最大波动幅度」的平均值。${result['atr']:.2f} 相当于股价的 "
                f"{result['atr_pct']:.1f}%，意思是**这只票平均每天上下晃动这么多**。"
                + ("波动偏大，设止损时要留足空间，否则容易被日常波动扫出局。" if result['atr_pct'] > 3
                   else "波动温和，适合设置较紧的止损。"),
                "warn" if result['atr_pct'] > 3 else "neutral", title="ATR波幅", target=qi1)
            why(f"止损位 = 现价 − 1.5×ATR = ${result['price_now']:.2f} − 1.5×${result['atr']:.2f} "
                f"= **${result['stop_loss']:.2f}**（{result['stop_loss_pct']:.1f}%）。"
                f"用ATR而不是固定百分比，是为了让止损宽度匹配这只票自身的波动性——波动大的票给更宽的空间。",
                "neutral", title="建议止损位", target=qi2)
            why(f"夏普比率 = 日均收益 ÷ 日收益标准差 × √252，衡量**每承担一单位风险能换来多少回报**。"
                + (f"{result['sharpe']:.2f} 属于优秀（>1.5），收益是靠稳定上涨而非大起大落赚来的。" if result['sharpe'] > 1.5
                   else f"{result['sharpe']:.2f} 属于良好（0.5–1.5），风险与收益基本匹配。" if result['sharpe'] > 0.5
                   else f"{result['sharpe']:.2f} 偏低甚至为负，说明这段时间承担的波动没换来相应回报，不如持有现金。"),
                "good" if result['sharpe'] > 1.5 else "neutral" if result['sharpe'] > 0.5 else "bad",
                title="夏普比率", target=qi3)
            why(f"对最近20个交易日的收盘价做一元线性回归，取斜率再除以现价，得到 **{result['slope_pct']:+.2f}%/日**。"
                f"它排除了单日跳空的干扰，比「近一月涨跌幅」更能反映趋势的**持续性**。"
                + ("目前斜率为正，趋势向上。" if result['slope_pct'] > 0.1
                   else "目前斜率为负，趋势向下。" if result['slope_pct'] < -0.1 else "斜率接近0，处于横盘整理。"),
                "good" if result['slope_pct'] > 0.1 else "bad" if result['slope_pct'] < -0.1 else "neutral",
                title="趋势斜率", target=qi4)
            why(f"OBV（能量潮）把上涨日的成交量累加、下跌日的成交量扣减，用来判断**资金是在进还是在出**。"
                f"当前OBV{'高于' if result['obv_pct'] > 0 else '低于'}其20日均线 {abs(result['obv_pct']):.1f}%，"
                + ("说明资金持续净流入，价格上涨有量能支撑。" if result['obv_trend'] == "上升"
                   else "说明资金在净流出，即使价格没怎么跌，也要警惕后续补跌。"),
                "good" if result['obv_trend'] == "上升" else "bad", title="OBV资金趋势", target=qi5)
            why(f"把52周最高价 ${result['price_52w_high']:.2f} 到最低价 ${result['price_52w_low']:.2f} 这段区间，"
                f"按斐波那契比例（23.6%/38.2%/50%/61.8%/78.6%）切分。"
                f"**${result['nearest_support']:.2f} 是现价下方最近的那条线**，跌到这里通常会遇到买盘承接。",
                "neutral", title="斐波那契支撑", target=qi6)
            why(f"同一套斐波那契分割线中，**现价上方最近的一条是 ${result['nearest_resistance']:.2f}**。"
                f"上涨到这个位置往往会遇到前期套牢盘解套抛售，需要放量才能有效突破。",
                "neutral", title="斐波那契阻力", target=qi7)
            _ma200_gap = (result['price_now'] - result['ma200']) / result['ma200'] * 100
            why(f"MA200 是过去200个交易日的平均成本，被视为**牛熊分界线**。"
                f"现价{'高于' if _ma200_gap > 0 else '低于'}它 {abs(_ma200_gap):.1f}%，"
                + ("处于长期上升结构中，是长线资金愿意持有的基本前提。" if _ma200_gap > 0
                   else "处于长期下降结构中，长线买入前最好等价格重新站回这条线之上。"),
                "good" if _ma200_gap > 0 else "bad", title="MA200趋势", target=qi8)

            # 斐波那契水平图
            st.subheader("📊 技术图表")

            # ── 图表选择器（用 session_state 保持选择，防止页面跳回顶部）──
            chart_options = ["📈 K线 + 斐波那契", "📉 K线 + 均线 + 布林带", "📊 RSI指标", "📦 成交量分析", "🌊 OBV能量潮"]
            if "chart_type" not in st.session_state:
                st.session_state["chart_type"] = chart_options[0]

            btn_cols = st.columns(len(chart_options))
            for i, opt in enumerate(chart_options):
                is_selected = st.session_state["chart_type"] == opt
                btn_style = (
                    "background:#534AB7;color:white;border:none;border-radius:8px;"
                    "padding:8px 12px;font-size:13px;cursor:pointer;width:100%;font-weight:600"
                    if is_selected else
                    "background:#f0f0f0;color:#333;border:1px solid #ddd;border-radius:8px;"
                    "padding:8px 12px;font-size:13px;cursor:pointer;width:100%"
                )
                if btn_cols[i].button(opt, key=f"chart_btn_{i}", use_container_width=True):
                    st.session_state["chart_type"] = opt

            chart_type = st.session_state["chart_type"]

            hist_c = result.get("hist")
            p_now  = result["price_now"]
            p_stop = result["stop_loss"]
            fib    = result["fib_levels"]

            # 静态数据无历史图表
            if hist_c is None:
                st.info("📊 图表数据同步中（通常需要3-5个交易日），请稍后再查看K线图。")
            elif chart_type == "📈 K线 + 斐波那契":
                fig_c = go.Figure()
                fig_c.add_trace(go.Candlestick(
                    x=hist_c.index,
                    open=hist_c["Open"], high=hist_c["High"],
                    low=hist_c["Low"],   close=hist_c["Close"],
                    name="K线",
                    increasing_line_color="#1D9E75",
                    decreasing_line_color="#E24B4A",
                    increasing_fillcolor="#1D9E75",
                    decreasing_fillcolor="#E24B4A",
                    showlegend=False,
                ))
                fib_cfgs = [
                    ("0.236", "Fib 23.6%", "#E07B39"),
                    ("0.382", "Fib 38.2%", "#D85A30"),
                    ("0.500", "Fib 50.0%", "#534AB7"),
                    ("0.618", "Fib 61.8%", "#3C3489"),
                    ("0.786", "Fib 78.6%", "#251F5C"),
                ]
                for key, label, _ in fib_cfgs:
                    v = fib[key]
                    clr = "#1D9E75" if v <= p_now else "#D85A30"
                    fig_c.add_hline(y=v, line_dash="dash", line_color=clr, line_width=1.5,
                                    annotation_text=f" {label}  ${v:.2f}",
                                    annotation_position="right",
                                    annotation_font=dict(color=clr, size=12))
                fig_c.add_hline(y=result["price_52w_high"], line_dash="dot",
                                line_color="#185FA5", line_width=1,
                                annotation_text=f" 52W高  ${result['price_52w_high']:.2f}",
                                annotation_position="right",
                                annotation_font=dict(color="#185FA5", size=11))
                fig_c.add_hline(y=result["price_52w_low"], line_dash="dot",
                                line_color="#534AB7", line_width=1,
                                annotation_text=f" 52W低  ${result['price_52w_low']:.2f}",
                                annotation_position="right",
                                annotation_font=dict(color="#534AB7", size=11))
                fig_c.add_hline(y=p_now, line_color="#0F6E56", line_width=2.5,
                                annotation_text=f" ▶ 现价  ${p_now:.2f}",
                                annotation_position="right",
                                annotation_font=dict(color="#0F6E56", size=13))
                fig_c.add_hline(y=p_stop, line_dash="dot", line_color="#A32D2D", line_width=1.8,
                                annotation_text=f" ⛔ 止损  ${p_stop:.2f}",
                                annotation_position="right",
                                annotation_font=dict(color="#A32D2D", size=12))
                fig_c.update_layout(
                    title=dict(text=f"{result['ticker']} · K线 + 斐波那契回撤位", font=dict(size=15)),
                    height=560, plot_bgcolor="#fafafa",
                    xaxis=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                               rangeslider=dict(visible=True, thickness=0.05)),
                    yaxis=dict(title="价格 ($)", showgrid=True, gridcolor="#eeeeee"),
                    margin=dict(t=90, b=50, l=60, r=160),
                    showlegend=False,
                )
                add_range_tools(fig_c, range_buttons=True, slider=False)

            # ── 图表2：K线 + 均线 + 布林带 ───────────────────────────────
            elif chart_type == "📉 K线 + 均线 + 布林带":
                close_s  = hist_c["Close"]
                ma20_s   = close_s.rolling(20).mean()
                ma50_s   = close_s.rolling(min(50,len(close_s))).mean()
                bb_mid_s = close_s.rolling(20).mean()
                bb_std_s = close_s.rolling(20).std()
                bb_up_s  = bb_mid_s + 2 * bb_std_s
                bb_lo_s  = bb_mid_s - 2 * bb_std_s

                fig_c = go.Figure()
                # 布林带填充
                fig_c.add_trace(go.Scatter(
                    x=hist_c.index, y=bb_up_s, mode="lines",
                    line=dict(color="rgba(83,74,183,0.3)", width=1),
                    name="布林上轨", showlegend=True,
                ))
                fig_c.add_trace(go.Scatter(
                    x=hist_c.index, y=bb_lo_s, mode="lines",
                    line=dict(color="rgba(83,74,183,0.3)", width=1),
                    fill="tonexty", fillcolor="rgba(83,74,183,0.06)",
                    name="布林下轨", showlegend=True,
                ))
                # K线
                fig_c.add_trace(go.Candlestick(
                    x=hist_c.index,
                    open=hist_c["Open"], high=hist_c["High"],
                    low=hist_c["Low"],   close=hist_c["Close"],
                    name="K线",
                    increasing_line_color="#1D9E75", decreasing_line_color="#E24B4A",
                    showlegend=False,
                ))
                fig_c.add_trace(go.Scatter(x=hist_c.index, y=ma20_s, mode="lines",
                    line=dict(color="#F5A623", width=1.8), name="MA20"))
                fig_c.add_trace(go.Scatter(x=hist_c.index, y=ma50_s, mode="lines",
                    line=dict(color="#534AB7", width=1.8), name="MA50"))
                fig_c.add_hline(y=p_now, line_color="#0F6E56", line_width=2,
                                annotation_text=f" 现价 ${p_now:.2f}",
                                annotation_position="right",
                                annotation_font=dict(color="#0F6E56", size=12))
                fig_c.update_layout(
                    title=dict(text=f"{result['ticker']} · K线 + MA20/MA50 + 布林带", font=dict(size=15)),
                    height=580, plot_bgcolor="#fafafa",
                    xaxis=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                               rangeslider=dict(visible=True, thickness=0.05)),
                    yaxis=dict(title="价格 ($)", showgrid=True, gridcolor="#eeeeee"),
                    legend=dict(orientation="h", y=1.08, x=0),
                    margin=dict(t=90, b=50, l=60, r=120),
                )
                add_range_tools(fig_c, range_buttons=True, slider=False)

            elif hist_c is not None and chart_type == "📊 RSI指标":
                close_s = hist_c["Close"].dropna()
                delta_s = close_s.diff()
                gain_s  = delta_s.clip(lower=0).rolling(14).mean()
                loss_s  = (-delta_s.clip(upper=0)).rolling(14).mean()
                rsi_s   = 100 - 100 / (1 + gain_s / loss_s.replace(0, 1e-9))

                from plotly.subplots import make_subplots as _msub
                fig_c = _msub(rows=2, cols=1, shared_xaxes=True,
                              row_heights=[0.6, 0.4], vertical_spacing=0.06,
                              subplot_titles=("价格走势", "RSI (14)"))
                fig_c.add_trace(go.Candlestick(
                    x=hist_c.index,
                    open=hist_c["Open"], high=hist_c["High"],
                    low=hist_c["Low"],   close=hist_c["Close"],
                    name="K线",
                    increasing_line_color="#1D9E75", decreasing_line_color="#E24B4A",
                    showlegend=False,
                ), row=1, col=1)
                fig_c.add_trace(go.Scatter(x=hist_c.index, y=rsi_s, mode="lines",
                    line=dict(color="#534AB7", width=2), name="RSI",
                    fill="tozeroy", fillcolor="rgba(83,74,183,0.08)",
                ), row=2, col=1)
                # 超买超卖区域
                fig_c.add_hrect(y0=70, y1=100, row=2, col=1,
                                fillcolor="rgba(226,75,74,0.1)", line_width=0)
                fig_c.add_hrect(y0=0, y1=30, row=2, col=1,
                                fillcolor="rgba(29,158,117,0.1)", line_width=0)
                fig_c.add_hline(y=70, line_dash="dash", line_color="#E24B4A",
                                line_width=1, row=2, col=1,
                                annotation_text=" 超买70", annotation_position="right",
                                annotation_font=dict(color="#E24B4A", size=11))
                fig_c.add_hline(y=30, line_dash="dash", line_color="#1D9E75",
                                line_width=1, row=2, col=1,
                                annotation_text=" 超卖30", annotation_position="right",
                                annotation_font=dict(color="#1D9E75", size=11))
                fig_c.update_layout(
                    title=dict(text=f"{result['ticker']} · RSI 相对强弱指标", font=dict(size=15)),
                    height=600, plot_bgcolor="#fafafa",
                    xaxis2=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                                rangeslider=dict(visible=True, thickness=0.04)),
                    yaxis=dict(showgrid=True, gridcolor="#eeeeee"),
                    yaxis2=dict(title="RSI", range=[0,100],
                                showgrid=True, gridcolor="#eeeeee"),
                    margin=dict(t=90, b=50, l=60, r=80),
                    showlegend=False,
                )
                # Add range selector to top chart (xaxis1)
                fig_c.update_xaxes(
                    rangeselector=dict(
                        buttons=[
                            dict(count=1,label="1月",step="month",stepmode="backward"),
                            dict(count=3,label="3月",step="month",stepmode="backward"),
                            dict(count=6,label="6月",step="month",stepmode="backward"),
                            dict(step="all",label="全部"),
                        ],
                        bgcolor="#f0f0f0", activecolor="#534AB7",
                        font=dict(size=11), x=0, y=1.02,
                    ), selector=dict(type="date"), row=1, col=1
                )

            elif hist_c is not None and chart_type == "📦 成交量分析":
                vol_ma20 = hist_c["Volume"].rolling(20).mean()
                bar_colors = ["#1D9E75" if c >= o else "#E24B4A"
                              for c, o in zip(hist_c["Close"], hist_c["Open"])]
                from plotly.subplots import make_subplots as _msub
                fig_c = _msub(rows=2, cols=1, shared_xaxes=True,
                              row_heights=[0.55, 0.45], vertical_spacing=0.06,
                              subplot_titles=("价格走势", "成交量（绿=上涨日，红=下跌日）"))
                fig_c.add_trace(go.Candlestick(
                    x=hist_c.index,
                    open=hist_c["Open"], high=hist_c["High"],
                    low=hist_c["Low"],   close=hist_c["Close"],
                    name="K线",
                    increasing_line_color="#1D9E75", decreasing_line_color="#E24B4A",
                    showlegend=False,
                ), row=1, col=1)
                fig_c.add_trace(go.Bar(
                    x=hist_c.index, y=hist_c["Volume"],
                    marker_color=bar_colors, name="成交量",
                    showlegend=False,
                ), row=2, col=1)
                fig_c.add_trace(go.Scatter(
                    x=hist_c.index, y=vol_ma20, mode="lines",
                    line=dict(color="#F5A623", width=2), name="20日均量",
                ), row=2, col=1)
                fig_c.update_layout(
                    title=dict(text=f"{result['ticker']} · 成交量分析", font=dict(size=15)),
                    height=600, plot_bgcolor="#fafafa",
                    xaxis2=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                                rangeslider=dict(visible=True, thickness=0.04)),
                    yaxis=dict(showgrid=True, gridcolor="#eeeeee"),
                    yaxis2=dict(title="成交量", showgrid=True, gridcolor="#eeeeee"),
                    legend=dict(orientation="h", y=1.08),
                    margin=dict(t=90, b=50, l=60, r=60),
                )
                fig_c.update_xaxes(
                    rangeselector=dict(
                        buttons=[
                            dict(count=1,label="1月",step="month",stepmode="backward"),
                            dict(count=3,label="3月",step="month",stepmode="backward"),
                            dict(count=6,label="6月",step="month",stepmode="backward"),
                            dict(step="all",label="全部"),
                        ],
                        bgcolor="#f0f0f0", activecolor="#534AB7",
                        font=dict(size=11), x=0, y=1.02,
                    ), selector=dict(type="date")
                )

            elif hist_c is not None and chart_type == "🌊 OBV能量潮":
                close_s = hist_c["Close"]
                vol_s   = hist_c["Volume"]
                obv_vals = []
                for i in range(len(close_s)):
                    if i == 0:
                        obv_vals.append(float(vol_s.iloc[i]))
                    else:
                        if close_s.iloc[i] > close_s.iloc[i-1]:
                            obv_vals.append(obv_vals[-1] + float(vol_s.iloc[i]))
                        elif close_s.iloc[i] < close_s.iloc[i-1]:
                            obv_vals.append(obv_vals[-1] - float(vol_s.iloc[i]))
                        else:
                            obv_vals.append(obv_vals[-1])
                import pandas as _pd
                obv_series = _pd.Series(obv_vals, index=close_s.index)
                obv_ma     = obv_series.rolling(20).mean()
                obv_color  = ["#1D9E75" if v >= 0 else "#E24B4A" for v in obv_vals]

                from plotly.subplots import make_subplots as _msub
                fig_c = _msub(rows=2, cols=1, shared_xaxes=True,
                              row_heights=[0.55, 0.45], vertical_spacing=0.06,
                              subplot_titles=("价格走势", "OBV 能量潮（资金净流向）"))
                fig_c.add_trace(go.Candlestick(
                    x=hist_c.index,
                    open=hist_c["Open"], high=hist_c["High"],
                    low=hist_c["Low"],   close=hist_c["Close"],
                    name="K线",
                    increasing_line_color="#1D9E75", decreasing_line_color="#E24B4A",
                    showlegend=False,
                ), row=1, col=1)
                fig_c.add_trace(go.Scatter(
                    x=hist_c.index, y=obv_series, mode="lines",
                    line=dict(color="#534AB7", width=2),
                    fill="tozeroy", fillcolor="rgba(83,74,183,0.08)",
                    name="OBV",
                ), row=2, col=1)
                fig_c.add_trace(go.Scatter(
                    x=hist_c.index, y=obv_ma, mode="lines",
                    line=dict(color="#F5A623", width=1.8, dash="dash"),
                    name="OBV MA20",
                ), row=2, col=1)
                fig_c.add_hline(y=0, line_color="#888", line_width=1, row=2, col=1)
                fig_c.update_layout(
                    title=dict(text=f"{result['ticker']} · OBV 能量潮（机构资金流向）", font=dict(size=15)),
                    height=600, plot_bgcolor="#fafafa",
                    xaxis2=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                                rangeslider=dict(visible=True, thickness=0.04)),
                    yaxis=dict(showgrid=True, gridcolor="#eeeeee"),
                    yaxis2=dict(title="OBV", showgrid=True, gridcolor="#eeeeee"),
                    legend=dict(orientation="h", y=1.08),
                    margin=dict(t=90, b=50, l=60, r=60),
                )
                fig_c.update_xaxes(
                    rangeselector=dict(
                        buttons=[
                            dict(count=1,label="1月",step="month",stepmode="backward"),
                            dict(count=3,label="3月",step="month",stepmode="backward"),
                            dict(count=6,label="6月",step="month",stepmode="backward"),
                            dict(step="all",label="全部"),
                        ],
                        bgcolor="#f0f0f0", activecolor="#534AB7",
                        font=dict(size=11), x=0, y=1.02,
                    ), selector=dict(type="date")
                )

            if hist_c is not None:
                try:
                    glass_chart(fig_c, use_container_width=True)
                except Exception:
                    pass

            # ── 长期投资分析 ──
            st.subheader("🏦 长期投资分析")
            lt = result
            lt_bg, lt_border = {
                "强烈推荐长期持有": ("#E1F5EE", "#0F6E56"),
                "适合长期投资":     ("#F0FAF5", "#1D9E75"),
                "中性，谨慎长持":   ("#FAEEDA", "#BA7517"),
                "不建议长期持有":   ("#FDF0EC", "#D85A30"),
                "规避，高风险资产": ("#FCEBEB", "#A32D2D"),
            }.get(lt["lt_rating"], ("#F5F5F5", "#999"))

            st.markdown(
                f'<div style="background:{lt_bg};border-left:5px solid {lt_border};'
                f'padding:14px 20px;border-radius:8px;margin-bottom:12px">'
                f'<span style="font-size:18px;font-weight:700;color:{lt_border}">'
                f'长期投资评级：{lt["lt_rating"]}</span>'
                f'<span style="margin-left:16px;color:#666;font-size:13px">长期评分：{lt["lt_score"]}/100</span>'
                f'</div>', unsafe_allow_html=True
            )

            # 自动生成长期分析文字
            def gen_lt_analysis(r):
                lines = []
                p = r["price_now"]
                ticker = r["ticker"]
                name = r.get("name", ticker)

                # 开头总结
                if r["lt_score"] >= 75:
                    lines.append(f"**{name}（{ticker}）具备较强的长期投资价值，综合量化评分 {r['lt_score']}/100。**")
                elif r["lt_score"] >= 60:
                    lines.append(f"**{name}（{ticker}）基本面与趋势均支持长期持有，综合评分 {r['lt_score']}/100。**")
                elif r["lt_score"] >= 45:
                    lines.append(f"**{name}（{ticker}）长期前景中性，需结合基本面深入研究，评分 {r['lt_score']}/100。**")
                else:
                    lines.append(f"**{name}（{ticker}）目前不具备明显的长期投资价值，综合评分 {r['lt_score']}/100，建议规避或等待更好入场时机。**")

                # 趋势稳定性
                if r["slope_pct"] > 0.1:
                    lines.append(f"📈 **趋势分析**：20日线性回归斜率为 +{r['slope_pct']:.2f}%/日，价格处于持续上升通道，长期持有者账面浮盈概率较高。")
                elif r["slope_pct"] < -0.1:
                    lines.append(f"📉 **趋势分析**：20日线性回归斜率为 {r['slope_pct']:.2f}%/日，价格处于持续下行通道，长期持有面临账面亏损风险，需等待趋势反转确认。")
                else:
                    lines.append(f"➡️ **趋势分析**：价格处于横盘整理阶段（斜率 {r['slope_pct']:+.2f}%/日），长期持有者需耐心等待方向突破。")

                # 资金面（OBV）
                if r["obv_trend"] == "上升":
                    lines.append(f"💰 **资金面**：OBV能量潮高于20日均线 {r['obv_pct']:.1f}%，机构资金长期净流入，是长期看涨的重要信号。")
                else:
                    lines.append(f"🚨 **资金面**：OBV能量潮低于20日均线 {abs(r['obv_pct']):.1f}%，资金持续净流出，长期持有需警惕进一步下跌。")

                # 风险调整收益（夏普）
                if r["sharpe"] > 1.5:
                    lines.append(f"⚡ **风险收益比**：年化夏普比率 {r['sharpe']:.2f}，属于优秀水平（>1.5），意味着每承担1单位风险可获得超过1.5单位收益，长期持有性价比高。")
                elif r["sharpe"] > 0.5:
                    lines.append(f"⚡ **风险收益比**：年化夏普比率 {r['sharpe']:.2f}，属于良好水平，风险与收益基本匹配，适合风险偏好中等的长期投资者。")
                elif r["sharpe"] < 0:
                    lines.append(f"⚠️ **风险收益比**：年化夏普比率 {r['sharpe']:.2f}（为负），意味着持有该股的风险调整后收益不及无风险利率，长期持有的机会成本较高。")
                else:
                    lines.append(f"⚡ **风险收益比**：年化夏普比率 {r['sharpe']:.2f}，风险收益比偏低，建议与其他资产组合配置以分散风险。")

                # MA200长期趋势
                if r["price_now"] > r["ma200"]:
                    gap = (r["price_now"] - r["ma200"]) / r["ma200"] * 100
                    lines.append(f"📊 **长期均线**：价格 ${r['price_now']:.2f} 高于200日均线 ${r['ma200']:.2f}（+{gap:.1f}%），处于长期牛市结构，是长期投资的基本条件。")
                else:
                    gap = (r["ma200"] - r["price_now"]) / r["ma200"] * 100
                    lines.append(f"📊 **长期均线**：价格 ${r['price_now']:.2f} 低于200日均线 ${r['ma200']:.2f}（-{gap:.1f}%），处于长期熊市结构，长期投资需谨慎，等待价格收复MA200后再考虑介入。")

                # 基本面
                if r["pe"] and r["pe"] > 0:
                    if r["pe"] < 15:
                        lines.append(f"💼 **估值**：P/E={r['pe']:.1f}x，估值偏低，具备较强安全边际，适合价值型长期投资者。")
                    elif r["pe"] < 30:
                        lines.append(f"💼 **估值**：P/E={r['pe']:.1f}x，估值合理，成长与价值兼顾。")
                    else:
                        lines.append(f"💼 **估值**：P/E={r['pe']:.1f}x，估值偏高，长期回报率可能受到压制，需依赖高增长兑现。")

                # Beta
                if r["beta"]:
                    if r["beta"] < 0.8:
                        lines.append(f"🛡️ **波动性**：Beta={r['beta']:.2f}，低于市场平均，防御性强，适合稳健型长期投资者。")
                    elif r["beta"] > 1.5:
                        lines.append(f"🎢 **波动性**：Beta={r['beta']:.2f}，高于市场平均，波动较大，长期持有需承受较大回撤，适合风险承受能力强的投资者。")
                    else:
                        lines.append(f"📌 **波动性**：Beta={r['beta']:.2f}，与市场波动基本一致。")

                # 斐波那契长期支撑
                lines.append(f"🎯 **关键价位**：长期投资者应关注斐波那契0.618支撑位 ${r['fib_levels']['0.618']:.2f}（强支撑），若价格跌破需重新评估持仓。理想建仓区间为 ${r['fib_levels']['0.618']:.2f}—${r['fib_levels']['0.500']:.2f}。")

                # 结论
                if r["lt_score"] >= 60:
                    lines.append(f"**✅ 长期投资结论**：建议以分批定投方式建立长期仓位，止损设于 ${r['stop_loss']:.2f}（1.5x ATR），目标持有周期12-36个月。")
                elif r["lt_score"] >= 45:
                    lines.append("**⚖️ 长期投资结论**：建议小仓位试探性介入，密切关注基本面变化，若业绩持续改善可逐步加仓。")
                else:
                    lines.append("**❌ 长期投资结论**：当前不具备长期投资价值，建议等待趋势反转（价格站稳MA200）且OBV转为净流入后再重新评估。")

                return lines

            lt_lines = gen_lt_analysis(result)
            for line in lt_lines:
                st.markdown(
                    f'<div style="background:{lt_bg};border-left:3px solid {lt_border};'
                    f'padding:10px 16px;border-radius:6px;margin-bottom:6px;'
                    f'font-size:14px;line-height:1.7">{line}</div>',
                    unsafe_allow_html=True
                )

            st.divider()

            # ── 静态数据提示 ──
            if result.get("static"):
                st.info("📊 **SPCX（SpaceX）** 于2026年6月12日上市，yfinance历史数据尚未完全同步。以下为基于公开市场信息的静态分析，图表将在数据同步后自动更新（通常3-5个交易日）。")

            # ── 价格图表 + 技术指标 ──
            hist = result.get("hist")
            if hist is None:
                st.subheader("📈 价格走势")
                st.warning("图表数据同步中，请3-5个交易日后再查看完整技术图表。")
            else:
                close = hist["Close"]
                ma20_s  = close.rolling(20).mean()
                ma50_s  = close.rolling(50).mean()
                bb_mid_s = close.rolling(20).mean()
                bb_std_s = close.rolling(20).std()

            if hist is not None:
                try:
                    from plotly.subplots import make_subplots as _ms
                    _fp = _ms(rows=3, cols=1, shared_xaxes=True,
                              row_heights=[0.6,0.2,0.2],
                              subplot_titles=("价格走势+均线+布林带","RSI(14)","成交量"),
                              vertical_spacing=0.06)
                    _fp.add_trace(go.Candlestick(
                        x=hist.index,open=hist["Open"],high=hist["High"],
                        low=hist["Low"],close=hist["Close"],name="K线",
                        increasing_line_color="#1D9E75",decreasing_line_color="#A32D2D",
                        showlegend=False),row=1,col=1)
                    _close=hist["Close"]
                    _ma20=_close.rolling(20).mean()
                    _ma50=_close.rolling(min(50,len(_close))).mean()
                    _bb_m=_close.rolling(20).mean()
                    _bb_s=_close.rolling(20).std()
                    _fp.add_trace(go.Scatter(x=hist.index,y=_ma20,name="MA20",
                        line=dict(color="#534AB7",width=1.5)),row=1,col=1)
                    _fp.add_trace(go.Scatter(x=hist.index,y=_ma50,name="MA50",
                        line=dict(color="#D85A30",width=1.5)),row=1,col=1)
                    _fp.add_trace(go.Scatter(x=hist.index,y=_bb_m+2*_bb_s,name="布林上轨",
                        line=dict(color="gray",width=1,dash="dot"),showlegend=False),row=1,col=1)
                    _fp.add_trace(go.Scatter(x=hist.index,y=_bb_m-2*_bb_s,name="布林下轨",
                        line=dict(color="gray",width=1,dash="dot"),
                        fill="tonexty",fillcolor="rgba(128,128,128,0.05)",showlegend=False),row=1,col=1)
                    _d=_close.diff()
                    _g=_d.clip(lower=0).rolling(14).mean()
                    _l=(-_d.clip(upper=0)).rolling(14).mean()
                    _rsi=100-100/(1+_g/_l.replace(0,1e-9))
                    _fp.add_trace(go.Scatter(x=hist.index,y=_rsi,name="RSI",
                        line=dict(color="#534AB7",width=1.5)),row=2,col=1)
                    _fp.add_hline(y=70,line_dash="dot",line_color="red",row=2,col=1)
                    _fp.add_hline(y=30,line_dash="dot",line_color="green",row=2,col=1)
                    _bc=["#1D9E75" if c>=o else "#A32D2D"
                         for c,o in zip(hist["Close"],hist["Open"])]
                    _fp.add_trace(go.Bar(x=hist.index,y=hist["Volume"],name="成交量",
                        marker_color=_bc),row=3,col=1)
                    _fp.update_layout(height=620,plot_bgcolor="#fafafa",
                        xaxis_rangeslider_visible=False,showlegend=True,
                        legend=dict(orientation="h",y=-0.08))
                    glass_chart(_fp, use_container_width=True)
                except Exception as _e:
                    st.warning(f"图表加载失败：{_e}")

            # ── 信号列表 ──
            st.subheader("📋 技术信号详情")
            sig_col1, sig_col2 = st.columns(2)
            for i, (icon, title, desc) in enumerate(result["signals"]):
                col = sig_col1 if i % 2 == 0 else sig_col2
                col.markdown(f"**{icon} {title}**  \n{desc}")

            # ── 基本面 ──
            # ── 基本面数据 + 解释 ──
            st.subheader("📊 基本面数据")

            def fmt_explain(label, value, explain, good_range, interpret):
                """渲染一个指标卡片+解释"""
                return f"""
                <div style="border:1px solid #e8e8e8;border-radius:10px;padding:14px 16px;
                            background:white;height:100%">
                    <div style="font-size:12px;color:#888;margin-bottom:4px">{label}</div>
                    <div style="font-size:22px;font-weight:700;color:#1a1a1a;margin-bottom:6px">{value}</div>
                    <div style="font-size:11px;color:#555;margin-bottom:4px">
                        📌 <b>正常范围</b>：{good_range}
                    </div>
                    <div style="font-size:12px;color:#333;line-height:1.5">{interpret}</div>
                </div>"""

            # 计算各指标的解释
            pe_v   = result["pe"]
            fpe_v  = result["fwd_pe"]
            pb_v   = result["pb"]
            beta_v = result["beta"]

            pe_str   = f"{pe_v:.1f}x"   if pe_v   else "N/A"
            fpe_str  = f"{fpe_v:.1f}x"  if fpe_v  else "N/A"
            pb_str   = f"{pb_v:.2f}x"   if pb_v   else "N/A"
            beta_str = f"{beta_v:.2f}"  if beta_v  else "N/A"

            def pe_interpret(v):
                if not v: return "数据不足，无法判断。"
                if v < 0:   return "🔴 公司当前亏损，P/E为负，需关注扭亏时间表。"
                if v < 10:  return "🟢 估值极低，可能被低估，或市场对前景悲观。"
                if v < 20:  return "🟢 估值合理，属于价值投资区间，性价比高。"
                if v < 35:  return "🟡 估值偏高，需要业绩增长支撑，适合成长股。"
                return        "🔴 估值较贵，市场已充分定价未来增长，追高风险大。"

            def fpe_interpret(v):
                if not v: return "数据不足。"
                if v < 15:  return "🟢 按未来盈利计算估值便宜，市场预期改善空间大。"
                if v < 25:  return "🟡 合理，反映市场对未来盈利的温和预期。"
                return        "🔴 市场对未来盈利预期很高，若业绩不达预期将大幅回调。"

            def pb_interpret(v):
                if not v: return "数据不足。"
                if v < 1:   return "🟢 股价低于账面价值，资产被严重低估（银行/地产常见）。"
                if v < 3:   return "🟢 估值合理，资产质量有保障。"
                if v < 8:   return "🟡 品牌/技术溢价，科技股常见，需关注ROE是否匹配。"
                return        "🔴 高溢价，完全依赖无形资产和未来增长，回撤风险高。"

            def beta_interpret(v):
                if not v: return "数据不足。"
                if v < 0.5: return "🟢 极低波动，防御性强（公用事业/消费必需品），适合保守投资者。"
                if v < 1.0: return "🟢 低于市场波动，相对稳健，下跌时跌得少。"
                if v < 1.5: return "🟡 与市场同步，市场涨它涨，市场跌它跌。"
                if v < 2.0: return "🟠 高波动，市场上涨时涨幅更大，但下跌时跌幅也更大。"
                return        "🔴 极高波动，适合短线交易者，长期持有心理压力大。"

            fc1, fc2, fc3, fc4 = st.columns(4)
            with fc1:
                st.markdown(fmt_explain(
                    "P/E（市盈率）", pe_str,
                    "解释：你花多少钱买1元利润",
                    "价值股10-20x，成长股20-40x",
                    pe_interpret(pe_v)
                ), unsafe_allow_html=True)
            with fc2:
                st.markdown(fmt_explain(
                    "Forward P/E（预期市盈率）", fpe_str,
                    "解释：按未来12个月预期利润计算",
                    "低于当前P/E = 盈利预期改善",
                    fpe_interpret(fpe_v)
                ), unsafe_allow_html=True)
            with fc3:
                st.markdown(fmt_explain(
                    "P/B（市净率）", pb_str,
                    "解释：股价相对账面净资产的倍数",
                    "传统行业<2x，科技股3-10x正常",
                    pb_interpret(pb_v)
                ), unsafe_allow_html=True)
            with fc4:
                st.markdown(fmt_explain(
                    "Beta（市场敏感度）", beta_str,
                    "解释：相对大盘的波动幅度",
                    "<1=防御，=1=同步，>1=进攻",
                    beta_interpret(beta_v)
                ), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if result["target_analyst"]:
                upside = (result["target_analyst"] - result["price_now"]) / result["price_now"] * 100
                ua_color = "#0F6E56" if upside >= 0 else "#A32D2D"
                st.markdown(
                    f'<div style="background:#EEF4FF;border-left:4px solid #185FA5;'
                    f'padding:12px 16px;border-radius:8px;font-size:13px">'
                    f'🎯 <b>华尔街分析师平均目标价：${result["target_analyst"]:.2f}</b>'
                    f'&nbsp;&nbsp;较现价 <span style="color:{ua_color};font-weight:700">'
                    f'{"+"+str(round(upside,1)) if upside>=0 else round(upside,1)}%</span>'
                    f'&nbsp;&nbsp;|&nbsp;&nbsp;解释：这是华尔街各大投行分析师对该股未来12个月目标价的平均值，'
                    f'高于现价说明分析师整体看涨，低于现价说明分析师整体看空。</div>',
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── 财报分析 ──
            st.subheader("📋 财报与季报自动分析")
            st.caption("数据来自雅虎财经，自动分析最近四个季度营收/利润趋势并预测未来走势")

            @st.cache_data(ttl=3600)
            def fetch_financials(tk):
                try:
                    import yfinance as yf
                    import pandas as pd
                    t = yf.Ticker(tk)

                    # 季度财报
                    q_income = t.quarterly_income_stmt
                    q_balance = t.quarterly_balance_sheet
                    q_cashflow = t.quarterly_cashflow
                    annual_income = t.income_stmt

                    return {
                        "q_income":    q_income,
                        "q_balance":   q_balance,
                        "q_cashflow":  q_cashflow,
                        "annual":      annual_income,
                        "info":        t.info,
                    }
                except Exception as e:
                    return {"error": str(e)}

            fin_data = fetch_financials(result["ticker"])

            if "error" in fin_data:
                st.warning(f"财报数据暂时无法获取：{fin_data['error']}")
            else:
                fin_tabs = st.tabs(["📅 季度营收趋势", "💰 盈利能力", "🏦 资产负债", "💵 现金流", "📆 年报对比", "🔮 多情景预测"])

                # ── 季度营收 ──
                with fin_tabs[0]:
                    try:
                        qi = fin_data["q_income"]
                        if qi is not None and not qi.empty:
                            rev_row = None
                            for k in ["Total Revenue","Revenue","Net Revenue"]:
                                if k in qi.index:
                                    rev_row = qi.loc[k]
                                    break
                            if rev_row is not None:
                                rev_row = rev_row.dropna().sort_index()
                                cols_q = [str(c)[:10] for c in rev_row.index]
                                vals_q = [v/1e6 for v in rev_row.values]

                                # 趋势判断
                                if len(vals_q) >= 2:
                                    trend_pct = (vals_q[-1] - vals_q[0]) / abs(vals_q[0]) * 100 if vals_q[0] != 0 else 0
                                    qoq = (vals_q[-1] - vals_q[-2]) / abs(vals_q[-2]) * 100 if vals_q[-2] != 0 else 0
                                else:
                                    trend_pct = 0; qoq = 0

                                fig_rev = go.Figure()
                                fig_rev.add_trace(go.Bar(
                                    x=cols_q, y=vals_q,
                                    marker_color=["#1D9E75" if v >= vals_q[0] else "#E24B4A" for v in vals_q],
                                    text=[f"${v:.0f}M" for v in vals_q],
                                    textposition="outside",
                                    name="季度营收",
                                ))
                                # 趋势线
                                import numpy as np_f
                                if len(vals_q) >= 3:
                                    z = np_f.polyfit(range(len(vals_q)), vals_q, 1)
                                    trend_line = np_f.poly1d(z)(range(len(vals_q)))
                                    fig_rev.add_trace(go.Scatter(
                                        x=cols_q, y=trend_line, mode="lines",
                                        line=dict(color="#534AB7", width=2, dash="dash"),
                                        name="趋势线",
                                    ))
                                fig_rev.update_layout(
                                    height=380, plot_bgcolor="#fafafa",
                                    title=f"季度营收趋势（百万美元）",
                                    yaxis_title="营收 ($M)",
                                    margin=dict(t=50,b=40,l=60,r=40),
                                )
                                glass_chart(fig_rev, use_container_width=True)

                                # 自动解读
                                t_color = "#0F6E56" if trend_pct >= 0 else "#A32D2D"
                                q_color = "#0F6E56" if qoq >= 0 else "#A32D2D"
                                st.markdown(
                                    f'<div style="background:#F8F9FA;border-radius:8px;padding:12px 16px;font-size:13px;line-height:1.8">'
                                    f'📊 <b>营收趋势解读</b><br>'
                                    f'• 最近一季营收：<b>${vals_q[-1]:.0f}M</b>，环比上季 <span style="color:{q_color};font-weight:600">{"+"+str(round(qoq,1)) if qoq>=0 else round(qoq,1)}%</span><br>'
                                    f'• 过去{len(vals_q)}个季度整体趋势：<span style="color:{t_color};font-weight:600">{"增长" if trend_pct>=0 else "下滑"} {abs(trend_pct):.1f}%</span><br>'
                                    f'• {"🟢 营收持续增长，业务扩张信号良好，支持股价长期上行。" if trend_pct > 10 else "🟡 营收增长平稳，业务较为稳定，适合稳健型投资者。" if trend_pct >= 0 else "🔴 营收出现下滑趋势，需关注公司是否有明确的反转计划。"}'
                                    f'</div>', unsafe_allow_html=True
                                )
                            else:
                                st.info("该公司暂无季度营收数据。")
                    except Exception as e:
                        st.warning(f"季度营收数据解析失败：{e}")

                # ── 盈利能力 ──
                with fin_tabs[1]:
                    try:
                        qi = fin_data["q_income"]
                        if qi is not None and not qi.empty:
                            metrics_map = {
                                "毛利润": ["Gross Profit"],
                                "营业利润": ["Operating Income","EBIT"],
                                "净利润": ["Net Income","Net Income Common Stockholders"],
                            }
                            fig_profit = go.Figure()
                            colors_p = {"毛利润":"#1D9E75","营业利润":"#534AB7","净利润":"#185FA5"}
                            found_any = False
                            for label, keys in metrics_map.items():
                                for k in keys:
                                    if k in qi.index:
                                        row = qi.loc[k].dropna().sort_index()
                                        cols_p = [str(c)[:10] for c in row.index]
                                        vals_p = [v/1e6 for v in row.values]
                                        fig_profit.add_trace(go.Bar(
                                            x=cols_p, y=vals_p,
                                            name=label,
                                            marker_color=colors_p.get(label,"#888"),
                                        ))
                                        found_any = True
                                        break
                            if found_any:
                                fig_profit.update_layout(
                                    height=380, plot_bgcolor="#fafafa",
                                    title="季度盈利能力（百万美元）",
                                    yaxis_title="金额 ($M)",
                                    barmode="group",
                                    legend=dict(orientation="h", y=1.1),
                                    margin=dict(t=60,b=40,l=60,r=40),
                                )
                                glass_chart(fig_profit, use_container_width=True)

                                # 毛利率解读
                                for k in ["Gross Profit"]:
                                    if k in qi.index:
                                        gp = qi.loc[k].dropna().sort_index()
                                        rev_keys = ["Total Revenue","Revenue"]
                                        for rk in rev_keys:
                                            if rk in qi.index:
                                                rv = qi.loc[rk].dropna().sort_index()
                                                common = gp.index.intersection(rv.index)
                                                if len(common) > 0:
                                                    margin = float(gp[common[-1]] / rv[common[-1]] * 100)
                                                    m_color = "#0F6E56" if margin > 40 else "#BA7517" if margin > 20 else "#A32D2D"
                                                    st.markdown(
                                                        f'<div style="background:#F8F9FA;border-radius:8px;padding:12px 16px;font-size:13px;line-height:1.8">'
                                                        f'💰 <b>盈利能力解读</b><br>'
                                                        f'• 最新季度毛利率：<span style="color:{m_color};font-weight:700">{margin:.1f}%</span><br>'
                                                        f'• {"🟢 毛利率超过40%，说明产品定价能力强，竞争护城河宽（科技/药品常见）。" if margin>40 else "🟡 毛利率20-40%，盈利能力中等，需关注成本控制。" if margin>20 else "🔴 毛利率低于20%，盈利空间薄，对成本上升非常敏感（零售/制造常见）。"}'
                                                        f'</div>', unsafe_allow_html=True
                                                    )
                                                break
                            else:
                                st.info("暂无盈利数据。")
                    except Exception as e:
                        st.warning(f"盈利数据解析失败：{e}")

                # ── 资产负债 ──
                with fin_tabs[2]:
                    try:
                        qb = fin_data["q_balance"]
                        if qb is not None and not qb.empty:
                            # 现金 vs 负债
                            cash_keys = ["Cash And Cash Equivalents","Cash Cash Equivalents And Short Term Investments"]
                            debt_keys = ["Total Debt","Long Term Debt"]
                            cash_row = None; debt_row = None
                            for k in cash_keys:
                                if k in qb.index: cash_row = qb.loc[k].dropna().sort_index(); break
                            for k in debt_keys:
                                if k in qb.index: debt_row = qb.loc[k].dropna().sort_index(); break

                            if cash_row is not None and debt_row is not None:
                                common_idx = cash_row.index.intersection(debt_row.index)
                                if len(common_idx) > 0:
                                    cols_b = [str(c)[:10] for c in common_idx]
                                    cash_v = [cash_row[c]/1e9 for c in common_idx]
                                    debt_v = [debt_row[c]/1e9 for c in common_idx]
                                    net_cash = [c-d for c,d in zip(cash_v,debt_v)]

                                    fig_bal = go.Figure()
                                    fig_bal.add_trace(go.Bar(x=cols_b, y=cash_v, name="现金及等价物",
                                                             marker_color="#1D9E75"))
                                    fig_bal.add_trace(go.Bar(x=cols_b, y=[-d for d in debt_v],
                                                             name="总债务（负值）", marker_color="#E24B4A"))
                                    fig_bal.add_trace(go.Scatter(x=cols_b, y=net_cash, mode="lines+markers",
                                                                 name="净现金", line=dict(color="#534AB7",width=2)))
                                    fig_bal.add_hline(y=0, line_color="#888", line_width=1)
                                    fig_bal.update_layout(
                                        height=380, plot_bgcolor="#fafafa",
                                        title="现金 vs 债务（十亿美元）",
                                        yaxis_title="金额 ($B)",
                                        barmode="relative",
                                        legend=dict(orientation="h", y=1.1),
                                        margin=dict(t=60,b=40,l=60,r=40),
                                    )
                                    glass_chart(fig_bal, use_container_width=True)

                                    latest_net = net_cash[-1]
                                    nc_color = "#0F6E56" if latest_net > 0 else "#A32D2D"
                                    st.markdown(
                                        f'<div style="background:#F8F9FA;border-radius:8px;padding:12px 16px;font-size:13px;line-height:1.8">'
                                        f'🏦 <b>资产负债解读</b><br>'
                                        f'• 最新净现金头寸：<span style="color:{nc_color};font-weight:700">${latest_net:.2f}B</span>（现金减去所有债务）<br>'
                                        f'• {"🟢 净现金为正，公司无债务压力，财务健康，抗风险能力强。" if latest_net>0 else "🔴 净现金为负，公司负债大于现金，需关注债务到期和再融资风险。"}'
                                        f'</div>', unsafe_allow_html=True
                                    )
                    except Exception as e:
                        st.warning(f"资产负债数据解析失败：{e}")

                # ── 现金流 ──
                with fin_tabs[3]:
                    try:
                        qcf = fin_data["q_cashflow"]
                        if qcf is not None and not qcf.empty:
                            ocf_keys = ["Operating Cash Flow","Cash From Operations"]
                            fcf_keys = ["Free Cash Flow","Capital Expenditure"]
                            ocf_row = None
                            for k in ocf_keys:
                                if k in qcf.index: ocf_row = qcf.loc[k].dropna().sort_index(); break

                            if ocf_row is not None:
                                cols_cf = [str(c)[:10] for c in ocf_row.index]
                                ocf_v   = [v/1e6 for v in ocf_row.values]
                                bar_clr = ["#1D9E75" if v >= 0 else "#E24B4A" for v in ocf_v]

                                fig_cf = go.Figure()
                                fig_cf.add_trace(go.Bar(
                                    x=cols_cf, y=ocf_v,
                                    marker_color=bar_clr,
                                    text=[f"${v:.0f}M" for v in ocf_v],
                                    textposition="outside",
                                    name="经营现金流",
                                ))
                                fig_cf.add_hline(y=0, line_color="#888", line_width=1)
                                fig_cf.update_layout(
                                    height=380, plot_bgcolor="#fafafa",
                                    title="季度经营现金流（百万美元）",
                                    yaxis_title="现金流 ($M)",
                                    margin=dict(t=50,b=40,l=60,r=40),
                                )
                                glass_chart(fig_cf, use_container_width=True)

                                pos_count = sum(1 for v in ocf_v if v > 0)
                                cf_color = "#0F6E56" if pos_count >= len(ocf_v)*0.75 else "#A32D2D"
                                st.markdown(
                                    f'<div style="background:#F8F9FA;border-radius:8px;padding:12px 16px;font-size:13px;line-height:1.8">'
                                    f'💵 <b>现金流解读</b><br>'
                                    f'• 最近{len(ocf_v)}季中有 <span style="color:{cf_color};font-weight:700">{pos_count}季</span> 经营现金流为正<br>'
                                    f'• 现金流为正 = 公司真实赚钱，不依赖融资输血<br>'
                                    f'• {"🟢 持续正向现金流，公司自我造血能力强，财务非常健康。" if pos_count==len(ocf_v) else "🟡 现金流偶有负值，关注是否为一次性投资支出还是持续亏损。" if pos_count>=len(ocf_v)*0.5 else "🔴 多季现金流为负，公司需依赖外部融资维持运营，风险较高。"}'
                                    f'</div>', unsafe_allow_html=True
                                )
                    except Exception as e:
                        st.warning(f"现金流数据解析失败：{e}")

                # ── 年报对比 ──
                with fin_tabs[4]:
                    try:
                        ai = fin_data["annual"]
                        if ai is not None and not ai.empty:
                            rev_row_a = None
                            for k in ["Total Revenue","Revenue"]:
                                if k in ai.index: rev_row_a = ai.loc[k].dropna().sort_index(); break

                            ni_row_a = None
                            for k in ["Net Income","Net Income Common Stockholders"]:
                                if k in ai.index: ni_row_a = ai.loc[k].dropna().sort_index(); break

                            gp_row_a = None
                            for k in ["Gross Profit"]:
                                if k in ai.index: gp_row_a = ai.loc[k].dropna().sort_index(); break

                            if rev_row_a is not None:
                                years    = [str(c)[:4] for c in rev_row_a.index]
                                rev_vals = [v/1e9 for v in rev_row_a.values]

                                fig_ann = go.Figure()
                                fig_ann.add_trace(go.Bar(
                                    x=years, y=rev_vals,
                                    name="年度营收", marker_color="#185FA5",
                                    text=[f"${v:.2f}B" for v in rev_vals],
                                    textposition="outside",
                                ))
                                if ni_row_a is not None:
                                    ni_years = [str(c)[:4] for c in ni_row_a.index]
                                    ni_vals  = [v/1e9 for v in ni_row_a.values]
                                    fig_ann.add_trace(go.Bar(
                                        x=ni_years, y=ni_vals,
                                        name="年度净利润",
                                        marker_color=["#1D9E75" if v>=0 else "#E24B4A" for v in ni_vals],
                                        text=[f"${v:.2f}B" for v in ni_vals],
                                        textposition="outside",
                                    ))
                                if gp_row_a is not None:
                                    gp_years = [str(c)[:4] for c in gp_row_a.index]
                                    gp_vals  = [v/1e9 for v in gp_row_a.values]
                                    fig_ann.add_trace(go.Scatter(
                                        x=gp_years, y=gp_vals,
                                        name="年度毛利润", mode="lines+markers",
                                        line=dict(color="#F5A623", width=2.5),
                                        marker=dict(size=8),
                                    ))

                                fig_ann.update_layout(
                                    height=400, plot_bgcolor="#fafafa",
                                    title="年度财报对比（十亿美元）",
                                    yaxis_title="金额 ($B)",
                                    barmode="group",
                                    legend=dict(orientation="h", y=1.1),
                                    margin=dict(t=60,b=40,l=60,r=40),
                                )
                                glass_chart(fig_ann, use_container_width=True)

                                # 年报自动解读
                                if len(rev_vals) >= 2:
                                    yoy_rev = (rev_vals[-1] - rev_vals[-2]) / abs(rev_vals[-2]) * 100 if rev_vals[-2] != 0 else 0
                                    cagr    = ((rev_vals[-1]/rev_vals[0])**(1/max(1,len(rev_vals)-1))-1)*100 if rev_vals[0]>0 else 0
                                else:
                                    yoy_rev = 0; cagr = 0

                                ni_latest = ni_row_a.iloc[-1]/1e9 if ni_row_a is not None and len(ni_row_a)>0 else None
                                rev_latest = rev_vals[-1] if rev_vals else 0
                                net_margin = (ni_latest/rev_latest*100) if (ni_latest and rev_latest) else None

                                lines_ann = []
                                lines_ann.append(f"📆 <b>年报综合解读</b>")
                                lines_ann.append(f"• 最新财年营收：<b>${rev_latest:.2f}B</b>，同比 {'<span style="color:#0F6E56">+' if yoy_rev>=0 else '<span style="color:#A32D2D">'}{yoy_rev:.1f}%</span>")
                                lines_ann.append(f"• {len(rev_vals)}年复合增长率(CAGR)：<b>{'<span style="color:#0F6E56">+' if cagr>=0 else '<span style="color:#A32D2D">'}{cagr:.1f}%</span></b>")
                                if net_margin is not None:
                                    color_m = "#0F6E56" if net_margin > 15 else "#BA7517" if net_margin > 0 else "#A32D2D"
                                    lines_ann.append(f"• 净利润率：<span style='color:{color_m};font-weight:700'>{net_margin:.1f}%</span>（{'🟢 盈利能力强' if net_margin>15 else '🟡 盈利能力中等' if net_margin>0 else '🔴 仍在亏损'}）")
                                if cagr > 15:
                                    lines_ann.append("• 🟢 <b>高速增长型公司</b>：营收CAGR超过15%，属于高成长股，适合成长型投资者，但需承受较高估值。")
                                elif cagr > 5:
                                    lines_ann.append("• 🟡 <b>稳健增长型公司</b>：营收增速稳定，现金流可预期，适合稳健型投资者。")
                                elif cagr >= 0:
                                    lines_ann.append("• 🟠 <b>成熟期公司</b>：营收增长放缓，需关注分红、回购等股东回报政策。")
                                else:
                                    lines_ann.append("• 🔴 <b>营收萎缩</b>：长期营收下滑，需深入了解公司转型计划和竞争壁垒是否仍存在。")

                                st.markdown(
                                    '<div style="background:#F8F9FA;border-radius:8px;padding:14px 16px;'
                                    'font-size:13px;line-height:2">'
                                    + "<br>".join(lines_ann) +
                                    '</div>', unsafe_allow_html=True
                                )
                        else:
                            st.info("暂无年度财报数据。")
                    except Exception as e:
                        st.warning(f"年报数据解析失败：{e}")

                # ── 多情景预测 ──
                with fin_tabs[5]:
                    st.markdown("**基于历史营收增长率，预测未来4个季度三种情景**")
                    try:
                        qi = fin_data["q_income"]
                        if qi is not None and not qi.empty:
                            rev_row = None
                            for k in ["Total Revenue","Revenue"]:
                                if k in qi.index: rev_row = qi.loc[k].dropna().sort_index(); break

                            if rev_row is not None and len(rev_row) >= 2:
                                import numpy as np_p
                                rev_vals = [v/1e6 for v in rev_row.values]
                                rev_cols = [str(c)[:10] for c in rev_row.index]

                                # 计算历史平均增长率
                                if len(rev_vals) >= 4:
                                    qoq_rates = [(rev_vals[i]-rev_vals[i-1])/abs(rev_vals[i-1])
                                                 for i in range(1,len(rev_vals)) if rev_vals[i-1]!=0]
                                    avg_growth = float(np_p.mean(qoq_rates)) if qoq_rates else 0.03
                                else:
                                    avg_growth = (rev_vals[-1]/rev_vals[0]-1)/(len(rev_vals)-1) if rev_vals[0]!=0 else 0.03

                                # 三种情景增长率
                                bull_g  = avg_growth * 1.5 + 0.02
                                base_g  = avg_growth
                                bear_g  = avg_growth * 0.5 - 0.02

                                import pandas as _pd2
                                from datetime import timedelta

                                last_rev = rev_vals[-1]

                                # 用真实日期做x轴，让历史柱和预测线在同一轴上连接
                                last_date = rev_row.index[-1]
                                # 推算未来4个季度日期（每季+91天）
                                future_dates = [last_date + timedelta(days=91*(i+1)) for i in range(4)]
                                future_labels = [str(d)[:10] for d in future_dates]

                                bull_fwd  = [last_rev * (1+bull_g)**(i+1) for i in range(4)]
                                base_fwd  = [last_rev * (1+base_g)**(i+1) for i in range(4)]
                                bear_fwd  = [last_rev * (1+bear_g)**(i+1) for i in range(4)]

                                fig_fwd = go.Figure()

                                # 历史柱状图
                                fig_fwd.add_trace(go.Bar(
                                    x=rev_cols, y=rev_vals,
                                    name="历史营收",
                                    marker_color="#534AB7",
                                    marker_line_color="#3C3489",
                                    marker_line_width=1,
                                ))

                                # 预测起点（最后一个历史点）+ 未来4季
                                x_pred = [rev_cols[-1]] + future_labels

                                fig_fwd.add_trace(go.Scatter(
                                    x=x_pred, y=[last_rev] + bull_fwd,
                                    mode="lines+markers+text",
                                    name="🚀 乐观情景",
                                    line=dict(color="#1D9E75", width=2.5),
                                    marker=dict(size=10, color="#1D9E75",
                                                line=dict(color="white", width=2)),
                                    text=[""] + [f"${v:.0f}M" for v in bull_fwd],
                                    textposition="top center",
                                    textfont=dict(size=10, color="#1D9E75"),
                                ))
                                fig_fwd.add_trace(go.Scatter(
                                    x=x_pred, y=[last_rev] + base_fwd,
                                    mode="lines+markers+text",
                                    name="📊 基准情景",
                                    line=dict(color="#F5A623", width=2.5),
                                    marker=dict(size=10, color="#F5A623",
                                                line=dict(color="white", width=2)),
                                    text=[""] + [f"${v:.0f}M" for v in base_fwd],
                                    textposition="top center",
                                    textfont=dict(size=10, color="#BA7517"),
                                ))
                                fig_fwd.add_trace(go.Scatter(
                                    x=x_pred, y=[last_rev] + bear_fwd,
                                    mode="lines+markers+text",
                                    name="🐻 悲观情景",
                                    line=dict(color="#E24B4A", width=2.5),
                                    marker=dict(size=10, color="#E24B4A",
                                                line=dict(color="white", width=2)),
                                    text=[""] + [f"${v:.0f}M" for v in bear_fwd],
                                    textposition="bottom center",
                                    textfont=dict(size=10, color="#A32D2D"),
                                ))

                                # 预测区间背景
                                fig_fwd.add_vrect(
                                    x0=rev_cols[-1], x1=future_labels[-1],
                                    fillcolor="rgba(83,74,183,0.06)",
                                    line_width=0,
                                )
                                # 分界线
                                fig_fwd.add_vline(
                                    x=rev_cols[-1],
                                    line_dash="dash", line_color="#888", line_width=1.5,
                                    annotation_text=" ← 历史  预测 →",
                                    annotation_position="top",
                                    annotation_font=dict(size=11, color="#555"),
                                )

                                fig_fwd.update_layout(
                                    height=460, plot_bgcolor="#fafafa",
                                    paper_bgcolor="white",
                                    title=dict(
                                        text="营收预测：历史趋势 + 未来4季度三情景",
                                        font=dict(size=15),
                                    ),
                                    yaxis_title="营收 ($M)",
                                    xaxis=dict(showgrid=True, gridcolor="#eeeeee"),
                                    yaxis=dict(showgrid=True, gridcolor="#eeeeee"),
                                    legend=dict(orientation="h", y=1.08, x=0),
                                    margin=dict(t=70, b=50, l=60, r=40),
                                    hovermode="x unified",
                                )
                                glass_chart(fig_fwd, use_container_width=True)

                                # 预测解读
                                bull_total = sum(bull_fwd); base_total = sum(base_fwd); bear_total = sum(bear_fwd)
                                hist_annual = sum(rev_vals[-4:]) if len(rev_vals)>=4 else sum(rev_vals)*4/len(rev_vals)

                                st.markdown(f"""
                                <div style="background:#F8F9FA;border-radius:8px;padding:14px 16px;font-size:13px;line-height:2">
                                <b>🔮 未来4季度营收预测汇总</b><br>
                                🚀 <b>乐观情景</b>（增长率 +{bull_g*100:.1f}%/季）：未来4季合计 <b style="color:#1D9E75">${bull_total:.0f}M</b><br>
                                📊 <b>基准情景</b>（增长率 {base_g*100:+.1f}%/季）：未来4季合计 <b style="color:#F5A623">${base_total:.0f}M</b><br>
                                🐻 <b>悲观情景</b>（增长率 {bear_g*100:.1f}%/季）：未来4季合计 <b style="color:#E24B4A">${bear_total:.0f}M</b><br>
                                <br>
                                📌 <b>说明</b>：预测基于历史季均增长率（{avg_growth*100:+.1f}%），乐观=历史增速×1.5+2%，悲观=历史增速×0.5-2%。
                                实际结果受宏观环境、行业竞争、管理层决策等多重因素影响，预测仅供参考。
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.info("营收数据不足，无法生成预测。")
                    except Exception as e:
                        st.warning(f"预测生成失败：{e}")

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

            # ── 宏观+微观联动分析 ──────────────────────────────────────────
            st.divider()
            st.subheader("🌐 宏观环境 × 个股影响分析")
            st.caption("结合当前宏观经济指标和新闻动态，分析对本股票的具体影响")

            macro_sig  = st.session_state.get("macro_signals", [])
            macro_sc   = st.session_state.get("macro_score", None)
            macro_out  = st.session_state.get("macro_outlook", None)
            macro_sum  = st.session_state.get("macro_summary", "")
            news_sc    = st.session_state.get("news_score", 0)
            news_items = st.session_state.get("news_list", [])

            if macro_sc is None:
                st.info("💡 请先前往「🌐 宏观分析」Tab 加载宏观数据，然后回到此处查看联动分析。")
            else:
                r = result
                sector  = r.get("sector","未知")
                beta    = r.get("beta") or 1.0
                pe      = r.get("pe")

                # 根据股票行业确定宏观敏感度
                sector_macro_map = {
                    "Technology":          ("科技股", "高利率环境压制高估值，降息周期受益最大。AI相关科技股对利率最敏感。"),
                    "Financial Services":  ("金融股", "高利率提升净息差，有利银行盈利；但衰退期贷款违约率上升。"),
                    "Consumer Cyclical":   ("消费股", "就业市场强健时受益；高通胀压制消费者购买力。"),
                    "Healthcare":          ("医疗股", "防御性强，经济周期相关性低，适合衰退环境。"),
                    "Energy":              ("能源股", "与通胀正相关；地缘冲突通常推高油价利好能源股。"),
                    "Real Estate":         ("房地产", "对利率极度敏感，高利率大幅提升融资成本。"),
                    "Communication Services":("传媒股","广告收入与经济周期相关；流媒体对利率敏感度中等。"),
                    "Industrials":         ("工业股", "GDP增长强劲时受益；贸易战和关税直接冲击供应链。"),
                    "Consumer Defensive":  ("必需消费","防御性最强，衰退期表现优于大盘。"),
                    "Utilities":           ("公用事业","高利率时与债券竞争，但现金流稳定。"),
                    "Basic Materials":     ("原材料", "地缘风险和通胀推升原材料价格，周期性强。"),
                }
                s_label, s_desc = sector_macro_map.get(sector, ("其他行业", "宏观敏感度中等。"))

                # 综合宏观+新闻+技术面分数
                combined_score = macro_sc + news_sc * 20
                macro_color = "#0F6E56" if combined_score > 15 else "#BA7517" if combined_score > -5 else "#A32D2D"

                # 展示综合评判
                st.markdown(
                    f'<div style="background:{macro_color};color:white;padding:16px 20px;'
                    f'border-radius:10px;margin-bottom:14px">'
                    f'<div style="font-size:16px;font-weight:700">宏观环境对 {r["ticker"]} 的综合影响</div>'
                    f'<div style="font-size:13px;opacity:0.9;margin-top:6px">'
                    f'宏观评分：{macro_sc:+d} &nbsp;|&nbsp; 新闻情绪：{"正面" if news_sc>0.1 else "负面" if news_sc<-0.1 else "中性"} &nbsp;|&nbsp; 行业：{s_label}'
                    f'</div></div>', unsafe_allow_html=True
                )

                # 行业敏感度分析
                ml1, ml2 = st.columns(2)
                with ml1:
                    st.markdown("**📌 行业宏观敏感度**")
                    st.markdown(
                        f'<div style="background:#F8F9FA;border-radius:8px;padding:12px 14px;'
                        f'font-size:13px;line-height:1.8">'
                        f'<b>{s_label}</b>：{s_desc}</div>',
                        unsafe_allow_html=True
                    )
                    # Beta影响
                    if beta:
                        if beta > 1.5:
                            beta_msg = f"Beta={beta:.2f}，高波动性股票，宏观利空时跌幅可能超过大盘{(beta-1)*100:.0f}%，利好时涨幅也相应放大。"
                        elif beta > 1.0:
                            beta_msg = f"Beta={beta:.2f}，波动性略高于大盘，宏观信号对本股影响被放大。"
                        elif beta > 0.5:
                            beta_msg = f"Beta={beta:.2f}，波动性低于大盘，宏观冲击影响相对温和。"
                        else:
                            beta_msg = f"Beta={beta:.2f}，防御性极强，几乎不受宏观周期影响。"
                        st.markdown(
                            f'<div style="background:#F0F4FF;border-radius:8px;padding:10px 14px;'
                            f'font-size:13px;line-height:1.7;margin-top:8px">'
                            f'⚡ <b>波动敏感度</b>：{beta_msg}</div>',
                            unsafe_allow_html=True
                        )

                with ml2:
                    st.markdown("**📋 关键宏观信号对本股影响**")
                    for icon, title, desc in macro_sig[:4]:
                        bg  = {"🟢":"#E1F5EE","🟡":"#FAEEDA","🟠":"#FDF0EC","🔴":"#FCEBEB"}.get(icon,"#F5F5F5")
                        bdr = {"🟢":"#0F6E56","🟡":"#BA7517","🟠":"#D85A30","🔴":"#A32D2D"}.get(icon,"#999")
                        st.markdown(
                            f'<div style="background:{bg};border-left:3px solid {bdr};'
                            f'padding:8px 12px;border-radius:5px;margin-bottom:6px;font-size:12px">'
                            f'<b>{icon} {title}</b><br>{desc}</div>',
                            unsafe_allow_html=True
                        )

                # 相关新闻（过滤与该股相关的）
                ticker_l = r["ticker"].lower()
                name_l   = r.get("name","").lower()[:10]
                relevant_news = [
                    n for n in news_items
                    if ticker_l in n["title"].lower() or name_l in n["title"].lower()
                ] if news_items else []

                if relevant_news:
                    st.markdown(f"**📰 与 {r['ticker']} 相关的最新新闻**")
                    for n in relevant_news[:3]:
                            st.markdown(f"• {n['title']} _{n['pub']}_")
                elif news_items:
                    st.caption("暂无直接相关新闻，显示行业背景新闻请前往「宏观分析」Tab查看。")

                # 综合操作建议
                st.markdown("**🎯 宏观视角下的操作建议**")
                tech_rating = r["rating"]
                if combined_score > 15 and tech_rating in ("强力买入","买入"):
                    final = ("🚀 强力建议", "#0F6E56",
                             f"技术面{tech_rating} + 宏观环境正面 + {s_label}受益，三重共振。建议积极布局，可适当提高仓位。")
                elif combined_score > 0 and tech_rating in ("强力买入","买入","持有"):
                    final = ("📈 建议买入", "#1D9E75",
                             f"技术面{tech_rating}，宏观中性偏正，{s_label}无明显逆风。建议正常仓位参与。")
                elif combined_score < -15 and tech_rating in ("卖出","强力卖出"):
                    final = ("💥 强烈规避", "#A32D2D",
                             f"技术面{tech_rating} + 宏观环境负面 + {s_label}面临逆风。建议清仓或空仓等待。")
                elif combined_score < 0 and tech_rating in ("卖出","强力卖出","持有"):
                    final = ("📉 建议减仓", "#D85A30",
                             f"技术面{tech_rating}，宏观有逆风，{s_label}面临压力。建议降低仓位至半仓以下。")
                else:
                    final = ("⚖️ 中性持有", "#BA7517",
                             f"技术面{tech_rating}，宏观信号混杂，建议持仓观望，等待更明确信号后再加减仓。")

                st.markdown(
                    f'<div style="background:{final[1]};color:white;padding:14px 18px;'
                    f'border-radius:8px;font-size:14px;line-height:1.8">'
                    f'<b>{final[0]}</b><br>{final[2]}</div>',
                    unsafe_allow_html=True
                )

            st.warning("⚠️ 以上分析基于技术指标及公开财报数据，仅供参考，不构成投资建议。投资有风险，入市需谨慎。")

# ── Tab 7: 我的持仓 ──────────────────────────────────────────────────────────────
with tabs[6]:
    st.subheader("💰 我的持仓")
    st.caption("记录你的真实持仓（含成本价），自动分析盈亏原因、长期投资前景与赛道潜力 · 支持股票/ETF/加密货币/大宗商品期货")

    if "holdings" not in st.session_state:
        st.session_state["holdings"] = [
            {"ticker": "NVDA",    "qty": 10.0,  "cost": 120.0,   "ccy": "USD 🇺🇸"},
            {"ticker": "BTC-USD", "qty": 0.05,  "cost": 60000.0, "ccy": "USD 🇺🇸"},
        ]
    # 兼容旧版没有货币字段的持仓数据
    for _pos in st.session_state["holdings"]:
        _pos.setdefault("ccy", "USD 🇺🇸")

    st.markdown("**添加/编辑持仓**")
    hh = st.columns([1.8, 1.3, 1.5, 1.4, 0.8])
    hh[0].markdown("**代码**")
    hh[1].markdown("**数量**")
    hh[2].markdown("**平均成本价**")
    hh[3].markdown("**成本价货币**")
    hh[4].markdown("**删除**")

    holdings = st.session_state["holdings"]
    h_to_remove = []
    for idx, pos in enumerate(holdings):
        rc = st.columns([1.8, 1.3, 1.5, 1.4, 0.8])
        with rc[0]:
            new_tk = ticker_autocomplete(f"h_t_{idx}", default=pos["ticker"],
                                         label="代码", label_visibility="collapsed")
        new_qty = rc[1].number_input("", value=float(pos["qty"]), min_value=0.0,
                                      step=1.0, key=f"h_q_{idx}", label_visibility="collapsed")
        new_cost = rc[2].number_input("", value=float(pos["cost"]), min_value=0.0,
                                       step=1.0, key=f"h_c_{idx}", label_visibility="collapsed")
        ccy_idx = CURRENCY_LIST.index(pos["ccy"]) if pos["ccy"] in CURRENCY_LIST else 0
        new_ccy = rc[3].selectbox("", CURRENCY_LIST, index=ccy_idx, key=f"h_ccy_{idx}",
                                   label_visibility="collapsed")
        if rc[4].button("🗑️", key=f"h_d_{idx}"):
            h_to_remove.append(idx)
        holdings[idx]["ticker"] = new_tk
        holdings[idx]["qty"]    = new_qty
        holdings[idx]["cost"]   = new_cost
        holdings[idx]["ccy"]    = new_ccy

    for i in sorted(h_to_remove, reverse=True):
        holdings.pop(i)
    if h_to_remove:
        st.rerun()

    ac = st.columns([1.8, 1.3, 1.5, 1.4, 0.8])
    with ac[0]:
        add_tk = ticker_autocomplete("h_ntk", default="",
                                     label="新增代码", label_visibility="collapsed")
    add_qty = ac[1].number_input("", value=1.0, min_value=0.0, step=1.0,
                                  key="h_nqty", label_visibility="collapsed")
    add_cost = ac[2].number_input("", value=100.0, min_value=0.0, step=1.0,
                                   key="h_ncost", label_visibility="collapsed")
    add_ccy = ac[3].selectbox("", CURRENCY_LIST, index=0, key="h_nccy",
                               label_visibility="collapsed")
    if ac[4].button("➕", key="h_add", use_container_width=True):
        if add_tk:
            holdings.append({"ticker": add_tk, "qty": add_qty, "cost": add_cost, "ccy": add_ccy})
            st.rerun()

    st.session_state["holdings"] = holdings
    st.caption("💡 成本价货币可切换为人民币/欧元/日元等，系统会用实时汇率自动换算为美元计算盈亏。")
    st.divider()

    valid_holdings = [h for h in holdings if h["ticker"] and h["qty"] > 0 and h["cost"] > 0]

    if not valid_holdings:
        st.info("👆 请添加至少一个持仓（代码、数量、成本价均需大于0）。股票用 AAPL 这类代码，加密货币用 BTC-USD 这类代码，大宗商品期货用 GC=F（黄金）/ HG=F（铜）这类代码。")
    else:
        with st.spinner("正在获取持仓实时数据并分析..."):
            pos_results = {}
            for h in valid_holdings:
                tk = h["ticker"]
                if tk not in pos_results:
                    pos_results[tk] = fetch_stock_analysis(tk)

        rows = []
        for h in valid_holdings:
            r = pos_results.get(h["ticker"])
            if r is None or "error" in r:
                continue
            ccy_code  = h["ccy"].split()[0]
            fx        = get_fx_rate(ccy_code)
            cost_usd  = h["cost"] * fx  # 统一换算为美元成本价用于盈亏计算
            cur_price = r["price_now"]
            mv      = h["qty"] * cur_price
            cost_v  = h["qty"] * cost_usd
            pnl     = mv - cost_v
            pnl_pct = (cur_price - cost_usd) / cost_usd * 100 if cost_usd > 0 else 0
            rows.append({"h": h, "r": r, "mv": mv, "cost_v": cost_v, "pnl": pnl, "pnl_pct": pnl_pct,
                        "ccy_code": ccy_code, "cost_usd": cost_usd})

        bad_tickers = [h["ticker"] for h in valid_holdings
                       if pos_results.get(h["ticker"]) is None or "error" in pos_results.get(h["ticker"], {})]
        if bad_tickers:
            st.warning(f"以下代码无法获取数据，请检查拼写：{', '.join(sorted(set(bad_tickers)))}")

        if not rows:
            st.error("无法获取任何持仓的数据，请检查代码是否正确。")
        else:
            total_cost    = sum(x["cost_v"] for x in rows)
            total_mv      = sum(x["mv"] for x in rows)
            total_pnl     = total_mv - total_cost
            total_pnl_pct = (total_mv / total_cost - 1) * 100 if total_cost > 0 else 0

            st.markdown("#### 📊 持仓总览")
            oc1, oc2, oc3, oc4 = st.columns(4)
            oc1.metric("总成本", f"${total_cost:,.2f}")
            oc2.metric("当前市值", f"${total_mv:,.2f}")
            oc3.metric("总盈亏", f"${total_pnl:+,.2f}", f"{total_pnl_pct:+.1f}%",
                       delta_color="normal" if total_pnl >= 0 else "inverse")
            win_n = sum(1 for x in rows if x["pnl"] >= 0)
            oc4.metric("盈利/持仓数", f"{win_n}/{len(rows)}")

            _best = max(rows, key=lambda x: x["pnl"])
            _worst = min(rows, key=lambda x: x["pnl"])
            why(f"= 每个持仓的「数量 × 成本价」之和（非美元成本已按实时汇率折算）。"
                f"这是你实际投进去的本金，也是所有收益率的分母。", "neutral", title="总成本", target=oc1)
            why(f"= 每个持仓的「数量 × 最新价」之和。价格取自雅虎财经的最近收盘价，"
                f"所以盘中看到的是上一个交易日收盘的口径，不是实时逐笔。", "neutral", title="当前市值", target=oc2)
            why(f"= 当前市值 − 总成本 = ${total_mv:,.2f} − ${total_cost:,.2f}。"
                f"这轮盈亏主要由 **{_best['h']['ticker']}（{_best['pnl']:+,.0f}）** 贡献，"
                f"**{_worst['h']['ticker']}（{_worst['pnl']:+,.0f}）** 拖累最多。"
                f"下方「逐个持仓深度分析」里会逐一解释每只为什么涨/跌。",
                "good" if total_pnl >= 0 else "bad", calc=f"${total_mv:,.2f} − ${total_cost:,.2f} = ${total_pnl:+,.2f}"
                f"　→　{total_pnl_pct:+.1f}%", title="总盈亏", target=oc3)
            why(f"{len(rows)} 个持仓中有 {win_n} 个当前处于盈利。这个比例反映的是**选股胜率**，"
                f"但它和总盈亏不是一回事——一个重仓的大亏损可以盖过好几个小盈利，所以要和上面的总盈亏一起看。",
                "good" if win_n * 2 >= len(rows) else "warn", title="盈利/持仓数", target=oc4)

            pie_c, list_c = st.columns([1, 2])
            with pie_c:
                fig_hp = go.Figure(go.Pie(
                    labels=[x["h"]["ticker"] for x in rows],
                    values=[max(x["mv"], 0.01) for x in rows],
                    hole=0.4, textinfo="label+percent",
                    marker=dict(colors=(COLORS * 3)[:len(rows)]),
                ))
                fig_hp.update_layout(height=280, margin=dict(t=10, b=10, l=10, r=10), showlegend=False,
                                     annotations=[dict(text=f"${total_mv:,.0f}", x=0.5, y=0.5,
                                                       font_size=13, showarrow=False)])
                glass_chart(fig_hp, use_container_width=True)

            with list_c:
                for x in rows:
                    h, r = x["h"], x["r"]
                    clr = "#0F6E56" if x["pnl"] >= 0 else "#A32D2D"
                    ccy_sym = CURRENCY_SYMBOLS.get(x["ccy_code"], "$")
                    cost_label = f'{ccy_sym}{h["cost"]:.2f} {x["ccy_code"]}'
                    if x["ccy_code"] != "USD":
                        cost_label += f'（≈${x["cost_usd"]:.2f}）'
                    st.markdown(
                        f'<div class="arow" style="border-left:4px solid {clr}">'
                        f'{logo_chip_html(h["ticker"], cls="arow-chip")}'
                        f'<span style="font-size:13px;color:#0f172a">'
                        f'<b>{h["ticker"]}</b> · {h["qty"]:g} @ {cost_label}</span>'
                        f'<span style="margin-left:auto;color:{clr};font-weight:700;font-size:13px">'
                        f'${x["pnl"]:+,.2f}（{x["pnl_pct"]:+.1f}%）</span>'
                        f'</div>', unsafe_allow_html=True
                    )

            st.divider()

            # ── 整体持仓评估（长期怎么样）──
            st.markdown("#### 🎯 整体持仓长期评估")
            weighted_lt = sum(x["r"]["lt_score"] * max(x["mv"], 0.01) for x in rows) / total_mv if total_mv > 0 else 0
            n_bull = sum(1 for x in rows if x["r"]["lt_score"] >= 60)
            n_bear = sum(1 for x in rows if x["r"]["lt_score"] < 45)
            verdict_color = "#0F6E56" if weighted_lt >= 60 else "#BA7517" if weighted_lt >= 45 else "#A32D2D"
            verdict_text = ("整体持仓长期质量偏高，多数标的具备可持续的成长逻辑，适合继续持有并定期复核。" if weighted_lt >= 60 else
                            "整体持仓长期质量中性，建议定期跟踪基本面变化，逢高适度调整配置结构。" if weighted_lt >= 45 else
                            "整体持仓长期质量偏弱，建议重新评估配置结构，逐步向长期评分更高的标的倾斜。")
            st.markdown(
                f'<div style="background:{verdict_color};color:white;padding:14px 18px;border-radius:10px;font-size:14px">'
                f'<b>持仓加权长期评分：{weighted_lt:.0f}/100</b>　|　长期看好 {n_bull} 个持仓　·　长期偏弱 {n_bear} 个持仓<br>'
                f'<span style="font-size:13px;opacity:0.9">{verdict_text}</span></div>',
                unsafe_allow_html=True
            )

            st.divider()
            st.markdown("#### 🔍 逐个持仓深度分析")
            st.caption("展开每个持仓查看：盈亏归因（为什么涨/跌）· 长期投资前景 · 所属赛道的市场潜力")

            def analyze_position_pnl(h, r, pnl_pct, cost_usd, ccy_code):
                """分析单个持仓的盈亏原因"""
                lines = []
                cur = r["price_now"]
                direction = "盈利" if pnl_pct >= 0 else "亏损"
                if ccy_code != "USD":
                    ccy_sym = CURRENCY_SYMBOLS.get(ccy_code, "$")
                    lines.append(f"**成本价 {ccy_sym}{h['cost']:.2f} {ccy_code}（≈${cost_usd:.2f}）→ 现价 ${cur:.2f}，当前{direction} {abs(pnl_pct):.1f}%**")
                else:
                    lines.append(f"**成本价 ${cost_usd:.2f} → 现价 ${cur:.2f}，当前{direction} {abs(pnl_pct):.1f}%**")

                if r["mom_1m"] > 5:
                    lines.append(f"📈 近1个月上涨 {r['mom_1m']:+.1f}%，短期动能是近期表现的主要驱动力。")
                elif r["mom_1m"] < -5:
                    lines.append(f"📉 近1个月下跌 {r['mom_1m']:.1f}%，短期抛压是近期走弱的主因。")
                else:
                    lines.append(f"➡️ 近1个月走势平淡（{r['mom_1m']:+.1f}%），短期没有明显单边驱动。")

                if r["rsi"] > 70:
                    lines.append(f"RSI={r['rsi']:.1f} 处于超买区间，若持仓正在盈利，需警惕短线获利回吐风险。")
                elif r["rsi"] < 30:
                    lines.append(f"RSI={r['rsi']:.1f} 处于超卖区间，若持仓正在亏损，历史上此位置出现反弹的概率较高。")

                if r["macd_hist"] > 0:
                    lines.append("MACD柱为正，多头动能仍在，短期趋势偏向支撑价格。")
                else:
                    lines.append("MACD柱为负，空头动能主导，短期趋势仍偏弱，是压制价格的因素之一。")

                if r["obv_trend"] == "上升":
                    lines.append(f"OBV资金面显示净流入（高于均线{r['obv_pct']:.1f}%），资金仍在积极参与，对价格形成支撑。")
                else:
                    lines.append(f"OBV资金面显示净流出（低于均线{abs(r['obv_pct']):.1f}%），资金持续撤离是价格承压的重要原因之一。")

                macro_sc  = st.session_state.get("macro_score")
                macro_out = st.session_state.get("macro_outlook")
                if macro_sc is not None:
                    beta = r.get("beta") or 1.0
                    if pnl_pct < 0 and macro_sc < 0:
                        lines.append(f"当前宏观环境评分为 {macro_sc:+d}（{macro_out}），高利率/通胀等逆风因素叠加该标的Beta={beta:.2f}，放大了下跌压力——部分亏损可归因于系统性宏观风险，而非仅仅是标的自身问题。")
                    elif pnl_pct >= 0 and macro_sc > 0:
                        lines.append(f"当前宏观环境评分为 {macro_sc:+d}（{macro_out}），顺风环境叠加该标的Beta={beta:.2f}放大了涨幅——部分盈利受益于系统性宏观利好，而非仅仅是个股alpha。")
                    else:
                        lines.append(f"当前宏观环境评分为 {macro_sc:+d}（{macro_out}），与该持仓当前走势方向不完全一致，说明个股/资产自身的基本面或资金面因素目前占主导。")
                else:
                    lines.append("💡 前往「🌐 宏观分析」Tab 加载宏观数据后，此处会补充宏观环境对该持仓盈亏的归因分析。")

                return lines

            for x in rows:
                h, r = x["h"], x["r"]
                icon = "🟢" if x["pnl"] >= 0 else "🔴"
                with st.expander(f"{icon} {h['ticker']} · {r.get('name', h['ticker'])} — 盈亏 {x['pnl_pct']:+.1f}%",
                                 expanded=False):
                    ccy_sym = CURRENCY_SYMBOLS.get(x["ccy_code"], "$")
                    cost_disp = (f"{ccy_sym}{h['cost']:.2f} {x['ccy_code']}"
                                if x["ccy_code"] != "USD" else f"${h['cost']:.2f}")

                    pc1, pc2, pc3, pc4 = st.columns(4)
                    pc1.metric("持仓数量", f"{h['qty']:g}")
                    pc2.metric("成本 / 现价", f"{cost_disp} / ${r['price_now']:.2f}")
                    pc3.metric("盈亏金额", f"${x['pnl']:+,.2f}")
                    pc4.metric("盈亏比例", f"{x['pnl_pct']:+.1f}%",
                               delta_color="normal" if x["pnl_pct"] >= 0 else "inverse")

                    st.markdown("**🧠 盈亏归因分析（为什么涨/跌）**")
                    for line in analyze_position_pnl(h, r, x["pnl_pct"], x["cost_usd"], x["ccy_code"]):
                        st.markdown(f"- {line}")

                    st.markdown("**🏦 长期投资前景**")
                    st.markdown(
                        f'<div style="background:#F8F9FA;border-left:4px solid {r["lt_color"]};'
                        f'padding:10px 14px;border-radius:6px;font-size:13px;margin-bottom:10px">'
                        f'<b style="color:{r["lt_color"]}">{r["lt_rating"]}</b>（长期评分 {r["lt_score"]}/100）'
                        f'&nbsp;·&nbsp;夏普比率 {r["sharpe"]:.2f}'
                        f'&nbsp;·&nbsp;20日趋势斜率 {r["slope_pct"]:+.2f}%/日'
                        f'&nbsp;·&nbsp;价格{"高于" if r["price_now"]>r["ma200"] else "低于"}MA200'
                        f'</div>', unsafe_allow_html=True
                    )

                    st.markdown("**🚀 赛道 / 市场潜力分析**")
                    track_name, track_color, track_desc = get_track_info(h["ticker"], r.get("sector"))
                    st.markdown(
                        f'<div style="background:#F8F9FA;border-left:4px solid {track_color};'
                        f'padding:10px 14px;border-radius:6px;font-size:13px">'
                        f'<b style="color:{track_color}">{track_name}</b><br>{track_desc}'
                        f'</div>', unsafe_allow_html=True
                    )

            st.warning("⚠️ 以上分析基于技术指标及公开财报数据，仅供参考，不构成投资建议。投资有风险，入市需谨慎。")

# ── Tab 8: 投资圣杯（达里欧分散化法则） ────────────────────────────────────────────
with tabs[7]:
    st.subheader("🏆 投资圣杯 · 达里欧的分散化法则")
    st.caption("Ray Dalio：「把 15 个以上互不相关的收益流组合起来，能在不牺牲收益的前提下把风险降低约 80%」—— 这是投资里唯一的免费午餐")

    why("达里欧发现：决定组合风险的不是你持有多少个标的，而是这些标的**彼此有多不相关**。"
        "持有 10 只都在 AI 赛道上的股票，看起来很分散，实际只是同一个赌注下了 10 次；"
        "而股票 + 长久期国债 + 黄金 + 大宗商品这种组合，即使只有 4 个，风险下降幅度也远大于前者。"
        "下面这条曲线就是圣杯的核心：**相关性越低，曲线掉得越快**。",
        "neutral", calc="组合风险 σₚ = σ × √( 1/n + (n−1)/n × ρ )　　n=资产个数，ρ=平均相关性",
        title="什么是投资圣杯")

    # ── 1. 圣杯理论曲线 ──
    _hg_n = np.arange(1, 21)
    fig_hg = go.Figure()
    for _rho, _clr in [(0.0, "#0F6E56"), (0.2, "#1D9E75"), (0.4, "#BA7517"), (0.6, "#A32D2D")]:
        _risk = np.sqrt(1 / _hg_n + (_hg_n - 1) / _hg_n * _rho) * 100
        fig_hg.add_trace(go.Scatter(
            x=_hg_n, y=_risk, mode="lines", name=f"平均相关性 ρ={_rho:.1f}",
            line=dict(color=_clr, width=2.6),
            hovertemplate=f"ρ={_rho:.1f}<br>%{{x}} 个资产<br>风险为单一资产的 %{{y:.0f}}%<extra></extra>",
        ))
    fig_hg.add_vline(x=5, line_dash="dot", line_color="#888", line_width=1.2,
                     annotation_text=" 5个资产", annotation_font=dict(size=11))
    fig_hg.add_vline(x=15, line_dash="dot", line_color="#534AB7", line_width=1.2,
                     annotation_text=" 达里欧建议的15个", annotation_font=dict(size=11, color="#534AB7"))
    fig_hg.update_layout(
        height=380, title=dict(text="圣杯曲线：资产越多、相关性越低，风险下降越快", font=dict(size=14)),
        xaxis=dict(title="互不相关的资产个数", dtick=1, showgrid=True, gridcolor="#eeeeee"),
        yaxis=dict(title="组合风险（相对单一资产 %）", showgrid=True, gridcolor="#eeeeee"),
        legend=dict(orientation="h", y=1.1, x=0), margin=dict(t=70, b=50, l=60, r=30),
        hovermode="x unified",
    )
    glass_chart(fig_hg)
    why("看 ρ=0（绿线）：1个资产风险是100%，5个降到45%，15个只剩26%——**风险砍掉约四分之三，而预期收益一分没少**。"
        "再看 ρ=0.6（红线）：从1个加到15个，风险只从100%降到约80%，加再多也降不下去了，"
        "因为 n→∞ 时曲线收敛于 √ρ（=77%）。这就是为什么达里欧强调「**不相关**」比「多」重要得多。",
        "good", title="这条曲线在说什么")

    st.divider()

    # ── 2. 选择要分析的资产 ──
    st.markdown("#### 🎯 分析你自己的组合")
    _hold_tks = [h["ticker"] for h in st.session_state.get("holdings", []) if h.get("ticker")]
    if "hg_tickers" not in st.session_state:
        st.session_state["hg_tickers"] = (_hold_tks if len(_hold_tks) >= 2
                                          else ["SPY", "TLT", "GLD", "DBC", "VNQ", "BTC-USD"])

    _hg_presets = {
        "🌦️ 全天候(达里欧)": ["VTI", "TLT", "IEF", "GLD", "DBC"],
        "📊 股债黄金": ["SPY", "TLT", "GLD"],
        "🌍 多元分散": ["SPY", "EFA", "VWO", "TLT", "GLD", "DBC", "VNQ", "BTC-USD"],
        "🤖 AI集中(反面教材)": ["NVDA", "AMD", "SMCI", "MSFT", "GOOGL", "META"],
    }
    _pc = st.columns(len(_hg_presets) + 1)
    for _i, (_pn, _pt) in enumerate(_hg_presets.items()):
        if _pc[_i].button(_pn, key=f"hg_preset_{_i}", use_container_width=True):
            st.session_state["hg_tickers"] = _pt
            st.rerun()
    if _pc[-1].button("💰 用我的持仓", key="hg_use_holdings", use_container_width=True,
                      disabled=len(_hold_tks) < 2):
        st.session_state["hg_tickers"] = _hold_tks
        st.rerun()

    _hg_c1, _hg_c2, _hg_c3 = st.columns([3, 1, 1])
    with _hg_c1:
        _hg_opts = list(dict.fromkeys(list(st.session_state["hg_tickers"]) + list(TICKER_UNIVERSE.keys())))
        try:
            _hg_tickers = st.multiselect(
                "🔍 选择资产（边打边出提示，建议 5 个以上且分属不同类别）",
                _hg_opts, default=st.session_state["hg_tickers"], key="hg_pick",
                format_func=_uni_label, accept_new_options=True,
                help="输入首字母即可联想，如 X → XOM / XLK；库里没有的代码也能直接输入")
        except TypeError:
            _hg_tickers = st.multiselect(
                "🔍 选择资产（建议 5 个以上且分属不同类别）",
                _hg_opts, default=st.session_state["hg_tickers"], key="hg_pick",
                format_func=_uni_label)
        _hg_tickers = [t.strip().upper() for t in _hg_tickers if t and t.strip()]
    _hg_period = _hg_c2.selectbox("回看区间", ["1y", "2y", "3y", "5y"], index=1, key="hg_period")
    _hg_bench = _hg_c3.selectbox("Beta基准", ["SPY", "QQQ", "VTI"], index=0, key="hg_bench")
    st.session_state["hg_tickers"] = _hg_tickers

    @st.cache_data(ttl=900, show_spinner=False)
    def fetch_returns_matrix(tickers, period, bench):
        """抓取各资产日收益率并对齐到共同交易日"""
        import yfinance as yf, pandas as pd
        series = {}
        for tk in list(tickers) + [bench]:
            try:
                h = yf.Ticker(tk).history(period=period)
                c = h["Close"].dropna()
                if len(c) < 60:
                    continue
                r = c.pct_change().dropna()
                idx = pd.to_datetime(r.index)
                try:
                    idx = idx.tz_localize(None)
                except (TypeError, AttributeError):
                    idx = idx.tz_convert(None) if getattr(idx, "tz", None) else idx
                r.index = idx.normalize()
                r = r[~r.index.duplicated(keep="last")]
                series[tk] = r
            except Exception:
                continue
        if len(series) < 2:
            return None, None
        df = pd.DataFrame(series).dropna()
        if len(df) < 40:
            return None, None
        # 基准单独取一列；若用户自己也选了基准，它仍保留在资产里（此时 β=1、α=0、R²=100%）
        bench_s = df[bench] if bench in df.columns else None
        keep = [t for t in tickers if t in df.columns]
        if len(keep) < 2:
            return None, None
        return df[keep], bench_s

    if len(_hg_tickers) < 2:
        st.info("👆 请至少输入 2 个资产代码（要看出圣杯效应，建议 5 个以上且分属不同资产类别）")
    else:
        with st.spinner("正在计算相关性矩阵与 Alpha/Beta..."):
            _rets, _bench_r = fetch_returns_matrix(tuple(_hg_tickers), _hg_period, _hg_bench)

        if _rets is None or _rets.shape[1] < 2:
            st.error("有效数据不足，请检查代码是否正确（至少需要 2 个能取到数据的资产）。")
        else:
            _missing = [t for t in _hg_tickers if t not in _rets.columns]
            if _missing:
                st.warning(f"以下代码取不到数据，已跳过：{', '.join(_missing)}")

            _n = _rets.shape[1]
            _corr = _rets.corr()
            _vols = _rets.std() * np.sqrt(252)
            _mask = ~np.eye(_n, dtype=bool)
            _rho_bar = float(_corr.values[_mask].mean())
            _pf_ret = _rets.mean(axis=1)                       # 等权组合
            _pf_vol = float(_pf_ret.std() * np.sqrt(252))
            _avg_vol = float(_vols.mean())
            _div_benefit = (1 - _pf_vol / _avg_vol) * 100 if _avg_vol > 0 else 0
            _n_eff = _n / (1 + (_n - 1) * max(_rho_bar, 0.0001))

            # ── 核心结论卡 ──
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("资产个数", f"{_n} 个", "达标 ✓" if _n >= 5 else "少于5个",
                      delta_color="normal" if _n >= 5 else "inverse")
            k2.metric("平均相关性 ρ", f"{_rho_bar:.2f}", "越低越好", delta_color="off")
            k3.metric("有效分散数", f"{_n_eff:.1f} 个", f"名义{_n}个", delta_color="off")
            k4.metric("风险下降幅度", f"{_div_benefit:.1f}%",
                      f"{_avg_vol*100:.1f}% → {_pf_vol*100:.1f}%", delta_color="normal")

            why(f"你选了 {_n} 个资产，它们两两之间的平均相关性是 **{_rho_bar:.2f}**。"
                + ("相关性很低，接近达里欧说的「互不相关的收益流」。" if _rho_bar < 0.3 else
                   "相关性偏高，说明它们很大程度上在赌同一件事。" if _rho_bar < 0.6 else
                   "相关性非常高，这些资产基本是同涨同跌，分散效果有限。"),
                "good" if _rho_bar < 0.3 else "warn" if _rho_bar < 0.6 else "bad",
                title=f"平均相关性 {_rho_bar:.2f}", target=k2)
            why(f"名义上你有 {_n} 个资产，但因为它们彼此相关，实际只相当于 **{_n_eff:.1f} 个独立赌注**。"
                f"相关性越高，这个数字缩水得越厉害——这才是衡量「真分散」的指标。",
                "good" if _n_eff >= 5 else "warn" if _n_eff >= 3 else "bad",
                calc=f"{_n} ÷ (1 + {_n-1} × {_rho_bar:.2f}) = {_n_eff:.1f}",
                title=f"有效分散数 {_n_eff:.1f}", target=k3)
            why(f"单个资产的平均年化波动率是 {_avg_vol*100:.1f}%，而等权组合的实际波动率只有 {_pf_vol*100:.1f}%，"
                f"**风险被抹掉了 {_div_benefit:.1f}%**。这部分降低完全来自资产之间的不相关性，"
                f"不需要你放弃任何预期收益——这就是达里欧说的免费午餐。",
                "good" if _div_benefit > 25 else "warn",
                calc=f"1 − {_pf_vol*100:.1f}% ÷ {_avg_vol*100:.1f}% = {_div_benefit:.1f}%",
                title=f"风险下降 {_div_benefit:.1f}%", target=k4)

            st.divider()

            # ── 3. 相关性矩阵 ──
            st.markdown("#### 🔥 相关性矩阵")
            fig_corr = go.Figure(go.Heatmap(
                z=_corr.values, x=list(_corr.columns), y=list(_corr.columns),
                colorscale="RdYlGn_r", zmin=-1, zmax=1,
                text=np.round(_corr.values, 2), texttemplate="%{text}",
                textfont=dict(size=11), colorbar=dict(title="相关性"),
                hovertemplate="%{y} vs %{x}<br>相关性 %{z:.2f}<extra></extra>",
            ))
            fig_corr.update_layout(height=90 + 52 * _n, margin=dict(t=20, b=40, l=90, r=30))
            glass_chart(fig_corr)

            _pairs = []
            _cols = list(_corr.columns)
            for _i in range(_n):
                for _j in range(_i + 1, _n):
                    _pairs.append((_cols[_i], _cols[_j], float(_corr.iloc[_i, _j])))
            _pairs.sort(key=lambda x: x[2])
            _lowest, _highest = _pairs[0], _pairs[-1]
            why(f"绿色=不相关（好），红色=同涨同跌（分散无效）。"
                f"当前**最理想的一对是 {_lowest[0]} 与 {_lowest[1]}（{_lowest[2]:.2f}）**，"
                f"它们几乎独立，是组合里真正起分散作用的部分；"
                f"而 **{_highest[0]} 与 {_highest[1]} 的相关性高达 {_highest[2]:.2f}**，"
                + ("这两个基本可以看作同一个资产，同时持有并不会带来额外的分散效果。"
                   if _highest[2] > 0.7 else "相关性偏高，分散作用有限。"),
                "neutral", title="怎么读这张图")

            st.divider()

            # ── 4. 你的组合在圣杯曲线上的位置 ──
            st.markdown("#### 📍 你的组合在圣杯曲线上的位置")
            fig_pos = go.Figure()
            for _rho, _clr in [(0.0, "#0F6E56"), (0.2, "#1D9E75"), (0.4, "#BA7517"), (0.6, "#A32D2D")]:
                fig_pos.add_trace(go.Scatter(
                    x=_hg_n, y=np.sqrt(1 / _hg_n + (_hg_n - 1) / _hg_n * _rho) * 100,
                    mode="lines", name=f"ρ={_rho:.1f}", line=dict(color=_clr, width=1.8, dash="dot"),
                    hoverinfo="skip",
                ))
            fig_pos.add_trace(go.Scatter(
                x=[_n], y=[_pf_vol / _avg_vol * 100 if _avg_vol > 0 else 100],
                mode="markers+text", name="你的组合",
                marker=dict(size=20, color="#534AB7", symbol="star",
                            line=dict(color="white", width=2)),
                text=[f" 你在这里（{_n}个资产，ρ={_rho_bar:.2f}）"], textposition="middle right",
                textfont=dict(size=12, color="#534AB7"),
            ))
            fig_pos.update_layout(
                height=400, xaxis=dict(title="资产个数", dtick=1, showgrid=True, gridcolor="#eeeeee"),
                yaxis=dict(title="组合风险（相对单一资产 %）", showgrid=True, gridcolor="#eeeeee"),
                legend=dict(orientation="h", y=1.1, x=0), margin=dict(t=60, b=50, l=60, r=140),
            )
            glass_chart(fig_pos)
            _room = _pf_vol / _avg_vol * 100 - np.sqrt(1 / max(_n, 1)) * 100
            why(f"紫色星星就是你现在的位置：{_n} 个资产、平均相关性 {_rho_bar:.2f}，"
                f"组合风险是单一资产的 {_pf_vol/_avg_vol*100:.0f}%。"
                f"如果这 {_n} 个资产完全不相关（ρ=0），风险本可以降到 {np.sqrt(1/max(_n,1))*100:.0f}%，"
                f"**中间这 {_room:.0f} 个百分点的差距就是相关性吃掉的分散收益**。"
                f"想往绿线靠，靠的不是继续加同类资产，而是加入定价逻辑完全不同的资产类别。",
                "good" if _room < 15 else "warn", title="怎么读这张图")

            st.divider()

            # ── 5. Alpha / Beta 分解 ──
            st.markdown(f"#### ⚖️ Alpha / Beta 分解（基准：{_hg_bench}）")
            why("达里欧把收益拆成两部分：**Beta 是你承担市场风险自动拿到的收益**（买指数就有，几乎免费）；"
                "**Alpha 是与市场无关的超额收益**（真正稀缺、需要能力）。"
                "分散化的意义在于：Beta 之间往往高度相关，而不同来源的 Alpha 天然不相关——"
                "所以圣杯的真正含义是「收集多个互不相关的 Alpha」。下面对每个资产做回归："
                "β 是它对大盘的敏感度，α 是剔除大盘影响后的年化超额收益，R² 是波动中由大盘解释的比例。",
                "neutral", calc="资产日收益 = α + β × 基准日收益 + ε　（最小二乘回归）",
                title="Alpha 和 Beta 有什么区别")

            if _bench_r is None:
                st.warning(f"无法取得基准 {_hg_bench} 的数据，跳过 Alpha/Beta 分解。")
            else:
                _bvar = float(_bench_r.var())
                _ab_rows = []
                for _tk in _rets.columns:
                    _a = _rets[_tk]
                    _beta = float(np.cov(_a, _bench_r)[0, 1] / _bvar) if _bvar > 0 else 0.0
                    _alpha = float((_a.mean() - _beta * _bench_r.mean()) * 252 * 100)
                    _r2 = float(np.corrcoef(_a, _bench_r)[0, 1] ** 2)
                    _ab_rows.append((_tk, _beta, _alpha, _r2))

                _ab_cards = []
                for _tk, _beta, _alpha, _r2 in _ab_rows:
                    _ac = "#0F6E56" if _alpha > 0 else "#A32D2D"
                    _ab_cards.append(
                        '<div class="ac">' + logo_watermark_html(_tk) +
                        '<div class="ac-glass">'
                        f'<div class="ac-top">{logo_chip_html(_tk)}'
                        f'<div><div class="ac-name">{_tk}</div>'
                        f'<div class="ac-sub">β={_beta:.2f} · R²={_r2*100:.0f}%</div></div></div>'
                        f'<div><div class="ac-val" style="color:{_ac}">α {_alpha:+.1f}%</div>'
                        f'<div class="ac-note">年化超额收益（剔除大盘影响后）</div></div>'
                        '</div></div>'
                    )
                render_asset_grid(_ab_cards, min_width=215)

                with st.expander("📖 每个资产的 Alpha/Beta 怎么读？", expanded=False):
                    for _tk, _beta, _alpha, _r2 in sorted(_ab_rows, key=lambda x: -x[3]):
                        _beta_txt = ("走势几乎与大盘无关，是组合里真正的分散来源" if abs(_beta) < 0.3 else
                                     "与大盘反向，是天然的对冲工具" if _beta < 0 else
                                     f"大盘涨1%它平均涨{_beta:.2f}%，属于放大版大盘" if _beta > 1.2 else
                                     f"大盘涨1%它平均涨{_beta:.2f}%，波动小于大盘，偏防御")
                        _r2_txt = (f"**{_r2*100:.0f}% 的波动由大盘解释**——这部分收益买指数就能拿到"
                                   if _r2 > 0.5 else
                                   f"只有 {_r2*100:.0f}% 的波动由大盘解释，**剩下 {(1-_r2)*100:.0f}% 是它自己的独立行情**，"
                                   f"这正是圣杯需要的那种不相关收益流")
                        _a_txt = (f"剔除大盘影响后年化 **{_alpha:+.1f}%** 的超额收益" if _alpha > 0 else
                                  f"剔除大盘影响后年化 **{_alpha:+.1f}%**，承担了额外风险却没换来相应回报")
                        why(f"β={_beta:.2f}，{_beta_txt}。{_r2_txt}。α：{_a_txt}。",
                            "good" if (_alpha > 0 and _r2 < 0.5) else "warn" if _alpha > 0 else "bad",
                            title=_tk)

                _w = 1.0 / _n
                _pf_beta = sum(b for _, b, _, _ in _ab_rows) * _w
                _pf_alpha = sum(a for _, _, a, _ in _ab_rows) * _w
                why(f"等权组合的加权 β = **{_pf_beta:.2f}**，加权 α = **{_pf_alpha:+.1f}%/年**。"
                    + (f"β 接近1说明你的组合本质上还是在赌大盘方向，" if 0.8 <= _pf_beta <= 1.2 else
                       f"β 只有 {_pf_beta:.2f}，组合对大盘的依赖度较低，这是好现象，" if _pf_beta < 0.8 else
                       f"β 高达 {_pf_beta:.2f}，组合是放大版的大盘，牛市爽、熊市痛，")
                    + "而真正决定你能否长期跑赢的是那部分 α。",
                    "good" if _pf_beta < 0.8 else "warn", title="组合整体的 Alpha 与 Beta")

            st.divider()

            # ── 6. 圣杯评分与改进建议 ──
            st.markdown("#### 🏅 圣杯评分")
            _sc_n   = 40 if _n >= 15 else 32 if _n >= 10 else 24 if _n >= 5 else 12 if _n >= 3 else 5
            _sc_rho = 40 if _rho_bar < 0.1 else 32 if _rho_bar < 0.3 else 20 if _rho_bar < 0.5 else 8 if _rho_bar < 0.7 else 2
            _sc_eff = 20 if _n_eff >= 8 else 14 if _n_eff >= 5 else 8 if _n_eff >= 3 else 3
            _hg_score = _sc_n + _sc_rho + _sc_eff
            _hg_color = ("#0F6E56" if _hg_score >= 75 else "#1D9E75" if _hg_score >= 60
                         else "#BA7517" if _hg_score >= 40 else "#A32D2D")
            _hg_verdict = ("接近圣杯：资产数量足够、彼此独立性强，风险被有效摊薄" if _hg_score >= 75 else
                           "分散良好：已经拿到大部分免费午餐，但仍有优化空间" if _hg_score >= 60 else
                           "分散不足：看起来持有多个标的，实际押注高度重合" if _hg_score >= 40 else
                           "几乎没有分散：这些资产本质上是同一个赌注")
            st.markdown(
                f'<div style="background:{_hg_color};color:white;padding:16px 20px;border-radius:12px;font-size:14px">'
                f'<span style="font-size:24px;font-weight:750">{_hg_score}/100</span>'
                f'　<span style="font-size:15px;font-weight:600">{_hg_verdict}</span><br>'
                f'<span style="font-size:12.5px;opacity:.92">资产数量 {_sc_n}/40　·　'
                f'相关性 {_sc_rho}/40　·　有效分散数 {_sc_eff}/20</span></div>',
                unsafe_allow_html=True)
            why(f"评分由三部分构成：**资产个数 {_n} 个（{_sc_n}/40）**——达里欧建议15个以上；"
                f"**平均相关性 {_rho_bar:.2f}（{_sc_rho}/40）**——这一项权重最重，因为它决定曲线的形状；"
                f"**有效分散数 {_n_eff:.1f}（{_sc_eff}/20）**——名义资产数打完相关性折扣后的真实赌注数。"
                f"{'你已满足「5个以上资产」的门槛，' if _n >= 5 else '你还没达到5个资产的基本门槛，'}"
                f"但圣杯的关键从来不是数量，而是相关性。",
                "good" if _hg_score >= 60 else "warn" if _hg_score >= 40 else "bad",
                calc=f"{_sc_n} + {_sc_rho} + {_sc_eff} = {_hg_score}/100", title="这个分数怎么来的")

            # 资产类别诊断
            def _classify(tk):
                t = tk.upper()
                if t.endswith("-USD"):
                    return "加密货币"
                if t in ("TLT","IEF","SHY","BND","AGG","TIP","LQD","HYG","ZROZ","EDV","GOVT"):
                    return "债券"
                if t in ("GLD","IAU","SLV","GC=F","SI=F","PPLT","GDX","NEM"):
                    return "贵金属"
                if t in ("DBC","DJP","USO","UNG","CL=F","HG=F","CORN","WEAT","PDBC","FCX"):
                    return "大宗商品"
                if t in ("VNQ","IYR","SCHH","O","XLRE"):
                    return "房地产"
                if t in ("EFA","VEA","VWO","EEM","FXI","MCHI","IEFA","IEMG","EWJ","BABA","JD","PDD","BIDU","NIO"):
                    return "非美股票"
                if t in ("UUP","FXE","FXY","USDU"):
                    return "汇率"
                return "美股"
            _classes = {}
            for _tk in _rets.columns:
                _classes.setdefault(_classify(_tk), []).append(_tk)
            _missing_cls = {
                "债券": ("长久期国债（TLT / IEF）", "经济衰退、避险时上涨，是股票最经典的负相关对冲；利率下行周期收益尤其明显"),
                "贵金属": ("黄金（GLD / IAU）", "定价锚是实际利率和地缘风险，与企业盈利无关，常在股债双杀时逆势走强"),
                "大宗商品": ("大宗商品（DBC / PDBC）", "通胀上行期股债往往同跌，而商品同涨，是对抗通胀情景的关键一块"),
                "非美股票": ("非美股票（EFA / VWO）", "不同经济周期和货币体系，能摊薄单一国家的政策与汇率风险"),
                "房地产": ("REITs（VNQ）", "租金现金流与股票盈利周期不完全同步，提供另一条收益来源"),
                "加密货币": ("加密资产（BTC-USD）", "定价逻辑独立于企业盈利，但近年与纳指相关性上升，权重不宜过高"),
            }
            _have = set(_classes.keys())
            _sugg = [(v[0], v[1]) for k, v in _missing_cls.items() if k not in _have]
            st.markdown("**当前组合的资产类别构成**")
            st.markdown(
                " ".join(f'<span style="display:inline-block;background:rgba(83,74,183,.12);color:#534AB7;'
                         f'border-radius:99px;padding:3px 12px;font-size:12px;font-weight:600;margin:2px">'
                         f'{k}：{", ".join(v)}</span>' for k, v in _classes.items()),
                unsafe_allow_html=True)
            if _sugg:
                why("你的组合目前缺少以下资产类别，它们与股票的定价逻辑不同，是把平均相关性压下来最有效的方式："
                    + "；".join(f"**{name}** — {rsn}" for name, rsn in _sugg[:4]) + "。",
                    "warn", title="想往绿线靠，可以补什么")
            else:
                why("你的组合已经覆盖了主要的低相关资产类别（股、债、金、商品等），"
                    "接下来的优化方向不是继续加类别，而是调整各类别的**风险权重**——"
                    "达里欧的全天候策略就是按风险平价（risk parity）而非金额平均来配置的。",
                    "good", title="类别覆盖情况")

            st.warning("⚠️ 相关性会随市场环境变化——危机时各类资产的相关性往往同时飙升（所谓「危机时刻相关性趋近于1」），"
                       "历史相关性只能作为参考，不构成投资建议。")
