# 🛒 Système Intelligent d'Analyse des Produits Best-Sellers E-commerce

**Projet de Fin d'Études - Licence Sciences Mathématiques et Informatique**  
**Université Ibn Zohr - Faculté des Sciences**

---

## 📖 Description du Projet

Système intelligent d'analyse des produits les plus demandés sur les plateformes e-commerce via des **agents IA communicants (MCP)** et **automatisation no-code avec n8n**.

Le système permet de :
- ✅ Scraper automatiquement les best-sellers de multiples plateformes (Amazon, AliExpress, Temu, Jumia)
- ✅ Analyser les tendances en temps réel grâce à des agents IA
- ✅ Visualiser les résultats via une interface Streamlit moderne
- ✅ Automatiser les workflows via n8n avec déclenchement Telegram
- ✅ Stocker les données dans SQLite et Google Sheets

---

## 🏗️ Architecture du Système

### Partie 1 : Agent IA basé sur MCP
- **Claude Desktop** : Interface principale avec agents IA
- **Serveurs MCP** :
  - `mcp-server-puppeteer` : Automatisation navigateur pour scraping
  - `mcp-server-sqlite` : Base de données locale
  - `mcp-server-brave-search` : Recherche web
  - `mcp-server-filesystem` : Accès aux fichiers
- **Streamlit** : Visualisation des produits scrapés

### Partie 2 : Automatisation avec n8n
- **Workflow Telegram** : Déclenchement via messages texte/vocal
- **OpenAI/GPT** : Analyse intelligente des requêtes
- **Scraping automatisé** : Extraction multi-plateformes
- **Google Sheets** : Stockage des résultats
- **Streamlit Marketplace** : Interface de visualisation

---

## 🚀 Installation

### Prérequis

```bash
# 1. Claude Desktop
# Télécharger depuis: https://claude.ai/download

# 2. Node.js et npm
# Télécharger depuis: https://nodejs.org/

# 3. Python 3.8+
# Télécharger depuis: https://www.python.org/downloads/

# 4. uv (optionnel mais recommandé)
# https://docs.astral.sh/uv/

# 5. n8n
npm install -g n8n
```

### Installation des dépendances Python

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration Claude Desktop MCP

### Étape 1 : Configuration automatique

```bash
python setup_claude_mcp.py
```

### Étape 2 : Configuration manuelle (si nécessaire)

Ouvrir le fichier : `%APPDATA%\Claude\claude_desktop_config.json`

Ajouter la configuration suivante :

```json
{
  "mcpServers": {
    "mcp-puppeteer": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-puppeteer"
      ],
      "env": {
        "PUPPETEER_LAUNCH_OPTIONS": "{\"headless\": false, \"executablePath\": \"C:/Program Files/Google/Chrome/Application/chrome.exe\", \"args\": []}",
        "ALLOW_DANGEROUS": "true"
      }
    },
    "brave": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave"
      ],
      "env": {
        "BRAVE_API_KEY": "VOTRE_CLE_API_BRAVE"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\VOTRE_USERNAME\\Desktop",
        "C:\\"
      ]
    },
    "sqlite": {
      "command": "uvx",
      "args": [
        "mcp-server-sqlite",
        "--db-path",
        "C:\\Users\\VOTRE_USERNAME\\Desktop\\projet_sys_rep\\products.db"
      ]
    }
  }
}
```

**Important** : Remplacer `VOTRE_USERNAME` et `VOTRE_CLE_API_BRAVE` par vos valeurs.

### Étape 3 : Redémarrer Claude Desktop

---

## 💻 Utilisation

### Méthode 1 : Via Claude Desktop (Agent IA)

1. **Lancer Claude Desktop**
2. **Demander à Claude** :

```
Donne-moi 5 produits gagnants sur Jumia. 
Pour chaque produit, donne : 
- le nom
- le prix
- le lien vers le produit
- petite description.
Puis stocke les résultats dans la base SQLite.
```

Claude utilisera automatiquement :
- **Brave Search** pour trouver les pages pertinentes
- **Puppeteer** pour extraire les données
- **SQLite** pour stocker les résultats

### Méthode 2 : Via Script Python

```bash
python main.py
```

### Méthode 3 : Via Frontend Streamlit

```bash
streamlit run frontend/app.py
```

Ouvrir : **http://localhost:8501**

### Méthode 4 : Via n8n Workflow

1. **Lancer n8n** :
```bash
n8n start
```

2. **Ouvrir** : http://localhost:5678

3. **Importer le workflow** : `n8n_workflows/workflow_best_sellers.json`

4. **Envoyer un message Telegram** au bot pour déclencher le scraping

---

## 📁 Structure du Projet

```
projet_sys_rep/
├── agents/                    # Agents de scraping
│   ├── base_agent.py
│   ├── amazon_agent.py
│   ├── temu_agent.py
│   └── aliexpress_agent.py
│
├── frontend/                  # Interface Streamlit
│   └── app.py
│
├── n8n_workflows/             # Workflows n8n
│   └── workflow_best_sellers.json
│
├── database.py                # Gestion SQLite
├── main.py                    # Point d'entrée
├── config.py                  # Configuration
├── setup_claude_mcp.py       # Configuration MCP automatique
├── requirements.txt           # Dépendances Python
└── README.md                  # Ce fichier
```

---

## 🛠️ Fonctionnalités

### ✅ Scraping Multi-Plateformes
- Amazon
- AliExpress
- Temu
- Jumia (et autres plateformes)

### ✅ Agents IA Intelligents
- Compréhension contextuelle des requêtes
- Extraction automatique des données
- Gestion des popups et cookies
- Adaptation aux structures HTML variables

### ✅ Visualisation
- Interface Streamlit moderne
- Graphiques interactifs
- Recherche et filtres avancés
- Export des données (CSV, JSON, Excel)

### ✅ Automatisation n8n
- Déclenchement via Telegram (texte/vocal)
- Workflow intelligent avec IA
- Sauvegarde automatique Google Sheets
- Réponses dynamiques personnalisées

---

## 📊 Base de Données SQLite

### Structure de la table `products`

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER | Identifiant unique |
| title | TEXT | Nom du produit |
| price | REAL | Prix |
| url | TEXT | Lien vers le produit |
| image_url | TEXT | URL de l'image |
| platform | TEXT | Plateforme (amazon, temu, etc.) |
| rating | REAL | Note moyenne |
| reviews_count | INTEGER | Nombre d'avis |
| description | TEXT | Description |
| scraped_at | DATETIME | Date de scraping |

---

## 🔧 Configuration PowerShell (Windows)

Si vous rencontrez des problèmes avec PowerShell :

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Get-ExecutionPolicy
```

---

## 📚 Documentation Technique

### Serveurs MCP Utilisés

1. **Puppeteer MCP** : Automatisation Chrome pour scraping
2. **Brave Search MCP** : Recherche web via API Brave
3. **SQLite MCP** : Gestion base de données locale
4. **Filesystem MCP** : Accès sécurisé aux fichiers

### Technologies

- **Python 3.8+** : Langage principal
- **Streamlit** : Framework web pour visualisation
- **SQLite** : Base de données légère
- **n8n** : Plateforme d'automatisation no-code
- **Puppeteer** : Automatisation navigateur
- **Claude Desktop** : Interface IA avec MCP

---

## 🎯 Exemples d'Utilisation

### Exemple 1 : Scraping via Claude Desktop

```
Utilisateur : "Donne-moi les 10 meilleurs produits électroniques sur Amazon"
Claude : 
  1. Utilise Brave Search pour trouver les pages Amazon
  2. Utilise Puppeteer pour naviguer et extraire
  3. Stocke dans SQLite
  4. Affiche les résultats
```

### Exemple 2 : Workflow n8n avec Telegram

```
1. Utilisateur envoie : "Recherche les best-sellers AliExpress en mode"
2. n8n reçoit le message Telegram
3. OpenAI analyse la demande
4. Scraping automatisé via API
5. Données sauvegardées dans Google Sheets
6. Réponse générée et envoyée via Telegram
```

---

## 🆘 Dépannage

### "Module non trouvé"
```bash
pip install -r requirements.txt
```

### "Claude Desktop ne reconnaît pas les serveurs MCP"
- Vérifier le fichier de configuration
- Redémarrer Claude Desktop
- Vérifier que les chemins sont corrects

### "Puppeteer ne fonctionne pas"
- Vérifier que Chrome est installé
- Vérifier le chemin dans la configuration
- Essayer avec `headless: true`

---

## 📝 Notes Importantes

- ⚠️ Respect des robots.txt et conditions d'utilisation des sites
- 🔒 Toutes les données sont stockées localement (confidentialité)
- 🆓 Tous les outils utilisés sont gratuits/open-source
- 📊 Les données peuvent être exportées à tout moment

---

## 👥 Auteurs

- **OSSAMA IBOURG**
- **MOHAMED MAKACH**

**Encadré par** : KARIM AFDEL  
**Année universitaire** : 2024-2025

---

## 📖 Références

- [Documentation MCP](https://modelcontextprotocol.io)
- [Claude Desktop](https://claude.ai/download)
- [n8n Documentation](https://docs.n8n.io)
- [Streamlit Documentation](https://docs.streamlit.io)

---

**Bon scraping et bonne analyse ! 🚀**
