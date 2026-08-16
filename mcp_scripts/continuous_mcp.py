"""
Serveur MCP pour scraping continu toutes les minutes
"""
import json
import sys
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
CONTINUOUS_SCRIPT = BASE_DIR / 'automation' / 'continuous_scraper.py'

# Flag pour arrêter le scraping continu
continuous_scraping_active = False
continuous_thread = None


def start_continuous_scraping():
    """Démarrer le scraping continu"""
    global continuous_scraping_active, continuous_thread
    
    if continuous_scraping_active:
        return {
            "status": "already_running",
            "message": "Le scraping continu est déjà en cours"
        }
    
    def run_continuous():
        global continuous_scraping_active
        try:
            continuous_scraping_active = True
            result = subprocess.run(
                ['python', str(CONTINUOUS_SCRIPT)],
                cwd=BASE_DIR,
                capture_output=False,
                text=True
            )
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            continuous_scraping_active = False
    
    continuous_thread = threading.Thread(target=run_continuous, daemon=True)
    continuous_thread.start()
    
    return {
        "status": "started",
        "message": "Scraping continu démarré (toutes les minutes)"
    }


def stop_continuous_scraping():
    """Arrêter le scraping continu"""
    global continuous_scraping_active
    continuous_scraping_active = False
    return {
        "status": "stopped",
        "message": "Scraping continu arrêté"
    }


def get_scraping_status():
    """Obtenir le statut du scraping"""
    global continuous_scraping_active
    return {
        "status": "running" if continuous_scraping_active else "stopped",
        "active": continuous_scraping_active
    }


def run_single_scraping():
    """Exécuter un scraping unique"""
    try:
        result = subprocess.run(
            ['python', str(BASE_DIR / 'main.py')],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=600  # Timeout de 10 minutes
        )
        return {
            "status": "success" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "message": "Le scraping a pris trop de temps"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def handle_mcp_request(request):
    """Gérer une requête MCP"""
    method = request.get('method', '')
    params = request.get('params', {})
    
    if method == 'start_continuous_scraping':
        return start_continuous_scraping()
    elif method == 'stop_continuous_scraping':
        return stop_continuous_scraping()
    elif method == 'get_scraping_status':
        return get_scraping_status()
    elif method == 'run_scraping':
        return run_single_scraping()
    elif method == 'get_stats':
        try:
            sys.path.insert(0, str(BASE_DIR))
            from database import DatabaseManager
            
            db = DatabaseManager()
            stats = {}
            
            for platform in ['amazon', 'temu', 'aliexpress']:
                products = db.get_products(platform=platform, limit=1000)
                stats[platform] = len(products)
            
            db.close()
            
            return {
                "status": "success",
                "stats": stats,
                "total": sum(stats.values()),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    else:
        return {
            "status": "error",
            "error": f"Méthode inconnue: {method}"
        }


if __name__ == '__main__':
    # Lecture de la requête depuis stdin
    try:
        request = json.load(sys.stdin)
        response = handle_mcp_request(request)
        print(json.dumps(response))
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": str(e)
        }))

