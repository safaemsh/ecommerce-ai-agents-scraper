# 🚀 Ce Qu'il Faut Lancer

## ✅ POUR LA PARTIE 1 (Agent IA avec Claude Desktop)

### ❌ VOUS N'AVEZ RIEN À LANCER !

**C'est tout automatique !**

1. **Ouvrez simplement Claude Desktop** (l'application)
2. **Donnez votre demande**
3. **C'est tout !**

Les serveurs MCP (Puppeteer, SQLite) sont lancés **automatiquement** par Claude Desktop quand il en a besoin.

Vous n'avez **PAS besoin de** :
- ❌ Lancer Puppeteer manuellement
- ❌ Lancer SQLite manuellement
- ❌ Lancer des services en arrière-plan
- ❌ Ouvrir des terminaux

**Claude Desktop fait tout automatiquement !**

---

## 📋 CE QUI EST DÉJÀ CONFIGURÉ

### ✅ Configuration faite une seule fois
- `python setup_claude_mcp.py` → **DÉJÀ FAIT**
- Les chemins sont dans le fichier de config
- Claude Desktop les lit au démarrage

### ✅ Quand vous ouvrez Claude Desktop
- Il lit le fichier de config automatiquement
- Il "sait" comment lancer Puppeteer si besoin
- Il "sait" où est la base SQLite

### ✅ Quand vous donnez une demande
- Claude utilise Puppeteer → **Lancé automatiquement**
- Claude utilise SQLite → **Lancé automatiquement**
- Tout se passe en arrière-plan
- Vous ne voyez rien, ça fonctionne !

---

## 🎯 ACTION À FAIRE

### Pour tester maintenant :

1. **Ouvrir Claude Desktop**
   ```
   Double-cliquez sur l'icône Claude Desktop
   ```

2. **Vérifier les outils** (optionnel)
   ```
   Tapez : "Quels outils MCP as-tu ?"
   ```

3. **Donner la demande de scraping**
   ```
   Tapez : "Utilise l'outil Puppeteer MCP pour naviguer sur 
   https://www.jumia.ma et scraper 5 produits best-sellers. 
   Ensuite, utilise l'outil SQLite MCP pour stocker ces produits 
   dans products.db."
   ```

4. **Attendre que Claude fasse le travail**
   - Puppeteer s'ouvre automatiquement (vous verrez Chrome s'ouvrir)
   - Claude scrape les produits
   - Claude stocke dans SQLite
   - Claude vous montre les résultats

**C'est tout ! Pas besoin de lancer autre chose !**

---

## 🖥️ POUR LA PARTIE 2 (n8n - Automatisation)

**Seulement si vous voulez utiliser n8n :**

### Il faut lancer n8n :

```bash
n8n start
```

Puis ouvrir : http://localhost:5678

**Mais ce n'est pas nécessaire pour tester la Partie 1 !**

---

## ✅ RÉSUMÉ

### Partie 1 (Agent IA MCP) :
- ✅ **Rien à lancer**
- ✅ Ouvrir Claude Desktop
- ✅ Donner la demande
- ✅ C'est tout !

### Partie 2 (n8n) :
- ⚙️ Lancer n8n : `n8n start`
- ⚙️ Configurer les workflows
- ⚙️ Activer l'automatisation

---

## 🎯 COMMENCEZ PAR LA PARTIE 1

**Action immédiate :**

1. Ouvrez Claude Desktop
2. Copiez-collez le prompt (voir `PROMPTS_CLAUDE.md`)
3. Regardez Claude travailler !

**C'est vraiment aussi simple que ça ! 🚀**

