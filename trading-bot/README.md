# NuXYOC Trading Bot

This repository contains the main trading bot for NuXYOC, designed to trade futures through the Tradovate API.

## Project Structure

```
trading-bot/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main bot entry point
│   ├── config.py            # Configuration management
│   ├── strategy.py          # Trading strategy logic
│   ├── supersmoother.py     # MRC supersmoother indicator
│   ├── candle_detector.py   # Reversal candle detection
│   ├── data_fetcher.py      # Market data retrieval
│   └── trader.py            # Order execution
├── tests/
│   ├── test_indicators.py  # Indicator tests
│   ├── test_config.py      # Configuration tests
│   └── test_trading.py     # Strategy tests
├── requirements.txt         # Python dependencies
├── .env.example            # Environment configuration
└── .gitignore              # Git ignore rules
```

## Strategy Overview

**Indicator**: MRC supersmoother (smoothing bands)
**Entry**: Price trading in/through bands + reversal candle
**Exit**: Profit target or stop loss
**Asset**: Futures (ES - E-mini S&P 500)

## Strategy Rules

- **Long Entry**: Price below lower band + bullish reversal candle
- **Short Entry**: Price above upper band + bearish reversal candle
- **Exit**: 2% profit target or 1% stop loss

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure API credentials in `.env`
3. Run the bot: `python src/main.py`

## API Integration

This bot integrates with the Tradovate API for futures trading.

## Tasks for Claude Code

1. Implement the MRC supersmoother indicator in `supersmoother.py`
2. Implement reversal candle detection in `candle_detector.py`
3. Implement the main trading strategy in `strategy.py`
4. Create the main application in `main.py`
5. Implement data fetching from Tradovate API in `data_fetcher.py`
6. Implement order execution in `trader.py`
7. Create unit tests for all components
8. Test the complete system