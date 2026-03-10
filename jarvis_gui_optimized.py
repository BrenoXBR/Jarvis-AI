#!/usr/bin/env python3
"""
J.A.R.V.I.S. - Versão Otimizada e Refatorada
Interface Integrada com arquitetura melhorada e performance otimizada
"""

import os
import sys
import re
import time
import json
import sqlite3
import threading
import queue
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from contextlib import contextmanager
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Imports essenciais com tratamento robusto
try:
    import customtkinter as ctk
    import pyautogui
    import google.generativeai as genai
    from dotenv import load_dotenv
    import speech_recognition as sr
    import pyttsx3
    from PIL import Image
except ImportError as e:
    print(f"❌ Erro crítico de importação: {e}")
    sys.exit(1)

# Import do módulo de controle de sistema
try:
    from jarvis_system_controller import SystemController
    SYSTEM_CONTROL_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Módulo de controle de sistema não disponível: {e}")
    SYSTEM_CONTROL_AVAILABLE = False

# Configuração global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Constantes centralizadas
@dataclass
class JarvisConfig:
    """Configurações centralizadas do JARVIS"""
    BASE_DIR: Path = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
    ENV_FILE: Path = BASE_DIR / '.env'
    DB_FILE: Path = BASE_DIR / 'jarvis_memory.db'
    LOG_FILE: Path = BASE_DIR / 'jarvis_log.txt'
    ERROR_FILE: Path = BASE_DIR / 'ERRO_CRITICO.txt'
    
    # UI Config
    WINDOW_SIZE: str = "900x700"
    MIN_SIZE: str = "700x500"
    CHAT_HISTORY_LIMIT: int = 100
    MEMORY_LIMIT: int = 50
    
    # API Config
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7
    
    # Cores Stark Industries
    COLORS: Dict[str, str] = {
        "background": "#0B0E14",
        "border": "#00D2FF",
        "component_bg": "#002B36",
        "ia_text": "#80E8FF",
        "button_normal": "#00D2FF",
        "button_hover": "#0095B3",
        "button_text": "#000000",
        "user_name": "#e5e5e5",
        "system_name": "#ffaa00",
        "jarvis_name": "#00D2FF"
    }

class PathManager:
    """Gerenciador centralizado de caminhos"""
    
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.base_dir = config.BASE_DIR
    
    def get_relative_path(self, filename: str) -> Path:
        """Retorna caminho relativo ao diretório base"""
        return self.base_dir / filename
    
    def ensure_dir(self, path: Path) -> Path:
        """Garante que o diretório existe"""
        path.mkdir(parents=True, exist_ok=True)
        return path

class Logger:
    """Sistema de logging otimizado"""
    
    def __init__(self, config: JarvisConfig):
        self.config = config
        self._init_log()
    
    def _init_log(self) -> None:
        """Inicializa arquivo de log"""
        try:
            with open(self.config.LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"🤖 J.A.R.V.I.S. - INÍCIO DE SESSÃO\n")
                f.write(f"{'='*60}\n")
                f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Sistema: {sys.platform}\n")
                f.write(f"Python: {sys.version}\n")
                f.write(f"Diretório: {self.config.BASE_DIR}\n")
                f.write(f"{'='*60}\n\n")
        except Exception as e:
            print(f"❌ Erro ao inicializar log: {e}")
    
    def log(self, level: str, message: str, module: str = "GERAL") -> None:
        """Registra mensagem de log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] [{module}] {message}\n"
        
        try:
            with open(self.config.LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"❌ Erro ao registrar log: {e}")
    
    def info(self, message: str, module: str = "GERAL") -> None:
        self.log("INFO", message, module)
    
    def error(self, error: Exception, context: str = "Desconhecido", module: str = "GERAL") -> None:
        """Registra erro completo"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Log normal
        self.log("ERROR", f"{context}: {type(error).__name__}: {str(error)}", module)
        
        # Arquivo de erro crítico
        try:
            with open(self.config.ERROR_FILE, 'w', encoding='utf-8') as f:
                f.write("🤖 J.A.R.V.I.S. - ERRO CRÍTICO\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Data/Hora: {timestamp}\n")
                f.write(f"Módulo: {module}\n")
                f.write(f"Contexto: {context}\n\n")
                f.write("ERRO:\n")
                f.write(f"Tipo: {type(error).__name__}\n")
                f.write(f"Mensagem: {str(error)}\n\n")
                f.write("TRACEBACK:\n")
                import traceback
                f.write(traceback.format_exc())
        except Exception as e:
            print(f"❌ Erro ao salvar erro crítico: {e}")

class EnvironmentManager:
    """Gerenciador de variáveis de ambiente"""
    
    def __init__(self, config: JarvisConfig, logger: Logger):
        self.config = config
        self.logger = logger
        self._load_env()
    
    def _load_env(self) -> None:
        """Carrega variáveis de ambiente"""
        if self.config.ENV_FILE.exists():
            try:
                load_dotenv(self.config.ENV_FILE, encoding='utf-8', override=True)
                self.logger.info(f".env carregado: {self.config.ENV_FILE}", "AMBIENTE")
            except UnicodeDecodeError:
                try:
                    load_dotenv(self.config.ENV_FILE, encoding='latin-1', override=True)
                    self.logger.warning(f".env carregado com latin-1: {self.config.ENV_FILE}", "AMBIENTE")
                except Exception as e:
                    self.logger.error(e, f"Falha ao carregar .env: {self.config.ENV_FILE}", "AMBIENTE")
                    load_dotenv(override=True)
        else:
            self.logger.warning(f".env não encontrado: {self.config.ENV_FILE}", "AMBIENTE")
            load_dotenv(override=True)
    
    def get_api_key(self) -> Optional[str]:
        """Retorna API key mascarada para debug"""
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key and len(api_key) > 10:
            masked_key = f"{api_key[:8]}...{api_key[-4:]}"
            self.logger.info(f"API Key detectada: {masked_key}", "AMBIENTE")
        return api_key

class MemoryManager:
    """Sistema de memória otimizado"""
    
    def __init__(self, config: JarvisConfig, logger: Logger):
        self.config = config
        self.logger = logger
        self._init_database()
    
    def _init_database(self) -> None:
        """Inicializa banco de dados"""
        try:
            with sqlite3.connect(self.config.DB_FILE) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fact TEXT NOT NULL,
                        category TEXT NOT NULL,
                        data TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
            self.logger.info("Banco de dados inicializado", "MEMÓRIA")
        except Exception as e:
            self.logger.error(e, "Falha ao inicializar banco", "MEMÓRIA")
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexões"""
        conn = sqlite3.connect(self.config.DB_FILE)
        try:
            yield conn
        finally:
            conn.close()
    
    def add_memory(self, fact: str, category: str = "general", data: str = "") -> None:
        """Adiciona memória de forma assíncrona"""
        def add_async():
            try:
                with self.get_connection() as conn:
                    conn.execute(
                        "INSERT INTO memory (fact, category, data) VALUES (?, ?, ?)",
                        (fact, category, data)
                    )
                    conn.commit()
            except Exception as e:
                self.logger.error(e, "Falha ao adicionar memória", "MEMÓRIA")
        
        threading.Thread(target=add_async, daemon=True).start()
    
    def get_recent_memories(self, limit: int = 5) -> List[tuple]:
        """Recupera memórias recentes"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT fact, category, timestamp FROM memory ORDER BY timestamp DESC LIMIT ?",
                    (limit,)
                )
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(e, "Falha ao recuperar memórias", "MEMÓRIA")
            return []

class VisionManager:
    """Sistema de visão computacional otimizado"""
    
    def __init__(self, config: JarvisConfig, logger: Logger, env_manager: EnvironmentManager):
        self.config = config
        self.logger = logger
        self.api_key = env_manager.get_api_key()
        self.vision_enabled = False
        
        if self.api_key and self.api_key != 'sua_chave_api_aqui':
            try:
                genai.configure(api_key=self.api_key)
                self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
                self.vision_enabled = True
                self.logger.info("Visão computacional inicializada", "VISÃO")
            except Exception as e:
                self.logger.error(e, "Falha ao inicializar visão", "VISÃO")
        else:
            self.logger.warning("API key não configurada", "VISÃO")
    
    def capture_and_analyze(self) -> str:
        """Captura e analisa tela de forma otimizada"""
        if not self.vision_enabled:
            return "❌ Visão computacional não disponível"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_file = self.config.get_relative_path(f"temp_screen_{timestamp}.png")
        
        try:
            # Captura
            pyautogui.screenshot(str(temp_file))
            
            # Análise
            with Image.open(temp_file) as img:
                prompt = """Analise esta tela e forneça:
1. Descrição do que está sendo exibido
2. Elementos técnicos relevantes
3. Contexto do ambiente
4. Ações ou problemas identificados

Seja técnico e direto."""
                
                response = self.vision_model.generate_content([prompt, img])
                return response.text
                
        except Exception as e:
            self.logger.error(e, "Falha na análise de tela", "VISÃO")
            return f"❌ Erro na análise: {e}"
        finally:
            if temp_file.exists():
                temp_file.unlink()

class VoiceManager:
    """Sistema de voz otimizado"""
    
    def __init__(self, config: JarvisConfig, logger: Logger):
        self.config = config
        self.logger = logger
        self.voice_enabled = False
        
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.engine = pyttsx3.init()
            self.voice_enabled = True
            self.logger.info("Sistema de voz inicializado", "VOZ")
        except Exception as e:
            self.logger.error(e, "Falha ao inicializar voz", "VOZ")
    
    def listen_for_speech(self, callback) -> None:
        """Escuta comandos de voz de forma assíncrona"""
        if not self.voice_enabled:
            callback("❌ Sistema de voz não disponível")
            return
        
        def listen_async():
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                try:
                    text = self.recognizer.recognize_google(audio, language='pt-BR')
                    callback(text)
                except sr.UnknownValueError:
                    callback("❌ Não consegui entender")
                except sr.RequestError as e:
                    callback(f"❌ Erro no reconhecimento: {e}")
                    
            except sr.WaitTimeoutError:
                callback("⏰ Tempo esgotado")
            except Exception as e:
                self.logger.error(e, "Erro na escuta", "VOZ")
                callback(f"❌ Erro na escuta: {e}")
        
        threading.Thread(target=listen_async, daemon=True).start()

class ChatManager:
    """Gerenciador de chat otimizado"""
    
    def __init__(self, config: JarvisConfig, logger: Logger):
        self.config = config
        self.logger = logger
        self.chat_history: List[Dict[str, Any]] = []
        self.max_history = config.CHAT_HISTORY_LIMIT
    
    def add_message(self, sender: str, message: str, msg_type: str) -> Dict[str, Any]:
        """Adiciona mensagem ao histórico"""
        msg_data = {
            "sender": sender,
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "type": msg_type
        }
        
        self.chat_history.append(msg_data)
        
        # Limita histórico
        if len(self.chat_history) > self.max_history:
            self.chat_history = self.chat_history[-self.max_history:]
        
        return msg_data
    
    def get_conversation_context(self, limit: int = 10) -> str:
        """Retorna contexto da conversa"""
        recent = self.chat_history[-limit:]
        context_lines = []
        
        for msg in recent:
            if msg["type"] == "user":
                context_lines.append(f"VOCÊ: {msg['message']}")
            elif msg["type"] == "jarvis":
                context_lines.append(f"JARVIS: {msg['message']}")
            elif msg["type"] == "system":
                context_lines.append(f"SISTEMA: {msg['message']}")
        
        return "\n".join(context_lines)

class JarvisGUI:
    """Interface Principal Otimizada"""
    
    def __init__(self):
        self.config = JarvisConfig()
        self.logger = Logger(self.config)
        self.path_manager = PathManager(self.config)
        self.env_manager = EnvironmentManager(self.config, self.logger)
        self.memory_manager = MemoryManager(self.config, self.logger)
        self.vision_manager = VisionManager(self.config, self.logger, self.env_manager)
        self.voice_manager = VoiceManager(self.config, self.logger)
        self.chat_manager = ChatManager(self.config, self.logger)
        
        # Inicializa controlador de sistema
        if SYSTEM_CONTROL_AVAILABLE:
            self.system_controller = SystemController(self.logger)
            self.logger.info("Controlador de sistema inicializado", "SISTEMA")
        else:
            self.system_controller = None
            self.logger.warning("Controlador de sistema não disponível", "SISTEMA")
        
        # Estado
        self.is_listening = False
        self.is_processing = False
        self.message_queue = queue.Queue()
        
        self._setup_ui()
        self._load_initial_data()
    
    def _setup_ui(self) -> None:
        """Configura interface otimizada"""
        self.root = ctk.CTk()
        self.root.title("🤖 J.A.R.V.I.S. - Stark Industries")
        self.root.geometry(self.config.WINDOW_SIZE)
        self.root.minsize(*[int(x) for x in self.config.MIN_SIZE.split('x')])
        self.root.configure(fg_color=self.config.COLORS["background"])
        
        self._create_main_layout()
        self._bind_events()
    
    def _create_main_layout(self) -> None:
        """Cria layout principal"""
        # Container principal
        self.main_frame = ctk.CTkFrame(
            self.root, 
            corner_radius=10,
            border_color=self.config.COLORS["border"],
            fg_color=self.config.COLORS["component_bg"]
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self._create_header()
        
        # Chat area
        self._create_chat_area()
        
        # Input area
        self._create_input_area()
    
    def _create_header(self) -> None:
        """Cria cabeçalho"""
        header = ctk.CTkFrame(
            self.main_frame,
            height=60,
            border_color=self.config.COLORS["border"],
            fg_color=self.config.COLORS["component_bg"]
        )
        header.pack(fill="x", padx=10, pady=(10, 20))
        header.pack_propagate(False)
        
        # Título
        title = ctk.CTkLabel(
            header,
            text="🤖 J.A.R.V.I.S.",
            font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
            text_color=self.config.COLORS["ia_text"]
        )
        title.pack(side="left", padx=20, pady=15)
        
        # Status
        self.status_label = ctk.CTkLabel(
            header,
            text="🟢 Online",
            font=ctk.CTkFont(family="Consolas", size=14),
            text_color=self.config.COLORS["ia_text"]
        )
        self.status_label.pack(side="right", padx=20, pady=15)
    
    def _create_chat_area(self) -> None:
        """Cria área de chat"""
        chat_frame = ctk.CTkFrame(
            self.main_frame,
            border_color=self.config.COLORS["border"],
            fg_color=self.config.COLORS["component_bg"]
        )
        chat_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=self.config.COLORS["background"],
            border_color=self.config.COLORS["border"],
            text_color="#ffffff",
            wrap="word",
            state="disabled"
        )
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=20)
    
    def _create_input_area(self) -> None:
        """Cria área de input"""
        self.input_frame = ctk.CTkFrame(
            self.main_frame,
            height=80,
            border_color=self.config.COLORS["border"],
            fg_color=self.config.COLORS["component_bg"]
        )
        self.input_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        self.input_frame.pack_propagate(False)
        
        # Campo de texto
        self.text_input = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Digite seu comando ou fale com o Jarvis...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=40,
            border_color=self.config.COLORS["border"],
            fg_color=self.config.COLORS["component_bg"],
            text_color="#ffffff"
        )
        self.text_input.pack(side="left", fill="both", expand=True, padx=(10, 10), pady=20)
        
        # Container de botões
        button_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        button_container.pack(side="right", padx=(0, 10), pady=20)
        
        # Botões
        self.vision_button = ctk.CTkButton(
            button_container,
            text="👁️",
            width=50,
            height=40,
            command=self._handle_vision
        )
        self.vision_button.pack(side="left", padx=(0, 5))
        
        # Botão de emergência - Protocolo Silêncio
        self.emergency_button = ctk.CTkButton(
            button_container,
            text="🚨",
            width=50,
            height=40,
            fg_color="#FF4444",  # Vermelho para emergência
            hover_color="#CC0000",
            command=self._emergency_silence
        )
        self.emergency_button.pack(side="left", padx=(0, 5))
        
        self.listen_button = ctk.CTkButton(
            button_container,
            text="🎤 Ouvir",
            width=100,
            height=40,
            command=self._toggle_listening
        )
        self.listen_button.pack(side="left", padx=5)
        
        self.send_button = ctk.CTkButton(
            button_container,
            text="📤 Enviar",
            width=80,
            height=40,
            command=self._send_message
        )
        self.send_button.pack(side="left", padx=5)
    
    def _bind_events(self) -> None:
        """Configura eventos"""
        self.text_input.bind("<Return>", lambda e: self._send_message())
    
    def _load_initial_data(self) -> None:
        """Carrega dados iniciais"""
        memories = self.memory_manager.get_recent_memories(3)
        if memories:
            self._add_message("Sistema", f"📚 Carregadas {len(memories)} memórias recentes", "system")
        
        # Mensagem inicial aprimorada
        initial_message = "👋 Olá! Sou o J.A.R.V.I.S. com controle de sistema integrado!\n\n"
        initial_message += "🤖 **Minhas capacidades:**\n"
        initial_message += "• � **Protocolo Silêncio** - Emergência instantânea\n"
        initial_message += "• �� Abrir aplicativos (Chrome, VS Code, Spotify, etc.)\n"
        initial_message += "• 🌐 Acessar links rápidos (YouTube, GitHub, etc.)\n"
        initial_message += "• 🔊 Controlar volume e brilho\n"
        initial_message += "• 👁️ Análise de tela com visão computacional\n"
        initial_message += "• 🎤 Reconhecimento de voz\n"
        initial_message += "• 🧠 Memória persistente\n\n"
        initial_message += "💡 **Diga:** 'Jarvis, protocolo silêncio' para emergências!"
        
        self._add_message("Jarvis", initial_message, "jarvis")
    
    def _add_message(self, sender: str, message: str, msg_type: str) -> None:
        """Adiciona mensagem ao chat"""
        # Adiciona ao gerenciador
        msg_data = self.chat_manager.add_message(sender, message, msg_type)
        
        # Atualiza UI
        self.chat_display.configure(state="normal")
        
        if msg_type == "jarvis":
            self.chat_display.insert("end", "JARVIS\n", "jarvis_name")
            self.chat_display.tag_config("jarvis_name", foreground=self.config.COLORS["jarvis_name"])
            self.chat_display.insert("end", f"{message}\n\n", "jarvis_message")
            self.chat_display.tag_config("jarvis_message", foreground="#ffffff")
        elif msg_type == "user":
            self.chat_display.insert("end", "VOCÊ\n", "user_name")
            self.chat_display.tag_config("user_name", foreground=self.config.COLORS["user_name"])
            self.chat_display.insert("end", f"{message}\n\n", "user_message")
            self.chat_display.tag_config("user_message", foreground="#ffffff")
        elif msg_type == "system":
            self.chat_display.insert("end", "SISTEMA\n", "system_name")
            self.chat_display.tag_config("system_name", foreground=self.config.COLORS["system_name"])
            self.chat_display.insert("end", f"{message}\n\n", "system_message")
            self.chat_display.tag_config("system_message", foreground="#ffffff")
        
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
    
    def _send_message(self) -> None:
        """Envia mensagem"""
        message = self.text_input.get().strip()
        if not message:
            return
        
        self.text_input.delete(0, "end")
        self._add_message("Você", message, "user")
        self._process_message(message)
    
    def _process_message(self, message: str) -> None:
        """Processa mensagem com Gemini e controle de sistema"""
        # Primeiro, verifica se é um comando de sistema
        if self.system_controller:
            command_intent = self.system_controller.detect_command_intent(message)
            if command_intent:
                command_type, command_data = command_intent
                result = self.system_controller.execute_command(command_type, command_data)
                self._add_message("Jarvis", result, "jarvis")
                
                # Salva na memória como comando executado
                self.memory_manager.add_memory(f"Comando sistema: {message} → {result}", "system_command")
                return
        
        # Se não for comando de sistema, processa com Gemini
        if not self.vision_manager.api_key or self.vision_manager.api_key == 'sua_chave_api_aqui':
            self._add_message("Jarvis", "❌ Configure sua API key no arquivo .env", "jarvis")
            return
        
        self.is_processing = True
        self.status_label.configure(text="🟡 Processando...")
        
        def process_async():
            try:
                # Contexto
                context = self.chat_manager.get_conversation_context()
                memories = self.memory_manager.get_recent_memories(3)
                memory_context = "\n".join([f"- {mem[0]}" for mem in memories]) if memories else ""
                
                # Adiciona informações de comandos disponíveis ao contexto
                system_commands_info = ""
                if self.system_controller:
                    system_commands_info = "\n\nComandos de sistema disponíveis:\n" + \
                                        self.system_controller.list_available_commands()
                
                # Detecção de detalhamento ou pedido de comandos
                needs_detail = any(keyword in message.lower() for keyword in [
                    'mais detalhes', 'continue', 'explique melhor', 'pode detalhar'
                ])
                
                asks_for_commands = any(keyword in message.lower() for keyword in [
                    'comandos', 'o que você pode fazer', 'ajuda', 'help', 'funcionalidades'
                ])
                
                # Prompt otimizado
                if asks_for_commands:
                    prompt = f"""Você é J.A.R.V.I.S. com controle de sistema integrado.

Contexto da conversa:
{context}

Memórias:
{memory_context}
{system_commands_info}

Comando: {message}

Responda listando suas capacidades incluindo controle de aplicativos, volume, brilho e links rápidos. Seja detalhado e técnico."""
                elif needs_detail:
                    prompt = f"""Você é J.A.R.V.I.S. com controle de sistema integrado. Forneça análise detalhada.

Contexto da conversa:
{context}

Memórias:
{memory_context}
{system_commands_info}

Comando: {message}

Responda com detalhamento técnico completo."""
                else:
                    prompt = f"""Você é J.A.R.V.I.S. com controle de sistema integrado. Seja técnico e direto.

Contexto:
{context}

Memórias:
{memory_context}
{system_commands_info}

Comando: {message}

Responda de forma concisa e técnica."""
                
                # Chamada API
                model = genai.GenerativeModel(
                    'gemini-2.5-flash',
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=self.config.MAX_TOKENS,
                        temperature=self.config.TEMPERATURE,
                        candidate_count=1
                    )
                )
                
                response = model.generate_content(prompt)
                cleaned_response = self._clean_response(response.text)
                
                # Exibe resposta
                self.root.after(0, lambda: self._typewriter_effect(cleaned_response))
                
                # Salva memória
                self.memory_manager.add_memory(f"Usuário: {message}", "conversation")
                self.memory_manager.add_memory(f"Jarvis: {cleaned_response[:100]}...", "conversation")
                
            except Exception as e:
                self.logger.error(e, "Erro ao processar mensagem", "GEMINI")
                self.root.after(0, lambda: self._add_message("Jarvis", f"❌ Erro: {e}", "jarvis"))
            finally:
                self.root.after(0, self._reset_processing_state)
        
        threading.Thread(target=process_async, daemon=True).start()
    
    def _clean_response(self, text: str) -> str:
        """Limpa resposta da API"""
        if not text:
            return ""
        
        # Remove markdown
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'`(.*?)`', r'\1', text)
        text = re.sub(r'^[-*]{3,}\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _typewriter_effect(self, message: str) -> None:
        """Efeito typewriter otimizado"""
        if not message:
            return
        
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", "JARVIS\n", "jarvis_name")
        self.chat_display.tag_config("jarvis_name", foreground=self.config.COLORS["jarvis_name"])
        
        def type_chars():
            try:
                for i, char in enumerate(message):
                    if not self.is_processing:
                        # Se interrompido, adiciona resto
                        remaining = message[i:]
                        self.chat_display.insert("end", remaining, "jarvis_message")
                        break
                    
                    self.chat_display.insert("end", char, "jarvis_message")
                    self.chat_display.tag_config("jarvis_message", foreground="#ffffff")
                    self.chat_display.see("end")
                    time.sleep(0.01)
                
                self.chat_display.insert("end", "\n\n", "jarvis_message")
                self.chat_display.see("end")
            finally:
                self.chat_display.configure(state="disabled")
        
        threading.Thread(target=type_chars, daemon=True).start()
    
    def _reset_processing_state(self) -> None:
        """Reseta estado de processamento"""
        self.is_processing = False
        self.status_label.configure(text="🟢 Online")
    
    def _toggle_listening(self) -> None:
        """Alterna modo de escuta"""
        if not self.is_listening:
            self._start_listening()
        else:
            self._stop_listening()
    
    def _start_listening(self) -> None:
        """Inicia escuta"""
        self.is_listening = True
        self.listen_button.configure(text="⏹️ Parar")
        self.status_label.configure(text="🎤 Ouvindo...")
        
        def voice_callback(text):
            self.root.after(0, lambda: self._handle_voice_result(text))
        
        self.voice_manager.listen_for_speech(voice_callback)
    
    def _stop_listening(self) -> None:
        """Para escuta"""
        self.is_listening = False
        self.listen_button.configure(text="🎤 Ouvir")
        self.status_label.configure(text="🟢 Online")
    
    def _handle_voice_result(self, result: str) -> None:
        """Processa resultado da voz"""
        self._stop_listening()
        
        if result.startswith("❌"):
            self._add_message("Sistema", result, "system")
        else:
            self._add_message("Você", result, "user")
            self._process_message(result)
    
    def _handle_vision(self) -> None:
        """Processa comando de visão"""
        if not self.vision_manager.vision_enabled:
            self._add_message("Sistema", "❌ Visão não disponível", "system")
            return
        
        self._add_message("Sistema", "📸 Capturando e analisando...", "system")
        
        def analyze_async():
            try:
                result = self.vision_manager.capture_and_analyze()
                self.root.after(0, lambda: self._add_message("Jarvis", result, "jarvis"))
            except Exception as e:
                self.logger.error(e, "Erro na análise", "VISÃO")
                self.root.after(0, lambda: self._add_message("Sistema", f"❌ Erro: {e}", "system"))
        
        threading.Thread(target=analyze_async, daemon=True).start()
    
    def _emergency_silence(self) -> None:
        """Executa Protocolo Silêncio via botão de emergência"""
        if not self.system_controller:
            self._add_message("Sistema", "❌ Controlador de sistema não disponível", "system")
            return
        
        # Feedback visual imediato
        self._add_message("Sistema", "🚨 **PROTOCOLO SILÊNCIO ATIVADO!**", "system")
        self.status_label.configure(text="🚨 EMERGÊNCIA", text_color="#FF4444")
        
        def execute_emergency():
            try:
                result = self.system_controller.execute_command("emergency_silence", {})
                self.root.after(0, lambda: self._add_message("Jarvis", result, "jarvis"))
            except Exception as e:
                self.logger.error(e, "Erro no Protocolo Silêncio", "EMERGÊNCIA")
                self.root.after(0, lambda: self._add_message("Sistema", f"❌ Erro: {e}", "system"))
            finally:
                # Reseta status após 3 segundos
                self.root.after(3000, lambda: self.status_label.configure(
                    text="🟢 Online", 
                    text_color=self.config.COLORS["ia_text"]
                ))
        
        # Executa imediatamente em thread separada
        threading.Thread(target=execute_emergency, daemon=True).start()
    
    def run(self) -> None:
        """Inicia aplicação"""
        try:
            self.logger.info("Iniciando J.A.R.V.I.S. otimizado", "SISTEMA")
            self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.info("Programa interrompido", "SISTEMA")
        except Exception as e:
            self.logger.error(e, "Erro crítico", "SISTEMA")
        finally:
            self._shutdown()
    
    def _shutdown(self) -> None:
        """Encerra aplicação"""
        try:
            self.is_processing = False
            self.is_listening = False
            if hasattr(self, 'root'):
                self.root.quit()
                self.root.destroy()
        except Exception as e:
            self.logger.error(e, "Erro no encerramento", "SISTEMA")
        finally:
            sys.exit(0)

def main():
    """Função principal otimizada"""
    try:
        app = JarvisGUI()
        app.run()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
