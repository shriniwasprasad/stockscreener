# Stock Screener Project

## Project Overview
- **Project name**: Indian Stock Screener Pro
- **Type**: Real-time stock screening web application
- **Core functionality**: Fetch and filter NSE (India) stocks based on technical and fundamental criteria with expert recommendations
- **Target users**: Indian traders and investors looking for undervalued stocks with momentum

## Technical Stack
- **Language**: Python 3.12
- **Data Source**: yfinance library (NSE data)
- **UI Framework**: Streamlit
- **Data Processing**: pandas, numpy
- **Visualization**: Plotly (interactive charts)

## Core Features
1. **Stock Coverage**: 200+ NSE stocks (Large Cap, Mid Cap, Small Cap)
2. **Sector Filtering**: Finance, IT, FMCG, Pharma, Energy, Metals, Cement, Auto, etc.
3. **Fundamental Filters**:
   - P/E Ratio (configurable threshold)
   - Market Cap classification
4. **Technical Indicators**:
   - RSI (14-period)
   - MACD (12, 26, 9)
   - SMA 20, 50, 200
   - Volume ratio (current vs 20-day average)
5. **Buy/Sell Recommendations**:
   - Score-based ranking (0-12)
   - Target price (configurable %, default 20%)
   - Stop loss (configurable %, default 10%)
   - Categories: STRONG BUY, BUY, HOLD, WAIT
6. **Interactive Charts**: Price+SMA, MACD, RSI

## Project Structure
```
stockscreener/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── CLAUDE.md           # AI project notes (this file)
├── .gitignore          # Git ignore rules
└── test_yfinance.py    # Test script for API
```

## Running the Application
- **Port**: 8501 (default)
- **URL**: http://localhost:8501
- **Command**: `streamlit run app.py --server.port 8501`
- **Python**: Activate virtual environment first (`.venv\Scripts\activate`)

## Dependencies
```
yfinance>=0.2.36
streamlit>=1.29.0
pandas>=2.1.0
numpy>=1.24.0
plotly>=5.18.0
```

## Notes
- NSE stocks use ".NS" suffix in yfinance
- yfinance may have rate limits - scanning too many stocks may be slow
- Default target: +20%, stop loss: -10%
- Technical analysis is for educational purposes only