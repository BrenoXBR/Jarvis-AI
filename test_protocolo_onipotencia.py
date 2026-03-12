#!/usr/bin/env python3
"""
Teste do Protocolo Omnipotência - Jarvis Mark 13
Testa todas as funcionalidades implementadas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logger import JarvisLogger
from actions import SystemActions

def test_web_functionalities():
    """Testa funcionalidades web"""
    print("🌐 TESTANDO FUNCIONALIDADES WEB...")
    
    logger = JarvisLogger()
    actions = SystemActions(logger)
    
    # Testa clima
    print("\n🌤️ Testando clima...")
    result = actions.get_weather_votorantim()
    print(f"Resultado: {result}")
    
    # Testa cotação
    print("\n💱 Testando cotação...")
    result = actions.get_currency_final("dólar")
    print(f"Resultado: {result}")
    
    # Testa notícias
    print("\n📰 Testando notícias...")
    result = actions.get_news_headlines()
    print(f"Resultado: {result}")

def test_system_functionalities():
    """Testa funcionalidades de sistema"""
    print("\n🖥️ TESTANDO FUNCIONALIDADES DE SISTEMA...")
    
    logger = JarvisLogger()
    actions = SystemActions(logger)
    
    # Testa status do sistema
    print("\n📊 Testando status do sistema...")
    result = actions.get_system_status()
    print(f"Resultado: {result}")
    
    # Testa processos
    print("\n⚡ Testando top processos...")
    result = actions.get_top_processes()
    print(f"Resultado: {result}")
    
    # Testa gerador de senha
    print("\n🔐 Testando gerador de senha...")
    result = actions.generate_password(12)
    print(f"Resultado: {result}")

def test_focus_functionalities():
    """Testa funcionalidades de foco"""
    print("\n🎯 TESTANDO FUNCIONALIDADES DE FOCO...")
    
    logger = JarvisLogger()
    actions = SystemActions(logger)
    
    # Testa música
    print("\n🎵 Testando busca de música...")
    result = actions.play_music("test music")
    print(f"Resultado: {result}")
    
    # Testa Pomodoro
    print("\n⏰ Testando Pomodoro...")
    result = actions.start_pomodoro_timer("Teste")
    print(f"Resultado: {result}")

def main():
    """Função principal de teste"""
    print("🤖 J.A.R.V.I.S. Mark 13 - Protocolo Omnipotência Test Suite")
    print("=" * 60)
    
    try:
        # Testa web
        test_web_functionalities()
        
        # Testa sistema
        test_system_functionalities()
        
        # Testa foco
        test_focus_functionalities()
        
        print("\n✅ Testes concluídos! Verifique os logs para detalhes.")
        
    except Exception as e:
        print(f"\n❌ Erro nos testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
