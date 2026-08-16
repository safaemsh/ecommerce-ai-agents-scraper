"""
Frontend Streamlit moderne pour visualiser les produits scrapés
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import DatabaseManager
from datetime import datetime, timedelta
import time
import threading
from pathlib import Path
import sys
import re

# Ajouter le répertoire parent au path
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configuration de la page avec design moderne
st.set_page_config(
    page_title="Dashboard Produits E-commerce",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS moderne et professionnel
st.markdown("""
    <style>
    /* Variables de couleur */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --danger-color: #d62728;
        --bg-color: #f8f9fa;
        --card-bg: #ffffff;
        --text-color: #333333;
        --border-color: #e0e0e0;
    }
    
    /* Style général */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header moderne */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        padding: 1rem;
    }
    
    /* Cartes de produits modernes */
    .product-card-modern {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid var(--border-color);
    }
    
    .product-card-modern:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Badge plateforme */
    .platform-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .platform-amazon {
        background: linear-gradient(135deg, #FF9900 0%, #FFB84D 100%);
        color: white;
    }
    
    .platform-temu {
        background: linear-gradient(135deg, #E50000 0%, #FF3333 100%);
        color: white;
    }
    
    .platform-aliexpress {
        background: linear-gradient(135deg, #FF6600 0%, #FF8833 100%);
        color: white;
    }
    
    /* Image placeholder moderne */
    .image-placeholder {
        width: 150px;
        height: 150px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        color: white;
        font-size: 0.9rem;
        text-align: center;
        padding: 0.5rem;
    }
    
    /* Métriques modernes */
    .metric-modern {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--primary-color);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Boutons modernes */
    .stButton>button {
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar moderne */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=30)
def get_products_data(platform=None):
    """Récupérer les produits de la base de données avec nettoyage complet"""
    db = DatabaseManager()
    try:
        products = db.get_products(platform=platform, limit=1000)
        data = []
        seen_urls = set()
        
        for p in products:
            # Normaliser URL pour déduplication
            product_url = p.product_url if p.product_url else None
            image_url = p.image_url if p.image_url else None
            
            def clean_url(url, platform):
                if not url or not url.strip():
                    return None
                url = str(url).strip()
                
                # Supprimer doubles domaines
                if url.count('www.') > 1:
                    last_www = url.rfind('www.')
                    if last_www >= 0:
                        url = 'https://' + url[last_www:]
                
                # Supprimer doubles slashes
                if url.startswith('https://'):
                    url = 'https://' + url[8:].replace('//', '/')
                elif url.startswith('http://'):
                    url = 'http://' + url[7:].replace('//', '/')
                
                # Protocole manquant
                if url.startswith('//'):
                    url = 'https:' + url
                elif url.startswith('/') and not url.startswith('//'):
                    if platform == 'amazon':
                        url = 'https://www.amazon.fr' + url
                    elif platform == 'temu':
                        url = 'https://www.temu.com' + url
                    elif platform == 'aliexpress':
                        url = 'https://www.aliexpress.com' + url
                
                # Validation basique
                if not url.startswith('http'):
                    return None
                
                return url
            
            # Nettoyer URLs
            if product_url:
                product_url = clean_url(product_url, p.platform)
            if image_url:
                image_url = clean_url(image_url, p.platform)
            
            # Déduplication par URL normalisée
            if product_url:
                # Extraire ID unique pour déduplication
                url_key = product_url
                if '/item/' in url_key:
                    item_id = url_key.split('/item/')[-1].split('/')[0].split('?')[0]
                    if item_id:
                        url_key = f"{p.platform}_item_{item_id}"
                elif '/dp/' in url_key:
                    asin = url_key.split('/dp/')[-1].split('/')[0].split('?')[0]
                    if asin:
                        url_key = f"{p.platform}_dp_{asin}"
                
                if url_key in seen_urls:
                    continue
                seen_urls.add(url_key)
            
            # Nettoyer le titre
            title = p.title if p.title else 'Titre non disponible'
            if title:
                title = re.sub(r'MAD\d+[.,]\d+', '', title)
                title = re.sub(r'€\s*\d+[.,]\d+', '', title)
                title = re.sub(r'\d+[.,]\d+\s*-\s*\d+%', '', title)
                title = re.sub(r'\d+[.,]\d+\s+sold', '', title, flags=re.IGNORECASE)
                title = ' '.join(title.split())
                if len(title) > 200:
                    title = title[:200] + "..."
            
            data.append({
                'ID': p.id,
                'Plateforme': p.platform if p.platform else 'Inconnue',
                'Titre': title,
                'Prix': float(p.price) if p.price else None,
                'Note': float(p.rating) if p.rating else None,
                'Avis': int(p.reviews_count) if p.reviews_count else None,
                'Image': image_url,
                'URL': product_url,
                'Rang': int(p.sales_rank) if p.sales_rank else None,
                'Date': p.scraped_at.strftime("%Y-%m-%d %H:%M") if p.scraped_at else "",
            })
        
        return pd.DataFrame(data)
    finally:
        db.close()


@st.cache_data(ttl=30)
def get_statistics():
    """Obtenir les statistiques"""
    db = DatabaseManager()
    try:
        stats = {}
        for platform in ['amazon', 'temu', 'aliexpress']:
            products = db.get_products(platform=platform, limit=10000)
            stats[platform] = len(products)
        
        all_products = []
        for platform in ['amazon', 'temu', 'aliexpress']:
            products = db.get_products(platform=platform, limit=10000)
            for p in products:
                if p.price:
                    all_products.append({
                        'platform': platform,
                        'price': p.price,
                        'rating': p.rating or 0,
                    })
        
        return stats, pd.DataFrame(all_products)
    finally:
        db.close()


def run_scraping_stream():
    """Lancer le scraping en arrière-plan"""
    from main import main as run_scraping
    
    placeholder = st.empty()
    with placeholder.container():
        st.info("🔄 Scraping en cours...")
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        status_text.text("Initialisation des agents...")
        progress_bar.progress(10)
        
        def scrape_thread():
            nonlocal results
            results = run_scraping()
        
        results = {}
        thread = threading.Thread(target=scrape_thread)
        thread.start()
        
        for i in range(20, 100, 10):
            time.sleep(1)
            progress_bar.progress(i)
            status_text.text(f"Scraping en cours... ({i}%)")
        
        thread.join(timeout=300)
        progress_bar.progress(100)
        status_text.text("✅ Scraping terminé!")
        
        time.sleep(1)
        placeholder.empty()
        
        if results:
            st.success(f"✅ Scraping terminé: {sum(results.values())} produits scrapés")
            st.json(results)
            st.cache_data.clear()
            st.rerun()
    except Exception as e:
        st.error(f"❌ Erreur: {e}")


def main():
    """Fonction principale"""
    st.markdown('<h1 class="main-header">🛒 Dashboard E-commerce Produits</h1>', unsafe_allow_html=True)
    
    # Sidebar moderne
    with st.sidebar:
        st.markdown("### 📊 Navigation")
        page = st.radio("", ["Dashboard", "Produits", "Statistiques", "Scraping Live"], label_visibility="collapsed")
        
        st.divider()
        st.markdown("### 🔍 Filtres")
        platform_filter = st.selectbox("Plateforme", ["Toutes", "amazon", "temu", "aliexpress"])
        
        st.divider()
        st.markdown("### ⚙️ Actions")
        if st.button("🔄 Actualiser", use_container_width=True, type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    # Page Dashboard
    if page == "Dashboard":
        st.header("📊 Vue d'ensemble")
        
        stats, price_df = get_statistics()
        
        # Métriques modernes
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Produits", sum(stats.values()), delta=None)
        with col2:
            st.metric("Amazon", stats.get('amazon', 0))
        with col3:
            st.metric("Temu", stats.get('temu', 0))
        with col4:
            st.metric("Aliexpress", stats.get('aliexpress', 0))
        
        # Graphiques
        if stats:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie = px.pie(
                    values=list(stats.values()),
                    names=list(stats.keys()),
                    title="Répartition par Plateforme",
                    color_discrete_map={
                        'amazon': '#FF9900',
                        'temu': '#E50000',
                        'aliexpress': '#FF6600'
                    }
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                fig_bar = px.bar(
                    x=list(stats.keys()),
                    y=list(stats.values()),
                    title="Nombre de Produits",
                    color=list(stats.keys()),
                    color_discrete_map={
                        'amazon': '#FF9900',
                        'temu': '#E50000',
                        'aliexpress': '#FF6600'
                    }
                )
                st.plotly_chart(fig_bar, use_container_width=True)
    
    # Page Produits
    elif page == "Produits":
        st.header("📦 Catalogue des Produits")
        
        platform = None if platform_filter == "Toutes" else platform_filter
        df = get_products_data(platform=platform)
        
        # Afficher les statistiques par plateforme
        if df.empty:
            st.warning("⚠️ Aucun produit trouvé dans la base de données.")
            st.info("💡 Lancez le scraping depuis la page 'Scraping Live' pour ajouter des produits.")
        else:
            # Statistiques par plateforme
            platform_stats = df.groupby('Plateforme').size()
            stats_cols = st.columns(len(platform_stats) if len(platform_stats) > 0 else 1)
            for idx, (platform, count) in enumerate(platform_stats.items()):
                with stats_cols[idx % len(stats_cols)]:
                    st.metric(platform.upper(), count)
            
            # Barre de recherche et filtres
            col1, col2 = st.columns([3, 1])
            with col1:
                search_term = st.text_input("🔍 Rechercher un produit", placeholder="Tapez le nom d'un produit...", key="search")
            with col2:
                view_mode = st.selectbox("Affichage", ["Grille", "Liste"], key="view_mode")
            
            # Filtrer par recherche
            if search_term:
                df = df[df['Titre'].str.contains(search_term, case=False, na=False)]
            
            # Filtres avancés
            with st.expander("🔽 Filtres Avancés", expanded=False):
                filter_col1, filter_col2, filter_col3 = st.columns(3)
                with filter_col1:
                    min_price = st.number_input("💰 Prix min (€)", min_value=0.0, value=0.0, step=1.0)
                with filter_col2:
                    max_price_val = float(df['Prix'].max()) if not df.empty and df['Prix'].notna().any() else 1000.0
                    max_price = st.number_input("💰 Prix max (€)", min_value=0.0, value=max_price_val, step=10.0)
                with filter_col3:
                    min_rating = st.number_input("⭐ Note min", min_value=0.0, max_value=5.0, value=0.0, step=0.5)
            
            # Appliquer filtres
            if not df.empty:
                mask_price = (df['Prix'].isna()) | (df['Prix'] == 0) | ((df['Prix'] >= min_price) & (df['Prix'] <= max_price))
                df = df[mask_price]
                if min_rating > 0:
                    mask_rating = (df['Note'].isna()) | (df['Note'] == 0) | (df['Note'] >= min_rating)
                    df = df[mask_rating]
            
            st.markdown(f"### 📦 **{len(df)} produit(s) unique(s) trouvé(s)**")
            
            # Affichage selon le mode
            if view_mode == "Grille":
                # Affichage en grille moderne (3 colonnes)
                num_cols = 3
                cols = st.columns(num_cols)
                
                for idx, (_, row) in enumerate(df.iterrows()):
                    col_idx = idx % num_cols
                    with cols[col_idx]:
                        # Carte produit moderne
                        st.markdown('<div class="product-card-modern">', unsafe_allow_html=True)
                        
                        # Image
                        image_url = row['Image'] if pd.notna(row['Image']) else None
                        if image_url and len(str(image_url)) > 10:
                            try:
                                st.image(str(image_url), use_container_width=True)
                            except:
                                st.markdown('<div class="image-placeholder">Image non disponible</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="image-placeholder">Pas d\'image</div>', unsafe_allow_html=True)
                        
                        # Badge plateforme
                        platform_name = row['Plateforme'].upper() if pd.notna(row['Plateforme']) else "INCONNU"
                        platform_class = f"platform-{row['Plateforme'].lower()}" if pd.notna(row['Plateforme']) else ""
                        st.markdown(f'<div class="platform-badge {platform_class}">{platform_name}</div>', unsafe_allow_html=True)
                        
                        # Titre
                        title = str(row['Titre'])[:80] if pd.notna(row['Titre']) else "Titre non disponible"
                        st.markdown(f"**{title}**")
                        
                        # Prix en grand
                        if pd.notna(row['Prix']) and row['Prix'] > 0:
                            st.markdown(f'<h3 style="color: #d62728; margin: 0.5rem 0;">💰 {row["Prix"]:.2f} €</h3>', unsafe_allow_html=True)
                        
                        # Note
                        if pd.notna(row['Note']) and row['Note'] > 0:
                            st.write(f"⭐ {row['Note']:.1f}/5")
                        
                        # Lien produit avec validation
                        product_url = row['URL'] if pd.notna(row['URL']) else None
                        if product_url and product_url.startswith('http'):
                            st.markdown(f'<a href="{product_url}" target="_blank" rel="noopener" style="display:block;text-align:center;padding:0.5rem;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;text-decoration:none;border-radius:5px;margin-top:0.5rem;font-weight:bold;">Voir le produit →</a>', unsafe_allow_html=True)
                        else:
                            st.caption("🔗 URL non disponible")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
            else:
                # Affichage en liste
                for idx, row in df.iterrows():
                    with st.container():
                        st.markdown('<div class="product-card-modern">', unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns([2, 5, 1])
                        
                        with col1:
                            image_url = row['Image'] if pd.notna(row['Image']) else None
                            if image_url and len(str(image_url)) > 10:
                                try:
                                    st.image(str(image_url), width=200)
                                except:
                                    st.markdown('<div class="image-placeholder">Image non disponible</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="image-placeholder">Pas d\'image</div>', unsafe_allow_html=True)
                        
                        with col2:
                            title = str(row['Titre'])[:150] if pd.notna(row['Titre']) else "Titre non disponible"
                            st.markdown(f"### {title}")
                            
                            info_col1, info_col2, info_col3 = st.columns(3)
                            with info_col1:
                                if pd.notna(row['Prix']) and row['Prix'] > 0:
                                    st.metric("💰 Prix", f"{row['Prix']:.2f} €")
                                else:
                                    st.write("💰 Prix: N/A")
                            with info_col2:
                                if pd.notna(row['Note']) and row['Note'] > 0:
                                    st.metric("⭐ Note", f"{row['Note']:.1f}/5")
                                else:
                                    st.write("⭐ Note: N/A")
                            with info_col3:
                                st.caption(f"📅 {row['Date']}")
                            
                            product_url = row['URL'] if pd.notna(row['URL']) else None
                            if product_url and product_url.startswith('http'):
                                st.markdown(f'<a href="{product_url}" target="_blank" rel="noopener" style="color: #667eea; font-weight: bold;">🔗 Voir le produit →</a>', unsafe_allow_html=True)
                        
                        with col3:
                            platform_name = row['Plateforme'].upper() if pd.notna(row['Plateforme']) else "INCONNU"
                            platform_class = f"platform-{row['Plateforme'].lower()}" if pd.notna(row['Plateforme']) else ""
                            st.markdown(f'<div class="platform-badge {platform_class}">{platform_name}</div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
    
    # Page Statistiques
    elif page == "Statistiques":
        st.header("📈 Statistiques Détaillées")
        stats, price_df = get_statistics()
        df = get_products_data()
        
        if not df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                price_data = df[df['Prix'] > 0]['Prix']
                if not price_data.empty:
                    fig_hist = px.histogram(price_data, nbins=30, title="Distribution des Prix")
                    st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                rating_data = df[df['Note'] > 0]['Note']
                if not rating_data.empty:
                    fig_rating = px.histogram(rating_data, nbins=20, title="Distribution des Notes")
                    st.plotly_chart(fig_rating, use_container_width=True)
    
    # Page Scraping Live
    elif page == "Scraping Live":
        st.header("🔄 Scraping en Temps Réel")
        
        if st.button("🚀 Lancer le Scraping", type="primary", use_container_width=True):
            run_scraping_stream()


if __name__ == "__main__":
    main()
