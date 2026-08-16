# ⚠️ CORRECTION URGENTE - Claude Desktop ne Voit pas les Outils MCP

## 🚨 LE PROBLÈME

Claude Desktop ne liste que :
- web_search
- web_fetch
- Artifacts

**Mais PAS les outils MCP :**
- ❌ Puppeteer
- ❌ SQLite
- ❌ Filesystem

---

## ✅ SOLUTION : Redémarrer Claude Desktop CORRECTEMENT

### Étape 1 : Fermer COMPLÈTEMENT Claude Desktop

1. **Fermez TOUTES les fenêtres Claude Desktop**

2. **Ouvrir le Gestionnaire des tâches**
   - Appuyez sur `Ctrl + Shift + Esc`

3. **Terminer TOUS les processus Claude**
   - Dans le Gestionnaire des tâches, cherchez "claude"
   - Pour chaque processus "claude", faites clic droit → **"Terminer la tâche"**
   - Continuez jusqu'à ce qu'il n'y ait plus aucun processus "claude"

### Étape 2 : Attendre 10 secondes

### Étape 3 : Rouvrir Claude Desktop

1. Double-cliquez sur l'icône Claude Desktop
2. **Attendez 15-20 secondes** que Claude Desktop se charge complètement
3. Vous devriez voir l'interface se charger

### Étape 4 : Vérifier les Outils MCP

**Dans Claude Desktop, demandez :**
```
"Peux-tu me lister tous tes outils et capacités disponibles ? 
Spécifiquement, as-tu accès aux outils Puppeteer MCP, SQLite MCP, 
et Filesystem MCP ?"
```

**Si Claude liste maintenant Puppeteer et SQLite → ✅ Ça marche !**

**Si Claude ne les liste toujours pas → Voir Solution Alternative ci-dessous**

---

## 🔧 SOLUTION ALTERNATIVE : Utiliser Python Directement

**Le projet fonctionne PARFAITEMENT sans Claude Desktop MCP !**

### Option A : Scraper avec Python

```bash
python main.py
```

Cela va :
- ✅ Scraper Amazon, Temu, AliExpress
- ✅ Stocker dans products.db
- ✅ Afficher les résultats

### Option B : Voir dans le Frontend

```bash
streamlit run frontend/app.py
```

Puis ouvrir : http://localhost:8501

**Cela fonctionne SANS besoin de Claude Desktop MCP !**

---

## 🔍 VÉRIFICATION DU FICHIER DE CONFIG

Vérifions que le fichier de config est correct :

**Chemin du fichier :**
```
C:\Users\Lenovo\AppData\Roaming\Claude\claude_desktop_config.json
```

**Il doit contenir :**
```json
{
  "mcpServers": {
    "mcp-puppeteer": { ... },
    "sqlite": { ... },
    "filesystem": { ... }
  }
}
```

**Si le fichier n'existe pas ou est incorrect :**
```bash
python setup_claude_mcp.py
```

Puis redémarrer Claude Desktop.

---

## 💡 POURQUOI CLAUDE DESKTOP NE VOIT PAS LES OUTILS ?

**Raisons possibles :**

1. **Claude Desktop n'a pas été redémarré** après la configuration
   - → Solution : Fermer complètement et rouvrir

2. **Le fichier de config n'est pas lu correctement**
   - → Solution : Vérifier le chemin et le contenu

3. **Les serveurs MCP ne démarrent pas**
   - → Solution : Vérifier que Node.js est installé
   - → Solution : Vérifier que npx fonctionne

4. **Version de Claude Desktop incompatible**
   - → Solution : Mettre à jour Claude Desktop

---

## ✅ RÉSUMÉ DES ACTIONS

### Si vous voulez utiliser Claude Desktop MCP :

1. ✅ Fermer TOUT Claude Desktop (toutes fenêtres)
2. ✅ Terminer tous les processus "claude" dans Gestionnaire des tâches
3. ✅ Attendre 10 secondes
4. ✅ Rouvrir Claude Desktop
5. ✅ Attendre 15-20 secondes
6. ✅ Demander : "Liste tes outils MCP"

### Si Claude Desktop MCP ne fonctionne toujours pas :

**Pas de problème ! Utilisez Python directement :**

```bash
python main.py
streamlit run frontend/app.py
```

**Le projet fonctionne parfaitement comme ça ! 🚀**

---

## 🎯 RECOMMANDATION

**Pour tester rapidement :**
```bash
python main.py
```

**Cela scrap les produits et les stocke automatiquement !**

**Ensuite :**
```bash
streamlit run frontend/app.py
```

**Vous verrez les produits dans le frontend !**

**Pas besoin de Claude Desktop MCP pour que le projet fonctionne ! ✅**


