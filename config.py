#!/usr/bin/env python3
"""
Arquivo de configuração do Assistente Jarvis
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Classe de configuração do Jarvis"""
    
    # Configurações da API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Configurações de áudio
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    
    # Configurações do assistente
    KEYWORD = "jarvis"
    WAKE_WORD_TIMEOUT = 1  # segundos
    COMMAND_TIMEOUT = 5    # segundos
    COMMAND_PHRASE_LIMIT = 10  # segundos
    
    # Configurações de voz
    VOICE_RATE = 150
    VOICE_VOLUME = 0.9
    
    # Configurações da IA
    AI_MODEL = 'gemini-pro'
    MAX_HISTORY = 5
    TEMPERATURE = 0.7
    MAX_TOKENS = 150
    
    # Configurações do Action Handler
    WORKSPACE_PATH = os.getenv('WORKSPACE_PATH', os.path.expanduser("~/Desktop"))
    ENABLE_SYSTEM_ACTIONS = os.getenv('ENABLE_SYSTEM_ACTIONS', 'true').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Valida as configurações"""
        errors = []
        
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == 'sua_api_key_aqui':
            errors.append("GEMINI_API_KEY não configurada no arquivo .env")
            
        return errors
