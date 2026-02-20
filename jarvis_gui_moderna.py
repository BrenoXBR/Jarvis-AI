#!/usr/bin/env python3
"""
Interface Moderna para o Jarvis com CustomTkinter
Dark Mode com campo de chat e botão de ouvinte estilizado
"""

import customtkinter as ctk
import threading
import queue
import time
from datetime import datetime
import sys
import os

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JarvisGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🤖 J.A.R.V.I.S. - Assistente Inteligente")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Fila de mensagens para thread-safe
        self.message_queue = queue.Queue()
        
        # Estado da aplicação
        self.is_listening = False
        self.is_processing = False
        
        # Histórico de conversas
        self.chat_history = []
        
        self.setup_ui()
        self.setup_styles()
        
    def setup_styles(self):
        """Configura estilos personalizados"""
        # Cor de fundo principal
        self.root.configure(fg_color=("#1a1a1a", "#1a1a1a"))
        
    def setup_ui(self):
        """Monta a interface principal"""
        
        # Container principal
        main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header com título
        header_frame = ctk.CTkFrame(main_frame, height=60)
        header_frame.pack(fill="x", padx=10, pady=(10, 20))
        header_frame.pack_propagate(False)
        
        # Título estilizado
        title_font = ctk.CTkFont(family="Arial", size=24, weight="bold")
        title_label = ctk.CTkLabel(
            header_frame,
            text="🤖 J.A.R.V.I.S.",
            font=title_font,
            text_color=("#00ff88", "#00ff88")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Status indicator
        status_font = ctk.CTkFont(family="Arial", size=14)
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="🔴 Offline",
            font=status_font,
            text_color=("#ff4444", "#ff4444")
        )
        self.status_label.pack(side="right", padx=20, pady=15)
        
        # Área de chat
        chat_frame = ctk.CTkFrame(main_frame)
        chat_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        # Scrollable text box para mensagens
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            wrap="word",
            activate_scrollbars=True
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Área de input
        input_frame = ctk.CTkFrame(main_frame, height=80)
        input_frame.pack(fill="x", padx=10)
        input_frame.pack_propagate(False)
        
        # Campo de texto
        self.text_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Digite seu comando ou fale com o Jarvis...",
            height=40
        )
        self.text_input.pack(side="left", fill="both", expand=True, padx=(10, 10), pady=20)
        
        # Bind para Enter
        self.text_input.bind("<Return>", self.send_message)
        
        # Botão de ouvir estilizado
        self.listen_button = ctk.CTkButton(
            input_frame,
            text="🎤 Ouvir",
            width=120,
            height=40,
            fg_color=("#00ff88", "#00cc66"),
            hover_color=("#00cc66", "#00aa55"),
            text_color=("#000000", "#000000"),
            command=self.toggle_listening
        )
        self.listen_button.pack(side="right", padx=(0, 10), pady=20)
        
        # Botão de enviar
        self.send_button = ctk.CTkButton(
            input_frame,
            text="📤 Enviar",
            width=100,
            height=40,
            command=self.send_message
        )
        self.send_button.pack(side="right", padx=(0, 10), pady=20)
        
        # Mensagem inicial
        self.add_message("Jarvis", "👋 Olá! Sou o J.A.R.V.I.S., seu assistente pessoal. Como posso ajudar você hoje?", is_jarvis=True)
        
    def toggle_listening(self):
        """Alterna o estado de escuta"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Inicia o modo de escuta"""
        self.is_listening = True
        self.listen_button.configure(
            text="⏹️ Parar",
            fg_color=("#ff4444", "#cc3333"),
            hover_color=("#cc3333", "#aa2222")
        )
        self.status_label.configure(
            text="🟢 Ouvindo...",
            text_color=("#00ff88", "#00ff88")
        )
        
        # Simulação de escuta (em produção, aqui viria o reconhecimento de voz)
        self.add_message("Sistema", "🎤 Modo de escuta ativado. Fale claramente...", is_system=True)
        
        # Thread para simulação
        threading.Thread(target=self.simulate_listening, daemon=True).start()
    
    def stop_listening(self):
        """Para o modo de escuta"""
        self.is_listening = False
        self.listen_button.configure(
            text="🎤 Ouvir",
            fg_color=("#00ff88", "#00cc66"),
            hover_color=("#00cc66", "#00aa55")
        )
        self.status_label.configure(
            text="🔴 Offline",
            text_color=("#ff4444", "#ff4444")
        )
        self.add_message("Sistema", "⏹️ Modo de escuta desativado.", is_system=True)
    
    def simulate_listening(self):
        """Simula o processo de escuta (placeholder para integração real)"""
        time.sleep(2)
        if self.is_listening:
            self.add_message("Jarvis", "🔊 Detectado: 'Olá Jarvis, como você está?'", is_jarvis=True)
            time.sleep(1)
            self.add_message("Jarvis", "✨ Estou funcionando perfeitamente! Pronto para ajudar com suas tarefas de programação.", is_jarvis=True)
            self.stop_listening()
    
    def send_message(self, event=None):
        """Envia mensagem digitada"""
        message = self.text_input.get().strip()
        if not message:
            return
        
        # Limpa o campo
        self.text_input.delete(0, "end")
        
        # Adiciona mensagem do usuário
        self.add_message("Você", message, is_user=True)
        
        # Simula resposta do Jarvis (em produção, aqui viria a chamada à API)
        self.simulate_jarvis_response(message)
    
    def simulate_jarvis_response(self, user_message):
        """Simula resposta do Jarvis (placeholder para integração real)"""
        self.is_processing = True
        self.status_label.configure(
            text="🟡 Processando...",
            text_color=("#ffaa00", "#ffaa00")
        )
        
        # Thread para simular processamento
        def process_and_respond():
            time.sleep(1.5)  # Simula tempo de processamento
            
            responses = {
                "ajuda": "🔧 Posso ajudar com: análise de código, modo gamer, memória de longo prazo, debugger assistido e muito mais!",
                "olá": "👋 Olá! Como posso ajudar em sua jornada de programação hoje?",
                "tchau": "👋 Até logo! Estarei aqui quando precisar.",
                "modo gamer": "🎮 Ativando modo gamer! Abrindo Discord, Opera GX e Steam...",
                "analise": "👁️ Vou analisar sua tela. Deixe-me capturar o que está acontecendo...",
            }
            
            # Resposta padrão
            response = responses.get(user_message.lower(), f"🤖 Recebi seu comando: '{user_message}'. Estou processando e em breve terei uma resposta para você!")
            
            # Adiciona resposta na thread principal
            self.root.after(0, lambda: self.add_message("Jarvis", response, is_jarvis=True))
            self.root.after(0, lambda: self.status_label.configure(text="🟢 Online", text_color=("#00ff88", "#00ff88")))
            self.root.after(0, lambda: setattr(self, 'is_processing', False))
        
        threading.Thread(target=process_and_respond, daemon=True).start()
    
    def add_message(self, sender, message, is_user=False, is_jarvis=False, is_system=False):
        """Adiciona mensagem ao chat com formatação"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Define cores baseadas no remetente
        if is_user:
            prefix = f"👤 [{timestamp}] Você:"
            color = "#00aaff"
        elif is_jarvis:
            prefix = f"🤖 [{timestamp}] Jarvis:"
            color = "#00ff88"
        elif is_system:
            prefix = f"⚙️ [{timestamp}] Sistema:"
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
