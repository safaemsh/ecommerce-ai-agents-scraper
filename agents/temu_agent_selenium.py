"""
Agent de scraping pour Temu avec Selenium (pour JavaScript)
"""
from bs4 import BeautifulSoup
from agents.base_agent import BaseAgent
import logging
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

logger = logging.getLogger(__name__)


class TemuAgentSelenium(BaseAgent):
    """Agent pour scraper les meilleures ventes de Temu avec Selenium"""
    
    def __init__(self):
        from config import AGENTS_CONFIG
        super().__init__('temu', AGENTS_CONFIG['temu'])
        self.base_url = 'https://www.temu.com'
        self.driver = None
        self._init_driver()
    
    def _init_driver(self):
        """Initialiser le driver Selenium"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Mode headless
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument(f'user-agent={self.ua.random}')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Driver Selenium initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du driver: {e}")
            self.driver = None
    
    def scrape_best_sellers(self):
        """Scraper les meilleures ventes de Temu avec Selenium"""
        logger.info("Démarrage du scraping Temu avec Selenium...")
        
        if not self.driver:
            logger.error("Driver Selenium non initialisé, tentative avec BeautifulSoup...")
            return self._fallback_scraping()
        
        try:
            # URLs Temu pour bestsellers
            urls = [
                f"{self.base_url}/fr/g/best-sellers.html",
                f"{self.base_url}/fr/g/top-sellers.html",
                f"{self.base_url}/fr/category/bestsellers.html",
            ]
            
            all_products = []
            for url in urls:
                try:
                    logger.info(f"Scraping Temu avec Selenium: {url}")
                    self.driver.get(url)
                    
                    # Attendre que la page se charge
                    time.sleep(5)
                    
                    # Attendre que les produits soient chargés
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='product'], [class*='item'], a[href*='/goods/']"))
                        )
                    except:
                        logger.warning("Timeout en attendant les produits")
                    
                    # Scroll pour charger plus de produits
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                    time.sleep(2)
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    
                    # Récupérer le HTML après chargement JavaScript
                    html = self.driver.page_source
                    products = self.parse_category_page(html)
                    
                    if products:
                        all_products.extend(products)
                        logger.info(f"Trouvé {len(products)} produits sur {url}")
                        if len(all_products) >= self.config.get('max_products', 50):
                            break
                    
                    self.delay()
                    
                except Exception as e:
                    logger.warning(f"Erreur avec l'URL {url}: {e}")
                    continue
            
            logger.info(f"Total: {len(all_products)} produits trouvés sur Temu")
            return all_products
            
        except Exception as e:
            logger.error(f"Erreur lors du scraping Temu: {e}")
            return self._fallback_scraping()
    
    def _fallback_scraping(self):
        """Méthode de repli sans Selenium"""
        from agents.temu_agent import TemuAgent
        fallback_agent = TemuAgent()
        return fallback_agent.scrape_best_sellers()
    
    def parse_category_page(self, html):
        """Parser une page de catégorie Temu"""
        soup = BeautifulSoup(html, 'lxml')
        products = []
        
        # Chercher les produits avec plusieurs méthodes
        product_selectors = [
            ('a', {'href': re.compile(r'/goods/|/product/')}),
            ('div', {'class': re.compile(r'.*product.*|.*goods.*|.*item-card.*')}),
            ('article', {'class': re.compile(r'.*product.*')}),
        ]
        
        product_items = []
        seen_urls = set()
        
        for selector, attrs in product_selectors:
            items = soup.find_all(selector, attrs)
            for item in items:
                # Extraire l'URL pour éviter les doublons
                link = item if item.name == 'a' else item.find('a', href=re.compile(r'/goods/|/product/'))
                if link:
                    href = link.get('href', '')
                    if href and href not in seen_urls:
                        seen_urls.add(href)
                        product_items.append(item)
                        if len(product_items) >= self.config.get('max_products', 50) * 2:
                            break
            if len(product_items) >= self.config.get('max_products', 50):
                break
        
        logger.info(f"Trouvé {len(product_items)} éléments produits potentiels sur Temu")
        
        for idx, item in enumerate(product_items[:self.config.get('max_products', 50)]):
            try:
                product = self.parse_product(item)
                if product:
                    product['sales_rank'] = idx + 1
                    products.append(product)
                    self.save_product(product)
            except Exception as e:
                logger.debug(f"Erreur lors du parsing d'un produit Temu: {e}")
                continue
        
        return products
    
    def parse_product(self, product_element):
        """Parser un élément produit Temu"""
        try:
            product_data = {}
            
            container = product_element
            if product_element.name == 'a':
                container = product_element.parent or product_element
            
            # URL
            link_elem = container.find('a', href=re.compile(r'/goods/|/product/'))
            if not link_elem and container.name == 'a':
                link_elem = container
            
            if link_elem:
                href = link_elem.get('href', '')
                if href:
                    if '?' in href:
                        href = href.split('?')[0]
                    if not href.startswith('http'):
                        href = f"{self.base_url}{href}" if href.startswith('/') else f"{self.base_url}/{href}"
                    product_data['product_url'] = href
            
            # Titre - chercher dans plusieurs endroits
            title_selectors = [
                ('span', {'class': re.compile(r'.*title.*|.*name.*')}),
                ('div', {'class': re.compile(r'.*title.*|.*name.*|.*product.*title.*')}),
                ('h2', {}),
                ('h3', {}),
                ('a', {'href': re.compile(r'/goods/|/product/')}),
            ]
            
            for selector, attrs in title_selectors:
                title_elem = container.find(selector, attrs)
                if title_elem:
                    title_text = title_elem.get_text(strip=True)
                    if title_text and len(title_text) > 5 and len(title_text) < 500:
                        product_data['title'] = title_text
                        break
            
            # Prix - plusieurs formats
            price_selectors = [
                ('span', {'class': re.compile(r'.*price.*|.*cost.*')}),
                ('div', {'class': re.compile(r'.*price.*')}),
            ]
            
            for selector, attrs in price_selectors:
                price_elem = container.find(selector, attrs)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Extraire le prix
                    price_match = re.search(r'([\d,]+[.,]\d{2})', price_text.replace(',', '.'))
                    if price_match:
                        try:
                            price_str = price_match.group(1).replace(',', '.').replace(' ', '')
                            product_data['price'] = float(price_str)
                            break
                        except ValueError:
                            continue
            
            # Si pas de prix trouvé, chercher dans tout le texte
            if 'price' not in product_data:
                container_text = container.get_text()
                price_match = re.search(r'€\s*([\d,]+[.,]\d{2})|([\d,]+[.,]\d{2})\s*€', container_text)
                if price_match:
                    price_str = (price_match.group(1) or price_match.group(2)).replace(',', '.').replace(' ', '')
                    try:
                        product_data['price'] = float(price_str)
                    except ValueError:
                        pass
            
            # Image
            img_elem = container.find('img')
            if img_elem:
                img_src = img_elem.get('src', '') or img_elem.get('data-src', '') or img_elem.get('data-lazy-src', '')
                if img_src and 'http' in img_src:
                    product_data['image_url'] = img_src
            
            # Note
            rating_elem = container.find(['span', 'div'], class_=re.compile(r'.*rating.*|.*star.*|.*score.*'))
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+[.,]\d+)', rating_text)
                if rating_match:
                    try:
                        product_data['rating'] = float(rating_match.group(1).replace(',', '.'))
                    except ValueError:
                        pass
            
            if product_data.get('title') and product_data.get('product_url'):
                return product_data
            
        except Exception as e:
            logger.debug(f"Erreur lors du parsing Temu: {e}")
        
        return None
    
    def close(self):
        """Fermer les ressources"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        super().close()

