#!/usr/bin/env python3
"""
Script para construir o executável do J.A.R.V.I.S.
"""

import os
import sys
import subprocess
import shutil

def clean_build_dirs():
    """Limpa diretórios de build anteriores"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Limpando diretório {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Limpa arquivos .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def check_requirements():
    """Verifica se todos os requisitos estão instalados"""
    print("🔍 Verificando requisitos...")
    
    required_packages = [
        ('customtkinter', 'customtkinter'),
        ('google-generativeai', 'google.generativeai'), 
        ('python-dotenv', 'dotenv'),
        ('pyautogui', 'pyautogui'),
        ('Pillow', 'PIL'),
        ('speechrecognition', 'speech_recognition'),
        ('pyttsx3', 'pyttsx3'),
        ('sqlite3', 'sqlite3')  # Built-in, mas verificamos import
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name}")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️ Pacotes faltando: {', '.join(missing_packages)}")
        print("Instale com: pip install -r requirements.txt")
        return False
    
    return True

def build_executable():
    """Constrói o executável com PyInstaller"""
    print("🔨 Construindo executável...")
    
    # Comando PyInstaller com opções otimizadas
    cmd = [
        'pyinstaller',
        '--name=JarvisGUI',
        '--onefile',  # Cria um único arquivo executável
        '--windowed',  # Sem console (aplicação GUI)
        '--add-data=.env;.',  # Inclui arquivo .env
        '--hidden-import=customtkinter',
        '--hidden-import=google.generativeai',
        '--hidden-import=speech_recognition',
        '--hidden-import=pyttsx3',
        '--hidden-import=pyautogui',
        '--hidden-import=PIL',
        '--hidden-import=sqlite3',
        '--hidden-import=dotenv',
        '--collect-all=customtkinter',
        'jarvis_gui_integrada.py'
    ]
    
    # Adiciona ícone se existir
    if os.path.exists('icon.ico'):
        cmd.insert(-1, '--icon=icon.ico')
    
    # Adiciona arquivo de versão se existir
    if os.path.exists('version_info.txt'):
        cmd.insert(-1, '--version-file=version_info.txt')
    
    try:
        print(f"🔧 Executando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executável construído com sucesso!")
            print(f"📍 Local: dist/JarvisGUI.exe")
            return True
        else:
            print("❌ Erro na construção:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar PyInstaller: {e}")
        return False

def create_portable_package():
    """Cria um pacote portátil com todos os arquivos necessários"""
    print("📦 Criando pacote portátil...")
    
    # Cria diretório para o pacote
    package_dir = "Jarvis_Portable"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    # Copia o executável
    if os.path.exists('dist/JarvisGUI.exe'):
        shutil.copy('dist/JarvisGUI.exe', package_dir)
        print("✅ Executável copiado")
    
    # Copia arquivos necessários
    required_files = ['.env', 'README.md', 'requirements.txt']
    
    for file_name in required_files:
        if os.path.exists(file_name):
            shutil.copy(file_name, package_dir)
            print(f"✅ {file_name} copiado")
        else:
            print(f"⚠️ {file_name} não encontrado")
    
    # Cria arquivo de instruções
    instructions = """J.A.R.V.I.S. - Assistente Inteligente Portable

🚀 COMO USAR:

1. Execute JarvisGUI.exe
2. Aguarde a interface carregar
3. Configure sua API Key no arquivo .env se necessário

📁 ARQUIVOS IMPORTANTES:
- JarvisGUI.exe: Programa principal
- .env: Configurações (API Key do Gemini)
- README.md: Instruções detalhadas
- requirements.txt: Dependências (para desenvolvedores)

⚙️ CONFIGURAÇÃO:
Edite o arquivo .env e adicione sua API Key:
GEMINI_API_KEY=sua_chave_api_aqui

🔧 REQUISITOS:
- Windows 10 ou superior
- Conexão com internet
- Microfone (opcional, para comandos de voz)

🤖 FUNCIONALIDADES:
- Chat com IA Gemini
- Comandos de voz
- Análise de tela
- Memória persistente
- Interface Stark Industries

Desenvolvido com ❤️ por Windsurf
"""
    
    with open(os.path.join(package_dir, 'INSTRUCOES.txt'), 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Pacote portátil criado!")
    print(f"📍 Local: {package_dir}/")

def main():
    """Função principal"""
    print("🤖 J.A.R.V.I.S. - Construtor de Executável")
    print("=" * 50)
    
    # Verifica requisitos
    if not check_requirements():
        print("\nRequisitos não atendidos. O programa será encerrado.")
        return
    
    # Limpa builds anteriores
    clean_build_dirs()
    
    # Constrói o executável
    if build_executable():
        # Cria pacote portátil
        create_portable_package()
        
        print("\n🎉 Processo concluído com sucesso!")
        print("\n📋 RESUMO:")
        print("✅ Executável: dist/JarvisGUI.exe")
        print("✅ Pacote Portable: Jarvis_Portable/")
        print("\n🚀 Para distribuir, compacte a pasta Jarvis_Portable/")
    else:
        print("\n❌ Falha na construção do executável")
    
    print("\nBuild concluído. O programa será encerrado.")

if __name__ == "__main__":
    main()
