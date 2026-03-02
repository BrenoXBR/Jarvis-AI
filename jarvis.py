#!/usr/bin/env python3
"""
Jarvis Assistant com Sistema de Threads
Versão otimizada com QThread para evitar travamentos
"""

import sys
import os
import time
import signal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from jarvis_gui import JarvisGUI
from jarvis_threads import ThreadManager
from dotenv import load_dotenv

class JarvisThreadedApp:
    """Aplicação Jarvis com sistema de threads"""
    
    def __init__(self):
        self.app = None
        self.window = None
        self.thread_manager = None
        
        # Configura handler para sinal de interrupção (Ctrl+C)
        signal.signal(signal.SIGINT, self._force_shutdown)
        
    def _force_shutdown(self, signum, frame):
        """Força o encerramento completo do sistema"""
        print("\n🛑 ENCERRAMENTO FORÇADO DETECTADO!")
        print("Fechando todos os processos...")
        
        # Tenta parar threads de forma limpa
        if self.thread_manager:
            try:
                self.thread_manager.stop_all()
            except:
                pass
                
        # Fecha a aplicação Qt
        if self.app:
            try:
                self.app.quit()
            except:
                pass
        
        # Força encerramento completo
        print("🔥 EXECUTANDO DESLIGAMENTO FORÇADO!")
        os._exit(0)
        
    def start(self):
        """Inicia a aplicação completa"""
        # Carrega variáveis de ambiente com encoding UTF-8
        load_dotenv(encoding='utf-8')
        
        # Inicializa QApplication
        self.app = QApplication(sys.argv)
        
        # Cria a janela principal
        self.window = JarvisGUI()
        self.window.show()
        
        # O thread manager já é inicializado dentro da GUI
        self.thread_manager = self.window.thread_manager
        
        # Configura timer para manter a aplicação responsiva
        self.setup_heartbeat()
        
        # Inicia o event loop com tratamento de interrupção
        try:
            sys.exit(self.app.exec())
        except KeyboardInterrupt:
            print("\n🛑 Ctrl+C detectado no event loop!")
            self._force_shutdown(None, None)
        
    def setup_heartbeat(self):
        """Configura heartbeat para manter a aplicação responsiva"""
        self.heartbeat_timer = QTimer()
        self.heartbeat_timer.timeout.connect(self.check_system_health)
        self.heartbeat_timer.start(5000)  # Verifica a cada 5 segundos
        
    def check_system_health(self):
        """Verifica a saúde do sistema"""
        if self.thread_manager:
            # Verifica se os workers estão ativos
            if hasattr(self.thread_manager, 'voice_worker'):
                if not self.thread_manager.voice_worker.is_running:
                    print("Voice worker parado, reiniciando...")
                    self.thread_manager.voice_worker.start_listening()

def main():
    """Função principal"""
    # Verifica se está rodando como executável sem console
    if getattr(sys, 'frozen', False):
        try:
            # Redireciona stdin/stdout/stderr para evitar erros
            import io
            sys.stdin = io.StringIO()
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
        except:
            # Se falhar, apenas ignora
            pass
    
    print("Iniciando Jarvis com sistema de threads...")
    print("Interface grafica com processamento paralelo")
    print("Voz e IA em threads separadas")
    print("Interface nunca trava!")
    print("-" * 50)
    
    try:
        app = JarvisThreadedApp()
        app.start()
    except KeyboardInterrupt:
        print("\n🛑 Interrupção pelo usuário detectada!")
        print("Encerrando Jarvis forçadamente...")
        os._exit(0)
    except Exception as e:
        print(f"Erro ao iniciar: {e}")
        print("Encerrando aplicação...")
        os._exit(1)

if __name__ == "__main__":
    main()
