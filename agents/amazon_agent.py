"""
Agent de scraping pour Amazon
"""
from bs4 import BeautifulSoup
from agents.base_agent import BaseAgent
import logging
import re

logger = logging.getLogger(__name__)


class AmazonAgent(BaseAgent):
    """Agent pour scraper les meilleures ventes d'Amazon"""
    
    def __init__(self):
        from config import AGENTS_CONFIG
        super().__init__('amazon', AGENTS_CONFIG['amazon'])
        self.base_url = 'https://www.amazon.fr'
        self.best_sellers_url = 'https://www.amazon.fr/gp/bestsellers'
    
    def scrape_best_sellers(self):
        """Scraper les meilleures ventes d'Amazon"""
        logger.info("Démarrage du scraping Amazon...")
        
        try:
            # Scraper différentes catégories
            categories = [
                '/gp/bestsellers/electronics',
                '/gp/bestsellers/home-garden',
                '/gp/bestsellers/sports-outdoors',
                '/gp/bestsellers/beauty',
                '/gp/bestsellers/clothing',
            ]
            
            products = []
            for category in categories:  # Scraper toutes les catégories
                url = f"{self.base_url}{category}"
                logger.info(f"Scraping de la catégorie: {category}")
                
                response = self.fetch_page(url)
                if response:
                    category_products = self.parse_category_page(response.text)
                    products.extend(category_products)
                    if len(products) >= self.config.get('max_products', 100):
                        break
                    self.delay()
            
            logger.info(f"{len(products)} produits trouvés sur Amazon")
            return products
            
        except Exception as e:
            logger.error(f"Erreur lors du scraping Amazon: {e}")
            return []
    
    def parse_category_page(self, html):
        """Parser une page de catégorie"""
        soup = BeautifulSoup(html, 'lxml')
        products = []
        
        # Chercher les éléments produits (structure Amazon - multiples méthodes)
        product_items = soup.find_all('div', {'id': re.compile(r'p13n-asin-index-\d+')})
        
        if not product_items:
            # Alternative: chercher par classe zg-item
            product_items = soup.find_all('div', class_=re.compile(r'.*zg-item.*'))
        
        if not product_items:
            # Alternative: chercher par structure li dans ol
            product_items = soup.find_all('li', class_=re.compile(r'.*zg-item.*'))
        
        if not product_items:
            # Dernière alternative: chercher tous les liens avec /dp/
            links = soup.find_all('a', href=re.compile(r'/dp/[A-Z0-9]+'))
            seen_asin = set()
            for link in links:
                asin_match = re.search(r'/dp/([A-Z0-9]+)', link.get('href', ''))
                if asin_match:
                    asin = asin_match.group(1)
                    if asin not in seen_asin:
                        seen_asin.add(asin)
                        # Créer un conteneur factice avec le lien
                        container = link.parent
                        if container:
                            product_items.append(container)
                            if len(product_items) >= self.config.get('max_products', 50):
                                break
        
        logger.info(f"Trouvé {len(product_items)} éléments produits potentiels")
        
        for idx, item in enumerate(product_items[:self.config.get('max_products', 50)]):
            try:
                product = self.parse_product(item)
                if product:
                    product['sales_rank'] = idx + 1
                    products.append(product)
                    self.save_product(product)
            except Exception as e:
                logger.debug(f"Erreur lors du parsing d'un produit: {e}")
                continue
        
        return products
    
    def parse_product(self, product_element):
        """Parser un élément produit"""
        try:
            product_data = {}
            
            # URL d'abord (pour obtenir l'ASIN)
            link_elem = product_element.find('a', href=re.compile(r'/dp/[A-Z0-9]+'))
            if link_elem:
                href = link_elem.get('href', '')
                # Nettoyer l'URL
                if '?' in href:
                    href = href.split('?')[0]
                product_data['product_url'] = f"{self.base_url}{href}" if href.startswith('/') else href
            else:
                # Chercher dans tous les liens
                all_links = product_element.find_all('a', href=True)
                for link in all_links:
                    if '/dp/' in link.get('href', ''):
                        href = link.get('href', '').split('?')[0]
                        product_data['product_url'] = f"{self.base_url}{href}" if href.startswith('/') else href
                        break
            
            # Titre - plusieurs méthodes
            title_elem = product_element.find(['span', 'div'], class_=re.compile(r'.*p13n-sc-truncate.*|.*zg-item-title.*'))
            if not title_elem:
                title_elem = product_element.find('a', {'class': re.compile(r'.*a-link-normal.*')})
            if not title_elem and link_elem:
                title_elem = link_elem
            if title_elem:
                title_text = title_elem.get_text(strip=True)
                if title_text and len(title_text) > 5:  # Titre valide
                    product_data['title'] = title_text[:500]  # Limiter la longueur
            
            # Prix - plusieurs formats
            price_elem = product_element.find('span', class_=re.compile(r'.*p13n-sc-price.*|.*a-price.*'))
            if not price_elem:
                # Chercher prix dans le texte
                price_spans = product_element.find_all('span', string=re.compile(r'[\d,]+[.,]\d+'))
                for span in price_spans:
                    if '€' in span.get_text() or '$' in span.get_text() or re.search(r'[\d,]+[.,]\d+', span.get_text()):
                        price_elem = span
                        break
            
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Extraire le prix avec regex
                price_match = re.search(r'([\d\s,]+[.,]\d{2})', price_text.replace(',', '.').replace(' ', ''))
                if price_match:
                    try:
                        price_str = price_match.group(1).replace(',', '.').replace(' ', '')
                        product_data['price'] = float(price_str)
                    except ValueError:
                        pass
            
            # Image
            img_elem = product_element.find('img', src=True)
            if img_elem:
                img_src = img_elem.get('src', '') or img_elem.get('data-src', '')
                if img_src and 'http' in img_src:
                    product_data['image_url'] = img_src
            
            # Note - plusieurs méthodes
            rating_elem = product_element.find('span', class_=re.compile(r'.*a-icon-alt.*'))
            if not rating_elem:
                rating_elem = product_element.find('span', string=re.compile(r'\d+[.,]\d+.*étoiles?|\d+[.,]\d+.*stars?'))
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+[.,]\d+)', rating_text)
                if rating_match:
                    try:
                        product_data['rating'] = float(rating_match.group(1).replace(',', '.'))
                    except ValueError:
                        pass
            
            # Nombre d'avis
            reviews_elem = product_element.find('a', href=re.compile(r'#customerReviews'))
            if reviews_elem:
                reviews_text = reviews_elem.get_text(strip=True)
                reviews_match = re.search(r'([\d\s]+)', reviews_text.replace(' ', ''))
                if reviews_match:
                    try:
                        product_data['reviews_count'] = int(reviews_match.group(1).replace(' ', ''))
                    except ValueError:
                        pass
            
            if product_data.get('title') and product_data.get('product_url'):
                return product_data
            
        except Exception as e:
            logger.debug(f"Erreur lors du parsing: {e}")
        
        return None

