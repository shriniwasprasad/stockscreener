# Indian Stock Screener Pro

A real-time stock screening application for Indian NSE stocks with technical analysis, buy/sell recommendations, and interactive charts.

## 📊 Project Overview

This application helps investors and traders identify potential stock picks based on:

- **Fundamental Filters**: P/E Ratio, Market Cap classification
- **Technical Indicators**: RSI, MACD, Moving Averages (SMA 20, 50, 200)
- **Volume Analysis**: Volume spikes relative to 20-day average
- **Expert Recommendations**: Score-based buy/sell signals with target and stop-loss

### Features

- ✅ Real-time data from NSE (India) via yfinance
- ✅ 200+ stocks including Large Cap, Mid Cap, and Small Cap
- ✅ Sector-wise filtering (Finance, IT, FMCG, Pharma, etc.)
- ✅ Interactive charts (Candlestick, MACD, RSI, SMA)
- ✅ Configurable target % and stop-loss %
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

## 🖥️ Starting and Stopping the Server

### Start the Server

**Windows (PowerShell):**
```powershell
# Navigate to project folder
cd D:\inter\new_learning\python\stockscreener

# Activate virtual environment
.venv\Scripts\activate

# Run the application
streamlit run app.py --server.port 8501

# Or run without activating (using full path)
.venv\Scripts\streamlit.exe run app.py --server.port 8501
```

**Windows (Command Prompt):**
```cmd
cd D:\inter\new_learning\python\stockscreener
.venv\Scripts\activate.bat
streamlit run app.py --server.port 8501
```

**Mac/Linux:**
```bash
cd /path/to/stockscreener
source .venv/bin/activate
streamlit run app.py --server.port 8501
```

### Stop the Server

The server runs in your terminal. To stop it:

1. **Press `Ctrl + C`** in the terminal window where the server is running

2. **Or close the terminal** - this will stop the server

3. **Or kill the process manually**:

**Windows (PowerShell):**
```powershell
# Kill all Python processes (be careful!)
Get-Process -Name python | Stop-Process -Force

# Or kill specific Streamlit process
Get-Process | Where-Object { $_.CommandLine -like "*streamlit*" } | Stop-Process -Force
```

**Windows (Command Prompt):**
```cmd
taskkill /F /IM python.exe
```

**Mac/Linux:**
```bash
pkill -f "streamlit run"
# or
killall python
```

### Verify Server Status

After starting, you should see:
```
Uvicorn server started on 0.0.0.0:8501

You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.1.100:8501
```

## 🧹 Clearing Cache

### Why Clear Cache?

If you encounter issues like:
- Stale stock data
- Old filter settings not updating
- Charts not loading properly

### Method 1: Streamlit Clear Cache (In-App)

Streamlit caches some data automatically. To force a fresh scan:

1. Click the **three dots (⋮)** in the top-right corner of the Streamlit app
2. Click **"Clear cache"** (if available)
3. Or simply press `Ctrl + R` (Windows) / `Cmd + R` (Mac) to hard refresh your browser

### Method 2: Restart the Server

```bash
# Stop the current server (Ctrl + C)
# Then restart:

streamlit run app.py --server.port 8501
```

### Method 3: Clear Python Cache Files

**Windows (PowerShell):**
```powershell
# Remove __pycache__ directories
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Remove .pyc files
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
```

**Mac/Linux:**
```bash
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete
```

### Method 4: Clear yfinance Data Cache

yfinance stores temporary data in different locations:

**Windows (PowerShell):**
```powershell
# Method 1: Clear Temp folder yfinance cache
Remove-Item -Path "$env:LOCALAPPDATA\Temp\yfinance" -Recurse -Force -ErrorAction SilentlyContinue

# Method 2: Clear yfinance cache in AppData
$yfCache = "$env:LOCALAPPDATA\Packages\PythonSoftwareFoundation.Python*"
Get-ChildItem -Path $yfCache -Recurse -Directory -Filter "yfinance" -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

# Method 3: Clear all Python cached packages
Remove-Item -Path "$env:LOCALAPPDATA\pip\cache" -Recurse -Force -ErrorAction SilentlyContinue
```

**Windows (Command Prompt):**
```cmd
:: Clear yfinance temp cache
del /s /q "%LOCALAPPDATA%\Temp\yfinance*" 2>nul

:: Clear pip cache
del /s /q "%LOCALAPPDATA%\pip\cache" 2>nul
```

**Mac/Linux:**
```bash
# Remove yfinance cache
rm -rf ~/Library/Caches/yfinance/

# Also clear pip cache
rm -rf ~/.cache/pip/
```

### Method 5: Fresh Start (Complete Reset)

**Windows (PowerShell):**
```powershell
# 1. Stop the server (Ctrl + C)

# 2. Delete cache folders
Remove-Item -Path ".streamlit" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Filter "*.pyc" -Recurse | Remove-Item -Force

# 3. Clear Streamlit config cache
Remove-Item -Path "$env:APPDATA\Streamlit\config.toml" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:APPDATA\Streamlit\credentials.toml" -Force -ErrorAction SilentlyContinue

# 4. Restart the server
streamlit run app.py --server.port 8501
```

**Mac/Linux:**
```bash
# 1. Stop the server (Ctrl + C)

# 2. Delete cache folders
rm -rf .streamlit/
rm -rf __pycache__/
rm -rf ~/.cache/streamlit/

# 3. Restart the server
streamlit run app.py --server.port 8501
```

### Quick Cache Clear Script (Windows)

Create a file `clear_cache.ps1` and run it:

```powershell
# clear_cache.ps1
Write-Host "Clearing caches..." -ForegroundColor Yellow

# Clear Python cache
Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

# Clear Streamlit cache
Remove-Item -Path ".streamlit" -Recurse -Force -ErrorAction SilentlyContinue

# Clear pip cache
Remove-Item -Path "$env:LOCALAPPDATA\pip\cache" -Recurse -Force -ErrorAction SilentlyContinue

# Clear yfinance temp
Remove-Item -Path "$env:LOCALAPPDATA\Temp\yfinance*" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Cache cleared!" -ForegroundColor Green
```

Run with:
```powershell
powershell -ExecutionPolicy Bypass -File clear_cache.ps1
```

## 📱 How to Use

### 1. Select Filters (Sidebar)
- **Cap Type**: Large Cap / Mid Cap / Small Cap
- **Sector**: Choose industries (Finance, IT, Pharma, etc.)
- **Technical Filters**: Adjust P/E, RSI, Volume thresholds
- **Target/Stop Loss**: Set your risk parameters

### 2. Scan Stocks
- Adjust the "Stocks to Scan" slider (50-500)
- Click anywhere on the page to trigger a rescan
- Enable auto-refresh for continuous monitoring

### 3. Review Results
- **Filtered Results Table**: Shows all matching stocks
- **Top 5 Expert Picks**: Highlighted buy recommendations
- **Detailed Analysis**: Expand any stock for charts

### 4. Analyze Charts
- **Price + SMA**: Price movement with 20 & 50 day moving averages
- **MACD**: Trend momentum indicator
- **RSI**: Overbought/oversold signals

## 📸 Sample Data

### Main Dashboard
```
Rank | Ticker | Sector     | Cap      | Price  | P/E  | Vol   | RSI | MACD | Score | Rec
-----|--------|------------|----------|--------|------|-------|-----|------|-------|-------------
1    | COFORGE| IT         | Large Cap| ₹1,368 | 20.7 | 2.24x | 58  | 🟢   | 8     | STRONG BUY
2    | ACC    | Cement     | Mid Cap  | ₹1,392 | 11.7 | 2.15x | 39  | 🟢   | 8     | STRONG BUY
3    | HDFCBANK| Finance   | Large Cap| ₹781   | 12.4 | 1.04x | 44  | 🟢   | 6     | STRONG BUY
4    | COALINDIA| Metals   | Large Cap| ₹456   | 7.9  | 1.22x | 60  | 🟢   | 6     | STRONG BUY
5    | BRITANNIA| FMCG     | Large Cap| ₹5,520 | 40.9 | 5.76x | 41  | 🔴   | 6     | STRONG BUY
```

### Technical Indicators Included
- **RSI (14)**: Relative Strength Index
- **MACD**: Moving Average Convergence Divergence
- **SMA 20/50/200**: Simple Moving Averages
- **Volume Ratio**: Current volume vs 20-day average
- **52-Week Range**: Low and High prices

### Recommendation System
- **STRONG BUY**: Score 7+ (Strong fundamentals + bullish technicals)
- **BUY**: Score 5-6 (Good opportunity)
- **HOLD**: Score 3-4 (Neutral)
- **WAIT**: Score <3 (Not recommended)

## 📁 Project Structure

```
stockscreener/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── CLAUDE.md           # AI project notes
├── README.md           # Project documentation
├── .gitignore          # Git ignore rules
└── test_yfinance.py    # Test script for API
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