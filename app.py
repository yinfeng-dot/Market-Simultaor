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

            # 斐波那契水平图
            st.subheader("📏 斐波那契支撑/阻力位")

            # X轴=时间，Y轴=价格，斐波那契水平线横跨全图
            p_now  = result["price_now"]
            p_stop = result["stop_loss"]
            fib    = result["fib_levels"]
            hist_c = result["hist"]

            fig_fib = go.Figure()

            # K线
            fig_fib.add_trace(go.Candlestick(
                x=hist_c.index,
                open=hist_c["Open"], high=hist_c["High"],
                low=hist_c["Low"],   close=hist_c["Close"],
                name="K线",
                increasing_line_color="#1D9E75",
                decreasing_line_color="#A32D2D",
                showlegend=False,
            ))

            # 斐波那契水平线
            fib_configs = [
                ("0.236", "Fib 23.6%",  "#E07B39", "dash"),
                ("0.382", "Fib 38.2%",  "#D85A30", "dash"),
                ("0.500", "Fib 50.0%",  "#534AB7", "dash"),
                ("0.618", "Fib 61.8%",  "#3C3489", "dash"),
                ("0.786", "Fib 78.6%",  "#251F5C", "dash"),
            ]
            for key, label, color, dash in fib_configs:
                v = fib[key]
                line_color = "#1D9E75" if v <= p_now else "#D85A30"
                fig_fib.add_hline(
                    y=v,
                    line_dash="dash",
                    line_color=line_color,
                    line_width=1.2,
                    annotation_text=f"{label}  ${v:.2f}",
                    annotation_position="right",
                    annotation_font=dict(color=line_color, size=11),
                )

            # 52周高低点线
            fig_fib.add_hline(y=result["price_52w_high"], line_dash="dot",
                              line_color="#185FA5", line_width=1,
                              annotation_text=f"52W高  ${result['price_52w_high']:.2f}",
                              annotation_position="right",
                              annotation_font=dict(color="#185FA5", size=11))
            fig_fib.add_hline(y=result["price_52w_low"], line_dash="dot",
                              line_color="#534AB7", line_width=1,
                              annotation_text=f"52W低  ${result['price_52w_low']:.2f}",
                              annotation_position="right",
                              annotation_font=dict(color="#534AB7", size=11))

            # 现价线
            fig_fib.add_hline(
                y=p_now,
                line_color="#0F6E56",
                line_width=2,
                annotation_text=f"现价  ${p_now:.2f}",
                annotation_position="right",
                annotation_font=dict(color="#0F6E56", size=12, family="Arial Black"),
            )

            # 止损线
            fig_fib.add_hline(
                y=p_stop,
                line_dash="dot",
                line_color="#A32D2D",
                line_width=1.8,
                annotation_text=f"止损  ${p_stop:.2f}",
                annotation_position="right",
                annotation_font=dict(color="#A32D2D", size=11),
            )

            fig_fib.update_layout(
                height=420,
                plot_bgcolor="#fafafa",
                paper_bgcolor="white",
                xaxis=dict(
                    title="日期",
                    showgrid=True, gridcolor="#eeeeee",
                    rangeslider=dict(visible=False),
                ),
                yaxis=dict(
                    title="价格 ($)",
                    showgrid=True, gridcolor="#eeeeee",
                    side="left",
                ),
                margin=dict(t=20, b=40, l=60, r=140),
                showlegend=False,
            )
            st.plotly_chart(fig_fib, use_container_width=True)

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
