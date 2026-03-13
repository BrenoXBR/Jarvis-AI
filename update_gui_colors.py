#!/usr/bin/env python3
"""
Script para atualizar todas as referências de cores no gui.py
Substitui M13_COLORS por Config.get_color()
"""

import re

def update_gui_colors():
    """Atualiza todas as referências de cores no arquivo gui.py"""
    
    with open('gui.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substitui todas as referências M13_COLORS["..."] por Config.get_color("...")
    pattern = r'self\.M13_COLORS\["([^"]+)"\]'
    
    def replacement_func(match):
        color_name = match.group(1)
        return f'Config.get_color("{color_name}")'
    
    content = re.sub(pattern, replacement_func, content)
    
    # Substitui referências diretas a M13_COLORS
    content = content.replace('self.M13_COLORS', 'Config.M13_COLORS')
    
    with open('gui.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Cores atualizadas no gui.py")

if __name__ == "__main__":
    update_gui_colors()
