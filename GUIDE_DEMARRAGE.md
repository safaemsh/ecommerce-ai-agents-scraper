# 🚀 Guide de Démarrage - Prochaines Étapes

## 📋 Checklist Complète

### ✅ ÉTAPE 1 : Installation des Prérequis

#### 1.1 Installer Claude Desktop
```
1. Télécharger depuis : https://claude.ai/download
2. Installer l'application
3. S'assurer qu'elle fonctionne
```

#### 1.2 Installer Node.js et npm
```
1. Télécharger depuis : https://nodejs.org/
2. Installer (inclut npm automatiquement)
3. Vérifier : node --version et npm --version
```

#### 1.3 Installer Python (si pas déjà fait)
```
1. Télécharger depuis : https://www.python.org/downloads/
2. Installer Python 3.8 ou supérieur
3. Cocher "Add Python to PATH" lors de l'installation
```

#### 1.4 Installer uv (optionnel mais recommandé)
```
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Vérifier
uv --version
```

#### 1.5 Installer n8n
```bash
npm install -g n8n
```

---

### ✅ ÉTAPE 2 : Configuration Claude Desktop MCP

#### 2.1 Installer les dépendances Python
```bash
pip install -r requirements.txt
```

#### 2.2 Configurer les serveurs MCP automatiquement
```bash
python setup_claude_mcp.py
```

**⚠️ IMPORTANT** : Après la configuration, vous devez :
1. Obtenir votre clé API Brave : https://brave.com/search/api/
2. Ouvrir le fichier : `%APPDATA%\Claude\claude_desktop_config.json`
3. Remplacer `VOTRE_CLE_API_BRAVE_ICI` par votre vraie clé

#### 2.3 Redémarrer Claude Desktop
```
- Fermer complètement Claude Desktop
- Rouvrir Claude Desktop
- Vérifier que les serveurs MCP sont détectés (26 outils disponibles)
```

---

### ✅ ÉTAPE 3 : Tester l'Agent IA avec Claude Desktop

#### 3.1 Test Simple
Dans Claude Desktop, demandez :
```
"Donne-moi 5 produits gagnants sur Jumia. 
Pour chaque produit, donne : 
- le nom
- le prix  
- le lien vers le produit
- petite description.
Puis stocke les résultats dans la base SQLite."
```

#### 3.2 Ce qui doit se passer
1. Claude utilise **Brave Search** pour trouver les pages Jumia
2. Claude utilise **Puppeteer** pour naviguer et extraire les données
3. Claude stocke les résultats dans **SQLite**
4. Vous voyez les produits dans la réponse de Claude

---

### ✅ ÉTAPE 4 : Configuration n8n Workflow

#### 4.1 Démarrer n8n
```bash
n8n start
```

Ouvrir dans le navigateur : **http://localhost:5678**

#### 4.2 Obtenir les Clés API nécessaires

##### a) Telegram Bot API
```
1. Ouvrir Telegram et chercher @BotFather
2. Envoyer : /newbot
3. Suivre les instructions pour créer un bot
4. Copier le token API reçu
```

##### b) OpenAI API Key
```
1. Aller sur : https://platform.openai.com/api-keys
2. Créer un compte (si nécessaire)
3. Créer une nouvelle clé API
4. Copier la clé (commence par sk-...)
```

##### c) Firecrawl API (optionnel - pour scraping avancé)
```
1. Aller sur : https://firecrawl.dev
2. Créer un compte
3. Obtenir la clé API
```

##### d) Google Sheets API
```
1. Aller sur : https://console.cloud.google.com
2. Créer un projet
3. Activer Google Sheets API
4. Créer des credentials OAuth2
```

#### 4.3 Configurer les Credentials dans n8n

Dans l'interface n8n :
1. Aller dans **Credentials**
2. Créer les credentials suivants :
   - **Telegram Bot** : Coller votre token Telegram
   - **OpenAI API** : Coller votre clé OpenAI
   - **Firecrawl API** (si utilisé) : Coller votre clé
   - **Google Sheets OAuth2** : Configurer avec vos credentials Google

#### 4.4 Importer le Workflow

1. Dans n8n, cliquer sur **Workflows**
2. Cliquer sur **Import from File**
3. Sélectionner : `n8n_workflows/workflow_best_sellers.json`
4. Le workflow apparaît dans votre liste

#### 4.5 Configurer le Workflow

1. Ouvrir le workflow importé
2. Pour chaque nœud qui nécessite des credentials :
   - Cliquer sur le nœud
   - Sélectionner les credentials appropriés
   - Sauvegarder

3. Pour le nœud Google Sheets :
   - Remplacer `VOTRE_SHEET_ID` par l'ID de votre Google Sheet
   - Créer un Google Sheet et copier son ID depuis l'URL

#### 4.6 Activer le Workflow

1. Cliquer sur le bouton **Active** en haut à droite
2. Le workflow est maintenant actif et écoute les messages Telegram

---

### ✅ ÉTAPE 5 : Tester le Workflow n8n

#### 5.1 Tester avec Telegram
1. Ouvrir Telegram
2. Chercher votre bot (le nom que vous avez donné)
3. Envoyer un message texte :
   ```
   Recherche les 5 best-sellers électroniques sur Amazon
   ```

4. OU envoyer un message vocal avec la même demande

#### 5.2 Ce qui doit se passer
1. n8n reçoit le message Telegram
2. Si vocal → Transcription avec Whisper
3. Analyse de la demande avec GPT-4
4. Scraping des produits (Firecrawl ou API)
5. Sauvegarde dans Google Sheets
6. Génération d'une réponse avec GPT-4
7. Envoi de la réponse via Telegram

---

### ✅ ÉTAPE 6 : Tester le Frontend Streamlit

#### 6.1 Lancer le Frontend
```bash
streamlit run frontend/app.py
```

#### 6.2 Ouvrir dans le navigateur
```
http://localhost:8501
```

#### 6.3 Fonctionnalités disponibles
- **Dashboard** : Vue d'ensemble avec graphiques
- **Produits** : Catalogue avec recherche et filtres
- **Statistiques** : Analyses par plateforme
- **Scraping Live** : Lancer le scraping depuis l'interface

---

## 🎯 Résumé des Étapes Clés

### Pour Partie 1 (Agent IA MCP) :
```
1. ✅ Installer Claude Desktop
2. ✅ Installer Node.js/npm
3. ✅ python setup_claude_mcp.py
4. ✅ Obtenir clé API Brave
5. ✅ Redémarrer Claude Desktop
6. ✅ Tester : "Donne-moi 5 produits Jumia"
```

### Pour Partie 2 (n8n Workflow) :
```
1. ✅ npm install -g n8n
2. ✅ n8n start
3. ✅ Obtenir toutes les clés API (Telegram, OpenAI, Google, Firecrawl)
4. ✅ Configurer credentials dans n8n
5. ✅ Importer workflow_best_sellers.json
6. ✅ Activer le workflow
7. ✅ Tester avec Telegram
```

---

## 🆘 Problèmes Courants

### "Module Python non trouvé"
```bash
pip install -r requirements.txt
```

### "Claude Desktop ne détecte pas les serveurs MCP"
- Vérifier le fichier de configuration
- Redémarrer Claude Desktop
- Vérifier que les chemins sont corrects

### "n8n ne démarre pas"
```bash
# Vérifier que le port 5678 est libre
netstat -ano | findstr :5678

# Redémarrer n8n
n8n start
```

### "Workflow n8n ne reçoit pas les messages Telegram"
- Vérifier que le bot Telegram est bien créé
- Vérifier que le token est correct dans n8n
- Vérifier que le workflow est activé

---

## 📞 Support

Pour plus d'aide :
- Consulter `README.md` pour la documentation complète
- Vérifier les logs dans `logs/scraping.log`
- Vérifier les exécutions n8n dans l'interface web

---

**Bon courage pour la mise en place ! 🚀**

