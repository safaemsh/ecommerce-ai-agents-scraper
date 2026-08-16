"""
Point d'entrée principal du système multi-agents
"""
import logging
from agents.amazon_agent import AmazonAgent
from agents.temu_agent import TemuAgent
from agents.aliexpress_agent import AliexpressAgent
from config import AGENTS_CONFIG
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraping.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Lancer tous les agents de scraping"""
    logger.info("=== Démarrage du système multi-agents ===")
    
    agents = []
    results = {}
    
    # Initialiser les agents activés
    if AGENTS_CONFIG['amazon']['enabled']:
        agents.append(('Amazon', AmazonAgent()))
    
    if AGENTS_CONFIG['temu']['enabled']:
        agents.append(('Temu', TemuAgent()))
    
    if AGENTS_CONFIG['aliexpress']['enabled']:
        agents.append(('Aliexpress', AliexpressAgent()))
    
    # Exécuter les agents
    for name, agent in agents:
        try:
            logger.info(f"Exécution de l'agent {name}...")
            products = agent.scrape_best_sellers()
            results[name] = len(products)
            logger.info(f"Agent {name} terminé: {len(products)} produits scrapés")
        except Exception as e:
            logger.error(f"Erreur avec l'agent {name}: {e}")
            results[name] = 0
        finally:
            agent.close()
    
    # Résumé
    logger.info("=== Résumé du scraping ===")
    for name, count in results.items():
        logger.info(f"{name}: {count} produits")
    
    total = sum(results.values())
    logger.info(f"Total: {total} produits scrapés")
    logger.info("=== Fin du scraping ===")
    
    return results


if __name__ == '__main__':
    main()

