import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for the trading bot"""
    
    # API Configuration
    API_KEY = os.getenv("TRADOVATE_API_KEY")
    CLIENT_ID = os.getenv("TRADOVATE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TRADOVATE_CLIENT_SECRET")
    USERNAME = os.getenv("TRADOVATE_USERNAME")
    PASSWORD = os.getenv("TRADOVATE_PASSWORD")
    ACCOUNT_ID = os.getenv("TRADOVATE_ACCOUNT_ID")
    
    # Trading Configuration
    SYMBOL = os.getenv("SYMBOL", "ES")  # Default to ES (E-mini S&P 500)
    PROFIT_TARGET = float(os.getenv("PROFIT_TARGET", 0.02))  # 2% profit target
    STOP_LOSS = float(os.getenv("STOP_LOSS", 0.01))  # 1% stop loss
    
    # Market Data
    BAR_SIZE = "1m"  # 1-minute bars
    LOOKBACK_PERIODS = 200  # Number of periods for indicator calculation
    
    # Trading Logic
    MIN_PRICE_MOVEMENT = 0.25  # Minimum price movement for valid signals
    MAX_SPREAD = 0.5  # Maximum acceptable spread
    
    # Risk Management
    MAX_POSITION_SIZE = 1  # Maximum contracts per position
    MAX_DAILY_TRADES = 5  # Maximum trades per day
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        required_fields = ["API_KEY", "CLIENT_ID", "CLIENT_SECRET", "USERNAME", "PASSWORD", "ACCOUNT_ID"]
        
        for field in required_fields:
            if not getattr(cls, field):
                raise ValueError(f"Missing required configuration: {field}")
        
        if cls.PROFIT_TARGET <= 0 or cls.STOP_LOSS <= 0:
            raise ValueError("Profit target and stop loss must be positive")
        
        if cls.PROFIT_TARGET <= cls.STOP_LOSS:
            raise ValueError("Profit target must be greater than stop loss")