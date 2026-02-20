#!/usr/bin/env python3
"""
Action Handler para Jarvis
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
        self.command_mappings = {
            'bloco de notas': 'notepad.exe',
            'notepad': 'notepad.exe',
            'calculadora': 'calc.exe',
            'calc': 'calc.exe',
            'paint': 'mspaint.exe',
            'editor de imagem': 'mspaint.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'chrome': 'chrome.exe',
            'navegador': 'chrome.exe',
            'explorador de arquivos': 'explorer.exe',
            'gerenciador de arquivos': 'explorer.exe',
            'discord': 'Discord.exe',
            'vscode': 'Code.exe',
            'visual studio code': 'Code.exe',
            'code': 'Code.exe'
        }
        self.app_mappings = self._load_app_mappings()
        self.code_generator = CodeGenerator(workspace_path=self.workspace_path)
        self.multi_lang_generator = MultiLanguageGenerator(workspace_path=self.workspace_path)
        
    def _load_app_mappings(self):
        """Carrega mapeamentos de aplicativos comuns"""
        mappings = {
            # Navegadores
            'chrome': self._find_chrome(),
            'google chrome': self._find_chrome(),
            'firefox': self._find_firefox(),
            'mozilla firefox': self._find_firefox(),
            'edge': self._find_edge(),
            'microsoft edge': self._find_edge(),
            
            # Mídia
            'spotify': self._find_spotify(),
            'vlc': self._find_vlc(),
            'windows media player': self._find_wmp(),
            
            # Produtividade
            'notepad': 'notepad.exe',
            'bloco de notas': 'notepad.exe',
            'word': self._find_office_app('WINWORD.EXE'),
            'excel': self._find_office_app('EXCEL.EXE'),
            'powerpoint': self._find_office_app('POWERPNT.EXE'),
            
            # Comunicação
            'discord': self._find_discord(),
            'slack': self._find_slack(),
            'teams': self._find_teams(),
            'zoom': self._find_zoom(),
            
            # Desenvolvimento
            'vscode': self._find_vscode(),
            'visual studio code': self._find_vscode(),
            'code': self._find_vscode(),
            
            # Sistema
            'explorer': 'explorer.exe',
            'windows explorer': 'explorer.exe',
            'calculadora': 'calc.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
        }
        return mappings
        
    def _find_chrome(self):
        """Encontra o executável do Chrome"""
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]
        return self._find_executable(possible_paths)
        
    def _find_firefox(self):
        """Encontra o executável do Firefox"""
        possible_paths = [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            os.path.expanduser(r"~\AppData\Local\Mozilla Firefox\firefox.exe")
        ]
        return self._find_executable(possible_paths)
        
    def _find_edge(self):
        """Encontra o executável do Edge"""
        possible_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
        return self._find_executable(possible_paths)
        
    def _find_spotify(self):
        """Encontra o executável do Spotify"""
        possible_paths = [
            r"C:\Program Files\Spotify\Spotify.exe",
            r"C:\Program Files (x86)\Spotify\Spotify.exe",
            os.path.expanduser(r"~\AppData\Roaming\Spotify\Spotify.exe")
        ]
        return self._find_executable(possible_paths)
        
    def _find_vlc(self):
        """Encontra o executável do VLC"""
        possible_paths = [
            r"C:\Program Files\VideoLAN\VLC\vlc.exe",
            r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
        ]
        return self._find_executable(possible_paths)
        
    def _find_wmp(self):
        """Encontra o Windows Media Player"""
        return "wmplayer.exe"
        
    def _find_discord(self):
        """Encontra o executável do Discord"""
        possible_paths = [
            os.path.expanduser(r"~\AppData\Local\Discord\app-1.0.9007\Discord.exe"),
            os.path.expanduser(r"~\AppData\Local\Discord\app-*\Discord.exe")
        ]
        return self._find_executable(possible_paths, pattern="Discord.exe")
        
    def _find_slack(self):
        """Encontra o executável do Slack"""
        possible_paths = [
            os.path.expanduser(r"~\AppData\Local\slack\app-4.29.149\slack.exe"),
            os.path.expanduser(r"~\AppData\Local\slack\app-*\slack.exe")
        ]
        return self._find_executable(possible_paths, pattern="slack.exe")
        
    def _find_teams(self):
        """Encontra o executável do Teams"""
        possible_paths = [
            os.path.expanduser(r"~\AppData\Local\Microsoft\Teams\current\Teams.exe")
        ]
        return self._find_executable(possible_paths)
        
    def _find_zoom(self):
        """Encontra o executável do Zoom"""
        possible_paths = [
            r"C:\Program Files\Zoom\bin\Zoom.exe",
            r"C:\Program Files (x86)\Zoom\bin\Zoom.exe",
            os.path.expanduser(r"~\AppData\Roaming\Zoom\bin\Zoom.exe")
        ]
        return self._find_executable(possible_paths)
        
    def _find_vscode(self):
        """Encontra o executável do VS Code"""
        possible_paths = [
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
            os.path.expanduser(r"~\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        ]
        return self._find_executable(possible_paths)
        
    def _find_office_app(self, exe_name):
        """Encontra aplicativos do Microsoft Office"""
        try:
            # Tenta encontrar no registro do Windows
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\\" + exe_name)
            path = winreg.QueryValue(key, "")
            winreg.CloseKey(key)
            return path
        except:
            # Fallback para caminhos comuns
            office_paths = [
                r"C:\Program Files\Microsoft Office\root\Office16",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16",
                r"C:\Program Files\Microsoft Office\Office16",
                r"C:\Program Files (x86)\Microsoft Office\Office16"
            ]
            for office_path in office_paths:
                full_path = os.path.join(office_path, exe_name)
                if os.path.exists(full_path):
                    return full_path
        return None
        
    def gerar_e_colar_codigo(self, command, ai_model=None):
        """Gera código com Gemini e cola no aplicativo especificado"""
        command_lower = command.lower()
        
        # Verifica se é um comando para gerar código
        if any(word in command_lower for word in ['escreva um código', 'gere um código', 'crie um código', 'gerar código', 'escrever código']):
            try:
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
                    
                    response = ai_model.generate_content(prompt)
                    codigo_gerado = response.text if response and hasattr(response, 'text') else f"Código {tipo_codigo}"
                    
                    # Limpa o código
                    codigo_gerado = codigo_gerado.strip()
                    if not codigo_gerado:
                        codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                    
                    print(f"✅ Código gerado: {len(codigo_gerado)} caracteres")
                else:
                    # Fallback se não tiver modelo
                    codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                
                # Copia o código para a área de transferência
                pyperclip.copy(codigo_gerado)
                print("📋 Código copiado para a área de transferência")
                
                # Abre o aplicativo
                print(f"🚀 Abrindo {app_display}...")
                os.startfile(app_to_open)
                
                # Aguarda a janela carregar completamente
                print("⏳ Aguardando janela carregar...")
                time.sleep(2)
                
                # Garante que a janela está ativa
                pyautogui.click(x=500, y=500)  # Clica no centro para garantir foco
                time.sleep(0.5)
                
                # Cola o código
                print("📋 Colando código...")
                pyautogui.hotkey('ctrl', 'v')
                
                return f"Código {tipo_codigo} gerado e colado no {app_display}, mestre."
                
            except Exception as e:
                print(f"❌ Erro ao gerar e colar código: {e}")
                return f"Erro ao gerar e colar código: {str(e)}, mestre."
        
        return None
        
    def _find_executable(self, paths, pattern=None):
        """Encontra um executável em uma lista de caminhos possíveis"""
        for path in paths:
            if '*' in path:
                # Para caminhos com wildcard
                import glob
                matches = glob.glob(path)
                if matches:
                    return matches[0]
            elif os.path.exists(path):
                return path
        return None
        
    def gerar_e_colar_codigo(self, command, ai_model=None):
        """Gera código com Gemini e cola no aplicativo especificado"""
        command_lower = command.lower()
        
        # Verifica se é um comando para gerar código
        if any(word in command_lower for word in ['escreva um código', 'gere um código', 'crie um código', 'gerar código', 'escrever código']):
            try:
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
                    
                    response = ai_model.generate_content(prompt)
                    codigo_gerado = response.text if response and hasattr(response, 'text') else f"Código {tipo_codigo}"
                    
                    # Limpa o código
                    codigo_gerado = codigo_gerado.strip()
                    if not codigo_gerado:
                        codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                    
                    print(f"✅ Código gerado: {len(codigo_gerado)} caracteres")
                else:
                    # Fallback se não tiver modelo
                    codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                
                # Copia o código para a área de transferência
                pyperclip.copy(codigo_gerado)
                print("📋 Código copiado para a área de transferência")
                
                # Abre o aplicativo
                print(f"🚀 Abrindo {app_display}...")
                os.startfile(app_to_open)
                
                # Aguarda a janela carregar completamente
                print("⏳ Aguardando janela carregar...")
                time.sleep(2)
                
                # Garante que a janela está ativa
                pyautogui.click(x=500, y=500)  # Clica no centro para garantir foco
                time.sleep(0.5)
                
                # Cola o código
                print("📋 Colando código...")
                pyautogui.hotkey('ctrl', 'v')
                
                return f"Código {tipo_codigo} gerado e colado no {app_display}, mestre."
                
            except Exception as e:
                print(f"❌ Erro ao gerar e colar código: {e}")
                return f"Erro ao gerar e colar código: {str(e)}, mestre."
        
        return None
        
    def process_command(self, command, ai_model=None):
        """Processa um comando e executa a ação correspondente"""
        print(f"🎯 ActionHandler recebendo comando: '{command}'")
        command_lower = command.lower()
        
        # Limpa o comando removendo pontos e espaços extras
        clean_command = command.strip().rstrip('.')
        print(f"🧹 Comando limpo: '{clean_command}'")
        
        # Verifica se é uma solicitação de código multi-linguagem primeiro
        multi_lang_result = self.multi_lang_generator.process_multi_language_request(command, ai_model, getattr(self, 'speak_callback', None))
        if multi_lang_result:
            return multi_lang_result
        
        # Verifica se é uma solicitação de código
        code_result = self._handle_code_request(command)
        if code_result:
            return code_result
        
        # Verifica se é uma resposta positiva para salvar código
        command_lower = command.lower()
        if any(word in command_lower for word in ['sim', 'salvar', 'salve', 'pode salvar', 'quero salvar']):
            if hasattr(self, 'last_generated_code'):
                return self.save_code_to_file()
        
        # Verifica se é uma solicitação de código Python
        code_result = self.code_generator.process_code_request(command, ai_model)
        if code_result:
            return code_result
        
        # Verifica se é um comando para gerar e colar código
        gerar_result = self.gerar_e_colar_codigo(command, ai_model)
        if gerar_result:
            return gerar_result
        
        # Ações de abrir aplicativos
        if any(word in command_lower for word in ['abra', 'abre', 'abrir', 'open']):
            # Verifica se é um comando combinado primeiro
            combined_result = self.abrir_e_digitar(command)
            if combined_result:
                return combined_result
            
            print("🚀 Detectado comando de abrir aplicativo")
            return self._handle_open_command(command)
            
        # Ações de fechar aplicativos
        elif any(word in command_lower for word in ['feche', 'fecha', 'fechar', 'close']):
            print("🔪 Detectado comando de fechar aplicativo")
            return self.fechar_aplicativo(command)
            
        # Ações de digitar texto
        elif any(word in command_lower for word in ['digite', 'digitar', 'escreva', 'escrever', 'type', 'cole', 'colar', 'paste']):
            print("⌨️ Detectado comando de digitação")
            return self.digitar_texto(command)
            
        # Ações de listar arquivos
        elif any(word in command_lower for word in ['liste', 'listar', 'lista', 'mostrar', 'mostra', 'arquivos', 'files']):
            return self._handle_list_command(command)
            
        # Ações de sistema
        elif any(word in command_lower for word in ['desligue', 'desligar', 'reiniciar', 'reboot', 'bloquear', 'lock']):
            return self._handle_system_command(command)
            
        else:
            return None
        
    def gerar_e_colar_codigo(self, command, ai_model=None):
        """Gera código com Gemini e cola no aplicativo especificado"""
        command_lower = command.lower()
        
        # Verifica se é um comando para gerar código
        if any(word in command_lower for word in ['escreva um código', 'gere um código', 'crie um código', 'gerar código', 'escrever código']):
            try:
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
                    
                    response = ai_model.generate_content(prompt)
                    codigo_gerado = response.text if response and hasattr(response, 'text') else f"Código {tipo_codigo}"
                    
                    # Limpa o código
                    codigo_gerado = codigo_gerado.strip()
                    if not codigo_gerado:
                        codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                    
                    print(f"✅ Código gerado: {len(codigo_gerado)} caracteres")
                else:
                    # Fallback se não tiver modelo
                    codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                
                # Copia o código para a área de transferência
                pyperclip.copy(codigo_gerado)
                print("📋 Código copiado para a área de transferência")
                
                # Abre o aplicativo
                print(f"🚀 Abrindo {app_display}...")
                os.startfile(app_to_open)
                
                # Aguarda a janela carregar completamente
                print("⏳ Aguardando janela carregar...")
                time.sleep(2)
                
                # Garante que a janela está ativa
                pyautogui.click(x=500, y=500)  # Clica no centro para garantir foco
                time.sleep(0.5)
                
                # Cola o código
                print("📋 Colando código...")
                pyautogui.hotkey('ctrl', 'v')
                
                return f"Código {tipo_codigo} gerado e colado no {app_display}, mestre."
                
            except Exception as e:
                print(f"❌ Erro ao gerar e colar código: {e}")
                return f"Erro ao gerar e colar código: {str(e)}, mestre."
        
        return None
            
    def _handle_open_command(self, command):
        """Lida com comandos para abrir aplicativos usando Busca Universal"""
        command_lower = command.lower()
        
        # Verifica se é um comando de abrir
        if any(word in command_lower for word in ['abra', 'abre', 'abrir', 'open']):
            # Extrai o nome do aplicativo após a palavra de comando
            app_name = command_lower
            for word in ['abra', 'abre', 'abrir', 'open']:
                app_name = app_name.replace(word, '').strip()
            
            print(f"🔍 Verificação: command_lower='{command_lower}'")
            print(f"🔍 App name extraído: '{app_name}'")
            print(f"🔍 Letras 'O' mantidas: {'o' in app_name}")
            
            if app_name:
                print(f"🔍 Busca Universal: '{app_name}'")
                return self._universal_search(app_name)
        
        return None
        
    def gerar_e_colar_codigo(self, command, ai_model=None):
        """Gera código com Gemini e cola no aplicativo especificado"""
        command_lower = command.lower()
        
        # Verifica se é um comando para gerar código
        if any(word in command_lower for word in ['escreva um código', 'gere um código', 'crie um código', 'gerar código', 'escrever código']):
            try:
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
                    
                    response = ai_model.generate_content(prompt)
                    codigo_gerado = response.text if response and hasattr(response, 'text') else f"Código {tipo_codigo}"
                    
                    # Limpa o código
                    codigo_gerado = codigo_gerado.strip()
                    if not codigo_gerado:
                        codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                    
                    print(f"✅ Código gerado: {len(codigo_gerado)} caracteres")
                else:
                    # Fallback se não tiver modelo
                    codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                
                # Copia o código para a área de transferência
                pyperclip.copy(codigo_gerado)
                print("📋 Código copiado para a área de transferência")
                
                # Abre o aplicativo
                print(f"🚀 Abrindo {app_display}...")
                os.startfile(app_to_open)
                
                # Aguarda a janela carregar completamente
                print("⏳ Aguardando janela carregar...")
                time.sleep(2)
                
                # Garante que a janela está ativa
                pyautogui.click(x=500, y=500)  # Clica no centro para garantir foco
                time.sleep(0.5)
                
                # Cola o código
                print("📋 Colando código...")
                pyautogui.hotkey('ctrl', 'v')
                
                return f"Código {tipo_codigo} gerado e colado no {app_display}, mestre."
                
            except Exception as e:
                print(f"❌ Erro ao gerar e colar código: {e}")
                return f"Erro ao gerar e colar código: {str(e)}, mestre."
        
        return None
    
    def _universal_search(self, app_name):
        """Busca universal usando pyautogui no Menu Iniciar"""
        try:
            print(f"🚀 Iniciando Busca Universal para: '{app_name}'")
            print(f"� Digitando exatamente: '{app_name}' (sem abreviar)")
            
            # Pressiona a tecla do Windows para abrir o Menu Iniciar
            pyautogui.press('win')
            time.sleep(0.5)
            
            # Digita o nome do aplicativo EXATAMENTE como recebido
            pyautogui.write(app_name)
            time.sleep(0.5)
            
            # Pressiona Enter para abrir o primeiro resultado
            pyautogui.press('enter')
            time.sleep(1)
            
            print(f"✅ Aplicativo '{app_name}' aberto via Busca Universal")
            return f"{app_name.title()} aberto com sucesso, mestre."
            
        except Exception as e:
            print(f"❌ Erro na Busca Universal: {e}")
            return f"Não consegui abrir '{app_name}' via Busca Universal, mestre."
            
    def _search_start_menu(self, app_name):
        """Busca aplicativos no Menu Iniciar usando pyautogui"""
        try:
            print(f"🔍 Buscando '{app_name}' no Menu Iniciar...")
            
            # Pressiona a tecla do Windows para abrir o Menu Iniciar
            pyautogui.press('win')
            time.sleep(1)
            
            # Digita o nome do aplicativo
            pyautogui.write(app_name)
            time.sleep(1)
            
            # Pressiona Enter para abrir o primeiro resultado
            pyautogui.press('enter')
            time.sleep(2)
            
            print(f"✅ Aplicativo '{app_name}' aberto via Menu Iniciar")
            return f"{app_name.title()} aberto com sucesso, mestre."
            
        except Exception as e:
            print(f"❌ Erro ao buscar no Menu Iniciar: {e}")
            return f"Não consegui encontrar '{app_name}' no Menu Iniciar, mestre."
    
    def _generate_code_with_gemini(self, task):
        """Gera código usando Gemini para uma tarefa específica"""
        try:
            print(f"🤖 Pedindo código ao Gemini para: {task}")
            
            # Configura o contexto do Jarvis
            context = """
            Você é o Jarvis, assistente pessoal e parceiro de programação.
            Seu objetivo é ajudar com tarefas de desenvolvimento, ideias e soluções técnicas.
            Forneça código limpo, comentado e funcional.
            """
            
            # Gera o código
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"{context}\n\nTarefa: {task}\n\nPor favor, gere o código completo para esta tarefa:"
            response = model.generate_content(prompt)
            
            code = str(response.text) if response and hasattr(response, 'text') else ""
            print(f"📝 Código gerado pelo Gemini")
            return code
            
        except Exception as e:
            print(f'ERRO TÉCNICO AO GERAR CÓDIGO: {e}')
            import traceback
            traceback.print_exc()
            return f"Não consegui gerar código para '{task}', mestre. Erro técnico: {str(e)}"
    
    def _handle_list_command(self, command):
        """Lida com comandos para listar arquivos"""
        command_lower = command.lower()
        
        # Verifica se menciona workspace
        if 'workspace' in command_lower:
            return self._list_workspace_files()
            
        # Verifica se menciona desktop
        elif 'desktop' in command_lower or 'área de trabalho' in command_lower:
            return self._list_desktop_files()
            
        # Lista do diretório atual
        else:
            return self._list_current_files()
    
    def _handle_code_request(self, command):
        """Lida com comandos para gerar código"""
        command_lower = command.lower()
        
        # Verifica se é um pedido de código com múltiplas palavras-chave
        code_keywords = [
            'escreva um código para', 'gere um código para', 'programe', 
            'crie um script', 'crie uma função', 'desenvolva', 
            'implemente', 'crie um programa', 'escreva um script'
        ]
        
        is_code_request = any(keyword in command_lower for keyword in code_keywords)
        
        if is_code_request:
            # Extrai a tarefa do comando
            task = command_lower
            for keyword in code_keywords:
                if keyword in command_lower:
                    task = command_lower.replace(keyword, '').strip()
                    break
            
            print(f"💻 Solicitação de código detectada: {task}")
            
            # Gera o código com Gemini
            code = self._generate_code_with_gemini(task)
            
            if code and not code.startswith("Não consegui"):
                # Exibe no console formatado
                print("\n" + "="*60)
                print("🤖 CÓDIGO GERADO PELO JARVIS 🤖")
                print("="*60)
                print(code)
                print("="*60)
                
                # Armazena o código para possível salvamento
                self.last_generated_code = code
                self.last_code_task = task
                
                return f"Código gerado para '{task}'. Deseja que eu salve este código em um arquivo .py, mestre?"
            else:
                return code
        
        return None
        
    def gerar_e_colar_codigo(self, command, ai_model=None):
        """Gera código com Gemini e cola no aplicativo especificado"""
        command_lower = command.lower()
        
        # Verifica se é um comando para gerar código
        if any(word in command_lower for word in ['escreva um código', 'gere um código', 'crie um código', 'gerar código', 'escrever código']):
            try:
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
                    
                    response = ai_model.generate_content(prompt)
                    codigo_gerado = response.text if response and hasattr(response, 'text') else f"Código {tipo_codigo}"
                    
                    # Limpa o código
                    codigo_gerado = codigo_gerado.strip()
                    if not codigo_gerado:
                        codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                    
                    print(f"✅ Código gerado: {len(codigo_gerado)} caracteres")
                else:
                    # Fallback se não tiver modelo
                    codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                
                # Copia o código para a área de transferência
                pyperclip.copy(codigo_gerado)
                print("📋 Código copiado para a área de transferência")
                
                # Abre o aplicativo
                print(f"🚀 Abrindo {app_display}...")
                os.startfile(app_to_open)
                
                # Aguarda a janela carregar completamente
                print("⏳ Aguardando janela carregar...")
                time.sleep(2)
                
                # Garante que a janela está ativa
                pyautogui.click(x=500, y=500)  # Clica no centro para garantir foco
                time.sleep(0.5)
                
                # Cola o código
                print("📋 Colando código...")
                pyautogui.hotkey('ctrl', 'v')
                
                return f"Código {tipo_codigo} gerado e colado no {app_display}, mestre."
                
            except Exception as e:
                print(f"❌ Erro ao gerar e colar código: {e}")
                return f"Erro ao gerar e colar código: {str(e)}, mestre."
        
        return None
    
    def save_code_to_file(self, filename=None):
        """Salva o último código gerado em um arquivo"""
        try:
            if not hasattr(self, 'last_generated_code'):
                return "Não há código para salvar, mestre."
            
            # Define o nome do arquivo
            if not filename:
                # Gera nome baseado na tarefa
                task_words = self.last_code_task.split()[:3]  # Primeiras 3 palavras
                filename = "_".join(task_words) + ".py"
                # Remove caracteres inválidos
                filename = "".join(c for c in filename if c.isalnum() or c in "_-")
            
            # Caminho completo
            filepath = os.path.join(self.workspace_path, filename)
            
            # Salva o arquivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.last_generated_code)
            
            print(f"💾 Código salvo em: {filepath}")
            return f"Código salvo com sucesso em '{filename}', mestre."
            
        except Exception as e:
            print(f"❌ Erro ao salvar código: {e}")
            return f"Erro ao salvar código: {str(e)}, mestre."
            
    def _list_workspace_files(self):
        """Lista arquivos do workspace"""
        try:
            if not os.path.exists(self.workspace_path):
                return f"O caminho do workspace não existe: {self.workspace_path}"
                
            files = []
            folders = []
            
            for item in os.listdir(self.workspace_path):
                item_path = os.path.join(self.workspace_path, item)
                if os.path.isdir(item_path):
                    folders.append(f"📁 {item}")
                else:
                    files.append(f"📄 {item}")
                    
            result = f"Arquivos em {self.workspace_path}:\n\n"
            if folders:
                result += "Pastas:\n" + "\n".join(folders[:10]) + "\n\n"
            if files:
                result += "Arquivos:\n" + "\n".join(files[:15])
                
            return result
            
        except Exception as e:
            return f"Erro ao listar workspace: {str(e)}"
            
    def _list_desktop_files(self):
        """Lista arquivos da área de trabalho"""
        desktop_path = os.path.expanduser("~/Desktop")
        self.workspace_path = desktop_path
        return self._list_workspace_files()
        
    def _list_current_files(self):
        """Lista arquivos do diretório atual"""
        current_path = os.getcwd()
        self.workspace_path = current_path
        return self._list_workspace_files()
        
    def _handle_system_command(self, command):
        """Lida com comandos de sistema"""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ['desligue', 'desligar', 'shutdown']):
            return "Comando de desligamento não permitido por segurança, mestre."
            
        elif any(word in command_lower for word in ['reiniciar', 'reboot', 'restart']):
            return "Comando de reinicialização não permitido por segurança, mestre."
            
        elif any(word in command_lower for word in ['bloquear', 'lock']):
            try:
                print("🔒 Bloqueando sistema...")
                subprocess.Popen("rundll32.exe user32.dll,LockWorkStation", shell=True)
                return "Sistema bloqueado, mestre."
            except:
                return "Não consegui bloquear o sistema, mestre."
                
        return "Comando de sistema não reconhecido, mestre."
        
    def set_workspace_path(self, path):
        """Define o caminho do workspace"""
        if os.path.exists(path):
            self.workspace_path = path
            return f"Workspace definido para: {path}"
        else:
            return f"O caminho não existe: {path}"
            
    def fechar_aplicativo(self, command):
        """Fecha aplicativos específicos baseados no comando"""
        command_lower = command.lower()
        
        # Mapeamento de comandos para processos
        app_mapping = {
            'bloco de notas': 'notepad',
            'notepad': 'notepad',
            'discord': 'discord',
            'chrome': 'chrome',
            'google chrome': 'chrome',
            'firefox': 'firefox',
            'edge': 'msedge',
            'microsoft edge': 'msedge',
            'excel': 'excel',
            'word': 'winword',
            'powerpoint': 'powerpnt',
            'spotify': 'spotify',
            'telegram': 'telegram',
            'whatsapp': 'whatsapp',
            'vs code': 'code',
            'visual studio code': 'code',
            'explorer': 'explorer',
            'windows explorer': 'explorer',
            'calculadora': 'calculator',
            'calculator': 'calculator',
            'paint': 'mspaint',
            'mspaint': 'mspaint',
            'task manager': 'taskmgr',
            'gerenciador de tarefas': 'taskmgr'
        }
        
        # Verifica qual aplicativo fechar
        for app_name, process_name in app_mapping.items():
            if app_name in command_lower:
                try:
                    print(f"🔪 Fechando aplicativo: {app_name} (processo: {process_name}.exe)")
                    
                    # Usa taskkill para forçar o fechamento
                    result = os.system(f'taskkill /F /IM {process_name}.exe /T')
                    
                    if result == 0:
                        return f"{app_name.capitalize()} fechado com sucesso, mestre."
                    else:
                        return f"Não consegui fechar {app_name}. Talvez não esteja em execução, mestre."
                        
                except Exception as e:
                    print(f"❌ Erro ao fechar {app_name}: {e}")
                    return f"Erro ao fechar {app_name}: {str(e)}, mestre."
        
        return "Não reconheci qual aplicativo fechar, mestre. Tente: 'fechar bloco de notas', 'fechar discord', 'fechar chrome', etc."
        
    def digitar_texto(self, command):
        """Digita texto em aplicativos abertos"""
        command_lower = command.lower()
        
        # Verifica se é um comando para digitar
        if any(word in command_lower for word in ['digite', 'digitar', 'escreva', 'escrever', 'type']):
            try:
                # Extrai o texto para digitar (remove a parte do comando)
                texto_para_digitar = command_lower
                
                # Remove variações do comando
                prefixes_to_remove = [
                    'digite ', 'digitar ', 'escreva ', 'escrever ', 
                    'type ', 'digite no bloco de notas ', 'digitar no bloco de notas ',
                    'escreva no bloco de notas ', 'escrever no bloco de notas '
                ]
                
                for prefix in prefixes_to_remove:
                    if texto_para_digitar.startswith(prefix):
                        texto_para_digitar = texto_para_digitar[len(prefix):]
                        break
                
                # Se ainda tiver "no bloco de notas" ou similar, remove
                app_references = ['no bloco de notas', 'no notepad', 'no bloco', 'no editor']
                for ref in app_references:
                    texto_para_digitar = texto_para_digitar.replace(ref, '').strip()
                
                if not texto_para_digitar:
                    return "O que você gostaria que eu digitasse, mestre?"
                
                print(f"⌨️ Digitando texto: '{texto_para_digitar}'")
                
                # Aguarda um momento para garantir que a janela está focada
                time.sleep(1)
                
                # Digita o texto com intervalo pequeno para simular digitação humana
                pyautogui.write(texto_para_digitar, interval=0.01)
                
                return f"Texto digitado com sucesso: '{texto_para_digitar}', mestre."
                
            except Exception as e:
                print(f"❌ Erro ao digitar texto: {e}")
                return f"Erro ao digitar texto: {str(e)}, mestre."
        
        # Verifica se é um comando para colar
        elif any(word in command_lower for word in ['cole', 'colar', 'paste']):
            try:
                print("📋 Colando texto da área de transferência...")
                
                # Aguarda um momento para garantir que a janela está focada
                time.sleep(1)
                
                # Cola o texto
                pyautogui.hotkey('ctrl', 'v')
                
                return "Texto colado com sucesso, mestre."
                
            except Exception as e:
                print(f"❌ Erro ao colar texto: {e}")
                return f"Erro ao colar texto: {str(e)}, mestre."
        
        return "Não reconheci o comando de digitação. Tente: 'digite [texto]' ou 'cole [texto]', mestre."
        
    def abrir_e_digitar(self, command):
        """Abre um aplicativo e digita texto nele"""
        command_lower = command.lower()
        
        # Verifica se é um comando combinado
        if any(word in command_lower for word in ['abra e digite', 'abre e digita', 'abrir e digitar', 'open and type']):
            try:
                # Mapeamento de aplicativos para abrir
                app_mapping = {
                    'bloco de notas': 'notepad.exe',
                    'notepad': 'notepad.exe',
                    'calculadora': 'calc.exe',
                    'calculator': 'calc.exe',
                    'paint': 'mspaint.exe',
                    'word': 'winword.exe',
                    'excel': 'excel.exe'
                }
                
                # Encontra qual aplicativo abrir
                app_to_open = None
                for app_name, exe_name in app_mapping.items():
                    if app_name in command_lower:
                        app_to_open = exe_name
                        app_display = app_name
                        break
                
                if not app_to_open:
                    return "Não reconheci qual aplicativo abrir. Tente: 'abra e digite no bloco de notas', mestre."
                
                # Extrai o texto para digitar
                texto_para_digitar = command_lower
                
                # Remove a parte do comando de abrir
                for app_name in app_mapping.keys():
                    if f'abra e digite no {app_name}' in texto_para_digitar:
                        texto_para_digitar = texto_para_digitar.replace(f'abra e digite no {app_name}', '').strip()
                    elif f'abre e digita no {app_name}' in texto_para_digitar:
                        texto_para_digitar = texto_para_digitar.replace(f'abre e digita no {app_name}', '').strip()
                    elif f'abrir e digitar no {app_name}' in texto_para_digitar:
                        texto_para_digitar = texto_para_digitar.replace(f'abrir e digitar no {app_name}', '').strip()
                
                if not texto_para_digitar:
                    return f"O que você gostaria que eu digitasse no {app_display}, mestre?"
                
                print(f"🚀 Abrindo {app_display} e digitando: '{texto_para_digitar}'")
                
                # Abre o aplicativo
                os.startfile(app_to_open)
                
                # Aguarda a janela carregar
                time.sleep(2)
                
                # Digita o texto
                pyautogui.write(texto_para_digitar, interval=0.01)
                
                return f"{app_display.capitalize()} aberto e texto digitado: '{texto_para_digitar}', mestre."
                
            except Exception as e:
                print(f"❌ Erro ao abrir e digitar: {e}")
                return f"Erro ao abrir e digitar: {str(e)}, mestre."
        
        return None
        
    def gerar_e_colar_codigo(self, command, ai_model=None):
        """Gera código com Gemini e cola no aplicativo especificado"""
        command_lower = command.lower()
        
        # Verifica se é um comando para gerar código
        if any(word in command_lower for word in ['escreva um código', 'gere um código', 'crie um código', 'gerar código', 'escrever código']):
            try:
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
                    
                    response = ai_model.generate_content(prompt)
                    codigo_gerado = response.text if response and hasattr(response, 'text') else f"Código {tipo_codigo}"
                    
                    # Limpa o código
                    codigo_gerado = codigo_gerado.strip()
                    if not codigo_gerado:
                        codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                    
                    print(f"✅ Código gerado: {len(codigo_gerado)} caracteres")
                else:
                    # Fallback se não tiver modelo
                    codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                
                # Copia o código para a área de transferência
                pyperclip.copy(codigo_gerado)
                print("📋 Código copiado para a área de transferência")
                
                # Abre o aplicativo
                print(f"🚀 Abrindo {app_display}...")
                os.startfile(app_to_open)
                
                # Aguarda a janela carregar completamente
                print("⏳ Aguardando janela carregar...")
                time.sleep(2)
                
                # Garante que a janela está ativa
                pyautogui.click(x=500, y=500)  # Clica no centro para garantir foco
                time.sleep(0.5)
                
                # Cola o código
                print("📋 Colando código...")
                pyautogui.hotkey('ctrl', 'v')
                
                return f"Código {tipo_codigo} gerado e colado no {app_display}, mestre."
                
            except Exception as e:
                print(f"❌ Erro ao gerar e colar código: {e}")
                return f"Erro ao gerar e colar código: {str(e)}, mestre."
        
        return None
