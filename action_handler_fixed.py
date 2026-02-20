#!/usr/bin/env python3
"""
Action Handler para Jarvis - Versão Corrigida
Sistema para interpretar intenções e executar ações no sistema
"""

import os
import sys
import platform
import subprocess
import pyautogui
import time
import pyperclip
from pathlib import Path
import winreg
from code_generator import CodeGenerator
from multi_language_generator import MultiLanguageGenerator
import google.generativeai as genai

class ActionHandler:
    def __init__(self, workspace_path=None):
        """Inicializa o Action Handler"""
        self.system = platform.system()
        self.workspace_path = workspace_path or os.path.expanduser("~/Desktop")
        
        # Configura a API do Gemini
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            print("🤖 API do Gemini configurada com sucesso")
        else:
            print("⚠️ API key do Gemini não encontrada")
        
        # Mapeamento fixo de comandos para executáveis
        self.executable_mappings = {
            'chrome': 'chrome.exe',
            'google chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe',
            'microsoft edge': 'msedge.exe',
            'discord': 'Discord.exe',
            'spotify': 'Spotify.exe',
            'telegram': 'Telegram.exe',
            'vscode': 'Code.exe',
            'visual studio code': 'Code.exe',
            'code': 'Code.exe'
        }
        self.app_mappings = self._load_app_mappings()
        self.code_generator = CodeGenerator(workspace_path=self.workspace_path)
        self.multi_lang_generator = MultiLanguageGenerator(workspace_path=self.workspace_path)
        
    def gerar_e_colar_codigo(self, command, ai_model=None):
        """Gera código com Gemini e cola no aplicativo especificado - VERSÃO CORRIGIDA"""
        command_lower = command.lower()
        
        # Verifica se é um comando para gerar código
        if any(word in command_lower for word in ['escreva um código', 'gere um código', 'crie um código', 'gerar código', 'escrever código']):
            try:
                print(f"🎯 Processando comando: '{command}'")
                
                # Mapeamento de aplicativos
                app_mapping = {
                    'bloco de notas': 'notepad.exe',
                    'notepad': 'notepad.exe',
                    'calculadora': 'calc.exe',
                    'paint': 'mspaint.exe',
                    'word': 'winword.exe',
                    'excel': 'excel.exe'
                }
                
                # Encontra o aplicativo
                app_to_open = None
                app_display = None
                for app_name, exe_name in app_mapping.items():
                    if f'no {app_name}' in command_lower or f'em {app_name}' in command_lower:
                        app_to_open = exe_name
                        app_display = app_name
                        break
                
                if not app_to_open:
                    app_to_open = 'notepad.exe'
                    app_display = 'bloco de notas'
                
                # Extrai o tipo de código solicitado
                tipo_codigo = command_lower
                prefixes_to_remove = [
                    'escreva um código de ', 'gere um código de ', 'crie um código de ',
                    'escreva um código ', 'gere um código ', 'crie um código ',
                    'gerar código de ', 'escrever código de '
                ]
                
                for prefix in prefixes_to_remove:
                    if tipo_codigo.startswith(prefix):
                        tipo_codigo = tipo_codigo[len(prefix):]
                        break
                
                # Remove referências ao aplicativo
                for app_name in app_mapping.keys():
                    tipo_codigo = tipo_codigo.replace(f' no {app_name}', '').replace(f' em {app_name}', '').strip()
                
                if not tipo_codigo:
                    tipo_codigo = "hello world"
                
                print(f"🤖 Gerando código do tipo: '{tipo_codigo}' para {app_display}")
                
                # Gera o código com Gemini
                if ai_model:
                    prompt = f"""
                    Gere um código {tipo_codigo} simples e funcional.
                    Retorne apenas o código, sem explicações ou comentários desnecessários.
                    """
                    
                    try:
                        response = ai_model.generate_content(prompt)
                        codigo_gerado = response.text if response and hasattr(response, 'text') else f"Código {tipo_codigo}"
                    except Exception as gemini_error:
                        print(f"⚠️ Erro no Gemini: {gemini_error}")
                        codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                    
                    # Limpa o código
                    codigo_gerado = codigo_gerado.strip()
                    if not codigo_gerado:
                        codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                    
                    print(f"✅ Código gerado: {len(codigo_gerado)} caracteres")
                else:
                    # Fallback se não tiver modelo
                    codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                
                # Copia o código para a área de transferência com tratamento de erro
                try:
                    pyperclip.copy(codigo_gerado)
                    print("📋 Código copiado para a área de transferência")
                except Exception as clip_error:
                    print(f"❌ Erro ao copiar para área de transferência: {clip_error}")
                    return f"Erro ao copiar código: {str(clip_error)}, mestre."
                
                # Abre o aplicativo com tratamento de erro
                try:
                    print(f"🚀 Abrindo {app_display}...")
                    os.startfile(app_to_open)
                except Exception as open_error:
                    print(f"❌ Erro ao abrir aplicativo: {open_error}")
                    return f"Erro ao abrir {app_display}: {str(open_error)}, mestre."
                
                # Aguarda a janela carregar completamente
                print("⏳ Aguardando janela carregar...")
                time.sleep(2)
                
                # Garante que a janela está ativa (com tratamento de erro)
                try:
                    pyautogui.click(x=500, y=500)  # Clica no centro para garantir foco
                    time.sleep(0.5)
                except Exception as click_error:
                    print(f"⚠️ Erro ao clicar para focar: {click_error}")
                    # Continua mesmo se falhar o clique
                
                # Cola o código com múltiplos métodos de fallback
                print("📋 Colando código...")
                try:
                    pyautogui.hotkey('ctrl', 'v')
                    print("✅ Código colado com sucesso (Ctrl+V)")
                except Exception as paste_error:
                    print(f"⚠️ Erro ao colar com Ctrl+V: {paste_error}")
                    # Tenta método alternativo: digitação direta
                    try:
                        print("📝 Tentando digitação alternativa...")
                        pyautogui.write(codigo_gerado, interval=0.01)
                        print("✅ Código digitado com sucesso")
                    except Exception as type_error:
                        print(f"❌ Falha em digitar também: {type_error}")
                        return f"Não consegui colar o código em {app_display}, mestre. Tente colar manualmente."
                
                return f"Código {tipo_codigo} gerado e colado no {app_display}, mestre."
                
            except Exception as e:
                print(f"❌ Erro geral ao gerar e colar código: {e}")
                return f"Erro ao gerar e colar código: {str(e)}, mestre."
        
        return None
    
    def process_command(self, command, ai_model=None):
        """Processa um comando e executa a ação correspondente"""
        print(f"🎯 ActionHandler recebendo comando: '{command}'")
        command_lower = command.lower()
        
        # Verifica se é um comando para gerar e colar código
        gerar_result = self.gerar_e_colar_codigo(command, ai_model)
        if gerar_result:
            return gerar_result
        
        return None
