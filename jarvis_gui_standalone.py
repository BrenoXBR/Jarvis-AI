#!/usr/bin/env python3
"""
Versão standalone da GUI Jarvis para testes
"""

import sys
from PyQt6.QtWidgets import QApplication
from jarvis_gui import JarvisGUI
import threading
import time

def test_gui():
    """Função para testar a GUI standalone"""
    app = QApplication(sys.argv)
    window = JarvisGUI()
    window.show()
    
    # Simula algumas atividades para teste
    def simulate_activity():
        time.sleep(2)
        window.log_signal.emit("Sistema iniciado", "SUCCESS")
        window.state_signal.emit("idle")
        
        time.sleep(3)
        window.log_signal.emit("Aguardando palavra-chave 'Jarvis'...", "INFO")
        
        time.sleep(5)
        window.state_signal.emit("listening")
        window.log_signal.emit("Palavra-chave detectada!", "SUCCESS")
        
        time.sleep(2)
        window.state_signal.emit("speaking")
        window.speak_signal.emit("Sim, mestre? Estou ouvindo.")
        
        time.sleep(3)
        window.state_signal.emit("processing")
        window.log_signal.emit("Processando comando...", "INFO")
        
        time.sleep(2)
        window.state_signal.emit("speaking")
        window.speak_signal.emit("Abrindo Spotify para você, mestre.")
        
        time.sleep(3)
        window.state_signal.emit("idle")
        window.log_signal.emit("Tarefa concluída", "SUCCESS")
    
    # Inicia simulação em thread separada
    activity_thread = threading.Thread(target=simulate_activity, daemon=True)
    activity_thread.start()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    test_gui()
