"""
Serveur MCP pour intégration avec Claude Desktop
Ce script peut être utilisé comme serveur MCP pour automatiser les tâches
"""
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def run_scraping():
    """Exécuter le scraping via MCP"""
    try:
        result = subprocess.run(
            ['python', 'main.py'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        return {
            "status": "success" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def get_database_stats():
    """Obtenir les statistiques de la base de données"""
    try:
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
            "total": sum(stats.values())
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
    
    if method == 'run_scraping':
        return run_scraping()
    elif method == 'get_stats':
        return get_database_stats()
    elif method == 'generate_prompt':
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        from generate_prompt import generate_daily_prompt
        return {
            "status": "success",
            "prompt": generate_daily_prompt()
        }
    else:
        return {
            "status": "error",
            "error": f"Méthode inconnue: {method}"
        }


if __name__ == '__main__':
    # Lecture de la requête depuis stdin
    request = json.load(sys.stdin)
    response = handle_mcp_request(request)
    print(json.dumps(response))

