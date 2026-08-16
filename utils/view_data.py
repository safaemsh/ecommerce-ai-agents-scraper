"""
Utilitaire pour visualiser les données de la base
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from database import DatabaseManager
from tabulate import tabulate


def view_products(platform=None, limit=20):
    """Afficher les produits de la base de données"""
    db = DatabaseManager()
    
    try:
        products = db.get_products(platform=platform, limit=limit)
        
        if not products:
            print("Aucun produit trouvé dans la base de données.")
            return
        
        # Préparer les données pour l'affichage
        table_data = []
        for product in products:
            table_data.append([
                product.id,
                product.platform,
                product.title[:50] + "..." if len(product.title) > 50 else product.title,
                f"{product.price:.2f} €" if product.price else "N/A",
                f"{product.rating:.1f}" if product.rating else "N/A",
                product.reviews_count or "N/A",
                product.scraped_at.strftime("%Y-%m-%d %H:%M") if product.scraped_at else "N/A"
            ])
        
        headers = ["ID", "Plateforme", "Titre", "Prix", "Note", "Avis", "Date"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal: {len(products)} produits affichés")
        
    finally:
        db.close()


def get_statistics():
    """Afficher les statistiques de la base de données"""
    db = DatabaseManager()
    
    try:
        stats = {}
        for platform in ['amazon', 'temu', 'aliexpress']:
            products = db.get_products(platform=platform, limit=10000)
            stats[platform] = len(products)
        
        total = sum(stats.values())
        
        print("\n=== Statistiques de la Base de Données ===\n")
        for platform, count in stats.items():
            print(f"{platform.capitalize()}: {count} produits")
        print(f"\nTotal: {total} produits")
        
    finally:
        db.close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualiser les données de la base')
    parser.add_argument('--platform', choices=['amazon', 'temu', 'aliexpress'], help='Filtrer par plateforme')
    parser.add_argument('--limit', type=int, default=20, help='Nombre de produits à afficher')
    parser.add_argument('--stats', action='store_true', help='Afficher les statistiques')
    
    args = parser.parse_args()
    
    if args.stats:
        get_statistics()
    else:
        view_products(platform=args.platform, limit=args.limit)

