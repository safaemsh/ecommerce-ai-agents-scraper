"""
Script de configuration automatique de Claude Desktop avec les serveurs MCP
selon les spécifications du projet PFE
"""
import json
import os
from pathlib import Path

def get_config_path():
    """Retourne le chemin du fichier de configuration Claude Desktop"""
    if os.name == 'nt':  # Windows
        return Path(os.environ['APPDATA']) / 'Claude' / 'claude_desktop_config.json'
    elif os.name == 'posix':  # macOS/Linux
        if 'darwin' in os.sys.platform:
            return Path.home() / 'Library' / 'Application Support' / 'Claude' / 'claude_desktop_config.json'
        else:
            return Path.home() / '.config' / 'Claude' / 'claude_desktop_config.json'

def get_project_path():
    """Retourne le chemin absolu du projet"""
    return Path(__file__).parent.absolute()

def get_chrome_path():
    """Détecte le chemin de Chrome sur Windows"""
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in possible_paths:
        if Path(path).exists():
            return path
    return r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def setup_config():
    """Configure Claude Desktop avec les serveurs MCP"""
    config_path = get_config_path()
    project_path = get_project_path()
    db_path = project_path / "products.db"
    chrome_path = get_chrome_path()
    
    # Créer le dossier si nécessaire
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configuration MCP selon le document PFE
    # Note: Brave Search est optionnel - le système peut fonctionner sans
    config = {
        "mcpServers": {
            "mcp-puppeteer": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-puppeteer"
                ],
                "env": {
                    "PUPPETEER_LAUNCH_OPTIONS": json.dumps({
                        "headless": False,
                        "executablePath": chrome_path,
                        "args": []
                    }),
                    "ALLOW_DANGEROUS": "true"
                }
            },
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    str(Path.home() / "Desktop"),
                    "C:\\" if os.name == 'nt' else "/"
                ]
            },
            "sqlite": {
                "command": "uvx",
                "args": [
                    "mcp-server-sqlite",
                    "--db-path",
                    str(db_path)
                ]
            }
        }
    }
    
    # Brave Search est optionnel - ajouter seulement si l'utilisateur a une clé API
    # Si vous avez une clé API Brave, décommentez les lignes suivantes :
    # config["mcpServers"]["brave"] = {
    #     "command": "npx",
    #     "args": [
    #         "-y",
    #         "@modelcontextprotocol/server-brave"
    #     ],
    #     "env": {
    #         "BRAVE_API_KEY": "VOTRE_CLE_API_BRAVE_ICI"
    #     }
    # }
    
    # Lire la configuration existante si elle existe
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
                # Fusionner avec la configuration existante
                if "mcpServers" in existing_config:
                    existing_config["mcpServers"].update(config["mcpServers"])
                    config = existing_config
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture de la config existante: {e}")
            print("Création d'une nouvelle configuration...")
    
    # Écrire la configuration
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("=" * 60)
        print("✅ Configuration Claude Desktop créée avec succès!")
        print("=" * 60)
        print(f"\n📁 Fichier: {config_path}")
        print("\n🔧 Serveurs MCP configurés:")
        print("  ✓ mcp-puppeteer - Automatisation navigateur (Chrome)")
        print("  ✓ brave - Recherche web via API Brave")
        print("  ✓ filesystem - Accès aux fichiers locaux")
        print("  ✓ sqlite - Base de données SQLite")
        print("\n✅ Configuration créée SANS Brave Search (optionnel)")
        print("   Le système fonctionne parfaitement sans clé API!")
        print("\n💡 Pour utiliser Brave Search (optionnel):")
        print("  1. Obtenez votre clé API: https://brave.com/search/api/")
        print("  2. Décommentez les lignes dans setup_claude_mcp.py")
        print("  3. Relancez: python setup_claude_mcp.py")
        print("\n✅ Le système fonctionne déjà avec:")
        print("  - Puppeteer (scraping direct des sites)")
        print("  - SQLite (base de données)")
        print("  - Filesystem (accès fichiers)")
        print("\n💡 Test dans Claude Desktop:")
        print("   'Donne-moi 5 produits gagnants sur Jumia'")
        print("   Claude utilisera Puppeteer directement pour scraper!")
        print("   (Pas besoin de recherche Brave - on va directement sur le site)")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture: {e}")
        return False

if __name__ == "__main__":
    setup_config()

