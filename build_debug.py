#!/usr/bin/env python3
"""
Script para construir executável com debug completo
"""

import subprocess
import sys
import os

def build_debug():
    """Constrói executável com debug completo"""
    print("🔨 Construindo JarvisGUI.exe com DEBUG COMPLETO...")
    
    # Limpa builds anteriores
    print("🧹 Limpando builds anteriores...")
    if os.path.exists('dist'):
        import shutil
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Comando PyInstaller com debug completo
    cmd = [
        'pyinstaller',
        '--name=JarvisGUI_Debug',
        '--onefile',
        '--debug=all',  # Debug completo
        '--log-level=DEBUG',  # Log detalhado
        '--noconsole',  # Mantém sem console, mas com debug
        '--icon=jarvis.ico',
        '--add-data=.env;.',
        '--hidden-import=customtkinter',
        '--hidden-import=google.generativeai',
        '--hidden-import=speech_recognition',
        '--hidden-import=pyttsx3',
        '--hidden-import=pyautogui',
        '--hidden-import=PIL',
        '--hidden-import=sqlite3',
        '--hidden-import=dotenv',
        '--collect-all=customtkinter',  # Força coleta completa
        '--collect-all=PIL',  # Força coleta do PIL
        'jarvis_gui_integrada.py'
    ]
    
    print(f"🔧 Executando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("\n📋 SAÍDA DO PYINSTALLER:")
        print("=" * 50)
        print(result.stdout)
        
        if result.stderr:
            print("\n⚠️ STDERR:")
            print("=" * 50)
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ Build com debug concluído com sucesso!")
            print(f"📍 Executável: dist/JarvisGUI_Debug.exe")
            
            # Verifica se o arquivo foi criado
            if os.path.exists('dist/JarvisGUI_Debug.exe'):
                size = os.path.getsize('dist/JarvisGUI_Debug.exe') / (1024*1024)
                print(f"📊 Tamanho: {size:.1f} MB")
            
            return True
        else:
            print(f"\n❌ Erro no build (código: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar PyInstaller: {e}")
        return False

def create_debug_package():
    """Cria pacote com versão debug"""
    print("\n📦 Criando pacote debug...")
    
    package_dir = "Jarvis_Debug_v1.0"
    if os.path.exists(package_dir):
        import shutil
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    # Copia executável debug
    if os.path.exists('dist/JarvisGUI_Debug.exe'):
        import shutil
        shutil.copy('dist/JarvisGUI_Debug.exe', package_dir)
        print("✅ Executável debug copiado")
    
    # Copia arquivos essenciais
    essential_files = ['.env', 'README.md', 'requirements.txt', 'jarvis.ico']
    
    for file_name in essential_files:
        if os.path.exists(file_name):
            shutil.copy(file_name, package_dir)
            print(f"✅ {file_name} copiado")
    
    # Cria instruções debug
    debug_instructions = """🤖 J.A.R.V.I.S. - VERSÃO DEBUG v1.0
🔍 Pacote com Diagnóstico Completo

═══════════════════════════════════════════════════════════════

🎯 OBJETIVO DESTA VERSÃO:

Esta versão foi criada para diagnosticar problemas de inicialização.
Ela inclui:

• Captura global de erros de importação
• Salvamento automático de erros em ERRO_CRITICO.txt
• Log detalhado do PyInstaller
• Debug completo no executável

═══════════════════════════════════════════════════════════════

🔍 COMO USAR PARA DIAGNÓSTICO:

1️⃣ Execute JarvisGUI_Debug.exe
2️⃣ Se fechar silenciosamente, verifique ERRO_CRITICO.txt
3️⃣ Se não criar ERRO_CRITICO.txt, verifique os logs abaixo

═══════════════════════════════════════════════════════════════

📁 ARQUIVOS IMPORTANTES:

• JarvisGUI_Debug.exe → Executável com debug
• ERRO_CRITICO.txt → Criado automaticamente em caso de erro
• .env → Configurações (se necessário)
• README.md → Documentação

═══════════════════════════════════════════════════════════════

🔧 POSSÍVEIS PROBLEMAS E SOLUÇÕES:

❌ Se ERRO_CRITICO.txt mencionar CustomTkinter:
   → Problema: CustomTkinter não foi bundleado corretamente
   → Solução: Reinstalar: pip install --force-reinstall customtkinter

❌ Se ERRO_CRITICO.txt mencionar DLL:
   → Problema: Dependências Windows faltando
   → Solução: Instalar Visual C++ Redistributable

❌ Se ERRO_CRITICO.txt mencionar memória:
   → Problema: Falta de RAM para inicialização
   → Solução: Fechar outros programas

❌ Se não criar ERRO_CRITICO.txt:
   → Problema: Erro antes do Python iniciar
   → Solução: Verificar compatibilidade do Windows

═══════════════════════════════════════════════════════════════

📊 INFORMAÇÕES COLETADAS:

O ERRO_CRITICO.txt incluirá:

• Data/hora do erro
• Sistema operacional
• Versão do Python
• Tipo exato do erro
• Traceback completo
• Lista de arquivos no diretório
• Sugestões de solução

═══════════════════════════════════════════════════════════════

🆘 PRÓXIMOS PASSOS:

1. Execute esta versão debug
2. Cole o conteúdo de ERRO_CRITICO.txt (se criado)
3. Descreva exatamente o que aconteceu
4. Informe seu sistema operacional

═══════════════════════════════════════════════════════════════

🏢 Powered by Stark Industries Debug Division
📅 Versão Debug 1.0 - 2026
"""
    
    with open(os.path.join(package_dir, 'DEBUG_INSTRUCTIONS.txt'), 'w', encoding='utf-8') as f:
        f.write(debug_instructions)
    
    print("✅ Instruções debug criadas")
    print(f"\n🎉 PACOTE DEBUG CRIADO EM: {package_dir}/")

if __name__ == "__main__":
    print("🤖 J.A.R.V.I.S. - BUILD COMPLETO DEBUG")
    print("=" * 50)
    
    success = build_debug()
    
    if success:
        create_debug_package()
        print("\n🎉 PROCESSO DEBUG CONCLUÍDO!")
        print("📦 Use Jarvis_Debug_v1.0/ para testar")
    else:
        print("\n❌ Falha no build debug")
    
    print("\nBuild de debug concluído. O programa será encerrado.")
    sys.exit(0 if success else 1)
