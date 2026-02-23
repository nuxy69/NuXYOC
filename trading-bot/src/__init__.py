#!/usr/bin/env python3

"""
MRC SuperSmoother Trading Bot

A trading bot implementing the MRC supersmoother indicator strategy with reversal candle detection.

Usage:
  python src/main.py              # Run in live trading mode
  python src/main.py test         # Run in test mode

Configuration:
  Copy .env.example to .env and fill in your Tradovate API credentials.

Strategy:
  - Uses MRC supersmoother indicator to create dynamic bands
  - Detects reversal candles (doji, hammer, shooting star, engulfing)
  - Enters trades when price is in/through bands and reversal occurs
  - Exits trades at 2% profit target or 1% stop loss

Assets:
  - Futures: ES (E-mini S&P 500)
  - Timeframe: 1-minute bars

Risk Management:
  - Maximum 1 contract per position
  - Maximum 5 trades per day
  - 2% profit target
  - 1% stop loss

Structure:
  src/
    main.py          - Main application
    config.py        - Configuration management
    strategy.py      - Trading strategy logic
    supersmoother.py - MRC supersmoother indicator
    candle_detector.py - Reversal candle detection
    data_fetcher.py  - Market data retrieval
    trader.py        - Order execution
  tests/
    test_indicators.py - Indicator tests
    test_config.py    - Configuration tests
    test_trading.py   - Strategy tests
"""

__version__ = "1.0.0"
__author__ = "MRC Trading Bot"