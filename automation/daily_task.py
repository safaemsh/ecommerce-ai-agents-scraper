"""
Tâche quotidienne à exécuter (peut être appelée par n8n ou cron)
"""
import sys
import logging
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from main import main as run_scraping
from database import DatabaseManager
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def daily_task():
    """Tâche quotidienne complète"""
    logger.info("=== Démarrage de la tâche quotidienne ===")
    
    # 1. Exécuter le scraping
    results = run_scraping()
    
    # 2. Générer un rapport
    db = DatabaseManager()
    report = {
        "date": datetime.now().isoformat(),
        "scraping_results": results,
        "database_stats": {}
    }
    
    for platform in ['amazon', 'temu', 'aliexpress']:
        products = db.get_products(platform=platform, limit=1000)
        report["database_stats"][platform] = len(products)
    
    report["database_stats"]["total"] = sum(report["database_stats"].values())
    db.close()
    
    # 3. Sauvegarder le rapport
    reports_dir = BASE_DIR / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    report_file = reports_dir / f"daily_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Rapport sauvegardé: {report_file}")
    logger.info("=== Fin de la tâche quotidienne ===")
    
    return report


if __name__ == '__main__':
    daily_task()

