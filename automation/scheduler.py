"""
Script d'automatisation avec planification des tâches
"""
import schedule
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent


def run_daily_scraping():
    """Exécuter le scraping quotidien"""
    logger.info("=== Démarrage du scraping automatique ===")
    try:
        result = subprocess.run(
            ['python', str(BASE_DIR / 'main.py')],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("Scraping terminé avec succès")
            logger.info(result.stdout)
        else:
            logger.error(f"Erreur lors du scraping: {result.stderr}")
        
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Erreur: {e}")
        return False


def generate_daily_report():
    """Générer un rapport quotidien"""
    logger.info("Génération du rapport quotidien...")
    try:
        from database import DatabaseManager
        
        db = DatabaseManager()
        report = {
            "date": datetime.now().isoformat(),
            "platforms": {}
        }
        
        for platform in ['amazon', 'temu', 'aliexpress']:
            products = db.get_products(platform=platform, limit=1000)
            report["platforms"][platform] = len(products)
        
        report["total"] = sum(report["platforms"].values())
        
        # Sauvegarder le rapport
        reports_dir = BASE_DIR / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / f"report_{datetime.now().strftime('%Y%m%d')}.json"
        import json
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        db.close()
        logger.info(f"Rapport sauvegardé: {report_file}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la génération du rapport: {e}")
        return False


def main():
    """Planifier les tâches automatiques"""
    # Planifier le scraping quotidien à 2h du matin
    schedule.every().day.at("02:00").do(run_daily_scraping)
    
    # Planifier le rapport quotidien à 3h du matin
    schedule.every().day.at("03:00").do(generate_daily_report)
    
    logger.info("Planificateur démarré")
    logger.info("Scraping planifié tous les jours à 02:00")
    logger.info("Rapport planifié tous les jours à 03:00")
    
    # Boucle principale
    while True:
        schedule.run_pending()
        time.sleep(60)  # Vérifier toutes les minutes


if __name__ == '__main__':
    main()

