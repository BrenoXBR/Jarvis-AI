#!/usr/bin/env python3
"""
Interface Integrada do Jarvis com todos os módulos
Dark Mode com integração completa: Memória, Gemini, Voz e Visão
"""

# Importações essenciais que devem estar sempre disponíveis
import re
import sys
import os
from datetime import datetime

# BLOCO DE CAPTURA GLOBAL DE ERROS DE IMPORTAÇÃO
try:
    import customtkinter as ctk
    print("✅ CustomTkinter importado com sucesso")
except ImportError as e:
    print(f"❌ Erro crítico ao importar CustomTkinter: {e}")
    # Salva erro em arquivo
    import sys
    import os
    from datetime import datetime
    
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    error_file = os.path.join(base_path, 'ERRO_CRITICO.txt')
    
    with open(error_file, 'w', encoding='utf-8') as f:
        f.write("🤖 J.A.R.V.I.S. - ERRO CRÍTICO DE IMPORTAÇÃO\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Sistema: {sys.platform}\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Executável: {getattr(sys, 'frozen', False)}\n")
        f.write(f"Diretório: {base_path}\n\n")
        f.write("ERRO:\n")
        f.write(f"Tipo: {type(e).__name__}\n")
        f.write(f"Mensagem: {str(e)}\n\n")
        f.write("SOLUÇÃO:\n")
        f.write("1. Verifique se o CustomTkinter foi instalado corretamente\n")
        f.write("2. Tente reinstalar: pip install customtkinter\n")
        f.write("3. Verifique se o PyInstaller incluiu a biblioteca\n")
    
    print("Erro crítico detectado. Verifique ERRO_CRITICO.txt. O programa será encerrado.")
    sys.exit(1)

try:
    import threading
    import queue
    import time
    import sqlite3
    import json
    import pyautogui
    import tempfile
    from PIL import Image
    import google.generativeai as genai
    from dotenv import load_dotenv
    import speech_recognition as sr
    import pyttsx3
    print("✅ Todas as bibliotecas importadas com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar bibliotecas: {e}")
    print("Erro de importação. O programa será encerrado.")
    sys.exit(1)

# Import do módulo de controle de sistema
try:
    from jarvis_system_controller import SystemController
    SYSTEM_CONTROL_AVAILABLE = True
    print("✅ Módulo de controle de sistema importado")
except ImportError as e:
    print(f"⚠️ Módulo de controle de sistema não disponível: {e}")
    SYSTEM_CONTROL_AVAILABLE = False

# SISTEMA DE LOG DE ERRO GLOBAL
class JarvisLogger:
    """Sistema de log para o J.A.R.V.I.S."""
    
    def __init__(self):
        # Determina o diretório base
        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.log_file = os.path.join(self.base_path, 'jarvis_log.txt')
        self.error_file = os.path.join(self.base_path, 'ERRO_CRITICO.txt')
        
        # Inicializa o arquivo de log
        self._init_log_file()
    
    def _init_log_file(self):
        """Inicializa o arquivo de log"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"🤖 J.A.R.V.I.S. - INÍCIO DE SESSÃO\n")
                f.write(f"{'='*60}\n")
                f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Sistema: {sys.platform}\n")
                f.write(f"Python: {sys.version}\n")
                f.write(f"Executável: {getattr(sys, 'frozen', False)}\n")
                f.write(f"Diretório: {self.base_path}\n")
                f.write(f"{'='*60}\n\n")
        except Exception as e:
            print(f"❌ Erro ao criar log: {e}")
    
    def log_info(self, message, module="GERAL"):
        """Registra mensagem informativa"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] [INFO] [{module}] {message}\n")
        except Exception as e:
            print(f"❌ Erro ao registrar log: {e}")
    
    def log_error(self, error, context="Desconhecido", module="GERAL"):
        """Registra erro completo"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Registra no log normal
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] [ERROR] [{module}] {context}\n")
                f.write(f"  Tipo: {type(error).__name__}\n")
                f.write(f"  Mensagem: {str(error)}\n")
                import traceback
                f.write(f"  Traceback: {traceback.format_exc()}\n")
                f.write(f"{'-'*60}\n\n")
            
            # Salva erro crítico separado
            with open(self.error_file, 'w', encoding='utf-8') as f:
                f.write("🤖 J.A.R.V.I.S. - ERRO CRÍTICO\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Data/Hora: {timestamp}\n")
                f.write(f"Sistema: {sys.platform}\n")
                f.write(f"Python: {sys.version}\n")
                f.write(f"Executável: {getattr(sys, 'frozen', False)}\n")
                f.write(f"Diretório: {self.base_path}\n")
                f.write(f"Módulo: {module}\n")
                f.write(f"Contexto: {context}\n\n")
                f.write("ERRO:\n")
                f.write(f"Tipo: {type(error).__name__}\n")
                f.write(f"Mensagem: {str(error)}\n\n")
                f.write("TRACEBACK COMPLETO:\n")
                f.write(traceback.format_exc())
                f.write("\n\n")
                f.write("INFORMAÇÕES ADICIONAIS:\n")
                f.write(f"Arquivos no diretório:\n")
                try:
                    for item in os.listdir(self.base_path):
                        f.write(f"  - {item}\n")
                except Exception as list_error:
                    f.write(f"  Erro ao listar diretório: {list_error}\n")
                f.write("\n")
                f.write("SUGESTÕES:\n")
                f.write("1. Verifique sua conexão com internet\n")
                f.write("2. Confirme se a API key está correta\n")
                f.write("3. Reinicie o aplicativo\n")
                f.write("4. Verifique se o Windows está atualizado\n")
                f.write("5. Feche outros aplicativos pesados\n")
            
            print(f"❌ Erro crítico salvo em: {self.error_file}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar erro crítico: {e}")
    
    def log_warning(self, message, module="GERAL"):
        """Registra aviso"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] [WARNING] [{module}] {message}\n")
        except Exception as e:
            print(f"❌ Erro ao registrar aviso: {e}")
    
    def log_success(self, message, module="GERAL"):
        """Registra sucesso"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] [SUCCESS] [{module}] {message}\n")
        except Exception as e:
            print(f"❌ Erro ao registrar sucesso: {e}")

# Inicializa o logger global
logger = JarvisLogger()
logger.log_info("Sistema de log inicializado", "SISTEMA")

# Configuração do tema Stark Industries
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Configuração de cores personalizadas Stark Industries
STARK_COLORS = {
    "background": "#0B0E14",
    "border": "#00D2FF", 
    "component_bg": "#002B36",
    "ia_text": "#80E8FF",
    "button_normal": "#00D2FF",
    "button_hover": "#0095B3",
    "button_text": "#000000"
}

class JarvisMemory:
    """Sistema de memória persistente simplificado"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            # Caminho relativo que funciona tanto em dev quanto no executável
            if getattr(sys, 'frozen', False):
                # Estamos rodando como executável
                base_path = os.path.dirname(sys.executable)
            else:
                # Estamos rodando como script Python
                base_path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_path, 'jarvis_memory.db')
        self.db_path = db_path
        
        # Log de inicialização
        logger.log_info(f"Inicializando memória em: {db_path}", "MEMÓRIA")
        
        self.init_database()
        
    def init_database(self):
        """Inicializa o banco de dados SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fact TEXT NOT NULL,
                    category TEXT NOT NULL,
                    data TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.log_success("Banco de dados inicializado com sucesso", "MEMÓRIA")
        except Exception as e:
            logger.log_error(e, "Falha ao inicializar banco de dados", "MEMÓRIA")
    
    def add_memory(self, fact, category="general", data=""):
        """Adiciona uma memória"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO memory (fact, category, data) VALUES (?, ?, ?)",
                (fact, category, data)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao adicionar memória: {e}")
    
    def get_recent_memories(self, limit=5):
        """Recupera memórias recentes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT fact, category, created_at FROM memory ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
            memories = cursor.fetchall()
            conn.close()
            return memories
        except Exception as e:
            print(f"Erro ao recuperar memórias: {e}")
            return []

class JarvisVision:
    """Sistema de visão computacional simplificado"""
    
    def __init__(self, api_key=None):
        # Determina o diretório base (executável ou script)
        if getattr(sys, 'frozen', False):
            # Estamos rodando como executável PyInstaller
            base_dir = os.path.dirname(sys.executable)
            logger.log_info(f"Executável detectado, diretório base: {base_dir}", "VISÃO")
        else:
            # Estamos rodando como script Python
            base_dir = os.path.dirname(os.path.abspath(__file__))
            logger.log_info(f"Script detectado, diretório base: {base_dir}", "VISÃO")
        
        # Caminho absoluto para o .env
        env_path = os.path.join(base_dir, '.env')
        logger.log_info(f"Procurando .env em: {env_path}", "VISÃO")
        
        # Carrega o .env se existir, forçando encoding UTF-8
        if os.path.exists(env_path):
            try:
                # Força UTF-8 e override=True para garantir que as variáveis sejam carregadas
                load_dotenv(env_path, encoding='utf-8', override=True)
                logger.log_success(f"Arquivo .env carregado com UTF-8: {env_path}", "VISÃO")
            except UnicodeDecodeError:
                # Fallback: tenta ler com encoding latin-1
                try:
                    load_dotenv(env_path, encoding='latin-1', override=True)
                    logger.log_warning(f"Arquivo .env carregado com latin-1: {env_path}", "VISÃO")
                except Exception as e:
                    logger.log_error(e, f"Falha ao carregar .env: {env_path}", "VISÃO")
                    # Tenta carregar do diretório atual como último recurso
                    load_dotenv(override=True)
        else:
            logger.log_warning(f"Arquivo .env não encontrado em: {env_path}", "VISÃO")
            # Tenta carregar do diretório atual como fallback
            load_dotenv(override=True)
            
        # Obtém a API key e adiciona debug mascarado
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        # Debug: mostra API key mascarada no log
        if self.api_key:
            if len(self.api_key) > 10:
                masked_key = f"{self.api_key[:8]}...{self.api_key[-4:]}"
            else:
                masked_key = "***"
            logger.log_info(f"API Key detectada (mascarada): {masked_key}", "VISÃO")
        else:
            logger.log_error("API Key não encontrada no ambiente!", "VISÃO")
        
        if self.api_key and self.api_key != 'sua_chave_api_aqui':
            try:
                genai.configure(api_key=self.api_key)
                self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
                self.vision_enabled = True
                logger.log_success("Visão computacional inicializada com Gemini 1.5 Flash", "VISÃO")
            except Exception as e:
                logger.log_error(e, "Falha ao inicializar visão computacional", "VISÃO")
                self.vision_enabled = False
        else:
            logger.log_warning("API key não configurada para visão computacional", "VISÃO")
            self.vision_enabled = False
    
    def capture_and_analyze(self):
        """Captura e analisa a tela"""
        if not self.vision_enabled:
            return "❌ Visão computacional não está disponível. Verifique sua API key."
        
        try:
            # Captura tela com caminho relativo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Define o diretório base para arquivos temporários
            if getattr(sys, 'frozen', False):
                # Estamos rodando como executável
                base_path = os.path.dirname(sys.executable)
            else:
                # Estamos rodando como script Python
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            temp_file = os.path.join(base_path, f"temp_screen_{timestamp}.png")
            pyautogui.screenshot(temp_file)
            
            # Analisa com Gemini 1.5 Flash
            try:
                with Image.open(temp_file) as img:
                    # Prompt otimizado para gemini-1.5-flash
                    prompt = """Você é J.A.R.V.I.S. com visão computacional avançada.

Analise esta tela capturada e forneça:

1. **Descrição Geral**: O que está sendo exibido
2. **Elementos Técnicos**: Se houver código, erros, terminal, IDE
3. **Contexto**: Que aplicativo/ambiente está sendo mostrado
4. **Ações Relevantes**: Se houver algo que precise de atenção

Seja detalhado, técnico e focado no que é útil para um programador. 
Se identificar erros, sugira correções. Se for código, explique o que faz."""

                    response = self.vision_model.generate_content([
                        prompt,
                        img
                    ])
                    result = response.text
                
                # Remove arquivo temporário
                os.remove(temp_file)
                return result
                
            except Exception as e:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                
                # Tratamento específico para erro 404
                if "404" in str(e) or "not found" in str(e).lower():
                    return "❌ Erro 404: Modelo de visão não encontrado. Verifique se o modelo 'gemini-1.5-flash' está disponível em sua região."
                else:
                    return f"❌ Erro na análise: {e}"
                
        except Exception as e:
            return f"❌ Erro ao capturar tela: {e}"

class JarvisGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🤖 J.A.R.V.I.S. - Stark Industries")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # Aplicar paleta Stark Industries
        self.root.configure(fg_color=STARK_COLORS["background"])
        
        # Inicializa módulos
        self.memory = JarvisMemory()
        
        # Carrega API key do ambiente para passar para JarvisVision
        api_key = os.getenv('GEMINI_API_KEY')
        self.vision = JarvisVision(api_key=api_key)
        self.setup_voice()
        
        # Inicializa controlador de sistema
        if SYSTEM_CONTROL_AVAILABLE:
            self.system_controller = SystemController(logger)
            logger.info("Controlador de sistema inicializado", "SISTEMA")
        else:
            self.system_controller = None
            logger.warning("Controlador de sistema não disponível", "SISTEMA")
        
        # Estado da aplicação
        self.is_listening = False
        self.is_processing = False
        self.progress_animation_active = False
        self.current_response = None  # Armazena resposta completa para evitar limpeza
        
        # Fila de mensagens para thread-safe
        self.message_queue = queue.Queue()
        
        # Histórico de conversas
        self.chat_history = []
        
        self.setup_ui()
        self.load_memory_history()
        
    def setup_voice(self):
        """Configura sistema de voz"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.engine = pyttsx3.init()
            self.voice_enabled = True
        except Exception as e:
            print(f"Erro ao configurar voz: {e}")
            self.voice_enabled = False
    
    def setup_ui(self):
        """Monta a interface principal estilo Gemini/ChatGPT"""
        
        # Container principal
        main_frame = ctk.CTkFrame(self.root, corner_radius=10, border_color=STARK_COLORS["border"], fg_color=STARK_COLORS["component_bg"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header com título e status
        header_frame = ctk.CTkFrame(main_frame, height=60, border_color=STARK_COLORS["border"], fg_color=STARK_COLORS["component_bg"])
        header_frame.pack(fill="x", padx=10, pady=(10, 20))
        header_frame.pack_propagate(False)
        
        # Título estilizado
        title_font = ctk.CTkFont(family="Consolas", size=24, weight="bold")
        title_label = ctk.CTkLabel(
            header_frame,
            text="🤖 J.A.R.V.I.S.",
            font=title_font,
            text_color=STARK_COLORS["ia_text"]
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Status indicator
        status_font = ctk.CTkFont(family="Consolas", size=14)
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="🟢 Online",
            font=status_font,
            text_color=STARK_COLORS["ia_text"]
        )
        self.status_label.pack(side="right", padx=20, pady=15)
        
        # Área de chat limpa estilo Gemini/ChatGPT
        chat_frame = ctk.CTkFrame(main_frame, border_color=STARK_COLORS["border"], fg_color=STARK_COLORS["component_bg"])
        chat_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # CTkTextbox para chat com layout clean
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=ctk.CTkFont(family="Segoe UI", size=13),  # Fonte um pouco maior para melhor legibilidade
            fg_color=STARK_COLORS["background"],
            border_color=STARK_COLORS["border"],
            text_color="#ffffff",
            wrap="word",
            state="disabled"  # Desabilitado para edição direta
        )
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame de Comandos (parte inferior)
        self.frame_input = ctk.CTkFrame(
            main_frame, 
            height=80, 
            border_color=STARK_COLORS["border"], 
            fg_color=STARK_COLORS["component_bg"]
        )
        self.frame_input.pack(side="bottom", fill="x", padx=20, pady=20)
        self.frame_input.pack_propagate(False)
        
        # Campo de texto dentro do frame de comandos
        self.text_input = ctk.CTkEntry(
            self.frame_input,
            placeholder_text="Digite seu comando ou fale com o Jarvis...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=40,
            border_color="#00D2FF",
            fg_color=STARK_COLORS["component_bg"],
            text_color="#ffffff"
        )
        self.text_input.pack(side="left", fill="both", expand=True, padx=(10, 10), pady=20)
        
        # Bind para Enter
        self.text_input.bind("<Return>", self.send_message)
        
        # Container de botões dentro do frame de comandos
        button_container = ctk.CTkFrame(self.frame_input, fg_color="transparent")
        button_container.pack(side="right", padx=(0, 10), pady=20)
        
        # Botão de visão
        self.vision_button = ctk.CTkButton(
            button_container,
            text="👁️",
            width=50,
            height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            border_color=STARK_COLORS["border"],
            fg_color=STARK_COLORS["component_bg"],
            hover_color=STARK_COLORS["button_hover"],
            command=self.capture_and_analyze_screen
        )
        self.vision_button.pack(side="left", padx=(0, 5))
        
        # Botão de emergência - Protocolo Silêncio
        if SYSTEM_CONTROL_AVAILABLE:
            self.emergency_button = ctk.CTkButton(
                button_container,
                text="🚨",
                width=50,
                height=40,
                font=ctk.CTkFont(family="Segoe UI", size=12),
                border_color=STARK_COLORS["border"],
                fg_color="#FF4444",  # Vermelho para emergência
                hover_color="#CC0000",
                command=self.emergency_silence
            )
            self.emergency_button.pack(side="left", padx=(0, 5))
        
        # Botão de ouvir
        self.listen_button = ctk.CTkButton(
            button_container,
            text="🎤 Ouvir",
            width=100,
            height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            border_color=STARK_COLORS["border"],
            fg_color=STARK_COLORS["button_normal"],
            hover_color=STARK_COLORS["button_hover"],
            text_color=STARK_COLORS["button_text"],
            command=self.toggle_listening
        )
        self.listen_button.pack(side="left", padx=5)
        
        # Botão de enviar
        self.send_button = ctk.CTkButton(
            button_container,
            text="📤 Enviar",
            width=80,
            height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            border_color=STARK_COLORS["border"],
            fg_color=STARK_COLORS["button_normal"],
            hover_color=STARK_COLORS["button_hover"],
            text_color=STARK_COLORS["button_text"],
            command=self.send_message
        )
        self.send_button.pack(side="left", padx=5)
        
        # Barra de progresso (opcional, não empacotada)
        self.progress_bar = ctk.CTkProgressBar(
            self.frame_input,
            width=200,
            height=4,
            progress_color=STARK_COLORS["button_normal"],
            fg_color=STARK_COLORS["component_bg"],
            border_color=STARK_COLORS["border"]
        )
        # progress_bar não será empacotado para não ocupar espaço
        
        # Histórico de chat
        self.chat_history = []
        
        # Mensagem inicial
        if SYSTEM_CONTROL_AVAILABLE:
            initial_message = "👋 Olá! Sou o J.A.R.V.I.S. com controle de sistema integrado!\n\n"
            initial_message += "🤖 **Minhas capacidades:**\n"
            initial_message += "• 🚨 **Protocolo Silêncio** - Emergência instantânea (botão 🚨)\n"
            initial_message += "• 📱 Abrir aplicativos (Chrome, VS Code, Discord, etc.)\n"
            initial_message += "• 🌐 Acessar links rápidos (YouTube, GitHub, etc.)\n"
            initial_message += "• 🔊 Controlar volume e brilho\n"
            initial_message += "• 👁️ Análise de tela com visão computacional\n"
            initial_message += "• 🎤 Reconhecimento de voz\n"
            initial_message += "• 🧠 Memória persistente\n\n"
            initial_message += "💡 **Diga:** 'Jarvis, protocolo silêncio' para emergências!"
            self.add_message("Jarvis", initial_message, is_jarvis=True)
        else:
            self.add_message("Jarvis", "👋 Olá! Sou o J.A.R.V.I.S. com todos os módulos integrados. Posso ouvir, ver, lembrar e analisar para você!", is_jarvis=True)
        
    def start_progress_animation(self):
        """Inicia animação da barra de progresso"""
        self.progress_animation_active = True
        self.progress_bar.set(0)
        
        def animate():
            progress = 0
            while self.progress_animation_active:
                progress += 0.02
                if progress >= 1.0:
                    progress = 0
                self.progress_bar.set(progress)
                time.sleep(0.05)
        
        threading.Thread(target=animate, daemon=True).start()
    
    def stop_progress_animation(self):
        """Para animação da barra de progresso"""
        self.progress_animation_active = False
        self.progress_bar.set(0)
        
    def load_memory_history(self):
        """Carrega histórico da memória ao iniciar"""
        memories = self.memory.get_recent_memories(3)
        if memories:
            self.add_message("Sistema", f"📚 Carregadas {len(memories)} memórias recentes.", is_system=True)
    
    def toggle_listening(self):
        """Alterna o estado de escuta"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Inicia o modo de escuta"""
        if not self.voice_enabled:
            self.add_message("Sistema", "❌ Sistema de voz não disponível.", is_system=True)
            return
            
        self.is_listening = True
        self.listen_button.configure(
            text="⏹️ Parar",
            fg_color=STARK_COLORS["component_bg"],
            hover_color=STARK_COLORS["button_hover"],
            text_color=STARK_COLORS["ia_text"]
        )
        self.status_label.configure(
            text="🎤 Ouvindo...",
            text_color=STARK_COLORS["ia_text"]
        )
        
        # Thread para escuta
        threading.Thread(target=self.listen_for_speech, daemon=True).start()
    
    def stop_listening(self):
        """Para o modo de escuta"""
        self.is_listening = False
        self.listen_button.configure(
            text="🎤 Ouvir",
            fg_color=STARK_COLORS["button_normal"],
            hover_color=STARK_COLORS["button_hover"],
            text_color=STARK_COLORS["button_text"]
        )
        self.status_label.configure(
            text="🟢 Online",
            text_color=STARK_COLORS["ia_text"]
        )
    
    def listen_for_speech(self):
        """Escuta comandos de voz"""
        try:
            with self.microphone as source:
                self.root.after(0, lambda: self.add_message("Sistema", "🎤 Ajustando ruído ambiente...", is_system=True))
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.root.after(0, lambda: self.add_message("Sistema", "🎤 Ouvindo... Fale agora!", is_system=True))
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Reconhece o áudio
            try:
                text = self.recognizer.recognize_google(audio, language='pt-BR')
                self.root.after(0, lambda: self.process_voice_command(text))
            except sr.UnknownValueError:
                self.root.after(0, lambda: self.add_message("Sistema", "🔇 Não consegui entender. Fale novamente.", is_system=True))
            except sr.RequestError as e:
                self.root.after(0, lambda: self.add_message("Sistema", f"❌ Erro no reconhecimento: {e}", is_system=True))
                
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.add_message("Sistema", "⏰ Tempo esgotado. Tente novamente.", is_system=True))
        except sr.RequestError as e:
            self.root.after(0, lambda: self.add_message("Sistema", f"❌ Erro no microfone: {e}", is_system=True))
        except Exception as e:
            self.root.after(0, lambda: self.add_message("Sistema", f"❌ Erro na escuta: {e}", is_system=True))
        finally:
            self.root.after(0, self.stop_listening)
    
    def process_voice_command(self, text):
        """Processa comando de voz"""
        self.add_message("Você", text, is_user=True)
        self.process_with_gemini(text)
    
    def capture_and_analyze_screen(self):
        """Wrapper para captura e análise de tela que exibe resultado na interface"""
        if not self.vision.vision_enabled:
            self.add_message("Sistema", "❌ Visão computacional não está disponível. Verifique sua API key.", is_system=True)
            return
        
        # Adiciona mensagem de sistema indicando captura
        self.add_message("Sistema", "📸 Capturando e analisando tela...", is_system=True)
        
        # Executa a captura em thread para não bloquear a interface
        def analyze_in_thread():
            try:
                result = self.vision.capture_and_analyze()
                if result:
                    # Exibe o resultado como mensagem do Jarvis
                    self.root.after(0, lambda: self.add_message("Jarvis", result, is_jarvis=True))
                else:
                    self.root.after(0, lambda: self.add_message("Sistema", "❌ Falha ao analisar a tela.", is_system=True))
            except Exception as e:
                error_msg = f"❌ Erro na análise: {str(e)}"
                self.root.after(0, lambda: self.add_message("Sistema", error_msg, is_system=True))
        
        threading.Thread(target=analyze_in_thread, daemon=True).start()
    
    def send_message(self, event=None):
        """Envia mensagem digitada"""
        message = self.text_input.get().strip()
        if not message:
            return
        
        # Limpa o campo
        self.text_input.delete(0, "end")
        
        # Adiciona mensagem do usuário
        self.add_message("Você", message, is_user=True)
        
        # Processa com Gemini
        self.process_with_gemini(message)
    
    def process_with_gemini(self, message):
        """Processa mensagem com Gemini e controle de sistema"""
        # Primeiro, verifica se é um comando de sistema
        if SYSTEM_CONTROL_AVAILABLE and self.system_controller:
            command_intent = self.system_controller.detect_command_intent(message)
            if command_intent:
                command_type, command_data = command_intent
                result = self.system_controller.execute_command(command_type, command_data)
                self.add_message("Jarvis", result, is_jarvis=True)
                
                # Salva na memória como comando executado
                self.memory.add_memory(f"Comando sistema: {message} → {result}", "system_command")
                return
        
        # Se não for comando de sistema, processa com Gemini
        if not self.vision.api_key or self.vision.api_key == 'sua_chave_api_aqui':
            self.add_message("Jarvis", "❌ Configure sua API key do Gemini no arquivo .env para usar esta funcionalidade.", is_jarvis=True)
            return
        
        self.is_processing = True
        self.status_label.configure(
            text="🟡 Processando...",
            text_color=STARK_COLORS["ia_text"]
        )
        
        # Inicia animação da barra de progresso
        self.start_progress_animation()
        
        # Thread para processamento
        def process_and_respond():
            try:
                # Contexto da conversa (últimas 5-10 mensagens)
                conversation_history = ""
                if len(self.chat_history) > 0:
                    # Pega as últimas 10 mensagens do histórico
                    recent_messages = self.chat_history[-10:]
                    history_lines = []
                    for msg in recent_messages:
                        if msg.get('is_user'):
                            history_lines.append(f"VOCÊ: {msg['message']}")
                        elif msg.get('is_jarvis'):
                            history_lines.append(f"JARVIS: {msg['message']}")
                        elif msg.get('is_system'):
                            history_lines.append(f"SISTEMA: {msg['message']}")
                    
                    conversation_history = "\n".join(history_lines)
                
                # Memórias do sistema (apenas para contexto profundo)
                memories = self.memory.get_recent_memories(3)
                memory_context = "\n".join([f"- {mem[0]}" for mem in memories]) if memories else ""
                
                # Adiciona informações de comandos disponíveis ao contexto
                system_commands_info = ""
                if SYSTEM_CONTROL_AVAILABLE and self.system_controller:
                    system_commands_info = "\n\nComandos de sistema disponíveis:\n" + \
                                        self.system_controller.list_available_commands()
                
                # Detecção de pedido de detalhamento
                needs_detail = any(keyword in message.lower() for keyword in ['mais detalhes', 'continue', 'explique melhor', 'pode detalhar', 'mais informações'])
                
                # Prompt otimizado com contexto da conversa
                if needs_detail:
                    prompt = f"""Você é J.A.R.V.I.S., assistente de IA avançada com controle de sistema.

Regras para esta resposta:
- Forneça análise profunda e técnica (ignore a regra de concisão)
- Use todo o contexto disponível
- Seja detalhado e completo

Histórico da conversa recente:
{conversation_history}

Memórias do sistema:
{memory_context}
{system_commands_info}

Comando atual: {message}

Responda com detalhamento técnico completo."""
                else:
                    prompt = f"""Você é J.A.R.V.I.S., assistente de IA avançada com controle de sistema.

Regras de resposta:
- Seja objetivo e direto, sem introduções longas
- Limite: 2-3 parágrafos curtos
- Tom: técnico, útil, levemente sarcástico/atencioso
- Sem enrolações como "Com certeza" ou "Aqui está sua análise"

Histórico da conversa recente:
{conversation_history}

Memórias do sistema:
{memory_context}
{system_commands_info}

Comando: {message}

Responda de forma técnica e direta."""
                
                # Chamada à API com configuração otimizada
                model = genai.GenerativeModel(
                    'gemini-2.5-flash',
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=4096,  # Aumentado para 4096
                        temperature=0.7,
                        stop_sequences=None,  # Remove stop sequences para não cortar
                        candidate_count=1
                    )
                )
                response = model.generate_content(prompt)
                
                # 1. PRIMEIRO: Extrai o texto bruto da resposta
                try:
                    full_response = response.text
                    print(f"✅ Texto extraído: {len(full_response)} caracteres")
                except Exception as extract_error:
                    print(f"❌ Erro ao extrair texto da resposta: {extract_error}")
                    full_response = str(response)  # Fallback para string da resposta
                
                # 2. DEPOIS: Limpeza de Markdown com tratamento de erro
                try:
                    # Limpeza direta de Markdown
                    cleaned_response = full_response.replace('###', '').replace('**', '').replace('---', '').replace('*', '').replace('`', '')
                    # Limpeza adicional com regex
                    cleaned_response = re.sub(r'^#{1,6}\s+', '', cleaned_response, flags=re.MULTILINE)
                    cleaned_response = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_response)
                    cleaned_response = re.sub(r'\*(.*?)\*', r'\1', cleaned_response)
                    cleaned_response = re.sub(r'`(.*?)`', r'\1', cleaned_response)
                    cleaned_response = re.sub(r'^[-*]{3,}\s*$', '', cleaned_response, flags=re.MULTILINE)
                    cleaned_response = re.sub(r'\s+', ' ', cleaned_response)
                    
                    # Usa o texto limpo
                    final_response = cleaned_response
                    print(f"✅ Markdown limpo com sucesso")
                    
                except Exception as clean_error:
                    print(f"⚠️ Erro na limpeza de Markdown: {clean_error}")
                    # Se falhar, usa o texto original
                    final_response = full_response
                    print(f"🔄 Usando texto original devido a erro na limpeza")
                
                # Verifica se a resposta foi truncada
                if len(final_response) < 10:
                    print(f"⚠️ Resposta curta detectada: {len(final_response)} caracteres")
                elif len(final_response) >= 4080:
                    print(f"⚠️ Resposta pode estar truncada: {len(final_response)} caracteres")
                
                print(f"✅ Resposta final pronta: {len(final_response)} caracteres")
                
                # Armazena resposta completa em variável de instância para evitar limpeza
                self.current_response = final_response
                
                # Efeito typewriter na thread principal
                # Garante que a resposta está completa antes de iniciar typewriter
                if final_response and len(final_response.strip()) > 0:
                    self.root.after(0, lambda: self.typewriter_effect("Jarvis", self.current_response))
                else:
                    self.root.after(0, lambda: self.add_message("Jarvis", "❌ Resposta vazia recebida", is_jarvis=True))
                
                # Salva na memória
                self.memory.add_memory(f"Usuário perguntou: {message}", "conversation")
                self.memory.add_memory(f"Jarvis respondeu: {final_response[:100]}...", "conversation")
                
            except Exception as e:
                error_msg = f"❌ Erro ao processar: {e}"
                self.root.after(0, lambda: self.add_message("Jarvis", error_msg, is_jarvis=True))
            finally:
                self.root.after(0, lambda: self.status_label.configure(text="🟢 Online", text_color=STARK_COLORS["ia_text"]))
                self.root.after(0, lambda: setattr(self, 'is_processing', False))
            self.root.after(0, lambda: self.status_label.configure(text="🟢 Online", text_color=STARK_COLORS["ia_text"]))
            self.root.after(0, lambda: setattr(self, 'is_processing', False))
            self.root.after(0, lambda: self.stop_progress_animation())
        
        # Executa a thread dentro do escopo correto
        threading.Thread(target=process_and_respond, daemon=True).start()
    
    def emergency_silence(self):
        """Executa Protocolo Silêncio via botão de emergência"""
        if not SYSTEM_CONTROL_AVAILABLE or not self.system_controller:
            self.add_message("Sistema", "❌ Controlador de sistema não disponível", is_system=True)
            return
        
        # Feedback visual imediato
        self.add_message("Sistema", "🚨 **PROTOCOLO SILÊNCIO ATIVADO!**", is_system=True)
        self.status_label.configure(text="🚨 EMERGÊNCIA", text_color="#FF4444")
        
        def execute_emergency():
            try:
                result = self.system_controller.execute_command("emergency_silence", {})
                self.root.after(0, lambda: self.add_message("Jarvis", result, is_jarvis=True))
            except Exception as e:
                logger.error(e, "Erro no Protocolo Silêncio", "EMERGÊNCIA")
                self.root.after(0, lambda: self.add_message("Sistema", f"❌ Erro: {e}", is_system=True))
            finally:
                # Reseta status após 3 segundos
                self.root.after(3000, lambda: self.status_label.configure(
                    text="🟢 Online", 
                    text_color=STARK_COLORS["ia_text"]
                ))
        
        # Executa imediatamente em thread separada
        threading.Thread(target=execute_emergency, daemon=True).start()

    def typewriter_effect(self, sender, message):
        """Efeito typewriter para mensagens do Jarvis no layout clean"""
        # Verifica se a mensagem é válida antes de processar
        if not message or not isinstance(message, str):
            self.add_message("Jarvis", "❌ Mensagem inválida para exibição", is_jarvis=True)
            return
        
        # Habilita o textbox para edição
        self.chat_display.configure(state="normal")
        
        # Layout Clean: Nome JARVIS em azul neon
        self.chat_display.insert("end", "JARVIS\n", "jarvis_name")
        self.chat_display.tag_config("jarvis_name", foreground="#00D2FF")
        
        # Armazena a mensagem completa em variável local para garantir persistência durante o loop
        complete_message = str(message)  # Garante que é string
        self.current_response = complete_message  # Backup em variável de instância
        
        # Efeito typewriter para a mensagem
        def add_char_by_char():
            try:
                # Usa a variável de instância para garantir persistência durante o loop
                message_to_type = self.current_response
                
                for i, char in enumerate(message_to_type):
                    # Verifica se ainda está processando antes de cada caractere
                    if not self.is_processing:
                        # Se interrompido, adiciona o resto da mensagem de uma vez
                        remaining_text = message_to_type[i:]
                        self.chat_display.insert("end", remaining_text, "jarvis_message")
                        self.chat_display.tag_config("jarvis_message", foreground="#ffffff")
                        break
                    
                    # Adiciona caractere por caractere
                    self.chat_display.insert("end", char, "jarvis_message")
                    self.chat_display.tag_config("jarvis_message", foreground="#ffffff")
                    
                    # Auto-scroll e pequena pausa
                    self.chat_display.see("end")
                    self.root.update()
                    time.sleep(0.01)  # Pequena pausa para efeito
                
                # Adiciona espaçamento final após a mensagem
                self.chat_display.insert("end", "\n\n", "jarvis_message")
                self.chat_display.tag_config("jarvis_message", foreground="#ffffff")
                
                # Auto-scroll final
                self.chat_display.see("end")
                
            except Exception as e:
                print(f"Erro no efeito typewriter: {e}")
                # Em caso de erro, adiciona a mensagem completa
                self.chat_display.insert("end", f"{message_to_type}\n\n", "jarvis_message")
                self.chat_display.tag_config("jarvis_message", foreground="#ffffff")
                self.chat_display.see("end")
            finally:
                # Sempre desabilita o textbox no final
                self.chat_display.configure(state="disabled")
        
        # Executa o efeito em uma thread separada para não bloquear a interface
        threading.Thread(target=add_char_by_char, daemon=True).start()

    def clear_chat(self):
        """Limpa o chat"""
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.chat_history.clear()

    def filter_ai_text(self, text):
        """Filtra texto da IA removendo símbolos indesejados e limpando formatação"""
        if not text or not isinstance(text, str):
            return text
            
        # Usa expressões regulares para limpeza mais eficiente
        filtered_text = text
        
        # Remove cabeçalhos Markdown (###, ##, #)
        filtered_text = re.sub(r'^#{1,6}\s+', '', filtered_text, flags=re.MULTILINE)
        
        # Remove negrito (**texto**)
        filtered_text = re.sub(r'\*\*(.*?)\*\*', r'\1', filtered_text)
        
        # Remove itálico (*texto*)
        filtered_text = re.sub(r'\*(.*?)\*', r'\1', filtered_text)
        
        # Remove código inline (`texto`)
        filtered_text = re.sub(r'`(.*?)`', r'\1', filtered_text)
        
        # Remove linhas horizontais (--- ou ***)
        filtered_text = re.sub(r'^[-*]{3,}\s*$', '', filtered_text, flags=re.MULTILINE)
        
        # Remove múltiplos espaços em branco
        filtered_text = re.sub(r'\s+', ' ', filtered_text)
        
        # Remove espaços no início e fim de cada linha
        lines = filtered_text.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        
        return '\n'.join(cleaned_lines)

    def add_message(self, sender, message, is_user=False, is_jarvis=False, is_system=False):
        """Adiciona mensagem ao chat estilo Gemini/ChatGPT com cores diferentes"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Habilita o textbox para edição
        self.chat_display.configure(state="normal")
        
        # Layout Clean: Texto corrido estilo Gemini
        if is_jarvis:
            # Nome JARVIS em azul neon acima da resposta
            self.chat_display.insert("end", f"JARVIS\n", "jarvis_name")
            self.chat_display.tag_config("jarvis_name", foreground="#00D2FF")
            
            # Resposta em branco com espaçamento adequado
            self.chat_display.insert("end", f"{message}\n\n", "jarvis_message")
            self.chat_display.tag_config("jarvis_message", foreground="#ffffff")
            
        elif is_user:
            # Mensagem do usuário
            self.chat_display.insert("end", f"VOCÊ\n", "user_name")
            self.chat_display.tag_config("user_name", foreground="#e5e5e5")
            
            self.chat_display.insert("end", f"{message}\n\n", "user_message")
            self.chat_display.tag_config("user_message", foreground="#ffffff")
            
        elif is_system:
            # Mensagem do sistema
            self.chat_display.insert("end", f"SISTEMA\n", "system_name")
            self.chat_display.tag_config("system_name", foreground="#ffaa00")
            
            self.chat_display.insert("end", f"{message}\n\n", "system_message")
            self.chat_display.tag_config("system_message", foreground="#ffffff")
            
        else:
            # Outros remetentes
            self.chat_display.insert("end", f"{sender}\n", "other_name")
            self.chat_display.tag_config("other_name", foreground="#ffffff")
            
            self.chat_display.insert("end", f"{message}\n\n", "other_message")
            self.chat_display.tag_config("other_message", foreground="#ffffff")
        
        # Nota: CTkTextbox não suporta recuo por tag, então o recuo foi removido
        # O texto será exibido com alinhamento padrão
        
        # Auto-scroll para o final
        self.chat_display.see("end")
        
        # Desabilita o textbox novamente
        self.chat_display.configure(state="disabled")
        
        # Salva no histórico
        self.chat_history.append({
            "sender": sender,
            "message": message,
            "timestamp": timestamp,
            "is_user": is_user,
            "is_jarvis": is_jarvis,
            "is_system": is_system
        })

    def run(self):
        """Inicia a aplicação com tratamento robusto"""
        try:
            print("🚀 Iniciando interface J.A.R.V.I.S. Stark Industries...")
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Encerrando interface do Jarvis...")
            self.force_shutdown()
        except Exception as e:
            print(f"❌ Erro crítico na interface: {e}")
            self.force_shutdown()
        finally:
            print("✅ Interface encerrada com segurança")

    def force_shutdown(self):
        """Força encerramento seguro da aplicação"""
        try:
            # Para todas as animações
            self.is_processing = False
            self.progress_animation_active = False
            
            # Fecha a janela principal
            if hasattr(self, 'root') and self.root:
                self.root.quit()
                self.root.destroy()
        except Exception as e:
            print(f"⚠️ Erro no encerramento: {e}")
        finally:
            import sys
            sys.exit(0)

def main():
    """Função principal"""
    
    # Carrega variáveis de ambiente no início
    if getattr(sys, 'frozen', False):
        # Estamos rodando como executável PyInstaller
        base_dir = os.path.dirname(sys.executable)
        print(f"🔧 Executável detectado, diretório base: {base_dir}")
    else:
        # Estamos rodando como script Python
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"🔧 Script detectado, diretório base: {base_dir}")
    
    # Caminho absoluto para o .env
    env_path = os.path.join(base_dir, '.env')
    print(f"🔧 Procurando .env em: {env_path}")
    
    # Carrega o .env se existir
    if os.path.exists(env_path):
        try:
            load_dotenv(env_path, encoding='utf-8', override=True)
            print(f"✅ Arquivo .env carregado com UTF-8")
            
            # Debug: mostra API key mascarada
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and len(api_key) > 10:
                masked_key = f"{api_key[:8]}...{api_key[-4:]}"
                print(f"🔑 API Key detectada: {masked_key}")
            elif api_key:
                print("🔑 API Key detectada (curta)")
            else:
                print("❌ API Key não encontrada no .env!")
                
        except Exception as e:
            print(f"❌ Erro ao carregar .env: {e}")
            # Fallback
            load_dotenv(override=True)
    else:
        print(f"⚠️ Arquivo .env não encontrado em: {env_path}")
        # Tenta carregar do diretório atual
        load_dotenv(override=True)
    
    # Correção para executável sem console (PyInstaller --noconsole)
    if getattr(sys, 'frozen', False):
        # Redireciona stdin, stdout e stderr para evitar erros
        import io
        sys.stdin = io.StringIO()
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        logger.log_info("Executável detectado - Redirecionando I/O para modo gráfico", "SISTEMA")
    
    logger.log_info("Iniciando função principal do J.A.R.V.I.S.", "SISTEMA")
    
    try:
        logger.log_info("Criando instância da interface GUI", "SISTEMA")
        app = JarvisGUI()
        logger.log_info("Interface criada com sucesso, iniciando mainloop", "SISTEMA")
        app.run()
    except KeyboardInterrupt:
        logger.log_info("Programa interrompido pelo usuário", "SISTEMA")
        print("\n👋 Encerrando interface do Jarvis...")
        sys.exit(0)
    except Exception as e:
        logger.log_error(e, "Erro crítico ao iniciar interface", "SISTEMA")
        
        # Salva erro crítico em arquivo (redundância com logger, mas garante)
        try:
            # Determina o diretório base (executável ou script)
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            error_file = os.path.join(base_path, 'ERRO_CRITICO.txt')
            
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write("🤖 J.A.R.V.I.S. - ERRO CRÍTICO DE INICIALIZAÇÃO\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Sistema: {sys.platform}\n")
                f.write(f"Python: {sys.version}\n")
                f.write(f"Executável: {getattr(sys, 'frozen', False)}\n")
                f.write(f"Diretório: {base_path}\n")
                f.write(f"Módulo: {__name__}\n")
                f.write(f"Contexto: main\n\n")
                f.write("ERRO:\n")
                f.write(f"Tipo: {type(e).__name__}\n")
                f.write(f"Mensagem: {str(e)}\n\n")
                f.write("TRACEBACK COMPLETO:\n")
                import traceback
                f.write(traceback.format_exc())
                f.write("\n\n")
                f.write("INFORMAÇÕES ADICIONAIS:\n")
                f.write(f"Arquivos no diretório:\n")
                for item in os.listdir(base_path):
                    f.write(f"  - {item}\n")
            
            print(f"❌ Erro crítico salvo em: {error_file}")
            
        except Exception as save_error:
            logger.log_error(save_error, "Erro ao salvar arquivo de erro crítico", "SISTEMA")
        
        print(f"❌ Erro ao iniciar interface: {e}")
        print("Erro ao iniciar interface. O programa será encerrado.")
        sys.exit(1)

if __name__ == "__main__":
    main()
