# 💬 Prompts Précis pour Claude Desktop

## ⚠️ IMPORTANT

Ne dites PAS simplement "donne-moi des produits". Claude doit utiliser les **outils MCP** explicitement !

---

## ✅ PROMPT 1 : Vérifier les outils disponibles

```
"Quels outils MCP as-tu à ta disposition ? Liste-moi tous les outils disponibles."
```

**Objectif** : Vérifier que Puppeteer et SQLite sont bien disponibles.

---

## ✅ PROMPT 2 : Scraping avec Puppeteer + Stockage SQLite

```
"Utilise l'outil Puppeteer MCP pour naviguer sur https://www.jumia.ma 
et scraper 5 produits best-sellers ou produits tendance.

Pour chaque produit, extrais :
- le nom/titre complet
- le prix en dirhams (DH)
- le lien URL vers le produit
- une description courte (si disponible)

Ensuite, utilise l'outil SQLite MCP pour stocker ces 5 produits 
dans la base de données products.db, dans la table 'products'.

Après avoir stocké, affiche-moi la liste des produits qui ont été 
sauvegardés en interrogeant la base SQLite."
```

---

## ✅ PROMPT 3 : Vérifier ce qui est dans la base

```
"Utilise l'outil SQLite MCP pour afficher tous les produits 
stockés dans la table 'products' de la base 'products.db'.
Montre-moi le nombre total de produits et leurs détails."
```

---

## ✅ PROMPT 4 : Scraping Amazon

```
"Utilise Puppeteer MCP pour aller sur https://www.amazon.fr,
cherche la section 'Meilleures ventes' ou 'Best Sellers',
et scrape 5 produits avec leur nom, prix, lien et description.

Stocke-les dans SQLite avec l'outil SQLite MCP dans products.db."
```

---

## ✅ PROMPT 5 : Scraping AliExpress

```
"Utilise l'outil Puppeteer MCP pour naviguer sur https://www.aliexpress.com,
trouve 5 produits populaires/tendance,
et extrais leurs informations (nom, prix, URL, description).

Puis utilise SQLite MCP pour les enregistrer dans products.db."
```

---

## 🎯 FORMAT STANDARD DU PROMPT

**Toujours inclure :**
1. ✅ "Utilise l'outil Puppeteer MCP" (pour scraper)
2. ✅ L'URL du site à scraper
3. ✅ Ce qu'il faut extraire (nom, prix, lien, description)
4. ✅ "Utilise l'outil SQLite MCP" (pour stocker)
5. ✅ Le nom de la base : "products.db"
6. ✅ "Affiche-moi les résultats" (pour vérifier)

---

## ❌ À ÉVITER

❌ "Donne-moi des produits Jumia"  
❌ "Scrape Jumia"  
❌ "Trouve des produits"

**Pourquoi ?** Claude ne sait pas qu'il doit utiliser les outils MCP !

---

## ✅ À UTILISER

✅ "Utilise l'outil Puppeteer MCP pour..."  
✅ "Ensuite utilise l'outil SQLite MCP pour..."  
✅ "Affiche-moi ce qui a été stocké dans SQLite"

**Pourquoi ?** Claude comprend qu'il doit utiliser les outils spécifiques !

---

## 🔍 COMMENT SAVOIR SI ÇA MARCHE ?

### Signes que ça fonctionne :
✅ Claude dit "J'utilise Puppeteer pour naviguer..."  
✅ Claude mentionne "Outil Puppeteer" dans ses réponses  
✅ Claude dit "J'enregistre dans SQLite..."  
✅ Vous voyez les vrais produits avec vrais prix/liens  
✅ Les produits apparaissent dans le frontend Streamlit

### Signes que ça ne fonctionne PAS :
❌ Claude génère du code au lieu d'utiliser les outils  
❌ Claude invente des produits  
❌ Claude ne mentionne pas Puppeteer ou SQLite  
❌ Les produits ne sont pas dans products.db

---

## 🆘 SI CLAUDE NE COMPREND TOUJOURS PAS

Essayez ce prompt encore plus explicite :

```
"Je veux que tu utilises les outils MCP configurés sur ce système.

ÉTAPE 1 : Utilise l'outil Puppeteer MCP disponible dans tes outils.
          Va sur https://www.jumia.ma
          Scrape 5 vrais produits avec leurs informations.

ÉTAPE 2 : Utilise l'outil SQLite MCP disponible dans tes outils.
          Insère ces 5 produits dans la base products.db,
          table 'products', avec les colonnes: title, price, url, description.

ÉTAPE 3 : Utilise SQLite MCP pour lire et m'afficher les produits stockés.

Utilise tes outils MCP, ne génère pas de code !"
```

---

**Utilisez ces prompts exacts et ça fonctionnera ! 🚀**

