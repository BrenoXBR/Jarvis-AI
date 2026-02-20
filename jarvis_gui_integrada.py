#!/usr/bin/env python3
"""
Interface Integrada do Jarvis com todos os módulos
Dark Mode com integração completa: Memória, Gemini, Voz e Visão
"""

import customtkinter as ctk
import threading
import queue
import time
from datetime import datetime
import sys
import os
import sqlite3
import json
import pyautogui
import tempfile
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3

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
            db_path = os.path.join(os.getcwd(), 'jarvis_memory.db')
        self.db_path = db_path
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao inicializar memória: {e}")
    
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
        load_dotenv()
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if self.api_key and self.api_key != 'sua_chave_api_aqui':
            try:
                genai.configure(api_key=self.api_key)
                self.vision_model = genai.GenerativeModel('gemini-pro-vision')
                self.vision_enabled = True
            except Exception as e:
                print(f"Erro ao inicializar visão: {e}")
                self.vision_enabled = False
        else:
            self.vision_enabled = False
    
    def capture_and_analyze(self):
        """Captura e analisa a tela"""
        if not self.vision_enabled:
            return "❌ Visão computacional não está disponível. Verifique sua API key."
        
        try:
            # Captura tela
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_file = f"temp_screen_{timestamp}.png"
            pyautogui.screenshot(temp_file)
            
            # Analisa com Gemini
            try:
                with Image.open(temp_file) as img:
                    response = self.vision_model.generate_content([
                        "Analise esta tela descrevendo o que você vê. Se houver código, erros ou algo relevante, descreva detalhadamente.",
                        img
                    ])
                    result = response.text
                
                # Remove arquivo temporário
                os.remove(temp_file)
                return result
                
            except Exception as e:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
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
        self.vision = JarvisVision()
        self.setup_voice()
        
        # Estado da aplicação
        self.is_listening = False
        self.is_processing = False
        self.progress_animation_active = False
        
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
        """Monta a interface principal"""
        
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
        
        # Área de chat
        chat_frame = ctk.CTkFrame(main_frame, border_color=STARK_COLORS["border"], fg_color=STARK_COLORS["component_bg"])
        chat_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        # Scrollable text box para mensagens
        chat_font = ctk.CTkFont(family="Consolas", size=12)
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=chat_font,
            wrap="word",
            activate_scrollbars=True
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Área de input e botões
        input_frame = ctk.CTkFrame(main_frame, height=100, border_color=STARK_COLORS["border"], fg_color=STARK_COLORS["component_bg"])
        input_frame.pack(fill="x", padx=10)
        input_frame.pack_propagate(False)
        
        # Campo de texto
        input_font = ctk.CTkFont(family="Consolas", size=14)
        self.text_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Digite seu comando ou fale com o Jarvis...",
            font=input_font,
            height=40,
            border_color=STARK_COLORS["border"],
            fg_color=STARK_COLORS["component_bg"]
        )
        self.text_input.pack(side="left", fill="both", expand=True, padx=(10, 10), pady=(10, 5))
        
        # Bind para Enter
        self.text_input.bind("<Return>", self.send_message)
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(
            input_frame,
            width=200,
            height=4,
            progress_color=STARK_COLORS["button_normal"],
            fg_color=STARK_COLORS["component_bg"],
            border_color=STARK_COLORS["border"]
        )
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=(0, 10))
        self.progress_bar.set(0)  # Inicia oculta
        
        # Container de botões
        button_container = ctk.CTkFrame(input_frame, border_color=STARK_COLORS["border"], fg_color=STARK_COLORS["component_bg"])
        button_container.pack(side="right", padx=(0, 10), pady=(10, 5))
        
        # Botão de visão
        self.vision_button = ctk.CTkButton(
            button_container,
            text="👁️",
            width=50,
            height=40,
            border_color=STARK_COLORS["border"],
            fg_color=STARK_COLORS["component_bg"],
            hover_color=STARK_COLORS["button_hover"],
            command=self.capture_and_analyze_screen
        )
        self.vision_button.pack(side="left", padx=(0, 5))
        
        # Botão de ouvir
        self.listen_button = ctk.CTkButton(
            button_container,
            text="🎤 Ouvir",
            width=100,
            height=40,
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
            border_color=STARK_COLORS["border"],
            fg_color=STARK_COLORS["button_normal"],
            hover_color=STARK_COLORS["button_hover"],
            text_color=STARK_COLORS["button_text"],
            command=self.send_message
        )
        self.send_button.pack(side="left", padx=5)
        
        # Mensagem inicial
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
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Reconhece o áudio
            try:
                text = self.recognizer.recognize_google(audio, language='pt-BR')
                self.root.after(0, lambda: self.process_voice_command(text))
            except sr.UnknownValueError:
                self.root.after(0, lambda: self.add_message("Sistema", "🔇 Não consegui entender. Fale novamente.", is_system=True))
            except sr.RequestError as e:
                self.root.after(0, lambda: self.add_message("Sistema", f"❌ Erro no reconhecimento: {e}", is_system=True))
                
        except Exception as e:
            self.root.after(0, lambda: self.add_message("Sistema", f"❌ Erro na escuta: {e}", is_system=True))
        finally:
            self.root.after(0, self.stop_listening)
    
    def process_voice_command(self, text):
        """Processa comando de voz"""
        self.add_message("Você", text, is_user=True)
        self.process_with_gemini(text)
    
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
        """Processa mensagem com Gemini e exibe com efeito typewriter"""
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
                # Contexto da memória
                memories = self.memory.get_recent_memories(3)
                memory_context = "\n".join([f"- {mem[0]}" for mem in memories]) if memories else ""
                
                # Prompt com contexto
                prompt = f"""Você é J.A.R.V.I.S., assistente de programação. 
                
Memórias recentes:
{memory_context}

Comando do usuário: {message}

Responda de forma útil, educativa e técnica. Se for sobre programação, forneça exemplos de código quando relevante."""
                
                # Chamada à API com configuração otimizada
                model = genai.GenerativeModel(
                    'gemini-2.5-flash',
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=2048,
                        temperature=0.7,
                        stop_sequences=None,  # Remove stop sequences para não cortar
                        candidate_count=1
                    )
                )
                response = model.generate_content(prompt)
                full_response = response.text
                
                # Verifica se a resposta foi truncada
                if len(full_response) < 10:
                    print(f"⚠️ Resposta curta detectada: {len(full_response)} caracteres")
                elif len(full_response) >= 2040:
                    print(f"⚠️ Resposta pode estar truncada: {len(full_response)} caracteres")
                
                print(f"✅ Resposta completa recebida: {len(full_response)} caracteres")
                
                # Efeito typewriter na thread principal
                # Garante que a resposta está completa antes de iniciar typewriter
                if full_response and len(full_response.strip()) > 0:
                    self.root.after(0, lambda: self.typewriter_effect("Jarvis", full_response))
                else:
                    self.root.after(0, lambda: self.add_message("Jarvis", "❌ Resposta vazia recebida", is_jarvis=True))
                
                # Salva na memória
                self.memory.add_memory(f"Usuário perguntou: {message}", "conversation")
                self.memory.add_memory(f"Jarvis respondeu: {full_response[:100]}...", "conversation")
                
            except Exception as e:
                error_msg = f"❌ Erro ao processar: {e}"
                self.root.after(0, lambda: self.add_message("Jarvis", error_msg, is_jarvis=True))
            finally:
                self.root.after(0, lambda: self.status_label.configure(text="🟢 Online", text_color=STARK_COLORS["ia_text"]))
                self.root.after(0, lambda: setattr(self, 'is_processing', False))
                self.root.after(0, lambda: self.stop_progress_animation())
        
        threading.Thread(target=process_and_respond, daemon=True).start()
    
    def typewriter_effect(self, sender, message):
        """Efeito typewriter para mensagens do Jarvis"""
        # Verifica se a mensagem é válida antes de processar
        if not message or not isinstance(message, str):
            self.add_message("Jarvis", "❌ Mensagem inválida para exibição", is_jarvis=True)
            return
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"🤖 [{timestamp}] {sender}:"
        
        # Adiciona prefixo
        self.chat_display.insert("end", f"{prefix}\n", "prefix_jarvis")
        self.chat_display.tag_config("prefix_jarvis", foreground=STARK_COLORS["ia_text"])
        
        # Armazena a mensagem completa para garantir processamento
        complete_message = str(message)  # Garante que é string
        
        # Efeito typewriter
        def add_char_by_char():
            try:
                for i, char in enumerate(complete_message):
                    # Verifica se ainda está processando antes de cada caractere
                    if not self.is_processing:
                        # Se interrompido, adiciona o resto da mensagem de uma vez
                        remaining_text = complete_message[i:]
                        self.chat_display.insert("end", remaining_text, "message_jarvis")
                        break
                    
                    self.chat_display.insert("end", char, "message_jarvis")
                    self.chat_display.see("end")
                    self.root.update()
                    time.sleep(0.02)  # Velocidade do typewriter
            except Exception as e:
                # Se der erro, adiciona a mensagem completa
                self.chat_display.insert("end", complete_message, "message_jarvis")
            finally:
                # Configura cor e adiciona espaçamento final
                self.chat_display.tag_config("message_jarvis", foreground=STARK_COLORS["ia_text"])
                self.chat_display.insert("end", "\n\n", "message_jarvis")
        
        # Executa em thread para não bloquear
        threading.Thread(target=add_char_by_char, daemon=True).start()
    
    def capture_and_analyze_screen(self):
        """Captura e analisa a tela"""
        self.add_message("Sistema", "📸 Capturando tela...", is_system=True)
        self.status_label.configure(
            text="👁️ Analisando...",
            text_color=STARK_COLORS["ia_text"]
        )
        
        # Inicia animação da barra de progresso
        self.start_progress_animation()
        
        # Thread para captura e análise
        def analyze():
            result = self.vision.capture_and_analyze()
            self.root.after(0, lambda: self.add_message("Jarvis", result, is_jarvis=True))
            self.root.after(0, lambda: self.status_label.configure(text="🟢 Online", text_color=STARK_COLORS["ia_text"]))
            self.root.after(0, lambda: self.stop_progress_animation())
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def add_message(self, sender, message, is_user=False, is_jarvis=False, is_system=False):
        """Adiciona mensagem ao chat com formatação"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Define cores baseadas no remetente
        if is_user:
            prefix = f"👤 [{timestamp}] Você:"
            color = "#00aaff"
        elif is_jarvis:
            prefix = f"🤖 [{timestamp}] {sender}:"
            color = STARK_COLORS["ia_text"]  # Azul Neon
        elif is_system:
            prefix = f"⚙️ [{timestamp}] {sender}:"
            color = "#ffaa00"
        else:
            prefix = f"[{timestamp}] {sender}:"
            color = "#ffffff"
        
        # Adiciona ao display
        self.chat_display.insert("end", f"{prefix}\n", f"prefix_{sender}")
        self.chat_display.insert("end", f"{message}\n\n", f"message_{sender}")
        
        # Configura cores
        self.chat_display.tag_config(f"prefix_{sender}", foreground=color)
        self.chat_display.tag_config(f"message_{sender}", foreground="#ffffff")
        
        # Auto-scroll
        self.chat_display.see("end")
        
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
        """Inicia a aplicação"""
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        app = JarvisGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Encerrando interface do Jarvis...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro ao iniciar interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
