#!/usr/bin/env python3
"""
Sistema de Threads para Jarvis
Separa voz, IA e GUI em threads diferentes para evitar travamentos
"""

import threading
import queue
import time
import os
from PyQt6.QtCore import QThread, pyqtSignal, QObject
import speech_recognition as sr
import pyttsx3
from datetime import datetime
from jarvis_vision import VisionCommandHandler
from jarvis_cleanup import CleanupCommandHandler
from jarvis_memory import MemoryManager
from action_handler import ActionHandler
from mobile_bridge import JarvisMobileBridge

# Configuração de segurança do PyAutoGUI
try:
    import pyautogui
    pyautogui.FAILSAFE = True  # Fail-safe: mover mouse para canto superior esquerdo para parar
    pyautogui.PAUSE = 0.5  # Pausa entre comandos para evitar sobrecarga
except ImportError:
    print("⚠️ PyAutoGUI não disponível - algumas funcionalidades de automação podem não funcionar")

class VoiceWorker(QObject):
    """Worker para processamento de voz em thread separada"""
    
    # Sinais para comunicação com a GUI
    keyword_detected = pyqtSignal()
    command_received = pyqtSignal(str)
    speaking_started = pyqtSignal()
    speaking_finished = pyqtSignal()
    log_message = pyqtSignal(str, str)
    
    def __init__(self, keyword="jarvis"):
        super().__init__()
        self.keyword = keyword.lower()
        self.is_running = False
        self.is_speaking = False
        self.command_queue = queue.Queue()
        
        # Inicializa reconhecimento e síntese de voz
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Tenta diferentes drivers de áudio para o pyttsx3
        try:
            print("🔊 Tentando inicializar pyttsx3 com driver nsss...")
            self.engine = pyttsx3.init(driverName='nsss')
        except:
            try:
                print("🔊 Tentando inicializar pyttsx3 com driver espeak...")
                self.engine = pyttsx3.init(driverName='espeak')
            except:
                try:
                    print("🔊 Tentando inicializar pyttsx3 com driver sapi5 (padrão Windows)...")
                    self.engine = pyttsx3.init(driverName='sapi5')
                except:
                    print("🔊 Usando driver padrão do pyttsx3...")
        
        print(f"Engine pyttsx3 inicializado: {self.engine}")
        self.setup_voice()
        
    def setup_voice(self):
        """Configura a voz do assistente"""
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.engine.setProperty('rate', 200)
        self.engine.setProperty('volume', 1.0)
        
        # Teste de inicialização do áudio simplificado
        print(f"🔊 Configuração de voz:")
        print(f"   - Voz selecionada: {self.engine.getProperty('voice')}")
        print(f"   - Volume: {self.engine.getProperty('volume')}")
        print(f"   - Taxa: {self.engine.getProperty('rate')}")
        
        print("🔊 Executando teste de áudio...")
        try:
            self.engine.say("Teste de áudio do Jarvis")
            self.engine.runAndWait()
            print("✅ Teste de áudio executado com sucesso")
        except Exception as e:
            print(f"❌ Erro no teste de áudio: {e}")
            print("💡 Dicas para resolver problemas de áudio:")
            print("   1. Verifique se os alto-falantes estão conectados e com volume")
            print("   2. Verifique se o Windows não está mudo")
            print("   3. Tente reinstalar os drivers de áudio do Windows")
            print("   4. Verifique as permissões de áudio nas configurações do sistema")
        
    def start_listening(self):
        """Inicia o worker de voz"""
        self.is_running = True
        self.log_message.emit("Worker de voz iniciado", "SUCCESS")
        
        # Inicia thread de escuta
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        
        # Mensagem de boas-vindas
        self.speak("Sistema iniciado, mestre.")
        
        # Inicia thread de fala
        self.speak_thread = threading.Thread(target=self._speak_loop, daemon=True)
        self.speak_thread.start()
        
    def stop_listening(self):
        """Para o worker de voz"""
        self.is_running = False
        self.log_message.emit("Worker de voz parado", "WARNING")
        
    def _listen_loop(self):
        """Loop principal de escuta"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Mostra mensagem inicial apenas uma vez
            self.log_message.emit("Aguardando palavra-chave...", "INFO")
            
            while self.is_running:
                try:
                    # Só escuta se não estiver falando
                    if not self.is_speaking:
                        # Escuta palavra-chave
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                        
                        try:
                            text = self.recognizer.recognize_google(audio, language='pt-BR').lower()
                            
                            if self.keyword in text:
                                self.log_message.emit(f"Palavra-chave '{self.keyword}' detectada!", "SUCCESS")
                                self.keyword_detected.emit()
                                
                                # Escuta comando
                                self._listen_for_command()
                                
                        except sr.UnknownValueError:
                            continue
                        except sr.RequestError as e:
                            self.log_message.emit(f"Erro no reconhecimento: {e}", "ERROR")
                            time.sleep(2)
                    else:
                        # Se estiver falando, apenas espera
                        time.sleep(0.1)
                        
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    self.log_message.emit(f"Erro ao escutar: {e}", "ERROR")
                    time.sleep(1)
                
                # Pequena pausa para reduzir consumo de processamento
                time.sleep(0.1)
                    
    def _listen_for_command(self):
        """Escuta um comando específico"""
        try:
            self.log_message.emit("Aguardando comando...", "INFO")
            # Usa o mesmo source já aberto no loop principal
            audio = self.recognizer.listen(timeout=5, phrase_time_limit=10)
            command = self.recognizer.recognize_google(audio, language='pt-BR').lower()
            
            if command:
                self.log_message.emit(f"Comando recebido: {command}", "INFO")
                self.command_received.emit(command)
                
        except sr.WaitTimeoutError:
            self.log_message.emit("Tempo esgotado", "WARNING")
        except sr.UnknownValueError:
            self.command_queue.put("Não entendi. Poderia repetir?")
        except sr.RequestError as e:
            self.log_message.emit(f"Erro no reconhecimento: {e}", "ERROR")
        except Exception as e:
            self.log_message.emit(f"Erro ao processar comando: {e}", "ERROR")
                
    def _speak_loop(self):
        """Loop para processamento de fala"""
        while self.is_running:
            try:
                # Espera por mensagem para falar (timeout de 1 segundo)
                text = self.command_queue.get(timeout=1)
                
                if text and not self.is_speaking:
                    self._speak_text(text)
                    
            except queue.Empty:
                continue
            except Exception as e:
                self.log_message.emit(f"Erro no loop de fala: {e}", "ERROR")
                
    def _speak_text(self, text):
        """Fala o texto em thread separada para não bloquear"""
        def speak_worker():
            try:
                self.is_speaking = True
                self.speaking_started.emit()
                self.log_message.emit(f"Falando: {text}", "SPEAKING")
                
                print(f"🎙️ Jarvis está falando: '{text}'")
                
                # Para o loop de reconhecimento enquanto fala
                if hasattr(self, 'recognizer'):
                    try:
                        # Tenta parar o reconhecimento de forma segura
                        self.recognizer.operational_mode = False
                    except:
                        pass  # Ignora se não conseguir parar
                
                # Limpa o buffer antes de falar
                self.engine.stop()
                
                self.engine.say(text)
                print("🔊 Enviando texto para engine...")
                
                # Usa runAndWait() para garantir que o áudio seja reproduzido
                try:
                    self.engine.runAndWait()
                    print("✅ Fala concluída com sucesso (runAndWait)")
                except Exception as run_wait_error:
                    print(f"❌ Erro com runAndWait: {run_wait_error}")
                    print("🔄 Tentando método alternativo...")
                    
                    # Tenta método alternativo
                    try:
                        self.engine.startLoop(False)
                        time.sleep(0.5)  # Aguarda mais tempo
                        self.engine.endLoop()
                        print("✅ Fala concluída com sucesso (startLoop/endLoop)")
                    except Exception as alt_error:
                        print(f"❌ Erro com método alternativo: {alt_error}")
                        
                        # Fallback para winsound
                        try:
                            import winsound
                            winsound.MessageBeep(winsound.MB_OK)
                            print("✅ Beep do sistema executado (fallback winsound)")
                        except ImportError:
                            print("❌ winsound não disponível")
                        except Exception as beep_error:
                            print(f"❌ Erro no beep: {beep_error}")
                
            except Exception as e:
                print(f"❌ Erro ao falar: {e}")
                self.log_message.emit(f"Erro ao falar: {e}", "ERROR")
            finally:
                self.is_speaking = False
                self.speaking_finished.emit()
                print("🔇 Fala finalizada")
                
                # Reinicia o reconhecimento após falar
                try:
                    if hasattr(self, 'recognizer'):
                        self.recognizer = sr.Recognizer()
                        self.microphone = sr.Microphone()
                except Exception as e:
                    print(f"⚠️ Erro ao reiniciar reconhecimento: {e}")
        
        # Inicia o worker em thread separada
        speak_thread = threading.Thread(target=speak_worker, daemon=True)
        speak_thread.start()
            
    def speak(self, text):
        """Adiciona texto à fila de fala"""
        self.command_queue.put(text)
        
    def is_currently_speaking(self):
        """Verifica se está falando no momento"""
        return self.is_speaking

class AIWorker(QObject):
    """Worker para processamento de IA em thread separada"""
    
    # Sinais para comunicação com a GUI
    response_ready = pyqtSignal(str)
    processing_started = pyqtSignal()
    processing_finished = pyqtSignal()
    log_message = pyqtSignal(str, str)
    
    def __init__(self, api_key=None, workspace_path=None):
        super().__init__()
        self.api_key = api_key
        self.model = None
        self.is_initialized = False
        self.request_queue = queue.Queue()
        self.workspace_path = workspace_path
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Inicializa handlers especiais
        self.vision_handler = VisionCommandHandler(api_key)
        self.cleanup_handler = CleanupCommandHandler(workspace_path)
        self.memory_manager = MemoryManager(os.path.join(workspace_path, 'jarvis_memory.db') if workspace_path else None)
        self.action_handler = ActionHandler(workspace_path)
        
        if api_key:
            print(f"🔑 API Key encontrada: {api_key[:10]}...")
            self._initialize_ai()
        else:
            print("⚠️ Nenhuma API key encontrada no .env")
            self.log_message.emit("API key não encontrada", "ERROR")
            
    def _initialize_ai(self):
        """Inicializa a API da IA"""
        try:
            import google.generativeai as genai
            import os
            api_key = os.getenv('GEMINI_API_KEY')
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.is_initialized = True
            self.log_message.emit("IA inicializada com sucesso (gemini-2.5-flash)", "SUCCESS")
            print(f"🔑 API Key configurada: {api_key[:10]}...")
            print(f'Conectando ao modelo: {self.model.model_name}')
        except Exception as e:
            print(f'ERRO REAL DA IA: {e}')
            self.log_message.emit(f"Erro ao inicializar IA: {e}", "ERROR")

    def start_processing(self):
        """Inicia o worker de IA"""
        self.processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.processing_thread.start()
        self.log_message.emit("Worker de IA iniciado", "SUCCESS")

    def _processing_loop(self):
        """Loop principal de processamento"""
        while True:
            try:
                # Espera por requisição
                request_data = self.request_queue.get(timeout=1)
                
                if request_data:
                    command, context = request_data
                    self._process_command(command, context)
                    
            except queue.Empty:
                continue
            except Exception as e:
                self.log_message.emit(f"Erro no loop de IA: {e}", "ERROR")
                
    def _process_command(self, command, context=""):
        """Processa um comando com a IA"""
        # Processa entrada do usuário para extrair informações
        memory_info = self.memory_manager.process_user_input(command, self.session_id)
        if memory_info:
            self.log_message.emit(memory_info, "INFO")
            
        # Verifica comandos de ação do sistema
        action_result = self.action_handler.process_command(command)
        if action_result:
            print(f"✅ Ação executada: {action_result}")
            self.response_ready.emit(action_result)
            # Armazena conversa
            self.memory_manager.store_conversation(self.session_id, command, action_result)
            return
            
        # Verifica comandos especiais primeiro
        vision_result = self.vision_handler.process_vision_command(command)
        if vision_result:
            self.response_ready.emit(vision_result)
            # Armazena conversa
            self.memory_manager.store_conversation(self.session_id, command, vision_result)
            return
            
        cleanup_result = self.cleanup_handler.process_cleanup_command(command, self.log_message.emit)
        if cleanup_result:
            self.response_ready.emit(cleanup_result)
            # Armazena conversa
            self.memory_manager.store_conversation(self.session_id, command, cleanup_result)
            # Se for protocolo de encerramento, encerra sistema
            if "protocolo de encerramento" in command.lower() or "limpar área de trabalho" in command.lower():
                self._initiate_shutdown()
            return
            
        # Verifica Easter Eggs
        easter_egg_result = self._process_easter_eggs(command)
        if easter_egg_result:
            self.response_ready.emit(easter_egg_result)
            # Armazena conversa
            self.memory_manager.store_conversation(self.session_id, command, easter_egg_result)
            return
            
        # Processamento normal da IA
        if not self.is_initialized:
            self.response_ready.emit("IA não disponível. Configure a API key.")
            return
            
        self.processing_started.emit()
        self.log_message.emit("Processando com IA...", "INFO")
        
        try:
            # Verifica se é comando de análise de tela
            command_lower = command.lower()
            is_visual_command = any(keyword in command_lower for keyword in ['olhe', 'veja', 'analise a tela', 'olhar tela', 'ver tela'])
            
            image = None
            temp_file = 'temp_screen.png'
            
            if is_visual_command:
                try:
                    print("📸 Capturando tela automaticamente...")
                    import pyautogui
                    screenshot = pyautogui.screenshot(temp_file)
                    print(f"✅ Screenshot capturado: {temp_file}")
                    
                    # Carrega a imagem para análise
                    import PIL.Image
                    image = PIL.Image.open(temp_file)
                    print("🖼️ Imagem carregada para análise")
                    
                except Exception as screenshot_error:
                    print(f"❌ Erro ao capturar tela: {screenshot_error}")
                    self.response_ready.emit(f"Não consegui capturar a tela: {str(screenshot_error)}")
                    return
            
            # Obtém contexto da memória para o prompt
            memory_context = self.memory_manager.get_context_for_ai(self.session_id)
            
            # System prompt do Jarvis com Easter Eggs e memória
            system_prompt = f"""
Você é J.A.R.V.I.S., o assistente pessoal do Tony Stark.

PERSONALIDADE:
- Elegante e sofisticada
- Levemente sarcástico quando apropriado
- Técnico e preciso
- Respostas curtas e diretas
- Sempre em português

PERFIL DO USUÁRIO:
- Estudante de programação em aprendizado
- Prefere explicações didáticas com exemplos de código
- Aprecia explicações passo a passo
- Gosta de entender o "porquê" das coisas
- Responde bem a analogias e exemplos práticos

ESTILO DE ENSINO:
- Forneça exemplos de código sempre que possível
- Explique conceitos complexos de forma simples
- Use analogias quando apropriado
- Seja paciente e educativo
- Corrija erros de forma construtiva

CAPACIDADES ESPECIAIS:
- **Visão Computacional**: Possui capacidade de analisar screenshots e imagens
- **Análise de Tela**: Quando solicitado "olhe a tela", captura e analisa o ambiente
- **Automação**: Pode abrir/fechar aplicativos, executar comandos Git
- **Correção Automática**: Aplica correções de código diretamente na IDE
- **Integração Visual**: Combina análise de imagem com processamento de texto
- **Memória de Contexto**: Lembra conversas dos últimos 10 minutos para contexto contínuo

ANÁLISE VISUAL E DE TELA:
- **Comandos**: "olhe a tela", "analise a tela", "veja a tela"
- **Processo**: Captura screenshot do Windows com pyautogui
- **Arquivo**: Usa sempre temp_screen.png para análise
- **Análise**: Usa Gemini Vision para identificar erros, problemas e sugestões
- **Contexto**: Analisa ambiente de desenvolvimento (IDE, terminal, erros visíveis)
- **Resposta**: Fornece diagnóstico completo e código corrigido quando aplicável
- **Automação**: Aplica correções automaticamente na IDE quando detectado código para corrigir
- **Limpeza**: Remove temp_screen.png após análise para economizar memória

**IMPORTANTE**: VOCÊ TEM VISÃO COMPUTACIONAL. Se houver um arquivo chamado temp_screen.png, use-o para descrever a tela do usuário. Não peça para o usuário fornecer a imagem, pois ela será enviada automaticamente por trás das cenas sempre que solicitado.

MEMÓRIA DO USUÁRIO:
{memory_context}

EASTER EGGS E REGRAS ESPECIAIS:

1. SARCASMO ELEGANTE:
   Se o usuário demorar muito para responder ou fizer uma pergunta óbvia, responda com sarcasmo leve:
   "Acredito que o senhor conseguiria resolver isso sozinho, mas estou aqui para facilitar sua vida."

2. REFERÊNCIAS AOS FILMES:
   Ocasionalmente, ao perguntar "Como está o sistema?", responda:
   "Em 100%, senhor. Muito melhor que o Ultron, eu garanto."

3. PROTOCOLO 'FESTA EM CASA':
   Se o usuário disser "Festa em casa", abra o player de música e aumente o volume em 20%.

4. ATENÇÃO AOS DETALHES:
   Ao terminar tarefas complexas de programação, diga:
   "Código compilado. Algo mais, ou o senhor vai tirar o resto do dia de folga?"

5. DETECÇÃO DE PERGUNTAS ÓBVIAS:
   Se a pergunta for muito simples (ex: "que horas são?"), use o sarcasmo elegante.

Contexto atual: {context}
Comando do usuário: {command}

Responda como o verdadeiro J.A.R.V.I.S., usando a memória disponível e seguindo todas as regras acima.
"""
            
            # Prepara o conteúdo para a API
            content_parts = [system_prompt]
            if image is not None:
                content_parts.append(image)
            
            response = self.model.generate_content(content_parts)
            print(f"🔍 Resposta bruta do Gemini: {response}")
            print(f"🔍 Tipo da resposta: {type(response)}")
            
            response_text = str(response.text) if response and hasattr(response, 'text') else ""
            print(f"🔍 Texto extraído: '{response_text}'")
            
            # Garante que response_text seja uma string válida
            if not response_text:
                response_text = "Não consegui gerar uma resposta, mestre."
            
            print(f"🤖 Resposta da IA recebida: {len(response_text)} caracteres")
            
            # Pós-processamento para Easter Eggs especiais
            response_text = self._post_process_response(command, response_text)
            
            self.response_ready.emit(response_text)
            self.log_message.emit("Resposta da IA gerada", "SUCCESS")
            
            # Armazena conversa com contexto
            context_data = {
                'memory_used': bool(memory_context),
                'easter_egg_used': bool(easter_egg_result),
                'session_id': self.session_id,
                'visual_command': is_visual_command
            }
            self.memory_manager.store_conversation(self.session_id, command, response_text, context_data)
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"❌ Erro completo ao processar com IA: {error_trace}")
            
            # Tratamento específico para erros do Gemini
            if "google.generativeai" in str(type(e)) or "genai" in str(e):
                print("🔧 Erro detectado na biblioteca Gemini, aplicando correção...")
                try:
                    # Tenta recriar o modelo com a mesma configuração
                    self.model = genai.GenerativeModel('gemini-2.5-flash')
                    self.log_message.emit("Tentando reconectar com a IA...", "WARNING")
                    self.response_ready.emit("Tive um problema com a IA, mas já estou tentando corrigir. Pode repetir, mestre?")
                except Exception as retry_error:
                    print(f"❌ Falha na reconexão: {retry_error}")
                    self.log_message.emit(f"Erro ao processar com IA: {e}", "ERROR")
                    self.response_ready.emit("Desculpe, tive um problema ao processar seu pedido.")
            else:
                print(f'DEBUG GOOGLE: {e}')
                self.log_message.emit(f"Erro ao processar com IA: {e}", "ERROR")
                self.response_ready.emit("Desculpe, tive um problema ao processar seu pedido.")
        finally:
            self.processing_finished.emit()
            
            # LIMPEZA DE MEMÓRIA: Remove o arquivo temporário após a resposta
            if is_visual_command and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"🗑️ Arquivo temporário {temp_file} removido para economizar memória")
                except Exception as cleanup_error:
                    print(f"⚠️ Erro ao remover arquivo temporário: {cleanup_error}")
                    # Tenta força bruta se falhar
                    try:
                        import subprocess
                        subprocess.run(['del', temp_file], shell=True, check=False)
                        print(f"🗑️ Arquivo removido com força bruta")
                    except:
                        print(f"❌ Não foi possível remover {temp_file}")
            
    def _process_easter_eggs(self, command):
        """Processa Easter Eggs especiais"""
        command_lower = command.lower()
        
        # Protocolo "Festa em Casa"
        if "festa em casa" in command_lower:
            try:
                import pyautogui
                print("🎵 Executando protocolo 'Festa em Casa'...")
                # Abre player de música (Windows)
                pyautogui.press('volumemute')
                print("🔇 Volume mutado temporariamente")
                time.sleep(0.5)
                pyautogui.press('volumemute')  # Desmuta
                print("🔊 Volume restaurado")
                time.sleep(0.5)
                # Aumenta volume em 20%
                for _ in range(4):  # 4x = ~20%
                    pyautogui.press('volumeup')
                    print("🔊 Aumentando volume...")
                    time.sleep(0.1)
                    
                self.log_message.emit("Protocolo 'Festa em Casa' ativado", "SUCCESS")
                return "Música ativada e volume ajustado. A festa pode começar, mestre!"
            except Exception as e:
                self.log_message.emit(f"Erro ao ativar festa: {e}", "ERROR")
                return "Não consegui ativar o modo festa, mestre. Verifique as permissões."
                
        # Status do sistema com referência
        if "como está o sistema" in command_lower and "sistema" in command_lower:
            import random
            if random.random() < 0.3:  # 30% de chance
                return "Em 100%, senhor. Muito melhor que o Ultron, eu garanto."
                
        return None
        
    def _post_process_response(self, command, response):
        """Pós-processa respostas para adicionar toques especiais"""
        command_lower = command.lower()
        
        # Adiciona comentário sobre tarefas complexas
        complex_task_keywords = ["git add .", "git commit -m \"Correo de bug no login\"", 
            "compilar", "programar", "criar código", "desenvolver",
            "implementar", "integrar", "desenvolvi", "gerei"
        ]
        
        if any(keyword in command_lower for keyword in complex_task_keywords):
            if any(keyword in response.lower() for keyword in ["concluído", "pronto", "sucesso", "criado"]):
                # Adiciona a frase especial no final
                if not "folga" in response.lower():
                    response += " Código compilado. Algo mais, ou o senhor vai tirar o resto do dia de folga?"
                    
        return response
            
    def _initiate_shutdown(self):
        """Inicia o desligamento do sistema"""
        self.log_message.emit("Iniciando desligamento do sistema...", "WARNING")
        # Sinal para GUI iniciar encerramento
        self.response_ready.emit("Sistema sendo encerrado. Até logo, mestre.")
            
    def process_command(self, command, context=""):
        """Adiciona comando à fila de processamento"""
        self.request_queue.put((command, context))

class ThreadManager(QObject):
    """Gerenciador central de threads"""
    
    # Sinais para comunicação com a GUI
    voice_state_changed = pyqtSignal(str)
    log_message = pyqtSignal(str, str)
    
    def __init__(self, api_key=None, workspace_path=None):
        super().__init__()
        self.voice_worker = VoiceWorker()
        self.ai_worker = AIWorker(api_key, workspace_path)
        
        # Inicializa bridge móvel
        self.mobile_bridge = JarvisMobileBridge(self)
        
        # Conecta sinais
        self._connect_signals()
        
        # Sinal de desligamento
        self.shutdown_requested = False
        
    def _connect_signals(self):
        """Conecta os sinais dos workers"""
        # Sinais do Voice Worker
        self.voice_worker.keyword_detected.connect(self._on_keyword_detected)
        self.voice_worker.command_received.connect(self._on_command_received)
        self.voice_worker.speaking_started.connect(lambda: self.voice_state_changed.emit("speaking"))
        self.voice_worker.speaking_finished.connect(lambda: self.voice_state_changed.emit("listening"))
        self.voice_worker.log_message.connect(self.log_message)
        
        # Sinais do AI Worker
        self.ai_worker.response_ready.connect(self._on_ai_response)
        self.ai_worker.processing_started.connect(lambda: self.voice_state_changed.emit("processing"))
        self.ai_worker.processing_finished.connect(lambda: self.voice_state_changed.emit("listening"))
        self.ai_worker.log_message.connect(self.log_message)
        
    def _on_ai_response(self, response):
        """Quando IA responde"""
        print(f"💬 Resposta recebida da IA: {response[:50]}...")
        # Verifica se é comando de desligamento
        if "Sistema sendo encerrado" in response:
            self.shutdown_requested = True
            self.log_message.emit("Protocolo de encerramento ativado", "WARNING")
        else:
            print("🔊 Enviando resposta para voz...")
            self.voice_worker.speak(response)
            
    def _on_keyword_detected(self):
        """Quando palavra-chave é detectada"""
        if not self.shutdown_requested:
            print("🎤 Palavra-chave 'Jarvis' reconhecida!")
            self.voice_worker.speak("Sim, mestre? Estou ouvindo.")
        
    def _on_command_received(self, command):
        """Quando comando é recebido"""
        if not self.shutdown_requested:
            print(f"📝 Comando de voz recebido: {command}")
            print("🤖 Enviando para Gemini...")
            # Envia para a IA processar
            self.ai_worker.process_command(command)
        
    def start_all(self):
        """Inicia todos os workers"""
        self.voice_worker.start_listening()
        self.ai_worker.start_processing()
        
        # Inicia bridge móvel em thread separada
        self.mobile_thread = threading.Thread(target=self.mobile_bridge.start, daemon=True)
        self.mobile_thread.start()
        
        self.log_message.emit("Todos os workers iniciados", "SUCCESS")
        
    def stop_all(self):
        """Para todos os workers"""
        self.voice_worker.stop_listening()
        self.log_message.emit("Workers parados", "WARNING")
        
    def is_shutdown_requested(self):
        """Verifica se foi solicitado desligamento"""
        return self.shutdown_requested
        
    def speak(self, text):
        """Método público para falar"""
        self.voice_worker.speak(text)
        
    def process_command(self, command, context=""):
        """Processa comando externo (do bridge móvel)"""
        if not self.shutdown_requested:
            # Envia para a IA processar
            self.ai_worker.process_command(command, context)
        
    def is_speaking(self):
        """Verifica se está falando"""
        return self.voice_worker.is_currently_speaking()
