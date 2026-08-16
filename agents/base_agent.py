"""
Agent de base pour le scraping
"""
from abc import ABC, abstractmethod
import time
import requests
from fake_useragent import UserAgent
from database import DatabaseManager
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Classe de base pour tous les agents de scraping"""
    
    def __init__(self, platform_name, config):
        self.platform_name = platform_name
        self.config = config
        self.db = DatabaseManager()
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    @abstractmethod
    def scrape_best_sellers(self):
        """Scraper les produits les plus vendus"""
        pass
    
    @abstractmethod
    def parse_product(self, product_element):
        """Parser un élément produit"""
        pass
    
    def save_product(self, product_data):
        """Sauvegarder un produit dans la base de données"""
        product_data['platform'] = self.platform_name
        return self.db.add_product(product_data)
    
    def fetch_page(self, url, retries=3):
        """Récupérer une page avec retry"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response
            except Exception as e:
                logger.warning(f"Tentative {attempt + 1}/{retries} échouée: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    logger.error(f"Impossible de récupérer {url}")
                    return None
    
    def delay(self):
        """Respecter le délai configuré entre les requêtes"""
        time.sleep(self.config.get('delay', 2))
    
    def close(self):
        """Fermer les ressources"""
        self.db.close()
        self.session.close()

