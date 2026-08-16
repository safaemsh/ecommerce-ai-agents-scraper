@echo off
title Visualiser les Produits
echo.
echo === VISUALISATION DES PRODUITS ===
echo.
echo Choisissez une option:
echo 1. Voir tous les produits
echo 2. Voir les produits Amazon
echo 3. Voir les produits Temu
echo 4. Voir les produits AliExpress
echo.
set /p choice="Votre choix (1-4): "
if "%choice%"=="1" python utils/view_data.py --limit 50
if "%choice%"=="2" python utils/view_data.py --platform amazon --limit 50
if "%choice%"=="3" python utils/view_data.py --platform temu --limit 50
if "%choice%"=="4" python utils/view_data.py --platform aliexpress --limit 50
echo.
pause

