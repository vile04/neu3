@echo off
title PsychAnalytica - Iniciando Servidor
echo ========================================
echo       PSYCHANALYTICA PLATFORM
echo ========================================
echo.

:: Verificar se o ambiente virtual existe
if not exist venv (
    echo ERRO: Ambiente virtual não encontrado!
    echo Execute setup.bat primeiro para configurar o projeto.
    pause
    exit /b 1
)

:: Ativar ambiente virtual
echo [1/4] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual
    pause
    exit /b 1
)
echo ✓ Ambiente virtual ativado

:: Carregar variáveis de ambiente do arquivo .env
echo [2/4] Carregando configurações...
if exist .env (
    for /f "usebackq tokens=1,2 delims==" %%a in (.env) do (
        if not "%%a"=="" if not "%%a:~0,1%%"=="#" (
            set "%%a=%%b"
        )
    )
    echo ✓ Configurações carregadas
) else (
    echo ⚠ Arquivo .env não encontrado, usando configurações padrão
    set DATABASE_URL=sqlite:///psychanalytica.db
    set SESSION_SECRET=dev-secret-key
)

:: Verificar/criar banco de dados
echo [3/4] Inicializando banco de dados...
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✓ Banco de dados inicializado')
"
if errorlevel 1 (
    echo ERRO: Falha ao inicializar banco de dados
    pause
    exit /b 1
)

:: Iniciar servidor
echo [4/4] Iniciando servidor...
echo.
echo ========================================
echo     SERVIDOR INICIADO COM SUCESSO!
echo ========================================
echo.
echo Plataforma disponível em:
echo http://localhost:5000
echo.
echo Pressione Ctrl+C para parar o servidor
echo ========================================
echo.

:: Aguardar 2 segundos e abrir navegador
timeout /t 2 /nobreak >nul
start http://localhost:5000

:: Iniciar servidor Flask
python main.py

:: Se chegou aqui, o servidor foi interrompido
echo.
echo ========================================
echo       SERVIDOR INTERROMPIDO
echo ========================================
echo.
pause