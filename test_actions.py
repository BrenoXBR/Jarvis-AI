#!/usr/bin/env python3
"""
Script para testar as ações do Action Handler
"""

from action_handler import ActionHandler
from config import Config

def test_action_handler():
    """Testa as funcionalidades do Action Handler"""
    print("=" * 50)
    print("    TESTE DO ACTION HANDLER")
    print("=" * 50)
    
    # Inicializa o Action Handler
    handler = ActionHandler(workspace_path=Config.WORKSPACE_PATH)
    
    # Lista de comandos para testar
    test_commands = [
        "abra o chrome",
        "abra o spotify", 
        "liste os arquivos do workspace",
        "liste os arquivos da desktop",
        "abra o bloco de notas",
        "abra o calculadora",
        "abra o vscode"
    ]
    
    print(f"Workspace: {Config.WORKSPACE_PATH}")
    print(f"Ações do sistema: {Config.ENABLE_SYSTEM_ACTIONS}")
    print("\nTestando comandos:")
    print("-" * 30)
    
    for command in test_commands:
        print(f"\n🔧 Comando: '{command}'")
        result = handler.interpret_and_execute(command)
        if result:
            print(f"✅ Resultado: {result}")
        else:
            print("❌ Nenhuma ação executada")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_action_handler()
