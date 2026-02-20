#!/usr/bin/env python3
"""
Teste do Sistema de Threads do Jarvis
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer
from jarvis_threads import ThreadManager

class ThreadTestWindow(QWidget):
    """Janela de teste para o sistema de threads"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Thread Test")
        self.setGeometry(100, 100, 400, 300)
        
        # Layout
        layout = QVBoxLayout()
        
        # Botões de teste
        self.btn_test_voice = QPushButton("Testar Voz")
        self.btn_test_voice.clicked.connect(self.test_voice)
        
        self.btn_test_ai = QPushButton("Testar IA")
        self.btn_test_ai.clicked.connect(self.test_ai)
        
        self.btn_test_queue = QPushButton("Testar Fila")
        self.btn_test_queue.clicked.connect(self.test_queue)
        
        # Adiciona ao layout
        layout.addWidget(self.btn_test_voice)
        layout.addWidget(self.btn_test_ai)
        layout.addWidget(self.btn_test_queue)
        
        self.setLayout(layout)
        
        # Inicializa thread manager
        self.init_thread_manager()
        
    def init_thread_manager(self):
        """Inicializa o thread manager"""
        try:
            from dotenv import load_dotenv
            import os
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
            
            self.thread_manager = ThreadManager(api_key)
            
            # Conecta sinais
            self.thread_manager.voice_state_changed.connect(self.on_state_change)
            self.thread_manager.log_message.connect(self.on_log)
            
            # Inicia
            self.thread_manager.start_all()
            
            self.setWindowTitle("Jarvis Thread Test - ✅ Ativo")
            print("✅ Thread manager iniciado com sucesso!")
            
        except Exception as e:
            self.setWindowTitle(f"Jarvis Thread Test - ❌ Erro: {e}")
            print(f"❌ Erro ao iniciar threads: {e}")
            
    def test_voice(self):
        """Testa o sistema de voz"""
        print("🎤 Testando sistema de voz...")
        self.thread_manager.speak("Teste do sistema de voz em thread separada.")
        
    def test_ai(self):
        """Testa o sistema de IA"""
        print("🤖 Testando sistema de IA...")
        self.thread_manager.ai_worker.process_command(
            "Qual é a capital do Brasil?", 
            "Teste do sistema de threads"
        )
        
    def test_queue(self):
        """Testa o sistema de filas"""
        print("📋 Testando sistema de filas...")
        
        # Envia múltiplas mensagens
        messages = [
            "Primeira mensagem da fila",
            "Segunda mensagem da fila",
            "Terceira mensagem da fila"
        ]
        
        for msg in messages:
            self.thread_manager.speak(msg)
            time.sleep(0.5)  # Pequeno intervalo
            
    def on_state_change(self, state):
        """Recebe mudanças de estado"""
        print(f"🔄 Estado mudou para: {state}")
        
    def on_log(self, message, level):
        """Recebe logs"""
        print(f"[{level}] {message}")
        
    def closeEvent(self, event):
        """Evento de fechamento"""
        if self.thread_manager:
            self.thread_manager.stop_all()
        event.accept()

def main():
    """Função principal do teste"""
    app = QApplication(sys.argv)
    window = ThreadTestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
