@echo off
title Frontend Streamlit
echo.
echo === LANCEMENT DU FRONTEND ===
echo.
echo Le frontend sera accessible sur: http://localhost:8501
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.
python -m streamlit run frontend/app.py --server.port 8501
pause

