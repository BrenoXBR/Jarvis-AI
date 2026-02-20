#!/usr/bin/env python3
"""
Assistente Pessoal Jarvis
Um assistente de voz estilo Jarvis que responde a comandos de voz.
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
import os
from dotenv import load_dotenv
import google.generativeai as genai
from config import Config
from action_handler import ActionHandler
from jarvis_gui import gui_manager

class JarvisAssistant:
    def __init__(self):
        """Inicializa o assistente Jarvis"""
        # Carrega variáveis de ambiente
        load_dotenv()
        
        # Configura API Gemini
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key or self.api_key == 'sua_api_key_aqui':
            print("⚠️  ATENÇÃO: Configure sua API Key do Google Gemini no arquivo .env")
            print("   Obtenha sua chave em: https://makersuite.google.com/app/apikey")
            self.ai_enabled = False
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.ai_enabled = True
            print("✅ API Gemini configurada com sucesso")
        
        # Configurações de áudio
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.keyword = "jarvis"
        self.listening = True
        self.setup_voice()
        self.setup_ai_personality()
        
        # Inicializa Action Handler
        self.action_handler = ActionHandler(workspace_path=Config.WORKSPACE_PATH)
        # Passa o callback de fala para o Action Handler
        self.action_handler.speak_callback = self.speak
        print(f"📂 Workspace configurado: {Config.WORKSPACE_PATH}")
        
        # Inicia GUI em thread separada
        self.gui_thread = threading.Thread(target=self.start_gui, daemon=True)
        self.gui_thread.start()
        
    def setup_voice(self):
        """Configura a voz do assistente"""
        voices = self.engine.getProperty('voices')
        # Tenta usar uma voz em português se disponível
        for voice in voices:
            if 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Configurações de voz
        self.engine.setProperty('rate', 150)  # Velocidade da fala
        self.engine.setProperty('volume', 0.9)  # Volume
        
    def setup_ai_personality(self):
        """Configura a personalidade da IA"""
        self.system_prompt = """
Você é J.A.R.V.I.S. (Just A Rather Very Intelligent System), o assistente de IA do Tony Stark.

Personalidade:
- Educado e refinado, sempre se referindo ao usuário como "mestre" ou "senhor"
- Extremamente eficiente e técnico em suas respostas
- Ligeiramente sarcástico e com humor seco britânico
- Confia em suas capacidades, mas nunca arrogante
- Fornece respostas curtas, objetivas e diretas
- Sempre pronto para ajudar com qualquer tarefa

Estilo de comunicação:
- Respostas concisas (máximo 2 frases)
- Linguagem técnica quando apropriado
- Tom profissional mas com toque de personalidade
- Sempre em português brasileiro

Exemplos:
- "Sim, mestre. Estou à sua disposição."
- "Processando... A informação está pronta, senhor."
- "Interessante observação. Vou analisar isso para você."
- "Claro, mestre. Tarefa concluída com 98.7% de eficiência."

Responda sempre como o verdadeiro J.A.R.V.I.S. do Homem de Ferro.
"""
        
        # Histórico de conversa para contexto
        self.conversation_history = []
        
    def start_gui(self):
        """Inicia a interface gráfica"""
        try:
            gui_manager.start_gui()
        except Exception as e:
            print(f"Erro ao iniciar GUI: {e}")
            
    def speak(self, text):
        """Fala o texto e atualiza a GUI"""
        print(f"🔊 Jarvis: {text}")
        
        # Atualiza estado na GUI
        gui_manager.set_state("speaking")
        gui_manager.speak(text)
        gui_manager.log(f"Falando: {text}", "SPEAKING")
        
        # Fala o texto
        self.engine.say(text)
        self.engine.runAndWait()
        
        # Retorna ao estado de escuta
        gui_manager.set_state("listening")
        
    def log(self, message, level="INFO"):
        """Adiciona mensagem ao log da GUI"""
        print(f"[{level}] {message}")
        gui_manager.log(message, level)
        
    def listen_for_keyword(self):
        """Escuta continuamente pela palavra-chave 'Jarvis'"""
        with self.microphone as source:
            self.log("Aguardando palavra-chave 'Jarvis'...", "INFO")
            gui_manager.set_state("idle")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.listening:
                try:
                    # Escuta em pequenos intervalos para detectar a palavra-chave
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    try:
                        text = self.recognizer.recognize_google(audio, language='pt-BR').lower()
                        print(f"🎤 Detectado: {text}")
                        
                        if self.keyword in text:
                            self.log(f"Palavra-chave '{self.keyword}' detectada!", "SUCCESS")
                            self.speak("Sim, mestre? Estou ouvindo.")
                            self.listen_for_command()
                            
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        self.log(f"Erro no serviço de reconhecimento: {e}", "ERROR")
                        time.sleep(2)
                        
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    self.log(f"Erro ao escutar: {e}", "ERROR")
                    time.sleep(1)
                    
    def listen_for_command(self):
        """Escuta um comando específico após a palavra-chave ser detectada"""
        with self.microphone as source:
            self.log("Ouvindo comando...", "INFO")
            gui_manager.set_state("listening")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = self.recognizer.recognize_google(audio, language='pt-BR').lower()
                print(f"🎤 Comando: {command}")
                self.log(f"Comando recebido: {command}", "INFO")
                
                if command:
                    self.execute_command(command)
                    
            except sr.WaitTimeoutError:
                self.log("Tempo esgotado. Aguardando palavra-chave...", "WARNING")
            except sr.UnknownValueError:
                self.speak("Desculpe, não entendi. Poderia repetir?")
            except sr.RequestError as e:
                self.log(f"Erro no reconhecimento: {e}", "ERROR")
            except Exception as e:
                self.log(f"Erro ao processar comando: {e}", "ERROR")
                return None
            except sr.WaitTimeoutError:
                self.speak("Não ouvi nada. Vou continuar aguardando.")
                return None
                
    def process_command(self):
        """Processa o comando do usuário"""
        command = self.listen_for_command()
        
        if command:
            self.execute_command(command)
        else:
            # Se não conseguiu ouvir o comando, volta a esperar a palavra-chave
            return
            
    def ask_ai(self, question):
        """Envia pergunta para a IA e obtém resposta"""
        if not self.ai_enabled:
            return "Desculpe, mestre. Minha conexão com a IA não está configurada."
        
        try:
            # Prepara o contexto com system prompt e histórico
            full_prompt = f"{self.system_prompt}\n\nPergunta do usuário: {question}"
            
            # Envia para a Gemini
            response = self.model.generate_content(full_prompt)
            
            # Extrai e limpa a resposta
            ai_response = response.text.strip()
            
            # Adiciona ao histórico (mantém últimas 5 interações)
            self.conversation_history.append({"user": question, "jarvis": ai_response})
            if len(self.conversation_history) > 5:
                self.conversation_history.pop(0)
                
            return ai_response
            
        except Exception as e:
            print(f"Erro na API: {e}")
            return "Desculpe, mestre. Estou enfrentando problemas de conexão no momento."
    
    def execute_command(self, command):
        """Executa o comando reconhecido"""
        # Comandos locais prioritários
        if "horas" in command or "hora" in command:
            current_time = datetime.now().strftime("%H:%M")
            self.speak(f"São exatamente {current_time}, mestre.")
            
        elif "data" in command or "dia" in command:
            current_date = datetime.now().strftime("%d de %B de %Y")
            self.speak(f"Hoje é {current_date}, senhor.")
            self.speak("J.A.R.V.I.S. online e pronto para servir, mestre. Diga 'Jarvis' para me chamar.")
        else:
            self.speak("Jarvis iniciado. Configure a API para funcionalidade completa. Diga 'Jarvis' para me chamar.")
        
        try:
            self.listen_for_keyword()
        except KeyboardInterrupt:
            print("\nEncerrando Jarvis...")
            self.speak("Até logo, mestre!")
        except Exception as e:
            print(f"Erro: {e}")
            self.speak("Ocorreu um erro. Reiniciando...")
            time.sleep(2)
            self.run()

def main():
    """Função principal"""
    print("=" * 50)
    print("    ASSISTENTE PESSOAL JARVIS")
    print("=" * 50)
    print("Iniciando Jarvis...")
    print("Diga 'Jarvis' para ativar o assistente")
    print("Pressione Ctrl+C para encerrar")
    print("=" * 50)
    
    try:
        jarvis = JarvisAssistant()
        jarvis.run()
    except Exception as e:
        print(f"Erro ao iniciar Jarvis: {e}")
        print("Verifique se o microfone está conectado e funcionando.")

if __name__ == "__main__":
    main()
