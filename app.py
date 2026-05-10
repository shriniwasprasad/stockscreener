import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="Indian Stock Screener Pro", page_icon="📈", layout="wide")

# Comprehensive NSE Stock List with Sector and Cap Classification
STOCK_DATA = {
    # LARGE CAP - Nifty 50
    "RELIANCE.NS": {"sector": "Energy", "cap": "Large Cap"},
    "TCS.NS": {"sector": "IT", "cap": "Large Cap"},
    "HDFCBANK.NS": {"sector": "Finance", "cap": "Large Cap"},
    "INFOSYS.NS": {"sector": "IT", "cap": "Large Cap"},
    "ICICIBANK.NS": {"sector": "Finance", "cap": "Large Cap"},
    "SBIN.NS": {"sector": "Finance", "cap": "Large Cap"},
    "BHARTIARTL.NS": {"sector": "Telecom", "cap": "Large Cap"},
    "HINDUNILVR.NS": {"sector": "FMCG", "cap": "Large Cap"},
    "ITC.NS": {"sector": "FMCG", "cap": "Large Cap"},
    "LT.NS": {"sector": "Infrastructure", "cap": "Large Cap"},
    "KOTAKBANK.NS": {"sector": "Finance", "cap": "Large Cap"},
    "AXISBANK.NS": {"sector": "Finance", "cap": "Large Cap"},
    "BAJFINANCE.NS": {"sector": "Finance", "cap": "Large Cap"},
    "MARUTI.NS": {"sector": "Auto", "cap": "Large Cap"},
    "WIPRO.NS": {"sector": "IT", "cap": "Large Cap"},
    "HCLTECH.NS": {"sector": "IT", "cap": "Large Cap"},
    "ASIANPAINT.NS": {"sector": "Chemicals", "cap": "Large Cap"},
    "TITAN.NS": {"sector": "Consumer", "cap": "Large Cap"},
    "SUNPHARMA.NS": {"sector": "Pharma", "cap": "Large Cap"},
    "ULTRACEMCO.NS": {"sector": "Cement", "cap": "Large Cap"},
    "NESTLEIND.NS": {"sector": "FMCG", "cap": "Large Cap"},
    "TATASTEEL.NS": {"sector": "Metals", "cap": "Large Cap"},
    "POWERGRID.NS": {"sector": "Power", "cap": "Large Cap"},
    "NTPC.NS": {"sector": "Power", "cap": "Large Cap"},
    "COALINDIA.NS": {"sector": "Metals", "cap": "Large Cap"},
    "JSWSTEEL.NS": {"sector": "Metals", "cap": "Large Cap"},
    "BAJAJFINSV.NS": {"sector": "Finance", "cap": "Large Cap"},
    "ADANIPORTS.NS": {"sector": "Logistics", "cap": "Large Cap"},
    "GRASIM.NS": {"sector": "Cement", "cap": "Large Cap"},
    "HDFCLIFE.NS": {"sector": "Finance", "cap": "Large Cap"},
    "DIVISLAB.NS": {"sector": "Pharma", "cap": "Large Cap"},
    "APOLLOHOSP.NS": {"sector": "Healthcare", "cap": "Large Cap"},
    "BRITANNIA.NS": {"sector": "FMCG", "cap": "Large Cap"},
    "CIPLA.NS": {"sector": "Pharma", "cap": "Large Cap"},
    "EICHERMOT.NS": {"sector": "Auto", "cap": "Large Cap"},
    "BPCL.NS": {"sector": "Energy", "cap": "Large Cap"},
    "DRREDDY.NS": {"sector": "Pharma", "cap": "Large Cap"},
    "INDUSINDBK.NS": {"sector": "Finance", "cap": "Large Cap"},
    "ONGC.NS": {"sector": "Energy", "cap": "Large Cap"},
    "SHREECEM.NS": {"sector": "Cement", "cap": "Large Cap"},
    "UPL.NS": {"sector": "Chemicals", "cap": "Large Cap"},
    "M&M.NS": {"sector": "Auto", "cap": "Large Cap"},
    "TECHM.NS": {"sector": "IT", "cap": "Large Cap"},
    "TATAMOTORS.NS": {"sector": "Auto", "cap": "Large Cap"},
    "SUNTV.NS": {"sector": "Media", "cap": "Large Cap"},
    "TORNTPHARM.NS": {"sector": "Pharma", "cap": "Large Cap"},
    "BOSCHLTD.NS": {"sector": "Auto", "cap": "Large Cap"},
    "PETRONET.NS": {"sector": "Energy", "cap": "Large Cap"},
    "GAIL.NS": {"sector": "Energy", "cap": "Large Cap"},
    "BIOCON.NS": {"sector": "Pharma", "cap": "Large Cap"},
    "SIEMENS.NS": {"sector": "Capital Goods", "cap": "Large Cap"},
    "PIDILITIND.NS": {"sector": "Chemicals", "cap": "Large Cap"},
    "COFORGE.NS": {"sector": "IT", "cap": "Large Cap"},
    "SBILIFE.NS": {"sector": "Finance", "cap": "Large Cap"},
    # MID CAP
    "CUMMINSIND.NS": {"sector": "Capital Goods", "cap": "Mid Cap"},
    "GODREJPROP.NS": {"sector": "Realty", "cap": "Mid Cap"},
    "LICHSGFIN.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "BANKBARODA.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "INDIGO.NS": {"sector": "Aviation", "cap": "Mid Cap"},
    "BANDHANBNK.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "PNB.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "IDFCFIRSTB.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "NHPC.NS": {"sector": "Power", "cap": "Mid Cap"},
    "SJVN.NS": {"sector": "Power", "cap": "Mid Cap"},
    "NMDC.NS": {"sector": "Metals", "cap": "Mid Cap"},
    "SAIL.NS": {"sector": "Metals", "cap": "Mid Cap"},
    "GMRINFRA.NS": {"sector": "Infrastructure", "cap": "Mid Cap"},
    "ADANIPOWER.NS": {"sector": "Power", "cap": "Mid Cap"},
    "TATAPOWER.NS": {"sector": "Power", "cap": "Mid Cap"},
    "JINDALSTEL.NS": {"sector": "Metals", "cap": "Mid Cap"},
    "EPL.NS": {"sector": "Consumer", "cap": "Mid Cap"},
    "GRAPHITE.NS": {"sector": "Chemicals", "cap": "Mid Cap"},
    "CENTURYTEXT.NS": {"sector": "Textiles", "cap": "Mid Cap"},
    "JKCEMENT.NS": {"sector": "Cement", "cap": "Mid Cap"},
    "AMBUJCEM.NS": {"sector": "Cement", "cap": "Mid Cap"},
    "ACC.NS": {"sector": "Cement", "cap": "Mid Cap"},
    "BERGEPAINT.NS": {"sector": "Chemicals", "cap": "Mid Cap"},
    "HAVELLS.NS": {"sector": "Consumer", "cap": "Mid Cap"},
    "DMART.NS": {"sector": "Retail", "cap": "Mid Cap"},
    "POLYCAB.NS": {"sector": "Consumer", "cap": "Mid Cap"},
    "TRENT.NS": {"sector": "Retail", "cap": "Mid Cap"},
    "HINDZINC.NS": {"sector": "Metals", "cap": "Mid Cap"},
    "HINDALCO.NS": {"sector": "Metals", "cap": "Mid Cap"},
    "FEDERALBNK.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "RBLBANK.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "YESBANK.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "KARURVYSYA.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "AUBLIMITED.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "KAJARIACER.NS": {"sector": "Consumer", "cap": "Mid Cap"},
    "AMRUTANJAN.NS": {"sector": "Healthcare", "cap": "Mid Cap"},
    "CASTROLIND.NS": {"sector": "Energy", "cap": "Mid Cap"},
    "MUTHOOTFIN.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "CHOLAHLDNG.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "DLF.NS": {"sector": "Realty", "cap": "Mid Cap"},
    "OBEROIREALTY.NS": {"sector": "Realty", "cap": "Mid Cap"},
    "PRESTIGE.NS": {"sector": "Realty", "cap": "Mid Cap"},
    "BRIGADE.NS": {"sector": "Realty", "cap": "Mid Cap"},
    "MANAPPURAM.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "SPANDANA.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "MCX.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "NEWGEN.NS": {"sector": "IT", "cap": "Mid Cap"},
    "HPCL.NS": {"sector": "Energy", "cap": "Mid Cap"},
    "MGL.NS": {"sector": "Energy", "cap": "Mid Cap"},
    "IGL.NS": {"sector": "Energy", "cap": "Mid Cap"},
    "VGUARD.NS": {"sector": "Consumer", "cap": "Mid Cap"},
    "WHIRLPOOL.NS": {"sector": "Consumer", "cap": "Mid Cap"},
    "SYMPHONY.NS": {"sector": "Consumer", "cap": "Mid Cap"},
    "VOLTAS.NS": {"sector": "Consumer", "cap": "Mid Cap"},
    "FINCABLES.NS": {"sector": "Capital Goods", "cap": "Mid Cap"},
    "KEI.NS": {"sector": "Capital Goods", "cap": "Mid Cap"},
    "RRKABEL.NS": {"sector": "Capital Goods", "cap": "Mid Cap"},
    "VEDL.NS": {"sector": "Metals", "cap": "Mid Cap"},
    "KALPATPOWR.NS": {"sector": "Power", "cap": "Mid Cap"},
    "TATAELXSI.NS": {"sector": "IT", "cap": "Mid Cap"},
    "MINDTREE.NS": {"sector": "IT", "cap": "Mid Cap"},
    "LTI.NS": {"sector": "IT", "cap": "Mid Cap"},
    "MPHASIS.NS": {"sector": "IT", "cap": "Mid Cap"},
    "PERSISTENT.NS": {"sector": "IT", "cap": "Mid Cap"},
    "LAKSHVILAS.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "TMBL.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "DCBBANK.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "KARNATAKABANK.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "J&KBANK.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "AUBANK.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "UNIONBANK.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "UCOBANK.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "INDIACEM.NS": {"sector": "Cement", "cap": "Mid Cap"},
    "BIRLAcorp.NS": {"sector": "Cement", "cap": "Mid Cap"},
    "NATIONALUM.NS": {"sector": "Chemicals", "cap": "Mid Cap"},
    "M&MFIN.NS": {"sector": "Finance", "cap": "Mid Cap"},
    "COROMANDEL.NS": {"sector": "Fertilizers", "cap": "Mid Cap"},
    "GSFC.NS": {"sector": "Fertilizers", "cap": "Mid Cap"},
    "GNFC.NS": {"sector": "Chemicals", "cap": "Mid Cap"},
    "DEEPAKFERT.NS": {"sector": "Fertilizers", "cap": "Mid Cap"},
    "GSPL.NS": {"sector": "Energy", "cap": "Mid Cap"},
    "GREENPOCO.NS": {"sector": "Energy", "cap": "Mid Cap"},
    "RALLIS.NS": {"sector": "Chemicals", "cap": "Mid Cap"},
    "DODLA.NS": {"sector": "FMCG", "cap": "Mid Cap"},
    "VADILALIND.NS": {"sector": "FMCG", "cap": "Mid Cap"},
    "HATSUN.NS": {"sector": "FMCG", "cap": "Mid Cap"},
    "AVANTIFEED.NS": {"sector": "FMCG", "cap": "Mid Cap"},
    "CARBORUNIV.NS": {"sector": "Chemicals", "cap": "Mid Cap"},
    "TANLA.NS": {"sector": "IT", "cap": "Mid Cap"},
    "ZOMATO.NS": {"sector": "IT", "cap": "Mid Cap"},
    "SIGNATURE.NS": {"sector": "Retail", "cap": "Mid Cap"},
    "METRO.BRAND.NS": {"sector": "Retail", "cap": "Mid Cap"},
    "JUBLFOOD.NS": {"sector": "FMCG", "cap": "Mid Cap"},
    "DEVYANI.NS": {"sector": "FMCG", "cap": "Mid Cap"},
    "WESTLIFE.NS": {"sector": "Retail", "cap": "Mid Cap"},
    "IRCTC.NS": {"sector": "Logistics", "cap": "Mid Cap"},
    "CONCOR.NS": {"sector": "Logistics", "cap": "Mid Cap"},
    "VRLLOGISTICS.NS": {"sector": "Logistics", "cap": "Mid Cap"},
    "KEC.NS": {"sector": "Capital Goods", "cap": "Mid Cap"},
    "THERMAX.NS": {"sector": "Capital Goods", "cap": "Mid Cap"},
    "CUMMINS.NS": {"sector": "Capital Goods", "cap": "Mid Cap"},
    # SMALL CAP - High Growth Potential
    "ADANIENT.NS": {"sector": "Infrastructure", "cap": "Small Cap"},
    "ADANIENSOL.NS": {"sector": "Power", "cap": "Small Cap"},
    "ADANIGREEN.NS": {"sector": "Power", "cap": "Small Cap"},
    "ADANITRANS.NS": {"sector": "Logistics", "cap": "Small Cap"},
    "ADANIWILMAR.NS": {"sector": "FMCG", "cap": "Small Cap"},
    "TORNTPOWER.NS": {"sector": "Power", "cap": "Small Cap"},
    "RAIN.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "GODREJCP.NS": {"sector": "FMCG", "cap": "Small Cap"},
    "CONCOR.NS": {"sector": "Logistics", "cap": "Small Cap"},
    "IDEA.NS": {"sector": "Telecom", "cap": "Small Cap"},
    "IBULHSGFIN.NS": {"sector": "Finance", "cap": "Small Cap"},
    "RECLIMITED.NS": {"sector": "Finance", "cap": "Small Cap"},
    "VRLLOGISTICS.NS": {"sector": "Logistics", "cap": "Small Cap"},
    "ALLIEDBLDRS.NS": {"sector": "Construction", "cap": "Small Cap"},
    "MAHLOGISTICS.NS": {"sector": "Logistics", "cap": "Small Cap"},
    "SMCGLOBAL.NS": {"sector": "Finance", "cap": "Small Cap"},
    "HGINFRA.NS": {"sector": "Infrastructure", "cap": "Small Cap"},
    "PNCINFRA.NS": {"sector": "Infrastructure", "cap": "Small Cap"},
    "IRB.NS": {"sector": "Infrastructure", "cap": "Small Cap"},
    "KIRLOSENG.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "BHEL.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "AJRINFRA.NS": {"sector": "Infrastructure", "cap": "Small Cap"},
    "BEW Eng.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "NEEPCO.NS": {"sector": "Power", "cap": "Small Cap"},
    "KIRLOSKAR.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "PAGEIND.NS": {"sector": "FMCG", "cap": "Small Cap"},
    "NAUKRI.NS": {"sector": "IT", "cap": "Small Cap"},
    "ABB.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "SOMANYCERAM.NS": {"sector": "Consumer", "cap": "Small Cap"},
    "AKZOINDIA.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "Nerolac.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "Bajajelect.NS": {"sector": "Consumer", "cap": "Small Cap"},
    "KRISHNA.NS": {"sector": "FMCG", "cap": "Small Cap"},
    "MPLATFORMS.NS": {"sector": "IT", "cap": "Small Cap"},
    "RUCHIRA.NS": {"sector": "Paper", "cap": "Small Cap"},
    "ENERGYDEV.NS": {"sector": "Power", "cap": "Small Cap"},
    "NIACL.NS": {"sector": "Finance", "cap": "Small Cap"},
    "GICRE.NS": {"sector": "Finance", "cap": "Small Cap"},
    "TATAINVEST.NS": {"sector": "Finance", "cap": "Small Cap"},
    "WONDERLA.NS": {"sector": "Entertainment", "cap": "Small Cap"},
    "GPIL.NS": {"sector": "Metals", "cap": "Small Cap"},
    "OPTOCIRCUI.NS": {"sector": "Electronics", "cap": "Small Cap"},
    "BLUESTARCO.NS": {"sector": "Consumer", "cap": "Small Cap"},
    "PHOENIXLTD.NS": {"sector": "Realty", "cap": "Small Cap"},
    "BALRAMCHIN.NS": {"sector": "Agri", "cap": "Small Cap"},
    "EIDPARRY.NS": {"sector": "Agri", "cap": "Small Cap"},
    "DWARKESH.NS": {"sector": "Agri", "cap": "Small Cap"},
    "BANARISUG.NS": {"sector": "Agri", "cap": "Small Cap"},
    "RENUKA.NS": {"sector": "Agri", "cap": "Small Cap"},
    "TRIVENI.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "BKMINDUS.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "KCP.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "CHAMBLFERT.NS": {"sector": "Fertilizers", "cap": "Small Cap"},
    "BASF.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "PIRAMALSA.NS": {"sector": "Finance", "cap": "Small Cap"},
    "JARASUGAR.NS": {"sector": "Agri", "cap": "Small Cap"},
    "DALMIAFERT.NS": {"sector": "Fertilizers", "cap": "Small Cap"},
    "RCF.NS": {"sector": "Fertilizers", "cap": "Small Cap"},
    "NFL.NS": {"sector": "Fertilizers", "cap": "Small Cap"},
    "FACT.NS": {"sector": "Fertilizers", "cap": "Small Cap"},
    "TRIVENI.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "TATAARMSTR.NS": {"sector": "Auto", "cap": "Small Cap"},
}

NSE_TICKERS = list(STOCK_DATA.keys())

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_hist = macd - macd_signal
    return macd, macd_signal, macd_hist

def calculate_sma(prices, period):
    return prices.rolling(window=period).mean()

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        hist = stock.history(period="90d")
        if hist is None or hist.empty:
            hist = stock.history(period="6mo")

        if hist is None or hist.empty:
            return None

        current_price = hist['Close'].iloc[-1]
        current_volume = hist['Volume'].iloc[-1]
        avg_volume_20 = hist['Volume'].iloc[-20:].mean() if len(hist) >= 20 else hist['Volume'].mean()
        volume_ratio = current_volume / avg_volume_20 if avg_volume_20 > 0 else 1.0

        close_prices = hist['Close']

        rsi = calculate_rsi(close_prices, 14)
        current_rsi = rsi.iloc[-1] if not rsi.empty else 50

        macd, macd_signal, macd_hist = calculate_macd(close_prices)
        current_macd = macd.iloc[-1] if not macd.empty else 0
        current_macd_signal = macd_signal.iloc[-1] if not macd_signal.empty else 0
        macd_bullish = current_macd > current_macd_signal

        sma_20 = calculate_sma(close_prices, 20)
        sma_50 = calculate_sma(close_prices, 50)
        sma_200 = calculate_sma(close_prices, 200)

        current_sma20 = sma_20.iloc[-1] if not sma_20.empty else current_price
        current_sma50 = sma_50.iloc[-1] if not sma_50.empty else current_price
        current_sma200 = sma_200.iloc[-1] if len(sma_200) >= 200 and not sma_200.iloc[-200:].empty else current_price

        above_sma20 = current_price > current_sma20
        above_sma50 = current_price > current_sma50
        above_sma200 = current_price > current_sma200 if current_sma200 != current_price else False

        pe_ratio = None
        if info.get('forwardPE') and info.get('forwardPE') > 0:
            pe_ratio = info.get('forwardPE')
        elif info.get('trailingPE') and info.get('trailingPE') > 0:
            pe_ratio = info.get('trailingPE')

        if pe_ratio is None or pe_ratio <= 0:
            pe_ratio = 50.0

        market_cap = info.get('marketCap', None)

        stock_info = STOCK_DATA.get(ticker, {"sector": "Other", "cap": "Small Cap"})

        low_52 = info.get('fiftyTwoWeekLow')
        high_52 = info.get('fiftyTwoWeekHigh')
        if (low_52 is None or high_52 is None) and len(hist) > 0:
            low_52 = hist['Low'].min()
            high_52 = hist['High'].max()

        score, rec = calculate_score(current_price, pe_ratio, current_rsi, volume_ratio, low_52, high_52, macd_bullish, above_sma20, above_sma50)

        return {
            'ticker': ticker.replace('.NS', ''),
            'full_ticker': ticker,
            'current_price': current_price,
            'pe_ratio': pe_ratio,
            'volume_ratio': volume_ratio,
            'rsi': current_rsi,
            'macd': current_macd,
            'macd_signal': current_macd_signal,
            'macd_bullish': macd_bullish,
            'sma20': current_sma20,
            'sma50': current_sma50,
            'sma200': current_sma200,
            'above_sma20': above_sma20,
            'above_sma50': above_sma50,
            'above_sma200': above_sma200,
            'market_cap': market_cap,
            'sector': stock_info['sector'],
            'cap': stock_info['cap'],
            'low_52': low_52,
            'high_52': high_52,
            'score': score,
            'recommendation': rec
        }
    except Exception as e:
        return None

def calculate_score(price, pe, rsi, volume_ratio, low_52, high_52, macd_bullish, above_sma20, above_sma50):
    score = 0

    if pe and 0 < pe < 15:
        score += 3
    elif pe and 15 <= pe < 25:
        score += 2
    elif pe and 25 <= pe < 35:
        score += 1

    if rsi > 70:
        score += 0
    elif 50 < rsi <= 70:
        score += 2
    elif 40 < rsi <= 50:
        score += 1

    if volume_ratio >= 2.0:
        score += 3
    elif volume_ratio >= 1.5:
        score += 2
    elif volume_ratio >= 1.2:
        score += 1

    if macd_bullish:
        score += 2

    if above_sma20 and above_sma50:
        score += 2
    elif above_sma20:
        score += 1

    if low_52 and high_52 and high_52 > low_52:
        price_pos = (price - low_52) / (high_52 - low_52)
        if price_pos < 0.3:
            score += 2
        elif price_pos < 0.5:
            score += 1
        elif price_pos > 0.9:
            score -= 1

    if score >= 7:
        rec = "STRONG BUY"
    elif score >= 5:
        rec = "BUY"
    elif score >= 3:
        rec = "HOLD"
    else:
        rec = "WAIT"

    return score, rec

# Chart functions - defined before main execution
def create_price_sma_chart(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        if hist is None or hist.empty:
            return None
        close = hist['Close']
        sma20 = close.rolling(20).mean()
        sma50 = close.rolling(50).mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=close, name='Price', line=dict(color='white', width=2)))
        fig.add_trace(go.Scatter(x=hist.index, y=sma20, name='SMA 20', line=dict(color='yellow', width=1)))
        fig.add_trace(go.Scatter(x=hist.index, y=sma50, name='SMA 50', line=dict(color='blue', width=1)))
        fig.update_layout(title=f'{ticker.replace(".NS", "")} - Price & SMA', template='plotly_dark', height=400)
        return fig
    except:
        return None

def create_macd_chart(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        if hist is None or hist.empty:
            return None
        close = hist['Close']
        macd, signal, hist_val = calculate_macd(close)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=macd, name='MACD', line=dict(color='blue', width=2)))
        fig.add_trace(go.Scatter(x=hist.index, y=signal, name='Signal', line=dict(color='orange', width=2)))
        fig.add_trace(go.Bar(x=hist.index, y=hist_val, name='Histogram', marker_color='gray'))
        fig.update_layout(title=f'{ticker.replace(".NS", "")} - MACD', template='plotly_dark', height=300)
        return fig
    except:
        return None

def create_rsi_chart(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        if hist is None or hist.empty:
            return None
        rsi = calculate_rsi(hist['Close'], 14)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=rsi.index, y=rsi, name='RSI', line=dict(color='purple', width=2)))
        fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
        fig.add_hline(y=50, line_dash="dot", line_color="gray")
        fig.update_layout(title=f'{ticker.replace(".NS", "")} - RSI', template='plotly_dark', height=300, yaxis=dict(range=[0, 100]))
        return fig
    except:
        return None

# Sidebar
st.sidebar.title("🇮🇳 Stock Screener Pro")

st.sidebar.markdown("### 📊 Filter Options")

cap_filter = st.sidebar.multiselect(
    "Cap Type",
    ["Large Cap", "Mid Cap", "Small Cap"],
    default=["Large Cap", "Mid Cap", "Small Cap"]
)

sector_filter = st.sidebar.multiselect(
    "Sector",
    ["Finance", "IT", "FMCG", "Pharma", "Energy", "Metals", "Cement", "Auto", "Consumer", "Power", "Infrastructure", "Realty", "Retail", "Chemicals", "Logistics", "Healthcare", "Other"],
    default=["Finance", "IT", "FMCG", "Pharma", "Energy", "Metals", "Cement", "Auto", "Consumer", "Power", "Infrastructure", "Realty", "Retail", "Chemicals", "Logistics", "Healthcare"]
)

st.sidebar.markdown("### 🎯 Technical Filters")
pe_max = st.sidebar.number_input("Max P/E Ratio", value=50, step=5)
rsi_min = st.sidebar.slider("Min RSI", 20, 70, 35)
vol_min = st.sidebar.slider("Min Volume Ratio", 0.5, 3.0, 0.8, step=0.1)
macd_bullish_only = st.sidebar.checkbox("MACD Bullish Only", value=False)
sma_bullish_only = st.sidebar.checkbox("SMA Bullish (20>50) Only", value=False)

st.sidebar.markdown("### 💰 Target & Stop Loss")
target_percent = st.sidebar.number_input("Target %", value=20, step=5)
stop_loss_percent = st.sidebar.number_input("Stop Loss %", value=10, step=2)

num_stocks = st.sidebar.slider("Stocks to Scan", 50, 500, 150, step=10)
auto_refresh = st.sidebar.checkbox("Auto-refresh", value=False)

# Main
st.title("🇮🇳 Indian Stock Screener Pro - Expert Analysis")
st.markdown(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")

progress_bar = st.progress(0)
status_text = st.empty()

results = []
total = min(num_stocks, len(NSE_TICKERS))
ticker_list = NSE_TICKERS[:total]

status_text.text(f"Scanning {total} Indian stocks...")

for i, ticker in enumerate(ticker_list):
    progress_bar.progress((i + 1) / total)
    data = get_stock_data(ticker)
    if data:
        results.append(data)

progress_bar.empty()
status_text.empty()

results.sort(key=lambda x: x['score'], reverse=True)

# Apply filters
filtered = []
for r in results:
    if r['cap'] not in cap_filter:
        continue
    if r['sector'] not in sector_filter:
        continue
    if r['pe_ratio'] and r['pe_ratio'] >= pe_max:
        continue
    if r['rsi'] <= rsi_min:
        continue
    if r['volume_ratio'] <= vol_min:
        continue
    if macd_bullish_only and not r['macd_bullish']:
        continue
    if sma_bullish_only and not (r['above_sma20'] and r['above_sma50']):
        continue
    filtered.append(r)

# Calculate targets
for r in filtered:
    r['target_price'] = r['current_price'] * (1 + target_percent/100)
    r['stop_loss'] = r['current_price'] * (1 - stop_loss_percent/100)
    r['upside'] = target_percent

st.markdown("---")

if filtered:
    st.subheader(f"✅ Filtered Results: {len(filtered)} stocks")

    df = pd.DataFrame([{
        'Rank': i+1,
        'Ticker': r['ticker'],
        'Sector': r['sector'],
        'Cap': r['cap'],
        'Price': f"₹{r['current_price']:.2f}",
        'P/E': f"{r['pe_ratio']:.1f}",
        'Vol': f"{r['volume_ratio']:.2f}x",
        'RSI': f"{r['rsi']:.0f}",
        'MACD': "🟢" if r['macd_bullish'] else "🔴",
        'SMA20': "✅" if r['above_sma20'] else "❌",
        'SMA50': "✅" if r['above_sma50'] else "❌",
        'Score': r['score'],
        'Rec': r['recommendation'],
        'Target': f"₹{r['target_price']:.2f}",
        'Stop': f"₹{r['stop_loss']:.2f}",
        'Upside': f"+{r['upside']}%"
    } for i, r in enumerate(filtered)])

    def color_rec(val):
        if 'STRONG' in str(val): return 'color: #00C853; font-weight: bold'
        if 'BUY' in str(val): return 'color: #4CAF50'
        if 'HOLD' in str(val): return 'color: #FF9800'
        return 'color: #9E9E9E'

    st.dataframe(df.style.map(color_rec, subset=['Rec']), use_container_width=True, height=400)

    # Expert Analysis - Top 5 Recommendations
    st.markdown("---")
    st.subheader("🏆 TOP 5 EXPERT PICKS - BUY NOW")

    top5 = filtered[:5]

    cols = st.columns(5)
    for i, r in enumerate(top5):
        with cols[i]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 15px; border-radius: 10px; margin: 5px; text-align: center;">
                <h4 style="color: #FFD700; margin: 0;">#{i+1} {r['ticker']}</h4>
                <p style="color: #aaa; font-size: 12px;">{r['sector']} | {r['cap']}</p>
                <h2 style="color: #4CAF50; margin: 5px 0;">₹{r['current_price']:.2f}</h2>
                <p style="color: #4CAF50; font-weight: bold;">{r['recommendation']}</p>
                <hr style="border-color: #333;">
                <p style="color: #fff; font-size: 11px;">Target: ₹{r['target_price']:.2f}</p>
                <p style="color: #f44336; font-size: 11px;">Stop: ₹{r['stop_loss']:.2f}</p>
                <p style="color: #FFD700; font-size: 14px; font-weight: bold;">+{r['upside']}% Upside</p>
            </div>
            """, unsafe_allow_html=True)

    # Detailed Analysis for Top 5
    st.markdown("---")
    st.subheader("📊 Detailed Analysis - Top 5 Stocks")

    for i, r in enumerate(top5, 1):
        with st.expander(f"#{i} {r['ticker']} - {r['recommendation']}", expanded=True):
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            c1.metric("Price", f"₹{r['current_price']:.2f}")
            c2.metric("Target", f"₹{r['target_price']:.2f}", f"+{r['upside']}%")
            c3.metric("Stop Loss", f"₹{r['stop_loss']:.2f}", f"-{stop_loss_percent}%")
            c4.metric("P/E", f"{r['pe_ratio']:.1f}")
            c5.metric("RSI", f"{r['rsi']:.0f}")
            c6.metric("Score", f"{r['score']}/12")

            st.markdown(f"""
            **Technical Indicators:**
            - MACD: {"🟢 Bullish" if r['macd_bullish'] else "🔴 Bearish"} (MACD: {r['macd']:.2f}, Signal: {r['macd_signal']:.2f})
            - SMA 20: ₹{r['sma20']:.2f} - Price {'✅ Above' if r['above_sma20'] else '❌ Below'}
            - SMA 50: ₹{r['sma50']:.2f} - Price {'✅ Above' if r['above_sma50'] else '❌ Below'}
            - Volume: {r['volume_ratio']:.2f}x average
            - 52W Range: ₹{r['low_52']:.2f} - ₹{r['high_52']:.2f}
            """)

            # Charts
            tabs = st.tabs(["📈 Price + SMA", "📊 MACD", "📉 RSI"])
            with tabs[0]:
                fig = create_price_sma_chart(r['full_ticker'])
                if fig: st.plotly_chart(fig, use_container_width=True)
            with tabs[1]:
                fig = create_macd_chart(r['full_ticker'])
                if fig: st.plotly_chart(fig, use_container_width=True)
            with tabs[2]:
                fig = create_rsi_chart(r['full_ticker'])
                if fig: st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No stocks match filters. Showing top by score.")
    st.subheader("📊 Top 10 by Score")

    df = pd.DataFrame([{
        'Rank': i+1,
        'Ticker': r['ticker'],
        'Sector': r['sector'],
        'Cap': r['cap'],
        'Price': f"₹{r['current_price']:.2f}",
        'P/E': f"{r['pe_ratio']:.1f}",
        'RSI': f"{r['rsi']:.0f}",
        'MACD': "🟢" if r['macd_bullish'] else "🔴",
        'Score': r['score'],
        'Rec': r['recommendation'],
    } for i, r in enumerate(results[:10])])

    def color_rec(val):
        if 'STRONG' in str(val): return 'color: #00C853; font-weight: bold'
        if 'BUY' in str(val): return 'color: #4CAF50'
        return 'color: #FF9800'

    st.dataframe(df.style.map(color_rec, subset=['Rec']), use_container_width=True)

if auto_refresh:
    time.sleep(60)
    st.rerun()

st.markdown("---")
st.markdown("""
<small>
⚠️ <b>Disclaimer:</b> For educational purposes only. Not financial advice. Always do your own research before investing.
| Target: +{}% | Stop Loss: -{}%
</small>
""".format(target_percent, stop_loss_percent), unsafe_allow_html=True)