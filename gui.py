"""
J.A.R.V.I.S. - GUI Module
Interface CustomTkinter profissional com System Monitor
"""

import os
import sys
import threading
import time
import customtkinter as ctk
from tkinter import messagebox, scrolledtext
from typing import List, Dict, Optional, Callable
import speech_recognition as sr
import pyautogui
from PIL import Image, ImageTk
import io
import base64

class JarvisGUI:
    """Interface principal do J.A.R.V.I.S. - Professional Version"""
    
    # Cores tema J.A.R.V.I.S. Mark 13 - Deep Charcoal & Electric Blue
    M13_COLORS = {
        "background": "#121212",  # Deep Charcoal
        "surface": "#1e1e1e",     # Charcoal médio
        "primary": "#00FBFF",     # Electric Blue
        "secondary": "#FF006E",    # Neon Pink/Rosa
        "success": "#00FF88",      # Verde neon suave
        "warning": "#FFAA00",     # Amarelo neon
        "ia_text": "#00FBFF",     # Electric Blue para J.A.R.V.I.S.
        "user_text": "#FFFFFF",   # Branco puro
        "system_text": "#FFB700",  # Dourado neon
        "border": "#00FBFF",      # Electric Blue para bordas
        "neon_green": "#00FF88",  # Verde neon para botões
        "neon_blue": "#00D4FF",   # Azul vibrante para botões
        "dark_border": "#2a2a2a"   # Bordas escuras
    }
    
    def __init__(self, logger, actions, core):
        self.logger = logger
        self.actions = actions
        self.core = core
        
        # Estado da interface
        self.is_processing = False
        self.is_listening = False
        self.voice_enabled = False
        self.typing_active = False
        
        # Histórico e mensagens
        self.chat_history = []
        self.current_response = ""
        
        # Componentes da interface
        self.root = None
        self.chat_display = None
        self.text_input = None
        self.send_button = None
        self.voice_button = None
        self.status_label = None
        self.system_monitor = None
        self.system_log_text = None
        self.monitor_visible = False
        
        # Inicialização
        self._setup_voice()
        self._setup_gui()
        
        self.logger.info("GUI inicializada com sucesso", "GUI")
        self.logger.system("Interface profissional carregada", "GUI")
    
    def _setup_voice(self):
        """Configura sistema de voz"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.voice_enabled = True
            self.logger.info("Sistema de voz configurado", "GUI")
        except Exception as e:
            self.logger.error(e, "Erro ao configurar voz", "GUI")
            self.voice_enabled = False
    
    def _setup_gui(self):
        """Configura a interface principal"""
        # Configuração do CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Janela principal
        self.root = ctk.CTk()
        self.root.title("🤖 J.A.R.V.I.S. - M-13 OMNI")
        self.root.geometry("1200x800")
        self.root.configure(fg_color=self.M13_COLORS["background"])
        
        # Layout principal
        self._create_main_layout()
        
        # Configurações finais
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.bind('<Return>', lambda e: self.send_message())
        
        # Mensagem inicial
        self._show_welcome_message()
    
    def _create_main_layout(self):
        """Cria o layout principal da interface"""
        # Container principal
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame superior (cabeçalho) com borda neon
        header_frame = ctk.CTkFrame(
            main_container, 
            fg_color=self.M13_COLORS["surface"], 
            corner_radius=10,
            border_width=2,
            border_color=self.M13_COLORS["border"]
        )
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Título com ícone de processamento
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚡ J.A.R.V.I.S. - M-13 OMNI",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.M13_COLORS["ia_text"]
        )
        title_label.pack(pady=10)
        
        # Barra de status
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="🟢 Systems Online",
            font=ctk.CTkFont(size=12),
            text_color=self.M13_COLORS["success"]
        )
        self.status_label.pack(pady=(0, 10))
        
        # Frame do conteúdo principal
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Layout em duas colunas
        content_grid = ctk.CTkFrame(content_frame, fg_color="transparent")
        content_grid.pack(fill="both", expand=True)
        
        # Coluna esquerda - Chat com borda neon
        chat_frame = ctk.CTkFrame(
            content_grid, 
            fg_color=self.M13_COLORS["surface"], 
            corner_radius=10,
            border_width=2,
            border_color=self.M13_COLORS["border"]
        )
        chat_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        content_grid.grid_columnconfigure(0, weight=3)
        content_grid.grid_rowconfigure(0, weight=1)  # Chat ocupa todo o espaço vertical
        
        self._create_chat_area(chat_frame)
        
        # Coluna direita - System Monitor com borda neon
        monitor_frame = ctk.CTkFrame(
            content_grid, 
            fg_color=self.M13_COLORS["surface"], 
            corner_radius=10,
            border_width=2,
            border_color=self.M13_COLORS["border"]
        )
        monitor_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        content_grid.grid_columnconfigure(1, weight=1)
        content_grid.grid_rowconfigure(0, weight=1)  # Monitor também ocupa todo espaço vertical
        
        self._create_system_monitor(monitor_frame)
    
    def _create_chat_area(self, parent):
        """Cria a área de chat com layout sem espaços vazios"""
        # Container principal que ocupa toda a área
        main_container = ctk.CTkFrame(parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configura grid para controle preciso
        main_container.grid_rowconfigure(0, weight=1)  # Chat ocupa 100% do espaço
        main_container.grid_rowconfigure(1, weight=0)  # Input não expande
        main_container.grid_columnconfigure(0, weight=1)  # Largura total
        
        # Frame do chat (expandido - weight=1)
        chat_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        chat_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        
        # Display de mensagens (ocupa 100% do frame do chat)
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.M13_COLORS["user_text"],
            fg_color=self.M13_COLORS["background"],
            border_width=2,
            border_color=self.M13_COLORS["dark_border"],
            wrap="word"
        )
        self.chat_display.pack(fill="both", expand=True)
        
        # Configura tags para cores
        self.chat_display.tag_config("jarvis", foreground=self.M13_COLORS["ia_text"])
        self.chat_display.tag_config("user", foreground=self.M13_COLORS["user_text"])
        self.chat_display.tag_config("system", foreground=self.M13_COLORS["system_text"])
        
        # Frame de entrada (fixo no rodapé - weight=0)
        input_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        input_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        
        # Campo de texto
        self.text_input = ctk.CTkEntry(
            input_frame,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.M13_COLORS["user_text"],
            fg_color=self.M13_COLORS["surface"],
            border_width=2,
            border_color=self.M13_COLORS["dark_border"],
            placeholder_text="Digite sua mensagem aqui..."
        )
        self.text_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botão de voz (azul vibrante)
        self.voice_button = ctk.CTkButton(
            input_frame,
            text="🎤",
            width=40,
            font=ctk.CTkFont(size=16),
            fg_color=self.M13_COLORS["neon_blue"],
            hover_color="#00A8CC",
            command=self._toggle_listening
        )
        self.voice_button.pack(side="left", padx=(0, 5))
        
        # Botão de envio (verde neon suave)
        self.send_button = ctk.CTkButton(
            input_frame,
            text="Enviar",
            width=80,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=self.M13_COLORS["neon_green"],
            hover_color="#00CC70",
            command=self.send_message
        )
        self.send_button.pack(side="left")
    
    def _create_system_monitor(self, parent):
        """Cria o System Monitor"""
        # Título do monitor
        monitor_header = ctk.CTkFrame(parent, fg_color="transparent")
        monitor_header.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            monitor_header,
            text="🖥️ SYSTEM MONITOR",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=self.M13_COLORS["ia_text"]
        )
        title_label.pack()
        
        # Botão de toggle
        toggle_button = ctk.CTkButton(
            monitor_header,
            text="👁️ SHOW/HIDE",
            width=120,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=self.M13_COLORS["primary"],
            hover_color=self.M13_COLORS["neon_blue"],
            command=self._toggle_monitor
        )
        toggle_button.pack(pady=5)
        
        # Área de log (inicialmente oculta)
        self.system_log_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.system_log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Display de logs com fonte futurista
        self.system_log_text = ctk.CTkTextbox(
            self.system_log_frame,
            font=ctk.CTkFont(family="Consolas", size=9),
            text_color="#00FF88",  # Verde neon para texto terminal
            fg_color="#0a0a0a",    # Preto profundo para fundo
            border_width=2,
            border_color=self.M13_COLORS["border"],
            wrap="word"
        )
        self.system_log_text.pack(fill="both", expand=True)
        
        # Configura para ser somente leitura
        self.system_log_text.configure(state="disabled")
        
        # Botão de limpar logs
        clear_button = ctk.CTkButton(
            self.system_log_frame,
            text="🗑️ CLEAR LOGS",
            width=100,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=self.M13_COLORS["secondary"],
            hover_color="#CC0055",
            command=self._clear_system_logs
        )
        clear_button.pack(pady=(5, 0))
        
        # Inicializa oculto
        self._toggle_monitor()
        
        # Inicia atualização de logs
        self._start_log_updater()
    
    def _toggle_monitor(self):
        """ Alterna visibilidade do System Monitor """
        self.monitor_visible = not self.monitor_visible
        
        if self.monitor_visible:
            self.system_log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            self.logger.system("System Monitor visível", "GUI")
        else:
            self.system_log_frame.pack_forget()
            self.logger.system("System Monitor oculto", "GUI")
    
    def _clear_system_logs(self):
        """Limpa os logs do sistema"""
        self.logger.clear_buffer()
        self.system_log_text.configure(state="normal")
        self.system_log_text.delete("1.0", "end")
        self.system_log_text.configure(state="disabled")
        self.logger.system("Logs do sistema limpos", "GUI")
    
    def _start_log_updater(self):
        """Inicia atualização automática dos logs"""
        def update_logs():
            while True:
                try:
                    if self.monitor_visible and not self.typing_active:
                        # Obtém logs do buffer
                        logs = self.logger.get_buffer_logs(20)
                        
                        if logs:
                            # Atualiza display
                            self.system_log_text.configure(state="normal")
                            self.system_log_text.delete("1.0", "end")
                            
                            for log in logs:
                                self.system_log_text.insert("end", log + "\n")
                            
                            # Auto-scroll para o final
                            self.system_log_text.see("end")
                            self.system_log_text.configure(state="disabled")
                    
                    time.sleep(1)  # Atualiza a cada segundo
                    
                except Exception as e:
                    self.logger.error(e, "Erro no atualizador de logs", "GUI")
                    time.sleep(5)
        
        # Executa em thread separada
        thread = threading.Thread(target=update_logs, daemon=True)
        thread.start()
    
    def _show_welcome_message(self):
        """Exibe mensagem de boas-vindas"""
        welcome_msg = """⚡ J.A.R.V.I.S. Mark 13 - OMNI SYSTEM ONLINE

🔧 **Core Systems Activated:**
• 🎤 Voice Command Interface
• 🖥️ Real-Time System Monitor  
• 🚀 Windows Deep Links Integration
• ⚡ Advanced Energy Protocols
• 🤖 Gemini AI Neural Interface
• 💱 Web APIs (Clima, Cotações, Notícias)
• 🎯 Focus Mode (Pomodoro, Music)

💡 **Quick Commands:**
• "dólar" - Cotação em tempo real
• "tempo hoje" - Clima Votorantim
• "processos" - Top 5 consumo RAM
• "pomodoro" - Timer de 25 min

**OMNI PROTOCOLS ENGAGED** 🚀"""
        
        self.add_message("Jarvis", welcome_msg, is_jarvis=True)
    
    def send_message(self, event=None):
        """Envia mensagem digitada"""
        if self.is_processing:
            return
        
        message = self.text_input.get().strip()
        if not message:
            return
        
        # Limpa campo e atualiza status
        self.text_input.delete(0, "end")
        self._update_status("🟡 Processando...", self.M13_COLORS["warning"])
        
        # Adiciona mensagem do usuário
        self.add_message("Você", message, is_user=True)
        
        # Processa mensagem
        self._process_message(message)
    
    def _process_message(self, message: str):
        """Processa mensagem do usuário"""
        self.is_processing = True
        
        def process_in_thread():
            try:
                # Tenta detectar comando de sistema primeiro
                command_result = self._detect_system_command(message)
                if command_result:
                    self._update_status("🟢 Online", self.M13_COLORS["success"])
                    return
                
                # Se não for comando de sistema, processa com Gemini
                if self.core.is_available():
                    # Prepara contexto
                    conversation_history = self._get_conversation_history()
                    memories = []  # Aqui poderia integrar com sistema de memória
                    system_commands_info = self._get_system_commands_info()
                    
                    # Processa com Gemini
                    response = self.core.process_message(message, conversation_history, memories, system_commands_info)
                    
                    # Exibe com efeito de digitação
                    self._display_with_typing("Jarvis", response)
                else:
                    self.add_message("Jarvis", "❌ API Gemini não disponível. Verifique sua configuração.", is_jarvis=True)
                
            except Exception as e:
                self.logger.error(e, "Erro ao processar mensagem", "GUI")
                self.add_message("Jarvis", f"❌ Erro ao processar: {e}", is_jarvis=True)
            finally:
                self.is_processing = False
                self._update_status("🟢 Online", self.M13_COLORS["success"])
        
        # Executa em thread separada
        thread = threading.Thread(target=process_in_thread, daemon=True)
        thread.start()
    
    def _detect_system_command(self, message: str) -> bool:
        """Detecta e executa comandos de sistema"""
        message_lower = message.lower()
        
        # Comandos de energia
        if any(keyword in message_lower for keyword in ["desligar", "desligue", "desliga", "shutdown", "desligamento"]):
            self._show_power_confirmation("shutdown")
            return True
        
        if any(keyword in message_lower for keyword in ["reiniciar", "reinicie", "restart", "reboot", "reinicialização", "reinicialize"]):
            self._show_power_confirmation("restart")
            return True
        
        if any(keyword in message_lower for keyword in ["suspender", "suspenda", "hibernar", "dormir", "sleep"]):
            result = self.actions.execute_power_command("suspend")
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Comandos de atualizações
        if any(keyword in message_lower for keyword in ["verificar atualizações", "verifique atualizações", "checar atualizações", "check updates", "procurar atualizações"]):
            result = self.actions.open_application("atualizações")
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Comandos de Hardware - Mark 13
        if any(keyword in message_lower for keyword in ["volume", "som", "áudio", "audio"]):
            # Extrai número da mensagem
            import re
            match = re.search(r'\d+', message_lower)
            if match:
                volume = match.group()
                result = self.actions.set_volume(volume)
            else:
                result = "🔊 Por favor, especifique o volume (ex: 'volume em 50')."
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        if any(keyword in message_lower for keyword in ["status do sistema", "sistema status", "status sistema", "uso do sistema", "performance"]):
            result = self.actions.get_system_status()
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        if any(keyword in message_lower for keyword in ["print", "screenshot", "captura", "capturar tela", "print screen", "printar"]):
            result = self.actions.take_screenshot()
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        if any(keyword in message_lower for keyword in ["gerar senha", "criar senha", "senha forte", "password", "gerar password"]):
            # Verifica se especificou comprimento
            import re
            match = re.search(r'\d+', message_lower)
            if match:
                length = int(match.group())
                result = self.actions.generate_password(length)
            else:
                result = self.actions.generate_password()
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        if any(keyword in message_lower for keyword in ["me lembre", "lembrete", "lembrar"]):
            # Extrai tempo
            import re
            time_match = re.search(r'(\d+)\s*(?:minuto| minutos|min|mins)', message_lower)
            if time_match:
                time_str = time_match.group()
            else:
                time_str = "30"  # default 30 minutos
            
            # Encontra a tarefa (após "de")
            task_match = re.search(r'(?:de|em)\s+(.+)', message_lower)
            task = task_match.group(1) if task_match else "tarefa não especificada"
            
            result = self.actions.set_reminder(time_str, task)
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Web - Clima
        if any(keyword in message_lower for keyword in ["tempo hoje", "clima hoje", "previsão do tempo", "tempo agora", "clima agora"]):
            result = self.actions.get_weather_votorantim()
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Web - Notícias
        if any(keyword in message_lower for keyword in ["notícias", "manchetes", "notícia do dia", "jornal"]):
            result = self.actions.get_news_headlines()
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Web - Cotações (específico)
        if any(keyword in message_lower for keyword in ["quanto está o dólar", "cotação do dólar", "dólar hoje", "usd brl"]):
            result = self.actions.get_currency_rate('USD', 'BRL')
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Web - Cotações (genérico)
        if any(keyword in message_lower for keyword in ["dólar", "dolar", "euro", "bitcoin", "real", "peso", "libra"]):
            # Encontra a moeda mencionada
            currency = None
            currencies = ["dólar", "dolar", "euro", "bitcoin", "real", "peso", "libra"]
            for coin in currencies:
                if coin in message_lower:
                    currency = coin
                    break
            
            if currency:
                result = self.actions.get_currency_final(currency)
            else:
                result = self.actions.get_currency_final("dólar")  # Default para dólar
            
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Sistema - Limpar Lixeira
        if any(keyword in message_lower for keyword in ["limpar lixeira", "esvaziar lixeira"]):
            result = self.actions.empty_recycle_bin()
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Sistema - Brilho
        if any(keyword in message_lower for keyword in ["aumentar brilho", "mais brilho", "bright"]):
            result = self.actions.adjust_brightness("aumentar")
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        if any(keyword in message_lower for keyword in ["diminuir brilho", "menos brilho", "dark", "escurecer"]):
            result = self.actions.adjust_brightness("diminuir")
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Sistema - Processos
        if any(keyword in message_lower for keyword in ["processos", "processos ativos", "apps mais consumidos", "top processos", "uso de memória"]):
            result = self.actions.get_top_processes()
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Foco - Música
        if any(keyword in message_lower for keyword in ["tocar", "play", "música", "youtube", "spotify", "ouvir"]):
            # Extrai nome da música/artista
            import re
            music_query = message_lower
            for keyword in ["tocar", "play", "música", "youtube", "spotify", "ouvir"]:
                if keyword in message_lower:
                    music_query = message_lower.replace(keyword, "", 1).strip()
                    break
            
            if music_query:
                result = self.actions.play_music(music_query)
                self.add_message("Jarvis", result, is_jarvis=True)
                return True
        
        # Foco - Pomodoro
        if any(keyword in message_lower for keyword in ["pomodoro", "timer", "cronômetro", "cronometro", "estudar", "foco"]):
            # Extrai tarefa
            task = "Estudo"
            for keyword in ["estudar", "foco"]:
                if keyword in message_lower:
                    task = keyword.title()
                    break
            
            result = self.actions.start_pomodoro_timer(task)
            self.add_message("Jarvis", result, is_jarvis=True)
            return True
        
        # Comandos de aplicativos
        # Extrai nome do aplicativo sem limpeza agressiva
        for keyword in ["abra", "abrir", "abre", "iniciar", "start", "open", "execute", "executar"]:
            if keyword in message_lower:
                # Apenas remove a palavra-chave, mantém o resto intacto
                app_name = message_lower.replace(keyword, "", 1).strip()
                
                if app_name:
                    result = self.actions.open_application(app_name)
                    self.add_message("Jarvis", result, is_jarvis=True)
                    return True
        
        # Comandos diretos sem palavra-chave (ex: "notepad", "calculadora")
        direct_apps = [
            "notepad", "bloco de notas", "calculadora", "calc", "calculator",
            "configurações", "configuracoes", "settings", "painel de controle",
            "cmd", "prompt", "terminal", "powershell", "explorer", "task manager",
            "gerenciador de tarefas", "defender", "windows defender", "antivírus"
        ]
        
        if any(app in message_lower for app in direct_apps):
            for app in direct_apps:
                if app in message_lower:
                    result = self.actions.open_application(app)
                    self.add_message("Jarvis", result, is_jarvis=True)
                    return True
        
        return False
    
    def _show_power_confirmation(self, action: str):
        """Mostra diálogo de confirmação para comandos de energia"""
        # Cria janela de confirmação
        confirm_window = ctk.CTkToplevel(self.root)
        confirm_window.title("🔌 Confirmação de Energia")
        confirm_window.geometry("400x200")
        confirm_window.configure(fg_color=self.M13_COLORS["surface"])
        confirm_window.transient(self.root)
        confirm_window.grab_set()
        
        # Centraliza
        confirm_window.update_idletasks()
        x = (confirm_window.winfo_screenwidth() // 2) - 200
        y = (confirm_window.winfo_screenheight() // 2) - 100
        confirm_window.geometry(f"400x200+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mensagem
        action_names = {"shutdown": "Desligamento", "restart": "Reinicialização"}
        action_name = action_names.get(action, action.title())
        
        message_label = ctk.CTkLabel(
            main_frame,
            text=f"🔌 {action_name} do Sistema\n\nSenhor, os sistemas serão encerrados.\nConfirma o protocolo?",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.M13_COLORS["ia_text"],
            wraplength=350
        )
        message_label.pack(pady=(20, 10))
        
        # Frame dos botões
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=10)
        
        # Botão Não
        no_button = ctk.CTkButton(
            button_frame,
            text="❌ Não",
            width=80,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#FF4444",
            hover_color="#CC0000",
            command=lambda: self._cancel_power_action(confirm_window)
        )
        no_button.pack(side="left", padx=(50, 10), expand=True)
        
        # Botão Sim
        yes_button = ctk.CTkButton(
            button_frame,
            text="✅ Sim",
            width=80,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#44FF44",
            hover_color="#00CC00",
            command=lambda: self._confirm_power_action(confirm_window, action)
        )
        yes_button.pack(side="right", padx=(10, 50), expand=True)
        
        confirm_window.focus_set()
    
    def _cancel_power_action(self, window):
        """Cancela ação de energia"""
        window.destroy()
        self.add_message("Jarvis", "🔌 Ação de energia cancelada, senhor.", is_jarvis=True)
    
    def _confirm_power_action(self, window, action: str):
        """Confirma e executa ação de energia"""
        window.destroy()
        result = self.actions.confirm_power_action(action)
        self.add_message("Jarvis", result, is_jarvis=True)
    
    def _display_with_typing(self, sender: str, message: str):
        """Exibe mensagem com efeito de digitação"""
        if not message or not isinstance(message, str):
            self.add_message(sender, "❌ Mensagem inválida", is_jarvis=True)
            return
        
        # Adiciona ao histórico
        self.chat_history.append({
            'sender': sender,
            'message': message,
            'timestamp': time.time(),
            'is_jarvis': sender == "Jarvis"
        })
        
        # Prepara display
        self.chat_display.configure(state="normal")
        
        # Nome do remetente
        self.chat_display.insert("end", f"\n{sender}:\n", "jarvis" if sender == "Jarvis" else "user")
        
        # Inicia efeito de digitação
        self.typing_active = True
        self.core.start_typing_effect(message, self._typing_callback)
    
    def _typing_callback(self, text: str, is_complete: bool):
        """Callback para efeito de digitação"""
        try:
            # Remove última entrada e adiciona nova
            self.chat_display.configure(state="normal")
            
            # Encontra última linha para substituir
            last_line = self.chat_display.index("end-1c")
            line_start = self.chat_display.index(f"{last_line} linestart")
            
            # Deleta última linha
            self.chat_display.delete(line_start, last_line)
            
            # Insere texto atualizado
            display_text = text if not is_complete else text
            self.chat_display.insert("end", display_text, "jarvis")
            
            # Auto-scroll
            self.chat_display.see("end")
            self.chat_display.configure(state="disabled")
            
            if is_complete:
                self.typing_active = False
                
        except Exception as e:
            self.logger.error(e, "Erro no callback de digitação", "GUI")
    
    def add_message(self, sender: str, message: str, is_user: bool = False, is_jarvis: bool = False, is_system: bool = False):
        """Adiciona mensagem ao chat"""
        # Adiciona ao histórico
        self.chat_history.append({
            'sender': sender,
            'message': message,
            'timestamp': time.time(),
            'is_user': is_user,
            'is_jarvis': is_jarvis,
            'is_system': is_system
        })
        
        # Exibe na interface
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n{sender}:\n", "jarvis" if is_jarvis else "user" if is_user else "system")
        self.chat_display.insert("end", f"{message}\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
    
    def _toggle_listening(self):
        """Alterna modo de escuta de voz"""
        if not self.voice_enabled:
            self.add_message("Sistema", "❌ Sistema de voz não disponível", is_system=True)
            return
        
        if self.is_listening:
            self._stop_listening()
        else:
            self._start_listening()
    
    def _start_listening(self):
        """Inicia modo de escuta"""
        self.is_listening = True
        self.voice_button.configure(
            text="🔴",
            fg_color=self.M13_COLORS["secondary"]
        )
        
        def listen():
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                try:
                    text = self.recognizer.recognize_google(audio, language='pt-BR')
                    self._process_voice_command(text)
                except sr.UnknownValueError:
                    self.add_message("Sistema", "🎤 Não entendi. Tente novamente.", is_system=True)
                except sr.RequestError as e:
                    self.logger.error(e, "Erro na API de reconhecimento", "GUI")
                    self.add_message("Sistema", "❌ Erro no reconhecimento de voz", is_system=True)
                    
            except sr.WaitTimeoutError:
                self.add_message("Sistema", "🎤 Tempo esgotado. Tente novamente.", is_system=True)
            except Exception as e:
                self.logger.error(e, "Erro na escuta de voz", "GUI")
                self.add_message("Sistema", f"❌ Erro: {e}", is_system=True)
            finally:
                self._stop_listening()
        
        # Executa em thread separada
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
    
    def _stop_listening(self):
        """Para modo de escuta"""
        self.is_listening = False
        self.voice_button.configure(
            text="🎤",
            fg_color=self.M13_COLORS["primary"]
        )
    
    def _process_voice_command(self, text: str):
        """Processa comando de voz"""
        self.add_message("Voz", text, is_user=True)
        self._process_message(text)
    
    def _update_status(self, text: str, color: str):
        """Atualiza barra de status"""
        self.status_label.configure(text=text, text_color=color)
    
    def _get_conversation_history(self) -> List[Dict]:
        """Retorna histórico da conversa"""
        return self.chat_history[-10:]  # Últimas 10 mensagens
    
    def _get_system_commands_info(self) -> str:
        """Retorna informações dos comandos de sistema"""
        return """
🔧 Comandos de Sistema Disponíveis:
• Energia: desligar, reiniciar, suspender
• Atualizações: verificar atualizações
• Aplicativos: abrir [nome do app]
• Voz: 🎤 Botão de ativação
• System Monitor: 🖥️ Logs em tempo real
"""
    
    def _on_closing(self):
        """Evento de fechamento da janela"""
        if self.is_processing:
            if not messagebox.askyesno("Confirmação", "J.A.R.V.I.S. está processando. Deseja fechar mesmo assim?"):
                return
        
        self.logger.info("Interface encerrada pelo usuário", "GUI")
        self.root.destroy()
    
    def run(self):
        """Inicia a interface"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.info("Programa interrompido", "GUI")
            self.root.destroy()
