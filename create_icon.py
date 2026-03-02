#!/usr/bin/env python3
"""
Cria um ícone simples para o J.A.R.V.I.S.
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os

    def create_jarvis_icon():
        """Cria um ícone 256x256 para o Jarvis"""
        size = 256
        
        # Cria imagem com fundo transparente
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Cores Stark Industries
        bg_color = (11, 14, 20)      # #0B0E14
        border_color = (0, 210, 255) # #00D2FF
        text_color = (128, 232, 255) # #80E8FF
        
        # Desenha círculo de fundo
        margin = 20
        draw.ellipse([margin, margin, size-margin, size-margin], 
                     fill=bg_color, outline=border_color, width=4)
        
        # Desenha o texto J.A.R.V.I.S.
        try:
            # Tenta usar uma fonte padrão
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            # Se não encontrar, usa fonte padrão
            font = ImageFont.load_default()
        
        text = "J.A.R.V.I.S."
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 20
        
        draw.text((x, y), text, fill=text_color, font=font, anchor="lt")
        
        # Desenha o robô emoji
        robot_text = "🤖"
        try:
            font_robot = ImageFont.truetype("seguiemj.ttf", 48)
        except:
            font_robot = ImageFont.load_default()
        
        robot_bbox = draw.textbbox((0, 0), robot_text, font=font_robot)
        robot_width = robot_bbox[2] - robot_bbox[0]
        robot_x = (size - robot_width) // 2
        robot_y = y + 40
        
        draw.text((robot_x, robot_y), robot_text, fill=text_color, font=font_robot, anchor="lt")
        
        # Salva como ICO
        img.save('icon.ico', format='ICO', sizes=[(256, 256)])
        print("✅ Ícone criado: icon.ico")
        
        # Também salva como PNG para preview
        img.save('icon_preview.png')
        print("✅ Preview criado: icon_preview.png")
    
    if __name__ == "__main__":
        create_jarvis_icon()
        
except ImportError:
    print("❌ Pillow não encontrado. Instale com: pip install Pillow")
    print("O ícone não é obrigatório para o executável funcionar.")
