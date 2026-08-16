"""
Utilitaires pour exporter les données
"""
import json
import csv
from pathlib import Path
from database import DatabaseManager
import pandas as pd
from datetime import datetime

def export_to_csv(output_file='products_export.csv'):
    """Exporter les produits vers CSV"""
    db = DatabaseManager()
    try:
        products = db.get_products(limit=10000)
        
        data = []
        for p in products:
            data.append({
                'ID': p.id,
                'Plateforme': p.platform,
                'Titre': p.title,
                'Prix': p.price or '',
                'Note': p.rating or '',
                'Nombre_Avis': p.reviews_count or '',
                'URL': p.product_url,
                'Image_URL': p.image_url or '',
                'Description': p.description or '',
                'Rang_Vente': p.sales_rank or '',
                'Categorie': p.category or '',
                'Date_Scraping': p.scraped_at.isoformat() if p.scraped_at else '',
            })
        
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"✅ Export CSV créé: {output_file} ({len(data)} produits)")
        return output_file
    finally:
        db.close()

def export_to_json(output_file='products_export.json'):
    """Exporter les produits vers JSON"""
    db = DatabaseManager()
    try:
        products = db.get_products(limit=10000)
        
        data = []
        for p in products:
            data.append({
                'id': p.id,
                'platform': p.platform,
                'title': p.title,
                'price': p.price,
                'rating': p.rating,
                'reviews_count': p.reviews_count,
                'product_url': p.product_url,
                'image_url': p.image_url,
                'description': p.description,
                'sales_rank': p.sales_rank,
                'category': p.category,
                'scraped_at': p.scraped_at.isoformat() if p.scraped_at else None,
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Export JSON créé: {output_file} ({len(data)} produits)")
        return output_file
    finally:
        db.close()

def export_to_excel(output_file='products_export.xlsx'):
    """Exporter les produits vers Excel"""
    db = DatabaseManager()
    try:
        products = db.get_products(limit=10000)
        
        data = []
        for p in products:
            data.append({
                'ID': p.id,
                'Plateforme': p.platform,
                'Titre': p.title,
                'Prix': p.price or '',
                'Note': p.rating or '',
                'Nombre_Avis': p.reviews_count or '',
                'URL': p.product_url,
                'Image_URL': p.image_url or '',
                'Description': p.description or '',
                'Rang_Vente': p.sales_rank or '',
                'Categorie': p.category or '',
                'Date_Scraping': p.scraped_at.isoformat() if p.scraped_at else '',
            })
        
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"✅ Export Excel créé: {output_file} ({len(data)} produits)")
        return output_file
    finally:
        db.close()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Exporter les données')
    parser.add_argument('--format', choices=['csv', 'json', 'excel', 'all'], default='csv',
                        help='Format d\'export')
    parser.add_argument('--output', help='Fichier de sortie')
    
    args = parser.parse_args()
    
    if args.format == 'csv' or args.format == 'all':
        export_to_csv(args.output or 'products_export.csv')
    if args.format == 'json' or args.format == 'all':
        export_to_json(args.output or 'products_export.json')
    if args.format == 'excel' or args.format == 'all':
        try:
            export_to_excel(args.output or 'products_export.xlsx')
        except ImportError:
            print("⚠️ openpyxl non installé. Installez-le avec: pip install openpyxl")

