# ✅ CE QUE VOUS DEVEZ FAIRE - Guide Simple

## 📦 1. INSTALLER LES LOGICIELS NÉCESSAIRES

### A. Installer Claude Desktop
```
👉 Aller sur : https://claude.ai/download
👉 Télécharger et installer
👉 C'est GRATUIT
```

### B. Installer Node.js (si pas déjà installé)
```
👉 Aller sur : https://nodejs.org/
👉 Télécharger la version LTS
👉 Installer (cochez "Add to PATH")
👉 Vérifier : ouvrir PowerShell et taper "node --version"
```

### C. Installer n8n
```bash
# Dans PowerShell
npm install -g n8n
```

### D. Python est déjà installé ✅

---

## 🔧 2. CONFIGURER LE PROJET

### Étape 2.1 : Installer les dépendances Python
```bash
# Ouvrir PowerShell dans le dossier du projet
# Vous êtes déjà dans : C:\Users\Lenovo\Desktop\projet_sys_rep

pip install -r requirements.txt
```

### Étape 2.2 : Configurer Claude Desktop automatiquement
```bash
python setup_claude_mcp.py
```

**⚠️ ATTENTION** : Après cette commande, vous devrez :
1. Obtenir une clé API Brave (GRATUITE)
2. Modifier le fichier de configuration

---

## 🔑 3. OBTENIR LA CLÉ API BRAVE (GRATUIT)

### Comment faire :
```
1. Aller sur : https://brave.com/search/api/
2. Créer un compte (GRATUIT)
3. Cliquer sur "Get API Key"
4. Copier votre clé API (elle ressemble à : BSA_xxxxxxx)
5. Garder cette clé quelque part
```

### Puis modifier le fichier de config :
```
1. Appuyer sur Windows + R
2. Taper : %APPDATA%\Claude
3. Ouvrir le dossier "Claude"
4. Ouvrir le fichier "claude_desktop_config.json" avec Notepad
5. Chercher : "VOTRE_CLE_API_BRAVE_ICI"
6. Remplacer par votre vraie clé (BSA_xxxxxxx)
7. Sauvegarder
```

---

## 🔄 4. REDÉMARRER CLAUDE DESKTOP

```
1. Fermer complètement Claude Desktop
2. Rouvrir Claude Desktop
3. Vérifier que tout fonctionne
```

---

## ✅ 5. TESTER QUE ÇA MARCHE

### Ouvrir Claude Desktop et taper :

```
"Donne-moi 5 produits gagnants sur Jumia. 
Pour chaque produit, donne : 
- le nom
- le prix
- le lien vers le produit
- petite description.
Puis stocke les résultats dans la base SQLite."
```

### Si ça fonctionne :
✅ Claude va utiliser Puppeteer pour scraper
✅ Les résultats seront stockés dans SQLite
✅ Vous verrez les produits dans la réponse

### Si ça ne fonctionne pas :
- Vérifier que vous avez bien redémarré Claude Desktop
- Vérifier que la clé API Brave est correcte
- Vérifier les erreurs dans Claude Desktop

---

## 🎯 RÉCAPITULATIF - CE QUE VOUS DEVEZ FAIRE MAINTENANT :

### ✅ À FAIRE IMMÉDIATEMENT :

1. **Installer Claude Desktop** (si pas déjà fait)
   - https://claude.ai/download

2. **Installer Node.js** (si pas déjà fait)
   - https://nodejs.org/

3. **Installer n8n**
   ```bash
   npm install -g n8n
   ```

4. **Installer les dépendances Python**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurer Claude Desktop**
   ```bash
   python setup_claude_mcp.py
   ```

6. **Obtenir la clé API Brave**
   - https://brave.com/search/api/
   - Créer un compte gratuit
   - Copier la clé

7. **Modifier le fichier de config**
   - Ouvrir : `%APPDATA%\Claude\claude_desktop_config.json`
   - Remplacer `VOTRE_CLE_API_BRAVE_ICI` par votre clé

8. **Redémarrer Claude Desktop**

9. **Tester** avec la commande ci-dessus

---

## ❓ QUESTIONS FRÉQUENTES

### "J'ai déjà tout installé, je fais quoi maintenant ?"
→ Passez directement à l'étape 5 (Configurer Claude Desktop)

### "Je n'ai pas de clé API Brave, c'est obligatoire ?"
→ Oui, c'est nécessaire pour que Claude puisse rechercher sur le web
→ C'est GRATUIT et rapide à obtenir

### "Je veux juste tester, je dois tout installer ?"
→ Pour tester la Partie 1 (Agent IA), vous avez besoin de :
   - Claude Desktop
   - Node.js/npm
   - Python (déjà installé)
   - La clé API Brave
   → n8n est optionnel pour le moment (Partie 2)

### "Comment savoir si tout est bien installé ?"
```bash
# Vérifier Node.js
node --version

# Vérifier npm
npm --version

# Vérifier Python
python --version

# Vérifier n8n
n8n --version
```

---

## 🆘 SI VOUS AVEZ UN PROBLÈME

### "pip n'est pas reconnu"
→ Python n'est pas dans le PATH
→ Réinstaller Python en cochant "Add to PATH"

### "npm n'est pas reconnu"
→ Node.js n'est pas dans le PATH
→ Réinstaller Node.js

### "Claude Desktop ne fonctionne pas"
→ Vérifier que vous avez bien redémarré après la configuration
→ Vérifier le fichier de configuration

---

## 📝 RÉSUMÉ ULTRA-SIMPLE

**CE QU'IL FAUT FAIRE :**
1. Installer Claude Desktop + Node.js (si pas déjà fait)
2. `npm install -g n8n`
3. `pip install -r requirements.txt`
4. `python setup_claude_mcp.py`
5. Obtenir clé API Brave et la mettre dans le fichier de config
6. Redémarrer Claude Desktop
7. Tester avec Claude

**C'EST TOUT ! 🎉**

