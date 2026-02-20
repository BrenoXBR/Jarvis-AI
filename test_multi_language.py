#!/usr/bin/env python3
"""
Script para testar o Multi-Language Generator do Jarvis
"""

from multi_language_generator import MultiLanguageGenerator
from config import Config

def test_multi_language_generator():
    """Testa as funcionalidades do Multi-Language Generator"""
    print("=" * 70)
    print("    TESTE DO MULTI-LANGUAGE GENERATOR")
    print("=" * 70)
    
    # Inicializa o gerador
    generator = MultiLanguageGenerator(workspace_path=Config.WORKSPACE_PATH)
    
    # Mostra ferramentas instaladas
    print("🔧 Ferramentas detectadas:")
    for lang, tools in generator.installed_tools.items():
        status = "✅" if (tools['compiler_available'] or tools['interpreter_available']) else "❌"
        print(f"  {status} {lang.upper()}: Compilador={tools['compiler_available']}, Interpretador={tools['interpreter_available']}")
    
    print(f"\n📁 Workspace: {Config.WORKSPACE_PATH}")
    print("\nTestando comandos:")
    print("-" * 50)
    
    # Lista de comandos para testar
    test_commands = [
        "crie um script em python para calcular o fatorial de um número",
        "gere um código em C++ para ordenar um array usando bubble sort",
        "faça um programa em JavaScript para criar uma API REST simples",
        "escreva um código em Java para implementar uma lista encadeada",
        "crie um script em Rust para calcular números fibonacci",
        "gere um programa em Go para fazer um servidor web básico",
        "faça um código em C para ler um arquivo de texto",
        "escreva um programa em C# para conectar a um banco de dados"
    ]
    
    for command in test_commands:
        print(f"\n💻 Comando: '{command}'")
        
        # Testa apenas a interpretação (sem gerar código)
        request = generator.interpret_code_request(command)
        if request:
            print(f"  🎯 Linguagem detectada: {request['language'].upper()}")
            print(f"  📋 Tarefa: {request['task']}")
            
            # Verifica se as ferramentas estão disponíveis
            tools = generator.installed_tools.get(request['language'], {})
            available = tools.get('compiler_available') or tools.get('interpreter_available')
            status = "✅ Disponível" if available else "❌ Não disponível"
            print(f"  🔧 Ferramentas: {status}")
        else:
            print("  ❌ Não foi possível interpretar o comando")
    
    print("\n" + "=" * 70)
    print("Para testar com geração real de código, execute:")
    print("python jarvis_assistant.py")
    print("E diga: 'Jarvis, crie um script em python para hello world'")

if __name__ == "__main__":
    test_multi_language_generator()
