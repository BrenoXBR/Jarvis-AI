#!/usr/bin/env python3
"""
Teste para verificar se as respostas completas estão funcionando
"""

import customtkinter as ctk
import threading
import time
from datetime import datetime

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

class TestResponseApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🤖 Teste de Resposta Completa")
        self.root.geometry("700x500")
        self.root.configure(fg_color=STARK_COLORS["background"])
        
        # Estado da aplicação
        self.is_processing = False
        self.current_response = None  # Armazena resposta completa
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura interface de teste"""
        
        # Título
        title_font = ctk.CTkFont(family="Consolas", size=18, weight="bold")
        title = ctk.CTkLabel(
            self.root,
            text="🤖 TESTE DE RESPOSTA COMPLETA",
            font=title_font,
            text_color=STARK_COLORS["ia_text"]
        )
        title.pack(pady=20)
        
        # Container principal
        main_frame = ctk.CTkFrame(
            self.root, 
            corner_radius=10, 
            border_color=STARK_COLORS["border"], 
            fg_color=STARK_COLORS["component_bg"]
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Área de chat
        chat_frame = ctk.CTkFrame(main_frame, border_color=STARK_COLORS["border"], fg_color=STARK_COLORS["component_bg"])
        chat_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        chat_font = ctk.CTkFont(family="Consolas", size=12)
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=chat_font,
            wrap="word",
            activate_scrollbars=True
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Área de input
        input_frame = ctk.CTkFrame(main_frame, border_color=STARK_COLORS["border"], fg_color=STARK_COLORS["component_bg"])
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Botões de teste
        button_font = ctk.CTkFont(family="Consolas", size=12, weight="bold")
        
        # Botão de resposta curta
        short_btn = ctk.CTkButton(
            input_frame,
            text="📝 Resposta Curta",
            font=button_font,
            fg_color=STARK_COLORS["button_normal"],
            hover_color=STARK_COLORS["button_hover"],
            text_color=STARK_COLORS["button_text"],
            command=self.test_short_response
        )
        short_btn.pack(side="left", padx=5, pady=10)
        
        # Botão de resposta longa
        long_btn = ctk.CTkButton(
            input_frame,
            text="📄 Resposta Longa",
            font=button_font,
            fg_color=STARK_COLORS["button_normal"],
            hover_color=STARK_COLORS["button_hover"],
            text_color=STARK_COLORS["button_text"],
            command=self.test_long_response
        )
        long_btn.pack(side="left", padx=5, pady=10)
        
        # Botão de resposta muito longa
        very_long_btn = ctk.CTkButton(
            input_frame,
            text="📚 Resposta Muito Longa",
            font=button_font,
            fg_color=STARK_COLORS["button_normal"],
            hover_color=STARK_COLORS["button_hover"],
            text_color=STARK_COLORS["button_text"],
            command=self.test_very_long_response
        )
        very_long_btn.pack(side="left", padx=5, pady=10)
        
        # Mensagem inicial
        self.add_message("Sistema", "🧪 Interface de teste para respostas completas. Clique nos botões para testar diferentes tamanhos de resposta.", is_system=True)
        
    def test_short_response(self):
        """Testa resposta curta"""
        response = "Esta é uma resposta curta para teste."
        self.simulate_api_response(response)
        
    def test_long_response(self):
        """Testa resposta longa"""
        response = """Esta é uma resposta longa para teste do sistema. 
Ela contém múltiplos parágrafos para verificar se o typewriter 
consegue processar textos completos sem cortar no meio. 
A resposta deve ser exibida por completo na interface, 
mantendo toda a formatação e conteúdo original. 
Este teste ajuda a identificar problemas com variáveis 
sendo limpas antes da animação terminar."""
        self.simulate_api_response(response)
        
    def test_very_long_response(self):
        """Testa resposta muito longa"""
        response = """Esta é uma resposta muito longa para teste do sistema. 
Ela contém muitos parágrafos para verificar se o typewriter 
consegue processar textos extensos sem cortar no meio. 

**Parágrafo 1**: O sistema deve manter a resposta completa em memória 
durante toda a animação do typewriter, sem perder caracteres 
ou truncar o conteúdo devido a conflitos com o mainloop.

**Parágrafo 2**: A variável current_response deve armazenar a resposta 
completa e a função typewriter_effect deve usar esta variável 
para garantir persistência durante o loop de animação.

**Parágrafo 3**: Testamos também se o aumento do max_output_tokens 
para 4096 resolve problemas de respostas sendo cortadas pela API 
do Gemini quando executado pelo arquivo .bat.

**Parágrafo 4**: O tratamento de erro robusto deve capturar qualquer 
problema e exibir a mensagem completa mesmo que ocorra uma 
exceção durante o processo de animação.

**Conclusão**: Esta resposta deve aparecer completamente na interface 
sem nenhum corte ou truncamento, provando que as correções 
implementadas resolveram o problema."""
        self.simulate_api_response(response)
        
    def simulate_api_response(self, response):
        """Simula resposta da API"""
        self.is_processing = True
        
        def process():
            # Simula tempo de processamento
            time.sleep(0.5)
            
            # Armazena resposta completa
            self.current_response = response
            
            print(f"✅ Resposta simulada: {len(response)} caracteres")
            
            # Inicia typewriter
            self.root.after(0, lambda: self.typewriter_effect("Teste", self.current_response))
            
            # Finaliza processamento
            time.sleep(2)
            self.is_processing = False
        
        threading.Thread(target=process, daemon=True).start()
        
    def typewriter_effect(self, sender, message):
        """Efeito typewriter para mensagens"""
        if not message or not isinstance(message, str):
            self.add_message("Sistema", "❌ Mensagem inválida", is_system=True)
            return
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"🤖 [{timestamp}] {sender}:"
        
        # Adiciona prefixo
        self.chat_display.insert("end", f"{prefix}\n", "prefix_test")
        self.chat_display.tag_config("prefix_test", foreground=STARK_COLORS["ia_text"])
        
        # Armazena mensagem completa
        complete_message = str(message)
        self.current_response = complete_message
        
        def add_char_by_char():
            try:
                message_to_type = self.current_response
                
                for i, char in enumerate(message_to_type):
                    if not self.is_processing:
                        remaining_text = message_to_type[i:]
                        self.chat_display.insert("end", remaining_text, "message_test")
                        break
                    
                    self.chat_display.insert("end", char, "message_test")
                    self.chat_display.see("end")
                    self.root.update()
                    time.sleep(0.01)  # Mais rápido para teste
                    
            except Exception as e:
                print(f"❌ Erro no typewriter: {e}")
                self.chat_display.insert("end", complete_message, "message_test")
            finally:
                self.chat_display.tag_config("message_test", foreground=STARK_COLORS["ia_text"])
                self.chat_display.insert("end", "\n\n", "message_test")
        
        threading.Thread(target=add_char_by_char, daemon=True).start()
        
    def add_message(self, sender, message, is_user=False, is_system=False):
        """Adiciona mensagem ao chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if is_user:
            prefix = f"👤 [{timestamp}] Você:"
            color = "#00aaff"
        elif is_system:
            prefix = f"⚙️ [{timestamp}] {sender}:"
            color = "#ffaa00"
        else:
            prefix = f"[{timestamp}] {sender}:"
            color = STARK_COLORS["ia_text"]
        
        self.chat_display.insert("end", f"{prefix}\n", f"prefix_{sender}")
        self.chat_display.insert("end", f"{message}\n\n", f"message_{sender}")
        
        self.chat_display.tag_config(f"prefix_{sender}", foreground=color)
        self.chat_display.tag_config(f"message_{sender}", foreground="#ffffff")
        
        self.chat_display.see("end")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TestResponseApp()
    app.run()
