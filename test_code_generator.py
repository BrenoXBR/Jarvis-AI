#!/usr/bin/env python3
"""
Script para testar o Code Generator do Jarvis
"""

from code_generator import CodeGenerator
from config import Config

def test_code_generator():
    """Testa as funcionalidades do Code Generator"""
    print("=" * 60)
    print("    TESTE DO CODE GENERATOR")
    print("=" * 60)
    
    # Inicializa o Code Generator
    generator = CodeGenerator(workspace_path=Config.WORKSPACE_PATH)
    
    # Lista de comandos para testar
    test_commands = [
        "crie um script em python para calcular a soma de dois números",
        "gere um código python para listar arquivos de um diretório",
        "faça um script em python para converter temperatura Celsius para Fahrenheit",
        "escreva um código python para verificar se um número é primo",
        "crie um programa em python para inverter uma string"
    ]
    
    print(f"Workspace: {Config.WORKSPACE_PATH}")
    print("\nTestando comandos:")
    print("-" * 40)
    
    for command in test_commands:
        print(f"\n💻 Comando: '{command}'")
        result = generator.process_code_request(command)
        if result:
            print(f"✅ Resultado: {result}")
        else:
            print("❌ Nenhuma ação executada")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_code_generator()
