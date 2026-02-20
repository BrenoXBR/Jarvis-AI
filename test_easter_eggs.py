#!/usr/bin/env python3
"""
Teste dos Easter Eggs do Jarvis
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PyQt6.QtCore import QTimer
from jarvis_threads import AIWorker
from dotenv import load_dotenv
import os

class EasterEggTestWindow(QWidget):
    """Janela de teste para Easter Eggs"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Easter Eggs Test")
        self.setGeometry(100, 100, 500, 400)
        
        # Layout
        layout = QVBoxLayout()
        
        # Área de log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(150)
        layout.addWidget(self.log_area)
        
        # Botões de teste
        self.btn_sarcasm = QPushButton("😏 Testar Sarcasmo Elegante")
        self.btn_sarcasm.clicked.connect(self.test_sarcasm)
        
        self.btn_ultron = QPushButton("🤖 Referência Ultron")
        self.btn_ultron.clicked.connect(self.test_ultron_reference)
        
        self.btn_party = QPushButton("🎉 Protocolo 'Festa em Casa'")
        self.btn_party.clicked.connect(self.test_party_protocol)
        
        self.btn_complex_task = QPushButton("💻 Tarefa Complexa")
        self.btn_complex_task.clicked.connect(self.test_complex_task)
        
        self.btn_obvious = QPushButton("🤔 Pergunta Óbvia")
        self.btn_obvious.clicked.connect(self.test_obvious_question)
        
        # Adiciona ao layout
        layout.addWidget(self.btn_sarcasm)
        layout.addWidget(self.btn_ultron)
        layout.addWidget(self.btn_party)
        layout.addWidget(self.btn_complex_task)
        layout.addWidget(self.btn_obvious)
        
        self.setLayout(layout)
        
        # Inicializa AI Worker
        self.init_ai_worker()
        
    def init_ai_worker(self):
        """Inicializa o AI Worker para testes"""
        try:
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
            workspace_path = os.getcwd()
            
            self.ai_worker = AIWorker(api_key, workspace_path)
            
            # Conecta sinais
            self.ai_worker.response_ready.connect(self.on_response)
            self.ai_worker.log_message.connect(self.on_log)
            
            # Inicia worker
            self.ai_worker.start_processing()
            
            self.log("✅ AI Worker inicializado para testes!")
            
        except Exception as e:
            self.log(f"❌ Erro ao inicializar: {e}")
            
    def log(self, message, level="INFO"):
        """Adiciona mensagem ao log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] [{level}] {message}")
        
    def on_response(self, response):
        """Recebe resposta do AI Worker"""
        self.log(f"🤖 Jarvis: {response}", "SUCCESS")
        
    def on_log(self, message, level):
        """Recebe log do AI Worker"""
        self.log(f"[{level}] {message}")
        
    def test_sarcasm(self):
        """Testa sarcasmo elegante"""
        self.log("😏 Testando sarcasmo elegante...", "INFO")
        # Simula pergunta óbvia
        self.ai_worker.process_command("quantos dias tem uma semana?", "Teste de sarcasmo")
        
    def test_ultron_reference(self):
        """Testa referência ao Ultron"""
        self.log("🤖 Testando referência ao Ultron...", "INFO")
        self.ai_worker.process_command("como está o sistema?", "Teste de referência")
        
    def test_party_protocol(self):
        """Testa protocolo 'Festa em Casa'"""
        self.log("🎉 Testando protocolo 'Festa em Casa'...", "INFO")
        self.ai_worker.process_command("festa em casa", "Teste de festa")
        
    def test_complex_task(self):
        """Testa resposta para tarefa complexa"""
        self.log("💻 Testando resposta para tarefa complexa...", "INFO")
        self.ai_worker.process_command("crie um sistema completo em python", "Teste de tarefa complexa")
        
    def test_obvious_question(self):
        """Testa resposta para pergunta óbvia"""
        self.log("🤔 Testando resposta para pergunta óbvia...", "INFO")
        self.ai_worker.process_command("que dia é hoje?", "Teste de pergunta óbvia")

def main():
    """Função principal do teste"""
    app = QApplication(sys.argv)
    window = EasterEggTestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
