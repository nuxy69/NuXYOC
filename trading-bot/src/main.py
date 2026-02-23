import os
import sys
import time
import logging
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, Optional, Tuple

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import Config
from src.strategy import TradingStrategy
from src.data_fetcher import DataFetcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TradingBot:
    """Main trading bot application"""
    
    def __init__(self):
        self.config = Config()
        self.strategy = None
        self.data_fetcher = DataFetcher()
        self.last_run_time = None
        
    def load_config(self):
        """Load configuration from environment"""
        try:
            self.config.validate()
            logger.info("Configuration loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Configuration error: {e}")
            return False
    
    def authenticate(self):
        """Authenticate with Tradovate API"""
        credentials = {
            "clientId": self.config.CLIENT_ID,
            "clientSecret": self.config.CLIENT_SECRET,
            "username": self.config.USERNAME,
            "password": self.config.PASSWORD
        }
        
        if not self.strategy:
            self.strategy = TradingStrategy(self.config)
        
        return self.strategy.authenticate(credentials)
    
    def fetch_market_data(self, symbol: str, interval: str, 
                         lookback_hours: int = 24) -> pd.DataFrame:
        """Fetch market data for analysis"""
        
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=lookback_hours)
        
        try:
            candles = self.data_fetcher.get_historical_data(
                symbol=symbol,
                interval=interval,
                start_date=start_time,
                end_date=end_time
            )
            
            if candles.empty:
                logger.warning("No historical data available")
                return pd.DataFrame()
            
            logger.info(f"Fetched {len(candles)} bars of {interval} data")
            return candles
            
        except Exception as e:
            logger.error(f"Failed to fetch market data: {e}")
            return pd.DataFrame()
    
    def run(self):
        """Main trading loop"""
        
        logger.info("Starting MRC SuperSmoother Trading Bot")
        
        # Load configuration
        if not self.load_config():
            logger.error("Exiting due to configuration error")
            return
        
        # Authenticate
        if not self.authenticate():
            logger.error("Exiting due to authentication error")
            return
        
        # Get account information
        try:
            account_info = self.data_fetcher.get_account_summary()
            logger.info(f"Account balance: ${account_info.get('balance', 0):.2f}")
        except Exception as e:
            logger.warning(f"Could not get account info: {e}")
        
        # Main trading loop
        try:
            while True:
                # Check if market is open
                market_open = self.data_fetcher.get_market_status(self.config.SYMBOL).get("tradingStatus", "")
                
                if market_open.lower() != "open":
                    logger.info("Market is closed. Waiting...")
                    time.sleep(60)
                    continue
                
                # Fetch market data
                candles = self.fetch_market_data(
                    symbol=self.config.SYMBOL,
                    interval=self.config.BAR_SIZE,
                    lookback_hours=24
                )
                
                if candles.empty:
                    logger.warning("No data available, waiting...")
                    time.sleep(60)
                    continue
                
                # Run strategy
                result = self.strategy.run(candles)
                
                # Log results
                logger.info(f"Signal: {result.get('signal')}")
                logger.info(f"Position: {result.get('position')}")
                
                # Wait before next run
                time.sleep(60)  # Run every minute
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Bot error: {e}")
            logger.error("Bot stopped")
    
    def test_strategy(self):
        """Test strategy with historical data"""
        
        logger.info("Testing MRC SuperSmoother Strategy")
        
        # Fetch historical data for testing
        candles = self.fetch_market_data(
            symbol=self.config.SYMBOL,
            interval=self.config.BAR_SIZE,
            lookback_hours=24
        )
        
        if candles.empty:
            logger.error("No data available for testing")
            return
        
        # Run strategy on historical data
        results = []
        
        for i in range(100, len(candles)):
            # Get last 100 candles for analysis
            window = candles.iloc[i-100:i]
            
            # Run strategy
            result = self.strategy.run(window)
            results.append(result)
            
            # For testing, exit after 10 iterations
            if len(results) >= 10:
                break
        
        logger.info(f"Test completed. Generated {len(results)} signals")
        
        # Calculate some statistics
        signals = [r['signal'] for r in results if r['signal']]
        logger.info(f"Signals generated: {len(signals)}")
        
        if signals:
            long_signals = sum(1 for s in signals if s == 'LONG')
            short_signals = sum(1 for s in signals if s == 'SHORT')
            logger.info(f"Long signals: {long_signals}, Short signals: {short_signals}")
    
    def run_test(self):
        """Run strategy in test mode"""
        
        logger.info("Starting MRC SuperSmoother in Test Mode")
        
        if not self.load_config():
            logger.error("Exiting due to configuration error")
            return
        
        if not self.authenticate():
            logger.error("Exiting due to authentication error")
            return
        
        # Run test
        self.test_strategy()

def main():
    """Main entry point"""
    
    # Check if we should run in test mode
    test_mode = len(sys.argv) > 1 and sys.argv[1] == "test"
    
    bot = TradingBot()
    
    if test_mode:
        bot.run_test()
    else:
        bot.run()

if __name__ == "__main__":
    main()