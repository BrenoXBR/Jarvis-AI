#!/usr/bin/env python3
"""
Checklist completo para verificar se o código está pronto para PyInstaller
"""

import os
import sys
import importlib.util

def check_imports():
    """Verifica se todos os imports podem ser encontrados"""
    print("🔍 VERIFICANDO IMPORTS...")
    
    required_imports = {
        'customtkinter': 'ctk',
        'threading': 'threading',
        'queue': 'queue',
        'time': 'time',
        'datetime': 'datetime',
        'sys': 'sys',
        'os': 'os',
        'sqlite3': 'sqlite3',
        'json': 'json',
        'pyautogui': 'pyautogui',
        'tempfile': 'tempfile',
        'PIL.Image': 'Image',
        'google.generativeai': 'genai',
        'dotenv': 'load_dotenv',
        'speech_recognition': 'sr',
        'pyttsx3': 'pyttsx3'
    }
    
    missing_imports = []
    
    for module_name, alias in required_imports.items():
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                print(f"❌ {module_name}")
                missing_imports.append(module_name)
            else:
                print(f"✅ {module_name}")
        except ImportError:
            print(f"❌ {module_name}")
            missing_imports.append(module_name)
    
    return len(missing_imports) == 0, missing_imports

def check_file_structure():
    """Verifica estrutura de arquivos"""
    print("\n📁 VERIFICANDO ESTRUTURA DE ARQUIVOS...")
    
    required_files = [
        'jarvis_gui_integrada.py',
        '.env',
        'requirements.txt'
    ]
    
    missing_files = []
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name}")
            missing_files.append(file_name)
    
    return len(missing_files) == 0, missing_files

def check_code_structure():
    """Verifica estrutura do código para PyInstaller"""
    print("\n🔧 VERIFICANDO ESTRUTURA DO CÓDIGO...")
    
    issues = []
    
    try:
        with open('jarvis_gui_integrada.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se tem __main__
        if '__name__ == "__main__"' in content:
            print("✅ Tem __main__")
        else:
            print("❌ Não tem __main__")
            issues.append("Falta __main__")
        
        # Verifica se usa sys.frozen para executável
        if 'getattr(sys, \'frozen\', False)' in content or 'sys.frozen' in content:
            print("✅ Tratamento para executável (sys.frozen)")
        else:
            print("❌ Não tem tratamento para executável")
            issues.append("Falta tratamento sys.frozen")
        
        # Verifica se usa caminhos relativos
        if 'os.path.join' in content and 'os.path.dirname' in content:
            print("✅ Usa caminhos relativos")
        else:
            print("❌ Não usa caminhos relativos adequadamente")
            issues.append("Falta caminhos relativos")
        
        # Verifica se tem tratamento de exceções
        if 'try:' in content and 'except' in content:
            print("✅ Tem tratamento de exceções")
        else:
            print("❌ Falta tratamento de exceções")
            issues.append("Falta tratamento de exceções")
        
        # Verifica se não usa imports relativos
        if 'from .' in content:
            print("❌ Usa imports relativos (problema para PyInstaller)")
            issues.append("Usa imports relativos")
        else:
            print("✅ Não usa imports relativos")
        
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        issues.append(f"Erro ao ler arquivo: {e}")
    
    return len(issues) == 0, issues

def check_gui_specific():
    """Verifica aspectos específicos de GUI"""
    print("\n🖥️ VERIFICANDO ASPECTOS DE GUI...")
    
    issues = []
    
    try:
        with open('jarvis_gui_integrada.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se tem mainloop
        if 'mainloop()' in content:
            print("✅ Tem mainloop()")
        else:
            print("❌ Não tem mainloop()")
            issues.append("Falta mainloop()")
        
        # Verifica se tem tratamento para fechar janela
        if 'destroy()' in content or 'quit()' in content:
            print("✅ Tem tratamento para fechar janela")
        else:
            print("⚠️ Poderia ter melhor tratamento para fechar janela")
        
        # Verifica se usa threads daemon
        if 'daemon=True' in content:
            print("✅ Usa threads daemon")
        else:
            print("⚠️ Deveria usar threads daemon")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        issues.append(f"Erro: {e}")
    
    return len(issues) == 0, issues

def check_resource_handling():
    """Verifica tratamento de recursos"""
    print("\n📦 VERIFICANDO TRATAMENTO DE RECURSOS...")
    
    issues = []
    
    try:
        with open('jarvis_gui_integrada.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica tratamento de .env
        if 'load_dotenv' in content and '.env' in content:
            print("✅ Trata arquivo .env")
        else:
            print("❌ Não trata arquivo .env")
            issues.append("Falta tratamento .env")
        
        # Verifica tratamento de banco de dados
        if 'sqlite3' in content and 'jarvis_memory.db' in content:
            print("✅ Trata banco de dados")
        else:
            print("❌ Não trata banco de dados")
            issues.append("Falta tratamento banco de dados")
        
        # Verifica tratamento de arquivos temporários
        if 'tempfile' in content or 'temp_screen' in content:
            print("✅ Trata arquivos temporários")
        else:
            print("⚠️ Poderia ter melhor tratamento de arquivos temporários")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        issues.append(f"Erro: {e}")
    
    return len(issues) == 0, issues

def generate_report():
    """Gera relatório completo"""
    print("🤖 J.A.R.V.I.S. - CHECKLIST PYINSTALLER")
    print("=" * 60)
    
    all_good = True
    all_issues = []
    
    # Verificações
    imports_ok, missing_imports = check_imports()
    all_good = all_good and imports_ok
    all_issues.extend(missing_imports)
    
    files_ok, missing_files = check_file_structure()
    all_good = all_good and files_ok
    all_issues.extend(missing_files)
    
    code_ok, code_issues = check_code_structure()
    all_good = all_good and code_ok
    all_issues.extend(code_issues)
    
    gui_ok, gui_issues = check_gui_specific()
    all_good = all_good and gui_ok
    all_issues.extend(gui_issues)
    
    resources_ok, resource_issues = check_resource_handling()
    all_good = all_good and resources_ok
    all_issues.extend(resource_issues)
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📋 RELATÓRIO FINAL")
    print("=" * 60)
    
    if all_good:
        print("🎉 CÓDIGO 100% PRONTO PARA PYINSTALLER!")
        print("\n✅ Todos os checks passaram:")
        print("  ✅ Imports funcionais")
        print("  ✅ Arquivos necessários presentes")
        print("  ✅ Estrutura do código adequada")
        print("  ✅ Aspectos de GUI tratados")
        print("  ✅ Recursos bem gerenciados")
        
        print("\n🚀 PODE PROSSEGUIR COM PYINSTALLER!")
        print("\nComando sugerido:")
        print("pyinstaller --name JarvisGUI --onefile --windowed --add-data .env;. jarvis_gui_integrada.py")
        
    else:
        print("⚠️ CÓDIGO PRECISA DE AJUSTES")
        print(f"\n❌ Issues encontrados: {len(all_issues)}")
        
        for issue in all_issues:
            print(f"  • {issue}")
        
        print("\n🔧 RESOLVA OS ISSUES ANTES DE PROSSEGUIR")
    
    print("\n" + "=" * 60)
    return all_good

if __name__ == "__main__":
    generate_report()
    print("\nRelatório gerado. O programa será encerrado.")
