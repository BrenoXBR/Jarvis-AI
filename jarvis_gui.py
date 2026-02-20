#!/usr/bin/env python3
"""
Interface Gráfica Jarvis GUI
Interface Stark com visualizador de áudio e console de log
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QLabel, QPushButton, QFrame, QSystemTrayIcon, QMenu,
    QLineEdit
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QRect
from PyQt6.QtGui import (
    QPainter, QColor, QPen, QBrush, QLinearGradient, QFont,
    QIcon, QPalette, QAction
)
import pyqtgraph as pg
import numpy as np
from datetime import datetime
import threading
import time
from jarvis_threads import ThreadManager

class AudioVisualizer(QWidget):
    """Visualizador de ondas sonoras estilo Stark"""
    
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 100)
        self.wave_data = np.random.random(100) * 0.1  # Dados iniciais
        self.state = "idle"  # idle, listening, speaking
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(50)
        self.phase = 0
        
    def update_animation(self):
        """Atualiza a animação do visualizador"""
        self.phase += 0.1
        
        if self.state == "listening":
            # Ondas ativas quando ouvindo
            self.wave_data = np.sin(np.linspace(0, 4*np.pi + self.phase, 100)) * 0.8
            self.wave_data += np.random.random(100) * 0.2
        elif self.state == "speaking":
            # Ondas intensas quando falando
            self.wave_data = np.sin(np.linspace(0, 6*np.pi + self.phase*2, 100)) * 0.9
            self.wave_data += np.random.random(100) * 0.3
        else:
            # Ondas suaves quando ocioso
            self.wave_data = np.sin(np.linspace(0, 2*np.pi + self.phase*0.5, 100)) * 0.2
            self.wave_data += np.random.random(100) * 0.05
            
        self.update()
        
    def set_state(self, state):
        """Define o estado do visualizador"""
        self.state = state
        
    def paintEvent(self, event):
        """Desenha o visualizador"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fundo escuro
        painter.fillRect(self.rect(), QColor(10, 10, 20, 200))
        
        # Gradiente neon azul
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(0, 255, 255, 150))
        gradient.setColorAt(0.5, QColor(0, 150, 255, 200))
        gradient.setColorAt(1, QColor(0, 255, 255, 150))
        
        pen = QPen(QBrush(gradient), 2)
        painter.setPen(pen)
        
        # Desenha as ondas
        width = self.width()
        height = self.height()
        center_y = height // 2
        
        points = []
        for i, value in enumerate(self.wave_data):
            x = (i / len(self.wave_data)) * width
            y = center_y + (value * height * 0.3)
            points.append((x, y))
            
        if len(points) > 1:
            for i in range(len(points) - 1):
                painter.drawLine(
                    int(points[i][0]), int(points[i][1]),
                    int(points[i+1][0]), int(points[i+1][1])
                )

class LogConsole(QPlainTextEdit):
    """Console de log em tempo real"""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumHeight(150)
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(10, 10, 20, 180);
                color: #00ffff;
                border: 1px solid #00ffff;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10px;
            }
        """)
        self.setMaximumBlockCount(100)  # Limita número de linhas
        
    def add_log(self, message, level="INFO"):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Cores por nível
        colors = {
            "INFO": "#00ffff",
            "SUCCESS": "#00ff00",
            "WARNING": "#ffff00",
            "ERROR": "#ff4444",
            "SPEAKING": "#ff00ff"
        }
        
        color = colors.get(level, "#00ffff")
        formatted_message = f'<span style="color: #888888;">[{timestamp}]</span> <span style="color: {color};">[{level}]</span> <span style="color: #ffffff;">{message}</span>'
        
        self.appendHtml(formatted_message)
        
        # Auto-scroll para o final
        cursor = self.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.setTextCursor(cursor)

class JarvisGUI(QMainWindow):
    """Janela principal do Jarvis GUI com threads"""
    
    def __init__(self):
        super().__init__()
        self.thread_manager = None
        self.init_ui()
        self.setup_tray_icon()
        self.init_thread_manager()
        
    def init_thread_manager(self):
        """Inicializa o gerenciador de threads"""
        try:
            from dotenv import load_dotenv
            import os
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
            workspace_path = os.getenv('WORKSPACE_PATH', os.getcwd())
            
            self.thread_manager = ThreadManager(api_key, workspace_path)
            
            # Conecta sinais do thread manager
            self.thread_manager.voice_state_changed.connect(self.on_state_change)
            self.thread_manager.log_message.connect(self.on_log)
            
            # Inicia os workers
            self.thread_manager.start_all()
            
            self.on_log("Sistema de threads iniciado", "SUCCESS")
            
            # Configura timer para verificar desligamento
            self.shutdown_timer = QTimer()
            self.shutdown_timer.timeout.connect(self.check_shutdown)
            self.shutdown_timer.start(2000)  # Verifica a cada 2 segundos
            
        except Exception as e:
            self.on_log(f"Erro ao iniciar threads: {e}", "ERROR")
        
    def init_ui(self):
        """Inicializa a interface"""
        # Configurações da janela
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 300)
        
        # Posição inicial (canto superior direito)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 420, 20)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Frame principal com borda neon
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 10, 20, 200);
                border: 2px solid #00ffff;
                border-radius: 10px;
            }
        """)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header com título e controles
        header_layout = QHBoxLayout()
        
        # Título
        title = QLabel("J.A.R.V.I.S.")
        title.setStyleSheet("""
            QLabel {
                color: #00ffff;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Arial', sans-serif;
                text-shadow: 0 0 10px #00ffff;
            }
        """)
        
        # Botão de fechar
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ff4444;
                border: 1px solid #ff4444;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff4444;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        
        # Visualizador de áudio
        self.visualizer = AudioVisualizer()
        
        # Status label
        self.status_label = QLabel("🔴 OFFLINE")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #ff4444;
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
                background-color: rgba(255, 68, 68, 30);
                border-radius: 5px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Console de log
        self.log_console = LogConsole()
        
        # Campo de texto para comandos
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Digite um comando para Jarvis (ex: abrir bloco de notas)...")
        self.command_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(20, 20, 30, 180);
                color: #00ffff;
                border: 1px solid #00ffff;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #00ff00;
            }
        """)
        self.command_input.returnPressed.connect(self.on_command_entered)
        
        # Conecta sinais (removidos os sinais locais, agora usa thread manager)
        
        # Monta o layout
        frame_layout.addLayout(header_layout)
        frame_layout.addWidget(self.visualizer)
        frame_layout.addWidget(self.status_label)
        frame_layout.addWidget(QLabel("Console:"))
        frame_layout.addWidget(self.log_console)
        frame_layout.addWidget(QLabel("Comandos:"))
        frame_layout.addWidget(self.command_input)
        
        main_layout.addWidget(main_frame)
        
        # Permitir mover a janela
        self.drag_position = None
        
    def setup_tray_icon(self):
        """Configura o ícone na bandeja do sistema"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            
            # Cria um ícone simples
            pixmap = QIcon()
            # Aqui você poderia adicionar um ícone real
            
            # Menu do tray
            tray_menu = QMenu()
            
            show_action = QAction("Mostrar", self)
            show_action.triggered.connect(self.show)
            tray_menu.addAction(show_action)
            
            quit_action = QAction("Sair", self)
            quit_action.triggered.connect(QApplication.quit)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
            
    def mousePressEvent(self, event):
        """Permite arrastar a janela"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """Move a janela ao arrastar"""
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseDoubleClickEvent(self, event):
        """Duplo clique para minimizar/restaurar"""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            
    def check_shutdown(self):
        """Verifica se foi solicitado desligamento"""
        if self.thread_manager and self.thread_manager.is_shutdown_requested():
            self.on_log("Encerrando aplicação...", "WARNING")
            self.close()
            
    def closeEvent(self, event):
        """Evento de fechamento da janela"""
        if self.thread_manager:
            self.thread_manager.stop_all()
        event.accept()
        
    def on_command_entered(self):
        """Processa comando digitado pelo usuário"""
        command = self.command_input.text().strip()
        if command:
            print(f"📝 Comando digitado: '{command}'")
            self.log_console.add_log(f"Comando digitado: {command}", "INFO")
            
            # Envia para o thread manager processar
            if self.thread_manager:
                self.thread_manager.process_command(command)
            else:
                self.log_console.add_log("Thread manager não disponível", "ERROR")
            
            # Limpa o campo
            self.command_input.clear()
        
    def on_log(self, message, level="INFO"):
        """Adiciona mensagem ao console"""
        self.log_console.add_log(message, level)
        
    def on_state_change(self, state):
        """Atualiza o estado do visualizador e status"""
        self.visualizer.set_state(state)
        
        if state == "listening":
            self.status_label.setText("🟢 OUVINDO")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #00ff00;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 5px;
                    background-color: rgba(0, 255, 0, 30);
                    border-radius: 5px;
                }
            """)
        elif state == "speaking":
            self.status_label.setText("🔵 FALANDO")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #00aaff;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 5px;
                    background-color: rgba(0, 170, 255, 30);
                    border-radius: 5px;
                }
            """)
        elif state == "processing":
            self.status_label.setText("🟡 PROCESSANDO")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #ffff00;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 5px;
                    background-color: rgba(255, 255, 0, 30);
                    border-radius: 5px;
                }
            """)
        else:
            self.status_label.setText("🔴 OFFLINE")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #ff4444;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 5px;
                    background-color: rgba(255, 68, 68, 30);
                    border-radius: 5px;
                }
            """)

class JarvisGUIManager:
    """Gerenciador da GUI para integração com o assistente"""
    
    def __init__(self):
        self.app = None
        self.window = None
        self.gui_thread = None
        
    def start_gui(self):
        """Inicia a GUI em uma thread separada"""
        if self.app is None:
            self.app = QApplication.instance()
            if self.app is None:
                self.app = QApplication(sys.argv)
                
        self.window = JarvisGUI()
        self.window.show()
        
        # Inicia o event loop
        self.app.exec()
        
    def speak(self, text):
        """Envia texto para a GUI (agora via thread manager)"""
        if self.window and self.window.thread_manager:
            self.window.thread_manager.speak(text)
            
    def log(self, message, level="INFO"):
        """Envia mensagem de log para a GUI"""
        if self.window:
            self.window.on_log(message, level)
            
    def set_state(self, state):
        """Define o estado do visualizador"""
        if self.window:
            self.window.on_state_change(state)

# Instância global para uso pelo assistente
gui_manager = JarvisGUIManager()
