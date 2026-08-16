# 📖 Comment Utiliser le Projet - Guide Complet

## 🎯 COMMENT LE PROJET FONCTIONNE

### ❌ Ce qui s'est passé (MAUVAIS)
Claude vous a donné du code React au lieu d'utiliser les outils MCP pour scraper réellement.

### ✅ Ce qui DOIT se passer (BON)
Claude doit utiliser les **outils MCP** pour :
1. **Puppeteer** → Aller sur Jumia et scraper les vrais produits
2. **SQLite** → Stocker les produits dans votre base `products.db`
3. Vous montrer les résultats

---

## 🚀 COMMENT FAIRE FONCTIONNER LE PROJET

### Étape 1 : Vérifier que les outils MCP sont disponibles

Dans Claude Desktop, demandez d'abord :

```
"Quels outils MCP as-tu à ta disposition ?"
```

Claude devrait répondre avec une liste incluant :
- Puppeteer (navigation, scraping)
- SQLite (base de données)
- Filesystem (fichiers)

### Étape 2 : Demander explicitement d'utiliser les outils MCP

**⚠️ IMPORTANT : Il faut être TRÈS PRÉCIS dans votre demande !**

Ne dites PAS simplement :
```
"Donne-moi des produits Jumia"
```

Dites EXACTEMENT :
```
"Utilise l'outil Puppeteer MCP pour naviguer sur https://www.jumia.ma 
et scraper 5 produits best-sellers. Pour chaque produit, extrais :
- le nom/titre
- le prix
- le lien URL
- une description courte

Ensuite, utilise l'outil SQLite MCP pour stocker ces produits dans 
la table 'products' de la base de données 'products.db'.

Après le stockage, affiche-moi les produits qui ont été sauvegardés."
```

### Étape 3 : Claude va utiliser les outils automatiquement

Quand vous donnez le bon prompt, Claude va :
1. Utiliser **Puppeteer** pour ouvrir Jumia dans Chrome
2. Naviguer sur le site
3. Extraire les vraies données des produits
4. Utiliser **SQLite** pour insérer dans `products.db`
5. Vous montrer ce qui a été stocké

---

## 🔧 SI CLAUDE NE RECONNAÎT PAS LES OUTILS MCP

### Problème 1 : Claude ne mentionne pas Puppeteer/SQLite

**Solution :**
1. Vérifier que Claude Desktop est bien redémarré
2. Vérifier le fichier de config : `%APPDATA%\Claude\claude_desktop_config.json`
3. Redémarrer Claude Desktop

### Problème 2 : Puppeteer ne fonctionne pas

**Solution :**
- Vérifier que Chrome est installé
- Vérifier le chemin dans la config

### Problème 3 : SQLite ne fonctionne pas

**Solution :**
- Vérifier que `products.db` existe dans le dossier du projet
- Vérifier le chemin dans la config

---

## 📝 PROMPTS EXEMPLES À UTILISER

### Exemple 1 : Scraping simple
```
"Utilise l'outil Puppeteer pour aller sur https://www.jumia.ma, 
cherche la section 'Meilleures ventes', et scrape 5 produits.
Stocke-les dans SQLite avec les colonnes: title, price, url, description."
```

### Exemple 2 : Vérifier la base de données
```
"Utilise l'outil SQLite pour afficher tous les produits 
dans la table 'products' de la base 'products.db'."
```

### Exemple 3 : Scraping avec stockage automatique
```
"Utilise Puppeteer MCP pour scraper 5 produits tendance sur Jumia.
Ensuite, utilise SQLite MCP pour les enregistrer dans products.db.
Montre-moi ce qui a été stocké."
```

---

## 🖥️ APRES LE SCRAPING : VOIR LES RESULTATS

Une fois que Claude a scrapé et stocké dans SQLite, vous pouvez :

### Option 1 : Via Claude Desktop
```
"Affiche-moi tous les produits stockés dans la base SQLite"
```

### Option 2 : Via le Frontend Streamlit
```bash
# Lancer le frontend
streamlit run frontend/app.py

# Ouvrir http://localhost:8501
```

Le frontend va lire les produits depuis `products.db` et les afficher !

---

## 🎯 WORKFLOW COMPLET

```
1. Vous → Claude Desktop : "Scrape 5 produits Jumia avec Puppeteer et stocke dans SQLite"

2. Claude → Puppeteer MCP : Ouvre Chrome, va sur Jumia, extrait les produits

3. Claude → SQLite MCP : Insère les produits dans products.db

4. Claude → Vous : "5 produits scrapés et stockés. Voici les résultats..."

5. Vous → Streamlit : Lancer le frontend pour voir visuellement les produits
```

---

## ❓ QUESTIONS FRÉQUENTES

### "Claude me donne du code au lieu d'utiliser les outils"
→ Votre prompt n'est pas assez précis. Utilisez les exemples ci-dessus avec "Utilise l'outil Puppeteer MCP" et "Utilise l'outil SQLite MCP".

### "Comment savoir si les produits sont vraiment dans la base ?"
→ Demandez à Claude : "Affiche-moi les produits de la base SQLite" ou lancez le frontend Streamlit.

### "Les outils MCP ne sont pas disponibles"
→ Redémarrer Claude Desktop et vérifier la configuration.

---

## ✅ CHECKLIST

- [ ] Claude Desktop redémarré
- [ ] Les outils MCP sont visibles (demander à Claude)
- [ ] Prompt précis avec "Utilise Puppeteer MCP" et "Utilise SQLite MCP"
- [ ] Produits scrapés et stockés
- [ ] Frontend Streamlit lancé pour visualiser

---

**Maintenant vous savez comment utiliser le projet correctement ! 🚀**

