"""
J.A.R.V.I.S. Mark 13 - Core Module
Núcleo de processamento do assistente com integração à API Gemini AI
e efeito de digitação em tempo real.
"""

# ==================== BIBLIOTECAS PADRÃO ====================
import os
import sys
import re
import threading
from datetime import datetime
from typing import Optional, Dict, List, Tuple

# ==================== BIBLIOTECAS DE TERCEIROS ====================
import google.generativeai as genai
from dotenv import load_dotenv

# ==================== MÓDULOS PRÓPRIOS ====================
from config import Config

class JarvisCore:
    """Núcleo de processamento do J.A.R.V.I.S. Mark 13 M-13 OMNI.
    
    Esta classe é responsável pelo processamento de linguagem natural,
    integração com a API Gemini AI e efeitos de digitação em tempo real.
    Implementa o sistema de memória contextual e tratamento de comandos.
    
    Attributes:
        logger: Instância do logger para registrar eventos
        api_key (str): Chave de API do Google Gemini
        vision_enabled (bool): Indica se a visão computacional está ativa
        model: Modelo de IA Gemini configurado
        typing_active (bool): Indica se efeito de digitação está ativo
        typing_callbacks (list): Lista de callbacks para efeito de digitação
    """
    
    def __init__(self, logger):
        """Inicializa o núcleo de processamento J.A.R.V.I.S.
        
        Configura a API Gemini, sistema de digitação e memória contextual.
        Valida a disponibilidade dos serviços e registra o status inicial.
        
        Args:
            logger: Instância do logger para registrar eventos do sistema
            
        Raises:
            Exception: Caso ocorra erro na configuração da API Gemini
        """
        self.logger = logger
        self.api_key = None
        self.vision_enabled = False
        self.typing_active = False
        self.typing_callbacks = []
        self.auth_error_message = None
        
        # Carrega API key
        self._load_api_key()
        
        # Inicializa modelo Gemini
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(Config.AI_MODEL)
                self.vision_enabled = True
                self.logger.info("API Gemini configurada com sucesso", "CORE")
            except Exception as e:
                error_str = str(e).lower()
                if any(keyword in error_str for keyword in ['permission', 'forbidden', 'unauthorized', 'invalid', 'blocked']):
                    self.logger.error("API KEY BLOQUEADA OU INVÁLIDA", "CORE")
                    self.vision_enabled = False
                    self.auth_error_message = "Senhor, houve um erro de autenticação com os protocolos de IA. Verifique sua chave de acesso."
                else:
                    self.logger.error(e, "Erro ao configurar API Gemini", "CORE")
                    self.vision_enabled = False
                    self.auth_error_message = None
        else:
            self.logger.warning("API key não encontrada", "CORE")
            self.auth_error_message = "Senhor, houve um erro de autenticação com os protocolos de IA. Verifique sua chave de acesso."
    
    def _load_api_key(self):
        """Carrega API key do arquivo .env na pasta atual do projeto com os.getcwd()"""
        try:
            # Usa a pasta atual onde o programa está rodando
            current_dir = os.getcwd()
            env_path = os.path.join(current_dir, '.env')
            
            self.logger.system(f"[DEBUG] Buscando .env em: {env_path}", "CORE")
            
            # Verifica se o arquivo .env existe na pasta atual
            if os.path.exists(env_path):
                self.logger.system("[SUCCESS] .env encontrado na pasta do projeto.", "CORE")
                
                # Força o carregamento do .env da pasta atual
                load_dotenv(env_path, override=True)
                
                # Tenta obter do ambiente (após load_dotenv)
                self.api_key = os.getenv('GEMINI_API_KEY')
                
                # Debug mascarado - mostra apenas os 4 primeiros dígitos
                if self.api_key:
                    key_preview = self.api_key[:4] + "..." if len(self.api_key) > 4 else "CURTA"
                    self.logger.system(f"[DEBUG] API Key encontrada: {key_preview} (comprimento: {len(self.api_key)})", "CORE")
                    
                    # Verificação de espaços extras ou aspas
                    cleaned_key = self.api_key.strip().strip('"\'')
                    if cleaned_key != self.api_key:
                        self.logger.warning("[DEBUG] Removidos espaços/aspas da API key", "CORE")
                        self.api_key = cleaned_key
                        key_preview = self.api_key[:4] + "..." if len(self.api_key) > 4 else "CURTA"
                        self.logger.system(f"[DEBUG] API Key limpa: {key_preview} (comprimento: {len(self.api_key)})", "CORE")
                    
                    # Verificação de chave padrão/inválida
                    if self.api_key and self.api_key != 'sua_chave_api_aqui' and len(self.api_key) > 10:
                        self.logger.info("API key carregada com sucesso", "CORE")
                    else:
                        self.logger.warning("API key parece ser padrão ou muito curta", "CORE")
                        self.api_key = None
                else:
                    self.logger.warning("[DEBUG] API key não encontrada no environment após load_dotenv", "CORE")
                    
                    # Fallback: leitura manual do arquivo
                    self.logger.system("[DEBUG] Tentando leitura manual do .env", "CORE")
                    with open(env_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            line = line.strip()
                            if line.startswith('GEMINI_API_KEY='):
                                self.api_key = line.split('=', 1)[1].strip().strip('"\'')
                                key_preview = self.api_key[:4] + "..." if len(self.api_key) > 4 else "CURTA"
                                self.logger.system(f"[DEBUG] API key manual (linha {line_num}): {key_preview}", "CORE")
                                
                                if self.api_key and self.api_key != 'sua_chave_api_aqui' and len(self.api_key) > 10:
                                    self.logger.info("API key carregada via leitura manual", "CORE")
                                else:
                                    self.logger.warning("API key manual inválida ou padrão", "CORE")
                                    self.api_key = None
                                break
            else:
                self.logger.error(f"[ERROR] Arquivo .env não encontrado na pasta atual: {env_path}", "CORE")
                
                # Tenta caminho alternativo (pasta do script/executável)
                if getattr(sys, 'frozen', False):
                    # Se for o .exe, pega a pasta do executável
                    alt_dir = os.path.dirname(sys.executable)
                else:
                    # Se for o script .py, pega a pasta do script
                    alt_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                alt_env_path = os.path.join(alt_dir, '.env')
                self.logger.system(f"[DEBUG] Tentando caminho alternativo: {alt_env_path}", "CORE")
                
                if os.path.exists(alt_env_path):
                    self.logger.system("[SUCCESS] .env encontrado no caminho alternativo.", "CORE")
                    load_dotenv(alt_env_path, override=True)
                    self.api_key = os.getenv('GEMINI_API_KEY')
                    
                    if self.api_key:
                        key_preview = self.api_key[:4] + "..." if len(self.api_key) > 4 else "CURTA"
                        self.logger.system(f"[DEBUG] API Key encontrada (alt): {key_preview} (comprimento: {len(self.api_key)})", "CORE")
                        
                        if self.api_key and self.api_key != 'sua_chave_api_aqui' and len(self.api_key) > 10:
                            self.logger.info("API key carregada com sucesso (caminho alternativo)", "CORE")
                        else:
                            self.logger.warning("API key alternativa inválida ou padrão", "CORE")
                            self.api_key = None
                    else:
                        self.logger.error("[ERROR] API key não encontrada mesmo no caminho alternativo", "CORE")
                else:
                    self.logger.error(f"[ERROR] Arquivo .env não encontrado em nenhum caminho", "CORE")
                    self.api_key = None
                
        except Exception as e:
            self.logger.error(e, "Erro ao carregar API key", "CORE")
            self.api_key = None
    
    def has_auth_error(self) -> bool:
        """Verifica se há erro de autenticação
        
        Returns:
            bool: True se houver erro de autenticação
        """
        return self.auth_error_message is not None
    
    def get_auth_error_message(self) -> str:
        """Obtém mensagem de erro de autenticação
        
        Returns:
            str: Mensagem de erro ou None se não houver erro
        """
        return self.auth_error_message
    
    def is_available(self) -> bool:
        """Verifica se a API Gemini está disponível
        
        Returns:
            bool: True se a API estiver disponível
        """
        return self.vision_enabled and not self.has_auth_error() and self.api_key is not None
    
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
