#!/usr/bin/env python3
"""
J.A.R.V.I.S. - Main Entry Point
Stark Industries AI Assistant - Professional Version
"""

import sys
import os
import customtkinter as ctk
from datetime import datetime

# Adiciona o diretório atual ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui import JarvisGUI
    from core import JarvisCore
    from actions import SystemActions
    from logger import JarvisLogger
except ImportError as e:
    # Tratamento de erro crítico de importação
    base_path = os.path.dirname(os.path.abspath(__file__))
    error_file = os.path.join(base_path, 'ERRO_CRITICO.txt')
    
    with open(error_file, 'w', encoding='utf-8') as f:
        f.write("🤖 J.A.R.V.I.S. - ERRO CRÍTICO DE IMPORTAÇÃO\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Sistema: {sys.platform}\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Diretório: {base_path}\n\n")
        f.write("ERRO DETALHADO:\n")
        f.write(str(e) + "\n\n")
        f.write("SOLUÇÕES POSSÍVEIS:\n")
        f.write("1. Verifique se todos os arquivos estão no diretório\n")
        f.write("2. Instale as dependências: pip install -r requirements.txt\n")
        f.write("3. Verifique a versão do Python (3.8+ recomendado)\n")
    
    print(f"❌ Erro crítico salvo em: {error_file}")
    print("Erro ao importar módulos. Verifique o arquivo ERRO_CRITICO.txt para detalhes.")
    sys.exit(1)

def main():
    """Função principal de inicialização"""
    try:
        # Configuração inicial do CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Inicialização dos componentes principais
        logger = JarvisLogger()
        actions = SystemActions(logger)
        core = JarvisCore(logger)
        
        # Inicialização da interface
        app = JarvisGUI(logger, actions, core)
        
        print("🚀 J.A.R.V.I.S. iniciado com sucesso!")
        print("📋 Versão: Professional - Modular Architecture")
        print("🔧 Componentes: GUI, Core, Actions, Logger")
        
        # Inicia o loop principal
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 J.A.R.V.I.S. encerrado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro fatal na inicialização: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
