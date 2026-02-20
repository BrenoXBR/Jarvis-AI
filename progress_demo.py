#!/usr/bin/env python3
"""
Demonstração da Barra de Progresso Stark Industries
"""

import customtkinter as ctk
import threading
import time

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ProgressDemo:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🤖 Stark Industries - Barra de Progresso")
        self.root.geometry("500x300")
        
        # Aplicar fundo Stark Industries
        self.root.configure(fg_color="#0B0E14")
        
        self.progress_animation_active = False
        self.setup_demo()
        
    def setup_demo(self):
        """Configura demonstração"""
        
        # Título
        title_font = ctk.CTkFont(family="Consolas", size=18, weight="bold")
        title = ctk.CTkLabel(
            self.root,
            text="🤖 BARRA DE PROGRESSO STARK INDUSTRIES",
            font=title_font,
            text_color="#80E8FF"
        )
        title.pack(pady=20)
        
        # Container principal
        main_frame = ctk.CTkFrame(
            self.root, 
            corner_radius=10, 
            border_color="#00D2FF", 
            fg_color="#002B36"
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campo de texto simulado
        input_font = ctk.CTkFont(family="Consolas", size=14)
        text_input = ctk.CTkEntry(
            main_frame,
            placeholder_text="Digite seu comando...",
            font=input_font,
            height=40,
            border_color="#00D2FF",
            fg_color="#002B36"
        )
        text_input.pack(fill="x", padx=10, pady=(10, 5))
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(
            main_frame,
            height=4,
            progress_color="#00D2FF",
            fg_color="#002B36",
            border_color="#00D2FF"
        )
        self.progress_bar.pack(fill="x", padx=10, pady=(0, 10))
        self.progress_bar.set(0)
        
        # Botões de controle
        button_frame = ctk.CTkFrame(
            main_frame,
            border_color="#00D2FF",
            fg_color="#002B36"
        )
        button_frame.pack(fill="x", padx=10, pady=10)
        
        button_font = ctk.CTkFont(family="Consolas", size=12, weight="bold")
        
        # Botão iniciar
        start_button = ctk.CTkButton(
            button_frame,
            text="🚀 INICIAR ANIMAÇÃO",
            font=button_font,
            fg_color="#00D2FF",
            hover_color="#0095B3",
            text_color="#000000",
            command=self.start_animation
        )
        start_button.pack(side="left", padx=5, pady=10)
        
        # Botão parar
        stop_button = ctk.CTkButton(
            button_frame,
            text="⏹️ PARAR",
            font=button_font,
            fg_color="#00D2FF",
            hover_color="#0095B3",
            text_color="#000000",
            command=self.stop_animation
        )
        stop_button.pack(side="left", padx=5, pady=10)
        
        # Botão teste rápido
        test_button = ctk.CTkButton(
            button_frame,
            text="⚡ TESTE RÁPIDO",
            font=button_font,
            fg_color="#00D2FF",
            hover_color="#0095B3",
            text_color="#000000",
            command=self.quick_test
        )
        test_button.pack(side="left", padx=5, pady=10)
        
        # Status
        status_font = ctk.CTkFont(family="Consolas", size=12)
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="🟢 Pronto para demonstração",
            font=status_font,
            text_color="#80E8FF"
        )
        self.status_label.pack(pady=10)
        
    def start_animation(self):
        """Inicia animação contínua"""
        if not self.progress_animation_active:
            self.progress_animation_active = True
            self.status_label.configure(text="🟡 Animação em andamento...", text_color="#80E8FF")
            
            def animate():
                progress = 0
                while self.progress_animation_active:
                    progress += 0.02
                    if progress >= 1.0:
                        progress = 0
                    self.progress_bar.set(progress)
                    time.sleep(0.05)
            
            threading.Thread(target=animate, daemon=True).start()
    
    def stop_animation(self):
        """Para animação"""
        self.progress_animation_active = False
        self.progress_bar.set(0)
        self.status_label.configure(text="🟢 Animação parada", text_color="#80E8FF")
    
    def quick_test(self):
        """Teste rápido de progresso"""
        self.status_label.configure(text="🟡 Teste rápido...", text_color="#80E8FF")
        
        def test():
            for i in range(101):
                if not self.progress_animation_active:
                    self.progress_bar.set(i / 100)
                    time.sleep(0.02)
            self.progress_bar.set(0)
            self.status_label.configure(text="🟢 Teste concluído", text_color="#80E8FF")
        
        threading.Thread(target=test, daemon=True).start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    demo = ProgressDemo()
    demo.run()
