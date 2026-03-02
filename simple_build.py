#!/usr/bin/env python3
"""
Script simples para construir o executável
"""

import subprocess
import sys

def build():
    """Constrói o executável"""
    print("🔨 Construindo JarvisGUI.exe...")
    
    cmd = [
        'pyinstaller',
        '--name=JarvisGUI',
        '--onefile',
        '--noconsole',  # --windowed pode causar problemas, usar --noconsole
        '--icon=jarvis.ico',  # Adiciona ícone
        '--add-data=.env;.',  # Inclui arquivo .env
        '--hidden-import=customtkinter',
        '--hidden-import=google.generativeai',
        '--hidden-import=speech_recognition',
        '--hidden-import=pyttsx3',
        '--hidden-import=pyautogui',
        '--hidden-import=PIL',
        '--hidden-import=sqlite3',
        '--hidden-import=dotenv',
        'jarvis_gui_integrada.py'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Sucesso! Executável em dist/JarvisGUI.exe")
            return True
        else:
            print("❌ Erro:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = build()
    print("\nBuild concluído. O programa será encerrado.")
    sys.exit(0 if success else 1)
