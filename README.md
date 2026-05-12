# Indian Stock Screener Pro

A real-time stock screening application for Indian NSE stocks with two powerful screening modes: **Classic Screener** and **Momentum Screener**.

## 📊 Project Overview

This application helps investors and traders identify potential stock picks using two different strategies:

### 🎯 Mode 1: Classic Screener
- **Fundamental Filters**: P/E Ratio, Market Cap classification
- **Technical Indicators**: RSI, MACD, Moving Averages (SMA 20, 50, 200)
- **Volume Analysis**: Volume spikes relative to 20-day average
- **Expert Recommendations**: Score-based buy/sell signals with target and stop-loss

### 📈 Mode 2: Momentum Screener (Nifty 200 Momentum 30)
Based on **Investors Way Swing Trading Framework - Strategy 1**

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

### Features

- ✅ **Dual Mode Screener**: Switch between Classic and Momentum modes
- ✅ Real-time data from NSE (India) via yfinance
- ✅ 200+ stocks including Large Cap, Mid Cap, and Small Cap
- ✅ Sector-wise filtering (Finance, IT, FMCG, Pharma, etc.)
- ✅ Interactive charts (Price+SMA, MACD, RSI)
- ✅ Buy/Sell timing predictions with targets and stop-loss
- ✅ GTT (Good Till Trigger) target calculations for near breakout stocks
- ✅ Auto-refresh capability
- ✅ Professional UI with color-coded recommendations

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.12 |
| **Data Source** | yfinance |
| **UI Framework** | Streamlit |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly |
| **Deployment** | Local (Streamlit) |

## 🚀 Steps to Run Locally

### Prerequisites

- Python 3.8 or higher
- Windows/Mac/Linux

### 1. Clone the Repository

```bash
git clone <repository-url>
cd stockscreener
```

### 2. Create Virtual Environment

**Windows (PowerShell/Command Prompt):**
```powershell
# Create virtual environment
python -m venv .venv

# Activate (PowerShell)
.venv\Scripts\Activate

# Activate (Command Prompt)
.venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py --server.port 8501
```

### 5. Access the App

Open your browser and navigate to:
- **Local**: http://localhost:8501
- **Network**: http://192.168.1.100:8501

## 🖥️ How to Use

### Selecting Screener Mode

Use the sidebar radio button to switch between:
- **📊 Classic Screener**: RSI/MACD/SMA filters, score-based ranking
- **🎯 Momentum Screener**: Nifty 200 Momentum 30 breakout strategy

### Classic Screener Mode

1. **Select Filters** (Sidebar)
   - **Cap Type**: Large Cap / Mid Cap / Small Cap
   - **Sector**: Choose industries (Finance, IT, Pharma, etc.)
   - **Technical Filters**: Adjust P/E, RSI, Volume thresholds
   - **Target/Stop Loss**: Set your risk parameters

2. **Review Results**
   - Filtered Results Table with all matching stocks
   - Top 5 Expert Picks with buy recommendations
   - Detailed Analysis with interactive charts

3. **Analyze Charts**
   - Price + SMA: Price movement with 20 & 50 day moving averages
   - MACD: Trend momentum indicator
   - RSI: Overbought/oversold signals

### Momentum Screener Mode

1. **Select Signal Type**
   - **BREAKOUT**: Fresh 52-week high breakouts
   - **NEAR BREAKOUT**: Stocks within 3% of 52-week high

2. **Review Results**
   - Results Table with Buy Zone, Stop Loss, Targets, R:R
   - Top Momentum Picks cards
   - Detailed Buy/Sell Timing Analysis

3. **Detailed Analysis** (Expand each stock)
   - **📥 BUY TIMING**: Entry Type, Recommendation, Confidence, Buy Zone
   - **📤 SELL TIMING**: Signal, Priority, Stop Loss, Risk/Share
   - **🎯 TARGETS**: Target 1, Target 2, R:R Ratio
   - **GTT TARGETS** (for NEAR BREAKOUT): GTT Price, T1, T2

## 📸 Sample Data

### Classic Screener Results
```
Rank | Ticker | Sector    | Cap      | Price  | P/E  | Vol   | RSI | MACD | Score | Rec
-----|--------|-----------|----------|--------|------|-------|-----|------|-------|-------------
1    | COFORGE| IT        | Large Cap| ₹1,368 | 20.7 | 2.24x | 58  | 🟢   | 8     | STRONG BUY
2    | ACC    | Cement    | Mid Cap  | ₹1,392 | 11.7 | 2.15x | 39  | 🟢   | 8     | STRONG BUY
3    | HDFCBANK| Finance  | Large Cap| ₹781   | 12.4 | 1.04x | 44  | 🟢   | 6     | STRONG BUY
```

### Momentum Screener Results
```
Rank | Ticker | Signal        | Price  | Score | Buy Zone    | Stop   | T1     | T2     | R:R
-----|--------|---------------|--------|-------|-------------|--------|--------|--------|----
1    | RELIANCE| BREAKOUT    | ₹1,250 | 11/11 | 1250-1260   | ₹1,230 | ₹1,285 | ₹1,345 | 1.5:1
2    | TCS     | NEAR BREAKOUT| ₹3,800 | 8/11 | 3780-3820   | ₹3,720 | ₹3,890 | ₹4,050 | 1.5:1
```

### Recommendation System (Classic Mode)
- **STRONG BUY**: Score 7+ (Strong fundamentals + bullish technicals)
- **BUY**: Score 5-6 (Good opportunity)
- **HOLD**: Score 3-4 (Neutral)
- **WAIT**: Score <3 (Not recommended)

### Momentum Scoring System
- **Regime OK** (Uptrend + Golden Cross + Base Rising): +3 points
- **ATR OK** (1.5% - 5%): +2 points
- **Fresh Breakout**: +5 points
- **Near Breakout**: +3 points
- **Volume > 2x avg**: +1 point

## 📁 Project Structure

```
stockscreener/
├── app.py                   # Main Streamlit application (Unified)
├── swing_trade_screener.py  # Standalone momentum screener (legacy)
├── requirements.txt         # Python dependencies
├── CLAUDE.md               # AI project notes
├── README.md               # Project documentation
├── .gitignore              # Git ignore rules
├── nifty200_momentum.pine  # Pine Script reference
└── test_yfinance.py        # Test script for API
```

## 🧹 Clearing Cache

### Method 1: In-App
1. Click the three dots (⋮) in the top-right corner
2. Click "Clear cache"

### Method 2: Restart Server
```bash
# Stop the current server (Ctrl + C)
# Then restart:
streamlit run app.py --server.port 8501
```

### Method 3: Clear Python Cache
**Windows (PowerShell):**
```powershell
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
```

**Mac/Linux:**
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
```

## ⚠️ Disclaimer

This application is for **educational purposes only**. The stock recommendations are generated based on technical indicators and should not be considered as financial advice. Always do your own research before making investment decisions.

## 🔧 Configuration

### Change Port
```bash
streamlit run app.py --server.port 8080
```

### Enable Headless Mode
```bash
streamlit run app.py --server.headless true
```

### Disable Usage Stats
Create `.streamlit/config.toml`:
```toml
[browser]
gatherUsageStats = false
```

## 📝 License

MIT License - Feel free to use and modify for your needs.

---

**Happy Investing!** 📈
