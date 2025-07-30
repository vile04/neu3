@echo off
title Configuração - PsychAnalytica Platform
echo ========================================
echo     CONFIGURAÇÃO PSYCHANALYTICA
echo ========================================
echo.

:: Verificar se Python está instalado
echo [1/7] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Por favor, instale Python 3.11+ de https://python.org
    pause
    exit /b 1
)
echo ✓ Python encontrado

:: Verificar se pip está instalado
echo [2/7] Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: pip não encontrado!
    echo Reinstale Python com pip incluído
    pause
    exit /b 1
)
echo ✓ pip encontrado

:: Criar ambiente virtual
echo [3/7] Criando ambiente virtual...
if exist venv (
    echo ⚠ Ambiente virtual já existe, removendo...
    rmdir /s /q venv
)
python -m venv venv
if errorlevel 1 (
    echo ERRO: Falha ao criar ambiente virtual
    pause
    exit /b 1
)
echo ✓ Ambiente virtual criado

:: Ativar ambiente virtual
echo [4/7] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual
    pause
    exit /b 1
)
echo ✓ Ambiente virtual ativado

:: Atualizar pip
echo [5/7] Atualizando pip...
python -m pip install --upgrade pip
echo ✓ pip atualizado

:: Instalar dependências
echo [6/7] Instalando dependências...
pip install flask flask-socketio flask-sqlalchemy google-genai openai psycopg2-binary reportlab requests sqlalchemy trafilatura werkzeug gunicorn email-validator
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependências
    pause
    exit /b 1
)
echo ✓ Dependências instaladas

:: Configurar variáveis de ambiente (arquivo .env)
echo [7/7] Configurando variáveis de ambiente...
(
echo # Configurações do Banco de Dados
echo DATABASE_URL=sqlite:///psychanalytica.db
echo.
echo # Chave Secreta da Sessão
echo SESSION_SECRET=your-secret-key-here-change-this
echo.
echo # APIs de IA ^(necessário configurar^)
echo # Obtenha sua chave em: https://ai.google.dev/
echo GEMINI_API_KEY=your-gemini-api-key-here
echo.
echo # Obtenha sua chave em: https://platform.openai.com/
echo OPENAI_API_KEY=your-openai-api-key-here
echo.
echo # Configurações do Flask
echo FLASK_ENV=development
echo FLASK_DEBUG=True
) > .env

echo ✓ Arquivo .env criado

echo.
echo ========================================
echo      CONFIGURAÇÃO CONCLUÍDA!
echo ========================================
echo.
echo PRÓXIMOS PASSOS:
echo 1. Edite o arquivo .env e adicione suas chaves de API
echo 2. Execute run.bat para iniciar a aplicação
echo.
echo APIs necessárias:
echo - Gemini API: https://ai.google.dev/
echo - OpenAI API: https://platform.openai.com/
echo.
pause