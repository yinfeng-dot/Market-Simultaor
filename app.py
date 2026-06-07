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

tabs = st.tabs(["🏠 市场概览","🔍 IPO详情","🎛️ 泡沫模拟","📜 历史对比","📈 趋势预测","🌐 宏观分析","🔬 股票分析器"])

# ── Tab 1: 市场概览 + 实时市场 ──────────────────────────────────────────────────
with tabs[0]:
    st.subheader("📊 市场实时动态")

    live_data_t1 = fetch_market_data()
    if live_data_t1:
        if st.button("🔄 刷新实时数据", key="refresh_t1"):
            st.cache_data.clear(); st.rerun()

        cols_t1 = st.columns(4)
        for i, (ticker, info) in enumerate(live_data_t1.items()):
            cols_t1[i % 4].metric(
                label=info["name"],
                value=f"{info['price']:,.2f}",
                delta=f"{info['change_pct']:+.2f}%",
                delta_color="inverse" if ticker == "^VIX" else "normal",
            )

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
        st.plotly_chart(fig_live_t1, use_container_width=True)

        sentiment_t1 = market_to_sentiment(live_data_t1)
        label_t1 = ("极度恐慌" if sentiment_t1 < 20 else "恐慌" if sentiment_t1 < 40
                    else "中性" if sentiment_t1 < 60 else "乐观" if sentiment_t1 < 80 else "极度狂热")
        st.subheader(f"当前市场情绪：{label_t1}（{sentiment_t1}/100）")
        st.progress(sentiment_t1 / 100)
        st.caption("基于纳斯达克涨跌幅、VIX恐慌指数、英伟达股价综合计算")
    else:
        st.warning("无法获取实时数据，请检查网络连接。")

    st.divider()
    st.subheader("📈 2026 IPO市场总览")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("预期总市值", "$3.12T", "12大待上市公司")
    c2.metric("Q1 2026 融资额", "$42.6B", "同比 +45%")
    c3.metric("AI占风投比例", "80%", "泡沫风险高", delta_color="inverse")
    c4.metric("泡沫综合指数", "74/100", "⚠ 高度警戒", delta_color="inverse")

    st.subheader("市场集中度风险")
    for label, val in {"AI估值集中":88,"流动性压力":79,"盈利能力缺口":72,"锁定期后抛压":65,"市场吸收能力":42}.items():
        st.progress(val/100, text=f"{label}：**{val}%**")

# ── Tab 2: IPO详情（含估值总览） ────────────────────────────────────────────────
with tabs[1]:
    # 估值分布图（从原市场概览移过来）
    st.subheader("核心IPO估值分布")
    names = [c["name"] for c in IPOS]
    vals  = [c["val_b"] for c in IPOS]
    fig_bar = go.Figure(go.Bar(
        x=names, y=vals, marker_color=COLORS,
        text=[f"${v/1000:.2f}T" if v>=1000 else f"${v}B" for v in vals],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>估值: $%{y}B<extra></extra>",
    ))
    fig_bar.update_layout(height=320, margin=dict(t=30,b=20),
                          yaxis_title="估值 ($B)", showlegend=False,
                          plot_bgcolor="#fafafa")
    st.plotly_chart(fig_bar, use_container_width=True)

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

# ── (实时市场已合并到Tab1) ──────────────────────────────────────────────────────

# ── Tab 5: 趋势预测 ──────────────────────────────────────────────────────────────
with tabs[4]:
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


# ── Tab 6: 宏观经济分析 ──────────────────────────────────────────────────────────
with tabs[5]:
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
                st.plotly_chart(fig_m, use_container_width=True)

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
    st.plotly_chart(fig_sec, use_container_width=True)
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



# ── Tab 7: 股票分析器 ──────────────────────────────────────────────────────────
with tabs[6]:
    st.subheader("🔬 股票智能分析器")
    st.caption("输入任意股票代码，自动分析技术面+基本面，给出评级与价格目标")

    # ── 全局 session_state 初始化 ──
    if "selected_ticker" not in st.session_state:
        st.session_state["selected_ticker"] = ""
    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = None
    if "chart_type" not in st.session_state:
        st.session_state["chart_type"] = "📈 K线 + 斐波那契"

    # 快捷选股（点击后存入 session_state，不触发分析）
    st.write("**快捷选择热门股票：**")
    qcols = st.columns(len(POPULAR_STOCKS))
    for i, (group, tickers) in enumerate(POPULAR_STOCKS.items()):
        with qcols[i]:
            st.caption(group)
            for tk in tickers:
                if st.button(tk, key=f"q_{group}_{tk}", use_container_width=True):
                    st.session_state["selected_ticker"] = tk
                    st.session_state["analysis_result"] = None  # 清空旧结果

    st.divider()

    # 股票代码输入框（从 session_state 读取默认值）
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        ticker_input = st.text_input(
            "输入股票代码（如 AAPL、TSLA、0700.HK）",
            value=st.session_state["selected_ticker"],
            placeholder="AAPL",
            key="ticker_text_input",
        ).strip().upper()
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

            hist_c = result["hist"]
            p_now  = result["price_now"]
            p_stop = result["stop_loss"]
            fib    = result["fib_levels"]

            # ── 图表1：K线 + 斐波那契 ──────────────────────────────────────
            if chart_type == "📈 K线 + 斐波那契":
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
                    height=500, plot_bgcolor="#fafafa",
                    xaxis=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                               rangeslider=dict(visible=False)),
                    yaxis=dict(title="价格 ($)", showgrid=True, gridcolor="#eeeeee"),
                    margin=dict(t=50, b=50, l=60, r=160),
                    showlegend=False,
                )

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
                    height=500, plot_bgcolor="#fafafa",
                    xaxis=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                               rangeslider=dict(visible=False)),
                    yaxis=dict(title="价格 ($)", showgrid=True, gridcolor="#eeeeee"),
                    legend=dict(orientation="h", y=1.05, x=0),
                    margin=dict(t=60, b=50, l=60, r=120),
                )

            # ── 图表3：RSI ─────────────────────────────────────────────────
            elif chart_type == "📊 RSI指标":
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
                    height=550, plot_bgcolor="#fafafa",
                    xaxis2=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                                rangeslider=dict(visible=False)),
                    yaxis=dict(showgrid=True, gridcolor="#eeeeee"),
                    yaxis2=dict(title="RSI", range=[0,100],
                                showgrid=True, gridcolor="#eeeeee"),
                    margin=dict(t=60, b=50, l=60, r=80),
                    showlegend=False,
                )

            # ── 图表4：成交量分析 ──────────────────────────────────────────
            elif chart_type == "📦 成交量分析":
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
                    height=550, plot_bgcolor="#fafafa",
                    xaxis2=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                                rangeslider=dict(visible=False)),
                    yaxis=dict(showgrid=True, gridcolor="#eeeeee"),
                    yaxis2=dict(title="成交量", showgrid=True, gridcolor="#eeeeee"),
                    legend=dict(orientation="h", y=1.05),
                    margin=dict(t=60, b=50, l=60, r=60),
                )

            # ── 图表5：OBV能量潮 ───────────────────────────────────────────
            elif chart_type == "🌊 OBV能量潮":
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
                    height=550, plot_bgcolor="#fafafa",
                    xaxis2=dict(title="日期", showgrid=True, gridcolor="#eeeeee",
                                rangeslider=dict(visible=False)),
                    yaxis=dict(showgrid=True, gridcolor="#eeeeee"),
                    yaxis2=dict(title="OBV", showgrid=True, gridcolor="#eeeeee"),
                    legend=dict(orientation="h", y=1.05),
                    margin=dict(t=60, b=50, l=60, r=60),
                )

            st.plotly_chart(fig_c, use_container_width=True)

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
                                st.plotly_chart(fig_rev, use_container_width=True)

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
                                st.plotly_chart(fig_profit, use_container_width=True)

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
                                    st.plotly_chart(fig_bal, use_container_width=True)

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
                                st.plotly_chart(fig_cf, use_container_width=True)

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
                                st.plotly_chart(fig_ann, use_container_width=True)

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
                                st.plotly_chart(fig_fwd, use_container_width=True)

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
