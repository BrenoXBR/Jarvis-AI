@echo off
title Jarvis Launcher
echo Iniciando Jarvis...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Check if Jarvis script exists
if not exist "jarvis.py" (
    echo [ERRO] Script do Jarvis nao encontrado!
    echo.
    pause
    exit /b 1
)

REM Run Jarvis using VBScript to avoid terminal window
cscript //nologo run_jarvis.vbs

if %ERRORLEVEL% EQU 0 (
    echo Jarvis iniciado com sucesso!
    echo O assistente esta rodando em segundo plano.
    echo.
    echo Para parar, feche a janela do Jarvis ou use o comando de voz.
) else (
    echo [ERRO] Falha ao iniciar Jarvis!
    echo Codigo de erro: %ERRORLEVEL%
    echo.
    pause
)

echo.
timeout /t 3 >nul
