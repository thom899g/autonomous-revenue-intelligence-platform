from typing import Dict, Optional
import logging
from datetime import datetime, timedelta
import requests
from sqlalchemy import create_engine

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

class DataCollector:
    """Class to collect market trends and customer behavior data."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.db_engine = create_engine(config['database_url'])
        
    def fetch_market_trends(self) -> Optional[Dict]:
        """
        Fetches real-time market trend data from external APIs.
        
        Returns:
            Dict: Market trends data or None if failed.
        """
        try:
            response = requests.get(
                self.config['market_api_url'],
                params={
                    'api_key': self.config['market_api_key'],
                    'date_range': (datetime.now() - timedelta(days=30)).isoformat()
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch market trends: {str(e)}")
            return None
            
    def collect_customer_data(self) -> Optional[Dict]:
        """
        Collects customer behavior data from internal databases.
        
        Returns:
            Dict: Customer data or None if failed.
        """
        try:
            # Example query to get recent customer interactions
            with self.db_engine.connect() as connection:
                result = connection.execute(
                    "SELECT * FROM customer_interactions WHERE timestamp > NOW() - INTERVAL '1 week'"
                )
                return [dict(row) for row in result]
        except Exception as e:
            logger.error(f"Failed to collect customer data: {str(e)}")
            return None