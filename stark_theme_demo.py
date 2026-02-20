#!/usr/bin/env python3
"""
Demonstração da Paleta de Cores Stark Industries
"""

import customtkinter as ctk

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StarkThemeDemo:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🤖 Stark Industries - Paleta de Cores")
        self.root.geometry("600x500")
        
        # Aplicar fundo Stark Industries
        self.root.configure(fg_color="#0B0E14")
        
        self.setup_demo()
        
    def setup_demo(self):
        """Demonstração das cores"""
        
        # Título
        title_font = ctk.CTkFont(family="Consolas", size=20, weight="bold")
        title = ctk.CTkLabel(
            self.root,
            text="🤖 STARK INDUSTRIES - PALETA DE CORES",
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
        
        # Amostra de cores
        colors_demo = [
            ("Fundo Geral", "#0B0E14"),
            ("Bordas e Frames", "#00D2FF"),
            ("Fundo de Componentes", "#002B36"),
            ("Texto da IA (Azul Neon)", "#80E8FF"),
            ("Botão de Ação", "#00D2FF"),
            ("Hover do Botão", "#0095B3"),
        ]
        
        font = ctk.CTkFont(family="Consolas", size=12)
        
        for i, (name, color) in enumerate(colors_demo):
            # Frame para cada cor
            color_frame = ctk.CTkFrame(
                main_frame,
                border_color="#00D2FF",
                fg_color="#002B36"
            )
            color_frame.pack(fill="x", padx=10, pady=5)
            
            # Nome da cor
            label = ctk.CTkLabel(
                color_frame,
                text=f"{name}:",
                font=font,
                text_color="#80E8FF",
                anchor="w"
            )
            label.pack(side="left", padx=10, pady=10)
            
            # Amostra da cor
            sample = ctk.CTkFrame(
                color_frame,
                width=100,
                height=30,
                fg_color=color,
                border_color="#00D2FF"
            )
            sample.pack(side="right", padx=10, pady=10)
            
            # Código hex
            hex_label = ctk.CTkLabel(
                color_frame,
                text=color,
                font=font,
                text_color="#ffffff"
            )
            hex_label.pack(side="right", padx=10, pady=10)
        
        # Botão de exemplo
        button_font = ctk.CTkFont(family="Consolas", size=14, weight="bold")
        demo_button = ctk.CTkButton(
            main_frame,
            text="🚀 BOTÃO STARK INDUSTRIES",
            font=button_font,
            fg_color="#00D2FF",
            hover_color="#0095B3",
            text_color="#000000",
            border_color="#00D2FF",
            height=40
        )
        demo_button.pack(pady=20)
        
        # Texto de exemplo
        text_frame = ctk.CTkFrame(
            main_frame,
            border_color="#00D2FF",
            fg_color="#002B36"
        )
        text_frame.pack(fill="x", padx=10, pady=10)
        
        chat_font = ctk.CTkFont(family="Consolas", size=12)
        chat_text = ctk.CTkTextbox(
            text_frame,
            font=chat_font,
            height=100,
            fg_color="#002B36",
            border_color="#00D2FF"
        )
        chat_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Texto de exemplo
        chat_text.insert("end", "🤖 [12:34:56] J.A.R.V.I.S.:\n", "prefix")
        chat_text.insert("end", "Sistema online com paleta Stark Industries aplicada.\n\n", "message")
        chat_text.insert("end", "👤 [12:35:01] Você:\n", "user_prefix")
        chat_text.insert("end", "Excelente! As cores ficaram perfeitas.\n\n", "user_message")
        
        chat_text.tag_config("prefix", foreground="#80E8FF")
        chat_text.tag_config("message", foreground="#80E8FF")
        chat_text.tag_config("user_prefix", foreground="#00aaff")
        chat_text.tag_config("user_message", foreground="#ffffff")
        
        chat_text.configure(state="disabled")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    demo = StarkThemeDemo()
    demo.run()
