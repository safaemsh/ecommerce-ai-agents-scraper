"""
Agent de scraping pour Aliexpress
"""
from bs4 import BeautifulSoup
from agents.base_agent import BaseAgent
import logging
import re

logger = logging.getLogger(__name__)


class AliexpressAgent(BaseAgent):
    """Agent pour scraper les meilleures ventes d'Aliexpress"""
    
    def __init__(self):
        from config import AGENTS_CONFIG
        super().__init__('aliexpress', AGENTS_CONFIG['aliexpress'])
        self.base_url = 'https://www.aliexpress.com'
    
    def scrape_best_sellers(self):
        """Scraper les meilleures ventes d'Aliexpress"""
        logger.info("Démarrage du scraping Aliexpress...")
        
        try:
            # Aliexpress - URL des produits populaires
            url = f"{self.base_url}/wholesale?SearchText=best+seller"
            
            response = self.fetch_page(url)
            if not response:
                logger.warning("Impossible de récupérer la page Aliexpress")
                return []
            
            products = self.parse_category_page(response.text)
            logger.info(f"{len(products)} produits trouvés sur Aliexpress")
            return products
            
        except Exception as e:
            logger.error(f"Erreur lors du scraping Aliexpress: {e}")
            return []
    
    def parse_category_page(self, html):
        """Parser une page de recherche Aliexpress"""
        soup = BeautifulSoup(html, 'lxml')
        products = []
        
        # Chercher les éléments produits (structure Aliexpress)
        product_items = soup.find_all('div', class_=re.compile(r'.*product-item.*|.*list--gallery.*'))
        
        # Alternative: chercher par data attributes
        if not product_items:
            product_items = soup.find_all('a', href=re.compile(r'/item/'))
        
        for idx, item in enumerate(product_items[:self.config.get('max_products', 50)]):
            try:
                product = self.parse_product(item)
                if product:
                    product['sales_rank'] = idx + 1
                    products.append(product)
                    self.save_product(product)
            except Exception as e:
                logger.warning(f"Erreur lors du parsing d'un produit: {e}")
                continue
        
        return products
    
    def parse_product(self, product_element):
        """Parser un élément produit Aliexpress"""
        try:
            product_data = {}
            
            # Trouver le conteneur parent si nécessaire
            container = product_element
            if product_element.name == 'a':
                container = product_element.parent
            
            # Titre - nettoyer pour enlever les prix et autres infos
            title_elem = container.find(['h1', 'h2', 'h3', 'a'], class_=re.compile(r'.*title.*|.*product-title.*'))
            if not title_elem:
                title_elem = container.find('a')
            if title_elem:
                title_text = title_elem.get_text(strip=True)
                # Nettoyer le titre : enlever les prix, notes, etc.
                # Supprimer les patterns comme MAD9.85, €9.85, 4.5, etc.
                title_text = re.sub(r'MAD\d+[.,]\d+', '', title_text)
                title_text = re.sub(r'€\s*\d+[.,]\d+', '', title_text)
                title_text = re.sub(r'\d+[.,]\d+\s*€', '', title_text)
                title_text = re.sub(r'\d+[.,]\d+\s*-\s*\d+%', '', title_text)  # Réductions
                title_text = re.sub(r'\d+[.,]\d+\s+sold', '', title_text, flags=re.IGNORECASE)
                title_text = re.sub(r'rating\s*\d+[.,]\d+', '', title_text, flags=re.IGNORECASE)
                title_text = re.sub(r'\d+\+\s*sold', '', title_text, flags=re.IGNORECASE)
                # Nettoyer les espaces multiples
                title_text = ' '.join(title_text.split())
                # Limiter la longueur
                if len(title_text) > 200:
                    title_text = title_text[:200] + "..."
                product_data['title'] = title_text
            
            # Prix - plusieurs formats améliorés
            price_found = False
            # Méthode 1: Chercher dans les éléments avec classe price
            price_elem = container.find(['span', 'div', 'strong'], class_=re.compile(r'.*price.*|.*cost.*|.*amount.*'))
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Chercher pattern MAD ou € suivi de nombre
                price_patterns = [
                    r'MAD\s*(\d+[.,]\d+)',
                    r'€\s*(\d+[.,]\d+)',
                    r'(\d+[.,]\d+)\s*€',
                    r'(\d+[.,]\d{2})',  # Format générique
                ]
                for pattern in price_patterns:
                    price_match = re.search(pattern, price_text.replace(',', '.'))
                    if price_match:
                        try:
                            price_str = price_match.group(1).replace(',', '.').replace(' ', '')
                            price_val = float(price_str)
                            if 0.01 <= price_val <= 100000:  # Plage raisonnable
                                product_data['price'] = price_val
                                price_found = True
                                break
                        except (ValueError, IndexError):
                            continue
            
            # Méthode 2: Chercher dans tout le texte du conteneur
            if not price_found:
                container_text = container.get_text()
                # Chercher le premier prix valide
                price_patterns = [
                    r'MAD\s*(\d+[.,]\d{2})',
                    r'€\s*(\d+[.,]\d{2})',
                    r'(\d+[.,]\d{2})\s*€',
                ]
                for pattern in price_patterns:
                    price_match = re.search(pattern, container_text.replace(',', '.'))
                    if price_match:
                        try:
                            price_str = price_match.group(1).replace(',', '.').replace(' ', '')
                            price_val = float(price_str)
                            if 0.01 <= price_val <= 100000:
                                product_data['price'] = price_val
                                break
                        except (ValueError, IndexError):
                            continue
            
            # URL
            link_elem = container.find('a', href=re.compile(r'/item/|/product/'))
            if link_elem:
                href = link_elem.get('href', '')
                product_data['product_url'] = f"{self.base_url}{href}" if href.startswith('/') else href
            
            # Image
            img_elem = container.find('img', src=True)
            if not img_elem:
                img_elem = container.find('img', {'data-src': True})
            if img_elem:
                img_src = img_elem.get('src', '') or img_elem.get('data-src', '') or img_elem.get('data-lazy-src', '')
                if img_src and 'http' in img_src:
                    product_data['image_url'] = img_src
            
            # Note (si disponible) - amélioré
            rating_elem = container.find(['span', 'div'], class_=re.compile(r'.*rating.*|.*star.*|.*score.*'))
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                # Chercher note entre 0 et 5
                rating_match = re.search(r'([0-5][.,]\d+)', rating_text)
                if rating_match:
                    try:
                        rating_val = float(rating_match.group(1).replace(',', '.'))
                        if 0 <= rating_val <= 5:
                            product_data['rating'] = rating_val
                    except ValueError:
                        pass
            
            # Chercher aussi dans le texte complet
            if 'rating' not in product_data:
                container_text = container.get_text()
                rating_match = re.search(r'([0-5][.,]\d+)\s*(?:stars?|étoiles?)', container_text, re.IGNORECASE)
                if not rating_match:
                    rating_match = re.search(r'rating[:\s]*([0-5][.,]\d+)', container_text, re.IGNORECASE)
                if rating_match:
                    try:
                        rating_val = float(rating_match.group(1).replace(',', '.'))
                        if 0 <= rating_val <= 5:
                            product_data['rating'] = rating_val
                    except ValueError:
                        pass
            
            # Nombre d'avis - amélioré
            reviews_elem = container.find(['span', 'div'], string=re.compile(r'\d+.*review|\d+.*avis|\d+.*sold', re.IGNORECASE))
            if reviews_elem:
                reviews_text = reviews_elem.get_text(strip=True)
            else:
                # Chercher dans le texte
                container_text = container.get_text()
                reviews_match = re.search(r'(\d+[\s,]*\d*)\s*(?:reviews?|avis|sold)', container_text, re.IGNORECASE)
                if reviews_match:
                    reviews_text = reviews_match.group(0)
                else:
                    reviews_text = ""
            
            if reviews_text:
                # Extraire le nombre
                reviews_match = re.search(r'(\d+[\s,]*\d+)', reviews_text.replace(',', '').replace(' ', ''))
                if reviews_match:
                    try:
                        reviews_str = reviews_match.group(1).replace(',', '').replace(' ', '')
                        product_data['reviews_count'] = int(reviews_str)
                    except ValueError:
                        pass
            
            if product_data.get('title') and product_data.get('product_url'):
                return product_data
            
        except Exception as e:
            logger.warning(f"Erreur lors du parsing Aliexpress: {e}")
        
        return None

