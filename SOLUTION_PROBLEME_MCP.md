# 🔧 Solution au Problème : Claude Desktop ne Voit pas les Outils MCP

## 🎯 Diagnostic

Votre configuration est **CORRECTE** ✅, mais Claude Desktop ne charge peut-être pas les serveurs MCP correctement.

---

## ✅ SOLUTIONS À ESSAYER (dans l'ordre)

### Solution 1 : Redémarrer Claude Desktop Correctement

1. **Fermer TOUTES les fenêtres Claude Desktop**
   - Cliquez sur toutes les fenêtres Claude Desktop
   - Fermez-les complètement (pas seulement minimiser)
   - Vérifiez la barre des tâches - il ne doit plus y avoir Claude Desktop

2. **Fermer les processus en arrière-plan**
   - Appuyez sur `Ctrl + Shift + Esc` pour ouvrir le Gestionnaire des tâches
   - Cherchez tous les processus "claude"
   - Faites clic droit → "Terminer la tâche" sur tous

3. **Rouvrir Claude Desktop**
   - Double-cliquez sur l'icône Claude Desktop
   - Attendez qu'il se charge complètement (quelques secondes)

4. **Vérifier les outils**
   ```
   Dans Claude Desktop, demandez :
   "Peux-tu me lister tous tes outils et capacités disponibles ?"
   ```

---

### Solution 2 : Vérifier que Node.js est Accessible

**Problème possible** : npx n'est pas dans le PATH système.

**Solution** :

1. Ouvrir PowerShell en tant qu'Administrateur

2. Vérifier Node.js :
   ```powershell
   node --version
   npm --version
   npx --version
   ```

3. Si npx fonctionne dans PowerShell mais pas pour Claude Desktop :
   - Redémarrer l'ordinateur (pour mettre à jour le PATH)
   - OU réinstaller Node.js et cocher "Add to PATH"

---

### Solution 3 : Installer uvx (pour SQLite MCP)

SQLite MCP utilise `uvx`. Si ce n'est pas installé :

**Option A : Installer uv**
```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Option B : Modifier la config pour utiliser une alternative**

---

### Solution 4 : Vérifier les Logs Claude Desktop

Claude Desktop peut avoir des logs d'erreur :

1. Ouvrir ce dossier :
   ```
   %APPDATA%\Claude\logs
   ```

2. Chercher les fichiers récents

3. Vérifier s'il y a des erreurs liées à MCP

---

### Solution 5 : Alternative - Utiliser le Serveur MCP Python

Au lieu d'utiliser les serveurs MCP npm, on peut utiliser notre serveur Python personnalisé qui est déjà configuré (`scraping-system`).

**Dans Claude Desktop, essayez :**
```
"Utilise le serveur scraping-system pour scraper Jumia"
```

---

## 🆘 SI RIEN NE FONCTIONNE

### Solution Alternative : Utiliser les Scripts Python Directement

Au lieu de passer par Claude Desktop avec MCP, vous pouvez utiliser directement :

```bash
# Scraper directement
python main.py

# Voir les produits
python utils/view_data.py --stats

# Lancer le frontend
streamlit run frontend/app.py
```

**Cela fonctionne SANS Claude Desktop !**

---

## ✅ CHECKLIST DE VÉRIFICATION

- [ ] Claude Desktop complètement fermé et redémarré
- [ ] Node.js installé et dans le PATH
- [ ] `npx --version` fonctionne dans PowerShell
- [ ] Fichier de config existe : `%APPDATA%\Claude\claude_desktop_config.json`
- [ ] Demander à Claude : "Liste tes outils" - doit montrer Puppeteer/SQLite
- [ ] Si rien ne fonctionne → Utiliser `python main.py` directement

---

## 💡 SOLUTION RAPIDE (Si MCP ne fonctionne pas)

**Utilisez les scripts Python directement :**

```bash
# 1. Scraper les produits
python main.py

# 2. Voir dans le frontend
streamlit run frontend/app.py
```

**Cela fonctionne SANS Claude Desktop MCP !**

---

## 📞 PROCHAINES ÉTAPES

1. **Essayez Solution 1** (redémarrer Claude Desktop)
2. **Si ça ne marche pas**, utilisez `python main.py` directement
3. **Le frontend fonctionne** avec `streamlit run frontend/app.py`

**Le projet fonctionne même sans MCP ! 🚀**

