@echo off
title Menu Principal - Systeme Multi-Agents
:MENU
cls
echo.
echo ========================================
echo   SYSTEME MULTI-AGENTS - SCRAPING
echo ========================================
echo.
echo 1. Lancer le scraping (recupere les produits)
echo 2. Lancer le frontend (voir les produits dans le navigateur)
echo 3. Voir les statistiques
echo 4. Voir les produits (dans le terminal)
echo 5. Scraping continu (toutes les minutes)
echo 6. Lancer n8n (automatisation - optionnel)
echo 0. Quitter
echo.
set /p choice="Votre choix (0-6): "
if "%choice%"=="1" goto SCRAPE
if "%choice%"=="2" goto FRONTEND
if "%choice%"=="3" goto STATS
if "%choice%"=="4" goto PRODUCTS
if "%choice%"=="5" goto CONTINUOUS
if "%choice%"=="6" goto N8N
if "%choice%"=="0" exit
goto MENU

:SCRAPE
cls
call scrape.bat
goto MENU

:FRONTEND
cls
call frontend.bat
goto MENU

:N8N
cls
call n8n.bat
goto MENU

:STATS
cls
call stats.bat
goto MENU

:PRODUCTS
cls
call view_products.bat
goto MENU

:CONTINUOUS
cls
call continuous_scrape.bat
goto MENU


