#!/usr/bin/env python3
"""
Arquivo de configuração do J.A.R.V.I.S. Mark 13 M-13 OMNI
Centraliza todas as configurações de cores, fontes e parâmetros
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Classe de configuração do J.A.R.V.I.S. Mark 13"""
    
    # ==================== CONFIGURAÇÕES DA API ====================
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # ==================== CONFIGURAÇÕES DE ÁUDIO ====================
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    
    # ==================== CONFIGURAÇÕES DO ASSISTENTE ====================
    KEYWORD = "jarvis"
    WAKE_WORD_TIMEOUT = 1  # segundos
    COMMAND_TIMEOUT = 5    # segundos
    COMMAND_PHRASE_LIMIT = 10  # segundos
    
    # ==================== CONFIGURAÇÕES DE VOZ ====================
    VOICE_RATE = 150
    VOICE_VOLUME = 0.9
    
    # ==================== CONFIGURAÇÕES DA IA ====================
    AI_MODEL = 'gemini-2.5-flash'
    MAX_HISTORY = 5
    TEMPERATURE = 0.7
    MAX_TOKENS = 150
    
    # ==================== CONFIGURAÇÕES DO SYSTEM ACTIONS ====================
    WORKSPACE_PATH = os.getenv('WORKSPACE_PATH', os.path.expanduser("~/Desktop"))
    ENABLE_SYSTEM_ACTIONS = os.getenv('ENABLE_SYSTEM_ACTIONS', 'true').lower() == 'true'
    
    # ==================== CONFIGURAÇÕES VISUAIS M-13 ====================
    
    # Tema Deep Charcoal & Electric Blue
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
    
    # Fontes
    FONTS = {
        "chat_family": "Segoe UI",
        "chat_size": 12,
        "monitor_family": "Consolas",
        "monitor_size": 9,
        "title_size": 22,
        "button_size": 12,
        "label_size": 10
    }
    
    # Dimensões da Interface
    UI_DIMENSIONS = {
        "window_width": 1200,
        "window_height": 800,
        "border_width": 2,
        "corner_radius": 10,
        "button_width": 80,
        "voice_button_width": 40,
        "toggle_button_width": 120,
        "clear_button_width": 100
    }
    
    # ==================== CONFIGURAÇÕES DE WEB APIs ====================
    
    # OpenWeatherMap (substituído por wttr.in)
    WEATHER_CONFIG = {
        "timeout": 10,
        "city": "Votorantim",
        "fallback_city": "Sorocaba",
        "units": "metric",
        "lang": "pt_br"
    }
    
    # Yahoo Finance
    CURRENCY_CONFIG = {
        "timeout": 10,
        "period": "1d",
        "default_from": "USD",
        "default_to": "BRL"
    }
    
    # G1 Notícias
    NEWS_CONFIG = {
        "url": "https://g1.globo.com/",
        "timeout": 10,
        "max_headlines": 3,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # ==================== CONFIGURAÇÕES DE SISTEMA ====================
    
    # Paths
    PATHS = {
        "capturas": "capturas",
        "logs": "jarvis_logs",
        "env_file": ".env"
    }
    
    # Hardware
    HARDWARE_CONFIG = {
        "brightness_step": 10,
        "volume_step": 0.1,
        "max_volume": 1.0,
        "min_volume": 0.0,
        "max_brightness": 100,
        "min_brightness": 0,
        "screenshot_format": "png"
    }
    
    # Pomodoro
    POMODORO_CONFIG = {
        "minutes": 25,
        "seconds": 1500,
        "default_task": "Estudo"
    }
    
    # ==================== MENSAGENS E TEXTOS ====================
    
    MESSAGES = {
        "welcome": """⚡ J.A.R.V.I.S. Mark 13 - OMNI SYSTEM ONLINE

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

**OMNI PROTOCOLS ENGAGED** 🚀""",
        
        "window_title": "🤖 J.A.R.V.I.S. - M-13 OMNI",
        "header_title": "⚡ J.A.R.V.I.S. - M-13 OMNI",
        "status_online": "🟢 Systems Online",
        "status_processing": "🟡 Processando...",
        "monitor_title": "🖥️ SYSTEM MONITOR",
        "toggle_monitor": "👁️ SHOW/HIDE",
        "clear_logs": "🗑️ CLEAR LOGS",
        "send_button": "Enviar",
        "voice_button": "🎤",
        "voice_recording": "🔴"
    }
    
    # ==================== CONFIGURAÇÕES DE TRATAMENTO DE ERROS ====================
    
    ERROR_MESSAGES = {
        "network_error": "❌ Serviço temporariamente indisponível. Verifique sua conexão com a internet.",
        "api_error": "❌ Erro ao comunicar com o serviço. Tente novamente em alguns minutos.",
        "parse_error": "❌ Erro ao processar resposta do servidor.",
        "timeout_error": "❌ Tempo de resposta esgotado. O serviço pode estar lento.",
        "file_error": "❌ Erro ao acessar arquivo. Verifique as permissões.",
        "system_error": "❌ Erro do sistema. Contate o suporte se o problema persistir.",
        "audio_error": "❌ Serviço de áudio não disponível neste sistema.",
        "brightness_error": "❌ Controle de brilho não disponível neste dispositivo.",
        "currency_error": "❌ Não foi possível obter cotação. Tente novamente mais tarde.",
        "weather_error": "❌ Serviço de clima temporariamente indisponível.",
        "news_error": "❌ Não foi possível carregar as notícias."
    }
    
    @classmethod
    def validate(cls):
        """Valida as configurações essenciais
        
        Returns:
            list: Lista de erros encontrados
        """
        errors = []
        
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == 'sua_api_key_aqui':
            errors.append("GEMINI_API_KEY não configurada no arquivo .env")
        
        # Valida paths
        for path_name, path_value in cls.PATHS.items():
            if path_name.endswith('_file') and not os.path.exists(path_value):
                if path_name == 'env_file':
                    errors.append(f"Arquivo {path_value} não encontrado")
        
        return errors
    
    @classmethod
    def get_color(cls, color_name: str) -> str:
        """Obtém uma cor do tema M-13
        
        Args:
            color_name (str): Nome da cor
            
        Returns:
            str: Código hexadecimal da cor
        """
        return cls.M13_COLORS.get(color_name, "#FFFFFF")
    
    @classmethod
    def get_font(cls, font_name: str) -> dict:
        """Obtém configurações de fonte
        
        Args:
            font_name (str): Nome da fonte
            
        Returns:
            dict: Configurações da fonte
        """
        font_config = {}
        if font_name == "chat":
            font_config["family"] = cls.FONTS["chat_family"]
            font_config["size"] = cls.FONTS["chat_size"]
        elif font_name == "monitor":
            font_config["family"] = cls.FONTS["monitor_family"]
            font_config["size"] = cls.FONTS["monitor_size"]
        elif font_name == "title":
            font_config["family"] = cls.FONTS["chat_family"]
            font_config["size"] = cls.FONTS["title_size"]
        elif font_name == "button":
            font_config["family"] = cls.FONTS["chat_family"]
            font_config["size"] = cls.FONTS["button_size"]
        elif font_name == "label":
            font_config["family"] = cls.FONTS["monitor_family"]
            font_config["size"] = cls.FONTS["label_size"]
        
        return font_config
