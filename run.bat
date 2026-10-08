@echo off
title B.Tech Student Performance Advisor
echo ============================================================
echo Starting B.Tech Student Performance Advisor Web Application...
echo ============================================================
if exist .venv\Scripts\streamlit.exe (
    call .venv\Scripts\streamlit.exe run app.py
) else (
    streamlit run app.py
)
pause
