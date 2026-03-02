@echo off
title J.A.R.V.I.S. - Stark Industries
echo Iniciando J.A.R.V.I.S. Completo (Memoria + Voz + Visao + Gemini)...
echo.
echo Aguarde a inicializacao da interface...
echo.

REM Limpa variaveis de ambiente que podem causar conflitos
set PYTHONPATH=
set PYTHONHOME=

REM Inicia o Python com configuracoes otimizadas para GUI
python -u jarvis_gui_integrada.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Erro ao executar o Jarvis. Verifique se todas as dependencias estao instaladas.
    echo Execute: pip install -r requirements.txt
    echo.
)

pause
