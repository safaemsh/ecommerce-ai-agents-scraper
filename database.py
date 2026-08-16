"""
Module de gestion de la base de données SQLite
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Product(Base):
    """Modèle de données pour les produits"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String(50), nullable=False)  # 'amazon', 'temu', 'aliexpress'
    title = Column(String(500), nullable=False)
    price = Column(Float)
    original_price = Column(Float)
    rating = Column(Float)
    reviews_count = Column(Integer)
    image_url = Column(Text)
    product_url = Column(Text, unique=True)
    description = Column(Text)
    sales_rank = Column(Integer)  # Rang de vente
    category = Column(String(200))
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Product(platform='{self.platform}', title='{self.title[:50]}...', price={self.price})>"


class DatabaseManager:
    """Gestionnaire de base de données"""
    
    def __init__(self, db_path='products.db'):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def normalize_url(self, url):
        """Normaliser une URL pour éviter les doublons"""
        if not url:
            return None
        url = str(url).strip()
        # Supprimer les paramètres de tracking
        if '?' in url:
            # Garder seulement le chemin de base avant ?
            base_url = url.split('?')[0]
            # Extraire l'ID du produit si présent
            if '/item/' in base_url:
                item_id = base_url.split('/item/')[-1].split('/')[0]
                if item_id:
                    # Reconstruire l'URL de base
                    domain = base_url.split('/item/')[0]
                    return f"{domain}/item/{item_id}"
            elif '/dp/' in base_url:
                asin = base_url.split('/dp/')[-1].split('/')[0]
                if asin:
                    domain = base_url.split('/dp/')[0]
                    return f"{domain}/dp/{asin}"
        return url
    
    def add_product(self, product_data):
        """Ajouter un produit à la base de données avec déduplication améliorée"""
        try:
            # Normaliser l'URL pour éviter les doublons
            original_url = product_data.get('product_url')
            normalized_url = self.normalize_url(original_url)
            
            # Vérifier si le produit existe déjà (par URL normalisée ou originale)
            existing = None
            if normalized_url:
                # Chercher par URL normalisée
                all_products = self.session.query(Product).all()
                for prod in all_products:
                    if prod.product_url and self.normalize_url(prod.product_url) == normalized_url:
                        existing = prod
                        break
            
            # Si pas trouvé, chercher par URL exacte
            if not existing and original_url:
                existing = self.session.query(Product).filter_by(
                    product_url=original_url
                ).first()
            
            # Chercher aussi par titre similaire et plateforme (pour éviter vrais doublons)
            if not existing and product_data.get('title') and product_data.get('platform'):
                title_lower = product_data['title'].lower()[:100]  # Premiers 100 caractères
                similar = self.session.query(Product).filter(
                    Product.platform == product_data['platform'],
                    Product.title.like(f"%{title_lower[:50]}%")
                ).first()
                if similar:
                    # Vérifier si c'est vraiment le même produit
                    if similar.product_url and original_url:
                        # Si les URLs pointent vers le même produit (même ID dans l'URL)
                        if '/item/' in original_url and '/item/' in similar.product_url:
                            orig_id = original_url.split('/item/')[-1].split('/')[0].split('?')[0]
                            sim_id = similar.product_url.split('/item/')[-1].split('/')[0].split('?')[0]
                            if orig_id == sim_id:
                                existing = similar
            
            if existing:
                # Mettre à jour le produit existant avec les nouvelles données
                for key, value in product_data.items():
                    if hasattr(existing, key):
                        # Mettre à jour seulement si la nouvelle valeur est meilleure
                        if value is not None:
                            if key == 'price' and existing.price is None:
                                setattr(existing, key, value)
                            elif key == 'rating' and existing.rating is None:
                                setattr(existing, key, value)
                            elif key == 'reviews_count' and existing.reviews_count is None:
                                setattr(existing, key, value)
                            elif key == 'image_url' and (not existing.image_url or len(str(existing.image_url)) < 10):
                                setattr(existing, key, value)
                            elif key not in ['price', 'rating', 'reviews_count', 'image_url']:
                                setattr(existing, key, value)
                existing.scraped_at = datetime.utcnow()
                product_data['product_url'] = normalized_url or original_url
            else:
                # Créer un nouveau produit avec URL normalisée
                product_data['product_url'] = normalized_url or original_url
                product = Product(**product_data)
                self.session.add(product)
            
            self.session.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout du produit: {e}")
            import traceback
            traceback.print_exc()
            self.session.rollback()
            return False
    
    def get_products(self, platform=None, limit=100):
        """Récupérer les produits de la base de données sans doublons"""
        query = self.session.query(Product)
        if platform:
            query = query.filter_by(platform=platform)
        # Ordonner par date de scraping décroissante pour avoir les plus récents
        products = query.order_by(Product.scraped_at.desc(), Product.sales_rank.asc()).limit(limit * 2).all()
        
        # Dédupliquer par URL normalisée
        seen_urls = set()
        unique_products = []
        for product in products:
            normalized = self.normalize_url(product.product_url)
            if normalized and normalized not in seen_urls:
                seen_urls.add(normalized)
                unique_products.append(product)
                if len(unique_products) >= limit:
                    break
        
        return unique_products
    
    def close(self):
        """Fermer la session"""
        self.session.close()

