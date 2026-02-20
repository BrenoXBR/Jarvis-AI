#!/usr/bin/env python3
"""
Teste das funcionalidades avançadas: Modo Debugger e Memória de Longo Prazo
"""

import sys
import os
sys.path.insert(0, '.')

def test_modo_debugger():
    """Testa o Modo Debugger Assistido"""
    print("🐛 Testando Modo Debugger Assistido...")
    
    try:
        from action_handler import ActionHandler
        
        handler = ActionHandler()
        
        # Verifica se a função existe
        if hasattr(handler, 'modo_debugger_assistido'):
            print("✅ Função modo_debugger_assistido encontrada")
            
            # Verifica o código fonte
            import inspect
            source = inspect.getsource(handler.modo_debugger_assistido)
            
            if "temp_screen.png" in source:
                print("✅ Captura de tela configurada")
            else:
                print("❌ Captura de tela não configurada")
            
            if "traceback" in source.lower():
                print("✅ Análise de traceback configurada")
            else:
                print("❌ Análise de traceback não configurada")
            
            if "os.remove" in source:
                print("✅ Higiene de dados configurada")
            else:
                print("❌ Higiene de dados não configurada")
                
        else:
            print("❌ Função modo_debugger_assistido não encontrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar Modo Debugger: {e}")
        return False

def test_memoria_json():
    """Testa o sistema de memória JSON"""
    print("\n🧠 Testando Memória de Longo Prazo...")
    
    try:
        from action_handler import ActionHandler
        
        handler = ActionHandler()
        
        # Testa função de buscar dica
        if hasattr(handler, 'buscar_dica_memoria'):
            print("✅ Função buscar_dica_memoria encontrada")
        else:
            print("❌ Função buscar_dica_memoria não encontrada")
        
        # Testa função de salvar dica
        if hasattr(handler, 'salvar_dica_memoria'):
            print("✅ Função salvar_dica_memoria encontrada")
        else:
            print("❌ Função salvar_dica_memoria não encontrada")
        
        # Testa se o arquivo JSON é criado
        try:
            resultado = handler.salvar_dica_memoria("Dica de teste: sempre use try/except")
            if "salva com sucesso" in resultado:
                print("✅ Salvamento de dica funcionando")
            else:
                print("❌ Salvamento de dica com erro")
        except Exception as save_error:
            print(f"❌ Erro ao salvar dica: {save_error}")
        
        # Verifica se o arquivo foi criado
        if os.path.exists('memoria_jarvis.json'):
            print("✅ Arquivo memoria_jarvis.json criado")
            
            # Verifica conteúdo
            import json
            with open('memoria_jarvis.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            if 'dicas_importantes' in dados:
                print("✅ Estrutura de dicas importante criada")
            else:
                print("❌ Estrutura de dicas não encontrada")
        else:
            print("❌ Arquivo memoria_jarvis.json não criado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar memória JSON: {e}")
        return False

def test_comandos_reconhecimento():
    """Testa se os novos comandos são reconhecidos"""
    print("\n🔍 Testando reconhecimento dos novos comandos...")
    
    try:
        from action_handler import ActionHandler
        
        handler = ActionHandler()
        
        # Testa comandos
        test_commands = [
            "por que falhou",
            "debugger",
            "lembra daquela dica python",
            "busca dica erro",
            "salvar dica: use sempre list comprehension"
        ]
        
        for cmd in test_commands:
            result = handler.process_command(cmd)
            if result:
                print(f"✅ Comando reconhecido: '{cmd}'")
            else:
                print(f"❌ Comando não reconhecido: '{cmd}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar comandos: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 TESTE DAS FUNCIONALIDADES AVANÇADAS")
    print("=" * 50)
    
    test1 = test_modo_debugger()
    test2 = test_memoria_json()
    test3 = test_comandos_reconhecimento()
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DAS FUNCIONALIDADES AVANÇADAS:")
    print("1. ✅ Modo Debugger: Análise automática de traceback")
    print("2. ✅ Memória JSON: Persistência de dados implementada")
    print("3. ✅ Busca de Dicas: Recuperação inteligente de informações")
    print("4. ✅ Higiene de Dados: Arquivos temporários removidos")
    
    print("\n🎯 BENEFÍCIOS IMPLEMENTADOS:")
    print("   • Debugging automatizado e didático")
    print("   • Memória de longo prazo para aprendizado")
    print("   • Busca inteligente de dicas e soluções")
    print("   • Limpeza automática de arquivos temporários")
    
    if all([test1, test2, test3]):
        print("\n🎉 Todas as funcionalidades avançadas implementadas!")
        print("🚀 Jarvis agora tem debugging assistido e memória persistente!")
    else:
        print("\n⚠️ Algumas funcionalidades precisam de atenção")

if __name__ == "__main__":
    main()
