import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="Nifty 200 Momentum 30", page_icon="🎯", layout="wide")

# Nifty 200 Stock List (Large + Mid Cap only)
NIFTY200_STOCKS = {
    # LARGE CAP - Nifty 50
    "RELIANCE.NS": {"sector": "Energy", "cap": "Large Cap"},
    "TCS.NS": {"sector": "IT", "cap": "Large Cap"},
    "HDFCBANK.NS": {"sector": "Finance", "cap": "Large Cap"},
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
}

# Small Cap stocks with good fundamentals (potential multi-baggers)
SMALL_CAP_STOCKS = {
    # AUTO & AUTO COMPONENTS
    "MRF.NS": {"sector": "Auto", "cap": "Small Cap"},
    "APOLLOTYRE.NS": {"sector": "Auto", "cap": "Small Cap"},
    "BALKRISIND.NS": {"sector": "Auto", "cap": "Small Cap"},
    "ENDURANCE.NS": {"sector": "Auto", "cap": "Small Cap"},
    "MOTHERSUMI.NS": {"sector": "Auto", "cap": "Small Cap"},

    # IT & ITES
    "LTIM.NS": {"sector": "IT", "cap": "Small Cap"},
    "COFORGE.NS": {"sector": "IT", "cap": "Small Cap"},
    "LTI.NS": {"sector": "IT", "cap": "Small Cap"},
    "PERSISTENT.NS": {"sector": "IT", "cap": "Small Cap"},
    "TATAELXSI.NS": {"sector": "IT", "cap": "Small Cap"},
    "MPHASIS.NS": {"sector": "IT", "cap": "Small Cap"},
    "TANLA.NS": {"sector": "IT", "cap": "Small Cap"},
    "ZOMATO.NS": {"sector": "IT", "cap": "Small Cap"},
    "NAUKRI.NS": {"sector": "IT", "cap": "Small Cap"},
    "INFOEDGE.NS": {"sector": "IT", "cap": "Small Cap"},
    "CYIENT.NS": {"sector": "IT", "cap": "Small Cap"},
    "INTELLECT.NS": {"sector": "IT", "cap": "Small Cap"},

    # FINANCE & NBFC
    "BANDHANBNK.NS": {"sector": "Finance", "cap": "Small Cap"},
    "IDFCFIRSTB.NS": {"sector": "Finance", "cap": "Small Cap"},
    "AUBANK.NS": {"sector": "Finance", "cap": "Small Cap"},
    "FINO.NS": {"sector": "Finance", "cap": "Small Cap"},
    "SPANDANA.NS": {"sector": "Finance", "cap": "Small Cap"},
    "MUTHOOTFIN.NS": {"sector": "Finance", "cap": "Small Cap"},
    "MANAPPURAM.NS": {"sector": "Finance", "cap": "Small Cap"},
    "CHOLAHLDNG.NS": {"sector": "Finance", "cap": "Small Cap"},
    "SHRIRAMFIN.NS": {"sector": "Finance", "cap": "Small Cap"},

    # PHARMA
    "AUROBINDO.NS": {"sector": "Pharma", "cap": "Small Cap"},
    "LUPIN.NS": {"sector": "Pharma", "cap": "Small Cap"},
    "GLENMARK.NS": {"sector": "Pharma", "cap": "Small Cap"},
    "IPCALAB.NS": {"sector": "Pharma", "cap": "Small Cap"},
    "DBL.NS": {"sector": "Pharma", "cap": "Small Cap"},
    "METROPOLIS.NS": {"sector": "Pharma", "cap": "Small Cap"},
    "DIAPHRAGM.NS": {"sector": "Pharma", "cap": "Small Cap"},

    # FMCG & CONSUMER
    "VARISHA.NS": {"sector": "FMCG", "cap": "Small Cap"},
    "HATSUN.NS": {"sector": "FMCG", "cap": "Small Cap"},
    "AVANTIFEED.NS": {"sector": "FMCG", "cap": "Small Cap"},
    "DODLA.NS": {"sector": "FMCG", "cap": "Small Cap"},
    "PATANJALI.NS": {"sector": "FMCG", "cap": "Small Cap"},
    "COLPAL.NS": {"sector": "FMCG", "cap": "Small Cap"},
    "GODREJCP.NS": {"sector": "FMCG", "cap": "Small Cap"},

    # CHEMICALS
    "TATACHEM.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "PIIND.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "AARTI.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "ALKYLAMINE.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "CAMEX.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "INDRAMEDCO.NS": {"sector": "Chemicals", "cap": "Small Cap"},

    # REALTY & INFRA
    "DLF.NS": {"sector": "Realty", "cap": "Small Cap"},
    "GODREJPROP.NS": {"sector": "Realty", "cap": "Small Cap"},
    "BRIGADE.NS": {"sector": "Realty", "cap": "Small Cap"},
    "PRESTIGE.NS": {"sector": "Realty", "cap": "Small Cap"},
    "OBEROIREALTY.NS": {"sector": "Realty", "cap": "Small Cap"},
    "MAHLIFE.NS": {"sector": "Realty", "cap": "Small Cap"},

    # METALS & MINING
    "NMDC.NS": {"sector": "Metals", "cap": "Small Cap"},
    "MOIL.NS": {"sector": "Metals", "cap": "Small Cap"},
    "GRAUWEIL.NS": {"sector": "Metals", "cap": "Small Cap"},
    "WELCORP.NS": {"sector": "Metals", "cap": "Small Cap"},

    # POWER & RENEWABLE
    "ADANIGREEN.NS": {"sector": "Power", "cap": "Small Cap"},
    "ADANIENSOL.NS": {"sector": "Power", "cap": "Small Cap"},
    "TATAPOWER.NS": {"sector": "Power", "cap": "Small Cap"},
    "ADANIPOWER.NS": {"sector": "Power", "cap": "Small Cap"},
    "KALPATPOWR.NS": {"sector": "Power", "cap": "Small Cap"},

    # CEMENT
    "DECCANCE.NS": {"sector": "Cement", "cap": "Small Cap"},
    "HEIDELBERG.NS": {"sector": "Cement", "cap": "Small Cap"},
    "STAR.NS": {"sector": "Cement", "cap": "Small Cap"},

    # SPECIALTY CHEMICALS
    "FINEORG.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "NATHBIOGEN.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "PUNJABCHEM.NS": {"sector": "Chemicals", "cap": "Small Cap"},

    # RETAIL
    "TRENT.NS": {"sector": "Retail", "cap": "Small Cap"},
    "TITAN.NS": {"sector": "Retail", "cap": "Small Cap"},
    "KALYANJEW.NS": {"sector": "Retail", "cap": "Small Cap"},
    "WNCL.NS": {"sector": "Retail", "cap": "Small Cap"},

    # HOSPITAL & HEALTHCARE
    "APOLLOHOSP.NS": {"sector": "Healthcare", "cap": "Small Cap"},
    "FORTIS.NS": {"sector": "Healthcare", "cap": "Small Cap"},
    "MAXHEALTH.NS": {"sector": "Healthcare", "cap": "Small Cap"},
    "METROHOSP.NS": {"sector": "Healthcare", "cap": "Small Cap"},
    "KIMS.NS": {"sector": "Healthcare", "cap": "Small Cap"},

    # TEXTILES
    "KPRMILL.NS": {"sector": "Textiles", "cap": "Small Cap"},
    "SPAPP.NS": {"sector": "Textiles", "cap": "Small Cap"},
    "NEGILACH.NS": {"sector": "Textiles", "cap": "Small Cap"},

    # LOGISTICS
    "CONCOR.NS": {"sector": "Logistics", "cap": "Small Cap"},
    "VRLLOGISTICS.NS": {"sector": "Logistics", "cap": "Small Cap"},
    "TCI.NS": {"sector": "Logistics", "cap": "Small Cap"},
    "MAHLOGISTICS.NS": {"sector": "Logistics", "cap": "Small Cap"},

    # CAPITAL GOODS
    "CGCL.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "ELGI.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "WHIRLPOOL.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "VOLTAS.NS": {"sector": "Capital Goods", "cap": "Small Cap"},
    "BLUESTARCO.NS": {"sector": "Capital Goods", "cap": "Small Cap"},

    # AGRI & FERTILIZERS
    "COROMANDEL.NS": {"sector": "Fertilizers", "cap": "Small Cap"},
    "BASF.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "DHANUKA.NS": {"sector": "Chemicals", "cap": "Small Cap"},
    "RALLIS.NS": {"sector": "Chemicals", "cap": "Small Cap"},
}

# Combine all stocks
ALL_STOCKS = {**NIFTY200_STOCKS, **SMALL_CAP_STOCKS}
ALL_TICKERS = list(ALL_STOCKS.keys())

NSE_TICKERS = list(NIFTY200_STOCKS.keys())

# Strategy Parameters (matching Pine Script exactly)
LOOKBACK_52W = 260  # 52-week high lookback bars
VOLUME_MULT_BREAKOUT = 2.0  # Volume multiplier for breakout day
VOL_AVG_LEN = 50  # Volume average length
NEAR_PCT = 3.0  # Near-breakout threshold (%)
VOL_NEAR_LEN = 20  # Volume avg for near-breakout
ATR_LEN = 14
ATR_MIN_PCT = 1.5
ATR_MAX_PCT = 5.0
BASE_WEEKS = 6  # Base rising look-back weeks
TRAIL_EMA_LEN = 10


def calculate_sma(prices, period):
    return prices.rolling(window=period).mean()


def calculate_ema(prices, period):
    return prices.ewm(span=period, adjust=False).mean()


def calculate_atr(hist, period=14):
    high = hist['High']
    low = hist['Low']
    close = hist['Close']
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return atr


def get_momentum_data(ticker):
    """Get data matching Nifty200 Momentum 30 strategy exactly"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")

        if hist is None or hist.empty:
            return None

        close = hist['Close']
        high = hist['High']
        low = hist['Low']
        volume = hist['Volume']

        # Current values
        current_price = close.iloc[-1]
        current_volume = volume.iloc[-1]

        # Get values from 1 day and bars ago
        close_1d_ago = close.iloc[-2] if len(close) > 1 else current_price
        high_1d_ago = high.iloc[-2] if len(high) > 1 else current_price
        low_1d_ago = low.iloc[-2] if len(low) > 1 else current_price

        # SMAs - matching Pine Script exactly
        sma50 = calculate_sma(close, 50)
        sma200 = calculate_sma(close, 200)
        current_sma50 = sma50.iloc[-1] if len(sma50) >= 50 else current_price
        current_sma200 = sma200.iloc[-1] if len(sma200) >= 200 else current_price

        # 6 weeks ago SMA50 (30 bars = 6 weeks * 5 trading days)
        sma50_6w_ago = sma50.iloc[-30] if len(sma50) >= 30 else sma50.iloc[0]

        # 52-week high - rolling max of 260 bars
        high_52w = high.rolling(window=LOOKBACK_52W).max()
        high_52w_current = high_52w.iloc[-1] if len(high_52w) >= LOOKBACK_52W else high.max()
        high_52w_1d_ago = high_52w.iloc[-2] if len(high_52w) >= 2 else high.iloc[-2] if len(high) >= 2 else high.max()

        # ATR
        atr = calculate_atr(hist, ATR_LEN)
        current_atr = atr.iloc[-1] if len(atr) >= ATR_LEN else 0
        atr_percent = (current_atr / current_price * 100) if current_price > 0 else 0

        # Volumes - matching Pine Script parameters
        vol_avg50 = volume.rolling(VOL_AVG_LEN).mean().iloc[-1] if len(volume) >= VOL_AVG_LEN else volume.mean()
        vol_avg20 = volume.rolling(VOL_NEAR_LEN).mean().iloc[-1] if len(volume) >= VOL_NEAR_LEN else volume.mean()

        # Trailing EMA (10)
        trail_ema = calculate_ema(close, TRAIL_EMA_LEN)
        current_trail_ema = trail_ema.iloc[-1] if len(trail_ema) >= TRAIL_EMA_LEN else current_price
        trail_ema_1d_ago = trail_ema.iloc[-2] if len(trail_ema) >= 2 else current_price

        # Traded Value
        traded_value = current_volume * current_price

        # Layer 1 - Market Regime (from Pine Script)
        uptrend = current_price > current_sma50 and current_price > current_sma200
        golden_cross = current_sma50 > current_sma200
        base_rising = current_sma50 > sma50_6w_ago
        regime_ok = uptrend and golden_cross and base_rising

        # Layer 2 - Volatility Filter
        atr_ok = atr_percent > ATR_MIN_PCT and atr_percent < ATR_MAX_PCT

        # Layer 3 - Breakout Conditions (matching Pine Script exactly)
        # Case A: Fresh breakout - closed above 52-week high today with 2x volume
        fresh_breakout = (current_price > high_52w_current and
                         close_1d_ago < high_52w_1d_ago and
                         current_volume > VOLUME_MULT_BREAKOUT * vol_avg50)

        # Case B: Near breakout - within 3% below high, volume compressing
        near_level = high_52w_current * (1 - NEAR_PCT / 100)
        near_breakout = (current_price >= near_level and
                         current_price < high_52w_current and
                         current_volume < vol_avg20)

        # Combined signals
        signal_fresh = regime_ok and atr_ok and fresh_breakout
        signal_near = regime_ok and atr_ok and near_breakout

        # Pattern classification
        if fresh_breakout and regime_ok and atr_ok:
            pattern = "BREAKOUT"
            days_since_breakout = 0
        elif near_breakout and regime_ok and atr_ok:
            pattern = "NEAR BREAKOUT"
            days_since_breakout = None
        else:
            pattern = None
            days_since_breakout = None

        # False breakout detection - price dropped after breakout
        false_breakout = False
        if fresh_breakout:
            # Check if price dropped more than 3% from 52w high within last 5 days
            for i in range(2, min(6, len(close))):
                if close.iloc[-i] > high_52w_current:
                    if (high_52w_current - close.iloc[-1]) / high_52w_current > 0.03:
                        false_breakout = True
                        break

        # Avoid stocks at resistance (multiple rejections near 52w high)
        rejection_count = 0
        for i in range(5, min(30, len(high))):
            if high.iloc[-i] > 0.98 * high_52w_current and close.iloc[-i] < 0.98 * high_52w_current:
                rejection_count += 1

        weak_setup = false_breakout or rejection_count >= 5  # Require 5+ rejections

        # ============== BUY/SELL TIMING PREDICTIONS ==============

        # Stop Loss - always below current price (use low or ATR-based)
        if low_1d_ago < current_price:
            stop_loss = low_1d_ago
        else:
            stop_loss = current_price - current_atr

        # Ensure stop loss is at least 1 ATR below current price
        stop_loss = min(stop_loss, current_price - current_atr)

        # Risk per share (must be positive)
        risk_per_share = current_price - stop_loss
        if risk_per_share <= 0:
            risk_per_share = current_atr  # Fallback to ATR if calculation is wrong

        # Targets (R multiples) - from entry price
        target1_price = current_price + (1.5 * risk_per_share)  # 1.5R
        target2_price = current_price + (3.0 * risk_per_share)   # 3R

        # Also calculate targets from GTT price for near breakout
        gtt_target1 = high_52w_current + (1.5 * risk_per_share)  # T1 from 52W high
        gtt_target2 = high_52w_current + (3.0 * risk_per_share)   # T2 from 52W high

        # Entry Timing Analysis
        # For fresh breakout - immediate entry or wait for pullback
        if pattern == "BREAKOUT":
            entry_type = "IMMEDIATE"
            entry_window = "Enter now at market price"
            pullback_entry = current_price - (0.5 * current_atr)  # Potential 0.5 ATR pullback
            entry_confidence = "HIGH"
        elif pattern == "NEAR BREAKOUT":
            entry_type = "GTT"
            entry_window = f"Set GTT at ₹{high_52w_current:.2f}"
            pullback_entry = current_price
            entry_confidence = "MEDIUM"
        else:
            entry_type = None
            entry_window = "No signal"
            pullback_entry = current_price
            entry_confidence = "LOW"

        # Sell Timing Analysis
        if current_price > current_trail_ema and close_1d_ago > trail_ema_1d_ago:
            sell_signal = "HOLD - Above trailing EMA"
            exit_priority = "Monitor for trail exit"
        elif current_price < current_trail_ema and close_1d_ago < trail_ema_1d_ago:
            sell_signal = "TRAIL EXIT - 2 closes below 10-EMA"
            exit_priority = "EXIT NOW"
        else:
            sell_signal = "NEUTRAL - Watch for confirmation"
            exit_priority = "Wait for 2nd candle below EMA"

        # Optimal Entry Time (based on intraday patterns - simplified)
        if pattern:
            optimal_entry = "Next candle open" if current_volume > vol_avg50 else "Wait for volume confirmation"
        else:
            optimal_entry = "No entry signal"

        # Time-based exit check
        days_in_trade = 0  # Would need position tracking

        # Risk-Reward Analysis
        if risk_per_share > 0:
            rr_ratio = (target1_price - current_price) / risk_per_share
            rr_ratio_2 = (target2_price - current_price) / risk_per_share
        else:
            rr_ratio = 0
            rr_ratio_2 = 0

        # Entry zone recommendation
        if pattern == "BREAKOUT":
            buy_zone_low = current_price
            buy_zone_high = current_price + current_atr
        elif pattern == "NEAR BREAKOUT":
            buy_zone_low = current_price - current_atr
            buy_zone_high = current_price
        else:
            buy_zone_low = current_price
            buy_zone_high = current_price

        stock_info = NIFTY200_STOCKS.get(ticker, {"sector": "Other", "cap": "Mid Cap"})

        # Calculate momentum score
        momentum_score = 0
        criteria_met = []

        if regime_ok:
            momentum_score += 3
            criteria_met.append("Regime OK")
        if atr_ok:
            momentum_score += 2
            criteria_met.append(f"ATR {atr_percent:.1f}%")
        if fresh_breakout:
            momentum_score += 5
            criteria_met.append("Fresh Breakout")
        elif near_breakout:
            momentum_score += 3
            criteria_met.append(f"Near 52W ({((current_price/high_52w_current)-1)*100:.1f}%)")
        if current_volume > VOLUME_MULT_BREAKOUT * vol_avg50:
            momentum_score += 1
            criteria_met.append(f"Vol {current_volume/vol_avg50:.1f}x")

        return {
            'ticker': ticker.replace('.NS', ''),
            'full_ticker': ticker,
            'current_price': current_price,
            'sma50': current_sma50,
            'sma200': current_sma200,
            'sma_50_6w_ago': sma50_6w_ago,
            'trail_ema': current_trail_ema,
            'atr': current_atr,
            'atr_percent': atr_percent,
            'high_52w': high_52w_current,
            'vol_avg50': vol_avg50,
            'vol_avg20': vol_avg20,
            'current_volume': current_volume,
            'traded_value': traded_value,
            'pattern': pattern,
            'days_since_breakout': days_since_breakout,
            'momentum_score': momentum_score,
            'max_score': 11,
            'criteria_met': criteria_met,
            'regime_ok': regime_ok,
            'atr_ok': atr_ok,
            'fresh_breakout': fresh_breakout,
            'near_breakout': near_breakout,
            'weak_setup': weak_setup,
            'sector': stock_info['sector'],
            'cap': stock_info['cap'],
            'low': low.iloc[-1],
            'near_pct': ((current_price / high_52w_current) - 1) * 100,
            # BUY/SELL TIMING PREDICTIONS
            'stop_loss': stop_loss,
            'target1': target1_price,
            'target2': target2_price,
            'risk_per_share': risk_per_share,
            'rr_ratio': rr_ratio,
            'rr_ratio_2': rr_ratio_2,
            'entry_type': entry_type,
            'entry_window': entry_window,
            'pullback_entry': pullback_entry,
            'entry_confidence': entry_confidence,
            'sell_signal': sell_signal,
            'exit_priority': exit_priority,
            'optimal_entry': optimal_entry,
            'buy_zone_low': buy_zone_low,
            'buy_zone_high': buy_zone_high,
            'gtt_target1': gtt_target1,
            'gtt_target2': gtt_target2,
            'uptrend': uptrend,
            'golden_cross': golden_cross,
            'base_rising': base_rising
        }
    except Exception as e:
        return None


def get_fundamental_data(ticker):
    """Get fundamental data for small cap stocks"""
    try:
        stock = yf.Ticker(ticker)

        # Get both info and history
        info = stock.info
        hist = stock.history(period="1y")

        if hist is None or hist.empty:
            return None

        close = hist['Close']
        high = hist['High']
        volume = hist['Volume']

        current_price = close.iloc[-1]
        current_volume = volume.iloc[-1]

        # Fundamental metrics from yfinance
        pe_ratio = info.get('forwardPE') or info.get('trailingPE') or 0
        roe = info.get('returnOnEquity') or 0
        de_ratio = info.get('debtToEquity') or 0
        market_cap = info.get('marketCap') or 0
        revenue = info.get('totalRevenue') or 0
        profit_margin = info.get('profitMargin') or 0
        fcf = info.get('freeCashflow') or 0
        promoter_holding = info.get('heldPercentInstitutions') or 0  # Institutional = proxy for quality

        # Handle None values
        if pe_ratio is None or pe_ratio <= 0:
            pe_ratio = 999
        if de_ratio is None or de_ratio < 0:
            de_ratio = 999
        if roe is None:
            roe = 0
        if profit_margin is None:
            profit_margin = 0

        # Calculate ROE percentage
        roe_pct = roe * 100 if roe else 0
        profit_margin_pct = profit_margin * 100 if profit_margin else 0

        # Market cap in Cr
        mcap_cr = market_cap / 10000000 if market_cap else 0

        # Price metrics
        sma50 = calculate_sma(close, 50)
        sma200 = calculate_sma(close, 200)
        current_sma50 = sma50.iloc[-1] if len(sma50) >= 50 else current_price
        current_sma200 = sma200.iloc[-1] if len(sma200) >= 200 else current_price

        # ATR
        atr = calculate_atr(hist, 14)
        current_atr = atr.iloc[-1] if len(atr) >= 14 else 0
        atr_percent = (current_atr / current_price * 100) if current_price > 0 else 0

        # 52W high
        high_52w = high.rolling(window=260).max().iloc[-1] if len(high) >= 260 else high.max()

        # Volume avg
        vol_avg50 = volume.rolling(50).mean().iloc[-1] if len(volume) >= 50 else volume.mean()
        traded_value = current_volume * current_price

        # Trend analysis
        above_sma50 = current_price > current_sma50
        above_sma200 = current_price > current_sma200
        golden_cross = current_sma50 > current_sma200

        # Price near 52W high
        near_52w_pct = ((current_price / high_52w) - 1) * 100

        # Technical score
        tech_score = 0
        if above_sma50: tech_score += 1
        if above_sma200: tech_score += 1
        if golden_cross: tech_score += 1

        # Fundamental score (out of 10)
        fund_score = 0
        fund_criteria = []

        # P/E scoring (lower is better, capped at 30)
        if 0 < pe_ratio <= 15:
            fund_score += 3
            fund_criteria.append(f"P/E: {pe_ratio:.1f} (Cheap)")
        elif 15 < pe_ratio <= 25:
            fund_score += 2
            fund_criteria.append(f"P/E: {pe_ratio:.1f} (Fair)")
        elif 25 < pe_ratio <= 35:
            fund_score += 1
            fund_criteria.append(f"P/E: {pe_ratio:.1f} (Expensive)")

        # ROE scoring (higher is better)
        if roe_pct >= 20:
            fund_score += 3
            fund_criteria.append(f"ROE: {roe_pct:.1f}% (Excellent)")
        elif roe_pct >= 15:
            fund_score += 2
            fund_criteria.append(f"ROE: {roe_pct:.1f}% (Good)")
        elif roe_pct >= 10:
            fund_score += 1
            fund_criteria.append(f"ROE: {roe_pct:.1f}% (Average)")

        # Debt/Equity scoring (lower is better)
        if 0 <= de_ratio <= 0.5:
            fund_score += 2
            fund_criteria.append(f"D/E: {de_ratio:.1f} (Low Debt)")
        elif de_ratio <= 1.0:
            fund_score += 1
            fund_criteria.append(f"D/E: {de_ratio:.1f} (Moderate)")

        # Profit margin scoring
        if profit_margin_pct >= 15:
            fund_score += 2
            fund_criteria.append(f"Margin: {profit_margin_pct:.1f}% (High)")
        elif profit_margin_pct >= 5:
            fund_score += 1
            fund_criteria.append(f"Margin: {profit_margin_pct:.1f}% (Ok)")

        # Market cap category
        if mcap_cr >= 20000:
            cap_cat = "Large Cap"
        elif mcap_cr >= 5000:
            cap_cat = "Mid Cap"
        else:
            cap_cat = "Small Cap"

        stock_info = NIFTY200_STOCKS.get(ticker, {"sector": "Other", "cap": cap_cat})

        # Combined score
        combined_score = fund_score + tech_score

        return {
            'ticker': ticker.replace('.NS', ''),
            'full_ticker': ticker,
            'current_price': current_price,
            'pe_ratio': pe_ratio,
            'roe_pct': roe_pct,
            'de_ratio': de_ratio,
            'market_cap': market_cap,
            'mcap_cr': mcap_cr,
            'profit_margin_pct': profit_margin_pct,
            'revenue_cr': revenue / 10000000 if revenue else 0,
            'sma50': current_sma50,
            'sma200': current_sma200,
            'atr_percent': atr_percent,
            'high_52w': high_52w,
            'near_52w_pct': near_52w_pct,
            'traded_value': traded_value,
            'above_sma50': above_sma50,
            'above_sma200': above_sma200,
            'golden_cross': golden_cross,
            'tech_score': tech_score,
            'fund_score': fund_score,
            'combined_score': combined_score,
            'max_fund_score': 10,
            'fund_criteria': fund_criteria,
            'sector': info.get('sector', 'Other') or stock_info.get('sector', 'Other'),
            'cap': cap_cat,
            'promoter_holding': promoter_holding * 100 if promoter_holding else 0
        }
    except Exception as e:
        return None


def create_momentum_chart(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        if hist is None or hist.empty:
            return None

        close = hist['Close']
        high = hist['High']

        sma50 = calculate_sma(close, 50)
        sma200 = calculate_sma(close, 200)
        ema10 = calculate_ema(close, 10)
        high_52w = high.rolling(260).max()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=close, name='Price', line=dict(color='white', width=2)))
        fig.add_trace(go.Scatter(x=hist.index, y=sma50, name='SMA 50', line=dict(color='blue', width=1.5)))
        fig.add_trace(go.Scatter(x=hist.index, y=sma200, name='SMA 200', line=dict(color='orange', width=1.5)))
        fig.add_trace(go.Scatter(x=hist.index, y=ema10, name='EMA 10', line=dict(color='purple', width=1, dash='dash')))
        fig.add_trace(go.Scatter(x=hist.index, y=high_52w, name='52W High', line=dict(color='green', width=1, dash='dot')))

        fig.update_layout(
            title=f'{ticker.replace(".NS", "")} - Nifty 200 Momentum',
            template='plotly_dark',
            height=400,
            xaxis_title='Date',
            yaxis_title='Price'
        )
        return fig
    except:
        return None


# Page Config
st.title("🎯 Nifty 200 Momentum 30 - Swing Trading")
st.markdown("*Based on: Investors Way Swing Trading Framework - Strategy 1*")

# Sidebar
st.sidebar.title("📊 Screener Options")
screener_mode = st.sidebar.radio(
    "Select Screener",
    ["📈 Momentum (N200)", "💎 Fundamental Small Cap", "🔥 Combined View"],
    index=0
)

# Momentum Filters
cap_filter = st.sidebar.multiselect(
    "Cap Type",
    ["Large Cap", "Mid Cap", "Small Cap"],
    default=["Large Cap", "Mid Cap", "Small Cap"]
)

sector_filter = st.sidebar.multiselect(
    "Sector",
    ["Finance", "IT", "FMCG", "Pharma", "Energy", "Metals", "Cement", "Auto", "Consumer", "Power", "Infrastructure", "Realty", "Retail", "Chemicals", "Logistics", "Healthcare", "Textiles", "Fertilizers", "Aviation", "Capital Goods", "Media", "Other"],
    default=["Finance", "IT", "FMCG", "Pharma", "Energy", "Metals", "Cement", "Auto", "Consumer", "Power", "Infrastructure", "Realty", "Retail", "Chemicals", "Logistics", "Healthcare", "Textiles", "Fertilizers", "Aviation", "Capital Goods", "Media", "Other"]
)

st.sidebar.markdown("### 🎯 Signal Type")
signal_filter = st.sidebar.multiselect(
    "Signal Type",
    ["BREAKOUT", "NEAR BREAKOUT"],
    default=["BREAKOUT", "NEAR BREAKOUT"]
)

st.sidebar.markdown("### ⚠️ Filters")
exclude_weak = st.sidebar.checkbox("Exclude Weak Setups", value=False, help="Remove stocks with false breakouts or multiple rejections")

st.sidebar.markdown("### 💰 Liquidity")
min_value = st.sidebar.number_input("Min Traded Value (₹M)", value=20, step=5)

# Fundamental Filters (for Small Cap mode)
st.sidebar.markdown("### 📊 Fundamental Filters")
fund_min_pe = st.sidebar.number_input("Max P/E Ratio", value=25, step=5)
fund_min_roe = st.sidebar.slider("Min ROE %", 0, 50, 15)
fund_max_de = st.sidebar.slider("Max Debt/Equity", 0.0, 2.0, 0.5, step=0.1)
fund_min_mcap = st.sidebar.selectbox("Min Market Cap", ["Any", "₹100Cr", "₹500Cr", "₹1000Cr"], index=2)

auto_refresh = st.sidebar.checkbox("Auto-refresh (60s)", value=False)

# Main Content
st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

progress_bar = st.progress(0)
status_text = st.empty()

# Determine which stocks to scan based on mode
if screener_mode == "📈 Momentum (N200)":
    scan_tickers = NSE_TICKERS
    mode_desc = f"Nifty 200 ({len(NSE_TICKERS)} stocks)"
elif screener_mode == "💎 Fundamental Small Cap":
    scan_tickers = list(SMALL_CAP_STOCKS.keys())
    mode_desc = f"Small Cap ({len(SMALL_CAP_STOCKS)} stocks)"
else:
    scan_tickers = ALL_TICKERS
    mode_desc = f"All Stocks ({len(ALL_TICKERS)} stocks)"

# Scan stocks
results_momentum = []
results_fundamental = []
total = len(scan_tickers)

status_text.text(f"Scanning {mode_desc}...")

for i, ticker in enumerate(scan_tickers):
    progress_bar.progress((i + 1) / total)

    if screener_mode in ["📈 Momentum (N200)", "🔥 Combined View"]:
        data = get_momentum_data(ticker)
        if data:
            results_momentum.append(data)

    if screener_mode in ["💎 Fundamental Small Cap", "🔥 Combined View"]:
        fund_data = get_fundamental_data(ticker)
        if fund_data:
            results_fundamental.append(fund_data)

progress_bar.empty()
status_text.empty()

# Process based on mode
if screener_mode == "📈 Momentum (N200)":
    results = results_momentum
elif screener_mode == "💎 Fundamental Small Cap":
    results = results_fundamental
else:
    # Combined View: merge both results
    # Add momentum data to fundamental results
    combined_results = []
    fund_dict = {r['ticker']: r for r in results_fundamental}

    for r in results_momentum:
        fund_data = fund_dict.get(r['ticker'])
        if fund_data:
            # Merge fundamental data into momentum result
            r_copy = r.copy()
            r_copy['pe_ratio'] = fund_data.get('pe_ratio', 0)
            r_copy['roe_pct'] = fund_data.get('roe_pct', 0)
            r_copy['de_ratio'] = fund_data.get('de_ratio', 0)
            r_copy['mcap_cr'] = fund_data.get('mcap_cr', 0)
            combined_results.append(r_copy)
        else:
            combined_results.append(r)

    results = combined_results

# Apply momentum filters
filtered = []
for r in results:
    if screener_mode in ["📈 Momentum (N200)", "🔥 Combined View"]:
        if r['cap'] not in cap_filter:
            continue
        if r['sector'] not in sector_filter:
            continue
        if r['traded_value'] <= min_value * 1000000:
            continue
        if r['pattern'] not in signal_filter:
            continue
        if exclude_weak and r.get('weak_setup', False):
            continue
        if not r['regime_ok']:
            continue
        if not r['atr_ok']:
            continue
    elif screener_mode == "💎 Fundamental Small Cap":
        # Apply fundamental filters
        if r['cap'] not in ["Small Cap", "Mid Cap"]:
            continue
        if r['pe_ratio'] > fund_min_pe:
            continue
        if r['roe_pct'] < fund_min_roe:
            continue
        if r['de_ratio'] > fund_max_de:
            continue
        if fund_min_mcap != "Any":
            min_mcap = float(fund_min_mcap.replace("₹", "").replace("Cr", "").strip())
            if r['mcap_cr'] < min_mcap:
                continue

    filtered.append(r)

# Sort based on mode
if screener_mode == "💎 Fundamental Small Cap":
    filtered.sort(key=lambda x: x['combined_score'], reverse=True)
else:
    filtered.sort(key=lambda x: x['momentum_score'], reverse=True)

st.markdown("---")

# Mode-specific headers
if screener_mode == "💎 Fundamental Small Cap":
    st.subheader(f"✅ Fundamental Small Cap: {len(filtered)} stocks")
elif screener_mode == "🔥 Combined View":
    st.subheader(f"✅ Combined Results: {len(filtered)} stocks")
else:
    st.subheader(f"✅ Momentum Results: {len(filtered)} stocks")

# Summary Stats (only for momentum modes)
if screener_mode != "💎 Fundamental Small Cap":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Fresh Breakouts", sum(1 for r in filtered if r['pattern'] == "BREAKOUT"))
    with col2:
        st.metric("Near Breakouts", sum(1 for r in filtered if r['pattern'] == "NEAR BREAKOUT"))
    with col3:
        st.metric("Avg Score", f"{sum(r['momentum_score'] for r in filtered)/len(filtered):.1f}")
    with col4:
        st.metric("High Score", max(r['momentum_score'] for r in filtered))

if filtered:
    st.markdown("### 📋 Results Table")
    df_data = [{'Rank': i+1, 'Ticker': r['ticker'], 'Price': f"₹{r['current_price']:.2f}", 'Score': f"{r['momentum_score']}/{r['max_score']}", 'Buy Zone': f"₹{r['buy_zone_low']:.0f}-{r['buy_zone_high']:.0f}", 'Stop': f"₹{r['stop_loss']:.2f}", 'T1': f"₹{r['target1']:.2f}", 'T2': f"₹{r['target2']:.2f}", 'R:R': f"{r['rr_ratio']:.1f}:1"} for i, r in enumerate(filtered)]
    st.dataframe(pd.DataFrame(df_data), width='stretch', height=350)

# Top Picks with Buy/Sell Info
st.markdown("---")
if screener_mode == "💎 Fundamental Small Cap":
    st.subheader("🏆 Top Fundamental Picks")
else:
    st.subheader("🏆 Top Momentum Picks")

cols = st.columns(min(5, len(filtered)))
for i, r in enumerate(filtered[:5]):
    with cols[i]:
        if screener_mode == "💎 Fundamental Small Cap":
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1A1A4A 0%, #2D2D5A 100%); padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #FFD700;">
                <h3 style="color: #FFD700; margin: 0;">💎 {r['ticker']}</h3>
                <p style="color: #aaa; font-size: 11px;">{r['sector']}</p>
                <h2 style="color: #fff; margin: 5px 0;">₹{r['current_price']:.2f}</h2>
                <hr style="border-color: #333;">
                <p style="color: #00FF00; font-size: 11px;">P/E: {r['pe_ratio']:.1f} | ROE: {r['roe_pct']:.1f}%</p>
                <p style="color: #aaa; font-size: 10px;">D/E: {r['de_ratio']:.1f} | MCap: ₹{r['mcap_cr']:.0f}Cr</p>
                <p style="color: #FFD700; font-size: 12px;">Score: {r['combined_score']}/{r['max_fund_score']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            emoji = "📈" if r.get('pattern') == "BREAKOUT" else "🔄"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0D3622 0%, #1B4332 100%); padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #00FF00;">
                <h3 style="color: #00FF00; margin: 0;">{emoji} {r['ticker']}</h3>
                <p style="color: #aaa; font-size: 11px;">{r['sector']}</p>
                <h2 style="color: #fff; margin: 5px 0;">₹{r['current_price']:.2f}</h2>
                <p style="color: #00FF00; font-size: 12px; font-weight: bold;">{r.get('pattern', 'N/A')}</p>
                <hr style="border-color: #333;">
                <p style="color: #FFD700; font-size: 14px; font-weight: bold;">Score: {r['momentum_score']}/{r['max_score']}</p>
                <p style="color: #00FF00; font-size: 11px;">Buy Zone: ₹{r['buy_zone_low']:.0f}-{r['buy_zone_high']:.0f}</p>
                <p style="color: #FF4444; font-size: 10px;">Stop: ₹{r['stop_loss']:.2f}</p>
                <p style="color: #aaa; font-size: 10px;">T1: ₹{r['target1']:.2f} | T2: ₹{r['target2']:.2f}</p>
                <p style="color: #00BFFF; font-size: 10px;">R:R = {r['rr_ratio']:.1f}:1</p>
            </div>
            """, unsafe_allow_html=True)

# Detailed Analysis - OUTSIDE the cards loop
if filtered:
    st.markdown("---")
    if screener_mode == "💎 Fundamental Small Cap":
        st.subheader("📊 Detailed Fundamental Analysis")
    else:
        st.subheader("📊 Detailed Momentum Analysis")

    for i, r in enumerate(filtered[:5], 1):
            if screener_mode == "💎 Fundamental Small Cap":
                with st.expander(f"#{i} {r['ticker']} | Score: {r['combined_score']}/{r['max_fund_score']}", expanded=False):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Price", f"₹{r['current_price']:.2f}")
                    c2.metric("P/E", f"{r['pe_ratio']:.1f}")
                    c3.metric("ROE", f"{r['roe_pct']:.1f}%")
                    c4.metric("D/E", f"{r['de_ratio']:.1f}")

                    c5, c6, c7, c8 = st.columns(4)
                    c5.metric("Market Cap", f"₹{r['mcap_cr']:.0f}Cr")
                    c6.metric("Revenue", f"₹{r['revenue_cr']:.0f}Cr" if r['revenue_cr'] > 0 else "N/A")
                    c7.metric("Margin", f"{r['profit_margin_pct']:.1f}%")
                    c8.metric("Near 52W", f"{r['near_52w_pct']:.1f}%")

                    st.markdown("---")
                    st.markdown(f"**Fundamental Criteria:** {', '.join(r['fund_criteria']) if r['fund_criteria'] else 'Basic fundamentals'}")

                    st.markdown(f"""
                    **Technical Setup:**
                    - Above SMA50: **{'✅' if r['above_sma50'] else '❌'}**
                    - Above SMA200: **{'✅' if r['above_sma200'] else '❌'}**
                    - Golden Cross: **{'✅' if r['golden_cross'] else '❌'}**
                    """)
            else:
                with st.expander(f"#{i} {r['ticker']} - {r.get('pattern', 'N/A')} | Score: {r['momentum_score']}/{r['max_score']}", expanded=False):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Price", f"₹{r['current_price']:.2f}")
                    c2.metric("52W High", f"₹{r['high_52w']:.2f}", f"{r['near_pct']:.1f}%")
                    c3.metric("ATR%", f"{r['atr_percent']:.2f}%")
                    c4.metric("Trail EMA", f"₹{r['trail_ema']:.2f}")

                    st.markdown("---")
                    st.markdown("### 🎯 BUY/SELL TIMING PREDICTIONS")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1B4332 0%, #0D3622 100%); padding: 15px; border-radius: 10px; border: 1px solid #00FF00;">
                            <h4 style="color: #00FF00;">📥 BUY TIMING</h4>
                            <hr style="border-color: #333;">
                            <p style="color: #fff;"><b>Entry Type:</b> {r.get('entry_type', 'N/A')}</p>
                            <p style="color: #FFD700;"><b>Recommendation:</b> {r.get('entry_window', 'N/A')}</p>
                            <p style="color: #aaa;"><b>Confidence:</b> {r.get('entry_confidence', 'N/A')}</p>
                            <p style="color: #aaa;"><b>Buy Zone:</b> ₹{r['buy_zone_low']:.2f} - ₹{r['buy_zone_high']:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #4A1A1A 0%, #2D0D0D 100%); padding: 15px; border-radius: 10px; border: 1px solid #FF4444;">
                            <h4 style="color: #FF4444;">📤 SELL TIMING</h4>
                            <hr style="border-color: #333;">
                            <p style="color: #fff;"><b>Signal:</b> {r.get('sell_signal', 'N/A')}</p>
                            <p style="color: #FFD700;"><b>Priority:</b> {r.get('exit_priority', 'N/A')}</p>
                            <p style="color: #aaa;"><b>Stop Loss:</b> ₹{r['stop_loss']:.2f}</p>
                            <p style="color: #aaa;"><b>Risk/Share:</b> ₹{r.get('risk_per_share', 0):.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        pattern = r.get('pattern', 'N/A')
                        if pattern == "NEAR BREAKOUT":
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #1A1A4A 0%, #0D0D2D 100%); padding: 15px; border-radius: 10px; border: 1px solid #00BFFF;">
                                <h4 style="color: #00BFFF;">🎯 GTT TARGETS</h4>
                                <hr style="border-color: #333;">
                                <p style="color: #fff;"><b>GTT Price:</b> ₹{r['high_52w']:.2f}</p>
                                <p style="color: #00FF00;"><b>Target 1:</b> ₹{r.get('gtt_target1', r['target1']):.2f}</p>
                                <p style="color: #00FF00;"><b>Target 2:</b> ₹{r.get('gtt_target2', r['target2']):.2f}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #1A1A4A 0%, #0D0D2D 100%); padding: 15px; border-radius: 10px; border: 1px solid #00BFFF;">
                                <h4 style="color: #00BFFF;">🎯 TARGETS</h4>
                                <hr style="border-color: #333;">
                                <p style="color: #fff;"><b>Target 1:</b> ₹{r['target1']:.2f}</p>
                                <p style="color: #00FF00;"><b>Target 2:</b> ₹{r['target2']:.2f}</p>
                                <p style="color: #FFD700;"><b>R:R:</b> {r['rr_ratio']:.1f}:1</p>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown("---")
                    st.markdown(f"**📋 Setup Criteria:** {', '.join(r.get('criteria_met', ['N/A']))}")

                    st.markdown(f"""
                    **Market Regime:**
                    - Uptrend: **{'✅' if r.get('uptrend') else '❌'}**
                    - Golden Cross: **{'✅' if r.get('golden_cross') else '❌'}**
                    - ATR OK: **{'✅' if r.get('atr_ok') else '❌'}** ({r['atr_percent']:.2f}%)
                    """)

else:
    st.warning("⚠️ No stocks match criteria. Try adjusting filters.")

st.markdown("---")
st.markdown("""
<small>
📋 **Nifty 200 Momentum 30 - Strategy Rules:**

**Layer 1 - Market Regime:**
- Uptrend: Close > SMA50 AND Close > SMA200
- Golden Cross: SMA50 > SMA200
- Base Rising: SMA50 > 6 weeks ago SMA50

**Layer 2 - Volatility Filter:**
- ATR: 1.5% - 5% of price

**Layer 3 - Signal Detection:**
- Fresh Breakout: Close > 52W High AND Yesterday Close < Yesterday 52W High AND Volume > 2x avg50
- Near Breakout: Within 3% of 52W High AND Volume < avg20 (consolidating)

**Exit Rules:**
- Trail Stop: 2 consecutive closes below 10-EMA
- Time Stop: 15 trading days

⚠️ <b>Disclaimer:</b> For educational purposes only. Not financial advice.
</small>
""", unsafe_allow_html=True)

if auto_refresh:
    time.sleep(60)
    st.rerun()