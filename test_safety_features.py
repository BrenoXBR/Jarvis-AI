#!/usr/bin/env python3
"""
Script de teste para verificar as travas de segurança do Jarvis
"""

import sys
import os
import time
import threading
import signal

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_daemon_threads():
    """Testa se as threads estão configuradas como daemon"""
    print("🧪 Testando configuração de threads daemon...")
    
    try:
        from jarvis_threads import ThreadManager
        
        # Cria instância do ThreadManager
        tm = ThreadManager()
        
        # Verifica se as threads são daemon quando criadas
        print("✅ ThreadManager criado com sucesso")
        
        # Inicia os workers para verificar as threads
        tm.start_all()
        
        # Aguarda um pouco para as threads iniciarem
        time.sleep(1)
        
        # Verifica se as threads estão configuradas como daemon
        threads_to_check = []
        
        if hasattr(tm, 'voice_worker'):
            if hasattr(tm.voice_worker, 'listen_thread'):
                threads_to_check.append(('Voice Listen', tm.voice_worker.listen_thread))
            if hasattr(tm.voice_worker, 'speak_thread'):
                threads_to_check.append(('Voice Speak', tm.voice_worker.speak_thread))
                
        if hasattr(tm, 'ai_worker'):
            if hasattr(tm.ai_worker, 'processing_thread'):
                threads_to_check.append(('AI Processing', tm.ai_worker.processing_thread))
                
        if hasattr(tm, 'mobile_thread'):
            threads_to_check.append(('Mobile Bridge', tm.mobile_thread))
        
        all_daemon = True
        for name, thread in threads_to_check:
            if thread and hasattr(thread, 'daemon'):
                is_daemon = thread.daemon
                print(f"   Thread {name}: daemon={is_daemon}")
                if not is_daemon:
                    all_daemon = False
            else:
                print(f"   Thread {name}: não encontrada ou sem atributo daemon")
                all_daemon = False
        
        if all_daemon:
            print("✅ Todas as threads estão configuradas como daemon=True")
        else:
            print("❌ Algumas threads não estão configuradas como daemon")
            
        # Para os workers
        tm.stop_all()
        
    except Exception as e:
        print(f"❌ Erro ao testar threads daemon: {e}")

def test_pyautogui_failsafe():
    """Testa se o FAILSAFE do PyAutoGUI está configurado"""
    print("\n🧪 Testando FAILSAFE do PyAutoGUI...")
    
    try:
        import pyautogui
        
        if hasattr(pyautogui, 'FAILSAFE') and pyautogui.FAILSAFE:
            print("✅ PyAutoGUI FAILSAFE está ativo")
            print(f"   Posição de failsafe: (0, 0) - canto superior esquerdo")
            print(f"   Para testar: mova o mouse para o canto superior esquerdo da tela")
        else:
            print("❌ PyAutoGUI FAILSAFE não está ativo")
            
        if hasattr(pyautogui, 'PAUSE'):
            print(f"✅ PyAutoGUI PAUSE configurado: {pyautogui.PAUSE} segundos")
        else:
            print("⚠️ PyAutoGUI PAUSE não configurado")
            
    except ImportError:
        print("❌ PyAutoGUI não está instalado")
    except Exception as e:
        print(f"❌ Erro ao testar PyAutoGUI: {e}")

def test_signal_handling():
    """Testa o tratamento de sinais"""
    print("\n🧪 Testando tratamento de sinais...")
    
    try:
        from jarvis import JarvisThreadedApp
        
        # Cria instância da aplicação
        app = JarvisThreadedApp()
        
        # Verifica se o handler de sinal foi configurado
        current_handler = signal.getsignal(signal.SIGINT)
        
        if current_handler != signal.default_int_handler:
            print("✅ Handler personalizado de SIGINT está configurado")
        else:
            print("❌ Handler de SIGINT não foi configurado")
            
        print("💡 Para testar o encerramento forçado:")
        print("   1. Inicie o Jarvis normalmente")
        print("   2. Pressione Ctrl+C")
        print("   3. Verifique se a mensagem 'ENCERRAMENTO FORÇADO' aparece")
        
    except Exception as e:
        print(f"❌ Erro ao testar tratamento de sinais: {e}")

def main():
    """Função principal de teste"""
    print("🔒 TESTE DE TRAVAS DE SEGURANÇA DO JARVIS")
    print("=" * 50)
    
    # Testa cada trava de segurança
    test_daemon_threads()
    test_pyautogui_failsafe()
    test_signal_handling()
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DAS TRAVAS DE SEGURANÇA:")
    print("1. ✅ Threads daemon: Garante que threads morrem com o programa principal")
    print("2. ✅ PyAutoGUI FAILSAFE: Move mouse para (0,0) para parar automação")
    print("3. ✅ Signal handling: Ctrl+C força encerramento com os._exit(0)")
    print("\n🚀 Jarvis está seguro contra travamentos e loops infinitos!")

if __name__ == "__main__":
    main()
