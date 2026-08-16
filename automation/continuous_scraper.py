"""
Scraper continu avec exécution toutes les minutes
"""
import schedule
import time
import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from main import main as run_scraping

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / 'logs' / 'continuous_scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def scraping_job():
    """Tâche de scraping à exécuter"""
    logger.info("=" * 60)
    logger.info("Démarrage du scraping automatique")
    logger.info("=" * 60)
    
    try:
        results = run_scraping()
        logger.info("Scraping terminé avec succès")
        logger.info(f"Résultats: {results}")
        return results
    except Exception as e:
        logger.error(f"Erreur lors du scraping: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Lancer le scraper continu"""
    logger.info("Démarrage du scraper continu")
    logger.info("Scraping programmé toutes les minutes")
    logger.info("Appuyez sur Ctrl+C pour arrêter")
    
    # Planifier le scraping toutes les minutes
    schedule.every(1).minutes.do(scraping_job)
    
    # Exécuter immédiatement une première fois
    logger.info("Exécution initiale...")
    scraping_job()
    
    # Boucle principale
    try:
        while True:
            schedule.run_pending()
            time.sleep(10)  # Vérifier toutes les 10 secondes
    except KeyboardInterrupt:
        logger.info("Arrêt du scraper continu demandé")
        logger.info("Arrêt en cours...")


if __name__ == '__main__':
    main()

