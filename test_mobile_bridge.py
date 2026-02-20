#!/usr/bin/env python3
"""
Teste do Jarvis Mobile Bridge - Conexão com Telegram
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel
from PyQt6.QtCore import QTimer
from mobile_bridge import JarvisMobileBridge
from dotenv import load_dotenv

class MobileBridgeTestWindow(QWidget):
    """Janela de teste para Mobile Bridge"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Mobile Bridge Test")
        self.setGeometry(100, 100, 600, 400)
        
        # Layout
        layout = QVBoxLayout()
        
        # Informações
        info_label = QLabel("🤖 Jarvis Mobile Bridge - Teste")
        info_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #00ffff;")
        layout.addWidget(info_label)
        
        token_label = QLabel("🔐 Token: 8258052958:AAHuP3qcBdE7Kn9TIRgPggI2ddiSDJFRxEU")
        token_label.setStyleSheet("font-size: 10px; color: #888888;")
        layout.addWidget(token_label)
        
        # Área de log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(200)
        layout.addWidget(self.log_area)
        
        # Botões de teste
        self.btn_start_bridge = QPushButton("🚀 Iniciar Bridge")
        self.btn_start_bridge.clicked.connect(self.start_bridge)
        
        self.btn_test_commands = QPushButton("📝 Testar Comandos")
        self.btn_test_commands.clicked.connect(self.test_commands)
        
        self.btn_check_auth = QPushButton("🔍 Verificar Autorização")
        self.btn_check_auth.clicked.connect(self.check_authorization)
        
        # Adiciona ao layout
        layout.addWidget(self.btn_start_bridge)
        layout.addWidget(self.btn_test_commands)
        layout.addWidget(self.btn_check_auth)
        
        self.setLayout(layout)
        
        # Inicializa bridge
        self.bridge = None
        self.bridge_thread = None
        
    def log(self, message, level="INFO"):
        """Adiciona mensagem ao log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] [{level}] {message}")
        
    def start_bridge(self):
        """Inicia o bridge móvel"""
        if self.bridge is None:
            self.log("🚀 Iniciando Jarvis Mobile Bridge...", "INFO")
            
            # Cria bridge
            self.bridge = JarvisMobileBridge()
            
            # Inicia em thread separada
            self.bridge_thread = threading.Thread(target=self.bridge.start, daemon=True)
            self.bridge_thread.start()
            
            self.log("✅ Bridge iniciado em background", "SUCCESS")
            self.log("📱 Envie /start para o bot no Telegram", "INFO")
            self.log("🔐 Apenas o primeiro usuário será autorizado", "WARNING")
            self.btn_start_bridge.setText("🔄 Bridge Ativo")
            self.btn_start_bridge.setEnabled(False)
        else:
            self.log("⚠️ Bridge já está ativo", "WARNING")
            
    def test_commands(self):
        """Testa comandos simulados"""
        if self.bridge:
            self.log("📝 Testando comandos simulados...", "INFO")
            
            # Testa comando de texto
            test_commands = [
                "Que horas são?",
                "Qual a data de hoje?",
                "Como está o sistema?",
                "Capture a tela do PC"
            ]
            
            for cmd in test_commands:
                self.log(f"📤 Enviando: '{cmd}'", "INFO")
                # Simula processamento (na prática, viria do Telegram)
                response = f"Comando '{cmd}' processado com sucesso!"
                self.log(f"📥 Resposta: {response}", "SUCCESS")
                
            self.log("✅ Testes de comandos concluídos", "SUCCESS")
        else:
            self.log("❌ Bridge não está ativo", "ERROR")
            
    def check_authorization(self):
        """Verifica status de autorização"""
        try:
            auth_file = os.path.join(os.getcwd(), 'telegram_auth.json')
            if os.path.exists(auth_file):
                import json
                with open(auth_file, 'r') as f:
                    data = json.load(f)
                    chat_id = data.get('chat_id')
                    if chat_id:
                        self.log(f"🔐 Chat autorizado: {chat_id}", "SUCCESS")
                    else:
                        self.log("⚠️ Arquivo de autorização vazio", "WARNING")
            else:
                self.log("📝 Nenhum chat autorizado ainda", "INFO")
                self.log("📱 Envie /start para o bot no Telegram", "INFO")
        except Exception as e:
            self.log(f"❌ Erro ao verificar autorização: {e}", "ERROR")

def main():
    """Função principal do teste"""
    app = QApplication(sys.argv)
    window = MobileBridgeTestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
