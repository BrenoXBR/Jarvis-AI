"""
J.A.R.V.I.S. - Core Module
Lógica de integração com a API do Gemini e processamento
"""

import os
import re
import threading
import google.generativeai as genai
from typing import Optional, Dict, List, Tuple
from datetime import datetime

class JarvisCore:
    """Núcleo de processamento do J.A.R.V.I.S."""
    
    def __init__(self, logger):
        self.logger = logger
        self.api_key = None
        self.vision_enabled = False
        self.typing_active = False
        self.typing_callbacks = []
        
        # Carrega API key
        self._load_api_key()
        
        # Inicializa modelo Gemini
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                self.vision_enabled = True
                self.logger.info("API Gemini configurada com sucesso", "CORE")
            except Exception as e:
                self.logger.error(e, "Erro ao configurar API Gemini", "CORE")
                self.vision_enabled = False
        else:
            self.logger.warning("API key não encontrada", "CORE")
    
    def _load_api_key(self):
        """Carrega API key do arquivo .env"""
        try:
            # Tenta carregar do arquivo .env
            env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
            
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('GEMINI_API_KEY='):
                            self.api_key = line.split('=', 1)[1].strip()
                            break
            
            if self.api_key and self.api_key != 'sua_chave_api_aqui':
                self.logger.info("API key carregada com sucesso", "CORE")
            else:
                self.logger.warning("API key inválida ou não encontrada", "CORE")
                self.api_key = None
                
        except Exception as e:
            self.logger.error(e, "Erro ao carregar API key", "CORE")
            self.api_key = None
    
    def is_available(self) -> bool:
        """Verifica se a API está disponível"""
        return self.vision_enabled and self.api_key is not None
    
    def process_message(self, message: str, conversation_history: List[Dict], memories: List[str], system_commands_info: str = "") -> str:
        """Processa mensagem com Gemini e retorna resposta"""
        if not self.is_available():
            return "❌ API Gemini não está disponível. Verifique sua API key no arquivo .env."
        
        try:
            self.logger.system("Enviando requisição para API Gemini...", "CORE")
            
            # Prepara contexto da conversa
            context = self._prepare_context(message, conversation_history, memories, system_commands_info)
            
            # Detecção de pedido de detalhamento
            needs_detail = any(keyword in message.lower() for keyword in ['mais detalhes', 'continue', 'explique melhor', 'pode detalhar', 'mais informações'])
            
            # Configuração do modelo
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=4096,
                temperature=0.7,
                stop_sequences=None,
                candidate_count=1
            )
            
            # Gera resposta
            response = self.model.generate_content(
                context,
                generation_config=generation_config
            )
            
            # Processa resposta
            full_response = self._extract_response_text(response)
            cleaned_response = self._clean_response(full_response)
            
            self.logger.system(f"Resposta recebida: {len(cleaned_response)} caracteres", "CORE")
            
            # Salva na memória
            self._save_to_memory(message, cleaned_response)
            
            return cleaned_response
            
        except Exception as e:
            self.logger.error(e, "Erro ao processar mensagem com Gemini", "CORE")
            return f"❌ Erro ao processar mensagem: {str(e)}"
    
    def _prepare_context(self, message: str, conversation_history: List[Dict], memories: List[str], system_commands_info: str) -> str:
        """Prepara o contexto completo para a API"""
        # Histórico da conversa
        history_lines = []
        if conversation_history:
            recent_messages = conversation_history[-10:]  # Últimas 10 mensagens
            for msg in recent_messages:
                if msg.get('is_user'):
                    history_lines.append(f"VOCÊ: {msg['message']}")
                elif msg.get('is_jarvis'):
                    history_lines.append(f"JARVIS: {msg['message']}")
                elif msg.get('is_system'):
                    history_lines.append(f"SISTEMA: {msg['message']}")
        
        conversation_context = "\n".join(history_lines)
        
        # Memórias do sistema
        memory_context = "\n".join([f"- {mem}" for mem in memories]) if memories else ""
        
        # Detecção de pedido de detalhamento
        needs_detail = any(keyword in message.lower() for keyword in ['mais detalhes', 'continue', 'explique melhor', 'pode detalhar', 'mais informações'])
        
        # Prompt otimizado
        if needs_detail:
            prompt = f"""Você é J.A.R.V.I.S., assistente de IA avançada com controle de sistema.

Regras para esta resposta:
- Forneça análise profunda e técnica (ignore a regra de concisão)
- Use todo o contexto disponível
- Seja detalhado e completo

Histórico da conversa recente:
{conversation_context}

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
{conversation_context}

Memórias do sistema:
{memory_context}
{system_commands_info}

Comando: {message}

Responda de forma técnica e direta."""
        
        return prompt
    
    def _extract_response_text(self, response) -> str:
        """Extrai texto bruto da resposta da API"""
        try:
            full_response = response.text
            self.logger.system(f"Texto extraído da API: {len(full_response)} caracteres", "CORE")
            return full_response
        except Exception as e:
            self.logger.error(e, "Erro ao extrair texto da resposta", "CORE")
            return str(response)  # Fallback
    
    def _clean_response(self, response: str) -> str:
        """Limpa Markdown e formatação da resposta"""
        try:
            # Limpeza direta de Markdown
            cleaned = response.replace('###', '').replace('**', '').replace('---', '').replace('*', '').replace('`', '')
            
            # Limpeza adicional com regex
            cleaned = re.sub(r'^#{1,6}\s+', '', cleaned, flags=re.MULTILINE)
            cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)
            cleaned = re.sub(r'\*(.*?)\*', r'\1', cleaned)
            cleaned = re.sub(r'`(.*?)`', r'\1', cleaned)
            cleaned = re.sub(r'^[-*]{3,}\s*$', '', cleaned, flags=re.MULTILINE)
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            self.logger.system("Markdown limpo com sucesso", "CORE")
            return cleaned.strip()
            
        except Exception as e:
            self.logger.error(e, "Erro na limpeza de Markdown", "CORE")
            return response  # Fallback para texto original
    
    def _save_to_memory(self, user_message: str, jarvis_response: str):
        """Salva interação na memória"""
        try:
            # Aqui poderia integrar com um sistema de memória persistente
            # Por enquanto, apenas loga
            self.logger.info(f"Memória: User='{user_message[:50]}...', Jarvis='{jarvis_response[:50]}...'", "CORE")
        except Exception as e:
            self.logger.error(e, "Erro ao salvar na memória", "CORE")
    
    def register_typing_callback(self, callback):
        """Registra callback para efeito de digitação"""
        self.typing_callbacks.append(callback)
    
    def start_typing_effect(self, message: str, callback):
        """Inicia efeito de digitação em thread separada"""
        if not message or not isinstance(message, str):
            callback("❌ Mensagem inválida para exibição")
            return
        
        self.typing_active = True
        self.logger.system("Iniciando efeito de digitação", "CORE")
        
        def typing_thread():
            try:
                # Efeito de digitação caracter por caracter
                displayed_text = ""
                for i, char in enumerate(message):
                    if not self.typing_active:
                        break
                    
                    displayed_text += char
                    
                    # Adiciona cursor piscante
                    text_with_cursor = displayed_text + "█"
                    
                    # Chama callback na thread principal
                    if hasattr(callback, '__call__'):
                        callback(text_with_cursor, i == len(message) - 1)
                    
                    # Pequeno delay para efeito de digitação
                    import time
                    time.sleep(0.02)  # 50ms por caractere
                
                # Remove cursor no final
                if self.typing_active:
                    callback(displayed_text, True)
                    
            except Exception as e:
                self.logger.error(e, "Erro no efeito de digitação", "CORE")
                callback(f"❌ Erro na exibição: {e}")
            finally:
                self.typing_active = False
        
        # Executa em thread separada para não bloquear
        thread = threading.Thread(target=typing_thread, daemon=True)
        thread.start()
    
    def stop_typing(self):
        """Para o efeito de digitação atual"""
        self.typing_active = False
        self.logger.system("Efeito de digitação parado", "CORE")
    
    def get_api_status(self) -> Dict[str, any]:
        """Retorna status da API"""
        return {
            'available': self.is_available(),
            'key_configured': self.api_key is not None,
            'model': 'gemini-2.5-flash' if self.is_available() else None,
            'last_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
