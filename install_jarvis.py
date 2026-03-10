#!/usr/bin/env python3
"""
Script de Instalação Automática do J.A.R.V.I.S.
Verifica dependências e instala o que for necessário
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ J.A.R.V.I.S. requer Python 3.8 ou superior")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_package(package):
    """Instala pacote individual"""
    try:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado com sucesso")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar {package}")
        return False

def check_and_install_dependencies():
    """Verifica e instala dependências"""
    print("\n🔍 Verificando dependências...")
    
    # Lista de pacotes essenciais
    essential_packages = [
        "customtkinter>=5.2.0",
        "google-generativeai>=0.8.0",
        "Pillow>=10.0.0",
        "SpeechRecognition>=3.10.0",
        "pyttsx3>=2.90",
        "pyautogui>=0.9.54",
        "python-dotenv>=1.0.0"
    ]
    
    # Pacotes opcionais (com fallback)
    optional_packages = [
        ("pycaw>=20230407", "Controle de volume avançado"),
        ("screen-brightness-control>=0.1", "Controle de brilho"),
        ("psutil>=7.0.0", "Informações do sistema")
    ]
    
    # Instala essenciais
    failed_packages = []
    for package in essential_packages:
        if not install_package(package):
            failed_packages.append(package)
    
    # Instala opcionais
    print("\n🎯 Instalando pacotes opcionais...")
    for package, description in optional_packages:
        print(f"\n📋 {description}")
        if not install_package(package):
            print(f"⚠️ {package} não foi instalado (opcional)")
    
    return len(failed_packages) == 0

def setup_env_file():
    """Configura arquivo .env"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Arquivo .env já existe")
        return
    
    print("\n📝 Configurando arquivo .env...")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write("# J.A.R.V.I.S. - Configurações\n")
        f.write("# Adicione sua API Key do Gemini abaixo\n")
        f.write("# Obtenha em: https://makersuite.google.com/app/apikey\n\n")
        f.write("GEMINI_API_KEY=sua_chave_api_gemini_aqui\n")
    
    print("✅ Arquivo .env criado")
    print("⚠️ Não se esqueça de adicionar sua API Key!")

def test_imports():
    """Testa imports principais"""
    print("\n🧪 Testando imports...")
    
    test_modules = [
        ("customtkinter", "Interface gráfica"),
        ("google.generativeai", "API Gemini"),
        ("PIL", "Processamento de imagem"),
        ("speech_recognition", "Reconhecimento de voz"),
        ("pyttsx3", "Síntese de voz"),
        ("pyautogui", "Automação"),
        ("dotenv", "Variáveis de ambiente")
    ]
    
    failed_imports = []
    
    for module, description in test_modules:
        try:
            __import__(module)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description} - Falha na importação")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def create_shortcuts():
    """Cria atalhos para facilitar uso"""
    print("\n🚀 Criando atalhos...")
    
    # Script para Windows
    if sys.platform == "win32":
        bat_content = '''@echo off
echo Iniciando J.A.R.V.I.S...
python jarvis_gui_optimized.py
pause
'''
        with open("iniciar_jarvis.bat", "w", encoding="utf-8") as f:
            f.write(bat_content)
        print("✅ Atalho 'iniciar_jarvis.bat' criado")
    
    # Script para Linux/Mac
    else:
        sh_content = '''#!/bin/bash
echo "Iniciando J.A.R.V.I.S..."
python3 jarvis_gui_optimized.py
'''
        with open("iniciar_jarvis.sh", "w", encoding="utf-8") as f:
            f.write(sh_content)
        os.chmod("iniciar_jarvis.sh", 0o755)
        print("✅ Atalho 'iniciar_jarvis.sh' criado")

def main():
    """Função principal de instalação"""
    print("🤖 J.A.R.V.I.S. - Instalação Automática")
    print("=" * 50)
    
    # Verifica Python
    if not check_python_version():
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    # Instala dependências
    if not check_and_install_dependencies():
        print("\n⚠️ Algumas dependências essenciais falharam")
        print("   Verifique sua conexão com internet e tente novamente")
    
    # Configura ambiente
    setup_env_file()
    
    # Testa imports
    if not test_imports():
        print("\n⚠️ Alguns módulos não puderam ser importados")
        print("   O J.A.R.V.I.S. pode não funcionar corretamente")
    
    # Cria atalhos
    create_shortcuts()
    
    print("\n🎉 Instalação concluída!")
    print("\n📋 Próximos passos:")
    print("1. Abra o arquivo .env e adicione sua API Key do Gemini")
    print("2. Execute: python jarvis_gui_optimized.py")
    print("3. Ou use o atalho criado")
    
    print("\n📖 Para mais informações, leia JARVIS_SETUP.md")
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
