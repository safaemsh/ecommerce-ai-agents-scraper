"""
Script pour tester si les serveurs MCP peuvent être lancés
"""
import subprocess
import sys
from pathlib import Path

def test_npx_command():
    """Tester si npx fonctionne"""
    try:
        result = subprocess.run(['npx', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ npx fonctionne : {result.stdout.strip()}")
            return True
        else:
            print(f"❌ npx erreur : {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ npx n'est pas trouvé. Node.js est-il installé ?")
        return False
    except Exception as e:
        print(f"❌ Erreur avec npx : {e}")
        return False

def test_uvx_command():
    """Tester si uvx fonctionne"""
    try:
        result = subprocess.run(['uvx', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ uvx fonctionne : {result.stdout.strip()}")
            return True
        else:
            print(f"❌ uvx erreur : {result.stderr}")
            return False
    except FileNotFoundError:
        print("⚠️  uvx n'est pas trouvé (optionnel)")
        return False
    except Exception as e:
        print(f"❌ Erreur avec uvx : {e}")
        return False

def test_puppeteer_server():
    """Tester si le serveur Puppeteer peut être lancé"""
    try:
        print("\n🔍 Test du serveur Puppeteer MCP...")
        result = subprocess.run(
            ['npx', '-y', '@modelcontextprotocol/server-puppeteer', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 or 'puppeteer' in result.stdout.lower() or 'puppeteer' in result.stderr.lower():
            print("✅ Serveur Puppeteer MCP peut être lancé")
            return True
        else:
            print(f"⚠️  Puppeteer : {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"⚠️  Erreur Puppeteer : {str(e)[:100]}")
        return False

def main():
    """Fonction principale"""
    print("=" * 60)
    print("TEST DES OUTILS MCP")
    print("=" * 60)
    
    print("\n1. Test de npx (Node.js)...")
    npx_ok = test_npx_command()
    
    print("\n2. Test de uvx (optionnel)...")
    uvx_ok = test_uvx_command()
    
    print("\n3. Test du serveur Puppeteer MCP...")
    puppeteer_ok = test_puppeteer_server()
    
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print(f"npx (requis) : {'✅ OK' if npx_ok else '❌ PROBLÈME'}")
    print(f"uvx (optionnel) : {'✅ OK' if uvx_ok else '⚠️  Non installé'}")
    print(f"Puppeteer MCP : {'✅ OK' if puppeteer_ok else '❌ PROBLÈME'}")
    
    if not npx_ok:
        print("\n⚠️  INSTALLEZ Node.js : https://nodejs.org/")
    
    if npx_ok and not puppeteer_ok:
        print("\n💡 Essayez de lancer manuellement :")
        print("   npx -y @modelcontextprotocol/server-puppeteer")

if __name__ == "__main__":
    main()

