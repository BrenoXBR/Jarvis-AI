#!/usr/bin/env python3
"""
Action Handler para Jarvis - Versão Mínima Funcional
"""

import os
import pyautogui
import time
import pyperclip
import psutil  # Para verificar processos
import google.generativeai as genai
from dotenv import load_dotenv

# Configurações de segurança do PyAutoGUI
pyautogui.FAILSAFE = True  # Fail-safe: mover mouse para canto superior esquerdo para
pyautogui.PAUSE = 0.5  # Pausa entre comandos para evitar sobrecarga

class ActionHandler:
    def __init__(self, workspace_path=None):
        """Inicializa o Action Handler"""
        self.workspace_path = workspace_path or os.path.expanduser("~/Desktop")
        
        # Configura a API do Gemini
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            print("🤖 API do Gemini configurada com sucesso")
        
        # Contador de segurança para evitar loops infinitos
        self.command_count = 0
        self.max_commands_per_session = 10
        
    def _is_process_active(self, process_name):
        """Verifica se um processo está ativo"""
        try:
            for proc in psutil.process_iter(['name']):
                if process_name.lower() in proc.info['name'].lower():
                    return True
            return False
        except:
            return False
    
    def _verify_window_focus(self, app_name):
        """Verifica se o aplicativo está em foco (simplificado)"""
        # Verificação básica se o processo está rodando
        process_names = {
            'bloco de notas': 'notepad',
            'notepad': 'notepad',
            'calculadora': 'calculator'
        }
        
        if app_name in process_names:
            return self._is_process_active(process_names[app_name])
        return True  # Se não souber, assume que está ok
    def gerar_e_colar_codigo(self, command, ai_model=None):
        """Gera código com Gemini e cola no aplicativo especificado"""
        # Verificação de segurança
        self.command_count += 1
        if self.command_count > self.max_commands_per_session:
            return "Limite de comandos atingido por segurança, mestre. Reinicie o Jarvis para continuar."
        
        command_lower = command.lower()
        
        # Verifica se é um comando para gerar código
        if any(word in command_lower for word in ['escreva um código', 'gere um código', 'crie um código', 'gerar código', 'escrever código']):
            try:
                # Mapeamento simples de aplicativos
                app_mapping = {
                    'bloco de notas': 'notepad.exe',
                    'notepad': 'notepad.exe',
                    'calculadora': 'calc.exe'
                }
                
                # Encontra o aplicativo
                app_to_open = 'notepad.exe'
                app_display = 'bloco de notas'
                for app_name, exe_name in app_mapping.items():
                    if f'no {app_name}' in command_lower:
                        app_to_open = exe_name
                        app_display = app_name
                        break
                
                # Extrai o tipo de código solicitado
                tipo_codigo = command_lower
                prefixes = ['escreva um código de ', 'gere um código de ', 'crie um código de ']
                for prefix in prefixes:
                    if tipo_codigo.startswith(prefix):
                        tipo_codigo = tipo_codigo[len(prefix):]
                        break
                
                # Remove referências ao aplicativo
                tipo_codigo = tipo_codigo.replace(' no bloco de notas', '').replace(' no notepad', '').strip()
                
                if not tipo_codigo:
                    tipo_codigo = "hello world"
                
                # Gera o código com Gemini
                if ai_model:
                    try:
                        prompt = f"Gere um código {tipo_codigo} simples e funcional."
                        response = ai_model.generate_content(prompt)
                        codigo_gerado = response.text if response and hasattr(response, 'text') else f"# Código {tipo_codigo}"
                    except Exception as e:
                        codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                else:
                    codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                
                codigo_gerado = codigo_gerado.strip()
                
                # Copia o código para a área de transferência
                try:
                    pyperclip.copy(codigo_gerado)
                except Exception as clip_error:
                    return f"Erro ao copiar código: {str(clip_error)}, mestre."
                
                # Abre o aplicativo
                try:
                    os.startfile(app_to_open)
                except Exception as open_error:
                    return f"Erro ao abrir {app_display}: {str(open_error)}, mestre."
                
                # Aguarda a janela carregar
                time.sleep(2)
                
                # Verifica se o processo está ativo antes de colar
                if not self._verify_window_focus(app_display):
                    return f"Não consegui verificar que {app_display} está ativo, mestre."
                
                # Cola o código
                try:
                    pyautogui.hotkey('ctrl', 'v')
                except Exception as paste_error:
                    # Tenta digitar como fallback
                    try:
                        pyautogui.write(codigo_gerado, interval=0.01)
                    except:
                        return f"Não consegui colar o código, mestre."
                
                return f"Código {tipo_codigo} gerado e colado no {app_display}, mestre."
                
            except Exception as e:
                return f"Erro ao processar: {str(e)}, mestre."
        
        return None
    
    def process_command(self, command, ai_model=None):
        """Processa um comando e executa a ação correspondente"""
        
        # Verifica se é um comando para gerar e colar código
        gerar_result = self.gerar_e_colar_codigo(command, ai_model)
        if gerar_result:
            return gerar_result
        
        return None
