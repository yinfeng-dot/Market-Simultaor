"""
2026 大型IPO与泡沫风险模拟器 - Streamlit版（含实时数据+趋势预测+股票分析器）
"""

import math
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="2026 IPO Bubble Simulator · IPO泡沫模拟器",
    page_icon="📈",
    layout="wide",
)

# ══════════════════════════════════════════════════════════════════════════════
# 🌍 多语言支持（界面骨架已翻译；深度分析正文目前仍为中文）
# ══════════════════════════════════════════════════════════════════════════════
LANGUAGES = {
    "zh": "🇨🇳 简体中文", "en": "🇺🇸 English",  "es": "🇪🇸 Español",
    "fr": "🇫🇷 Français", "de": "🇩🇪 Deutsch", "ja": "🇯🇵 日本語", "ko": "🇰🇷 한국어",
}

I18N = {
 "app_title": {
   "zh":"📈 2026 大型IPO与泡沫风险模拟器", "en":"📈 2026 Mega-IPO & Bubble Risk Simulator",
   "es":"📈 Simulador de Riesgo de Burbuja e IPO 2026", "fr":"📈 Simulateur de Risque de Bulle & IPO 2026",
   "de":"📈 Mega-IPO- & Blasenrisiko-Simulator 2026", "ja":"📈 2026 大型IPO・バブルリスク シミュレーター",
   "ko":"📈 2026 대형 IPO·버블 리스크 시뮬레이터"},
 "app_subtitle": {
   "zh":"数据基于公开市场信息 · 个人学习与技术演示项目",
   "en":"Built on public market data · A personal learning & tech demo project",
   "es":"Basado en datos públicos del mercado · Proyecto personal de aprendizaje y demostración",
   "fr":"Basé sur des données de marché publiques · Projet personnel d'apprentissage et de démonstration",
   "de":"Basiert auf öffentlichen Marktdaten · Persönliches Lern- und Demoprojekt",
   "ja":"公開市場データに基づく · 個人の学習・技術デモ用プロジェクト",
   "ko":"공개 시장 데이터 기반 · 개인 학습 및 기술 데모 프로젝트"},
 # ── 免责声明 ──
 "disc_title": {
   "zh":"免责声明：本站为个人学习与技术演示用途，不构成任何投资建议。",
   "en":"Disclaimer: This site is a personal learning and technical demo. It is NOT investment advice.",
   "es":"Aviso legal: Este sitio es un proyecto personal de aprendizaje y demostración técnica. NO constituye asesoramiento de inversión.",
   "fr":"Avertissement : Ce site est un projet personnel d'apprentissage et de démonstration technique. Il ne constitue PAS un conseil en investissement.",
   "de":"Haftungsausschluss: Diese Website dient dem persönlichen Lernen und der technischen Demonstration. Sie stellt KEINE Anlageberatung dar.",
   "ja":"免責事項：本サイトは個人の学習・技術デモを目的としたものであり、投資助言では一切ありません。",
   "ko":"면책 조항: 본 사이트는 개인 학습 및 기술 데모용이며, 투자 자문이 아닙니다."},
 "disc_body": {
   "zh":"这不是持牌金融机构或投资顾问服务。站内所有评分、评级、目标价、概率与预测，均由公开数据配合简化数学模型自动生成，可能存在错误或失真；部分数据为静态示例数据，行情亦有延迟。请勿据此做出真实投资决策，据此操作风险自负。",
   "en":"This is not a licensed financial institution or advisory service. All scores, ratings, price targets, probabilities and forecasts here are generated automatically from public data using simplified mathematical models and may be inaccurate or misleading. Some figures are static sample data, and quotes are delayed. Do not base real investment decisions on this content — you use it entirely at your own risk.",
   "es":"No es una institución financiera autorizada ni un servicio de asesoramiento. Todas las puntuaciones, calificaciones, precios objetivo, probabilidades y previsiones se generan automáticamente a partir de datos públicos mediante modelos matemáticos simplificados y pueden ser inexactas. Algunos datos son de muestra estática y las cotizaciones tienen retraso. No tome decisiones reales de inversión basándose en esto; el riesgo es exclusivamente suyo.",
   "fr":"Il ne s'agit ni d'un établissement financier agréé ni d'un service de conseil. Tous les scores, notations, objectifs de cours, probabilités et prévisions sont générés automatiquement à partir de données publiques via des modèles mathématiques simplifiés et peuvent être erronés. Certaines données sont des exemples statiques et les cotations sont différées. Ne fondez aucune décision d'investissement réelle sur ce contenu ; vous l'utilisez à vos propres risques.",
   "de":"Dies ist kein lizenziertes Finanzinstitut und keine Anlageberatung. Alle Scores, Ratings, Kursziele, Wahrscheinlichkeiten und Prognosen werden automatisch aus öffentlichen Daten mit vereinfachten mathematischen Modellen erzeugt und können fehlerhaft sein. Einige Daten sind statische Beispieldaten, Kurse sind verzögert. Treffen Sie keine realen Anlageentscheidungen auf dieser Grundlage — die Nutzung erfolgt auf eigenes Risiko.",
   "ja":"当サイトは免許を受けた金融機関でも投資顧問サービスでもありません。掲載されるスコア、レーティング、目標株価、確率、予測はすべて公開データと簡易的な数理モデルにより自動生成されたもので、誤りや歪みを含む可能性があります。一部は静的なサンプルデータであり、相場も遅延しています。実際の投資判断の根拠とせず、利用は自己責任でお願いします。",
   "ko":"본 사이트는 허가받은 금융기관이나 투자자문 서비스가 아닙니다. 모든 점수, 등급, 목표가, 확률, 예측은 공개 데이터와 단순화된 수학 모델로 자동 생성되며 오류가 있을 수 있습니다. 일부는 정적 샘플 데이터이며 시세도 지연됩니다. 이를 근거로 실제 투자 결정을 내리지 마시고, 사용에 따른 책임은 전적으로 본인에게 있습니다."},
 "disc_foot_title": {"zh":"⚠️ 免责声明 / Disclaimer", "en":"⚠️ Disclaimer", "es":"⚠️ Aviso legal",
   "fr":"⚠️ Avertissement", "de":"⚠️ Haftungsausschluss", "ja":"⚠️ 免責事項", "ko":"⚠️ 면책 조항"},
 "disc_f1": {
   "zh":"<b>本站为个人学习与技术演示项目，不构成任何投资建议、要约或推荐</b>，也不是持牌金融机构、券商或投资顾问提供的服务。",
   "en":"<b>This is a personal learning and technical demo project. Nothing here is investment advice, an offer, or a recommendation</b>, and it is not a service of any licensed financial institution, broker or advisor.",
   "es":"<b>Este es un proyecto personal de aprendizaje y demostración técnica. Nada aquí es asesoramiento, oferta ni recomendación de inversión</b>, ni un servicio de ninguna entidad financiera autorizada.",
   "fr":"<b>Ce projet personnel d'apprentissage et de démonstration ne constitue ni conseil, ni offre, ni recommandation d'investissement</b>, et n'émane d'aucun établissement agréé.",
   "de":"<b>Dies ist ein persönliches Lern- und Demoprojekt. Nichts davon ist Anlageberatung, ein Angebot oder eine Empfehlung</b> und stammt von keinem lizenzierten Finanzinstitut.",
   "ja":"<b>本サイトは個人の学習・技術デモであり、投資助言・勧誘・推奨には一切あたりません</b>。免許を受けた金融機関や証券会社によるサービスでもありません。",
   "ko":"<b>본 사이트는 개인 학습·기술 데모 프로젝트이며 투자 자문, 청약 권유, 추천이 아닙니다</b>. 허가받은 금융기관의 서비스도 아닙니다."},
 "disc_f2": {
   "zh":"站内全部评分、评级、目标价、泡沫概率、蒙地卡罗路径与长期预测，均由公开数据配合<b>简化数学模型自动生成</b>，不代表对未来表现的任何承诺或保证。",
   "en":"All scores, ratings, price targets, bubble probabilities, Monte-Carlo paths and long-term forecasts are <b>auto-generated by simplified mathematical models</b> and promise nothing about future performance.",
   "es":"Todas las puntuaciones, calificaciones, precios objetivo, probabilidades y simulaciones de Monte Carlo son <b>generadas automáticamente por modelos simplificados</b> y no garantizan resultados futuros.",
   "fr":"Scores, notations, objectifs de cours, probabilités et trajectoires de Monte-Carlo sont <b>générés automatiquement par des modèles simplifiés</b> et ne garantissent aucune performance future.",
   "de":"Alle Scores, Ratings, Kursziele, Wahrscheinlichkeiten und Monte-Carlo-Pfade werden <b>automatisch durch vereinfachte Modelle erzeugt</b> und garantieren keine künftige Wertentwicklung.",
   "ja":"スコア・レーティング・目標株価・バブル確率・モンテカルロ経路・長期予測はすべて<b>簡易モデルによる自動生成</b>であり、将来の成果を約束するものではありません。",
   "ko":"모든 점수·등급·목표가·버블 확률·몬테카를로 경로·장기 예측은 <b>단순화된 모델로 자동 생성</b>되며 미래 수익을 보장하지 않습니다."},
 "disc_f3": {
   "zh":"行情数据来自雅虎财经等公开来源，<b>美股约延迟15分钟</b>；其中IPO估值、宏观指标等部分内容为<b>静态示例数据</b>，可能与真实市场不符。",
   "en":"Quotes come from public sources such as Yahoo Finance and are <b>delayed ~15 minutes</b> for US equities. IPO valuations and macro indicators are partly <b>static sample data</b> that may differ from the real market.",
   "es":"Las cotizaciones provienen de fuentes públicas como Yahoo Finance y tienen <b>un retraso de ~15 minutos</b>. Las valoraciones de IPO y los indicadores macro son en parte <b>datos de muestra estáticos</b>.",
   "fr":"Les cotations proviennent de sources publiques (Yahoo Finance) et sont <b>différées d'environ 15 minutes</b>. Les valorisations d'IPO et indicateurs macro sont en partie des <b>données d'exemple statiques</b>.",
   "de":"Kurse stammen aus öffentlichen Quellen wie Yahoo Finance und sind <b>ca. 15 Minuten verzögert</b>. IPO-Bewertungen und Makrodaten sind teilweise <b>statische Beispieldaten</b>.",
   "ja":"相場データは Yahoo Finance 等の公開ソースで、米国株は<b>約15分遅延</b>します。IPO評価額やマクロ指標の一部は<b>静的なサンプルデータ</b>です。",
   "ko":"시세는 Yahoo Finance 등 공개 소스에서 가져오며 미국 주식은 <b>약 15분 지연</b>됩니다. IPO 밸류에이션과 매크로 지표 일부는 <b>정적 샘플 데이터</b>입니다."},
 "disc_f4": {
   "zh":"模拟结果基于历史数据与随机过程假设，<b>历史表现不代表未来收益</b>；实际投资可能导致本金部分或全部损失。",
   "en":"Simulations rest on historical data and stochastic assumptions. <b>Past performance does not indicate future returns</b>; real investing can lose part or all of your capital.",
   "es":"Las simulaciones se basan en datos históricos y supuestos estocásticos. <b>El rendimiento pasado no indica rendimientos futuros</b>; puede perder parte o todo su capital.",
   "fr":"Les simulations reposent sur des données historiques et des hypothèses stochastiques. <b>Les performances passées ne préjugent pas des performances futures</b> ; vous pouvez perdre tout ou partie de votre capital.",
   "de":"Simulationen beruhen auf historischen Daten und stochastischen Annahmen. <b>Vergangene Wertentwicklung ist kein Hinweis auf künftige Renditen</b>; Kapitalverluste sind möglich.",
   "ja":"シミュレーションは過去データと確率過程の仮定に基づきます。<b>過去の実績は将来の収益を示しません</b>。元本の一部または全部を失う可能性があります。",
   "ko":"시뮬레이션은 과거 데이터와 확률 과정 가정에 기반합니다. <b>과거 성과가 미래 수익을 보장하지 않으며</b>, 원금의 일부 또는 전부를 잃을 수 있습니다."},
 "disc_f5": {
   "zh":"请在做出任何真实投资决策前，咨询具备资质的专业人士。任何人因使用本站内容而产生的盈亏，均由使用者自行承担。",
   "en":"Consult a qualified professional before making any real investment decision. Any gains or losses from using this site are entirely your own responsibility.",
   "es":"Consulte a un profesional cualificado antes de invertir. Las ganancias o pérdidas derivadas del uso de este sitio son exclusivamente suyas.",
   "fr":"Consultez un professionnel qualifié avant toute décision d'investissement. Les gains ou pertes liés à l'usage de ce site relèvent de votre seule responsabilité.",
   "de":"Konsultieren Sie vor realen Anlageentscheidungen eine qualifizierte Fachperson. Gewinne oder Verluste aus der Nutzung liegen allein in Ihrer Verantwortung.",
   "ja":"実際の投資判断の前に、資格を持つ専門家にご相談ください。本サイト利用により生じた損益はすべて利用者の負担となります。",
   "ko":"실제 투자 결정 전에 자격을 갖춘 전문가와 상담하십시오. 본 사이트 이용으로 발생한 손익은 전적으로 이용자 책임입니다."},
 "disc_side": {
   "zh":"⚠️ **免责声明**：本站为个人学习与技术演示项目，所有分析与预测由简化模型自动生成，**不构成投资建议**，据此操作风险自负。",
   "en":"⚠️ **Disclaimer**: personal learning/demo project. All analysis is auto-generated by simplified models and is **not investment advice** — use at your own risk.",
   "es":"⚠️ **Aviso**: proyecto personal de aprendizaje. Todo el análisis es automático y **no es asesoramiento de inversión**; úselo bajo su responsabilidad.",
   "fr":"⚠️ **Avertissement** : projet personnel de démonstration. Analyses générées automatiquement, **pas un conseil en investissement** ; à vos risques.",
   "de":"⚠️ **Hinweis**: persönliches Lern-/Demoprojekt. Alle Analysen sind automatisch erzeugt und **keine Anlageberatung** — Nutzung auf eigenes Risiko.",
   "ja":"⚠️ **免責**：個人の学習・デモ用。分析は簡易モデルによる自動生成で、**投資助言ではありません**。自己責任でご利用ください。",
   "ko":"⚠️ **면책**: 개인 학습·데모 프로젝트. 모든 분석은 자동 생성되며 **투자 자문이 아닙니다**. 사용 책임은 본인에게 있습니다."},
 # ── 页签 ──
 "tab_market":{"zh":"🏠 市场概览","en":"🏠 Market","es":"🏠 Mercado","fr":"🏠 Marché","de":"🏠 Markt","ja":"🏠 マーケット","ko":"🏠 시장 개요"},
 "tab_ipo":{"zh":"🔍 IPO详情","en":"🔍 IPO Details","es":"🔍 Detalles IPO","fr":"🔍 Détails IPO","de":"🔍 IPO-Details","ja":"🔍 IPO詳細","ko":"🔍 IPO 상세"},
 "tab_history":{"zh":"📜 历史对比","en":"📜 History","es":"📜 Histórico","fr":"📜 Historique","de":"📜 Historie","ja":"📜 過去比較","ko":"📜 과거 비교"},
 "tab_forecast":{"zh":"📈 趋势预测 + 泡沫模拟","en":"📈 Forecast & Bubble Sim","es":"📈 Pronóstico y Burbuja","fr":"📈 Prévision & Bulle","de":"📈 Prognose & Blase","ja":"📈 予測・バブル試算","ko":"📈 예측·버블 시뮬"},
 "tab_macro":{"zh":"🌐 宏观分析","en":"🌐 Macro","es":"🌐 Macro","fr":"🌐 Macro","de":"🌐 Makro","ja":"🌐 マクロ分析","ko":"🌐 매크로"},
 "tab_analyzer":{"zh":"🔬 股票分析器","en":"🔬 Stock Analyzer","es":"🔬 Analizador","fr":"🔬 Analyseur","de":"🔬 Aktien-Analyse","ja":"🔬 銘柄分析","ko":"🔬 종목 분석"},
 "tab_holdings":{"zh":"💰 我的持仓","en":"💰 My Holdings","es":"💰 Mi Cartera","fr":"💰 Mon Portefeuille","de":"💰 Mein Depot","ja":"💰 保有銘柄","ko":"💰 내 보유"},
 "tab_grail":{"zh":"🏆 投资圣杯","en":"🏆 Holy Grail","es":"🏆 Santo Grial","fr":"🏆 Saint Graal","de":"🏆 Heiliger Gral","ja":"🏆 投資の聖杯","ko":"🏆 투자 성배"},
 # ── 侧边栏 / 盯盘 ──
 "lang_label":{"zh":"🌍 语言 / Language","en":"🌍 Language","es":"🌍 Idioma","fr":"🌍 Langue","de":"🌍 Sprache","ja":"🌍 言語","ko":"🌍 언어"},
 "watch_title":{"zh":"### 👀 盯盘模式","en":"### 👀 Watch Mode","es":"### 👀 Modo Vigilancia","fr":"### 👀 Mode Surveillance","de":"### 👀 Beobachtungsmodus","ja":"### 👀 ウォッチモード","ko":"### 👀 관찰 모드"},
 "watch_updated":{"zh":"本次数据更新于 **{ts}**","en":"Data updated at **{ts}**","es":"Datos actualizados a las **{ts}**","fr":"Données mises à jour à **{ts}**","de":"Daten aktualisiert um **{ts}**","ja":"データ更新時刻 **{ts}**","ko":"데이터 갱신 시각 **{ts}**"},
 "watch_active":{"zh":"🟢 盯盘中 · 每 {iv} 秒自动刷新","en":"🟢 Watching · auto-refresh every {iv}s","es":"🟢 Vigilando · cada {iv}s","fr":"🟢 Surveillance · toutes les {iv}s","de":"🟢 Aktiv · alle {iv}s","ja":"🟢 監視中 · {iv}秒ごとに更新","ko":"🟢 관찰 중 · {iv}초마다 갱신"},
 "watch_left":{"zh":"⏳ 剩余 {mm}:{ss}　·　已刷新 {n} 次","en":"⏳ {mm}:{ss} left · refreshed {n}×","es":"⏳ quedan {mm}:{ss} · {n} actualizaciones","fr":"⏳ {mm}:{ss} restantes · {n} actualisations","de":"⏳ {mm}:{ss} übrig · {n} Aktualisierungen","ja":"⏳ 残り {mm}:{ss} · {n} 回更新","ko":"⏳ {mm}:{ss} 남음 · {n}회 갱신"},
 "watch_stop":{"zh":"⏹ 结束盯盘","en":"⏹ Stop","es":"⏹ Detener","fr":"⏹ Arrêter","de":"⏹ Stoppen","ja":"⏹ 停止","ko":"⏹ 중지"},
 "watch_extend":{"zh":"⏱ 再延长","en":"⏱ Extend","es":"⏱ Extender","fr":"⏱ Prolonger","de":"⏱ Verlängern","ja":"⏱ 延長","ko":"⏱ 연장"},
 "watch_start":{"zh":"▶️ 开始盯盘","en":"▶️ Start Watching","es":"▶️ Iniciar","fr":"▶️ Démarrer","de":"▶️ Starten","ja":"▶️ 監視開始","ko":"▶️ 관찰 시작"},
 "watch_interval":{"zh":"刷新间隔","en":"Interval","es":"Intervalo","fr":"Intervalle","de":"Intervall","ja":"更新間隔","ko":"갱신 주기"},
 "watch_duration":{"zh":"盯盘时长","en":"Duration","es":"Duración","fr":"Durée","de":"Dauer","ja":"監視時間","ko":"관찰 시간"},
 "watch_manual":{"zh":"⚪ 当前为手动模式：只有你操作页面或点刷新时才会取新数据，不消耗后台资源。","en":"⚪ Manual mode: data is fetched only when you interact or hit refresh — no background load.","es":"⚪ Modo manual: los datos solo se actualizan al interactuar o pulsar actualizar.","fr":"⚪ Mode manuel : les données ne sont récupérées qu'à votre demande.","de":"⚪ Manueller Modus: Daten werden nur bei Interaktion geladen.","ja":"⚪ 手動モード：操作または更新時のみデータを取得します。","ko":"⚪ 수동 모드: 조작하거나 새로고침할 때만 데이터를 가져옵니다."},
 "watch_expired":{"zh":"⏸️ 盯盘时段已结束，自动刷新已停止（避免你离开后继续空转）。需要时再点开始。","en":"⏸️ Watch session ended; auto-refresh stopped so it doesn't idle while you're away. Start again when needed.","es":"⏸️ Sesión finalizada; la actualización automática se detuvo. Reinícielo cuando lo necesite.","fr":"⏸️ Session terminée ; l'actualisation automatique est arrêtée. Relancez si besoin.","de":"⏸️ Sitzung beendet; Auto-Aktualisierung gestoppt. Bei Bedarf neu starten.","ja":"⏸️ 監視時間が終了し、自動更新を停止しました。必要なときに再開してください。","ko":"⏸️ 관찰 시간이 끝나 자동 갱신을 중지했습니다. 필요할 때 다시 시작하세요."},
 "watch_src":{"zh":"行情来自雅虎财经，美股约延迟15分钟；加密货币 24 小时连续报价。","en":"Quotes from Yahoo Finance; US equities delayed ~15 min, crypto trades 24/7.","es":"Cotizaciones de Yahoo Finance; acciones de EE. UU. con ~15 min de retraso.","fr":"Cotations Yahoo Finance ; actions US différées d'environ 15 min.","de":"Kurse von Yahoo Finance; US-Aktien ca. 15 Min. verzögert.","ja":"相場は Yahoo Finance より。米国株は約15分遅延、暗号資産は24時間取引。","ko":"시세 출처 Yahoo Finance. 미국 주식 약 15분 지연, 암호화폐는 24시간 거래."},
 "force_refresh":{"zh":"🔄 立即强制刷新全部数据","en":"🔄 Force refresh all data","es":"🔄 Forzar actualización","fr":"🔄 Forcer l'actualisation","de":"🔄 Alles neu laden","ja":"🔄 全データを再取得","ko":"🔄 전체 데이터 새로고침"},
 # ── 通用 ──
 "refresh_live":{"zh":"🔄 刷新实时数据","en":"🔄 Refresh live data","es":"🔄 Actualizar datos","fr":"🔄 Actualiser","de":"🔄 Aktualisieren","ja":"🔄 データ更新","ko":"🔄 데이터 새로고침"},
 "view_analysis":{"zh":"📊 查看分析与走势","en":"📊 View analysis & chart","es":"📊 Ver análisis","fr":"📊 Voir l'analyse","de":"📊 Analyse ansehen","ja":"📊 分析とチャート","ko":"📊 분석·차트 보기"},
 "btn_analyze":{"zh":"分析","en":"Analyze","es":"Analizar","fr":"Analyser","de":"Analyse","ja":"分析","ko":"분석"},
 "btn_start_analyze":{"zh":"🔍 开始分析","en":"🔍 Analyze","es":"🔍 Analizar","fr":"🔍 Analyser","de":"🔍 Analysieren","ja":"🔍 分析する","ko":"🔍 분석 시작"},
 "btn_close":{"zh":"✕ 关闭","en":"✕ Close","es":"✕ Cerrar","fr":"✕ Fermer","de":"✕ Schließen","ja":"✕ 閉じる","ko":"✕ 닫기"},
 "col_code":{"zh":"代码","en":"Ticker","es":"Símbolo","fr":"Symbole","de":"Kürzel","ja":"銘柄コード","ko":"종목 코드"},
 "col_qty":{"zh":"数量","en":"Quantity","es":"Cantidad","fr":"Quantité","de":"Menge","ja":"数量","ko":"수량"},
 "col_cost":{"zh":"平均成本价","en":"Avg. cost","es":"Coste medio","fr":"Prix de revient","de":"Ø Kaufpreis","ja":"平均取得単価","ko":"평균 단가"},
 "col_ccy":{"zh":"成本价货币","en":"Cost currency","es":"Moneda","fr":"Devise","de":"Währung","ja":"通貨","ko":"통화"},
 "col_delete":{"zh":"删除","en":"Delete","es":"Eliminar","fr":"Supprimer","de":"Löschen","ja":"削除","ko":"삭제"},
 # ── 各区块标题 ──
 "sec_live":{"zh":"📊 市场实时动态","en":"📊 Live Market","es":"📊 Mercado en Vivo","fr":"📊 Marché en Direct","de":"📊 Live-Markt","ja":"📊 マーケット速報","ko":"📊 실시간 시장"},
 "sec_crypto_metals":{"zh":"💎 加密货币 & 有色金属/矿业","en":"💎 Crypto & Metals/Mining","es":"💎 Cripto y Metales","fr":"💎 Crypto & Métaux","de":"💎 Krypto & Metalle","ja":"💎 暗号資産・非鉄金属","ko":"💎 암호화폐·비철금속"},
 "sec_today_change":{"zh":"今日涨跌幅","en":"Today's Change","es":"Variación de Hoy","fr":"Variation du Jour","de":"Tagesveränderung","ja":"本日の騰落率","ko":"오늘 등락률"},
 "sec_holdings":{"zh":"💰 我的持仓","en":"💰 My Holdings","es":"💰 Mi Cartera","fr":"💰 Mon Portefeuille","de":"💰 Mein Depot","ja":"💰 保有銘柄","ko":"💰 내 보유 종목"},
 "sec_holdings_overview":{"zh":"#### 📊 持仓总览","en":"#### 📊 Portfolio Summary","es":"#### 📊 Resumen de Cartera","fr":"#### 📊 Synthèse du Portefeuille","de":"#### 📊 Depot-Übersicht","ja":"#### 📊 保有サマリー","ko":"#### 📊 보유 요약"},
 "sec_analyzer":{"zh":"🔬 股票智能分析器","en":"🔬 Smart Stock Analyzer","es":"🔬 Analizador de Acciones","fr":"🔬 Analyseur d'Actions","de":"🔬 Aktien-Analysetool","ja":"🔬 銘柄アナライザー","ko":"🔬 스마트 종목 분석기"},
 "sec_grail":{"zh":"🏆 投资圣杯 · 达里欧的分散化法则","en":"🏆 The Holy Grail · Dalio's Diversification Rule","es":"🏆 El Santo Grial · Diversificación de Dalio","fr":"🏆 Le Saint Graal · Diversification de Dalio","de":"🏆 Der Heilige Gral · Dalios Diversifikation","ja":"🏆 投資の聖杯 · ダリオの分散法則","ko":"🏆 투자의 성배 · 달리오의 분산 법칙"},
 "m_total_cost":{"zh":"总成本","en":"Total cost","es":"Coste total","fr":"Coût total","de":"Gesamtkosten","ja":"取得総額","ko":"총 매입금액"},
 "m_market_value":{"zh":"当前市值","en":"Market value","es":"Valor actual","fr":"Valeur actuelle","de":"Marktwert","ja":"評価額","ko":"평가금액"},
 "m_total_pnl":{"zh":"总盈亏","en":"Total P&L","es":"P&L total","fr":"P&L total","de":"Gesamt-G/V","ja":"損益合計","ko":"총 손익"},
 "m_win_ratio":{"zh":"盈利/持仓数","en":"Winners / positions","es":"Ganadoras / posiciones","fr":"Gagnantes / positions","de":"Gewinner / Positionen","ja":"利益銘柄 / 保有数","ko":"수익 종목 / 보유 수"},
 "i18n_note":{
   "zh":"", "en":"ℹ️ Interface is translated; the detailed auto-generated commentary is still in Chinese for now.",
   "es":"ℹ️ La interfaz está traducida; los comentarios analíticos detallados siguen en chino por ahora.",
   "fr":"ℹ️ L'interface est traduite ; les commentaires analytiques détaillés restent en chinois pour l'instant.",
   "de":"ℹ️ Die Oberfläche ist übersetzt; die ausführlichen Analysetexte sind vorerst auf Chinesisch.",
   "ja":"ℹ️ UIは翻訳済みですが、詳細な自動生成コメントは現時点では中国語のままです。",
   "ko":"ℹ️ 인터페이스는 번역되었지만 상세 자동 생성 해설은 아직 중국어입니다."},
 # ── Tab2 IPO详情 ──
 "sub_ipo_live":{"zh":"📡 已上市IPO实时行情","en":"📡 Live quotes: already-listed IPOs","es":"📡 Cotizaciones de IPO ya listadas","fr":"📡 Cours des IPO déjà cotées","de":"📡 Live-Kurse gelisteter IPOs","ja":"📡 上場済みIPOのリアルタイム相場","ko":"📡 상장된 IPO 실시간 시세"},
 "ipo_listed_on":{"zh":"🚀 纳斯达克上市 · 发行价 $135.00","en":"🚀 Listed on NASDAQ · IPO price $135.00","es":"🚀 Cotiza en NASDAQ · precio de salida $135.00","fr":"🚀 Coté au NASDAQ · prix d'introduction 135,00 $","de":"🚀 An der NASDAQ gelistet · Ausgabepreis 135,00 $","ja":"🚀 ナスダック上場 · 公開価格 $135.00","ko":"🚀 나스닥 상장 · 공모가 $135.00"},
 "btn_refresh_price":{"zh":"🔄 刷新实时价格","en":"🔄 Refresh prices","es":"🔄 Actualizar precios","fr":"🔄 Actualiser les cours","de":"🔄 Kurse aktualisieren","ja":"🔄 価格を更新","ko":"🔄 가격 새로고침"},
 "sub_val_dist":{"zh":"核心IPO估值分布","en":"Valuations of Key IPOs","es":"Valoraciones de las IPO clave","fr":"Valorisations des IPO clés","de":"Bewertungen der wichtigsten IPOs","ja":"主要IPOのバリュエーション","ko":"주요 IPO 밸류에이션"},
 "sub_company_deep":{"zh":"公司深度分析","en":"Company Deep Dive","es":"Análisis de la empresa","fr":"Analyse approfondie","de":"Unternehmensanalyse","ja":"企業の詳細分析","ko":"기업 심층 분석"},
 "sub_compare_all":{"zh":"所有公司对比","en":"All Companies Compared","es":"Comparativa de empresas","fr":"Comparaison des sociétés","de":"Alle Unternehmen im Vergleich","ja":"全社比較","ko":"전체 기업 비교"},
 "sel_company":{"zh":"选择公司","en":"Select a company","es":"Seleccionar empresa","fr":"Choisir une société","de":"Unternehmen wählen","ja":"企業を選択","ko":"기업 선택"},
 "m_exp_val":{"zh":"预期估值","en":"Expected valuation","es":"Valoración prevista","fr":"Valorisation attendue","de":"Erwartete Bewertung","ja":"想定バリュエーション","ko":"예상 밸류에이션"},
 "m_revenue":{"zh":"年收入","en":"Annual revenue","es":"Ingresos anuales","fr":"Chiffre d'affaires annuel","de":"Jahresumsatz","ja":"年間売上","ko":"연간 매출"},
 "m_ps":{"zh":"P/S倍数","en":"P/S multiple","es":"Múltiplo P/S","fr":"Multiple P/S","de":"P/S-Multiple","ja":"PSR","ko":"P/S 배수"},
 "m_profitable":{"zh":"盈利状态","en":"Profitability","es":"Rentabilidad","fr":"Rentabilité","de":"Profitabilität","ja":"収益状況","ko":"흑자 여부"},
 "yes_profit":{"zh":"✓ 盈利","en":"✓ Profitable","es":"✓ Rentable","fr":"✓ Rentable","de":"✓ Profitabel","ja":"✓ 黒字","ko":"✓ 흑자"},
 "no_profit":{"zh":"✗ 亏损","en":"✗ Loss-making","es":"✗ En pérdidas","fr":"✗ Déficitaire","de":"✗ Verlustreich","ja":"✗ 赤字","ko":"✗ 적자"},
 "m_day1_pop":{"zh":"首日预期涨幅","en":"Expected day-1 pop","es":"Subida esperada día 1","fr":"Hausse attendue jour 1","de":"Erwarteter Tag-1-Sprung","ja":"初日予想上昇率","ko":"상장 첫날 예상 상승률"},
 "m_bubble_risk":{"zh":"泡沫风险","en":"Bubble risk","es":"Riesgo de burbuja","fr":"Risque de bulle","de":"Blasenrisiko","ja":"バブルリスク","ko":"버블 리스크"},
 "btn_view_company":{"zh":"📈 查看 {name}（{tk}）的走势图与完整技术分析","en":"📈 View {name} ({tk}) chart and full technical analysis","es":"📈 Ver gráfico y análisis de {name} ({tk})","fr":"📈 Voir le graphique et l'analyse de {name} ({tk})","de":"📈 Chart und Analyse zu {name} ({tk})","ja":"📈 {name}（{tk}）のチャートと詳細分析","ko":"📈 {name}({tk}) 차트 및 전체 분석 보기"},
 "ipo_not_listed":{"zh":"🔒 {name} 尚未上市（预计 {date}），还没有可交易的股票代码，因此无法显示K线走势。上市后这里会自动出现走势图入口。你可以先在「📈 趋势预测」里用同板块的已上市标的做情景推演。",
   "en":"🔒 {name} has not listed yet (expected {date}), so there is no tradable ticker and no price chart to show. A chart link will appear here automatically once it lists. In the meantime you can run scenarios on a listed peer in the Forecast tab."},
 "quick_chart_title":{"zh":"#### 🔎 {tk} 走势与技术分析","en":"#### 🔎 {tk} chart & technical analysis","es":"#### 🔎 Gráfico y análisis de {tk}","fr":"#### 🔎 Graphique et analyse de {tk}","de":"#### 🔎 {tk} Chart & Analyse","ja":"#### 🔎 {tk} チャートと分析","ko":"#### 🔎 {tk} 차트·기술 분석"},
 "ax_valuation":{"zh":"估值 ($B)","en":"Valuation ($B)","es":"Valoración ($B)","fr":"Valorisation (Md$)","de":"Bewertung ($ Mrd.)","ja":"評価額（十億ドル）","ko":"밸류에이션($B)"},
 "ax_bubble_risk":{"zh":"泡沫风险 (%)","en":"Bubble risk (%)","es":"Riesgo de burbuja (%)","fr":"Risque de bulle (%)","de":"Blasenrisiko (%)","ja":"バブルリスク (%)","ko":"버블 리스크 (%)"},
 "ax_day1":{"zh":"首日预期涨幅 (%)","en":"Expected day-1 pop (%)","es":"Subida esperada día 1 (%)","fr":"Hausse attendue jour 1 (%)","de":"Erwarteter Tag-1-Sprung (%)","ja":"初日予想上昇率 (%)","ko":"첫날 예상 상승률 (%)"},
 "hover_val":{"zh":"估值","en":"Valuation"},
 # ── Tab3 历史对比 ──
 "sub_history":{"zh":"历史泡沫周期对比","en":"Historical Bubble Cycles Compared","es":"Comparación de burbujas históricas","fr":"Comparaison des bulles historiques","de":"Historische Blasenzyklen im Vergleich","ja":"過去のバブル局面との比較","ko":"과거 버블 사이클 비교"},
 "hist_dotcom":{"zh":"2000互联网","en":"2000 Dot-com"},
 "hist_spac":{"zh":"2021 SPAC","en":"2021 SPAC"},
 "hist_ai":{"zh":"2026 AI IPO(预测)","en":"2026 AI IPO (projected)"},
 "ax_index_base":{"zh":"指数 (基准=100)","en":"Index (base = 100)","es":"Índice (base = 100)","fr":"Indice (base = 100)","de":"Index (Basis = 100)","ja":"指数（基準=100）","ko":"지수 (기준=100)"},
 "hist_c1":{"zh":"**2000 互联网泡沫**\n\n纳斯达克峰值5,048点，随后暴跌78%。1500+科技公司破产，市值蒸发约$5万亿。",
   "en":"**The 2000 Dot-com Bubble**\n\nThe Nasdaq peaked at 5,048 and then fell 78%. More than 1,500 tech companies went bankrupt and roughly $5 trillion of market value evaporated."},
 "hist_c2":{"zh":"**2021 SPAC狂热**\n\n600+ SPAC上市，多数较峰值下跌70%+。利率上升刺破泡沫，散户损失惨重。",
   "en":"**The 2021 SPAC Mania**\n\nOver 600 SPACs listed; most fell more than 70% from their highs. Rising rates punctured the bubble and retail investors took the brunt of the losses."},
 "hist_c3":{"zh":"**2026 AI IPO浪潮**\n\n三巨头合计估值$3T，AI占风投80%。部分公司确有营收，但P/S倍数同样极端。",
   "en":"**The 2026 AI IPO Wave**\n\nThe top three are valued at $3T combined and AI takes 80% of venture funding. Some of these companies do have real revenue — but their P/S multiples are just as extreme."},
 # ── Tab7 我的持仓 ──
 "holdings_caption":{"zh":"记录你的真实持仓（含成本价），自动分析盈亏原因、长期投资前景与赛道潜力 · 支持股票/ETF/加密货币/大宗商品期货",
   "en":"Track your actual positions (with cost basis) and get automatic attribution of gains/losses, long-term outlook and sector potential · stocks, ETFs, crypto and commodity futures"},
 "add_edit_holdings":{"zh":"**添加/编辑持仓**","en":"**Add / edit positions**","es":"**Añadir / editar posiciones**","fr":"**Ajouter / modifier des positions**","de":"**Positionen hinzufügen / bearbeiten**","ja":"**保有銘柄の追加・編集**","ko":"**보유 종목 추가/편집**"},
 "ccy_hint":{"zh":"💡 成本价货币可切换为人民币/欧元/日元等，系统会用实时汇率自动换算为美元计算盈亏。",
   "en":"💡 Cost basis can be entered in CNY, EUR, JPY and more — it is converted to USD at live FX rates for the P&L math."},
 "holdings_empty":{"zh":"👆 请添加至少一个持仓（代码、数量、成本价均需大于0）。股票用 AAPL 这类代码，加密货币用 BTC-USD 这类代码，大宗商品期货用 GC=F（黄金）/ HG=F（铜）这类代码。",
   "en":"👆 Add at least one position (ticker, quantity and cost must all be greater than zero). Use tickers like AAPL for stocks, BTC-USD for crypto, and GC=F (gold) or HG=F (copper) for commodity futures."},
 "holdings_fetching":{"zh":"正在获取持仓实时数据并分析...","en":"Fetching live data and analysing your positions...","es":"Obteniendo datos y analizando posiciones...","fr":"Récupération des données et analyse des positions...","de":"Daten werden geladen und Positionen analysiert...","ja":"保有銘柄のデータを取得・分析中...","ko":"보유 종목 데이터를 가져와 분석 중..."},
 "holdings_none_ok":{"zh":"无法获取任何持仓的数据，请检查代码是否正确。","en":"Could not load data for any position — please check the tickers.","es":"No se pudieron cargar datos de ninguna posición.","fr":"Aucune position n'a pu être chargée.","de":"Für keine Position konnten Daten geladen werden.","ja":"いずれの保有銘柄もデータを取得できませんでした。","ko":"어떤 보유 종목도 데이터를 불러오지 못했습니다."},
 "sec_holdings_lt":{"zh":"#### 🎯 整体持仓长期评估","en":"#### 🎯 Long-term quality of the whole portfolio","es":"#### 🎯 Calidad a largo plazo de la cartera","fr":"#### 🎯 Qualité long terme du portefeuille","de":"#### 🎯 Langfrist-Qualität des Depots","ja":"#### 🎯 ポートフォリオ全体の長期評価","ko":"#### 🎯 포트폴리오 전체 장기 평가"},
 "sec_holdings_each":{"zh":"#### 🔍 逐个持仓深度分析","en":"#### 🔍 Position-by-position deep dive","es":"#### 🔍 Análisis posición por posición","fr":"#### 🔍 Analyse position par position","de":"#### 🔍 Analyse je Position","ja":"#### 🔍 保有銘柄ごとの詳細分析","ko":"#### 🔍 보유 종목별 심층 분석"},
 "holdings_each_cap":{"zh":"展开每个持仓查看：盈亏归因（为什么涨/跌）· 长期投资前景 · 所属赛道的市场潜力",
   "en":"Expand any position to see: P&L attribution (why it moved), long-term outlook, and the market potential of its sector"},
 "lt_weighted":{"zh":"<b>持仓加权长期评分：{score:.0f}/100</b>　|　长期看好 {bull} 个持仓　·　长期偏弱 {bear} 个持仓",
   "en":"<b>Value-weighted long-term score: {score:.0f}/100</b>　|　{bull} position(s) look strong long term　·　{bear} look weak"},
 "lt_verdict_hi":{"zh":"整体持仓长期质量偏高，多数标的具备可持续的成长逻辑，适合继续持有并定期复核。",
   "en":"Overall long-term quality is high: most holdings have a durable growth case. Keep holding and review periodically."},
 "lt_verdict_mid":{"zh":"整体持仓长期质量中性，建议定期跟踪基本面变化，逢高适度调整配置结构。",
   "en":"Overall long-term quality is neutral. Track fundamentals regularly and trim into strength where the case weakens."},
 "lt_verdict_lo":{"zh":"整体持仓长期质量偏弱，建议重新评估配置结构，逐步向长期评分更高的标的倾斜。",
   "en":"Overall long-term quality is weak. Reassess the structure and gradually rotate toward holdings with better long-term scores."},
 "pos_qty":{"zh":"持仓数量","en":"Quantity","es":"Cantidad","fr":"Quantité","de":"Stückzahl","ja":"保有数量","ko":"보유 수량"},
 "pos_cost_price":{"zh":"成本 / 现价","en":"Cost / price","es":"Coste / precio","fr":"Coût / cours","de":"Kosten / Kurs","ja":"取得単価 / 現在値","ko":"매입가 / 현재가"},
 "pos_pnl_amt":{"zh":"盈亏金额","en":"P&L","es":"P&L","fr":"P&L","de":"G/V","ja":"損益額","ko":"손익 금액"},
 "pos_pnl_pct":{"zh":"盈亏比例","en":"P&L %","es":"P&L %","fr":"P&L %","de":"G/V %","ja":"損益率","ko":"손익률"},
 "pos_attr":{"zh":"**🧠 盈亏归因分析（为什么涨/跌）**","en":"**🧠 Why it moved (P&L attribution)**","es":"**🧠 Por qué se movió**","fr":"**🧠 Pourquoi ça a bougé**","de":"**🧠 Warum es sich bewegt hat**","ja":"**🧠 損益の要因分析**","ko":"**🧠 손익 요인 분석**"},
 "pos_lt":{"zh":"**🏦 长期投资前景**","en":"**🏦 Long-term outlook**","es":"**🏦 Perspectiva a largo plazo**","fr":"**🏦 Perspective long terme**","de":"**🏦 Langfristausblick**","ja":"**🏦 長期の見通し**","ko":"**🏦 장기 전망**"},
 "pos_track":{"zh":"**🚀 赛道 / 市场潜力分析**","en":"**🚀 Sector & market potential**","es":"**🚀 Potencial del sector**","fr":"**🚀 Potentiel du secteur**","de":"**🚀 Sektor- & Marktpotenzial**","ja":"**🚀 セクターと市場のポテンシャル**","ko":"**🚀 섹터·시장 잠재력**"},
 "lt_score_line":{"zh":"（长期评分 {score}/100）&nbsp;·&nbsp;夏普比率 {sharpe:.2f}&nbsp;·&nbsp;20日趋势斜率 {slope:+.2f}%/日&nbsp;·&nbsp;价格{ma}MA200",
   "en":"(long-term score {score}/100)&nbsp;·&nbsp;Sharpe {sharpe:.2f}&nbsp;·&nbsp;20-day slope {slope:+.2f}%/day&nbsp;·&nbsp;price {ma} MA200"},
 "above":{"zh":"高于","en":"above"}, "below":{"zh":"低于","en":"below"},
 # ── Tab7 持仓归因 ──
 "w_total_cost":{"zh":"= 每个持仓的「数量 × 成本价」之和（非美元成本已按实时汇率折算）。这是你实际投进去的本金，也是所有收益率的分母。",
   "en":"= the sum of \u201cquantity × cost\u201d for each position (non-USD costs converted at live FX rates). This is the capital you actually put in, and the denominator of every return figure."},
 "w_mkt_value":{"zh":"= 每个持仓的「数量 × 最新价」之和。价格取自雅虎财经的最近收盘价，所以盘中看到的是上一个交易日收盘的口径，不是实时逐笔。",
   "en":"= the sum of \u201cquantity × latest price\u201d. Prices come from Yahoo Finance's most recent close, so during the session you are looking at the previous close, not tick-by-tick data."},
 "w_total_pnl":{"zh":"= 当前市值 − 总成本 = ${mv:,.2f} − ${cost:,.2f}。这轮盈亏主要由 **{best}（{bestv:+,.0f}）** 贡献，**{worst}（{worstv:+,.0f}）** 拖累最多。下方「逐个持仓深度分析」里会逐一解释每只为什么涨/跌。",
   "en":"= market value − total cost = ${mv:,.2f} − ${cost:,.2f}. **{best} ({bestv:+,.0f})** contributed most to this result, while **{worst} ({worstv:+,.0f})** was the biggest drag. The position-by-position section below explains why each one moved."},
 "w_win_ratio":{"zh":"{n} 个持仓中有 {win} 个当前处于盈利。这个比例反映的是**选股胜率**，但它和总盈亏不是一回事——一个重仓的大亏损可以盖过好几个小盈利，所以要和上面的总盈亏一起看。",
   "en":"{win} of {n} positions are currently in profit. This is your **hit rate**, which is not the same thing as total P&L — one large losing position can outweigh several small winners, so read it together with the total above."},
 "pnl_head":{"zh":"**成本价 {cost_disp} → 现价 ${cur:.2f}，当前{direction} {pct:.1f}%**",
   "en":"**Cost {cost_disp} → current ${cur:.2f}; currently {direction} {pct:.1f}%**"},
 "dir_profit":{"zh":"盈利","en":"up"}, "dir_loss":{"zh":"亏损","en":"down"},
 "pnl_mom_up":{"zh":"📈 近1个月上涨 {m:+.1f}%，短期动能是近期表现的主要驱动力。",
   "en":"📈 Up {m:+.1f}% over the past month — short-term momentum is the main driver of recent performance."},
 "pnl_mom_dn":{"zh":"📉 近1个月下跌 {m:.1f}%，短期抛压是近期走弱的主因。",
   "en":"📉 Down {m:.1f}% over the past month — short-term selling pressure is the main reason for the weakness."},
 "pnl_mom_flat":{"zh":"➡️ 近1个月走势平淡（{m:+.1f}%），短期没有明显单边驱动。",
   "en":"➡️ Little movement over the past month ({m:+.1f}%) — no clear one-way driver in the short run."},
 "pnl_rsi_hi":{"zh":"RSI={v:.1f} 处于超买区间，若持仓正在盈利，需警惕短线获利回吐风险。",
   "en":"RSI={v:.1f} is in overbought territory — if you are sitting on a gain, watch for short-term profit-taking."},
 "pnl_rsi_lo":{"zh":"RSI={v:.1f} 处于超卖区间，若持仓正在亏损，历史上此位置出现反弹的概率较高。",
   "en":"RSI={v:.1f} is in oversold territory — if you are underwater, history says a bounce from here is more likely than not."},
 "pnl_macd_pos":{"zh":"MACD柱为正，多头动能仍在，短期趋势偏向支撑价格。",
   "en":"The MACD histogram is positive: bullish momentum is intact and the short-term trend is supporting the price."},
 "pnl_macd_neg":{"zh":"MACD柱为负，空头动能主导，短期趋势仍偏弱，是压制价格的因素之一。",
   "en":"The MACD histogram is negative: bearish momentum dominates and the short-term trend is one of the forces holding the price down."},
 "pnl_obv_in":{"zh":"OBV资金面显示净流入（高于均线{v:.1f}%），资金仍在积极参与，对价格形成支撑。",
   "en":"On-balance volume shows net inflows ({v:.1f}% above its average) — money is still engaged and supporting the price."},
 "pnl_obv_out":{"zh":"OBV资金面显示净流出（低于均线{v:.1f}%），资金持续撤离是价格承压的重要原因之一。",
   "en":"On-balance volume shows net outflows ({v:.1f}% below its average) — persistent withdrawal of money is a key reason the price is under pressure."},
 "pnl_macro_bad":{"zh":"当前宏观环境评分为 {sc:+d}（{out}），高利率/通胀等逆风因素叠加该标的Beta={beta:.2f}，放大了下跌压力——部分亏损可归因于系统性宏观风险，而非仅仅是标的自身问题。",
   "en":"The macro backdrop scores {sc:+d} ({out}). Headwinds like high rates and inflation, amplified by this asset's beta of {beta:.2f}, magnify the downside — so part of the loss is systematic macro risk rather than something specific to this holding."},
 "pnl_macro_good":{"zh":"当前宏观环境评分为 {sc:+d}（{out}），顺风环境叠加该标的Beta={beta:.2f}放大了涨幅——部分盈利受益于系统性宏观利好，而非仅仅是个股alpha。",
   "en":"The macro backdrop scores {sc:+d} ({out}). A supportive environment, amplified by this asset's beta of {beta:.2f}, magnified the gain — so part of the profit came from systematic macro tailwinds rather than stock-specific alpha."},
 "pnl_macro_mixed":{"zh":"当前宏观环境评分为 {sc:+d}（{out}），与该持仓当前走势方向不完全一致，说明个股/资产自身的基本面或资金面因素目前占主导。",
   "en":"The macro backdrop scores {sc:+d} ({out}), which does not line up with this position's direction — meaning asset-specific fundamentals or flows are currently in the driver's seat."},
 "pnl_macro_none":{"zh":"💡 前往「🌐 宏观分析」Tab 加载宏观数据后，此处会补充宏观环境对该持仓盈亏的归因分析。",
   "en":"💡 Open the Macro tab to load macro data, and this section will add a macro attribution for this position."},
 "pos_expander":{"zh":"{icon} {tk} · {name} — 盈亏 {pct:+.1f}%","en":"{icon} {tk} · {name} — P&L {pct:+.1f}%"},
 "disc_tab_note":{"zh":"⚠️ 以上分析基于技术指标及公开财报数据，仅供参考，不构成投资建议。投资有风险，入市需谨慎。",
   "en":"⚠️ The analysis above is based on technical indicators and public filings. It is for reference only and is not investment advice — investing carries risk."},
 "where_holdings":{"zh":"持仓统计","en":"the portfolio totals"},
 # ── Tab8 投资圣杯 ──
 "hg_caption":{"zh":"Ray Dalio：「把 15 个以上互不相关的收益流组合起来，能在不牺牲收益的前提下把风险降低约 80%」—— 这是投资里唯一的免费午餐",
   "en":"Ray Dalio: \u201cCombine 15 or more uncorrelated return streams and you can cut risk by roughly 80% without giving up return\u201d — the only free lunch in investing"},
 "hg_intro":{"zh":"达里欧发现：决定组合风险的不是你持有多少个标的，而是这些标的**彼此有多不相关**。持有 10 只都在 AI 赛道上的股票，看起来很分散，实际只是同一个赌注下了 10 次；而股票 + 长久期国债 + 黄金 + 大宗商品这种组合，即使只有 4 个，风险下降幅度也远大于前者。下面这条曲线就是圣杯的核心：**相关性越低，曲线掉得越快**。",
   "en":"Dalio's insight: what determines portfolio risk is not how many positions you hold, but **how uncorrelated they are**. Ten AI stocks look diversified but are really the same bet placed ten times, whereas equities + long-duration Treasuries + gold + commodities cuts risk far more with just four holdings. The curve below is the heart of the Holy Grail: **the lower the correlation, the faster it falls**."},
 "hg_intro_calc":{"zh":"组合风险 σₚ = σ × √( 1/n + (n−1)/n × ρ )　　n=资产个数，ρ=平均相关性",
   "en":"Portfolio risk σₚ = σ × √( 1/n + (n−1)/n × ρ )　　n = number of assets, ρ = average correlation"},
 "hg_intro_title":{"zh":"什么是投资圣杯","en":"What the Holy Grail means"},
 "hg_curve_title":{"zh":"圣杯曲线：资产越多、相关性越低，风险下降越快","en":"The Holy Grail curve: more assets and lower correlation cut risk faster"},
 "hg_legend":{"zh":"平均相关性 ρ={r:.1f}","en":"avg correlation ρ={r:.1f}"},
 "hg_hover":{"zh":"个资产<br>风险为单一资产的","en":"assets<br>risk vs a single asset:"},
 "hg_ann_5":{"zh":" 5个资产","en":" 5 assets"},
 "hg_ann_15":{"zh":" 达里欧建议的15个","en":" Dalio's suggested 15"},
 "hg_ax_n":{"zh":"互不相关的资产个数","en":"Number of uncorrelated assets"},
 "hg_ax_n2":{"zh":"资产个数","en":"Number of assets"},
 "hg_ax_risk":{"zh":"组合风险（相对单一资产 %）","en":"Portfolio risk (% of a single asset)"},
 "hg_curve_read":{"zh":"看 ρ=0（绿线）：1个资产风险是100%，5个降到45%，15个只剩26%——**风险砍掉约四分之三，而预期收益一分没少**。再看 ρ=0.6（红线）：从1个加到15个，风险只从100%降到约80%，加再多也降不下去了，因为 n→∞ 时曲线收敛于 √ρ（=77%）。这就是为什么达里欧强调「**不相关**」比「多」重要得多。",
   "en":"Look at ρ=0 (green): one asset carries 100% risk, five drops it to 45%, fifteen leaves only 26% — **about three quarters of the risk is gone while expected return is untouched**. Now look at ρ=0.6 (red): going from one asset to fifteen only takes risk from 100% to roughly 80%, and adding more barely helps, because as n→∞ the curve converges to √ρ (=77%). That is why Dalio insists **uncorrelated** matters far more than *many*."},
 "hg_curve_read_t":{"zh":"这条曲线在说什么","en":"What this curve is telling you"},
 "hg_your_pf":{"zh":"#### 🎯 分析你自己的组合","en":"#### 🎯 Analyse your own portfolio"},
 "hg_preset_aw":{"zh":"🌦️ 全天候(达里欧)","en":"🌦️ All Weather (Dalio)"},
 "hg_preset_sbg":{"zh":"📊 股债黄金","en":"📊 Stocks + Bonds + Gold"},
 "hg_preset_div":{"zh":"🌍 多元分散","en":"🌍 Broadly diversified"},
 "hg_preset_ai":{"zh":"🤖 AI集中(反面教材)","en":"🤖 AI-concentrated (what not to do)"},
 "hg_use_holdings":{"zh":"💰 用我的持仓","en":"💰 Use my holdings"},
 "hg_pick_assets":{"zh":"🔍 选择资产（边打边出提示，建议 5 个以上且分属不同类别）","en":"🔍 Pick assets (type to search; aim for 5+ across different classes)"},
 "hg_pick_help":{"zh":"输入首字母即可联想，如 X → XOM / XLK；库里没有的代码也能直接输入","en":"Type the first letters to search, e.g. X → XOM / XLK; tickers outside the list can be entered directly"},
 "hg_lookback":{"zh":"回看区间","en":"Lookback"},
 "hg_bench":{"zh":"Beta基准","en":"Beta benchmark"},
 "hg_need2":{"zh":"👆 请至少输入 2 个资产代码（要看出圣杯效应，建议 5 个以上且分属不同资产类别）","en":"👆 Add at least 2 tickers (to see the Holy Grail effect properly, use 5+ from different asset classes)"},
 "hg_computing":{"zh":"正在计算相关性矩阵与 Alpha/Beta...","en":"Computing the correlation matrix and Alpha/Beta..."},
 "hg_nodata":{"zh":"有效数据不足，请检查代码是否正确（至少需要 2 个能取到数据的资产）。","en":"Not enough usable data — check the tickers (at least 2 must return data)."},
 "hg_where":{"zh":"相关性与Alpha/Beta计算","en":"the correlation and Alpha/Beta calculation"},
 "hg_m_n":{"zh":"资产个数","en":"Assets"},
 "hg_m_n_ok":{"zh":"达标 ✓","en":"target met ✓"}, "hg_m_n_bad":{"zh":"少于5个","en":"fewer than 5"},
 "hg_m_rho":{"zh":"平均相关性 ρ","en":"Avg correlation ρ"},
 "hg_m_rho_d":{"zh":"越低越好","en":"lower is better"},
 "hg_m_eff":{"zh":"有效分散数","en":"Effective bets"},
 "hg_m_eff_d":{"zh":"名义{n}个","en":"{n} nominal"},
 "hg_m_cut":{"zh":"风险下降幅度","en":"Risk reduction"},
 "hg_w_rho":{"zh":"你选了 {n} 个资产，它们两两之间的平均相关性是 **{rho:.2f}**。{verdict}",
   "en":"You selected {n} assets whose average pairwise correlation is **{rho:.2f}**. {verdict}"},
 "hg_rho_lo":{"zh":"相关性很低，接近达里欧说的「互不相关的收益流」。","en":"That is genuinely low — close to what Dalio means by uncorrelated return streams."},
 "hg_rho_mid":{"zh":"相关性偏高，说明它们很大程度上在赌同一件事。","en":"That is on the high side: these holdings are largely betting on the same thing."},
 "hg_rho_hi":{"zh":"相关性非常高，这些资产基本是同涨同跌，分散效果有限。","en":"That is very high — these assets rise and fall together, so diversification is doing little."},
 "hg_w_eff":{"zh":"名义上你有 {n} 个资产，但因为它们彼此相关，实际只相当于 **{eff:.1f} 个独立赌注**。相关性越高，这个数字缩水得越厉害——这才是衡量「真分散」的指标。",
   "en":"Nominally you hold {n} assets, but because they move together they amount to only **{eff:.1f} independent bets**. The higher the correlation, the more this number shrinks — it is the real measure of diversification."},
 "hg_w_cut":{"zh":"按当前权重，单个资产的平均年化波动率是 {avg:.1f}%，而{mode}的组合波动率只有 {pf:.1f}%，**风险被抹掉了 {cut:.1f}%**。这部分降低完全来自资产之间的不相关性，不需要你放弃任何预期收益——这就是达里欧说的免费午餐。",
   "en":"At the current weights the average single-asset volatility is {avg:.1f}% a year, yet {mode} realises only {pf:.1f}% — **{cut:.1f}% of the risk has been erased**. That reduction comes purely from the assets not moving together, and costs you nothing in expected return. This is Dalio's free lunch."},
 "hg_t_rho":{"zh":"平均相关性 {rho:.2f}","en":"Average correlation {rho:.2f}"},
 "hg_t_eff":{"zh":"有效分散数 {eff:.1f}","en":"Effective bets {eff:.1f}"},
 "hg_t_cut":{"zh":"风险下降 {cut:.1f}%","en":"Risk cut {cut:.1f}%"},
 "hg_corr_matrix":{"zh":"#### 🔥 相关性矩阵","en":"#### 🔥 Correlation matrix"},
 "hg_corr":{"zh":"相关性","en":"Correlation"},
 "hg_corr_read":{"zh":"绿色=不相关（好），红色=同涨同跌（分散无效）。当前**最理想的一对是 {lo1} 与 {lo2}（{lov:.2f}）**，它们几乎独立，是组合里真正起分散作用的部分；而 **{hi1} 与 {hi2} 的相关性高达 {hiv:.2f}**，{tail}",
   "en":"Green = uncorrelated (good), red = moving together (diversification failing). The best pair right now is **{lo1} and {lo2} ({lov:.2f})** — nearly independent, and the part of the portfolio actually doing the diversifying. Meanwhile **{hi1} and {hi2} are correlated at {hiv:.2f}**, {tail}"},
 "hg_corr_tail_hi":{"zh":"这两个基本可以看作同一个资产，同时持有并不会带来额外的分散效果。","en":"which makes them effectively the same asset — holding both adds no diversification."},
 "hg_corr_tail_mid":{"zh":"相关性偏高，分散作用有限。","en":"which is high enough that the diversification benefit is limited."},
 "hg_pos_title":{"zh":"#### 📍 你的组合在圣杯曲线上的位置","en":"#### 📍 Where your portfolio sits on the curve"},
 "hg_your_pf_marker":{"zh":"你的组合","en":"Your portfolio"},
 "hg_you_here":{"zh":" 你在这里（{n}个资产，ρ={rho:.2f}）","en":" You are here ({n} assets, ρ={rho:.2f})"},
 "hg_pos_read":{"zh":"紫色星星就是你现在的位置：{n} 个资产、平均相关性 {rho:.2f}，组合风险是单一资产的 {cur:.0f}%。如果这 {n} 个资产完全不相关（ρ=0），风险本可以降到 {ideal:.0f}%，**中间这 {room:.0f} 个百分点的差距就是相关性吃掉的分散收益**。想往绿线靠，靠的不是继续加同类资产，而是加入定价逻辑完全不同的资产类别。",
   "en":"The purple star is you: {n} assets, average correlation {rho:.2f}, portfolio risk at {cur:.0f}% of a single asset. Were these {n} assets perfectly uncorrelated (ρ=0), risk could fall to {ideal:.0f}% — **the {room:.0f} percentage points in between is exactly what correlation is costing you**. Getting closer to the green line is not about adding more of the same, but about adding asset classes priced by different forces."},
 "hg_ab_title":{"zh":"#### ⚖️ Alpha / Beta 分解（基准：{b}）","en":"#### ⚖️ Alpha / Beta decomposition (benchmark: {b})"},
 "hg_ab_intro":{"zh":"达里欧把收益拆成两部分：**Beta 是你承担市场风险自动拿到的收益**（买指数就有，几乎免费）；**Alpha 是与市场无关的超额收益**（真正稀缺、需要能力）。分散化的意义在于：Beta 之间往往高度相关，而不同来源的 Alpha 天然不相关——所以圣杯的真正含义是「收集多个互不相关的 Alpha」。下面对每个资产做回归：β 是它对大盘的敏感度，α 是剔除大盘影响后的年化超额收益，R² 是波动中由大盘解释的比例。",
   "en":"Dalio splits returns in two: **beta is what you get simply for carrying market risk** (buy an index and you have it — essentially free), while **alpha is the excess return unrelated to the market** (genuinely scarce and hard to produce). Diversification matters because betas are highly correlated with each other, whereas alphas from different sources are naturally uncorrelated — so the Holy Grail really means *collecting many uncorrelated alphas*. Below, each asset is regressed on the benchmark: β is its market sensitivity, α is the annualised excess return after stripping out the market, and R² is the share of its movement the market explains."},
 "hg_ab_calc":{"zh":"资产日收益 = α + β × 基准日收益 + ε　（最小二乘回归）","en":"asset daily return = α + β × benchmark daily return + ε　(OLS regression)"},
 "hg_ab_title2":{"zh":"Alpha 和 Beta 有什么区别","en":"How alpha differs from beta"},
 "hg_ab_nobench":{"zh":"无法取得基准 {b} 的数据，跳过 Alpha/Beta 分解。","en":"Could not load benchmark {b}; skipping the Alpha/Beta decomposition."},
 "hg_ab_note":{"zh":"年化超额收益（剔除大盘影响后）","en":"annualised excess return (market effect removed)"},
 "hg_ab_expander":{"zh":"📖 每个资产的 Alpha/Beta 怎么读？","en":"📖 How to read each asset's Alpha/Beta"},
 "hg_beta_indep":{"zh":"走势几乎与大盘无关，是组合里真正的分散来源","en":"it barely tracks the market — a genuine source of diversification"},
 "hg_beta_neg":{"zh":"与大盘反向，是天然的对冲工具","en":"it moves opposite the market — a natural hedge"},
 "hg_beta_hi":{"zh":"大盘涨1%它平均涨{b:.2f}%，属于放大版大盘","en":"when the market rises 1% it rises {b:.2f}% on average — a leveraged version of the market"},
 "hg_beta_lo":{"zh":"大盘涨1%它平均涨{b:.2f}%，波动小于大盘，偏防御","en":"when the market rises 1% it rises {b:.2f}% on average — less volatile than the market, defensive"},
 "hg_r2_hi":{"zh":"**{r:.0f}% 的波动由大盘解释**——这部分收益买指数就能拿到","en":"**{r:.0f}% of its movement is explained by the market** — that part you could get from an index fund"},
 "hg_r2_lo":{"zh":"只有 {r:.0f}% 的波动由大盘解释，**剩下 {rest:.0f}% 是它自己的独立行情**，这正是圣杯需要的那种不相关收益流",
   "en":"only {r:.0f}% of its movement is market-driven, **leaving {rest:.0f}% as its own independent path** — exactly the kind of uncorrelated return stream the Holy Grail needs"},
 "hg_alpha_pos":{"zh":"剔除大盘影响后年化 **{a:+.1f}%** 的超额收益","en":"**{a:+.1f}%** annualised excess return once the market is stripped out"},
 "hg_alpha_neg":{"zh":"剔除大盘影响后年化 **{a:+.1f}%**，承担了额外风险却没换来相应回报","en":"**{a:+.1f}%** annualised once the market is stripped out — extra risk taken without the reward to match"},
 "hg_ab_line":{"zh":"β={b:.2f}，{btxt}。{r2txt}。α：{atxt}。","en":"β={b:.2f} — {btxt}. {r2txt}. Alpha: {atxt}."},
 "hg_pf_ab":{"zh":"{mode}的加权 β = **{beta:.2f}**，加权 α = **{alpha:+.1f}%/年**。{tail}而真正决定你能否长期跑赢的是那部分 α。",
   "en":"{mode} has a weighted β of **{beta:.2f}** and a weighted α of **{alpha:+.1f}% a year**. {tail}What actually decides whether you outperform over time is that alpha."},
 "hg_pf_b_mid":{"zh":"β 接近1说明你的组合本质上还是在赌大盘方向，","en":"A beta near 1 means the portfolio is essentially a bet on market direction. "},
 "hg_pf_b_lo":{"zh":"β 只有 {b:.2f}，组合对大盘的依赖度较低，这是好现象，","en":"At just {b:.2f}, the portfolio depends relatively little on the market — a good sign. "},
 "hg_pf_b_hi":{"zh":"β 高达 {b:.2f}，组合是放大版的大盘，牛市爽、熊市痛，","en":"At {b:.2f} the portfolio is a leveraged version of the market: great in bull runs, painful in drawdowns. "},
 "hg_pf_ab_t":{"zh":"组合整体的 Alpha 与 Beta","en":"Portfolio-level alpha and beta"},
 "hg_score_title":{"zh":"#### 🏅 圣杯评分","en":"#### 🏅 Holy Grail score"},
 "hg_v_hi":{"zh":"接近圣杯：资产数量足够、彼此独立性强，风险被有效摊薄","en":"Close to the Grail: enough assets, genuinely independent, risk well spread"},
 "hg_v_mid":{"zh":"分散良好：已经拿到大部分免费午餐，但仍有优化空间","en":"Well diversified: most of the free lunch captured, some room left"},
 "hg_v_lo":{"zh":"分散不足：看起来持有多个标的，实际押注高度重合","en":"Under-diversified: many holdings, but the bets overlap heavily"},
 "hg_v_none":{"zh":"几乎没有分散：这些资产本质上是同一个赌注","en":"Barely diversified: these assets are essentially one bet"},
 "hg_score_break":{"zh":"资产数量 {n}/40　·　相关性 {r}/40　·　有效分散数 {e}/20","en":"assets {n}/40　·　correlation {r}/40　·　effective bets {e}/20"},
 "hg_score_why":{"zh":"评分由三部分构成：**资产个数 {n} 个（{sn}/40）**——达里欧建议15个以上；**平均相关性 {rho:.2f}（{sr}/40）**——这一项权重最重，因为它决定曲线的形状；**有效分散数 {eff:.1f}（{se}/20）**——名义资产数打完相关性折扣后的真实赌注数。{gate}但圣杯的关键从来不是数量，而是相关性。",
   "en":"The score has three parts: **{n} assets ({sn}/40)** — Dalio suggests 15 or more; **average correlation {rho:.2f} ({sr}/40)** — the heaviest weight, because it sets the shape of the curve; and **{eff:.1f} effective bets ({se}/20)** — your nominal asset count after the correlation haircut. {gate}But the Grail was never about quantity; it is about correlation."},
 "hg_gate_ok":{"zh":"你已满足「5个以上资产」的门槛，","en":"You have cleared the \u201c5+ assets\u201d bar. "},
 "hg_gate_no":{"zh":"你还没达到5个资产的基本门槛，","en":"You have not yet reached the basic bar of 5 assets. "},
 "cls_crypto":{"zh":"加密货币","en":"Crypto"}, "cls_bond":{"zh":"债券","en":"Bonds"},
 "cls_pm":{"zh":"贵金属","en":"Precious metals"}, "cls_comm":{"zh":"大宗商品","en":"Commodities"},
 "cls_re":{"zh":"房地产","en":"Real estate"}, "cls_intl":{"zh":"非美股票","en":"Non-US equities"},
 "cls_fx":{"zh":"汇率","en":"Currencies"}, "cls_us":{"zh":"美股","en":"US equities"},
 "hg_cls_title":{"zh":"**当前组合的资产类别构成**","en":"**Asset classes currently represented**"},
 "hg_sugg_bond":{"zh":"长久期国债（TLT / IEF）","en":"Long-duration Treasuries (TLT / IEF)"},
 "hg_sugg_bond_r":{"zh":"经济衰退、避险时上涨，是股票最经典的负相关对冲；利率下行周期收益尤其明显","en":"they rally in recessions and risk-off episodes — the classic negative correlation to equities, and especially rewarding when rates fall"},
 "hg_sugg_gold":{"zh":"黄金（GLD / IAU）","en":"Gold (GLD / IAU)"},
 "hg_sugg_gold_r":{"zh":"定价锚是实际利率和地缘风险，与企业盈利无关，常在股债双杀时逆势走强","en":"priced off real rates and geopolitics rather than corporate earnings, it often rises when stocks and bonds fall together"},
 "hg_sugg_comm":{"zh":"大宗商品（DBC / PDBC）","en":"Commodities (DBC / PDBC)"},
 "hg_sugg_comm_r":{"zh":"通胀上行期股债往往同跌，而商品同涨，是对抗通胀情景的关键一块","en":"when inflation rises stocks and bonds tend to fall together while commodities rise — the key piece for that scenario"},
 "hg_sugg_intl":{"zh":"非美股票（EFA / VWO）","en":"Non-US equities (EFA / VWO)"},
 "hg_sugg_intl_r":{"zh":"不同经济周期和货币体系，能摊薄单一国家的政策与汇率风险","en":"different economic cycles and currency regimes dilute single-country policy and FX risk"},
 "hg_sugg_re":{"zh":"REITs（VNQ）","en":"REITs (VNQ)"},
 "hg_sugg_re_r":{"zh":"租金现金流与股票盈利周期不完全同步，提供另一条收益来源","en":"rental cash flows do not track the equity earnings cycle exactly, adding another return stream"},
 "hg_sugg_crypto":{"zh":"加密资产（BTC-USD）","en":"Crypto (BTC-USD)"},
 "hg_sugg_crypto_r":{"zh":"定价逻辑独立于企业盈利，但近年与纳指相关性上升，权重不宜过高","en":"priced independently of corporate earnings, though its correlation with the Nasdaq has risen — keep the weight modest"},
 "hg_missing":{"zh":"你的组合目前缺少以下资产类别，它们与股票的定价逻辑不同，是把平均相关性压下来最有效的方式：","en":"Your portfolio is missing these asset classes. They are priced by different forces than equities, and adding them is the most effective way to pull the average correlation down: "},
 "hg_missing_t":{"zh":"想往绿线靠，可以补什么","en":"What to add to move toward the green line"},
 "hg_covered":{"zh":"你的组合已经覆盖了主要的低相关资产类别（股、债、金、商品等），接下来的优化方向不是继续加类别，而是调整各类别的**风险权重**——达里欧的全天候策略就是按风险平价（risk parity）而非金额平均来配置的。",
   "en":"Your portfolio already covers the main low-correlation classes (equities, bonds, gold, commodities). The next step is not more classes but **risk weighting** between them — Dalio's All Weather allocates by risk parity rather than equal dollars."},
 "hg_covered_t":{"zh":"类别覆盖情况","en":"Asset-class coverage"},
 "hg_warn":{"zh":"⚠️ 相关性会随市场环境变化——危机时各类资产的相关性往往同时飙升（所谓「危机时刻相关性趋近于1」），历史相关性只能作为参考，不构成投资建议。",
   "en":"⚠️ Correlations shift with the regime — in a crisis they tend to spike toward 1 across the board. Historical correlation is a reference only, not investment advice."},
 "sent_headline":{"zh":"当前市场情绪：{label}（{score}/100）","en":"Current market sentiment: {label} ({score}/100)",
   "es":"Sentimiento actual del mercado: {label} ({score}/100)","fr":"Sentiment de marché actuel : {label} ({score}/100)",
   "de":"Aktuelle Marktstimmung: {label} ({score}/100)","ja":"現在のマーケット心理：{label}（{score}/100）","ko":"현재 시장 심리: {label} ({score}/100)"},
 "ax_change":{"zh":"涨跌幅 (%)","en":"Change (%)","es":"Variación (%)","fr":"Variation (%)","de":"Veränderung (%)","ja":"騰落率 (%)","ko":"등락률 (%)"},
 "ax_change_24h":{"zh":"24h涨跌幅 (%)","en":"24h change (%)","es":"Variación 24h (%)","fr":"Variation 24h (%)","de":"24h-Veränderung (%)","ja":"24時間騰落率 (%)","ko":"24시간 등락률 (%)"},
 "ax_change_today":{"zh":"今日涨跌幅 (%)","en":"Today's change (%)","es":"Variación de hoy (%)","fr":"Variation du jour (%)","de":"Tagesveränderung (%)","ja":"本日の騰落率 (%)","ko":"오늘 등락률 (%)"},
 "sub_crypto":{"zh":"🪙 加密货币","en":"🪙 Crypto","es":"🪙 Cripto","fr":"🪙 Crypto","de":"🪙 Krypto","ja":"🪙 暗号資産","ko":"🪙 암호화폐"},
 "sub_metals":{"zh":"⛏️ 有色金属/矿业","en":"⛏️ Metals & Mining","es":"⛏️ Metales y Minería","fr":"⛏️ Métaux & Mines","de":"⛏️ Metalle & Bergbau","ja":"⛏️ 非鉄金属・鉱業","ko":"⛏️ 비철금속·광업"},
 "err_live":{"zh":"无法获取实时数据，请检查网络连接。","en":"Could not load live data — please check your connection.","es":"No se pudieron cargar los datos en vivo.","fr":"Impossible de charger les données en direct.","de":"Live-Daten konnten nicht geladen werden.","ja":"リアルタイムデータを取得できませんでした。","ko":"실시간 데이터를 불러오지 못했습니다."},
 "err_crypto":{"zh":"无法获取加密货币实时数据。","en":"Could not load live crypto data.","es":"No se pudieron cargar los datos de cripto.","fr":"Impossible de charger les données crypto.","de":"Krypto-Daten konnten nicht geladen werden.","ja":"暗号資産のデータを取得できませんでした。","ko":"암호화폐 데이터를 불러오지 못했습니다."},
 "err_metals":{"zh":"无法获取有色金属数据。","en":"Could not load metals data.","es":"No se pudieron cargar los datos de metales.","fr":"Impossible de charger les données métaux.","de":"Metalldaten konnten nicht geladen werden.","ja":"非鉄金属のデータを取得できませんでした。","ko":"금속 데이터를 불러오지 못했습니다."},
 "futures":{"zh":"期货合约","en":"Futures contract","es":"Contrato de futuros","fr":"Contrat à terme","de":"Futures-Kontrakt","ja":"先物","ko":"선물"},
 "quick_analysis":{"zh":"#### 🔎 {tk} 快速分析","en":"#### 🔎 {tk} quick analysis","es":"#### 🔎 Análisis rápido de {tk}","fr":"#### 🔎 Analyse rapide de {tk}","de":"#### 🔎 {tk} Schnellanalyse","ja":"#### 🔎 {tk} クイック分析","ko":"#### 🔎 {tk} 빠른 분석"},
 "analyzing":{"zh":"正在分析 {tk}...","en":"Analyzing {tk}...","es":"Analizando {tk}...","fr":"Analyse de {tk}...","de":"Analysiere {tk}...","ja":"{tk} を分析中...","ko":"{tk} 분석 중..."},
 "sub_ipo_overview":{"zh":"📈 2026 IPO市场总览","en":"📈 2026 IPO Market Overview","es":"📈 Panorama del mercado de IPO 2026","fr":"📈 Panorama du marché IPO 2026","de":"📈 IPO-Marktüberblick 2026","ja":"📈 2026 IPO市場概況","ko":"📈 2026 IPO 시장 개요"},
 "sub_conc_risk":{"zh":"市场集中度风险","en":"Market Concentration Risk","es":"Riesgo de concentración","fr":"Risque de concentration","de":"Konzentrationsrisiko","ja":"市場集中リスク","ko":"시장 집중 리스크"},
 "exp_four_numbers":{"zh":"📖 这四个数字分别说明什么？","en":"📖 What do these four numbers mean?","es":"📖 ¿Qué significan estas cuatro cifras?","fr":"📖 Que signifient ces quatre chiffres ?","de":"📖 Was sagen diese vier Zahlen aus?","ja":"📖 この4つの数字の意味","ko":"📖 이 네 숫자의 의미"},
 "m_total_mcap":{"zh":"预期总市值","en":"Expected total market cap","es":"Cap. de mercado prevista","fr":"Capitalisation attendue","de":"Erwartete Marktkap.","ja":"想定時価総額","ko":"예상 시가총액"},
 "m_total_mcap_d":{"zh":"12大待上市公司","en":"12 upcoming listings","es":"12 próximas salidas","fr":"12 introductions à venir","de":"12 anstehende Börsengänge","ja":"上場予定12社","ko":"상장 예정 12개사"},
 "m_q1_raise":{"zh":"Q1 2026 融资额","en":"Q1 2026 capital raised","es":"Capital captado Q1 2026","fr":"Levées de fonds T1 2026","de":"Kapital Q1 2026","ja":"2026年Q1 調達額","ko":"2026 Q1 조달액"},
 "m_q1_raise_d":{"zh":"同比 +45%","en":"+45% YoY","es":"+45% interanual","fr":"+45% sur un an","de":"+45% ggü. Vorjahr","ja":"前年比 +45%","ko":"전년比 +45%"},
 "m_ai_share":{"zh":"AI占风投比例","en":"AI share of VC funding","es":"Peso de la IA en el capital riesgo","fr":"Part de l'IA dans le capital-risque","de":"KI-Anteil am Wagniskapital","ja":"VC投資に占めるAI比率","ko":"VC 투자 중 AI 비중"},
 "m_ai_share_d":{"zh":"泡沫风险高","en":"High bubble risk","es":"Alto riesgo de burbuja","fr":"Risque de bulle élevé","de":"Hohes Blasenrisiko","ja":"バブルリスク高","ko":"버블 리스크 높음"},
 "m_bubble_idx":{"zh":"泡沫综合指数","en":"Composite bubble index","es":"Índice compuesto de burbuja","fr":"Indice composite de bulle","de":"Blasen-Gesamtindex","ja":"バブル総合指数","ko":"버블 종합 지수"},
 "m_bubble_idx_d":{"zh":"⚠ 高度警戒","en":"⚠ High alert","es":"⚠ Alerta alta","fr":"⚠ Alerte élevée","de":"⚠ Hohe Warnstufe","ja":"⚠ 高度警戒","ko":"⚠ 높은 경계"},
 # IPO 四个数字的解读
 "ipo_w1_t":{"zh":"预期总市值 $3.12T","en":"Expected total market cap $3.12T"},
 "ipo_w1":{"zh":"把2026年12家待上市公司的最新一轮估值加总得到。$3.12万亿这个体量本身就是信号——相当于一次性要市场消化掉一个「英伟达级别」的市值，而这些公司绝大多数还没有稳定盈利。",
   "en":"This is the sum of the latest private valuations of the 12 companies queued to list in 2026. The $3.12 trillion figure is itself the signal: the market would have to absorb an NVIDIA-sized market cap in one wave, and most of these companies are not yet reliably profitable."},
 "ipo_w2_t":{"zh":"Q1融资额 $42.6B 同比+45%","en":"Q1 raise $42.6B, +45% YoY"},
 "ipo_w2":{"zh":"一级市场融资额同比大增45%，说明资金正在加速涌入Pre-IPO阶段。融资越容易，公司上市时的估值起点就越高，留给二级市场投资者的安全边际也就越薄。",
   "en":"Private-market funding is up 45% year on year, meaning capital is rushing into the pre-IPO stage. The easier it is to raise, the higher the valuation companies start from when they list — and the thinner the margin of safety left for public investors."},
 "ipo_w3_t":{"zh":"AI占风投比例 80%","en":"AI is 80% of VC funding"},
 "ipo_w3":{"zh":"每100元风险投资里有80元投向AI。这个集中度在历史上只有2000年的互联网和2021年的SPAC可比——**赛道越拥挤，一旦叙事证伪，资金同时撤离造成的踩踏就越严重**。",
   "en":"Eighty of every hundred venture dollars go to AI. Historically only the 2000 dot-com era and the 2021 SPAC wave were this concentrated — **the more crowded a theme, the worse the stampede when the story is disproved and everyone exits at once**."},
 "ipo_w4_t":{"zh":"泡沫综合指数 74/100","en":"Composite bubble index 74/100"},
 "ipo_w4":{"zh":"由估值倍数（P/S）、盈利覆盖率、资金集中度和锁定期抛压四项加权得到。74分落在「高度警戒」区间（70以上），意味着当前定价已经把很多乐观假设提前兑现了。",
   "en":"A weighted blend of valuation multiples (P/S), earnings coverage, capital concentration and lock-up selling pressure. A score of 74 sits in the \u201chigh alert\u201d band (above 70), meaning today's prices already bake in a lot of optimistic assumptions."},
 # 集中度风险五项
 "conc_ai_t":{"zh":"AI估值集中","en":"AI valuation concentration"},
 "conc_ai":{"zh":"衡量市值有多少集中在少数AI标的上。88%意味着整个板块的涨跌几乎由几家公司决定，分散投资在这里失效了。",
   "en":"Measures how much market cap sits in a handful of AI names. At 88%, the sector's direction is decided by just a few companies — diversification stops working here."},
 "conc_liq_t":{"zh":"流动性压力","en":"Liquidity pressure"},
 "conc_liq":{"zh":"衡量市场有没有足够的资金接住这些新股。79%说明在高利率环境下，能承接$3万亿新增供给的增量资金并不充裕。",
   "en":"Measures whether there is enough money to absorb the new supply. At 79%, a high-rate environment simply does not have abundant incremental capital to take down $3 trillion of new issuance."},
 "conc_prof_t":{"zh":"盈利能力缺口","en":"Profitability gap"},
 "conc_prof":{"zh":"待上市公司中亏损企业的占比与亏损幅度。72%说明大部分标的的估值靠的是远期预期，而不是当期利润。",
   "en":"The share and depth of losses among companies queued to list. At 72%, most of these valuations rest on distant expectations rather than current profits."},
 "conc_lock_t":{"zh":"锁定期后抛压","en":"Post-lock-up selling pressure"},
 "conc_lock":{"zh":"IPO后约180天锁定期到期时，早期投资者和员工可抛售的股份占比。65%属于偏高水平，通常对应解禁后的一波明显回调。",
   "en":"The share of stock early investors and employees can sell once the ~180-day lock-up expires. 65% is on the high side and usually maps to a visible pullback after unlock."},
 "conc_absorb_t":{"zh":"市场吸收能力","en":"Market absorption capacity"},
 "conc_absorb":{"zh":"市场实际能消化多少新增供给。42%是唯一的低分项——**分数越低越危险**，说明供给远超需求承接力。",
   "en":"How much new supply the market can actually digest. 42% is the only low reading here — and **lower is worse**: supply far outstrips the demand available to absorb it."},
 "why_default":{"zh":"为什么是这个结果","en":"Why this result","es":"Por qué este resultado","fr":"Pourquoi ce résultat","de":"Warum dieses Ergebnis","ja":"なぜこの結果になるか","ko":"왜 이런 결과인가"},
 "why_score_src":{"zh":"这个分数怎么来的","en":"How this score is computed","es":"Cómo se calcula","fr":"Comment ce score est calculé","de":"Wie dieser Wert entsteht","ja":"このスコアの算出方法","ko":"이 점수의 산출 방식"},
 "why_overall":{"zh":"整体怎么看","en":"The big picture","es":"Visión general","fr":"Vue d'ensemble","de":"Gesamtbild","ja":"全体の見方","ko":"전체적으로 보면"},
 "why_howto_read":{"zh":"怎么读这张图","en":"How to read this chart","es":"Cómo leer este gráfico","fr":"Comment lire ce graphique","de":"So liest man diese Grafik","ja":"このグラフの読み方","ko":"이 차트 읽는 법"},
 "exp_read_each":{"zh":"📖 每个指标怎么读？（点开看每个数字为什么是这样）","en":"📖 How to read each indicator (why every number looks the way it does)","es":"📖 Cómo leer cada indicador","fr":"📖 Comment lire chaque indicateur","de":"📖 Wie man jeden Indikator liest","ja":"📖 各指標の読み方","ko":"📖 각 지표 읽는 법"},
 "exp_read_coin":{"zh":"📖 每个币怎么读？","en":"📖 How to read each coin","es":"📖 Cómo leer cada cripto","fr":"📖 Comment lire chaque crypto","de":"📖 Wie man jede Kryptowährung liest","ja":"📖 各通貨の読み方","ko":"📖 각 코인 읽는 법"},
 "exp_read_metal":{"zh":"📖 每个品种怎么读？","en":"📖 How to read each metal","es":"📖 Cómo leer cada metal","fr":"📖 Comment lire chaque métal","de":"📖 Wie man jedes Metall liest","ja":"📖 各銘柄の読み方","ko":"📖 각 품목 읽는 법"},
 "crypto_overall":{"zh":"加密市场整体 **{mood}**，平均涨跌 {avg:+.2f}%。加密资产没有现金流估值锚，价格几乎完全由流动性和风险偏好驱动，所以它常常是市场情绪的**放大版**——美联储宽松时涨得比纳斯达克更凶，收紧时也跌得更深。",
   "en":"Crypto overall: **{mood}**, average move {avg:+.2f}%. Crypto has no cash-flow valuation anchor, so price is driven almost entirely by liquidity and risk appetite — it tends to be an **amplified version** of equity sentiment, rallying harder than the Nasdaq when the Fed eases and falling further when it tightens."},
 "mood_up":{"zh":"🔥 普遍上涨，风险偏好回升","en":"🔥 broadly higher, risk appetite returning"},
 "mood_dn":{"zh":"📉 普遍下跌，避险情绪升温","en":"📉 broadly lower, risk-off building"},
 "mood_flat":{"zh":"⚖️ 涨跌互现，方向不明","en":"⚖️ mixed, no clear direction"},
 "metal_overall":{"zh":"板块平均 {avg:+.2f}%。有色金属有两条独立的定价逻辑：**贵金属（金/银）看实际利率和避险需求**——实际利率下行或地缘冲突升温时走强；**工业金属（铜）看全球经济需求**——电动车、电网升级和数据中心建设是长期需求来源。所以金涨铜跌通常意味着市场在担心衰退，金铜齐涨则多半是通胀预期在升温。",
   "en":"Sector average {avg:+.2f}%. Metals price off two separate engines: **precious metals (gold/silver) follow real rates and safe-haven demand**, strengthening when real rates fall or geopolitical risk rises; **industrial metals (copper) follow global demand**, with EVs, grid upgrades and data centres as the long-run drivers. So gold up with copper down usually signals recession worry, while both rising together typically means inflation expectations are heating up."},
 "crypto_hint":{"zh":"可在「🔬 股票分析器」或「💰 我的持仓」输入 BTC-USD / ETH-USD 等代码查看详细技术面分析",
   "en":"Enter tickers like BTC-USD / ETH-USD in the Stock Analyzer or My Holdings for full technical analysis"},
 "unit_sec":{"zh":"{n} 秒","en":"{n} sec","es":"{n} s","fr":"{n} s","de":"{n} Sek.","ja":"{n} 秒","ko":"{n}초"},
 "unit_min":{"zh":"{n} 分钟","en":"{n} min","es":"{n} min","fr":"{n} min","de":"{n} Min.","ja":"{n} 分","ko":"{n}분"},
 "watch_start_short":{"zh":"👀 开始盯盘","en":"👀 Start watching","es":"👀 Vigilar","fr":"👀 Surveiller","de":"👀 Beobachten","ja":"👀 監視開始","ko":"👀 관찰 시작"},
 "watch_bar_on":{"zh":"🟢 盯盘中 · 每 {iv} 秒自动刷新 · 剩余 {mm}:{ss} · 已刷新 {n} 次",
   "en":"🟢 Watching · refresh every {iv}s · {mm}:{ss} left · {n} refreshes",
   "es":"🟢 Vigilando · cada {iv}s · quedan {mm}:{ss} · {n} actualizaciones",
   "fr":"🟢 Surveillance · toutes les {iv}s · {mm}:{ss} restantes · {n} actualisations",
   "de":"🟢 Aktiv · alle {iv}s · {mm}:{ss} übrig · {n} Aktualisierungen",
   "ja":"🟢 監視中 · {iv}秒ごと更新 · 残り {mm}:{ss} · {n}回更新",
   "ko":"🟢 관찰 중 · {iv}초마다 갱신 · {mm}:{ss} 남음 · {n}회 갱신"},
 "watch_bar_off":{"zh":"⚪ 手动模式：数据只在你操作时更新。点「开始盯盘」后会每 {iv} 秒自动刷新一次，{mn} 分钟后自动停止（可在左侧边栏调整）。",
   "en":"⚪ Manual mode: data updates only when you interact. Hit \u201cStart watching\u201d to auto-refresh every {iv}s, stopping automatically after {mn} min (adjustable in the sidebar).",
   "es":"⚪ Modo manual: los datos solo se actualizan al interactuar. Pulse \u201cVigilar\u201d para actualizar cada {iv}s durante {mn} min.",
   "fr":"⚪ Mode manuel : les données ne changent qu\u2019à votre action. Cliquez sur \u00ab Surveiller \u00bb pour actualiser toutes les {iv}s pendant {mn} min.",
   "de":"⚪ Manueller Modus: Daten ändern sich nur bei Interaktion. \u201eBeobachten\u201c aktualisiert alle {iv}s für {mn} Min.",
   "ja":"⚪ 手動モード：操作時のみ更新。「監視開始」で {iv} 秒ごとに自動更新し、{mn} 分後に自動停止します。",
   "ko":"⚪ 수동 모드: 조작할 때만 갱신됩니다. \u201c관찰 시작\u201d을 누르면 {iv}초마다 갱신되고 {mn}분 후 자동 중지됩니다."},


 "i18n_note": {
   "zh":"界面已切换语言；部分深度分析正文暂以英文呈现。",
   "en":"Interface translated. Some in-depth analysis text is shown in English.",
   "es":"Interfaz traducida. Parte del análisis detallado se muestra en inglés.",
   "fr":"Interface traduite. Une partie de l\u2019analyse détaillée s\u2019affiche en anglais.",
   "de":"Oberfläche übersetzt. Teile der ausführlichen Analyse erscheinen auf Englisch.",
   "ja":"インターフェースを翻訳しました。詳細な分析の一部は英語で表示されます。",
   "ko":"인터페이스가 번역되었습니다. 상세 분석의 일부는 영어로 표시됩니다."},

 "hg_rf_note": {
   "zh":"α 为 Jensen's Alpha，已扣除无风险利率（10年期美债 {rf:.2f}%）：α = (Rp − rf) − β(Rm − rf)",
   "en":"α is Jensen's alpha, net of the risk-free rate (10Y Treasury {rf:.2f}%): α = (Rp − rf) − β(Rm − rf)",
   "es":"α es el alfa de Jensen, neto de la tasa libre de riesgo ({rf:.2f}%).",
   "fr":"α est l\u2019alpha de Jensen, net du taux sans risque ({rf:.2f}%).",
   "de":"α ist Jensens Alpha, abzüglich des risikofreien Zinssatzes ({rf:.2f}%).",
   "ja":"α はジェンセンのアルファで、無リスク金利（{rf:.2f}%）を控除しています。",
   "ko":"α는 젠센의 알파이며, 무위험 수익률({rf:.2f}%)을 차감했습니다."},

 "hg_wmode_label": {"zh":"权重方式","en":"Weighting","es":"Ponderación","fr":"Pondération",
   "de":"Gewichtung","ja":"ウェイト","ko":"가중 방식"},
 "hg_wmode_eq": {"zh":"等权（每个标的一样多）","en":"Equal weight","es":"Equiponderado",
   "fr":"Équipondéré","de":"Gleichgewichtet","ja":"等ウェイト","ko":"동일 비중"},
 "hg_wmode_mv": {"zh":"按我的持仓市值","en":"By my position sizes","es":"Por el tamaño de mis posiciones",
   "fr":"Selon la taille de mes positions","de":"Nach meinen Positionsgrößen",
   "ja":"保有時価に応じて","ko":"보유 시가 기준"},
 "hg_wmode_help": {
   "zh":"等权假设你在每个标的上投了一样多的钱。如果你实际是重仓一两只，等权会明显低估组合的真实波动——务必切到「按我的持仓市值」。",
   "en":"Equal weight assumes you put the same amount into every asset. If you are actually concentrated in one or two names, equal weight badly understates your true portfolio volatility — switch to position sizes.",
   "es":"El equiponderado asume la misma cantidad en cada activo; si estás concentrado, subestima tu volatilidad real.",
   "fr":"L\u2019équipondération suppose le même montant sur chaque actif ; si vous êtes concentré, elle sous-estime votre volatilité réelle.",
   "de":"Gleichgewichtung unterstellt denselben Betrag je Position; bei Konzentration unterschätzt sie Ihre echte Volatilität.",
   "ja":"等ウェイトは各銘柄に同額を投じた前提です。集中している場合、実際のボラティリティを大きく過小評価します。",
   "ko":"동일 비중은 모든 종목에 같은 금액을 넣었다고 가정합니다. 집중 투자 시 실제 변동성을 크게 과소평가합니다."},
 "hg_wmode_nomv": {
   "zh":"还没有可用的持仓市值，请先到「💰 我的持仓」页录入并等待行情加载，这里才能按真实权重计算。",
   "en":"No position values available yet — add positions on the 💰 My Holdings tab and let prices load first.",
   "es":"Aún no hay valores de posiciones; añádelas en la pestaña Mi Cartera.",
   "fr":"Aucune valeur de position disponible ; ajoutez-les dans l\u2019onglet Mon Portefeuille.",
   "de":"Noch keine Positionswerte vorhanden; bitte im Depot-Tab erfassen.",
   "ja":"保有時価がまだありません。「💰 保有銘柄」タブで入力してください。",
   "ko":"보유 시가가 아직 없습니다. 「💰 내 보유」 탭에서 먼저 입력하세요."},
 "hg_wmode_active": {"zh":"当前权重：{w}","en":"Weights in use: {w}","es":"Pesos: {w}",
   "fr":"Pondérations : {w}","de":"Verwendete Gewichte: {w}","ja":"適用ウェイト：{w}","ko":"적용 비중: {w}"},
 "hg_mv_missing": {
   "zh":"⚠️ {tks} 不在你的持仓里，市值按 0 处理（相当于没有配置），只影响权重不影响相关性。",
   "en":"⚠️ {tks} are not in your holdings, so they carry zero weight here — correlations are unaffected.",
   "es":"⚠️ {tks} no están en tu cartera: peso cero.",
   "fr":"⚠️ {tks} ne sont pas dans votre portefeuille : pondération nulle.",
   "de":"⚠️ {tks} sind nicht im Depot und erhalten Gewicht null.",
   "ja":"⚠️ {tks} は保有していないためウェイト0として扱います。",
   "ko":"⚠️ {tks}는 보유 종목이 아니므로 비중 0으로 처리됩니다."},
 "hg_eff_conc": {
   "zh":"　另外，只看权重集中度（不考虑相关性），你这份持仓相当于只持有 **{conc:.1f}** 个标的；如果改成等权，有效分散数会是 **{eq:.1f}**。",
   "en":"　Looking at weight concentration alone (ignoring correlation), your portfolio is equivalent to holding just **{conc:.1f}** assets; equally weighted, the effective-bets figure would be **{eq:.1f}**.",
   "es":"　Solo por concentración de pesos, equivale a tener **{conc:.1f}** activos; equiponderado sería **{eq:.1f}**.",
   "fr":"　Par la seule concentration des pondérations, cela équivaut à détenir **{conc:.1f}** actifs ; équipondéré ce serait **{eq:.1f}**.",
   "de":"　Allein nach Gewichtskonzentration entspricht das **{conc:.1f}** Positionen; gleichgewichtet wären es **{eq:.1f}**.",
   "ja":"　ウェイト集中度だけで見ると実質 **{conc:.1f}** 銘柄相当です。等ウェイトなら **{eq:.1f}** になります。",
   "ko":"　비중 집중도만 보면 실질 **{conc:.1f}**개 종목에 해당합니다. 동일 비중이라면 **{eq:.1f}**입니다."},

 "hg_mode_eq_n": {"zh":"等权组合","en":"the equal-weighted portfolio","es":"la cartera equiponderada",
   "fr":"le portefeuille équipondéré","de":"das gleichgewichtete Depot","ja":"等ウェイトの組み合わせ",
   "ko":"동일 비중 포트폴리오"},
 "hg_mode_mv_n": {"zh":"你的实际持仓","en":"your actual portfolio","es":"tu cartera real",
   "fr":"votre portefeuille réel","de":"Ihr tatsächliches Depot","ja":"実際の保有ポートフォリオ",
   "ko":"실제 보유 포트폴리오"},


 "bub_clamped": {
   "zh":"⚠️ 注意：分项贡献加总为 **{raw:.0f}%**，但模型把破裂概率锁在 5–95% 之间，所以头条显示 **{shown}%**。当前行情已经把模型推到量程边缘，这时的数字只说明「极端」，精确到个位没有意义。",
   "en":"⚠️ Note: the itemised contributions sum to **{raw:.0f}%**, but the model caps burst probability at 5–95%, so the headline shows **{shown}%**. Conditions have pushed the model to the edge of its range — read the number as \u201cextreme\u201d rather than precise."},

 "bub_label_from": {"zh":"← 这一档由破裂概率 {b}% 决定，与左侧温度是两个数",
   "en":"← this band comes from the {b}% burst probability, not the temperature on the left"},

 "ipo_asof": {
   "zh":"ℹ️ 下列估值、收入与递交状态为**手工整理的静态数据**（数据截至 {d}），非实时行情；已上市公司的价格在上方实时区。",
   "en":"ℹ️ The valuations, revenues and filing statuses below are **manually maintained static data** (as of {d}), not live quotes. Prices for listed companies appear in the live section above."},
 "ipo_asof_old": {
   "zh":"⚠️ 下列 IPO 数据最后更新于 {d}，距今已 {n} 天，很可能已经过时——估值、收入和上市进度请以最新公开信息为准。",
   "en":"⚠️ The IPO data below was last updated on {d}, {n} days ago, and is likely stale — check current public filings for valuations, revenue and timing."},

 "rev_runrate": {
   "zh":"年化跑步收入（最新月×12），非财年实际收入",
   "en":"Annualised run rate (latest month ×12), not a full fiscal year"},
 "rev_fy": {"zh":"上一财年实际收入","en":"Last full fiscal year"},
 "ps_basis_note": {
   "zh":"⚠️ P/S 倍数的分母口径并不统一：已上市公司用的是财年实际收入，尚未上市的 AI 公司只能拿到**年化跑步收入**（增长极快时会显著压低 P/S）。跨公司比较这一项时请留意。",
   "en":"⚠️ The P/S denominators are not on a common basis: listed companies use actual fiscal-year revenue, while the private AI companies only disclose an **annualised run rate**, which flatters P/S when growth is fast. Keep that in mind when comparing across names."},
 # ── 当前泡沫读数（自动） ──
 "bub_now_title": {"zh":"### 🌡️ 当前泡沫程度（实时自动测算）",
   "en":"### 🌡️ Current bubble reading (computed live)"},
 "bub_now_cap": {
   "zh":"下面这个读数不需要你做任何操作——它每次打开页面都会用当时的实时行情重新算一遍。四项输入全部来自公开市场数据，每一项对结果的贡献都在下方逐条列出。",
   "en":"This reading needs no input from you — it is recomputed from live market data every time the page loads. All four inputs come from public market data, and each one's contribution is itemised below."},
 "bub_temp": {"zh":"泡沫温度","en":"Bubble temperature"},
 "bub_burst": {"zh":"12个月内破裂概率","en":"Probability of bursting within 12m"},
 "bub_pop": {"zh":"新股首日预期涨幅","en":"Expected IPO first-day pop"},
 "bub_six": {"zh":"6个月后预期收益","en":"Expected 6-month return"},
 "bub_why_title": {"zh":"#### 🔍 为什么是这个数——逐项拆解",
   "en":"#### 🔍 Why this number — factor by factor"},
 "bub_why_cap": {
   "zh":"泡沫温度 = 情绪×0.4 + AI速度×0.3 + 散户热度×0.2 + (100−利率×8)×0.1　·　破裂概率 = 100 − 情绪×0.4 − AI速度×0.2 + 利率×6 − 散户热度×0.05",
   "en":"Temperature = sentiment×0.4 + AI×0.3 + retail×0.2 + (100−rate×8)×0.1　·　Burst = 100 − sentiment×0.4 − AI×0.2 + rate×6 − retail×0.05"},
 "bub_col_factor": {"zh":"因子","en":"Factor"},
 "bub_col_live": {"zh":"当前实时值","en":"Live value"},
 "bub_col_temp": {"zh":"对温度的贡献","en":"→ temperature"},
 "bub_col_burst": {"zh":"对破裂概率的贡献","en":"→ burst risk"},

 "bub_f_sentiment": {"zh":"市场情绪","en":"Market sentiment"},
 "bub_f_ai": {"zh":"AI 商业化速度","en":"AI commercialisation pace"},
 "bub_f_retail": {"zh":"散户参与热度","en":"Retail participation"},
 "bub_f_rate": {"zh":"利率环境","en":"Interest-rate environment"},

 "bub_d_sentiment": {
   "zh":"由 VIX、纳斯达克与英伟达当日涨跌实时算出（拆解见下）。情绪越高，说明市场越愿意为高估值买单，泡沫温度越高、短期破裂概率越低——但这份「低概率」本身就是泡沫的特征。",
   "en":"Computed live from VIX plus today's Nasdaq and Nvidia moves (broken out below). Higher sentiment means the market is more willing to pay up, which raises temperature and lowers near-term burst odds — though that very complacency is what a bubble looks like."},
 "bub_d_ai": {
   "zh":"用 AI 权重股（NVDA/MSFT/GOOGL/META/AMD/AVGO）相对标普500的 **3个月超额收益 {ex:+.1f}%** 换算：市场愿意为 AI 叙事付多少溢价，就代表它对商业化兑现速度的预期。跑赢越多，分数越高。",
   "en":"Derived from the AI mega-caps' (NVDA/MSFT/GOOGL/META/AMD/AVGO) **3-month excess return of {ex:+.1f}%** versus the S&P 500: how much premium the market pays for the AI story stands in for how fast it expects commercialisation to arrive."},
 "bub_d_ai_off": {
   "zh":"⚠️ 实时数据取不到，暂用中性值 60。这一项不影响其余三项的准确性。",
   "en":"⚠️ Live data unavailable, falling back to a neutral 60. The other three factors are unaffected."},
 "bub_d_retail": {
   "zh":"用 VIX 反推（100 − VIX×2）：市场越平静，散户越敢追高。**这是代理指标，不是真实的散户持仓数据**——公开数据里拿不到实时散户流向，所以只能用波动率做近似。",
   "en":"Inferred from VIX (100 − VIX×2): the calmer the market, the more retail chases. **This is a proxy, not actual retail positioning data** — real-time retail flow is not publicly available, so volatility stands in for it."},
 "bub_d_rate": {
   "zh":"取 10 年期美债收益率。**这是模型里权重最高的破裂因子（×6）**——历史上刺破泡沫的几乎都是利率上行：2000年互联网、2021年SPAC都是这样结束的。利率每涨1个百分点，破裂概率就加6。",
   "en":"The US 10-year Treasury yield. **This carries the heaviest weight on burst risk (×6)** — historically it is rising rates that pop bubbles: both the 2000 dot-com and 2021 SPAC manias ended that way. Every extra percentage point adds 6 to the burst probability."},

 "bub_sent_break": {"zh":"情绪分 {s}/100 的来源：从中性 50 起算",
   "en":"Where the {s}/100 sentiment comes from: starting from a neutral 50"},
 "bub_p_vix_lo": {"zh":"VIX {v} 偏低，市场几乎没有恐慌情绪",
   "en":"VIX at {v} is low — the market shows little fear"},
 "bub_p_vix_hi": {"zh":"VIX {v} 偏高，避险情绪明显",
   "en":"VIX at {v} is elevated — risk aversion is visible"},
 "bub_p_idx": {"zh":"纳斯达克当日 {v}（权重 ×3）","en":"Nasdaq today {v} (weight ×3)"},
 "bub_p_nvda": {"zh":"英伟达当日 {v}（权重 ×2，作为 AI 情绪的风向标）",
   "en":"Nvidia today {v} (weight ×2, as the AI sentiment bellwether)"},

 "bub_verdict": {"zh":"当前判定","en":"Current read"},
 "bub_nodata": {"zh":"⚠️ 暂时取不到实时行情，下面的读数可能不准，请稍后刷新。",
   "en":"⚠️ Live market data is unavailable right now; the reading below may be stale."},
 "bub_whatif": {"zh":"🎛️ 想试试别的情景？下面可以手动改参数",
   "en":"🎛️ Want to test other scenarios? Adjust the inputs manually below"},
 "bub_whatif_cap": {
   "zh":"上面是**现状**，下面是**假设**。手动模式用来回答「如果利率再涨1%会怎样」这类问题，改动不影响上面的实时读数。",
   "en":"Above is what is actually happening; below is what-if. Manual mode answers questions like \u201cwhat if rates rise another point\u201d, and does not affect the live reading above."},
 "bub_refresh": {"zh":"🔄 重新测算","en":"🔄 Recompute"},
 # ── 免责声明折叠 ──
 "disc_more": {"zh":"查看完整免责声明","en":"Read the full disclaimer","es":"Ver el aviso legal completo",
   "fr":"Lire l’avertissement complet","de":"Vollständigen Haftungsausschluss lesen",
   "ja":"免責事項の全文を読む","ko":"전체 면책 조항 보기"},

 # ── 持仓存档 / 导入导出 ──
 "pf_io_title": {"zh":"💾 持仓存档 · 导出 / 导入 / 分享链接","en":"💾 Save, restore & share this portfolio",
   "es":"💾 Guardar, restaurar y compartir la cartera","fr":"💾 Sauvegarder, restaurer et partager le portefeuille",
   "de":"💾 Depot sichern, laden & teilen","ja":"💾 保有銘柄の保存・復元・共有",
   "ko":"💾 보유 종목 저장·복원·공유"},
 "pf_io_hint": {"zh":"⚠️ 持仓只保存在当前浏览器会话里，**刷新页面就会丢失**。导出存档文件，或生成分享链接后收藏，即可长期保存、换设备继续用。",
   "en":"⚠️ Your positions live only in this browser session and **are lost when the page reloads**. Export a save file, or generate a share link and bookmark it, to keep them permanently and reopen them on any device.",
   "es":"⚠️ Tus posiciones solo existen en esta sesión del navegador y **se pierden al recargar**. Exporta un archivo o genera un enlace y guárdalo en favoritos.",
   "fr":"⚠️ Vos positions n’existent que dans cette session et **sont perdues au rechargement**. Exportez un fichier ou générez un lien à mettre en favori.",
   "de":"⚠️ Ihre Positionen existieren nur in dieser Browser-Sitzung und **gehen beim Neuladen verloren**. Exportieren Sie eine Datei oder erzeugen Sie einen Link als Lesezeichen.",
   "ja":"⚠️ 保有銘柄はこのブラウザセッションにのみ保存され、**再読み込みで失われます**。ファイルを書き出すか、共有リンクを作成してブックマークしてください。",
   "ko":"⚠️ 보유 종목은 현재 브라우저 세션에만 저장되어 **새로고침하면 사라집니다**. 파일로 내보내거나 공유 링크를 만들어 즐겨찾기에 저장하세요."},
 "pf_export": {"zh":"💾 导出存档","en":"💾 Export save file","es":"💾 Exportar archivo","fr":"💾 Exporter le fichier",
   "de":"💾 Datei exportieren","ja":"💾 ファイルを書き出す","ko":"💾 파일 내보내기"},
 "pf_export_h": {"zh":"下载一个 .json 存档文件，之后用「导入存档」即可完整恢复",
   "en":"Downloads a .json save file you can restore later with Import","es":"Descarga un .json restaurable con Importar",
   "fr":"Télécharge un .json restaurable via Importer","de":"Lädt eine .json-Datei, die per Import wiederhergestellt wird",
   "ja":"後で「読み込む」で復元できる .json を保存します","ko":"나중에 가져오기로 복원할 수 있는 .json 파일을 저장합니다"},
 "pf_import": {"zh":"📂 导入存档","en":"📂 Import save file","es":"📂 Importar archivo","fr":"📂 Importer un fichier",
   "de":"📂 Datei importieren","ja":"📂 ファイルを読み込む","ko":"📂 파일 가져오기"},
 "pf_import_ok": {"zh":"✅ 已导入 {n} 个持仓","en":"✅ Imported {n} positions","es":"✅ {n} posiciones importadas",
   "fr":"✅ {n} positions importées","de":"✅ {n} Positionen importiert","ja":"✅ {n} 件の保有銘柄を読み込みました",
   "ko":"✅ {n}개 보유 종목을 가져왔습니다"},
 "pf_import_err": {"zh":"⚠️ 无法读取该存档文件：{err}","en":"⚠️ Could not read that save file: {err}",
   "es":"⚠️ No se pudo leer el archivo: {err}","fr":"⚠️ Impossible de lire ce fichier : {err}",
   "de":"⚠️ Datei konnte nicht gelesen werden: {err}","ja":"⚠️ ファイルを読み込めませんでした：{err}",
   "ko":"⚠️ 파일을 읽을 수 없습니다: {err}"},
 "pf_link": {"zh":"🔗 生成分享链接","en":"🔗 Create share link","es":"🔗 Crear enlace","fr":"🔗 Créer un lien",
   "de":"🔗 Link erzeugen","ja":"🔗 共有リンクを作成","ko":"🔗 공유 링크 만들기"},
 "pf_link_h": {"zh":"把持仓编码进网址，收藏该网址即可随时恢复","en":"Encodes the portfolio into the URL — bookmark it to restore anytime",
   "es":"Codifica la cartera en la URL — guárdala en favoritos","fr":"Encode le portefeuille dans l’URL — mettez-la en favori",
   "de":"Codiert das Depot in die URL — als Lesezeichen speichern","ja":"保有銘柄をURLに埋め込みます。ブックマークすれば復元できます",
   "ko":"보유 종목을 URL에 인코딩합니다. 즐겨찾기하면 복원됩니다"},
 "pf_link_done": {"zh":"✅ 链接已写入浏览器地址栏 —— 直接复制地址栏，或按 Ctrl/Cmd+D 收藏。换设备打开这个网址，持仓会自动恢复。",
   "en":"✅ The link is now in your address bar — copy it, or press Ctrl/Cmd+D to bookmark. Opening that URL on any device restores this portfolio.",
   "es":"✅ El enlace está en la barra de direcciones — cópialo o pulsa Ctrl/Cmd+D.",
   "fr":"✅ Le lien est dans la barre d’adresse — copiez-le ou faites Ctrl/Cmd+D.",
   "de":"✅ Der Link steht in der Adresszeile — kopieren oder mit Strg/Cmd+D speichern.",
   "ja":"✅ リンクがアドレスバーに反映されました。コピーするか Ctrl/Cmd+D でブックマークしてください。",
   "ko":"✅ 링크가 주소창에 반영되었습니다. 복사하거나 Ctrl/Cmd+D로 즐겨찾기하세요."},
 "pf_link_clear": {"zh":"🧹 清除链接参数","en":"🧹 Clear link","es":"🧹 Borrar enlace","fr":"🧹 Effacer le lien",
   "de":"🧹 Link entfernen","ja":"🧹 リンクを消す","ko":"🧹 링크 지우기"},
 "pf_from_url": {"zh":"🔗 已从分享链接恢复 {n} 个持仓","en":"🔗 Restored {n} positions from the share link",
   "es":"🔗 {n} posiciones restauradas desde el enlace","fr":"🔗 {n} positions restaurées depuis le lien",
   "de":"🔗 {n} Positionen aus dem Link wiederhergestellt","ja":"🔗 共有リンクから {n} 件を復元しました",
   "ko":"🔗 공유 링크에서 {n}개를 복원했습니다"},

 # ── 报告下载 ──
 "rep_title": {"zh":"#### 📄 导出分析报告","en":"#### 📄 Export this analysis","es":"#### 📄 Exportar el análisis",
   "fr":"#### 📄 Exporter cette analyse","de":"#### 📄 Analyse exportieren","ja":"#### 📄 分析結果を書き出す",
   "ko":"#### 📄 분석 결과 내보내기"},
 "rep_hint": {"zh":"把本页算出来的全部结论打包带走 —— 报告含盈亏归因、长期评估与赛道判断，明细表可直接拖进 Excel。",
   "en":"Take everything on this page with you — the report carries the P&L attribution, long-term verdicts and sector calls; the table opens straight in Excel.",
   "es":"Llévate todo lo de esta página — el informe incluye atribución de P&L y veredictos; la tabla abre en Excel.",
   "fr":"Emportez tout le contenu de cette page — le rapport contient l’attribution du P&L et les verdicts ; le tableau s’ouvre dans Excel.",
   "de":"Nehmen Sie alles von dieser Seite mit — der Bericht enthält die GuV-Attribution und Bewertungen; die Tabelle öffnet sich in Excel.",
   "ja":"このページの結論をすべて持ち出せます。レポートには損益要因と長期評価、テーマ判定を含み、表はExcelでそのまま開けます。",
   "ko":"이 페이지의 모든 결론을 가져갈 수 있습니다. 리포트에는 손익 귀속과 장기 평가가 담기고, 표는 Excel에서 바로 열립니다."},
 "rep_dl_md": {"zh":"📄 下载分析报告 (Markdown)","en":"📄 Download report (Markdown)","es":"📄 Descargar informe (Markdown)",
   "fr":"📄 Télécharger le rapport (Markdown)","de":"📄 Bericht herunterladen (Markdown)",
   "ja":"📄 レポートを保存 (Markdown)","ko":"📄 리포트 저장 (Markdown)"},
 "rep_dl_csv": {"zh":"📊 下载持仓明细 (CSV)","en":"📊 Download positions (CSV)","es":"📊 Descargar posiciones (CSV)",
   "fr":"📊 Télécharger les positions (CSV)","de":"📊 Positionen herunterladen (CSV)",
   "ja":"📊 保有明細を保存 (CSV)","ko":"📊 보유 명세 저장 (CSV)"},
 "hg_dl_md": {"zh":"📄 下载分散化报告 (Markdown)","en":"📄 Download diversification report",
   "es":"📄 Descargar informe de diversificación","fr":"📄 Télécharger le rapport de diversification",
   "de":"📄 Diversifikationsbericht herunterladen","ja":"📄 分散化レポートを保存","ko":"📄 분산화 리포트 저장"},
 "hg_dl_csv": {"zh":"📊 下载相关性矩阵 (CSV)","en":"📊 Download correlation matrix (CSV)",
   "es":"📊 Descargar matriz de correlación","fr":"📊 Télécharger la matrice de corrélation",
   "de":"📊 Korrelationsmatrix herunterladen","ja":"📊 相関行列を保存 (CSV)","ko":"📊 상관행렬 저장 (CSV)"},
 "rep_gen_at": {"zh":"生成时间","en":"Generated","es":"Generado","fr":"Généré le","de":"Erstellt",
   "ja":"作成日時","ko":"생성 시각"},

}

# 标的显示名：非中文界面下使用英文名
ASSET_NAMES_EN = {
    "^IXIC":"NASDAQ Composite", "^GSPC":"S&P 500", "^VIX":"VIX Volatility Index",
    "^TNX":"US 10Y Treasury Yield", "^DJI":"Dow Jones", "SPCX":"SpaceX",
    "NVDA":"NVIDIA", "MSFT":"Microsoft", "GOOGL":"Alphabet", "META":"Meta", "AMZN":"Amazon",
    "BTC-USD":"Bitcoin", "ETH-USD":"Ethereum", "SOL-USD":"Solana", "BNB-USD":"BNB",
    "XRP-USD":"XRP", "DOGE-USD":"Dogecoin",
    "GC=F":"Gold Futures", "SI=F":"Silver Futures", "HG=F":"Copper Futures",
    "GDX":"Gold Miners ETF", "SLV":"Silver ETF", "FCX":"Freeport-McMoRan (Copper)",
}

def asset_name(ticker, zh_name):
    """中文界面用原中文名，其它语言优先用英文名"""
    if st.session_state.get("lang", "zh") == "zh":
        return zh_name
    return ASSET_NAMES_EN.get(ticker, ticker)

def _i18n_entry(key):
    """在两个文案字典里找 key。

    I18N 放界面文案、NARRATIVE 放分析正文，但历次翻译里有一批键登记错了
    字典，页面上就会直接漏出 "pnl_head" 这样的原始键名。两个字典没有任何
    重名，所以互相兜底既能一次性修好，也能防止以后再出现同类错误。
    """
    return I18N.get(key) or NARRATIVE.get(key) or {}


def _render(key, entry, kw):
    """按 当前语言 → 英文 → 中文 的顺序取文案，并套用格式化参数"""
    lang = st.session_state.get("lang", "zh")
    s = (entry.get(lang)
         or (entry.get("en") if lang != "zh" else None)
         or entry.get("zh")
         or key)
    try:
        return s.format(**kw) if kw else s
    except Exception:
        return s


def _nolatex(text):
    """转义 $，避免 Streamlit 把它当成 LaTeX 行内公式。

    Streamlit 的 Markdown 支持 $...$ 数学公式，所以像
    "发行价$135，首日收盘$161" 这样的文案里两个 $ 会被配成一对，
    中间的文字被当作公式渲染，整段就花了。本站不用 LaTeX，
    凡是走纯 Markdown 渲染的文本都先过一遍这个函数。
    （unsafe_allow_html=True 的调用走 HTML 渲染，不受影响。）
    """
    return str(text).replace("$", "\\$")


def tr(key, **kw):
    """取当前语言的界面文案；缺失时回退英文再回退中文"""
    return _render(key, _i18n_entry(key), kw)


# ══════════════════════════════════════════════════════════════════════════════
# 📝 分析正文翻译层：英文已完成；其余语言暂回退英文（中文界面始终用中文）
# ══════════════════════════════════════════════════════════════════════════════
NARRATIVE = {
 # ── VIX ──
 "vix_low":{"zh":"VIX 现在 {p:.2f}，处在**极低区间（低于13）**。它衡量的是标普500未来30天的预期波动，这么低说明几乎没人花钱买下跌保险、市场偏自满——历史上这种时候一旦有利空，回调反而更猛。",
   "en":"VIX is {p:.2f}, in the **very low zone (below 13)**. VIX measures expected S&P 500 volatility over the next 30 days, and a reading this low means almost nobody is paying for downside protection — the market is complacent. Historically, selloffs from here tend to be sharper."},
 "vix_calm":{"zh":"VIX 现在 {p:.2f}，属于**平静区间（13–20）**。市场预期未来一个月不会有大波动，风险偏好正常，资金愿意待在股票等风险资产里，这对高估值的AI和IPO标的是有利环境。",
   "en":"VIX is {p:.2f}, in the **calm zone (13–20)**. The market expects no major swings over the next month, risk appetite is normal, and capital is willing to stay in equities — a favourable backdrop for richly valued AI and IPO names."},
 "vix_tense":{"zh":"VIX 现在 {p:.2f}，已进入**紧张区间（20–30）**。投资者正在为下跌买保险，避险需求上升时，最先被卖掉的通常就是没有盈利支撑的高估值成长股。",
   "en":"VIX is {p:.2f}, now in the **tense zone (20–30)**. Investors are buying downside protection, and when hedging demand rises the first thing sold is usually unprofitable, high-multiple growth stock."},
 "vix_panic":{"zh":"VIX 现在 {p:.2f}，处于**恐慌区间（高于30）**。历史上这种水平只在系统性风险事件中出现（如2008、2020年3月），此时泡沫类资产的抛压最集中。",
   "en":"VIX is {p:.2f}, in the **panic zone (above 30)**. Levels like this historically appear only during systemic events (2008, March 2020), when bubble-type assets face the heaviest selling."},
 "vix_mv_down":{"zh":"今日**大幅回落**，说明恐慌情绪在快速消退、风险偏好回升（{chg:+.2f}%）。",
   "en":"It **fell sharply** today, meaning fear is draining fast and risk appetite is returning ({chg:+.2f}%)."},
 "vix_mv_up":{"zh":"今日**明显上升**，说明市场正在加速买入下跌保护、担忧升温（{chg:+.2f}%）。",
   "en":"It **rose notably** today — the market is rushing to buy protection and anxiety is building ({chg:+.2f}%)."},
 "vix_mv_flat":{"zh":"今日变化不大，情绪维持现状（{chg:+.2f}%）。",
   "en":"Little changed today; sentiment is holding steady ({chg:+.2f}%)."},
 # ── 10年期美债 ──
 "tnx_low":{"zh":"10年期美债收益率 {p:.2f}%，处于**低位**。它是全球资产定价的「无风险利率」基准，越低意味着未来现金流折现回来越值钱，对靠远期故事支撑的成长股最有利。今日{chg:+.2f}%。",
   "en":"The 10-year Treasury yield is {p:.2f}%, which is **low**. This is the global \u201crisk-free rate\u201d benchmark: the lower it goes, the more valuable distant future cash flows become — which benefits growth stocks built on long-dated stories. Today: {chg:+.2f}%."},
 "tnx_mid":{"zh":"10年期美债收益率 {p:.2f}%，处于**中性偏紧区间**。股票相对债券的吸引力被削弱，但还不至于压垮估值，市场会更看重公司能不能真正赚钱。今日{chg:+.2f}%。",
   "en":"The 10-year Treasury yield is {p:.2f}%, a **neutral-to-tight** range. Equities look less attractive versus bonds, though not fatally so — the market simply starts caring more about whether companies actually earn money. Today: {chg:+.2f}%."},
 "tnx_high":{"zh":"10年期美债收益率 {p:.2f}%，**偏高**。无风险利率越高，折现率就越高，没有当期盈利、只靠远期增长故事的AI股和新股受到的估值压制最大——这也是泡沫风险模型里利率权重很重的原因。今日{chg:+.2f}%。",
   "en":"The 10-year Treasury yield is {p:.2f}%, which is **elevated**. A higher risk-free rate means a higher discount rate, and the valuation pressure lands hardest on AI names and new listings that have no current earnings — which is exactly why interest rates carry so much weight in the bubble-risk model. Today: {chg:+.2f}%."},
 # ── 指数 ──
 "idx_up_big":{"zh":"{idx}今日上涨 {chg:+.2f}%，属于**明显放量的风险偏好回升**，通常伴随资金从防御性板块流向成长股。",
   "en":"{idx} rose {chg:+.2f}% today — a **clear risk-on move**, usually accompanied by rotation out of defensives and into growth."},
 "idx_up":{"zh":"{idx}今日小幅收涨 {chg:+.2f}%，市场情绪偏稳，没有出现方向性突破。",
   "en":"{idx} closed up {chg:+.2f}% today. Sentiment is steady, with no decisive directional breakout."},
 "idx_dn":{"zh":"{idx}今日小幅回落 {chg:+.2f}%，属于正常波动区间，暂时看不出趋势反转。",
   "en":"{idx} slipped {chg:+.2f}% today — within normal daily noise, no sign of a trend reversal yet."},
 "idx_dn_big":{"zh":"{idx}今日下跌 {chg:+.2f}%，跌幅偏大，需要留意是否有宏观利空（利率、通胀或财报）在发酵。",
   "en":"{idx} fell {chg:+.2f}% today, a sizeable drop — worth checking whether a macro negative (rates, inflation or earnings) is building."},
 "idx_nasdaq":{"zh":"纳斯达克（科技股集中）","en":"the Nasdaq (tech-heavy)"},
 "idx_sp":{"zh":"标普500（宽基大盘）","en":"the S&P 500 (broad market)"},
 # ── SpaceX ──
 "spcx":{"zh":"SpaceX 现价 ${p:.2f}，今日{chg:+.2f}%。作为2026年最大的IPO，它的走势是市场对「高估值、未盈利、故事驱动」这一类资产风险偏好的直接体温计。",
   "en":"SpaceX trades at ${p:.2f}, {chg:+.2f}% today. As the largest IPO of 2026, its price action is a direct thermometer for appetite toward richly valued, unprofitable, narrative-driven assets."},
 # ── 个股 ──
 "stk_up_big":{"zh":"{name}今日大涨 {chg:+.2f}%，明显强于大盘，多半有个股层面的催化（财报、订单或行业消息）在推动。",
   "en":"{name} jumped {chg:+.2f}% today, clearly outpacing the market — usually a sign of a stock-specific catalyst (earnings, orders or sector news)."},
 "stk_up":{"zh":"{name}今日收涨 {chg:+.2f}%，跟随大盘小幅走强，属于常规波动。",
   "en":"{name} closed up {chg:+.2f}%, drifting higher with the market — routine movement."},
 "stk_dn":{"zh":"{name}今日回落 {chg:+.2f}%，幅度不大，更像是随大盘整理而非个股利空。",
   "en":"{name} eased {chg:+.2f}% today. The move is small and looks like market-wide consolidation rather than a company-specific problem."},
 "stk_dn_big":{"zh":"{name}今日下跌 {chg:+.2f}%，跌幅偏大，建议结合「股票分析器」看是技术面破位还是基本面出了问题。",
   "en":"{name} dropped {chg:+.2f}% today — a large decline. Use the Stock Analyzer to check whether this is a technical breakdown or a fundamental issue."},
 # ── 加密货币 ──
 "crypto_up_big":{"zh":"现价 ${p:,.2f}，24小时{chg:+.2f}%，**涨势明显**。{role}。",
   "en":"Trading at ${p:,.2f}, {chg:+.2f}% over 24h — **clearly rallying**. {role}."},
 "crypto_up":{"zh":"现价 ${p:,.2f}，24小时{chg:+.2f}%，小幅走强。{role}。",
   "en":"Trading at ${p:,.2f}, {chg:+.2f}% over 24h, modestly higher. {role}."},
 "crypto_dn":{"zh":"现价 ${p:,.2f}，24小时{chg:+.2f}%，小幅回落，属于加密市场的日常波动。{role}。",
   "en":"Trading at ${p:,.2f}, {chg:+.2f}% over 24h — a mild pullback, normal for crypto. {role}."},
 "crypto_dn_big":{"zh":"现价 ${p:,.2f}，24小时{chg:+.2f}%，**跌幅较大**。{role}。",
   "en":"Trading at ${p:,.2f}, {chg:+.2f}% over 24h — **a sharp decline**. {role}."},
 "role_btc":{"zh":"比特币是整个加密市场的风险偏好温度计，与纳斯达克的相关性近年明显上升，流动性宽松时涨得最凶",
   "en":"Bitcoin is the risk-appetite thermometer for all of crypto; its correlation with the Nasdaq has risen sharply in recent years, and it rallies hardest when liquidity is loose"},
 "role_eth":{"zh":"以太坊的价格绑定链上活跃度（DeFi、Layer2、RWA），比比特币多一层「生态使用率」的基本面",
   "en":"Ethereum's price is tied to on-chain activity (DeFi, Layer 2, RWA), giving it a usage-based fundamental layer that Bitcoin lacks"},
 "role_sol":{"zh":"Solana 属于高贝塔品种，牛市涨幅通常超过主流币，回撤也更深",
   "en":"Solana is a high-beta asset: it typically outruns the majors in bull phases and draws down harder in reverse"},
 "role_bnb":{"zh":"币安币与交易所交易量和销毁机制挂钩，受监管消息影响特别大",
   "en":"BNB is tied to exchange volume and its burn mechanism, which makes it unusually sensitive to regulatory news"},
 "role_xrp":{"zh":"瑞波的价格主要由监管进展和跨境支付采用消息驱动，技术面之外的事件风险高",
   "en":"XRP is driven mainly by regulatory progress and cross-border payment adoption, so event risk outweighs technicals"},
 "role_doge":{"zh":"狗狗币没有现金流和技术护城河，价格几乎完全由社区情绪和名人效应驱动",
   "en":"Dogecoin has no cash flow or technical moat; its price is driven almost entirely by community hype and celebrity attention"},
 "role_generic":{"zh":"该币种价格主要由市场情绪和流动性驱动",
   "en":"This coin's price is driven mainly by sentiment and liquidity"},
 # ── 有色金属 ──
 "metal_up_big":{"zh":"现价 ${p:,.2f}，今日{chg:+.2f}%，**涨幅明显**。{logic}。",
   "en":"At ${p:,.2f}, {chg:+.2f}% today — **a strong gain**. {logic}."},
 "metal_up":{"zh":"现价 ${p:,.2f}，今日{chg:+.2f}%，小幅走强。{logic}。",
   "en":"At ${p:,.2f}, {chg:+.2f}% today, modestly firmer. {logic}."},
 "metal_dn":{"zh":"现价 ${p:,.2f}，今日{chg:+.2f}%，小幅回落。{logic}。",
   "en":"At ${p:,.2f}, {chg:+.2f}% today, slightly lower. {logic}."},
 "metal_dn_big":{"zh":"现价 ${p:,.2f}，今日{chg:+.2f}%，**跌幅较大**。{logic}。",
   "en":"At ${p:,.2f}, {chg:+.2f}% today — **a sharp drop**. {logic}."},
 "logic_gold":{"zh":"黄金涨跌主要看**实际利率和避险需求**：实际利率下行或地缘风险升温时黄金走强",
   "en":"Gold hinges on **real interest rates and safe-haven demand**: it strengthens when real rates fall or geopolitical risk rises"},
 "logic_silver":{"zh":"白银是**贵金属+工业金属**双重属性，除了避险，还受光伏和电子需求影响，弹性比黄金大",
   "en":"Silver is **both a precious and an industrial metal** — beyond safe-haven demand it tracks solar and electronics consumption, making it more volatile than gold"},
 "logic_copper":{"zh":"铜被称为「铜博士」，是**全球经济需求的领先指标**，电动车、电网和数据中心建设是长期需求来源",
   "en":"Copper is nicknamed \u201cDr. Copper\u201d — a **leading indicator of global demand**, with EVs, grid upgrades and data centres as its long-term drivers"},
 "logic_gdx":{"zh":"金矿股相对金价有**杠杆效应**，金价涨1%时矿股往往涨2-3%，但也多了矿山成本和运营风险",
   "en":"Gold miners are **leveraged to bullion**: a 1% move in gold often means 2–3% in the miners, at the cost of added mine-operating risk"},
 "logic_slv":{"zh":"白银ETF跟踪银价，走势同时受避险情绪和工业（光伏）需求影响",
   "en":"This silver ETF tracks spot silver, driven by both safe-haven flows and industrial (solar) demand"},
 "logic_fcx":{"zh":"自由港是全球最大上市铜生产商之一，业绩与铜价高度绑定，可视为**铜价的放大器**",
   "en":"Freeport is one of the largest listed copper producers; its earnings track the copper price closely, making it **an amplifier of copper**"},
 "logic_generic":{"zh":"该品种主要受大宗商品供需和美元汇率影响",
   "en":"This instrument is driven mainly by commodity supply/demand and the US dollar"},
 # ── 市场情绪分 ──
 "sent_text":{"zh":"这个 **{score}/100（{label}）** 不是拍脑袋来的，而是由三个实时数据加权算出来的：{notes}。三者共同决定了当前风险偏好水平，分数越高说明市场越愿意为高估值资产买单。",
   "en":"This **{score}/100 ({label})** is not a guess — it is computed from three live inputs: {notes}. Together they set the current level of risk appetite; the higher the score, the more willing the market is to pay up for expensive assets."},
 "sent_calc":{"zh":"计算过程：","en":"How it is computed: "},
 "sent_base":{"zh":"中性起点 50","en":"neutral base 50"},
 "sent_vix_note":{"zh":"VIX {v:.1f}（{eff}）","en":"VIX {v:.1f} ({eff})"},
 "sent_vix_plus":{"zh":"低波动加分","en":"low volatility, adds points"},
 "sent_vix_minus":{"zh":"波动升高扣分","en":"rising volatility, subtracts points"},
 "sent_ixic_note":{"zh":"纳指今日{c:+.2f}%","en":"Nasdaq {c:+.2f}% today"},
 "sent_nvda_note":{"zh":"英伟达（AI风向标）{c:+.2f}%","en":"NVIDIA (the AI bellwether) {c:+.2f}%"},
 "lbl_panic2":{"zh":"极度恐慌","en":"extreme fear"}, "lbl_panic":{"zh":"恐慌","en":"fear"},
 "lbl_neutral":{"zh":"中性","en":"neutral"}, "lbl_optimistic":{"zh":"乐观","en":"optimistic"},
 "lbl_euphoric":{"zh":"极度狂热","en":"euphoric"},
 # ── 泡沫模拟器 ──
 "sim_pop":{"zh":"首日涨幅是四个输入的加权和：情绪和散户热度推高发行日溢价，利率则是唯一的拖累项。当前**{top}贡献最大（{topv:+.1f}）**，而**{drag}拖累最多（{dragv:+.1f}）**。",
   "en":"The day-one pop is a weighted sum of four inputs: sentiment and retail enthusiasm push the listing premium up, while interest rates are the only drag. Right now **{top} contributes most ({topv:+.1f})**, and **{drag} weighs on it the most ({dragv:+.1f})**."},
 "sim_six":{"zh":"6个月收益衡量的是「上市热度退潮后还剩多少」。它以中性值（情绪50、AI50、散户50、利率4%）为基准，只看偏离量，所以数值通常远小于首日涨幅。利率每高出基准1个百分点就直接扣8个点，是四项里权重最重的。",
   "en":"The six-month return measures what survives once listing euphoria fades. It is benchmarked against neutral settings (sentiment 50, AI 50, retail 50, rate 4%) and counts only the deviation, so it is normally far smaller than the day-one pop. Every percentage point of rates above the 4% baseline subtracts 8 points — the heaviest weight of the four."},
 "sim_burst":{"zh":"泡沫破裂概率从100分往下扣：情绪越乐观、AI落地越快、散户越活跃，破裂概率越低；而利率是唯一的**加分项（权重最高，×6）**，因为历史上刺破泡沫的通常都是利率上行（2000年互联网、2021年SPAC都是如此）。当前利率 {rate}% 贡献了 {contrib:+.1f} 的破裂概率。",
   "en":"Burst probability counts down from 100: the more optimistic sentiment, the faster AI monetisation and the more active retail, the lower it goes. Interest rates are the only factor that **adds** to it — and with the largest weight (\u00d76) — because historically it is rising rates that pop bubbles (dot-com in 2000, SPACs in 2021). At {rate}%, rates currently contribute {contrib:+.1f} to the burst probability."},
 "sim_temp":{"zh":"泡沫温度计是情绪(40%)、AI速度(30%)、散户参与(20%)和低利率红利(10%)的综合打分，越接近100说明市场越亢奋。它和破裂概率是一体两面：温度越高，一旦流动性收紧，回撤空间也越大。",
   "en":"The bubble thermometer blends sentiment (40%), AI monetisation speed (30%), retail participation (20%) and the low-rate bonus (10%). The closer to 100, the more euphoric the market. It is the mirror image of burst probability: the hotter it runs, the further there is to fall once liquidity tightens."},
 "drv_sentiment":{"zh":"市场情绪","en":"market sentiment"},
 "drv_ai":{"zh":"AI商业化速度","en":"AI monetisation speed"},
 "drv_rate":{"zh":"利率环境","en":"the interest-rate backdrop"},
 "drv_retail":{"zh":"散户参与度","en":"retail participation"},
 "term_base":{"zh":"基础","en":"base"}, "term_sent":{"zh":"情绪","en":"sentiment"},
 "term_ai":{"zh":"AI速度","en":"AI speed"}, "term_rate":{"zh":"利率","en":"rate"},
 "term_retail":{"zh":"散户","en":"retail"}, "term_lowrate":{"zh":"低利率红利","en":"low-rate bonus"},
}

def nt(key, **kw):
    """取分析正文：当前语言 → 英文 → 中文"""
    return _render(key, _i18n_entry(key), kw)

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

/* ── 顶部免责声明横幅 ── */
.disclaimer-top {
    display: flex; gap: 12px; align-items: flex-start;
    background: rgba(186,117,23,0.10);
    border: 1px solid rgba(186,117,23,0.35);
    border-left: 4px solid #BA7517;
    border-radius: 12px;
    padding: 12px 16px; margin: 6px 0 16px;
    -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px);
}
.stApp .disclaimer-top, .stApp .disclaimer-top b { color: #6b4a10; }
.disclaimer-top .dt-icon { font-size: 19px; line-height: 1.3; }
.stApp .disclaimer-top .dt-sub { color: #7a5a22; font-size: 12px; line-height: 1.7; }


/* ── 深色系统兜底：即使没有 .streamlit/config.toml 也保持浅色一致 ── */
[data-testid="stSidebar"] {
  background: #FFFFFFEE !important;
  border-right: 1px solid rgba(15,23,42,.08);
}
[data-testid="stSidebar"] *:not(svg):not(path) { color: #0F172A !important; }
[data-testid="stSidebar"] small { color: #5B6678 !important; }

/* 下拉菜单 / 提示气泡渲染在 body 的 portal 层，不受主容器 CSS 管辖 */
[data-baseweb="popover"], [data-baseweb="menu"], [data-baseweb="layer"] [role="listbox"] {
  background: #FFFFFF !important;
  color: #0F172A !important;
}
[data-baseweb="popover"] li, [data-baseweb="menu"] li, [role="option"] {
  background: #FFFFFF !important; color: #0F172A !important;
}
[role="option"]:hover, [aria-selected="true"] { background: #EEF0FA !important; }

body { background: #F7F8FC; }

/* ── 折叠式免责声明 ── */
.disc-slim {
  display:flex; gap:10px; align-items:flex-start;
  background: linear-gradient(135deg, rgba(255,246,224,.92), rgba(253,240,210,.86));
  border: 1px solid rgba(186,117,23,.28);
  border-left: 4px solid #BA7517;
  border-radius: 10px; padding: 10px 14px; margin: 6px 0 2px;
  backdrop-filter: blur(8px) saturate(140%);
}
.stApp .disc-slim, .stApp .disc-slim b { color:#6b4a10; font-size:13.5px; line-height:1.55; }
.disc-slim .ds-icon { font-size:16px; line-height:1.4; }

/* ── 页脚免责声明 ── */
.disclaimer-foot {
    margin-top: 26px; padding: 16px 20px; border-radius: 14px;
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(255,255,255,0.75);
    -webkit-backdrop-filter: blur(18px); backdrop-filter: blur(18px);
    box-shadow: 0 4px 18px rgba(15,23,42,0.06);
    font-size: 12px; line-height: 1.85;
}
.stApp .disclaimer-foot, .stApp .disclaimer-foot li { color: #5b6678; }
.stApp .disclaimer-foot b { color: #0f172a; }
.disclaimer-foot ul { margin: 6px 0 0; padding-left: 20px; }

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
        _lang_codes = list(LANGUAGES.keys())
        st.selectbox(tr("lang_label"), _lang_codes,
                     index=_lang_codes.index(ss.get("lang", "zh")),
                     format_func=lambda c: LANGUAGES[c], key="lang")
        if ss.get("lang", "zh") in ("es", "fr", "de", "ja", "ko"):
            st.caption(tr("i18n_note"))
        st.divider()
        st.markdown(tr("watch_title"))
        st.caption(tr("watch_updated", ts=_dtn.now().strftime('%H:%M:%S')))
        if active:
            st.success(tr("watch_active", iv=iv) + "\n\n" +
                       tr("watch_left", mm=f"{left//60:02d}", ss=f"{left%60:02d}",
                         n=ss.get("watch_count", 0)))
            b1, b2 = st.columns(2)
            if b1.button(tr("watch_stop"), use_container_width=True, key="watch_stop"):
                stop_watch(); st.rerun()
            if b2.button(tr("watch_extend"), use_container_width=True, key="watch_extend",
                         help=f"再延长 {ss.get('watch_min', 15)} 分钟"):
                start_watch(); st.rerun()
        else:
            if ss.pop("watch_expired", False):
                st.info(tr("watch_expired"))
            c1, c2 = st.columns(2)
            # key 里带上语言：切换语言时强制重建控件，否则选项文案不会跟着刷新
            _lg = ss.get("lang", "zh")
            _iv = c1.selectbox(tr("watch_interval"), [30, 60, 120, 300],
                               index=[30, 60, 120, 300].index(ss.get("watch_iv", 60)),
                               key=f"watch_iv_sel_{_lg}",
                               format_func=lambda s: tr("unit_sec", n=s) if s < 60 else tr("unit_min", n=s // 60))
            _mn = c2.selectbox(tr("watch_duration"), [5, 15, 30, 60],
                               index=[5, 15, 30, 60].index(ss.get("watch_min", 15)),
                               key=f"watch_min_sel_{_lg}",
                               format_func=lambda m: tr("unit_min", n=m))
            if st.button(tr("watch_start"), use_container_width=True, type="primary", key="watch_start"):
                start_watch(minutes=_mn, interval=_iv); st.rerun()
            st.caption(tr("watch_manual"))
        st.caption(tr("watch_src"))
        if st.button(tr("force_refresh"), use_container_width=True, key="force_refresh_all"):
            st.cache_data.clear()
            st.rerun()
        st.divider()
        st.caption(tr("disc_side"))
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

def _md_bold(text):
    """把 **粗体** 转成 <b>粗体</b>。

    凡是用 unsafe_allow_html=True 塞进 HTML 块的文本，Streamlit 都不会再走
    Markdown 解析，写 **x** 会原样显示成星号。所有进 HTML 的文案都要过这里。
    """
    import re as _re_b
    return _re_b.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", str(text))


def why_html(text, tone="neutral", calc=None, title=None):
    import re
    if title is None:
        title = tr("why_default")
    c, bg = _WHY_C.get(tone, "#475569"), _WHY_BG.get(tone, "rgba(100,116,139,.09)")
    text = _md_bold(text)   # HTML 块内不会解析 markdown 粗体
    calc_html = f'<span class="calc">{calc}</span>' if calc else ""
    return (f'<div class="whybox" style="border-left:3px solid {c};background:{bg}">'
            f'<span class="wt" style="color:{c}">{title}：</span>{text}{calc_html}</div>')

def why(text, tone="neutral", calc=None, title=None, target=None):
    """在指标下方渲染一条解读"""
    (target or st).markdown(why_html(text, tone, calc, title), unsafe_allow_html=True)

def interpret_market(ticker, info):
    """解读市场概览里的每个标的：(解读文字, 语气)"""
    p, chg = info["price"], info["change_pct"]
    name = asset_name(ticker, info["name"])   # 句子里的标的名也跟随语言

    if ticker == "^VIX":
        if p < 13:
            base, tone = nt("vix_low", p=p), "warn"
        elif p < 20:
            base, tone = nt("vix_calm", p=p), "good"
        elif p < 30:
            base, tone = nt("vix_tense", p=p), "warn"
        else:
            base, tone = nt("vix_panic", p=p), "bad"
        move = (nt("vix_mv_down", chg=chg) if chg < -5 else
                nt("vix_mv_up", chg=chg) if chg > 5 else nt("vix_mv_flat", chg=chg))
        return base + " " + move, tone

    if ticker == "^TNX":
        if p < 3:
            return nt("tnx_low", p=p, chg=chg), "good"
        if p < 4.5:
            return nt("tnx_mid", p=p, chg=chg), "warn"
        return nt("tnx_high", p=p, chg=chg), "bad"

    if ticker in ("^IXIC", "^GSPC"):
        idx = nt("idx_nasdaq") if ticker == "^IXIC" else nt("idx_sp")
        if chg > 1.5:
            return nt("idx_up_big", idx=idx, chg=chg), "good"
        if chg > 0:
            return nt("idx_up", idx=idx, chg=chg), "good"
        if chg > -1.5:
            return nt("idx_dn", idx=idx, chg=chg), "neutral"
        return nt("idx_dn_big", idx=idx, chg=chg), "bad"

    if ticker == "SPCX":
        return nt("spcx", p=p, chg=chg), ("good" if chg >= 0 else "bad")

    # 个股
    if chg > 3:
        return nt("stk_up_big", name=name, chg=chg), "good"
    if chg > 0:
        return nt("stk_up", name=name, chg=chg), "good"
    if chg > -3:
        return nt("stk_dn", name=name, chg=chg), "neutral"
    return nt("stk_dn_big", name=name, chg=chg), "bad"

def interpret_crypto(ticker, info):
    chg, p = info["change_pct"], info["price"]
    role = nt({"BTC-USD": "role_btc", "ETH-USD": "role_eth", "SOL-USD": "role_sol",
               "BNB-USD": "role_bnb", "XRP-USD": "role_xrp", "DOGE-USD": "role_doge",
               }.get(ticker, "role_generic"))
    if chg > 3:
        return nt("crypto_up_big", p=p, chg=chg, role=role), "good"
    if chg > 0:
        return nt("crypto_up", p=p, chg=chg, role=role), "good"
    if chg > -3:
        return nt("crypto_dn", p=p, chg=chg, role=role), "neutral"
    return nt("crypto_dn_big", p=p, chg=chg, role=role), "bad"

def interpret_metal(ticker, info):
    chg, p = info["change_pct"], info["price"]
    logic = nt({"GC=F": "logic_gold", "SI=F": "logic_silver", "HG=F": "logic_copper",
                "GDX": "logic_gdx", "SLV": "logic_slv", "FCX": "logic_fcx",
                }.get(ticker, "logic_generic"))
    if chg > 2:
        return nt("metal_up_big", p=p, chg=chg, logic=logic), "good"
    if chg > 0:
        return nt("metal_up", p=p, chg=chg, logic=logic), "good"
    if chg > -2:
        return nt("metal_dn", p=p, chg=chg, logic=logic), "neutral"
    return nt("metal_dn_big", p=p, chg=chg, logic=logic), "bad"

def explain_sentiment(data, score):
    """拆解市场情绪分是怎么算出来的"""
    terms, notes = [nt("sent_base")], []
    if "^VIX" in data:
        v = data["^VIX"]["price"]
        pts = 20 if v < 15 else 10 if v < 20 else -10 if v < 30 else -25
        terms.append(f"VIX {v:.1f} → {pts:+d}")
        notes.append(nt("sent_vix_note", v=v,
                        eff=nt("sent_vix_plus") if pts > 0 else nt("sent_vix_minus")))
    if "^IXIC" in data:
        c = data["^IXIC"]["change_pct"]
        terms.append(f"Nasdaq {c:+.2f}% × 3 → {c*3:+.1f}")
        notes.append(nt("sent_ixic_note", c=c))
    if "NVDA" in data:
        c = data["NVDA"]["change_pct"]
        terms.append(f"NVDA {c:+.2f}% × 2 → {c*2:+.1f}")
        notes.append(nt("sent_nvda_note", c=c))
    label = (nt("lbl_panic2") if score < 20 else nt("lbl_panic") if score < 40 else
             nt("lbl_neutral") if score < 60 else nt("lbl_optimistic") if score < 80
             else nt("lbl_euphoric"))
    tone = "bad" if score < 40 else "neutral" if score < 60 else "good" if score < 80 else "warn"
    sep = "、" if st.session_state.get("lang", "zh") == "zh" else ", "
    text = nt("sent_text", score=score, label=label, notes=sep.join(notes))
    return text, tone, nt("sent_calc") + "　".join(terms) + f"　=　{score}"

def explain_simulate(sentiment, rate, ai_speed, retail, sim):
    """拆解泡沫模拟器的四个输出分别是怎么算出来的"""
    def fmt(terms, total, unit="%"):
        return "　".join(terms) + f"　=　{total}{unit}"

    _b, _s, _a, _r, _re = (nt("term_base"), nt("term_sent"), nt("term_ai"),
                           nt("term_rate"), nt("term_retail"))
    pop_terms = [f"{_b} 5", f"{_s} {sentiment}×0.4={sentiment*0.4:+.1f}",
                 f"{_a} {ai_speed}×0.2={ai_speed*0.2:+.1f}",
                 f"{_r} {rate}%×2={-rate*2:+.1f}", f"{_re} {retail}×0.15={retail*0.15:+.1f}"]
    six_terms = [f"({_s}{sentiment}-50)×0.3={(sentiment-50)*0.3:+.1f}",
                 f"({_a}{ai_speed}-50)×0.2={(ai_speed-50)*0.2:+.1f}",
                 f"({_r}{rate}-4)×8={-(rate-4)*8:+.1f}",
                 f"({_re}{retail}-50)×0.1={(retail-50)*0.1:+.1f}"]
    burst_terms = [f"{_b} 100", f"{_s} {sentiment}×0.4={-sentiment*0.4:+.1f}",
                   f"{_a} {ai_speed}×0.2={-ai_speed*0.2:+.1f}",
                   f"{_r} {rate}%×6={rate*6:+.1f}", f"{_re} {retail}×0.05={-retail*0.05:+.1f}"]

    # 找出影响最大的驱动因素
    drivers = {nt("drv_sentiment"): sentiment*0.4, nt("drv_ai"): ai_speed*0.2,
               nt("drv_rate"): -rate*2, nt("drv_retail"): retail*0.15}
    top = max(drivers.items(), key=lambda kv: abs(kv[1]))
    drag = min(drivers.items(), key=lambda kv: kv[1])

    return {
        "pop": (nt("sim_pop", top=top[0], topv=top[1], drag=drag[0], dragv=drag[1]),
                "good" if sim["pop"] > 20 else "neutral",
                fmt(pop_terms, sim["pop"])),
        "six_m": (nt("sim_six"),
                  "good" if sim["six_m"] > 0 else "bad",
                  fmt(six_terms, sim["six_m"])),
        "burst": (nt("sim_burst", rate=rate, contrib=rate*6),
                  "bad" if sim["burst"] > 65 else "warn" if sim["burst"] > 40 else "good",
                  fmt(burst_terms, sim["burst"])),
        "temp": (nt("sim_temp"),
                 "warn" if sim["temp"] > 60 else "neutral",
                 f"{_s} {sentiment}×0.4　{_a} {ai_speed}×0.3　{_re} {retail}×0.2　"
                 f"{nt('term_lowrate')} (100-{rate}×8)×0.1　=　{sim['temp']}/100"),
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
    "ICE":"洲际交易所 ICE", "CME":"芝商所 CME", "NDAQ":"纳斯达克交易所",
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

# 常见写错的代码 → 正确代码（公司名、简称、现货代号等）
TICKER_ALIASES = {
    "TESLA": "TSLA", "特斯拉": "TSLA", "SPACEX": "SPCX", "太空探索": "SPCX",
    "APPLE": "AAPL", "苹果": "AAPL", "GOOGLE": "GOOGL", "谷歌": "GOOGL",
    "AMAZON": "AMZN", "亚马逊": "AMZN", "NVIDIA": "NVDA", "英伟达": "NVDA",
    "MICROSOFT": "MSFT", "微软": "MSFT", "FACEBOOK": "META", "NETFLIX": "NFLX",
    "ALIBABA": "BABA", "阿里巴巴": "BABA", "BLOCK": "XYZ", "SQ": "XYZ",
    "BTC": "BTC-USD", "BITCOIN": "BTC-USD", "比特币": "BTC-USD",
    "ETH": "ETH-USD", "ETHEREUM": "ETH-USD", "以太坊": "ETH-USD",
    "SOL": "SOL-USD", "SOLANA": "SOL-USD", "XRP": "XRP-USD", "RIPPLE": "XRP-USD",
    "DOGE": "DOGE-USD", "BNB": "BNB-USD", "ADA": "ADA-USD", "LTC": "LTC-USD",
    "XAU": "GLD", "XAUUSD": "GLD", "GOLD": "GLD", "黄金": "GLD",
    "XAG": "SLV", "SILVER": "SLV", "白银": "SLV",
    "COPPER": "HG=F", "铜": "HG=F", "OIL": "USO", "原油": "USO", "WTI": "USO",
    "SP500": "SPY", "S&P500": "SPY", "标普500": "SPY",
    "NASDAQ": "QQQ", "纳斯达克": "QQQ", "纳指": "QQQ",
    "TENCENT": "0700.HK", "腾讯": "0700.HK", "US STEEL": "XME", "USSTEEL": "XME",
}

def suggest_ticker(tk):
    """把写错的代码猜成正确代码；猜不出就返回 None（宁可不猜，也不瞎猜）"""
    import re as _re
    t = (tk or "").strip().upper()
    if not t or t in TICKER_UNIVERSE:
        return None
    if t in TICKER_ALIASES:                       # 1. 已知别名，最可靠
        return TICKER_ALIASES[t]
    if f"{t}-USD" in TICKER_UNIVERSE:             # 2. 加密货币漏写后缀
        return f"{t}-USD"
    if len(t) < 3:                                # 3. 太短无从判断，交给下拉框去选
        return None
    for cand, nm in TICKER_UNIVERSE.items():      # 4. 按公司名匹配：须是完整单词或名称开头
        words = [w for w in _re.split(r"[\s（）()/·—-]+", nm.upper()) if w]
        if t in words or nm.upper().startswith(t):
            return cand
    for cand in TICKER_UNIVERSE:                  # 5. 代码前缀（输入够长时才用）
        if cand.startswith(t):
            return cand
    return None

def report_invalid_tickers(requested, valid, where="分析"):
    """把被丢掉的代码明确告诉用户，并给出「你是不是想输入…」建议"""
    missing = [t for t in requested if t and t not in valid]
    if not missing:
        return
    lines = []
    for t in missing:
        s = suggest_ticker(t)
        lines.append(f"**{t}** → 建议改成 **{s}**（{TICKER_UNIVERSE.get(s, '')}）" if s
                     else f"**{t}** → 雅虎财经查不到这个代码")
    st.warning(f"⚠️ 有 {len(missing)} 个代码取不到行情，已不计入{where}：\n\n" + "\n\n".join(f"· {l}" for l in lines))

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

def render_asset_grid_clickable(items, key_prefix, cols=4, btn_label=None):
    """items: [(ticker, card_html)]；每张卡下方带一个跳转按钮"""
    for start in range(0, len(items), cols):
        chunk = items[start:start + cols]
        cc = st.columns(cols)
        for i, (tk, html) in enumerate(chunk):
            with cc[i]:
                st.markdown(f'<div class="ac-grid" style="--acmin:100%;margin-bottom:6px">{html}</div>',
                            unsafe_allow_html=True)
                if st.button(btn_label or tr("view_analysis"),
                             key=f"{key_prefix}_{tk}", use_container_width=True):
                    st.session_state["quick_view_ticker"] = tk
                    st.session_state["quick_view_src"] = key_prefix   # 记住是哪一组点的
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
        f'<div style="font-size:12.5px;opacity:.92">趋势 {r.get("trend_score", r.get("score", 50))}/100　·　'
        f'位置 {r.get("stretch_score", 50)}/100</div>'
        f'</div></div></div>', unsafe_allow_html=True)

    q1, q2, q3, q4, q5 = st.columns(5)
    q1.metric("现价", f"${r['price_now']:.2f}")
    q2.metric("1个月动量", f"{r['mom_1m']:+.1f}%", delta_color="normal" if r['mom_1m'] >= 0 else "inverse")
    q3.metric("RSI(14)", f"{r['rsi']:.1f}",
              "超卖" if r['rsi'] < 30 else "超买" if r['rsi'] > 70 else "正常")
    q4.metric("52周区间", f"${r['price_52w_low']:.0f} – {r['price_52w_high']:.0f}",
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
        (sc1 if i % 2 == 0 else sc2).markdown(_nolatex(f"**{icon} {title}** — {desc}"))
    st.caption("想看完整分析（财报、斐波那契、量化面板、宏观联动）请前往「🔬 股票分析器」，代码已自动填好。")


def render_quick_view(src):
    """在触发它的那一组卡片正下方展开走势与分析。

    以前不管点哪一组，都固定画在页面顶部的主网格下面 —— 加密货币和
    贵金属的卡片在页面更下方，点完图跑到上面去了，用户得往回滚才看得见。
    现在按 quick_view_src 匹配，谁触发就画在谁下面。
    """
    if st.session_state.get("quick_view_src") != src:
        return
    _qv = st.session_state.get("quick_view_ticker")
    if not _qv:
        return
    st.divider()
    _qc1, _qc2 = st.columns([5, 1])
    _qc1.markdown(tr("quick_analysis", tk=_qv))
    if _qc2.button(tr("btn_close"), key=f"qv_close_{src}", use_container_width=True):
        st.session_state["quick_view_ticker"] = None
        st.session_state["quick_view_src"] = None
        st.rerun()
    with st.spinner(tr("analyzing", tk=_qv)):
        render_quick_analysis(_qv)
    st.divider()


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
# IPO 名单里的估值、收入、递交状态都是手工维护的静态数据 —— 不是实时行情。
# 之前 SPCX 的价格写死了三个多月没人发现，就是因为没有任何"数据何时采集"的标记。
# 改这个列表时，把下面这个日期一并改掉；页面会在超过 90 天后自动提示该核对了。
IPO_DATA_ASOF = "2026-09-18"

IPOS = [
    {"name": "SpaceX",       "sector": "太空科技", "val_b": 1770, "rev_b": 18.7,
     "profitable": False, "float_pct": 4,  "exp_pop": 19, "bubble_risk": 45,
     "date": "2026年6月12日 ✅已上市", "ticker": "SPCX",
     "ipo_price": 135.0,
     "desc": "2026年6月12日纳斯达克上市，发行价$135，首日收盘$161（+19%），史上最大IPO。2025年全年营收$187亿（同比+33%），EBITDA $66亿，但GAAP净亏损$49亿。已收购xAI，整合Grok AI和X（Twitter）。累计亏损$413亿。上市后股价见过$211、也回落到过$108，现价请看上方实时行情。"},
    {"name": "OpenAI",       "sector": "人工智能", "val_b": 852, "rev_b": 20.0,
     "rev_basis": "runrate",
     "profitable": False, "float_pct": 5,  "exp_pop": 30, "bubble_risk": 72,
     "date": "已保密递交 · 时间待定",
     "desc": "ChatGPT母公司。2026年5月22日向SEC保密递交S-1，但规模、条款、时间与交易所均未披露。"
             "最近一次定价为2026年3月31日完成的$1220亿融资，对应估值$8520亿；有分析师预计挂牌时估值可能超过$1万亿。"
             "2025年底收入已超过$200亿，但仍大幅亏损。原计划最早2026年9月上市，路透社6月末报道称可能推迟到2027年。"},
    {"name": "Anthropic",    "sector": "人工智能", "val_b": 965,  "rev_b": 65.0,
     "rev_basis": "runrate",
     "profitable": False, "float_pct": 5,  "exp_pop": 32, "bubble_risk": 70,
     "date": "已保密递交 · 最早2026年秋",
     "desc": "Claude系列模型公司。2026年6月1日向SEC保密递交S-1（保密件，EDGAR上尚不可查）。"
             "2026年5月完成$650亿融资的Series H-1对应估值$9650亿；投行与投资人讨论过的挂牌估值上限约$2万亿。"
             "年化收入跑步增长：2025年底约$90亿 → 2026年3月$190亿 → 5月约$470亿 → 7月底已超过$650亿，但尚未盈利。"
             "亚马逊和谷歌为主要战略投资方。开始交易的时间取决于SEC审核与市场状况，尚无确定日期。"},
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

# 赛道名称的英文对照（正文说明仍在后续批次翻译）
TRACK_NAME_EN = {
    "数字黄金 / 价值存储": "Digital gold / store of value",
    "智能合约平台 / Layer2 + DeFi生态": "Smart-contract platform / L2 + DeFi",
    "高性能公链": "High-throughput L1",
    "交易所生态币": "Exchange ecosystem token",
    "跨境支付": "Cross-border payments",
    "Meme币 / 社区驱动": "Meme coin / community-driven",
    "避险资产 / 抗通胀": "Safe haven / inflation hedge",
    "工业+贵金属双属性": "Industrial + precious metal",
    "电气化 / 新能源基建金属": "Electrification / clean-energy metal",
    "黄金矿业股（金价的杠杆敞口）": "Gold miners (leveraged gold exposure)",
    "铜矿开采（新能源金属敞口）": "Copper mining (clean-energy metals)",
    "黄金开采": "Gold mining",
    "科技 / AI基础设施": "Technology / AI infrastructure",
    "金融服务": "Financial services",
    "可选消费": "Consumer discretionary",
    "医疗健康": "Healthcare",
    "能源": "Energy",
    "房地产 / REITs": "Real estate / REITs",
    "传媒 / 互联网": "Media / internet",
    "工业 / 制造": "Industrials / manufacturing",
    "必需消费": "Consumer staples",
    "公用事业": "Utilities",
    "原材料 / 大宗商品": "Materials / commodities",
    "综合板块": "General sector",
}

def _track_name(zh_name):
    if st.session_state.get("lang", "zh") == "zh":
        return zh_name
    return TRACK_NAME_EN.get(zh_name, zh_name)

def get_track_info(ticker, sector=None):
    """返回 (赛道名称, 主题色, 潜力叙述)，优先按代码匹配，其次按行业匹配"""
    if ticker in TRACK_POTENTIAL:
        nm, color, desc = TRACK_POTENTIAL[ticker]
        return (_track_name(nm), color, desc)
    if sector in SECTOR_TRACK_MAP:
        name, desc = SECTOR_TRACK_MAP[sector]
        return (_track_name(name), "#534AB7", desc)
    return (_track_name("综合板块"), "#666666",
            "暂无该行业的专项赛道分析，建议结合公司基本面和所处行业竞争格局自行评估长期成长空间。")

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

@st.cache_data(ttl=3600, show_spinner=False)
def get_risk_free_rate() -> float:
    """年化无风险利率（小数形式，例如 0.0494 表示 4.94%）。

    取 10 年期美债收益率 ^TNX —— 注意它本身已经是百分数形式
    （返回 4.94 表示 4.94%），所以要除以 100。

    夏普比率和 Jensen's Alpha 都必须扣掉这一项：
    rf 越高、资产波动越低，不扣的偏差就越大（偏差 = rf/σ）。
    """
    try:
        import yfinance as yf
        h = yf.Ticker("^TNX").history(period="5d")["Close"].dropna()
        if len(h):
            r = float(h.iloc[-1]) / 100.0
            if 0.0 <= r <= 0.25:          # 合理区间，挡掉脏数据
                return r
    except Exception:
        pass
    return 0.04                            # 取不到时的保守默认值


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

@st.cache_data(ttl=900, show_spinner=False)
def compute_ai_speed():
    """把「AI 商业化速度」量化成 0-100，不再写死一个 60。

    代理指标：AI 权重股组合相对标普 500 的 3 个月超额收益。
    逻辑是——市场当前愿意为 AI 叙事付多少溢价，就反映了它对
    AI 商业化兑现速度的集体预期。跑赢大盘越多，说明预期越乐观。

    映射：相对大盘 −20% → 20 分；持平 → 50 分；+20% → 80 分。
    返回 (分数, 超额收益%, 是否取到真实数据)
    """
    try:
        import yfinance as yf
        basket = ["NVDA", "MSFT", "GOOGL", "META", "AMD", "AVGO"]
        rets = []
        for tk in basket:
            try:
                h = yf.Ticker(tk).history(period="3mo")["Close"].dropna()
                if len(h) > 20:
                    rets.append(float(h.iloc[-1] / h.iloc[0] - 1))
            except Exception:
                continue
        b = yf.Ticker("^GSPC").history(period="3mo")["Close"].dropna()
        if not rets or len(b) < 20:
            return 60, 0.0, False
        ai_ret = sum(rets) / len(rets)
        sp_ret = float(b.iloc[-1] / b.iloc[0] - 1)
        excess = (ai_ret - sp_ret) * 100
        return int(max(0, min(100, round(50 + excess * 1.5)))), round(excess, 1), True
    except Exception:
        return 60, 0.0, False


def bubble_now(live):
    """把实时行情换算成泡沫模型的四个输入，并逐项拆出它们的贡献。

    返回的 breakdown 里每一项都带着：实时值、换算过程、对温度/破裂概率的
    具体贡献 —— 这样页面上说的"为什么"是算出来的，不是编的。
    """
    def _v(tk, field="price", default=None):
        """取实时字段并强制转成 float。

        行情接口偶尔会回 "N/A" 之类的字符串，而这块现在是页面头条，
        一个脏字段不该让整页崩掉 —— 转不了就退回 default。
        """
        try:
            import math as _m_bn
            x = float(live[tk][field])
            return default if (_m_bn.isnan(x) or _m_bn.isinf(x)) else x
        except Exception:
            return default

    vix = _v("^VIX")
    ixic_chg = _v("^IXIC", "change_pct", 0.0) or 0.0
    nvda_chg = _v("NVDA", "change_pct", 0.0) or 0.0
    tnx = _v("^TNX")

    # ── 情绪分（复刻 market_to_sentiment 的算法，同时留下每一项的贡献）──
    sent_parts = []
    sent = 50.0
    if vix is not None:
        c = 20 if vix < 15 else 10 if vix < 20 else -10 if vix < 30 else -25
        sent += c
        sent_parts.append(("VIX", f"{vix:.1f}", c,
                           "vix_lo" if vix < 20 else "vix_hi"))
    if ixic_chg:
        c = ixic_chg * 3
        sent += c
        sent_parts.append(("NASDAQ", f"{ixic_chg:+.2f}%", c, "idx"))
    if nvda_chg:
        c = nvda_chg * 2
        sent += c
        sent_parts.append(("NVDA", f"{nvda_chg:+.2f}%", c, "nvda"))
    sentiment = int(max(0, min(100, sent)))

    rate = round(tnx, 2) if tnx is not None else 4.5
    ai_speed, ai_excess, ai_live = compute_ai_speed()
    # 散户热度用 VIX 反推：市场越平静，散户越敢追高。这是代理指标，不是真实持仓数据。
    retail = max(20, min(90, int(100 - vix * 2))) if vix is not None else 70

    sim = simulate(sentiment, rate, ai_speed, retail)

    # ── 四个输入对「泡沫温度」和「破裂概率」各自的贡献 ──
    # temp  = 情绪×0.4 + AI×0.3 + 散户×0.2 + (100−利率×8)×0.1
    # burst = 100 − 情绪×0.4 − AI×0.2 + 利率×6 − 散户×0.05
    breakdown = [
        {"key": "sentiment", "value": sentiment, "raw": f"{sentiment}/100",
         "temp": sentiment * 0.4, "burst": -sentiment * 0.4, "parts": sent_parts},
        {"key": "ai", "value": ai_speed, "raw": f"{ai_speed}/100",
         "temp": ai_speed * 0.3, "burst": -ai_speed * 0.2,
         "excess": ai_excess, "live": ai_live},
        {"key": "retail", "value": retail, "raw": f"{retail}/100",
         "temp": retail * 0.2, "burst": -retail * 0.05},
        {"key": "rate", "value": rate, "raw": f"{rate:.2f}%",
         "temp": (100 - rate * 8) * 0.1, "burst": rate * 6},
    ]
    # simulate() 把破裂概率截断在 5–95。极端行情下逐项加总会超出这个范围，
    # 界面上就会出现"分项加起来 119%、头条却写 95%"的矛盾，所以把原始值也带出去。
    raw_burst = 100 + sum(f["burst"] for f in breakdown)
    raw_temp = sum(f["temp"] for f in breakdown)

    return {"sentiment": sentiment, "rate": rate, "ai_speed": ai_speed,
            "retail": retail, "sim": sim, "breakdown": breakdown,
            "vix": vix, "ai_excess": ai_excess, "ai_live": ai_live,
            "raw_burst": raw_burst, "raw_temp": raw_temp,
            "burst_clamped": abs(raw_burst - sim["burst"]) > 1.5,
            "temp_clamped": abs(raw_temp - sim["temp"]) > 1.5,
            "has_data": bool(live)}


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
# 分析结果的结构版本。session_state 会跨代码更新保留，所以必须能认出旧结构：
# 改动 fetch_stock_analysis 返回的字段时，把这个数字 +1，旧结果会被自动丢弃重算。
ANALYSIS_SCHEMA = 2


@st.cache_data(ttl=120)
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
        # RSI (14) —— Wilder 平滑
        # 用 rolling(14).mean() 算出来的是 Cutler's RSI，只看最近 14 天，
        # 大涨大跌后会明显偏离 TradingView / 雪球 / 券商软件显示的数值
        # （实测分歧可达 20 点，足以把"超卖"读成"中性"）。
        # Wilder 原始定义是 α=1/14 的指数平滑，这里对齐它。
        delta  = close.diff()
        gain   = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
        loss   = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
        rs     = gain / loss.replace(0, 1e-9)
        rsi    = safe_float((100 - 100 / (1 + rs)).iloc[-1], 50.0)

        # MACD —— 标准 MACD 用递归 EMA，pandas 默认的 adjust=True 是加权展开式，
        # 两者在样本前段差别明显，这里对齐图表平台的算法
        ema12  = close.ewm(span=12, adjust=False).mean()
        ema26  = close.ewm(span=26, adjust=False).mean()
        macd   = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
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

        # 夏普比率（年化，已扣除无风险利率）
        # 原来直接用 mean/std，等于假设 rf=0。当 10 年期美债在 4~5% 时，
        # 这会把夏普整体抬高 rf/σ —— 低波动资产（债券、黄金）被抬得最多，
        # 而夏普又是 lt_score 里权重最大的单项（±15 分）。
        daily_returns = close.pct_change().dropna()
        rf_annual = get_risk_free_rate()
        if len(daily_returns) > 5 and float(daily_returns.std()) > 0:
            _rf_d  = rf_annual / 252
            sharpe = float(((daily_returns.mean() - _rf_d) / daily_returns.std()) * (252 ** 0.5))
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

        # ══ 评分系统：拆成两个正交的分数 ══════════════════════════════
        # 以前所有信号加进同一个 score，但它们回答的是两个不同的问题：
        #   · 动量/均线/MACD/斜率/OBV/成交量 → "往哪个方向走"（顺势）
        #   · RSI/布林/斐波那契             → "现在贵不贵"（反向）
        # 混在一起会互相抵消：强势上涨股 动量+10、RSI-5 = +5；
        # 暴跌股 动量-10、RSI+15 = +5 —— 两者得分几乎一样，方向信息全丢了。
        # 拆开后才能区分"趋势强但偏贵（等回调）"和"跌不动了但趋势没转（别接）"。
        trend_score   = 50      # 0-100，越高趋势越强
        stretch_score = 50      # 0-100，越高越超买（越贵）
        signals = []

        # ── 位置类信号：越高越超买 ─────────────────────────────────
        if rsi < 30:
            stretch_score -= 25
            signals.append(("✅", "RSI超卖", f"RSI={rsi:.1f}，技术面严重超卖，短线反弹概率高"))
        elif rsi < 45:
            stretch_score -= 12
            signals.append(("✅", "RSI偏低", f"RSI={rsi:.1f}，位置不算贵，进场性价比相对有利"))
        elif rsi > 75:
            stretch_score += 25
            signals.append(("🔴", "RSI超买", f"RSI={rsi:.1f}，短期获利回吐压力大"))
        elif rsi > 60:
            stretch_score += 12
            signals.append(("🟡", "RSI偏高", f"RSI={rsi:.1f}，位置偏高，追高性价比下降"))
        else:
            signals.append(("⚪", "RSI中性", f"RSI={rsi:.1f}，无明显超买超卖信号"))

        if price_now < bb_low:
            stretch_score -= 15
            signals.append(("✅", "触及布林下轨", f"价格${price_now:.2f}低于下轨${bb_low:.2f}，超卖区间"))
        elif price_now > bb_up:
            stretch_score += 15
            signals.append(("🔴", "突破布林上轨", f"价格${price_now:.2f}高于上轨${bb_up:.2f}，超买区间"))

        if abs(price_now - nearest_support) / price_now < 0.02:
            stretch_score -= 10
            signals.append(("✅", "斐波那契支撑", f"价格${price_now:.2f}接近支撑位${nearest_support:.2f}（Fib回撤）"))
        elif abs(price_now - nearest_resistance) / price_now < 0.02:
            stretch_score += 10
            signals.append(("🔴", "斐波那契阻力", f"价格${price_now:.2f}接近阻力位${nearest_resistance:.2f}（Fib回撤）"))
        else:
            signals.append(("⚪", "斐波那契中性", f"支撑${nearest_support:.2f} → 当前${price_now:.2f} → 阻力${nearest_resistance:.2f}"))

        # 距52周高点也是"位置"的一部分
        if price_from_high > -3:
            stretch_score += 8
            signals.append(("🟡", "逼近52周高点", f"距高点仅 {abs(price_from_high):.1f}%，上方没有套牢盘参照"))
        elif price_from_high < -35:
            stretch_score -= 8
            signals.append(("🟡", "深度回撤", f"距52周高点 {price_from_high:.1f}%，位置低但需确认趋势是否企稳"))

        stretch_score = max(0, min(100, stretch_score))

        # ── 趋势类信号：越高方向越向上 ─────────────────────────────
        if macd_hist > 0:
            trend_score += 12
            signals.append(("✅", "MACD金叉", f"MACD柱={macd_hist:.3f}，多头动能占优"))
        elif macd_hist < 0:
            trend_score -= 12
            signals.append(("🔴", "MACD死叉", f"MACD柱={macd_hist:.3f}，空头动能占优"))
        else:
            signals.append(("🟡", "MACD待确认", "MACD柱在零轴附近，方向未定"))

        if price_now > ma20 > ma50:
            trend_score += 10
            signals.append(("✅", "多头排列", f"价格>${ma20:.2f}(MA20)>${ma50:.2f}(MA50)"))
        elif price_now < ma20 < ma50:
            trend_score -= 10
            signals.append(("🔴", "空头排列", f"价格<MA20<MA50，下行趋势明确"))
        elif price_now > ma20:
            trend_score += 5
            signals.append(("🟡", "价格站上MA20", "短期趋势向好，但中期均线尚未跟上"))
        else:
            trend_score -= 5
            signals.append(("🟡", "价格跌破MA20", "短期趋势转弱"))

        if mom_1m > 10:
            trend_score += 10
            signals.append(("✅", "强势动量", f"1个月涨幅+{mom_1m:.1f}%，趋势强劲"))
        elif mom_1m < -15:
            trend_score -= 10
            signals.append(("🔴", "弱势动量", f"1个月跌幅{mom_1m:.1f}%，下行压力大"))

        if obv_trend == "上升" and obv_pct > 5:
            trend_score += 8
            signals.append(("✅", "OBV资金流入", f"能量潮高于均线{obv_pct:.1f}%，资金持续买入"))
        elif obv_trend == "下降" and obv_pct < -5:
            trend_score -= 8
            signals.append(("🔴", "OBV资金流出", f"能量潮低于均线{abs(obv_pct):.1f}%，资金持续流出"))
        else:
            signals.append(("⚪", "OBV中性", "资金流向尚不明确，趋势待确认"))

        if slope_pct > 0.15:
            trend_score += 6
            signals.append(("✅", "上升趋势", f"20日线性回归斜率 +{slope_pct:.2f}%/日，价格趋势向上"))
        elif slope_pct < -0.15:
            trend_score -= 6
            signals.append(("🔴", "下降趋势", f"20日线性回归斜率 {slope_pct:.2f}%/日，价格趋势向下"))
        else:
            signals.append(("⚪", "趋势平坦", f"20日线性回归斜率接近0（{slope_pct:.2f}%/日），横盘整理中"))

        if vol_ratio > 1.5 and mom_1m > 0:
            trend_score += 5
            signals.append(("✅", "放量上涨", f"成交量是均值的{vol_ratio:.1f}倍，资金流入确认"))
        elif vol_ratio > 1.5 and mom_1m < 0:
            trend_score -= 5
            signals.append(("🔴", "放量下跌", f"成交量是均值的{vol_ratio:.1f}倍，资金出逃信号"))

        if sharpe > 1.5:
            trend_score += 5
            signals.append(("✅", "夏普比率优秀", f"夏普={sharpe:.2f}（已扣无风险利率 {rf_annual*100:.2f}%），风险调整后收益极佳"))
        elif sharpe > 0.5:
            trend_score += 2
            signals.append(("🟡", "夏普比率良好", f"夏普={sharpe:.2f}（已扣无风险利率 {rf_annual*100:.2f}%），风险收益比尚可"))
        elif sharpe < 0:
            trend_score -= 5
            signals.append(("🔴", "夏普比率为负", f"夏普={sharpe:.2f}（已扣无风险利率 {rf_annual*100:.2f}%），跑不赢无风险收益，不如持有现金/短债"))

        trend_score = max(0, min(100, trend_score))

        # ── 基本面：既不是趋势也不是位置，单列 ─────────────────────
        if pe and pe > 0:
            if pe < 15:
                signals.append(("✅", "估值便宜", f"P/E={pe:.1f}x，低于市场平均"))
            elif pe > 50:
                signals.append(("🔴", "估值偏贵", f"P/E={pe:.1f}x，溢价明显需要高增长支撑"))

        if target and target > 0:
            _up = (target - price_now) / price_now * 100
            if _up > 20:
                signals.append(("✅", "分析师看多", f"一致目标价${target:.2f}，较现价上行空间{_up:.1f}%"))
            elif _up < -10:
                signals.append(("🔴", "分析师看空", f"一致目标价${target:.2f}，较现价下行风险{abs(_up):.1f}%"))

        # ── 评级：由"趋势 × 位置"二维组合决定，而不是把两者相加 ────────
        if trend_score >= 65:
            if stretch_score >= 70:
                rating = "顺势但偏贵"; rating_color = "#BA7517"; rating_emoji = "⏳"
                rating_note = "趋势方向是对的，但位置已经偏高，追进去的风险收益比不划算，等回调到均线附近更合适。"
            elif stretch_score <= 35:
                rating = "强力买入"; rating_color = "#0F6E56"; rating_emoji = "🚀"
                rating_note = "趋势强劲且位置不贵——方向和进场点同时有利，是技术面最理想的组合。"
            else:
                rating = "买入"; rating_color = "#1D9E75"; rating_emoji = "📈"
                rating_note = "趋势向上，位置处于中性区间，顺势参与的条件成立。"
        elif trend_score >= 45:
            if stretch_score <= 30:
                rating = "超卖反弹候选"; rating_color = "#BA7517"; rating_emoji = "🔍"
                rating_note = "趋势本身不强，但位置已经很低，属于博反弹而非趋势跟随，需要控制仓位。"
            elif stretch_score >= 70:
                rating = "回调风险"; rating_color = "#D85A30"; rating_emoji = "⚠️"
                rating_note = "趋势没有支撑，位置却已偏高——这是最容易被套的组合。"
            else:
                rating = "持有"; rating_color = "#BA7517"; rating_emoji = "⚖️"
                rating_note = "趋势与位置都在中性区间，缺乏明确的进出场信号，观望为主。"
        else:
            if stretch_score <= 30:
                rating = "止跌观察"; rating_color = "#D85A30"; rating_emoji = "🩹"
                rating_note = "跌幅已经很大、位置很低，但趋势尚未转向——「跌不动」不等于「要涨了」，等趋势确认再说。"
            elif stretch_score >= 70:
                rating = "强力卖出"; rating_color = "#A32D2D"; rating_emoji = "💥"
                rating_note = "趋势向下、位置却偏高，是风险收益比最差的组合。"
            else:
                rating = "卖出"; rating_color = "#D85A30"; rating_emoji = "📉"
                rating_note = "趋势向下，位置没有提供足够的安全边际。"

        # 兼容旧字段：score 现在代表趋势强度
        score = trend_score

        # ══ 价格区间：不再用动量外推一个"目标价" ═══════════════════════
        # 原来的写法是 mom_3m*0.5 + 15 + (100-rsi)*0.3 —— 把过去3个月的涨幅
        # 线性外推到未来，既没有估值锚，(100-rsi) 项还让"RSI越低目标价越高"，
        # 而这只票能进高档位又恰恰部分因为 RSI 低，属于循环论证。
        # 改成两样都给真实依据的东西：
        #   · 分析师一致目标价（yfinance 的 targetMeanPrice，真实数据）
        #   · 按这只票自身波动率推的 3 个月 ±1σ 区间（约 68% 概率落在其中）
        _sig_d = float(daily_returns.std()) if len(daily_returns) > 5 else 0.02
        _sig_3m = _sig_d * (63 ** 0.5)               # 3个月 ≈ 63 个交易日
        range_low  = price_now * math.exp(-_sig_3m)
        range_high = price_now * math.exp(_sig_3m)
        range_pct  = _sig_3m * 100

        analyst_target = float(target) if (target and target > 0) else None
        analyst_upside = ((analyst_target - price_now) / price_now * 100
                          if analyst_target else None)

        # 兼容旧字段：有分析师目标价就用它，否则退回现价（即"无预测"）
        price_target = analyst_target if analyst_target else price_now
        price_target_pct = analyst_upside if analyst_upside is not None else 0.0

        return {
            "ticker": ticker.upper(),
            "schema": ANALYSIS_SCHEMA,
            "rf_annual": rf_annual,
            "trend_score": trend_score,
            "stretch_score": stretch_score,
            "rating_note": rating_note,
            "range_low": range_low,
            "range_high": range_high,
            "range_pct": range_pct,
            "analyst_target": analyst_target,
            "analyst_upside": analyst_upside,
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
st.title(tr("app_title"))
st.caption(tr("app_subtitle"))

# ── 顶部免责声明（每个页面都能第一眼看到）──
st.markdown(
    '<div class="disc-slim">'
    '<span class="ds-icon">⚠️</span>'
    f'<div><b>{tr("disc_title")}</b></div>'
    '</div>', unsafe_allow_html=True)
with st.expander(tr("disc_more"), expanded=False):
    st.markdown(f'<span style="font-size:13px;line-height:1.75;color:#5b6678">{tr("disc_body")}</span>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 💾 持仓存档：导出 / 导入 / 编码进 URL
#    session_state 一刷新就没，所以提供三条持久化通路：
#    ① .json 存档文件  ② 分享链接（持仓编码进网址）  ③ 手动重录
# ══════════════════════════════════════════════════════════════════════════════
PF_SCHEMA = 1           # 存档格式版本，日后改结构时用来兼容旧档


def _ccy_full(code):
    """'USD' → 'USD 🇺🇸'（回退到列表第一项）"""
    code = (code or "").strip().upper()
    for c in CURRENCY_LIST:
        if c.split()[0] == code:
            return c
    return CURRENCY_LIST[0]


def pf_normalise(raw_list):
    """把任意来源（存档文件 / URL / 旧版 session）的持仓清洗成标准结构"""
    out = []
    for item in (raw_list or []):
        try:
            if isinstance(item, dict):
                tk   = str(item.get("ticker", "")).strip().upper()
                qty  = float(item.get("qty", 0) or 0)
                cost = float(item.get("cost", 0) or 0)
                ccy  = item.get("ccy") or item.get("currency") or "USD"
            else:                                   # 紧凑数组格式 [tk, qty, cost, ccy]
                tk   = str(item[0]).strip().upper()
                qty  = float(item[1])
                cost = float(item[2])
                ccy  = item[3] if len(item) > 3 else "USD"
            if not tk:
                continue
            out.append({"ticker": tk, "qty": qty, "cost": cost,
                        "ccy": _ccy_full(str(ccy).split()[0])})
        except Exception:
            continue                                 # 单条坏数据不影响其余持仓
    return out


def pf_encode(holdings):
    """持仓 → 可安全放进 URL 的 base64 短串"""
    import json, base64
    compact = [[h["ticker"], round(float(h["qty"]), 8), round(float(h["cost"]), 6),
                str(h.get("ccy", "USD")).split()[0]]
               for h in holdings if h.get("ticker")]
    raw = json.dumps([PF_SCHEMA, compact], separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def pf_decode(token):
    """base64 短串 → 持仓列表；解不开就返回 []"""
    import json, base64
    try:
        token = (token or "").strip()
        if not token:
            return []
        data = json.loads(base64.urlsafe_b64decode(
            token + "=" * (-len(token) % 4)).decode("utf-8"))
        payload = data[1] if isinstance(data, list) and len(data) == 2 else data
        return pf_normalise(payload)
    except Exception:
        return []


def pf_to_json_bytes(holdings):
    """持仓 → 带元信息的 .json 存档（给 download_button）"""
    import json
    from datetime import datetime as _dt_pf2
    doc = {
        "schema": PF_SCHEMA,
        "app": "2026 IPO Bubble Simulator",
        "saved_at": _dt_pf2.now().strftime("%Y-%m-%d %H:%M:%S"),
        "holdings": [{"ticker": h["ticker"], "qty": float(h["qty"]),
                      "cost": float(h["cost"]), "ccy": str(h.get("ccy", "USD")).split()[0]}
                     for h in holdings if h.get("ticker")],
    }
    return json.dumps(doc, indent=2, ensure_ascii=False).encode("utf-8")


def pf_from_json_bytes(blob):
    """.json 存档 → 持仓列表；抛异常交给调用方显示错误"""
    import json
    doc = json.loads(blob.decode("utf-8-sig"))
    raw = doc.get("holdings") if isinstance(doc, dict) else doc
    cleaned = pf_normalise(raw)
    if not cleaned:
        raise ValueError("no valid positions found")
    return cleaned



def _md_clean(text):
    """叙述文本里可能夹着 HTML 标签和实体，导出 Markdown 前清掉"""
    import re as _re_md
    t = _re_md.sub(r"<br\s*/?>", " ", str(text))
    t = _re_md.sub(r"<[^>]+>", "", t)
    for _ent, _ch in (("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"),
                      ("&gt;", ">"), ("&quot;", '"'), ("\u00a0", " ")):
        t = t.replace(_ent, _ch)
    return _re_md.sub(r"[ \t]{2,}", " ", t).strip()


def _md_heading(key):
    """把 I18N 里带 # 或 ** 装饰的小标题，还原成纯文字"""
    return _md_clean(tr(key)).strip("#* ").strip()


def _csv_bytes(header, rows):
    """行列表 → 带 BOM 的 CSV 字节流（BOM 让 Excel 正确认出 UTF-8 中文）"""
    import csv, io as _io_csv
    buf = _io_csv.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    return ("\ufeff" + buf.getvalue()).encode("utf-8")


def _report_header(title):
    """所有导出报告共用的抬头 —— 免责声明必须跟着报告一起走"""
    from datetime import datetime as _dt_rp
    return (f"# {title}\n\n"
            f"> {tr('rep_gen_at')}: {_dt_rp.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"> \n"
            f"> ⚠️ {_md_clean(tr('disc_title'))}\n"
            f"> {_md_clean(tr('disc_body'))}\n\n---\n\n")


tabs = st.tabs([tr("tab_market"), tr("tab_ipo"), tr("tab_history"), tr("tab_forecast"),
                tr("tab_macro"), tr("tab_analyzer"), tr("tab_holdings"), tr("tab_grail")])

# ── Tab 1: 市场概览 + 实时市场 ──────────────────────────────────────────────────
with tabs[0]:
    st.subheader(tr("sec_live"))

    live_data_t1 = fetch_market_data()
    if live_data_t1:
        _w_on, _w_iv, _w_left = watch_status()
        _wc1, _wc2, _wc3 = st.columns([1.1, 1.3, 3.6])
        if _wc1.button(tr("refresh_live"), key="refresh_t1", use_container_width=True):
            st.cache_data.clear(); st.rerun()
        if _w_on:
            if _wc2.button(tr("watch_stop"), key="watch_stop_t1", use_container_width=True):
                stop_watch(); st.rerun()
            _wc3.markdown(
                f'<div class="arow" style="margin-top:2px;background:rgba(29,158,117,.14);'
                f'border:1px solid rgba(29,158,117,.35)">'
                f'<span style="font-size:13px;color:#0F6E56;font-weight:600">'
                + tr("watch_bar_on", iv=_w_iv, mm=f"{_w_left//60:02d}", ss=f"{_w_left%60:02d}",
                     n=st.session_state.get("watch_count", 0)) + '</span></div>',
                unsafe_allow_html=True)
        else:
            if _wc2.button(tr("watch_start_short"), key="watch_start_t1", use_container_width=True, type="primary"):
                start_watch(); st.rerun()
            _wc3.markdown(
                f'<div class="arow" style="margin-top:2px">'
                f'<span style="font-size:12.5px;color:#64748b">'
                + tr("watch_bar_off", iv=st.session_state.get("watch_iv", 60),
                     mn=st.session_state.get("watch_min", 15)) + '</span></div>',
                unsafe_allow_html=True)

        cards_t1 = []
        for ticker, info in live_data_t1.items():
            if ticker == "^TNX":
                val = f"{info['price']:.2f}%"
            elif ticker.startswith("^"):
                val = f"{info['price']:,.2f}"
            else:
                val = f"${info['price']:,.2f}"
            _subs = ({"^IXIC": "NASDAQ 综合指数", "^GSPC": "S&P 500 指数",
                      "^VIX": "CBOE 波动率指数", "^TNX": "US 10Y Treasury"}
                     if st.session_state.get("lang", "zh") == "zh" else
                     {"^IXIC": "NASDAQ Composite", "^GSPC": "S&P 500 Index",
                      "^VIX": "CBOE Volatility Index", "^TNX": "US 10Y Treasury"})
            sub = _subs.get(ticker, ticker)
            cards_t1.append((ticker, asset_card_html(
                ticker, asset_name(ticker, info["name"]), sub, val, info["change_pct"],
                invert_color=(ticker == "^VIX"),
            )))
        render_asset_grid_clickable(cards_t1, key_prefix="t1card", cols=4)

        # ── 点击任意标的后，就在这一组卡片下方展开分析与走势 ──
        render_quick_view("t1card")

        with st.expander(tr("exp_read_each"), expanded=True):
            for ticker, info in live_data_t1.items():
                txt, tone = interpret_market(ticker, info)
                why(txt, tone, title=asset_name(ticker, info["name"]))

        st.subheader(tr("sec_today_change"))
        tl_t1 = [asset_name(k, v["name"]) for k, v in live_data_t1.items()]
        ch_t1 = [v["change_pct"] for v in live_data_t1.values()]
        fig_live_t1 = go.Figure(go.Bar(
            x=tl_t1, y=ch_t1,
            marker_color=["#A32D2D" if c < 0 else "#0F6E56" for c in ch_t1],
            text=[f"{c:+.2f}%" for c in ch_t1], textposition="outside",
        ))
        fig_live_t1.update_layout(
            height=300, yaxis_title=tr("ax_change"), plot_bgcolor="#fafafa",
            showlegend=False, margin=dict(t=20, b=20),
            yaxis=dict(zeroline=True, zerolinecolor="#cccccc"),
        )
        glass_chart(fig_live_t1, use_container_width=True)

        sentiment_t1 = market_to_sentiment(live_data_t1)
        label_t1 = (nt("lbl_panic2") if sentiment_t1 < 20 else nt("lbl_panic") if sentiment_t1 < 40
                    else nt("lbl_neutral") if sentiment_t1 < 60 else nt("lbl_optimistic")
                    if sentiment_t1 < 80 else nt("lbl_euphoric"))
        st.subheader(tr("sent_headline", label=label_t1, score=sentiment_t1))
        st.progress(sentiment_t1 / 100)
        _s_txt, _s_tone, _s_calc = explain_sentiment(live_data_t1, sentiment_t1)
        why(_s_txt, _s_tone, calc=_s_calc, title=tr("why_score_src"))
    else:
        st.warning(tr("err_live"))

    st.divider()
    st.subheader(tr("sec_crypto_metals"))

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

    cm_tab1, cm_tab2 = st.tabs([tr("sub_crypto"), tr("sub_metals")])
    with cm_tab1:
        crypto_data = fetch_crypto_metals_data(CRYPTO_TICKERS)
        if crypto_data:
            render_asset_grid_clickable([
                (tk, asset_card_html(tk, asset_name(tk, info["name"]), tk.replace("-USD", " / USD"),
                                     f"${info['price']:,.2f}", info["change_pct"],
                                     note=get_track_info(tk)[0]))
                for tk, info in crypto_data.items()
            ], key_prefix="cryptocard", cols=3)
            render_quick_view("cryptocard")
            fig_crypto = go.Figure(go.Bar(
                x=[asset_name(k, v["name"]) for k, v in crypto_data.items()],
                y=[v["change_pct"] for v in crypto_data.values()],
                marker_color=["#A32D2D" if v["change_pct"] < 0 else "#0F6E56" for v in crypto_data.values()],
                text=[f"{v['change_pct']:+.2f}%" for v in crypto_data.values()], textposition="outside",
            ))
            fig_crypto.update_layout(height=280, yaxis_title=tr("ax_change_24h"), plot_bgcolor="#fafafa",
                                     showlegend=False, margin=dict(t=20, b=20),
                                     yaxis=dict(zeroline=True, zerolinecolor="#cccccc"))
            glass_chart(fig_crypto, use_container_width=True)
            avg_chg = sum(v["change_pct"] for v in crypto_data.values()) / len(crypto_data)
            crypto_mood = (tr("mood_up") if avg_chg > 2 else
                           tr("mood_dn") if avg_chg < -2 else tr("mood_flat"))
            why(tr("crypto_overall", mood=crypto_mood, avg=avg_chg),
                "good" if avg_chg > 0 else "bad", title=tr("why_overall"))
            with st.expander(tr("exp_read_coin"), expanded=False):
                for tk, info in crypto_data.items():
                    txt, tone = interpret_crypto(tk, info)
                    why(txt, tone, title=asset_name(tk, info["name"]))
            st.caption(tr("crypto_hint"))
        else:
            st.warning(tr("err_crypto"))

    with cm_tab2:
        metals_data = fetch_crypto_metals_data(METALS_TICKERS)
        if metals_data:
            render_asset_grid_clickable([
                (tk, asset_card_html(tk, asset_name(tk, info["name"]),
                                     tr("futures") if "=" in tk else tk,
                                     f"${info['price']:,.2f}", info["change_pct"],
                                     note=get_track_info(tk)[0]))
                for tk, info in metals_data.items()
            ], key_prefix="metalcard", cols=3)
            render_quick_view("metalcard")
            fig_metals = go.Figure(go.Bar(
                x=[asset_name(k, v["name"]) for k, v in metals_data.items()],
                y=[v["change_pct"] for v in metals_data.values()],
                marker_color=["#A32D2D" if v["change_pct"] < 0 else "#0F6E56" for v in metals_data.values()],
                text=[f"{v['change_pct']:+.2f}%" for v in metals_data.values()], textposition="outside",
            ))
            fig_metals.update_layout(height=280, yaxis_title=tr("ax_change_today"), plot_bgcolor="#fafafa",
                                     showlegend=False, margin=dict(t=20, b=20),
                                     yaxis=dict(zeroline=True, zerolinecolor="#cccccc"))
            glass_chart(fig_metals, use_container_width=True)
            _m_avg = sum(v["change_pct"] for v in metals_data.values()) / len(metals_data)
            why(tr("metal_overall", avg=_m_avg),
                "good" if _m_avg > 0 else "neutral", title=tr("why_overall"))
            with st.expander(tr("exp_read_metal"), expanded=False):
                for tk, info in metals_data.items():
                    txt, tone = interpret_metal(tk, info)
                    why(txt, tone, title=asset_name(tk, info["name"]))
        else:
            st.warning(tr("err_metals"))

    st.divider()
    st.subheader(tr("sub_ipo_overview"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(tr("m_total_mcap"), "$3.12T", tr("m_total_mcap_d"))
    c2.metric(tr("m_q1_raise"), "$42.6B", tr("m_q1_raise_d"))
    c3.metric(tr("m_ai_share"), "80%", tr("m_ai_share_d"), delta_color="inverse")
    c4.metric(tr("m_bubble_idx"), "74/100", tr("m_bubble_idx_d"), delta_color="inverse")

    _ipo_why = [
        (tr("ipo_w1_t"), nt("ipo_w1"), "warn"),
        (tr("ipo_w2_t"), nt("ipo_w2"), "warn"),
        (tr("ipo_w3_t"), nt("ipo_w3"), "bad"),
        (tr("ipo_w4_t"), nt("ipo_w4"), "bad"),
    ]
    with st.expander(tr("exp_four_numbers"), expanded=False):
        for _ttl, _desc, _tone in _ipo_why:
            why(_desc, _tone, title=_ttl)

    st.subheader(tr("sub_conc_risk"))
    _conc_items = [
        ("conc_ai_t",      "conc_ai",      88),
        ("conc_liq_t",     "conc_liq",     79),
        ("conc_prof_t",    "conc_prof",    72),
        ("conc_lock_t",    "conc_lock",    65),
        ("conc_absorb_t",  "conc_absorb",  42),
    ]
    for _tk_, _dk_, _val_ in _conc_items:
        st.progress(_val_ / 100, text=f"{tr(_tk_)}：**{_val_}%**")
        why(nt(_dk_), "bad" if (_val_ >= 70 or _dk_ == "conc_absorb") else "warn", title=tr(_tk_))

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
            # 取不到就什么都不显示。宁可少一块，也不要再挂一个
            # 上市第 4 天写死的价格 —— 那正是之前价格三个月不更新的原因。
            return live
        except Exception:
            return {}

    live_ipo = fetch_ipo_live_prices()

    # 已上市公司实时价格横幅
    if live_ipo:
        st.subheader(tr("sub_ipo_live"))
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
                f'<div style="font-size:12px;opacity:.8;margin-top:2px">{tr("ipo_listed_on")}</div>'
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
        if st.button(tr("btn_refresh_price"), key="refresh_ipo_live"):
            st.cache_data.clear(); st.rerun()

    # 估值分布图（从原市场概览移过来）
    st.subheader(tr("sub_val_dist"))
    names = [c["name"] for c in IPOS]
    vals  = [c["val_b"] for c in IPOS]  # SpaceX已更新为上市后实际市值$1770B
    fig_bar = go.Figure(go.Bar(
        x=names, y=vals, marker_color=COLORS,
        text=[f"${v/1000:.2f}T" if v>=1000 else f"${v}B" for v in vals],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>" + tr("hover_val") + ": $%{y}B<extra></extra>",
    ))
    fig_bar.update_layout(height=320, margin=dict(t=30,b=20),
                          yaxis_title=tr("ax_valuation"), showlegend=False,
                          plot_bgcolor="#fafafa")
    glass_chart(fig_bar, use_container_width=True)

    st.divider()
    st.subheader(tr("sub_company_deep"))
    # 手工维护的数据必须让人看得见它有多旧
    from datetime import datetime as _dt_ipo
    try:
        _age = (_dt_ipo.now() - _dt_ipo.strptime(IPO_DATA_ASOF, "%Y-%m-%d")).days
    except Exception:
        _age = 0
    if _age > 90:
        st.warning(tr("ipo_asof_old", d=IPO_DATA_ASOF, n=_age))
    else:
        st.caption(tr("ipo_asof", d=IPO_DATA_ASOF))

    selected = st.selectbox(tr("sel_company"), [c["name"] for c in IPOS])
    company  = next(c for c in IPOS if c["name"] == selected)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(company["name"])
        st.caption(company["sector"] + " · " + company["date"])
        st.write(_nolatex(company["desc"]))
    with col2:
        ps      = round(company["val_b"] / company["rev_b"])
        val_str = f"${company['val_b']/1000:.2f}T" if company["val_b"] >= 1000 else f"${company['val_b']}B"
        m1,m2,m3 = st.columns(3)
        m1.metric(tr("m_exp_val"), val_str)
        m2.metric(tr("m_revenue"), f"${company['rev_b']}B")
        # 年化跑步收入 ≠ 财年实际收入。两者混在一起比 P/S 是不公平的，
        # 所以哪一条用的是跑步口径，必须在页面上说清楚。
        _rb = company.get("rev_basis")
        m2.caption(tr("rev_runrate") if _rb == "runrate" else tr("rev_fy"))
        m3.metric(tr("m_ps"), f"{ps}x")
        m4,m5,m6 = st.columns(3)
        m4.metric(tr("m_profitable"), tr("yes_profit") if company["profitable"] else tr("no_profit"))
        m5.metric(tr("m_day1_pop"), f"+{company['exp_pop']}%")
        m6.metric(tr("m_bubble_risk"), f"{company['bubble_risk']}%",
                  delta_color="inverse" if company["bubble_risk"]>60 else "normal")

    # ── 点进公司看真实走势与技术分析（已上市的才有行情）──
    _co_ticker = company.get("ticker")
    if _co_ticker:
        if st.button(tr("btn_view_company", name=company["name"], tk=_co_ticker),
                     key=f"ipo_analyze_{_co_ticker}", use_container_width=True, type="primary"):
            st.session_state["ipo_quick_view"] = _co_ticker
            st.session_state["selected_ticker"] = _co_ticker
            st.session_state["analysis_result"] = None
            st.rerun()
    else:
        st.info(tr("ipo_not_listed", name=company["name"], date=company["date"]))

    if st.session_state.get("ipo_quick_view"):
        _iv = st.session_state["ipo_quick_view"]
        st.divider()
        _ic1, _ic2 = st.columns([5, 1])
        _ic1.markdown(tr("quick_chart_title", tk=_iv))
        if _ic2.button(tr("btn_close"), key="ipo_qv_close", use_container_width=True):
            st.session_state["ipo_quick_view"] = None
            st.rerun()
        with st.spinner(tr("analyzing", tk=_iv)):
            render_quick_analysis(_iv)
        st.divider()

    st.caption(tr("ps_basis_note"))
    st.subheader(tr("sub_compare_all"))
    fig_bubble = go.Figure(go.Scatter(
        x=[c["bubble_risk"] for c in IPOS], y=[c["exp_pop"] for c in IPOS],
        mode="markers+text", text=[c["name"] for c in IPOS], textposition="top center",
        marker=dict(size=[max(14,math.log(c["val_b"]+1)*4) for c in IPOS],
                    color=[c["bubble_risk"] for c in IPOS], colorscale="RdYlGn_r",
                    showscale=True, colorbar=dict(title=tr("m_bubble_risk")),
                    line=dict(width=1, color="white")),
        hovertemplate="<b>%{text}</b><br>" + tr("m_bubble_risk") + ": %{x}%<br>" + tr("m_day1_pop") + ": +%{y}%<extra></extra>",
    ))
    fig_bubble.update_layout(height=380, xaxis_title=tr("ax_bubble_risk"),
                             yaxis_title=tr("ax_day1"), plot_bgcolor="#fafafa", margin=dict(t=10))
    glass_chart(fig_bubble, use_container_width=True)

# ── Tab 3: 历史对比 ─────────────────────────────────────────────────────────────
with tabs[2]:
    st.subheader(tr("sub_history"))
    nodes=HISTORICAL["节点"]; fig_hist=go.Figure()
    fig_hist.add_trace(go.Scatter(x=nodes,y=HISTORICAL["2000互联网"],name=tr("hist_dotcom"),
        line=dict(color="#E24B4A",dash="dash",width=2),mode="lines+markers"))
    fig_hist.add_trace(go.Scatter(x=nodes,y=HISTORICAL["2021 SPAC"],name=tr("hist_spac"),
        line=dict(color="#BA7517",dash="dot",width=2),mode="lines+markers"))
    fig_hist.add_trace(go.Scatter(x=nodes[:4],y=[100,130,180,240],name=tr("hist_ai"),
        line=dict(color="#534AB7",width=3),mode="lines+markers"))
    fig_hist.update_layout(height=420,yaxis_title=tr("ax_index_base"),
                           plot_bgcolor="#fafafa",legend=dict(orientation="h",y=-0.2))
    glass_chart(fig_hist, use_container_width=True)
    col1,col2,col3=st.columns(3)
    col1.error(_nolatex(nt("hist_c1")))
    col2.warning(nt("hist_c2"))
    col3.info(_nolatex(nt("hist_c3")))

# ── (实时市场已合并到Tab1) ──────────────────────────────────────────────────────

# ── Tab 4: 趋势预测 + 泡沫模拟 ────────────────────────────────────────────────────
with tabs[3]:

    # ══════════════════════════════════════════════════════════════════════
    # 🌡️ 当前泡沫程度 —— 打开页面就算好，不需要用户做任何操作
    # ══════════════════════════════════════════════════════════════════════
    live_data_sim = fetch_market_data()
    _bn = bubble_now(live_data_sim)
    _bsim = _bn["sim"]

    st.markdown(tr("bub_now_title"))
    st.caption(tr("bub_now_cap"))
    if not _bn["has_data"]:
        st.warning(tr("bub_nodata"))

    # 温度决定整条横幅的颜色
    _tv = _bsim["temp"]
    _tc = ("#A32D2D" if _tv >= 80 else "#D85A30" if _tv >= 65 else
           "#BA7517" if _tv >= 45 else "#1D9E75")
    st.markdown(
        f'<div style="background:linear-gradient(120deg,{_tc} 0%,{_tc}cc 60%,{_tc}99 100%);'
        f'color:white;padding:18px 22px;border-radius:14px;margin:6px 0 4px">'
        f'<div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap">'
        f'<span style="font-size:42px;font-weight:780;line-height:1">{_tv}</span>'
        f'<span style="font-size:15px;opacity:.9">/100　{tr("bub_temp")}</span>'
        f'<span style="margin-left:auto;text-align:right">'
        f'<span style="font-size:19px;font-weight:700">{_bsim["label"]}</span><br>'
        f'<span style="font-size:11.5px;opacity:.85">{tr("bub_label_from", b=_bsim["burst"])}</span>'
        f'</span>'
        f'</div>'
        f'<div style="font-size:13px;opacity:.95;margin-top:8px;line-height:1.65">'
        f'{_bsim["desc"]}</div></div>',
        unsafe_allow_html=True)

    _bc1, _bc2, _bc3 = st.columns(3)
    _bc1.metric(tr("bub_burst"), f"{_bsim['burst']}%")
    _bc2.metric(tr("bub_pop"), f"{_bsim['pop']:+d}%")
    _bc3.metric(tr("bub_six"), f"{_bsim['six_m']:+d}%")

    # ── 为什么是这个数：四个因子逐项拆解 ──
    st.markdown(tr("bub_why_title"))
    st.caption(tr("bub_why_cap"))
    if _bn.get("burst_clamped") or _bn.get("temp_clamped"):
        st.caption(tr("bub_clamped", raw=_bn["raw_burst"], shown=_bsim["burst"]))

    _fname = {"sentiment": "bub_f_sentiment", "ai": "bub_f_ai",
              "retail": "bub_f_retail", "rate": "bub_f_rate"}
    for _f in _bn["breakdown"]:
        _fk = _f["key"]
        # 对破裂概率为正 = 增加破裂风险；对温度贡献大 = 推高泡沫
        _tone = ("bad" if _f["burst"] > 15 else
                 "warn" if _f["temp"] > 25 else "neutral")
        if _fk == "ai":
            _desc = (tr("bub_d_ai", ex=_f.get("excess", 0.0)) if _f.get("live")
                     else tr("bub_d_ai_off"))
        else:
            _desc = tr("bub_d_" + _fk)

        # 情绪这一项再往下拆一层，让 VIX / 纳指 / 英伟达各自的贡献可见
        if _fk == "sentiment" and _f.get("parts"):
            _pl = []
            for _pn, _pv, _pc, _pk in _f["parts"]:
                if _pk in ("vix_lo", "vix_hi"):
                    _pt = tr("bub_p_vix_lo" if _pk == "vix_lo" else "bub_p_vix_hi", v=_pv)
                elif _pk == "idx":
                    _pt = tr("bub_p_idx", v=_pv)
                else:
                    _pt = tr("bub_p_nvda", v=_pv)
                _pl.append(f"{_pt} → **{_pc:+.1f}**")
            _desc += "　　" + tr("bub_sent_break", s=_f["value"]) + "：" + "；".join(_pl) + "。"

        why(_desc, _tone,
            calc=(f'{tr("bub_col_live")} {_f["raw"]}　→　'
                  f'{tr("bub_col_temp")} {_f["temp"]:+.1f}　·　'
                  f'{tr("bub_col_burst")} {_f["burst"]:+.1f}'),
            title=f'{tr(_fname[_fk])}　{_f["raw"]}')

    if st.button(tr("bub_refresh"), key="bub_recompute"):
        st.cache_data.clear()
        st.rerun()

    st.divider()


    # ══════════════════════════════════════════════════════════════════════
    # 🎛️ 泡沫模拟（已整合至趋势预测）
    # ══════════════════════════════════════════════════════════════════════
    with st.expander(tr("bub_whatif"), expanded=False):
        st.caption(tr("bub_whatif_cap"))
        # 四个输入直接复用页面顶部已经算好的实时读数，不再各算一遍
        auto_sentiment = _bn["sentiment"]
        auto_rate      = _bn["rate"]
        auto_retail    = _bn["retail"]
        auto_ai        = _bn["ai_speed"]
        vix            = _bn["vix"]
        
        mode_col1, mode_col2 = st.columns([1, 2])
        with mode_col1:
            auto_mode = st.toggle("🤖 自动驾驶模式", value=True,
                                  help="开启后从实时市场数据自动计算所有参数")
        with mode_col2:
            if auto_mode:
                st.success(f"✅ 已接入实时数据 · 情绪={auto_sentiment} · 利率={auto_rate}% · "
                           f"AI速度={auto_ai} · 散户={auto_retail}")
                if st.button("🔄 刷新实时参数", key="refresh_sim"):
                    st.cache_data.clear()
                    st.rerun()
            else:
                st.caption("💡 手动模式：拖动滑块或选择情景预设")
        
        st.divider()
        
        if auto_mode:
            sentiment = auto_sentiment
            rate      = auto_rate
            ai_speed  = auto_ai        # 原来写死 60，现在由 AI 板块相对强度实算
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
            st.info(f"**{sim['label']}** — {_nolatex(sim['desc'])}")
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
        hc[1].markdown(_nolatex("**投入金额 ($)**"))
        hc[2].markdown("**占比**")
        hc[3].markdown("**删除**")

        to_remove = []
        for idx, pos in enumerate(portfolio):
            rc = st.columns([2,2,1,1])
            with rc[0]:
                new_ticker = ticker_autocomplete(f"pf_t_{idx}", default=pos["ticker"],
                                                 label="股票代码", label_visibility="collapsed")
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
        with ac[0]:
            new_tk = ticker_autocomplete("pf_ntk", default="",
                                         label="新增股票代码", label_visibility="collapsed")
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
            pf_c3.metric("总投资额", f"${total_invest:,.0f}", "填写金额合计", delta_color="off")

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
            report_invalid_tickers([p["ticker"] for p in portfolio], set(pf_data.keys()), where="组合分析")
            if not valid_pf:
                st.error("没有任何一个代码能取到行情，因此无法分析。请用上面的下拉框重新选择标的"
                         "（输入首字母就会出候选，例如输入 TS 会出现 TSLA）。")
            else:
                valid_total = sum(p["amount"] for p in valid_pf)
                weights = [p["amount"]/valid_total for p in valid_pf]
                if abs(valid_total - total_invest) > 0.01:
                    why(f"上方「总投资额」显示的是你填写的全部金额 **${total_invest:,.0f}**，"
                        f"但其中只有 **${valid_total:,.0f}** 对应的代码能取到真实行情，"
                        f"下面的饼图、风险指标和蒙地卡罗模拟**只用这 ${valid_total:,.0f} 计算**。"
                        f"把上面标红的代码改对之后，这两个数字就会一致。",
                        "warn", title="为什么饼图和总投资额对不上")

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
                    st.info(_nolatex(f"≈ **${invest_usd:,.2f} USD** | 汇率: 1 {curr_code} = {fx_rate:.4f} USD"))
                else:
                    st.info(_nolatex(f"投资金额：**${invest_usd:,.2f} USD**"))

            # 计算可购买股数
            shares = invest_usd / params["price"] if params["price"] > 0 else 0
            st.caption(_nolatex(f"📊 以当前价格 ${params['price']:.2f} 可购入约 **{shares:.2f} 股** {params['ticker']}"))

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

    # ── 新闻情绪分类 ──────────────────────────────────────────────
    # 旧版是裸关键词匹配，两个毛病很致命：
    #   1. 把国名（china/russia/taiwan…）当成地缘风险词 ——
    #      "China retail sales beat expectations" 会被判成地缘利空；
    #   2. 只匹配裸名词 —— "inflation" 一律算利空，
    #      可 "inflation cools" 明明是利多。
    # 改成"主题词 + 方向词"的组合规则，并处理否定式。
    import re as _re_news

    # "价格类"主语 —— 只有绑定它，涨跌词才有确定的多空含义。
    # 这里刻意不放通配符：宁可漏判也不要判反。
    # "Nvidia surges" 没有主语词会落到中性，而 "Nvidia shares surge" 能命中。
    _MKT = (r"(stocks?|shares?|equit\w*|markets?|index|indices|futures|"
            r"nasdaq|s&p|dow|bitcoin|crypto|oil|gold|treasur\w*|bonds?|yields?)")

    _BULL_RULES = [
        r"rate cut", r"\bfed (cut|cuts|easing|pivot)",
        r"beat(s|ing)? (estimat|expect|forecast|street)",
        r"(record|all-time) (high|profit|revenue|quarter)",
        r"upgrade[sd]?\b", r"\brall(y|ies|ied)\b",
        # surge/jump/soar 必须绑定"价格类"主语：
        # "stocks surge" 是利多，"inflation surges" 是利空，裸词会两边都命中
        _MKT + r"\s+(\w+\s+){0,2}(surge|jump|soar|climb|gain|ris|advance|rebound)",
        r"strong (demand|growth|earnings|guidance|hiring)",
        r"(profit|revenue|earnings) (jump|surge|ris|beat|grow)",
        r"inflation (cool|eas|slow|fall|drop|declin|moderat|retreat|plunge|sink|tumbl|slid)",
        r"unemployment (fall|drop|declin|improv|ease|eas)",
        r"(raises|lifts|hikes) (guidance|outlook|forecast)",
        r"\bstimulus\b", r"\bai boost\b",
    ]
    _BEAR_RULES = [
        r"rate hike", r"\bfed (hike|hikes|raise|tighten)",
        r"\brecession\b", r"miss(es|ed|ing)? (estimat|expect|forecast|street)",
        # 同理，跌类词也要绑主语："inflation plunges" 其实是利多
        r"sell-?off", r"\bcrash(es|ed)?\b",
        _MKT + r"\s+(\w+\s+){0,2}(plunge|slump|tumble|sink|slide|drop|fall|dive)",
        r"\brout\b",
        r"layoff|job cuts|hiring freeze", r"bankrupt", r"downgrade[sd]?\b",
        r"inflation (surg|jump|spike|soar|acceler|climb|ris|hotter|heat|re-?accelerat)",
        r"unemployment (ris|jump|surg|climb|worsen)",
        r"weak (demand|growth|earnings|guidance|jobs)",
        r"(cuts|lowers|slashes) (guidance|outlook|forecast)",
        r"\bwarn(s|ing|ed)?\b", r"\bprobe\b|\binvestigation\b",
    ]
    # 真正的冲突/贸易壁垒词，不含任何国名
    _GEO_RULES = [
        r"\bwar\b(?! ?chest)", r"\binvasion\b|\binvade", r"\bmissile",
        r"air ?strike", r"\bsanction", r"\bembargo", r"\bceasefire",
        r"military (strike|action|buildup|operation)", r"\bcoup\b",
        r"\btariff", r"trade war", r"export (ban|control|restriction)",
    ]
    # 否定式：出现这些词时，命中的极性不能直接采信
    _NEG = _re_news.compile(
        r"(no longer|not |isn.t|aren.t|won.t|fails? to|unlikely|denies|denied|"
        r"rules out|avoids?|averted|no sign of|despite)")

    def classify_news(title):
        t = " " + str(title).lower().strip() + " "

        def _hits(rules):
            return sum(1 for p in rules if _re_news.search(p, t))

        g, b, r = _hits(_GEO_RULES), _hits(_BULL_RULES), _hits(_BEAR_RULES)
        negated = bool(_NEG.search(t))

        # 有否定词时，多空双方都降权到"存疑"，不硬判方向
        if negated and abs(b - r) <= 1:
            return ("⚪", "中性", "#555", "#F5F5F5",
                    "标题含否定或转折表述，方向不明确，未计入情绪打分。")

        # 地缘词只有在没有更强的多空信号时才主导
        if g and g >= max(b, r):
            return ("🌍", "地缘政治", "#534AB7", "#EEEDFE",
                    "地缘/贸易壁垒风险，通常推升避险需求，压制科技股和周期股。")
        if b > r:
            return ("🟢", "利多信号", "#0F6E56", "#E1F5EE",
                    "正面消息，可能推动相关板块上涨，成长股和科技股受益。")
        if r > b:
            return ("🔴", "利空信号", "#A32D2D", "#FCEBEB",
                    "负面消息，可能引发回调，防御性资产相对受益。")
        # 多空持平（含都没命中）一律归中性，不再偏向任何一边
        return ("⚪", "中性", "#555", "#F5F5F5",
                "未识别出明确的方向性信号，对市场整体影响视为中性。")

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

    st.caption("ℹ️ 新闻情绪由**关键词规则**判定（主题词+方向词组合，含否定式处理），"
               "不是语义理解，对反讽、复杂从句和一词多义会判错。仅作粗略参考。")

    # 地缘事件按半个利空计入：它通常压制风险资产，但强度弱于直接的基本面利空
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
    st.subheader(tr("sec_analyzer"))
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
                    if st.button(tr("btn_analyze"), key=f"q_{group}_{tk}", use_container_width=True):
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
        analyze_btn = st.button(tr("btn_start_analyze"), use_container_width=True, type="primary")

    # 触发分析：点击开始分析 或 输入框里有内容且与上次不同
    if analyze_btn and ticker_input:
        st.session_state["selected_ticker"] = ticker_input
        st.session_state["analysis_result"] = None  # 强制重新分析

    # session_state 跨代码更新会保留，旧结构的结果缺新字段会直接 KeyError，
    # 这里认出版本不符就丢掉重算，用户不用手动硬刷新。
    _cached = st.session_state.get("analysis_result")
    if (isinstance(_cached, dict) and "error" not in _cached
            and _cached.get("schema") != ANALYSIS_SCHEMA):
        st.session_state["analysis_result"] = None

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
            # 取一次就好。.get 回退是为了兼容结构更新前残留在 session_state
            # 里的旧结果（ANALYSIS_SCHEMA 已经会拦掉，这里是第二道保险）。
            _tsc = result.get("trend_score", result.get("score", 50))
            _ssc = result.get("stretch_score", 50)
            _rnote = result.get("rating_note", "")
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
                f'<div style="font-size:12.5px;opacity:.92">趋势 {_tsc}/100　·　'
                f'位置 {_ssc}/100</div>'
                f'</div></div></div>',
                unsafe_allow_html=True
            )

            # ── 核心指标 ──
            m1,m2,m3,m4,m5 = st.columns(5)
            _at = result.get("analyst_target")
            _au = result.get("analyst_upside")
            m1.metric("📍 当前价格", f"${result['price_now']:.2f}")
            if _at:
                m2.metric("🎯 分析师目标价", f"${_at:.2f}",
                          f"{_au:+.1f}%", delta_color="normal" if _au >= 0 else "inverse")
            else:
                m2.metric("🎯 分析师目标价", "—", "无覆盖", delta_color="off")
            m3.metric("📐 3个月波动区间",
                      f"${result.get('range_low', result['price_now']):.0f} – {result.get('range_high', result['price_now']):.0f}",
                      f"±{result.get('range_pct', 0):.0f}%", delta_color="off")
            m4.metric("📈 趋势强度", f"{_tsc}/100",
                      "向上" if _tsc >= 65 else
                      "向下" if _tsc < 45 else "中性",
                      delta_color="normal" if _tsc >= 65
                      else "inverse" if _tsc < 45 else "off")
            m5.metric("📍 位置（超买超卖）", f"{_ssc}/100",
                      "偏贵" if _ssc >= 70 else
                      "偏低" if _ssc <= 30 else "中性",
                      delta_color="inverse" if _ssc >= 70
                      else "normal" if _ssc <= 30 else "off")

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
            why((f"这是华尔街分析师的**一致目标价**（{result.get('analyst_n') or '多'}家机构均值，来自雅虎财经），"
                 f"不是本站算的。相对现价还有 **{_au:+.1f}%** 的空间。"
                 f"分析师目标价通常是 12 个月视角，且系统性偏乐观，看方向比看数值更有意义。"
                 if _at else
                 "雅虎财经没有这只标的的分析师覆盖数据（指数、商品期货、部分加密货币通常都没有）。"
                 "本站**不会自己编一个目标价**——右边的波动区间才是有依据的参考。"),
                "good" if (_au or 0) >= 0 else "bad", title="分析师目标价", target=m2)
            why(f"这不是预测，是按这只标的**自身的历史波动率**推出来的统计区间："
                f"日收益标准差 × √63（3个月的交易日数）得到 ±{result.get('range_pct', 0):.1f}%，"
                f"即约 **68% 的概率**落在 ${result.get('range_low', result['price_now']):.2f} – ${result.get('range_high', result['price_now']):.2f} 之间。"
                f"区间越宽说明这只票越颠簸，同样的仓位承担的风险越大。"
                f"（前提是收益近似对数正态且波动率不变——真实市场两条都只是近似。）",
                "neutral", title="3个月波动区间", target=m3)
            why(f"**趋势强度**只由方向性指标构成：MACD、均线排列、1个月动量、OBV资金流、"
                f"20日回归斜率、成交量配合、夏普比率。它回答的是「**往哪个方向走**」，"
                f"不掺任何超买超卖判断。当前 {_tsc}/100"
                + ("，方向明确向上。" if _tsc >= 65
                   else "，方向明确向下。" if _tsc < 45 else "，方向不明朗。"),
                "good" if _tsc >= 65 else "bad" if _tsc < 45 else "neutral",
                title="趋势强度", target=m4)
            why(f"**位置分**只由摆动指标构成：RSI {result['rsi']:.1f}、布林带位置、"
                f"斐波那契回撤、距52周高点 {result['price_from_high']:.1f}%。"
                f"它回答的是「**现在贵不贵**」，越高越超买。当前 {_ssc}/100"
                + ("，位置偏高，追进去性价比差。" if _ssc >= 70
                   else "，位置偏低，安全边际相对好。" if _ssc <= 30
                   else "，处在中性区间。")
                + "　这两个分数**故意分开**——把它们相加会互相抵消，"
                  "强势上涨股和暴跌股会得到几乎一样的分数。",
                "bad" if _ssc >= 70 else "good" if _ssc <= 30 else "neutral",
                title="位置（超买超卖）", target=m5)
            st.markdown(
                f'<div style="background:{result["rating_color"]};color:white;padding:12px 18px;'
                f'border-radius:10px;font-size:14px;margin:10px 0">'
                f'<b style="font-size:16px">{result["rating_emoji"]} {result["rating"]}</b>'
                f'　<span style="opacity:.9">趋势 {_tsc}/100　·　'
                f'位置 {_ssc}/100</span><br>'
                f'<span style="font-size:13px;opacity:.94">{_md_bold(_rnote)}</span></div>',
                unsafe_allow_html=True)
            why(f"评级不是把两个分数相加，而是看它们的**组合**："
                f"趋势 {_tsc} × 位置 {_ssc} 落在「{result['rating']}」这一格。"
                f"下方「技术信号详情」共 **{_pos} 条利多、{_neg} 条利空、{_neu} 条中性**。"
                f"　四个象限的含义：趋势强+位置低=最理想；趋势强+位置高=方向对但等回调；"
                f"趋势弱+位置低=跌多了但没转向，别急着接；趋势弱+位置高=风险收益比最差。",
                "good" if _tsc >= 65 else "bad" if _tsc < 45 else "neutral",
                title="评级怎么来的")

            # ── 买入/卖出理由 ──
            st.subheader("🧠 分析师意见")

            def gen_reason(r):
                lines = []
                p = r["price_now"]
                # 按趋势分判方向，而不是匹配评级名字 —— 评级现在有9种，写死名字必漏
                _ts = r.get("trend_score", r.get("score", 50))
                _ss = r.get("stretch_score", 50)
                _dir = "偏多" if _ts >= 65 else "偏空" if _ts < 45 else "中性"
                lines.append(f"**{r['ticker']} 技术面{_dir}：趋势强度 {_ts}/100、"
                             f"位置 {_ss}/100，给予「{r['rating']}」评级。**")

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
                    agree = ("与本模型的趋势判断一致。" if (upside > 0) == (r.get("trend_score", r.get("score", 50)) >= 50)
                             else "与本模型的趋势判断存在分歧，建议综合参考。")
                    lines.append(f"华尔街分析师平均目标价为 ${r['target_analyst']:.2f}，较现价 {'+' if upside>=0 else ''}{upside:.1f}%，{agree}")

                lines.append(
                    f"综合以上因素：趋势强度 {r.get('trend_score', r.get('score', 50))}/100、位置 {r.get('stretch_score', 50)}/100，"
                    f"评级为「{r['rating']}」。{r.get('rating_note', '')}"
                    f"　按该标的自身波动率推算，未来3个月约有 68% 的概率落在 "
                    f"${r.get('range_low', r['price_now']):.2f} – ${r.get('range_high', r['price_now']):.2f} 区间内。"
                    + (f"华尔街分析师一致目标价为 ${r.get('analyst_target') or 0:.2f}"
                       f"（{r.get('analyst_upside') or 0:+.1f}%）。" if r.get("analyst_target") else
                       "该标的没有分析师覆盖数据，本站不提供自编的目标价。"))

                if _ts >= 65 and _ss >= 70:
                    lines.append("趋势站在你这边，但位置已经偏高：与其追价，不如等回调到 MA20 附近再分批建仓，"
                                 "止损设于近期低点下方 3–5%。")
                elif _ts >= 65:
                    lines.append("方向与位置都不逆风，可逢低分批建仓，严格设置止损位（建议设于近期低点下方3-5%）。")
                elif _ts >= 45 and _ss <= 30:
                    lines.append("这是博反弹而非趋势跟随：只适合小仓位试错，且必须设硬止损，"
                                 "趋势指标转正之前不要加仓。")
                elif _ts >= 45:
                    lines.append("建议持仓观望，等待更明确的方向性信号后再做决策。")
                elif _ss <= 30:
                    lines.append("跌幅虽大但趋势尚未转向——「跌不动」不等于「要涨了」。"
                                 "等 MACD 翻正、价格站回 MA20 之后再考虑介入。")
                else:
                    lines.append("建议减仓或设置严格止损，控制下行风险，等待技术面好转后再考虑重新介入。")

                return lines

            # 直接复用评级自带的主色，省得再维护一份会漏掉新评级的映射表
            _tint = {"#0F6E56": "#E1F5EE", "#1D9E75": "#F0FAF5", "#BA7517": "#FAEEDA",
                     "#D85A30": "#FDF0EC", "#A32D2D": "#FCEBEB"}
            border = result["rating_color"]
            bg = _tint.get(border, "#F5F5F5")
            reason_lines = gen_reason(result)
            for line in reason_lines:
                st.markdown(
                    f'<div style="background:{bg};border-left:4px solid {border};'
                    f'padding:10px 16px;border-radius:6px;margin-bottom:8px;'
                    f'font-size:14px;line-height:1.7">{_md_bold(line)}</div>',
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
            _rf_disp = result.get("rf_annual", 0.04) * 100
            why(f"夏普比率 = (日均收益 − 无风险日收益) ÷ 日收益标准差 × √252，"
                f"衡量**每承担一单位风险能换来多少超过无风险利率的回报**。"
                f"这里的无风险利率取 10 年期美债 **{_rf_disp:.2f}%**——"
                f"不扣掉它就等于把「买国债也能拿到」的那部分收益也算成了你的本事，"
                f"波动越低的资产被抬高得越多。"
                + (f"{result['sharpe']:.2f} 属于优秀（>1.5），收益是靠稳定上涨而非大起大落赚来的。" if result['sharpe'] > 1.5
                   else f"{result['sharpe']:.2f} 属于良好（0.5–1.5），风险与收益基本匹配。" if result['sharpe'] > 0.5
                   else f"{result['sharpe']:.2f} 偏低甚至为负，说明这段时间承担的波动没换来超过国债的回报，不如直接持有现金/短债。"),
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
                    f'font-size:14px;line-height:1.7">{_md_bold(line)}</div>',
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
                col.markdown(_nolatex(f"**{icon} {title}**  \n{desc}"))

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
            st.caption("评级由**趋势强度**与**位置**两个分数的组合决定，而不是把它们相加——"
                       "相加会让「强势上涨」和「暴跌超卖」得到几乎一样的分数。")
            rating_guide = {
                "🚀 强力买入": "趋势≥65 且 位置≤35　—　方向向上、位置还不贵，技术面最理想的组合",
                "📈 买入": "趋势≥65 且 位置中性　—　顺势参与的条件成立",
                "⏳ 顺势但偏贵": "趋势≥65 但 位置≥70　—　方向对，但追高性价比差，等回调",
                "🔍 超卖反弹候选": "趋势45–65 且 位置≤30　—　博反弹而非趋势跟随，小仓位试错",
                "⚖️ 持有": "趋势45–65 且 位置中性　—　缺乏明确信号，观望为主",
                "⚠️ 回调风险": "趋势45–65 但 位置≥70　—　趋势撑不住高位，最容易被套",
                "🩹 止跌观察": "趋势<45 且 位置≤30　—　跌多了但没转向，「跌不动」≠「要涨了」",
                "📉 卖出": "趋势<45 且 位置中性　—　方向向下且没有安全边际",
                "💥 强力卖出": "趋势<45 但 位置≥70　—　又弱又贵，风险收益比最差",
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
                _tts = r.get("trend_score", r.get("score", 50))          # 用趋势分判方向，新评级名才不会漏判
                if combined_score > 15 and _tts >= 65:
                    final = ("🚀 强力建议", "#0F6E56",
                             f"技术面{tech_rating} + 宏观环境正面 + {s_label}受益，三重共振。建议积极布局，可适当提高仓位。")
                elif combined_score > 0 and _tts >= 45:
                    final = ("📈 建议买入", "#1D9E75",
                             f"技术面{tech_rating}，宏观中性偏正，{s_label}无明显逆风。建议正常仓位参与。")
                elif combined_score < -15 and _tts < 45:
                    final = ("💥 强烈规避", "#A32D2D",
                             f"技术面{tech_rating} + 宏观环境负面 + {s_label}面临逆风。建议清仓或空仓等待。")
                elif combined_score < 0 and _tts < 65:
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

            st.warning(tr("disc_tab_note"))

# ── Tab 7: 我的持仓 ──────────────────────────────────────────────────────────────
with tabs[6]:
    st.subheader(tr("sec_holdings"))
    st.caption(tr("holdings_caption"))

    if "holdings" not in st.session_state:
        # 分享链接里带持仓就优先用它，否则给一组示例
        _from_link = []
        try:
            _from_link = pf_decode(st.query_params.get("p", ""))
        except Exception:
            _from_link = []
        if _from_link:
            st.session_state["holdings"] = _from_link
            st.session_state["pf_link_restored"] = len(_from_link)
        else:
            st.session_state["holdings"] = [
                {"ticker": "NVDA",    "qty": 10.0,  "cost": 120.0,   "ccy": "USD 🇺🇸"},
                {"ticker": "BTC-USD", "qty": 0.05,  "cost": 60000.0, "ccy": "USD 🇺🇸"},
            ]

    if st.session_state.pop("pf_link_restored", None):
        st.success(tr("pf_from_url", n=len(st.session_state["holdings"])))
    # 兼容旧版没有货币字段的持仓数据
    for _pos in st.session_state["holdings"]:
        _pos.setdefault("ccy", "USD 🇺🇸")

    st.markdown(tr("add_edit_holdings"))
    hh = st.columns([1.8, 1.3, 1.5, 1.4, 0.8])
    hh[0].markdown(f"**{tr('col_code')}**")
    hh[1].markdown(f"**{tr('col_qty')}**")
    hh[2].markdown(f"**{tr('col_cost')}**")
    hh[3].markdown(f"**{tr('col_ccy')}**")
    hh[4].markdown(f"**{tr('col_delete')}**")

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
    st.caption(tr("ccy_hint"))

    # ── 💾 持仓存档：导出 / 导入 / 分享链接 ──
    with st.expander(tr("pf_io_title"), expanded=False):
        st.caption(tr("pf_io_hint"))
        _io1, _io2, _io3 = st.columns(3)

        with _io1:
            from datetime import datetime as _dt_pf
            st.download_button(
                tr("pf_export"),
                data=pf_to_json_bytes(holdings),
                file_name=f"portfolio_{_dt_pf.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True, key="pf_dl")
            st.caption(tr("pf_export_h"))

        with _io2:
            _up = st.file_uploader(tr("pf_import"), type=["json"],
                                   key="pf_up", label_visibility="visible")
            if _up is not None and st.session_state.get("pf_up_done") != _up.name:
                try:
                    _loaded = pf_from_json_bytes(_up.getvalue())
                    st.session_state["holdings"]  = _loaded
                    st.session_state["pf_up_done"] = _up.name
                    # 清掉旧的逐行控件状态，否则 Streamlit 会沿用上一批持仓的输入值
                    for _k in [k for k in st.session_state
                               if k.startswith(("h_t_", "h_q_", "h_c_", "h_ccy_"))]:
                        del st.session_state[_k]
                    st.success(tr("pf_import_ok", n=len(_loaded)))
                    st.rerun()
                except Exception as _e:
                    st.error(tr("pf_import_err", err=_e))

        with _io3:
            if st.button(tr("pf_link"), use_container_width=True, key="pf_mklink"):
                try:
                    st.query_params["p"] = pf_encode(holdings)
                    st.session_state["pf_link_made"] = True
                except Exception as _e:
                    st.error(str(_e))
            st.caption(tr("pf_link_h"))
            if st.session_state.get("pf_link_made"):
                st.success(tr("pf_link_done"))
                if st.button(tr("pf_link_clear"), key="pf_rmlink"):
                    try:
                        del st.query_params["p"]
                    except Exception:
                        pass
                    st.session_state["pf_link_made"] = False
                    st.rerun()

    st.divider()

    valid_holdings = [h for h in holdings if h["ticker"] and h["qty"] > 0 and h["cost"] > 0]

    if not valid_holdings:
        st.info(tr("holdings_empty"))
    else:
        with st.spinner(tr("holdings_fetching")):
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

        _ok_tks = {h["ticker"] for h in valid_holdings
                   if pos_results.get(h["ticker"]) and "error" not in pos_results.get(h["ticker"], {})}
        report_invalid_tickers([h["ticker"] for h in valid_holdings], _ok_tks, where=tr("where_holdings"))

        if not rows:
            st.error(tr("holdings_none_ok"))
        else:
            total_cost    = sum(x["cost_v"] for x in rows)
            total_mv      = sum(x["mv"] for x in rows)
            total_pnl     = total_mv - total_cost
            total_pnl_pct = (total_mv / total_cost - 1) * 100 if total_cost > 0 else 0

            # 按代码汇总市值，留给「投资圣杯」页按真实权重计算风险
            # （同一个代码可能被分多笔录入，这里合并）
            _mv_by_tk = {}
            for x in rows:
                _mv_by_tk[x["h"]["ticker"]] = _mv_by_tk.get(x["h"]["ticker"], 0.0) + x["mv"]
            st.session_state["holdings_mv"] = _mv_by_tk

            st.markdown(tr("sec_holdings_overview"))
            oc1, oc2, oc3, oc4 = st.columns(4)
            oc1.metric(tr("m_total_cost"), f"${total_cost:,.2f}")
            oc2.metric(tr("m_market_value"), f"${total_mv:,.2f}")
            oc3.metric(tr("m_total_pnl"), f"${total_pnl:+,.2f}", f"{total_pnl_pct:+.1f}%",
                       delta_color="normal" if total_pnl >= 0 else "inverse")
            win_n = sum(1 for x in rows if x["pnl"] >= 0)
            oc4.metric(tr("m_win_ratio"), f"{win_n}/{len(rows)}")

            _best = max(rows, key=lambda x: x["pnl"])
            _worst = min(rows, key=lambda x: x["pnl"])
            why(nt("w_total_cost"), "neutral", title=tr("m_total_cost"), target=oc1)
            why(nt("w_mkt_value"), "neutral", title=tr("m_market_value"), target=oc2)
            why(nt("w_total_pnl", mv=total_mv, cost=total_cost,
                      best=_best["h"]["ticker"], bestv=_best["pnl"],
                      worst=_worst["h"]["ticker"], worstv=_worst["pnl"]),
                "good" if total_pnl >= 0 else "bad", calc=f"${total_mv:,.2f} − ${total_cost:,.2f} = ${total_pnl:+,.2f}"
                f"　→　{total_pnl_pct:+.1f}%", title="总盈亏", target=oc3)
            why(nt("w_win_ratio", n=len(rows), win=win_n),
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
            st.markdown(tr("sec_holdings_lt"))
            weighted_lt = sum(x["r"]["lt_score"] * max(x["mv"], 0.01) for x in rows) / total_mv if total_mv > 0 else 0
            n_bull = sum(1 for x in rows if x["r"]["lt_score"] >= 60)
            n_bear = sum(1 for x in rows if x["r"]["lt_score"] < 45)
            verdict_color = "#0F6E56" if weighted_lt >= 60 else "#BA7517" if weighted_lt >= 45 else "#A32D2D"
            verdict_text = (nt("lt_verdict_hi") if weighted_lt >= 60 else
                            nt("lt_verdict_mid") if weighted_lt >= 45 else nt("lt_verdict_lo"))
            st.markdown(
                f'<div style="background:{verdict_color};color:white;padding:14px 18px;border-radius:10px;font-size:14px">'
                + tr("lt_weighted", score=weighted_lt, bull=n_bull, bear=n_bear) + '<br>'
                f'<span style="font-size:13px;opacity:0.9">{verdict_text}</span></div>',
                unsafe_allow_html=True
            )

            st.divider()
            st.markdown(tr("sec_holdings_each"))
            st.caption(tr("holdings_each_cap"))

            def analyze_position_pnl(h, r, pnl_pct, cost_usd, ccy_code):
                """分析单个持仓的盈亏原因"""
                lines = []
                cur = r["price_now"]
                direction = nt("dir_profit") if pnl_pct >= 0 else nt("dir_loss")
                if ccy_code != "USD":
                    ccy_sym = CURRENCY_SYMBOLS.get(ccy_code, "$")
                    _cd = f"{ccy_sym}{h['cost']:.2f} {ccy_code} (\u2248${cost_usd:.2f})"
                else:
                    _cd = f"${cost_usd:.2f}"
                lines.append(nt("pnl_head", cost_disp=_cd, cur=cur,
                                direction=direction, pct=abs(pnl_pct)))

                if r["mom_1m"] > 5:
                    lines.append(nt("pnl_mom_up", m=r["mom_1m"]))
                elif r["mom_1m"] < -5:
                    lines.append(nt("pnl_mom_dn", m=r["mom_1m"]))
                else:
                    lines.append(nt("pnl_mom_flat", m=r["mom_1m"]))

                if r["rsi"] > 70:
                    lines.append(nt("pnl_rsi_hi", v=r["rsi"]))
                elif r["rsi"] < 30:
                    lines.append(nt("pnl_rsi_lo", v=r["rsi"]))

                if r["macd_hist"] > 0:
                    lines.append(nt("pnl_macd_pos"))
                else:
                    lines.append(nt("pnl_macd_neg"))

                if r["obv_trend"] == "上升":
                    lines.append(nt("pnl_obv_in", v=r["obv_pct"]))
                else:
                    lines.append(nt("pnl_obv_out", v=abs(r["obv_pct"])))

                macro_sc  = st.session_state.get("macro_score")
                macro_out = st.session_state.get("macro_outlook")
                if macro_sc is not None:
                    beta = r.get("beta") or 1.0
                    if pnl_pct < 0 and macro_sc < 0:
                        lines.append(nt("pnl_macro_bad", sc=macro_sc, out=macro_out, beta=beta))
                    elif pnl_pct >= 0 and macro_sc > 0:
                        lines.append(nt("pnl_macro_good", sc=macro_sc, out=macro_out, beta=beta))
                    else:
                        lines.append(nt("pnl_macro_mixed", sc=macro_sc, out=macro_out))
                else:
                    lines.append(nt("pnl_macro_none"))

                return lines

            for x in rows:
                h, r = x["h"], x["r"]
                icon = "🟢" if x["pnl"] >= 0 else "🔴"
                with st.expander(tr("pos_expander", icon=icon, tk=h["ticker"],
                                     name=r.get("name", h["ticker"]), pct=x["pnl_pct"]),
                                 expanded=False):
                    ccy_sym = CURRENCY_SYMBOLS.get(x["ccy_code"], "$")
                    cost_disp = (f"{ccy_sym}{h['cost']:.2f} {x['ccy_code']}"
                                if x["ccy_code"] != "USD" else f"${h['cost']:.2f}")

                    pc1, pc2, pc3, pc4 = st.columns(4)
                    pc1.metric(tr("pos_qty"), f"{h['qty']:g}")
                    pc2.metric(tr("pos_cost_price"), f"{cost_disp} / ${r['price_now']:.2f}")
                    pc3.metric(tr("pos_pnl_amt"), f"${x['pnl']:+,.2f}")
                    pc4.metric(tr("pos_pnl_pct"), f"{x['pnl_pct']:+.1f}%",
                               delta_color="normal" if x["pnl_pct"] >= 0 else "inverse")

                    st.markdown(tr("pos_attr"))
                    for line in analyze_position_pnl(h, r, x["pnl_pct"], x["cost_usd"], x["ccy_code"]):
                        st.markdown(f"- {_nolatex(line)}")

                    st.markdown(tr("pos_lt"))
                    st.markdown(
                        f'<div style="background:#F8F9FA;border-left:4px solid {r["lt_color"]};'
                        f'padding:10px 14px;border-radius:6px;font-size:13px;margin-bottom:10px">'
                        f'<b style="color:{r["lt_color"]}">{r["lt_rating"]}</b>'
                        + tr("lt_score_line", score=r["lt_score"], sharpe=r["sharpe"],
                             slope=r["slope_pct"],
                             ma=tr("above") if r["price_now"] > r["ma200"] else tr("below"))
                        + '</div>', unsafe_allow_html=True
                    )

                    st.markdown(tr("pos_track"))
                    track_name, track_color, track_desc = get_track_info(h["ticker"], r.get("sector"))
                    st.markdown(
                        f'<div style="background:#F8F9FA;border-left:4px solid {track_color};'
                        f'padding:10px 14px;border-radius:6px;font-size:13px">'
                        f'<b style="color:{track_color}">{track_name}</b><br>{track_desc}'
                        f'</div>', unsafe_allow_html=True
                    )

            # ── 📄 导出分析报告 ──
            st.divider()
            st.markdown(tr("rep_title"))
            st.caption(tr("rep_hint"))

            def _build_holdings_report():
                """把本页所有结论拼成一份 Markdown 报告"""
                L = [_report_header(_md_heading("sec_holdings").lstrip("💰 ").strip())]

                L.append("## " + _md_heading("sec_holdings_overview") + "\n\n")
                L.append(f"| | |\n|---|---:|\n")
                L.append(f"| {_md_clean(tr('m_total_cost'))} | ${total_cost:,.2f} |\n")
                L.append(f"| {_md_clean(tr('m_market_value'))} | ${total_mv:,.2f} |\n")
                L.append(f"| {_md_clean(tr('m_total_pnl'))} | ${total_pnl:+,.2f} ({total_pnl_pct:+.1f}%) |\n")
                L.append(f"| {_md_clean(tr('m_win_ratio'))} | {win_n}/{len(rows)} |\n\n")

                L.append("## " + _md_heading("sec_holdings_lt") + "\n\n")
                L.append(_md_clean(tr("lt_weighted", score=weighted_lt, bull=n_bull, bear=n_bear)) + "\n\n")
                L.append(_md_clean(verdict_text) + "\n\n")

                L.append("## " + _md_heading("sec_holdings_each") + "\n\n")
                for x in rows:
                    h, r = x["h"], x["r"]
                    _sym = CURRENCY_SYMBOLS.get(x["ccy_code"], "$")
                    _cd = (f"{_sym}{h['cost']:.2f} {x['ccy_code']} (≈${x['cost_usd']:.2f})"
                           if x["ccy_code"] != "USD" else f"${h['cost']:.2f}")
                    L.append(f"### {h['ticker']} — {r.get('name', h['ticker'])}\n\n")
                    L.append(f"- {_md_clean(tr('pos_qty'))}: {h['qty']:g}\n")
                    L.append(f"- {_md_clean(tr('pos_cost_price'))}: {_cd} / ${r['price_now']:.2f}\n")
                    L.append(f"- {_md_clean(tr('pos_pnl_amt'))}: ${x['pnl']:+,.2f} "
                             f"({x['pnl_pct']:+.1f}%)\n\n")
                    L.append("**" + _md_heading("pos_attr") + "**\n\n")
                    for line in analyze_position_pnl(h, r, x["pnl_pct"], x["cost_usd"], x["ccy_code"]):
                        L.append(f"- {_md_clean(line)}\n")
                    L.append("\n**" + _md_heading("pos_lt") + "**\n\n")
                    L.append(f"{r['lt_rating']} — " + _md_clean(
                        tr("lt_score_line", score=r["lt_score"], sharpe=r["sharpe"],
                           slope=r["slope_pct"],
                           ma=tr("above") if r["price_now"] > r["ma200"] else tr("below"))) + "\n\n")
                    _tn, _tc, _td = get_track_info(h["ticker"], r.get("sector"))
                    L.append("**" + _md_heading("pos_track") + "**\n\n")
                    L.append(f"{_tn} — {_md_clean(_td)}\n\n---\n\n")

                L.append("*" + _md_clean(tr("disc_tab_note")) + "*\n")
                return "".join(L).encode("utf-8")

            def _build_holdings_csv():
                hdr = ["Ticker", "Name", "Qty", "Cost", "Currency", "Cost(USD)",
                       "Price(USD)", "MarketValue(USD)", "CostValue(USD)",
                       "PnL(USD)", "PnL(%)", "LongTermScore", "LongTermRating",
                       "RSI", "Momentum1M(%)", "Sharpe", "Track"]
                out = []
                for x in rows:
                    h, r = x["h"], x["r"]
                    _tn, _, _ = get_track_info(h["ticker"], r.get("sector"))
                    out.append([h["ticker"], r.get("name", ""), f"{h['qty']:g}",
                                f"{h['cost']:.4f}", x["ccy_code"], f"{x['cost_usd']:.4f}",
                                f"{r['price_now']:.4f}", f"{x['mv']:.2f}", f"{x['cost_v']:.2f}",
                                f"{x['pnl']:.2f}", f"{x['pnl_pct']:.2f}",
                                f"{r['lt_score']:.1f}", _md_clean(r["lt_rating"]),
                                f"{r['rsi']:.1f}", f"{r['mom_1m']:.2f}",
                                f"{r['sharpe']:.2f}", _md_clean(_tn)])
                out.append([])
                out.append(["TOTAL", "", "", "", "", "", "", f"{total_mv:.2f}",
                            f"{total_cost:.2f}", f"{total_pnl:.2f}", f"{total_pnl_pct:.2f}",
                            f"{weighted_lt:.1f}", "", "", "", "", ""])
                return _csv_bytes(hdr, out)

            from datetime import datetime as _dt_rep
            _stamp = _dt_rep.now().strftime("%Y%m%d_%H%M")
            _rc1, _rc2 = st.columns(2)
            _rc1.download_button(tr("rep_dl_md"), data=_build_holdings_report(),
                                 file_name=f"portfolio_report_{_stamp}.md",
                                 mime="text/markdown", use_container_width=True,
                                 key="rep_h_md")
            _rc2.download_button(tr("rep_dl_csv"), data=_build_holdings_csv(),
                                 file_name=f"portfolio_positions_{_stamp}.csv",
                                 mime="text/csv", use_container_width=True,
                                 key="rep_h_csv")

            st.warning(tr("disc_tab_note"))


_WM_OPTS = ["eq", "mv"]


def _set_wmode(mode):
    """程序性地切换权重口径。

    带 key 的控件，其 session_state 值优先于 index 参数，所以光改
    hg_wmode 是推不动控件的 —— 必须把控件自己的 key 删掉，
    让它下次渲染时重新按 hg_wmode 播种。
    """
    st.session_state["hg_wmode"] = mode
    for _k in [k for k in st.session_state if k.startswith("hg_wmode_pick_")]:
        del st.session_state[_k]


# ── Tab 8: 投资圣杯（达里欧分散化法则） ────────────────────────────────────────────
with tabs[7]:
    st.subheader(tr("sec_grail"))
    st.caption(nt("hg_caption"))

    why(nt("hg_intro"), "neutral", calc=nt("hg_intro_calc"), title=tr("hg_intro_title"))

    # ── 1. 圣杯理论曲线 ──
    _hg_n = np.arange(1, 21)
    fig_hg = go.Figure()
    for _rho, _clr in [(0.0, "#0F6E56"), (0.2, "#1D9E75"), (0.4, "#BA7517"), (0.6, "#A32D2D")]:
        _risk = np.sqrt(1 / _hg_n + (_hg_n - 1) / _hg_n * _rho) * 100
        fig_hg.add_trace(go.Scatter(
            x=_hg_n, y=_risk, mode="lines", name=tr("hg_legend", r=_rho),
            line=dict(color=_clr, width=2.6),
            hovertemplate=f"ρ={_rho:.1f}<br>%{{x}} " + tr("hg_hover") + " %{y:.0f}%<extra></extra>",
        ))
    fig_hg.add_vline(x=5, line_dash="dot", line_color="#888", line_width=1.2,
                     annotation_text=tr("hg_ann_5"), annotation_font=dict(size=11))
    fig_hg.add_vline(x=15, line_dash="dot", line_color="#534AB7", line_width=1.2,
                     annotation_text=tr("hg_ann_15"), annotation_font=dict(size=11, color="#534AB7"))
    fig_hg.update_layout(
        height=380, title=dict(text=tr("hg_curve_title"), font=dict(size=14)),
        xaxis=dict(title=tr("hg_ax_n"), dtick=1, showgrid=True, gridcolor="#eeeeee"),
        yaxis=dict(title=tr("hg_ax_risk"), showgrid=True, gridcolor="#eeeeee"),
        legend=dict(orientation="h", y=1.1, x=0), margin=dict(t=70, b=50, l=60, r=30),
        hovermode="x unified",
    )
    glass_chart(fig_hg)
    why(nt("hg_curve_read"), "good", title=tr("hg_curve_read_t"))

    st.divider()

    # ── 2. 选择要分析的资产 ──
    st.markdown(tr("hg_your_pf"))
    _hold_tks = [h["ticker"] for h in st.session_state.get("holdings", []) if h.get("ticker")]
    if "hg_tickers" not in st.session_state:
        st.session_state["hg_tickers"] = (_hold_tks if len(_hold_tks) >= 2
                                          else ["SPY", "TLT", "GLD", "DBC", "VNQ", "BTC-USD"])

    _hg_presets = {
        tr("hg_preset_aw"): ["VTI", "TLT", "IEF", "GLD", "DBC"],
        tr("hg_preset_sbg"): ["SPY", "TLT", "GLD"],
        tr("hg_preset_div"): ["SPY", "EFA", "VWO", "TLT", "GLD", "DBC", "VNQ", "BTC-USD"],
        tr("hg_preset_ai"): ["NVDA", "AMD", "SMCI", "MSFT", "GOOGL", "META"],
    }
    _pc = st.columns(len(_hg_presets) + 1)
    for _i, (_pn, _pt) in enumerate(_hg_presets.items()):
        if _pc[_i].button(_pn, key=f"hg_preset_{_i}", use_container_width=True):
            st.session_state["hg_tickers"] = _pt
            st.rerun()
    if _pc[-1].button(tr("hg_use_holdings"), key="hg_use_holdings", use_container_width=True,
                      disabled=len(_hold_tks) < 2):
        st.session_state["hg_tickers"] = list(dict.fromkeys(_hold_tks))
        # 带上真实市值权重：只传代码而按等权计算，会严重低估集中持仓的风险
        if st.session_state.get("holdings_mv"):
            _set_wmode("mv")
        st.rerun()

    # 预设组合本身就是等权思路，切过去时回到等权，避免沿用上一份持仓的权重
    for _i in range(len(_hg_presets)):
        if st.session_state.get(f"hg_preset_{_i}"):
            _set_wmode("eq")

    _hg_mv = st.session_state.get("holdings_mv") or {}
    if not _hg_mv:
        _set_wmode("eq")                          # 没有持仓数据就只能等权

    _hg_c1, _hg_c2, _hg_c3 = st.columns([3, 1, 1])
    with _hg_c1:
        _hg_opts = list(dict.fromkeys(list(st.session_state["hg_tickers"]) + list(TICKER_UNIVERSE.keys())))
        try:
            _hg_tickers = st.multiselect(
                tr("hg_pick_assets"),
                _hg_opts, default=st.session_state["hg_tickers"], key="hg_pick",
                format_func=_uni_label, accept_new_options=True,
                help=tr("hg_pick_help"))
        except TypeError:
            _hg_tickers = st.multiselect(
                tr("hg_pick_assets"),
                _hg_opts, default=st.session_state["hg_tickers"], key="hg_pick",
                format_func=_uni_label)
        _hg_tickers = [t.strip().upper() for t in _hg_tickers if t and t.strip()]
    _hg_period = _hg_c2.selectbox(tr("hg_lookback"), ["1y", "2y", "3y", "5y"], index=1, key="hg_period")
    _hg_bench = _hg_c3.selectbox(tr("hg_bench"), ["SPY", "QQQ", "VTI"], index=0, key="hg_bench")
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

    # ── 权重方式：等权 vs 按持仓市值 ──
    # 语言放进 key 里，切语言时选项文案才会跟着刷新；
    # 换 key 相当于新控件，所以下面要重新播种一次当前口径。
    _lgw = st.session_state.get("lang", "zh")
    _wkey = f"hg_wmode_pick_{_lgw}"
    if _wkey not in st.session_state:
        _seed = st.session_state.get("hg_wmode", "eq")
        st.session_state[_wkey] = _seed if (_seed in _WM_OPTS and (_seed != "mv" or _hg_mv)) else "eq"
    _wmode = st.radio(
        tr("hg_wmode_label"), _WM_OPTS,
        horizontal=True, key=_wkey,
        format_func=lambda m: (tr("hg_wmode_eq") if m == "eq" else tr("hg_wmode_mv")),
        help=tr("hg_wmode_help"))
    if _wmode == "mv" and not _hg_mv:
        st.info(tr("hg_wmode_nomv"))
        _wmode = "eq"
    st.session_state["hg_wmode"] = _wmode

    if len(_hg_tickers) < 2:
        st.info(tr("hg_need2"))
    else:
        with st.spinner(tr("hg_computing")):
            _rets, _bench_r = fetch_returns_matrix(tuple(_hg_tickers), _hg_period, _hg_bench)

        if _rets is None or _rets.shape[1] < 2:
            st.error(tr("hg_nodata"))
        else:
            report_invalid_tickers(_hg_tickers, set(_rets.columns), where=tr("hg_where"))

            _n = _rets.shape[1]
            _corr = _rets.corr()
            _vols = _rets.std() * np.sqrt(252)
            _mask = ~np.eye(_n, dtype=bool)
            _rho_bar = float(_corr.values[_mask].mean())

            # ── 权重向量 ──
            # 以前这里写死等权。但「用我的持仓」的人往往是重仓一两只，
            # 等权算出来的波动会比真实组合低一大截，甚至把"风险上升"报成"风险下降"。
            _missing_mv = []
            if _wmode == "mv" and _hg_mv:
                _wv = np.array([float(_hg_mv.get(t, 0.0)) for t in _rets.columns], dtype=float)
                _missing_mv = [t for t in _rets.columns if float(_hg_mv.get(t, 0.0)) <= 0]
                if _wv.sum() <= 0:
                    _wv = np.ones(_n, dtype=float)
                    _wmode = "eq"
            else:
                _wv = np.ones(_n, dtype=float)
            _wv = _wv / _wv.sum()
            _is_eq = (_wmode == "eq")

            _pf_ret = (_rets * _wv).sum(axis=1)
            _pf_vol = float(_pf_ret.std() * np.sqrt(252))
            # 对照基准：同样权重下"各资产各走各的、完全不分散"时的加权平均波动
            _avg_vol = float((_vols.values * _wv).sum())
            _div_benefit = (1 - _pf_vol / _avg_vol) * 100 if _avg_vol > 0 else 0
            # 有效分散数 = 分散化比率的平方 = (Σwᵢσᵢ)² / (w'Σw)
            # 等权且各资产波动相同时，它正好退化成教科书里的 n/(1+(n−1)ρ̄)
            _n_eff = (_avg_vol / _pf_vol) ** 2 if _pf_vol > 0 else 0.0
            # 切到等权后实际会看到的有效分散数（同样用 DR²，口径才一致）
            _eqw = np.ones(_n) / _n
            _pf_vol_eq = float((_rets * _eqw).sum(axis=1).std() * np.sqrt(252))
            _avg_vol_eq = float((_vols.values * _eqw).sum())
            _n_eff_eq = (_avg_vol_eq / _pf_vol_eq) ** 2 if _pf_vol_eq > 0 else 0.0
            # 名义等效持仓数（只看权重集中度，不看相关性）
            _conc = 1.0 / float((_wv ** 2).sum())

            if _missing_mv:
                st.warning(tr("hg_mv_missing", tks="、".join(_missing_mv)))
            if not _is_eq:
                st.caption(tr("hg_wmode_active", w="　·　".join(
                    f"{t} {w*100:.0f}%" for t, w in
                    sorted(zip(_rets.columns, _wv), key=lambda kv: -kv[1]))))

            # ── 核心结论卡 ──
            k1, k2, k3, k4 = st.columns(4)
            k1.metric(tr("hg_m_n"), f"{_n}", tr("hg_m_n_ok") if _n >= 5 else tr("hg_m_n_bad"),
                      delta_color="normal" if _n >= 5 else "inverse")
            k2.metric(tr("hg_m_rho"), f"{_rho_bar:.2f}", tr("hg_m_rho_d"), delta_color="off")
            k3.metric(tr("hg_m_eff"), f"{_n_eff:.1f}", tr("hg_m_eff_d", n=_n), delta_color="off")
            k4.metric(tr("hg_m_cut"), f"{_div_benefit:.1f}%",
                      f"{_avg_vol*100:.1f}% → {_pf_vol*100:.1f}%", delta_color="normal")

            why(nt("hg_w_rho", n=_n, rho=_rho_bar,
                      verdict=(nt("hg_rho_lo") if _rho_bar < 0.3 else
                               nt("hg_rho_mid") if _rho_bar < 0.6 else nt("hg_rho_hi"))),
                "good" if _rho_bar < 0.3 else "warn" if _rho_bar < 0.6 else "bad",
                title=tr("hg_t_rho", rho=_rho_bar), target=k2)
            why(nt("hg_w_eff", n=_n, eff=_n_eff)
                + ("" if _is_eq else tr("hg_eff_conc", conc=_conc, eq=_n_eff_eq)),
                "good" if _n_eff >= 5 else "warn" if _n_eff >= 3 else "bad",
                calc=f"({_avg_vol*100:.1f}% ÷ {_pf_vol*100:.1f}%)² = {_n_eff:.1f}"
                     + (f"　·　等权同波动的理论值 {_n} ÷ (1 + {_n-1} × {_rho_bar:.2f}) = "
                        f"{_n / (1 + (_n - 1) * max(_rho_bar, 0.0001)):.1f}" if _is_eq else ""),
                title=tr("hg_t_eff", eff=_n_eff), target=k3)
            why(nt("hg_w_cut", avg=_avg_vol*100, pf=_pf_vol*100, cut=_div_benefit,
                      mode=tr("hg_mode_eq_n") if _is_eq else tr("hg_mode_mv_n")),
                "good" if _div_benefit > 25 else "warn",
                calc=f"1 − {_pf_vol*100:.1f}% ÷ {_avg_vol*100:.1f}% = {_div_benefit:.1f}%",
                title=tr("hg_t_cut", cut=_div_benefit), target=k4)

            st.divider()

            # ── 3. 相关性矩阵 ──
            st.markdown(tr("hg_corr_matrix"))
            fig_corr = go.Figure(go.Heatmap(
                z=_corr.values, x=list(_corr.columns), y=list(_corr.columns),
                colorscale="RdYlGn_r", zmin=-1, zmax=1,
                text=np.round(_corr.values, 2), texttemplate="%{text}",
                textfont=dict(size=11), colorbar=dict(title=tr("hg_corr")),
                hovertemplate="%{y} vs %{x}<br>" + tr("hg_corr") + " %{z:.2f}<extra></extra>",
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
            why(nt("hg_corr_read", lo1=_lowest[0], lo2=_lowest[1], lov=_lowest[2],
                      hi1=_highest[0], hi2=_highest[1], hiv=_highest[2],
                      tail=nt("hg_corr_tail_hi") if _highest[2] > 0.7 else nt("hg_corr_tail_mid")),
                "neutral", title=tr("why_howto_read"))

            st.divider()

            # ── 4. 你的组合在圣杯曲线上的位置 ──
            st.markdown(tr("hg_pos_title"))
            fig_pos = go.Figure()
            for _rho, _clr in [(0.0, "#0F6E56"), (0.2, "#1D9E75"), (0.4, "#BA7517"), (0.6, "#A32D2D")]:
                fig_pos.add_trace(go.Scatter(
                    x=_hg_n, y=np.sqrt(1 / _hg_n + (_hg_n - 1) / _hg_n * _rho) * 100,
                    mode="lines", name=f"ρ={_rho:.1f}", line=dict(color=_clr, width=1.8, dash="dot"),
                    hoverinfo="skip",
                ))
            fig_pos.add_trace(go.Scatter(
                x=[_n], y=[_pf_vol / _avg_vol * 100 if _avg_vol > 0 else 100],
                mode="markers+text", name=tr("hg_your_pf_marker"),
                marker=dict(size=20, color="#534AB7", symbol="star",
                            line=dict(color="white", width=2)),
                text=[tr("hg_you_here", n=_n, rho=_rho_bar)], textposition="middle right",
                textfont=dict(size=12, color="#534AB7"),
            ))
            fig_pos.update_layout(
                height=400, xaxis=dict(title=tr("hg_ax_n2"), dtick=1, showgrid=True, gridcolor="#eeeeee"),
                yaxis=dict(title=tr("hg_ax_risk"), showgrid=True, gridcolor="#eeeeee"),
                legend=dict(orientation="h", y=1.1, x=0), margin=dict(t=60, b=50, l=60, r=140),
            )
            glass_chart(fig_pos)
            _room = _pf_vol / _avg_vol * 100 - np.sqrt(1 / max(_n, 1)) * 100
            why(nt("hg_pos_read", n=_n, rho=_rho_bar, cur=_pf_vol/_avg_vol*100,
                      ideal=np.sqrt(1/max(_n, 1))*100, room=_room),
                "good" if _room < 15 else "warn", title=tr("why_howto_read"))

            st.divider()

            # ── 5. Alpha / Beta 分解 ──
            st.markdown(tr("hg_ab_title", b=_hg_bench))
            why(nt("hg_ab_intro"), "neutral", calc=nt("hg_ab_calc"), title=tr("hg_ab_title2"))

            if _bench_r is None:
                st.warning(tr("hg_ab_nobench", b=_hg_bench))
            else:
                _bvar = float(_bench_r.var())
                # Jensen's Alpha：α = (Rp − rf) − β(Rm − rf)
                # 漏掉 rf 会让偏差变成 rf×(1−β)：β<1 的资产 α 被系统性高估，
                # 而债券、黄金这类低 β 资产正是本页在建议用户配置的那一类。
                _rf_ann = get_risk_free_rate()
                _rf_d = _rf_ann / 252
                _ab_rows = []
                for _tk in _rets.columns:
                    _a = _rets[_tk]
                    _beta = float(np.cov(_a, _bench_r)[0, 1] / _bvar) if _bvar > 0 else 0.0
                    _alpha = float(((_a.mean() - _rf_d)
                                    - _beta * (_bench_r.mean() - _rf_d)) * 252 * 100)
                    _r2 = float(np.corrcoef(_a, _bench_r)[0, 1] ** 2)
                    _ab_rows.append((_tk, _beta, _alpha, _r2))
                st.caption(tr("hg_rf_note", rf=_rf_ann * 100))

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
                        f'<div class="ac-note">{tr("hg_ab_note")}</div></div>'
                        '</div></div>'
                    )
                render_asset_grid(_ab_cards, min_width=215)

                with st.expander(tr("hg_ab_expander"), expanded=False):
                    for _tk, _beta, _alpha, _r2 in sorted(_ab_rows, key=lambda x: -x[3]):
                        _beta_txt = (nt("hg_beta_indep") if abs(_beta) < 0.3 else
                                     nt("hg_beta_neg") if _beta < 0 else
                                     nt("hg_beta_hi", b=_beta) if _beta > 1.2 else
                                     nt("hg_beta_lo", b=_beta))
                        _r2_txt = (nt("hg_r2_hi", r=_r2*100) if _r2 > 0.5
                                   else nt("hg_r2_lo", r=_r2*100, rest=(1-_r2)*100))
                        _a_txt = (nt("hg_alpha_pos", a=_alpha) if _alpha > 0
                                  else nt("hg_alpha_neg", a=_alpha))
                        why(nt("hg_ab_line", b=_beta, btxt=_beta_txt, r2txt=_r2_txt, atxt=_a_txt),
                            "good" if (_alpha > 0 and _r2 < 0.5) else "warn" if _alpha > 0 else "bad",
                            title=_tk)

                # β 和 α 都是线性的，按组合权重加权即可（_ab_rows 与 _rets.columns 同序）
                _pf_beta = float(sum(b * w for (_, b, _, _), w in zip(_ab_rows, _wv)))
                _pf_alpha = float(sum(a * w for (_, _, a, _), w in zip(_ab_rows, _wv)))
                _tail = (nt("hg_pf_b_mid") if 0.8 <= _pf_beta <= 1.2 else
                         nt("hg_pf_b_lo", b=_pf_beta) if _pf_beta < 0.8 else
                         nt("hg_pf_b_hi", b=_pf_beta))
                why(nt("hg_pf_ab", beta=_pf_beta, alpha=_pf_alpha, tail=_tail,
                          mode=tr("hg_mode_eq_n") if _is_eq else tr("hg_mode_mv_n")),
                    "good" if _pf_beta < 0.8 else "warn", title=tr("hg_pf_ab_t"))

            st.divider()

            # ── 6. 圣杯评分与改进建议 ──
            st.markdown(tr("hg_score_title"))
            _sc_n   = 40 if _n >= 15 else 32 if _n >= 10 else 24 if _n >= 5 else 12 if _n >= 3 else 5
            _sc_rho = 40 if _rho_bar < 0.1 else 32 if _rho_bar < 0.3 else 20 if _rho_bar < 0.5 else 8 if _rho_bar < 0.7 else 2
            _sc_eff = 20 if _n_eff >= 8 else 14 if _n_eff >= 5 else 8 if _n_eff >= 3 else 3
            _hg_score = _sc_n + _sc_rho + _sc_eff
            _hg_color = ("#0F6E56" if _hg_score >= 75 else "#1D9E75" if _hg_score >= 60
                         else "#BA7517" if _hg_score >= 40 else "#A32D2D")
            _hg_verdict = (nt("hg_v_hi") if _hg_score >= 75 else
                           nt("hg_v_mid") if _hg_score >= 60 else
                           nt("hg_v_lo") if _hg_score >= 40 else nt("hg_v_none"))
            st.markdown(
                f'<div style="background:{_hg_color};color:white;padding:16px 20px;border-radius:12px;font-size:14px">'
                f'<span style="font-size:24px;font-weight:750">{_hg_score}/100</span>'
                f'　<span style="font-size:15px;font-weight:600">{_hg_verdict}</span><br>'
                f'<span style="font-size:12.5px;opacity:.92">'
                + tr("hg_score_break", n=_sc_n, r=_sc_rho, e=_sc_eff) + '</span></div>',
                unsafe_allow_html=True)
            why(nt("hg_score_why", n=_n, sn=_sc_n, rho=_rho_bar, sr=_sc_rho, eff=_n_eff, se=_sc_eff,
                      gate=nt("hg_gate_ok") if _n >= 5 else nt("hg_gate_no")),
                "good" if _hg_score >= 60 else "warn" if _hg_score >= 40 else "bad",
                calc=f"{_sc_n} + {_sc_rho} + {_sc_eff} = {_hg_score}/100", title=tr("why_score_src"))

            # 资产类别诊断
            def _classify(tk):
                t = tk.upper()
                if t.endswith("-USD"):
                    return tr("cls_crypto")
                if t in ("TLT","IEF","SHY","BND","AGG","TIP","LQD","HYG","ZROZ","EDV","GOVT"):
                    return tr("cls_bond")
                if t in ("GLD","IAU","SLV","GC=F","SI=F","PPLT","GDX","NEM"):
                    return tr("cls_pm")
                if t in ("DBC","DJP","USO","UNG","CL=F","HG=F","CORN","WEAT","PDBC","FCX"):
                    return tr("cls_comm")
                if t in ("VNQ","IYR","SCHH","O","XLRE"):
                    return tr("cls_re")
                if t in ("EFA","VEA","VWO","EEM","FXI","MCHI","IEFA","IEMG","EWJ","BABA","JD","PDD","BIDU","NIO"):
                    return tr("cls_intl")
                if t in ("UUP","FXE","FXY","USDU"):
                    return tr("cls_fx")
                return tr("cls_us")
            _classes = {}
            for _tk in _rets.columns:
                _classes.setdefault(_classify(_tk), []).append(_tk)
            _missing_cls = {
                tr("cls_bond"):   (tr("hg_sugg_bond"),   nt("hg_sugg_bond_r")),
                tr("cls_pm"):     (tr("hg_sugg_gold"),   nt("hg_sugg_gold_r")),
                tr("cls_comm"):   (tr("hg_sugg_comm"),   nt("hg_sugg_comm_r")),
                tr("cls_intl"):   (tr("hg_sugg_intl"),   nt("hg_sugg_intl_r")),
                tr("cls_re"):     (tr("hg_sugg_re"),     nt("hg_sugg_re_r")),
                tr("cls_crypto"): (tr("hg_sugg_crypto"), nt("hg_sugg_crypto_r")),
            }
            _have = set(_classes.keys())
            _sugg = [(v[0], v[1]) for k, v in _missing_cls.items() if k not in _have]
            st.markdown(tr("hg_cls_title"))
            st.markdown(
                " ".join(f'<span style="display:inline-block;background:rgba(83,74,183,.12);color:#534AB7;'
                         f'border-radius:99px;padding:3px 12px;font-size:12px;font-weight:600;margin:2px">'
                         f'{k}：{", ".join(v)}</span>' for k, v in _classes.items()),
                unsafe_allow_html=True)
            if _sugg:
                why(nt("hg_missing")
                    + "；".join(f"**{name}** — {rsn}" for name, rsn in _sugg[:4]) + "。",
                    "warn", title=tr("hg_missing_t"))
            else:
                why(nt("hg_covered"), "good", title=tr("hg_covered_t"))

            # ── 📄 导出分散化报告 ──
            st.divider()
            st.markdown(tr("rep_title"))

            def _build_grail_report():
                L = [_report_header(_md_heading("sec_grail").lstrip("🏆 ").strip())]
                L.append(f"**{_md_clean(tr('hg_lookback'))}**: {_hg_period}　·　"
                         f"**{_md_clean(tr('hg_m_n'))}**: {_n}　·　"
                         f"**{_md_clean(tr('hg_wmode_label'))}**: "
                         f"{_md_clean(tr('hg_wmode_eq') if _is_eq else tr('hg_wmode_mv'))}\n\n")
                if not _is_eq:
                    L.append("| | |\n|---|---:|\n")
                    for _t_, _w_ in sorted(zip(_rets.columns, _wv), key=lambda kv: -kv[1]):
                        L.append(f"| {_t_} | {_w_*100:.1f}% |\n")
                    L.append("\n")
                L.append(f"| | |\n|---|---:|\n")
                L.append(f"| {_md_clean(tr('hg_m_n'))} | {_n} |\n")
                L.append(f"| {_md_clean(tr('hg_m_rho'))} | {_rho_bar:.3f} |\n")
                L.append(f"| {_md_clean(tr('hg_m_eff'))} | {_n_eff:.2f} |\n")
                L.append(f"| {_md_clean(tr('hg_m_cut'))} | {_div_benefit:.1f}% "
                         f"({_avg_vol*100:.1f}% → {_pf_vol*100:.1f}%) |\n\n")

                L.append("## " + _md_heading("hg_score_title") + "\n\n")
                L.append(f"**{_hg_score}/100** — {_md_clean(_hg_verdict)}\n\n")
                L.append(_md_clean(tr("hg_score_break", n=_sc_n, r=_sc_rho, e=_sc_eff)) + "\n\n")

                L.append("## " + _md_heading("hg_cls_title") + "\n\n")
                for k, v in _classes.items():
                    L.append(f"- **{k}**: {', '.join(v)}\n")
                L.append("\n")
                if _sugg:
                    L.append(_md_clean(nt("hg_missing")) + "\n\n")
                    for _nm, _rs in _sugg[:4]:
                        L.append(f"- **{_nm}** — {_md_clean(_rs)}\n")
                else:
                    L.append(_md_clean(nt("hg_covered")) + "\n")
                L.append("\n## " + _md_clean(tr("hg_m_rho")) + "\n\n")
                _cols = list(_corr.columns)
                L.append("| |" + "|".join(_cols) + "|\n")
                L.append("|---|" + "|".join(["---:"] * len(_cols)) + "|\n")
                for _rn in _cols:
                    L.append(f"|**{_rn}**|" +
                             "|".join(f"{_corr.loc[_rn, _cn]:.2f}" for _cn in _cols) + "|\n")
                L.append("\n*" + _md_clean(nt("hg_warn")) + "*\n")
                return "".join(L).encode("utf-8")

            def _build_corr_csv():
                _cols = list(_corr.columns)
                out = [[_rn] + [f"{_corr.loc[_rn, _cn]:.6f}" for _cn in _cols] for _rn in _cols]
                out.append([])
                out.append(["AvgCorrelation", f"{_rho_bar:.6f}"])
                out.append(["EffectiveBets", f"{_n_eff:.4f}"])
                out.append(["RiskReduction(%)", f"{_div_benefit:.4f}"])
                out.append(["AvgAssetVol(%)", f"{_avg_vol*100:.4f}"])
                out.append(["PortfolioVol(%)", f"{_pf_vol*100:.4f}"])
                out.append(["HolyGrailScore", f"{_hg_score}"])
                out.append(["Weighting", "equal" if _is_eq else "market-value"])
                for _t_, _w_ in zip(_rets.columns, _wv):
                    out.append(["Weight_" + str(_t_), f"{_w_:.6f}"])
                return _csv_bytes([""] + _cols, out)

            from datetime import datetime as _dt_hg
            _hstamp = _dt_hg.now().strftime("%Y%m%d_%H%M")
            _gc1, _gc2 = st.columns(2)
            _gc1.download_button(tr("hg_dl_md"), data=_build_grail_report(),
                                 file_name=f"diversification_report_{_hstamp}.md",
                                 mime="text/markdown", use_container_width=True,
                                 key="rep_g_md")
            _gc2.download_button(tr("hg_dl_csv"), data=_build_corr_csv(),
                                 file_name=f"correlation_matrix_{_hstamp}.csv",
                                 mime="text/csv", use_container_width=True,
                                 key="rep_g_csv")

            st.warning(nt("hg_warn"))

# ══════════════════════════════════════════════════════════════════════════════
# 📄 页脚免责声明（位于所有 Tab 之外，每个页面底部都会显示）
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="disclaimer-foot">'
    f'<b>{tr("disc_foot_title")}</b>'
    '<ul>'
    f'<li>{tr("disc_f1")}</li>'
    f'<li>{tr("disc_f2")}</li>'
    f'<li>{tr("disc_f3")}</li>'
    f'<li>{tr("disc_f4")}</li>'
    f'<li>{tr("disc_f5")}</li>'
    '</ul></div>', unsafe_allow_html=True)
