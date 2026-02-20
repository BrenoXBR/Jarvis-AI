#!/usr/bin/env python3
"""
Teste dos sistemas de Visão e Limpeza do Jarvis
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PyQt6.QtCore import QTimer
from jarvis_vision import VisionCommandHandler
from jarvis_cleanup import CleanupCommandHandler
from dotenv import load_dotenv

class VisionCleanupTestWindow(QWidget):
    """Janela de teste para visão e limpeza"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Vision & Cleanup Test")
        self.setGeometry(100, 100, 500, 400)
        
        # Layout
        layout = QVBoxLayout()
        
        # Área de log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(200)
        layout.addWidget(self.log_area)
        
        # Botões de visão
        self.btn_vision_screen = QPushButton("📸 Analisar Tela Inteira")
        self.btn_vision_screen.clicked.connect(self.test_vision_screen)
        
        self.btn_vision_window = QPushButton("🖼️ Analisar Janela Ativa")
        self.btn_vision_window.clicked.connect(self.test_vision_window)
        
        self.btn_vision_code = QPushButton("🐛 Analisar Erro de Código")
        self.btn_vision_code.clicked.connect(self.test_vision_code)
        
        # Botões de limpeza
        self.btn_cleanup_temp = QPushButton("🧹 Limpar Temporários")
        self.btn_cleanup_temp.clicked.connect(self.test_cleanup_temp)
        
        self.btn_cleanup_logs = QPushButton("📋 Limpar Logs")
        self.btn_cleanup_logs.clicked.connect(self.test_cleanup_logs)
        
        self.btn_cleanup_full = QPushButton("⚡ Protocolo Completo")
        self.btn_cleanup_full.clicked.connect(self.test_cleanup_full)
        
        # Adiciona ao layout
        layout.addWidget(self.btn_vision_screen)
        layout.addWidget(self.btn_vision_window)
        layout.addWidget(self.btn_vision_code)
        layout.addWidget(QLabel("---"))
        layout.addWidget(self.btn_cleanup_temp)
        layout.addWidget(self.btn_cleanup_logs)
        layout.addWidget(self.btn_cleanup_full)
        
        self.setLayout(layout)
        
        # Inicializa handlers
        self.init_handlers()
        
    def init_handlers(self):
        """Inicializa os handlers"""
        try:
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
            workspace_path = os.getenv('WORKSPACE_PATH', os.getcwd())
            
            self.vision_handler = VisionCommandHandler(api_key)
            self.cleanup_handler = CleanupCommandHandler(workspace_path)
            
            self.log("✅ Handlers inicializados com sucesso!")
            
        except Exception as e:
            self.log(f"❌ Erro ao inicializar: {e}")
            
    def log(self, message, level="INFO"):
        """Adiciona mensagem ao log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] [{level}] {message}")
        
    def test_vision_screen(self):
        """Testa análise de tela completa"""
        self.log("📸 Testando análise de tela inteira...", "INFO")
        result = self.vision_handler.process_vision_command("O que você vê na minha tela?")
        self.log(f"Resultado: {result}", "SUCCESS")
        
    def test_vision_window(self):
        """Testa análise de janela ativa"""
        self.log("🖼️ Testando análise de janela ativa...", "INFO")
        result = self.vision_handler.process_vision_command("Analise esta janela ativa")
        self.log(f"Resultado: {result}", "SUCCESS")
        
    def test_vision_code(self):
        """Testa análise de erro de código"""
        self.log("🐛 Testando análise de erro de código...", "INFO")
        result = self.vision_handler.process_vision_command("O que tem de errado no meu código? Aponte os erros.")
        self.log(f"Resultado: {result}", "SUCCESS")
        
    def test_cleanup_temp(self):
        """Testa limpeza de temporários"""
        self.log("🧹 Testando limpeza de arquivos temporários...", "INFO")
        result = self.cleanup_handler.process_cleanup_command("limpar temporários", self.log)
        self.log(f"Resultado: {result}", "SUCCESS")
        
    def test_cleanup_logs(self):
        """Testa limpeza de logs"""
        self.log("📋 Testando limpeza de logs...", "INFO")
        result = self.cleanup_handler.process_cleanup_command("limpar logs", self.log)
        self.log(f"Resultado: {result}", "SUCCESS")
        
    def test_cleanup_full(self):
        """Testa protocolo completo"""
        self.log("⚡ Testando protocolo de encerramento completo...", "WARNING")
        result = self.cleanup_handler.process_cleanup_command("protocolo de encerramento", self.log)
        self.log(f"Resultado: {result}", "SUCCESS")

def main():
    """Função principal do teste"""
    app = QApplication(sys.argv)
    window = VisionCleanupTestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
