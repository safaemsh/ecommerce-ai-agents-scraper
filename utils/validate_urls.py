"""
Utilitaire pour valider les URLs des produits
"""
import requests
from urllib.parse import urlparse

def is_valid_url(url, timeout=5):
    """Vérifier si une URL est valide"""
    if not url or not url.startswith('http'):
        return False
    
    try:
        # Vérifier que l'URL est bien formée
        parsed = urlparse(url)
        if not parsed.netloc:
            return False
        
        # Ne pas vérifier réellement (pour éviter trop de requêtes)
        # On vérifie juste le format
        return True
    except:
        return False

def clean_product_url(url, platform):
    """Nettoyer et valider une URL de produit"""
    if not url:
        return None
    
    url = url.strip()
    
    # Supprimer les doubles domaines
    if url.count('www.') > 1:
        last_www = url.rfind('www.')
        if last_www >= 0:
            url = 'https://' + url[last_www:]
    
    # Supprimer doubles slashes
    if url.startswith('https://'):
        url = 'https://' + url[8:].replace('//', '/')
    
    # Ajouter protocole si manquant
    if url.startswith('//'):
        url = 'https:' + url
    
    # Valider le format
    if not is_valid_url(url):
        return None
    
    return url


