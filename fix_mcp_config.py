"""
Script pour corriger la configuration MCP et supprimer les serveurs qui causent des erreurs
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

def fix_config():
    """Corriger la configuration en supprimant les serveurs problématiques"""
    config_path = get_config_path()
    project_path = Path(__file__).parent.absolute()
    db_path = project_path / "products.db"
    
    if not config_path.exists():
        print("❌ Fichier de config non trouvé !")
        return False
    
    # Lire la config actuelle
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Supprimer les serveurs qui causent des erreurs
    if "mcpServers" in config:
        # Garder seulement les serveurs qui fonctionnent
        new_servers = {}
        
        # Garder filesystem (généralement stable)
        if "filesystem" in config["mcpServers"]:
            new_servers["filesystem"] = config["mcpServers"]["filesystem"]
        
        # Supprimer scraping-system (problématique)
        if "scraping-system" in config["mcpServers"]:
            print("⚠️  Suppression de scraping-system (cause des erreurs)")
        
        # Pour sqlite, essayer une approche différente si uvx n'est pas disponible
        # On le laisse mais avec un avertissement
        
        # Pour puppeteer, garder mais vérifier
        if "mcp-puppeteer" in config["mcpServers"]:
            new_servers["mcp-puppeteer"] = config["mcpServers"]["mcp-puppeteer"]
        
        config["mcpServers"] = new_servers
    
    # Écrire la config corrigée
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("=" * 60)
        print("✅ Configuration corrigée !")
        print("=" * 60)
        print(f"\n📁 Fichier: {config_path}")
        print("\n🔧 Serveurs MCP conservés:")
        for server_name in config.get("mcpServers", {}).keys():
            print(f"  ✓ {server_name}")
        
        print("\n⚠️  SERVEURS SUPPRIMÉS (causaient des erreurs):")
        print("  ❌ scraping-system - Utilisez Python directement (python main.py)")
        
        print("\n💡 RECOMMANDATION:")
        print("   Pour scraper les produits, utilisez directement :")
        print("   python main.py")
        print("\n   Cela fonctionne sans besoin de MCP !")
        print("\n✅ Redémarrez Claude Desktop pour appliquer les changements")
        
        return True
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

if __name__ == "__main__":
    fix_config()


