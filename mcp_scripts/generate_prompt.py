"""
Script MCP pour générer des prompts automatisés pour Claude Desktop
"""
import json
import sys
from datetime import datetime
from pathlib import Path

def generate_daily_prompt():
    """Générer un prompt quotidien pour le scraping"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    prompt = f"""
# Prompt de Scraping Automatisé - {today}

Bonjour, veuillez exécuter le système de scraping multi-agents pour récupérer les produits les plus vendus des plateformes suivantes:

1. **Amazon** - Scraper les meilleures ventes
2. **Temu** - Scraper les produits populaires
3. **Aliexpress** - Scraper les meilleures ventes

## Instructions:
- Exécuter le script: `python main.py`
- Vérifier les logs dans `logs/scraping.log`
- Vérifier les données dans la base SQLite: `products.db`
- Générer un rapport des produits scrapés

## Objectifs:
- Collecter au moins 50 produits par plateforme
- Mettre à jour la base de données
- Préparer les données pour analyse

Date d'exécution: {today}
"""
    
    return prompt


def save_prompt(prompt, filename=None):
    """Sauvegarder le prompt dans un fichier"""
    if filename is None:
        filename = f"prompt_{datetime.now().strftime('%Y%m%d')}.txt"
    
    prompts_dir = Path(__file__).parent.parent / 'prompts'
    prompts_dir.mkdir(exist_ok=True)
    
    filepath = prompts_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    return filepath


def main():
    """Point d'entrée principal"""
    prompt = generate_daily_prompt()
    filepath = save_prompt(prompt)
    
    print(json.dumps({
        "prompt": prompt,
        "filepath": str(filepath),
        "status": "success"
    }))
    
    return prompt


if __name__ == '__main__':
    main()

