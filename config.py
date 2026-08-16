"""
Configuration du projet
"""
import os
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'products.db'
LOG_DIR = BASE_DIR / 'logs'
MCP_SCRIPTS_DIR = BASE_DIR / 'mcp_scripts'

# Créer les répertoires nécessaires
LOG_DIR.mkdir(exist_ok=True)
MCP_SCRIPTS_DIR.mkdir(exist_ok=True)

# Configuration des agents
AGENTS_CONFIG = {
    'amazon': {
        'enabled': True,
        'max_products': 100,
        'delay': 2,  # Délai entre les requêtes (secondes)
    },
    'temu': {
        'enabled': True,
        'max_products': 100,
        'delay': 3,  # Plus de délai pour Temu (JavaScript)
        'use_selenium': True,  # Utiliser Selenium pour JavaScript
    },
    'aliexpress': {
        'enabled': True,
        'max_products': 100,
        'delay': 2,
    }
}

# User agents pour éviter la détection
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
]

# Configuration n8n (si utilisé via API)
N8N_API_URL = os.getenv('N8N_API_URL', 'http://localhost:5678')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', '')

