#!/usr/bin/env python3
"""
Teste do Sistema de Memória do Jarvis
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit
from PyQt6.QtCore import QTimer
from jarvis_memory import MemoryManager
from dotenv import load_dotenv

class MemoryTestWindow(QWidget):
    """Janela de teste para sistema de memória"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Memory Test")
        self.setGeometry(100, 100, 600, 500)
        
        # Layout
        layout = QVBoxLayout()
        
        # Área de log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(200)
        layout.addWidget(self.log_area)
        
        # Input para simular comandos
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Digite um comando como se fosse o usuário...")
        layout.addWidget(self.input_field)
        
        # Botões de teste
        self.btn_test_input = QPushButton("🧠 Processar Input")
        self.btn_test_input.clicked.connect(self.test_input_processing)
        
        self.btn_search_memory = QPushButton("🔍 Buscar Memória")
        self.btn_search_memory.clicked.connect(self.test_memory_search)
        
        self.btn_get_context = QPushButton("📋 Obter Contexto IA")
        self.btn_get_context.clicked.connect(self.test_context_generation)
        
        self.btn_show_stats = QPushButton("📊 Mostrar Estatísticas")
        self.btn_show_stats.clicked.connect(self.test_memory_stats)
        
        self.btn_cleanup = QPushButton("🧹 Limpar Memória Antiga")
        self.btn_cleanup.clicked.connect(self.test_memory_cleanup)
        
        # Adiciona ao layout
        layout.addWidget(self.btn_test_input)
        layout.addWidget(self.btn_search_memory)
        layout.addWidget(self.btn_get_context)
        layout.addWidget(self.btn_show_stats)
        layout.addWidget(self.btn_cleanup)
        
        self.setLayout(layout)
        
        # Inicializa Memory Manager
        self.init_memory_manager()
        
    def init_memory_manager(self):
        """Inicializa o Memory Manager"""
        try:
            workspace_path = os.getcwd()
            self.memory_manager = MemoryManager(os.path.join(workspace_path, 'test_memory.db'))
            self.log("✅ Memory Manager inicializado para testes!")
            
        except Exception as e:
            self.log(f"❌ Erro ao inicializar: {e}")
            
    def log(self, message, level="INFO"):
        """Adiciona mensagem ao log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] [{level}] {message}")
        
    def test_input_processing(self):
        """Testa processamento de input"""
        user_input = self.input_field.text().strip()
        if not user_input:
            return
            
        self.log(f"🧠 Processando: '{user_input}'", "INFO")
        
        # Simula processamento
        memory_info = self.memory_manager.process_user_input(user_input, "test_session")
        if memory_info:
            self.log(f"📝 Memória: {memory_info}", "SUCCESS")
        else:
            self.log("📝 Nenhuma informação extraída", "INFO")
            
        # Simula resposta do Jarvis
        jarvis_response = f"Entendido, mestre. {user_input} processado com sucesso."
        self.memory_manager.store_conversation("test_session", user_input, jarvis_response)
        
        self.log(f"🤖 Jarvis: {jarvis_response}", "SUCCESS")
        self.input_field.clear()
        
    def test_memory_search(self):
        """Testa busca na memória"""
        query = "nome"  # Busca por nome como exemplo
        self.log(f"🔍 Buscando: '{query}'", "INFO")
        
        results = self.memory_manager.search_user_info(query)
        if results:
            self.log(f"📋 Resultados encontrados: {len(results)}", "SUCCESS")
            for result in results:
                self.log(f"  - {result['fact']} ({result['category']})", "INFO")
        else:
            self.log("📋 Nenhum resultado encontrado", "WARNING")
            
    def test_context_generation(self):
        """Testa geração de contexto para IA"""
        self.log("📋 Gerando contexto para IA...", "INFO")
        
        context = self.memory_manager.get_context_for_ai("test_session")
        self.log("📋 Contexto gerado:", "SUCCESS")
        self.log(context, "INFO")
        
    def test_memory_stats(self):
        """Testa estatísticas da memória"""
        self.log("📊 Obtendo estatísticas...", "INFO")
        
        stats = self.memory_manager.get_stats()
        self.log("📊 Estatísticas da Memória:", "SUCCESS")
        
        if 'facts_by_category' in stats:
            self.log("  Fatos por categoria:", "INFO")
            for category, count in stats['facts_by_category'].items():
                self.log(f"    - {category}: {count}", "INFO")
                
        if 'total_conversations' in stats:
            self.log(f"  Total de conversas: {stats['total_conversations']}", "INFO")
            
        if 'total_preferences' in stats:
            self.log(f"  Preferências salvas: {stats['total_preferences']}", "INFO")
            
    def test_memory_cleanup(self):
        """Testa limpeza de memória antiga"""
        self.log("🧹 Limpando memória antiga (7 dias)...", "WARNING")
        
        deleted_count = self.memory_manager.cleanup_memory(days=7)
        self.log(f"🧹 Limpeza concluída: {deleted_count} registros removidos", "SUCCESS")

def main():
    """Função principal do teste"""
    app = QApplication(sys.argv)
    window = MemoryTestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
