#!/usr/bin/env python3
"""
Script para testar o Debug Mode do Jarvis
"""

from debug_mode import DebugMode
from config import Config

def test_debug_mode():
    """Testa as funcionalidades do Debug Mode"""
    print("=" * 60)
    print("    TESTE DO DEBUG MODE")
    print("=" * 60)
    
    # Inicializa o Debug Mode
    debug = DebugMode(workspace_path=Config.WORKSPACE_PATH)
    
    print(f"📁 Workspace: {Config.WORKSPACE_PATH}")
    print(f"🔧 Máximo de tentativas: {debug.max_attempts}")
    print(f"📝 Log directory: {Config.WORKSPACE_PATH}/jarvis_logs")
    
    print("\nTestando análise de erros:")
    print("-" * 40)
    
    # Testes de análise de erros
    test_cases = [
        {
            'language': 'python',
            'error': 'File "test.py", line 5\n    print(x)\nNameError: name \'x\' is not defined',
            'code': 'print(x)',
            'task': 'imprimir variável'
        },
        {
            'language': 'cpp',
            'error': 'error: expected \';\' before \'}\' token',
            'code': 'int main() { return 0 }',
            'task': 'compilar programa'
        },
        {
            'language': 'javascript',
            'error': 'ReferenceError: myVar is not defined',
            'code': 'console.log(myVar)',
            'task': 'exibir variável'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Teste {i}: {test_case['language'].upper()}")
        print(f"   Erro: {test_case['error'][:50]}...")
        
        analysis = debug.analyze_error(
            test_case['error'], 
            test_case['language'], 
            test_case['code'], 
            test_case['task']
        )
        
        print(f"   📊 Tipo: {analysis['error_type']}")
        print(f"   🎯 Severidade: {analysis['severity']}")
        print(f"   📍 Linha: {analysis['error_line']}")
        print(f"   💬 Mensagem: {analysis['error_message'][:100]}...")
    
    print("\n" + "=" * 60)
    print("Para testar com IA real, execute:")
    print("python jarvis_assistant.py")
    print("E diga: 'Jarvis, crie um script em python com erro proposital'")
    print("\nLogs serão salvos em: jarvis_logs/")

if __name__ == "__main__":
    test_debug_mode()
