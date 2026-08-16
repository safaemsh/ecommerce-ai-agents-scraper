"""
Agent de scraping pour Temu
"""
from bs4 import BeautifulSoup
from agents.base_agent import BaseAgent
import logging
import re

logger = logging.getLogger(__name__)


class TemuAgent(BaseAgent):
    """Agent pour scraper les meilleures ventes de Temu"""
    
    def __init__(self):
        from config import AGENTS_CONFIG
        super().__init__('temu', AGENTS_CONFIG['temu'])
        self.base_url = 'https://www.temu.com'
    
    def scrape_best_sellers(self):
        """Scraper les meilleures ventes de Temu - essaie Selenium d'abord"""
        # Essayer avec Selenium si disponible (une seule fois)
        selenium_tried = False
        try:
            from agents.temu_agent_selenium import TemuAgentSelenium
            logger.info("Tentative avec Selenium pour Temu...")
            selenium_agent = TemuAgentSelenium()
            products = selenium_agent.scrape_best_sellers()
            selenium_agent.close()
            selenium_tried = True
            if products:
                return products
        except Exception as e:
            logger.info(f"Selenium non disponible, utilisation de BeautifulSoup: {e}")
        
        # Fallback vers BeautifulSoup (une seule fois)
        if not selenium_tried or not products:
            return self._scrape_with_bs4()
        return products
    
    def _scrape_with_bs4(self):
        """Scraper avec BeautifulSoup (fallback)"""
        logger.info("Démarrage du scraping Temu avec BeautifulSoup...")
        
        try:
            # Temu - Plusieurs URLs de produits populaires
            urls = [
                f"{self.base_url}/fr/g/best-sellers.html",
                f"{self.base_url}/fr/g/top-sellers.html",
                f"{self.base_url}/fr/g/popular.html",
            ]
            
            all_products = []
            for url in urls:  # Essayer toutes les URLs
                logger.info(f"Scraping de l'URL Temu: {url}")
                response = self.fetch_page(url)
                if response:
                    products = self.parse_category_page(response.text)
                    all_products.extend(products)
                    if len(all_products) >= self.config.get('max_products', 100):
                        break
                    if products:
                        self.delay()
            
            logger.info(f"{len(all_products)} produits trouvés sur Temu")
            return all_products
            
        except Exception as e:
            logger.error(f"Erreur lors du scraping Temu: {e}")
            return []
    
    def parse_category_page(self, html):
        """Parser une page de catégorie Temu"""
        soup = BeautifulSoup(html, 'lxml')
        products = []
        
        # Chercher les éléments produits (structure Temu - multiples méthodes)
        # Méthode 1: Chercher les liens produits
        product_links = soup.find_all('a', href=re.compile(r'/goods/|/product/'))
        
        # Méthode 2: Chercher par classes communes
        if not product_links:
            product_items = soup.find_all('div', class_=re.compile(r'.*product.*|.*item.*|.*goods.*'))
        else:
            # Utiliser les liens comme base
            seen_urls = set()
            product_items = []
            for link in product_links:
                href = link.get('href', '')
                if href and href not in seen_urls:
                    seen_urls.add(href)
                    # Prendre le parent comme conteneur
                    container = link.find_parent(['div', 'article', 'section'])
                    if container:
                        product_items.append(container)
                    else:
                        product_items.append(link.parent if link.parent else link)
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
            
            # Trouver le conteneur parent si nécessaire
            container = product_element
            if product_element.name == 'a':
                container = product_element.parent or product_element
            
            # URL d'abord
            link_elem = container.find('a', href=re.compile(r'/goods/|/product/'))
            if not link_elem and container.name == 'a':
                link_elem = container
            if link_elem:
                href = link_elem.get('href', '')
                if href:
                    if '?' in href:
                        href = href.split('?')[0]
                    product_data['product_url'] = f"{self.base_url}{href}" if href.startswith('/') else href
            
            # Titre - plusieurs méthodes
            title_elem = container.find(['div', 'span', 'h3', 'h2', 'a'], class_=re.compile(r'.*title.*|.*name.*|.*product.*title.*'))
            if not title_elem:
                title_elem = container.find('a')
            if not title_elem:
                # Chercher dans tous les textes
                all_text = container.get_text()
                if len(all_text) > 10 and len(all_text) < 200:
                    title_elem = container
            
            if title_elem:
                title_text = title_elem.get_text(strip=True)
                # Nettoyer le titre
                if title_text:
                    title_text = ' '.join(title_text.split())  # Normaliser les espaces
                    if len(title_text) > 5 and len(title_text) < 500:
                        product_data['title'] = title_text
            
            # Prix - plusieurs formats
            price_elem = container.find(['span', 'div', 'p'], class_=re.compile(r'.*price.*|.*cost.*'))
            if not price_elem:
                # Chercher prix dans le texte (format €X.XX ou $X.XX)
                price_patterns = [
                    r'€\s*([\d,]+[.,]\d+)',
                    r'\$\s*([\d,]+[.,]\d+)',
                    r'([\d,]+[.,]\d+)\s*€',
                ]
                container_text = container.get_text()
                for pattern in price_patterns:
                    price_match = re.search(pattern, container_text)
                    if price_match:
                        try:
                            price_str = price_match.group(1).replace(',', '.').replace(' ', '')
                            product_data['price'] = float(price_str)
                            break
                        except ValueError:
                            continue
            else:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'([\d,]+[.,]\d+)', price_text.replace(',', '.'))
                if price_match:
                    try:
                        price_str = price_match.group(1).replace(',', '.').replace(' ', '')
                        product_data['price'] = float(price_str)
                    except ValueError:
                        pass
            
            # Image
            img_elem = container.find('img', src=True)
            if not img_elem:
                img_elem = container.find('img', {'data-src': True})
            if img_elem:
                img_src = img_elem.get('src', '') or img_elem.get('data-src', '') or img_elem.get('data-lazy-src', '')
                if img_src and 'http' in img_src:
                    product_data['image_url'] = img_src
            
            # Note (si disponible)
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

