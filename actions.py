"""
J.A.R.V.I.S. - System Actions Module
Funções de controle do Windows e aplicações
"""

import os
import subprocess
import webbrowser
import glob
import shutil
import time
import random
import string
import psutil
import pyautogui
import threading
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import screen_brightness_control as sbc
import re
from bs4 import BeautifulSoup
import webbrowser
try:
    import pycaw
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

class SystemActions:
    """Classe responsável por todas as ações do sistema"""
    
    def __init__(self, logger):
        self.logger = logger
        self.audio_available = AUDIO_AVAILABLE
        self.wmi_available = WMI_AVAILABLE
        
        # Inicializa controle de áudio se disponível
        if self.audio_available:
            self._init_audio_control()
        
        # Inicializa lista de lembretes
        self.reminders = []
        
        self.logger.info("SystemActions inicializado", "ACTIONS")
        self.logger.system("Módulo de ações do sistema carregado", "INIT")
    
    def _init_audio_control(self):
        """Inicializa controle de áudio"""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = interface.QueryInterface(IAudioEndpointVolume)
            self.logger.info("Controle de áudio inicializado", "ACTIONS")
        except Exception as e:
            self.logger.error(e, "Erro ao inicializar áudio", "ACTIONS")
            self.audio_available = False
    
    def open_application(self, app_name: str) -> str:
        """Abre aplicativo usando dicionário rigoroso de sinônimos"""
        self.logger.system(f"Abrindo aplicativo: {app_name}", "APP")
        return self._rigorous_app_search(app_name)
    
    def _rigorous_app_search(self, app_name: str) -> str:
        """Busca rigorosa com mapeamento estrito e tratamento de preposições"""
        # Normalização simples
        app_name_normalized = app_name.lower().strip()
        
        # Log de verificação
        self.logger.system(f"[DEBUG] Comando original: '{app_name_normalized}'", "APP")
        
        # Remoção de stopwords
        stopwords = ['o', 'a', 'um', 'uma', 'por favor', 'please']
        nome_limpo = app_name_normalized
        for stopword in stopwords:
            nome_limpo = nome_limpo.replace(f' {stopword} ', ' ')
            nome_limpo = nome_limpo.replace(f' {stopword}', '')
            nome_limpo = nome_limpo.replace(f'{stopword} ', '')
        
        nome_limpo = nome_limpo.strip()
        
        # Tratamento do 'D' intruso - remove preposições e extrai palavras-chave
        palavras_chave = self._extrair_palavras_chave(nome_limpo)
        nome_processado = ' '.join(palavras_chave)
        
        # Log do nome processado
        self.logger.system(f"[DEBUG] Nome processado: '{nome_processado}' (palavras-chave: {palavras_chave})", "APP")
        
        # Mapeamento estrito de termos para executáveis
        mapeamento_estrito = {
            # Notepad - múltiplas combinações
            'bloco': 'notepad.exe',
            'notas': 'notepad.exe',
            'bloco notas': 'notepad.exe',
            'bloc notas': 'notepad.exe',  # Para erros de digitação
            'blocde notas': 'notepad.exe',  # Para erros de digitação
            'anotacoes': 'notepad.exe',
            'texto': 'notepad.exe',
            'editor texto': 'notepad.exe',
            
            # Calculadora
            'calc': 'calc.exe',
            'calculadora': 'calc.exe',
            'calcular': 'calc.exe',
            
            # CMD/Terminal
            'cmd': 'cmd.exe',
            'prompt': 'cmd.exe',
            'terminal': 'cmd.exe',
            'linha comando': 'cmd.exe',
            'comando': 'cmd.exe',
            
            # PowerShell
            'powershell': 'powershell.exe',
            'power shell': 'powershell.exe',
            'powershel': 'powershell.exe',  # Para erros de digitação
            
            # Explorador
            'explorer': 'explorer.exe',
            'arquivos': 'explorer.exe',
            'gerenciador arquivos': 'explorer.exe',
            
            # Task Manager
            'task': 'taskmgr.exe',
            'taskmgr': 'taskmgr.exe',
            'gerenciador tarefas': 'taskmgr.exe',
            'tarefas': 'taskmgr.exe',
            
            # Painel de Controle
            'painel': 'control.exe',
            'controle': 'control.exe',
            'painel controle': 'control.exe',
            
            # Paint
            'paint': 'mspaint.exe',
            'desenho': 'mspaint.exe',
            'mspaint': 'mspaint.exe',
            
            # Deep Links Windows
            'configuracoes': 'ms-settings:',
            'settings': 'ms-settings:',
            'loja': 'ms-windows-store:',
            'store': 'ms-windows-store:',
            'defender': 'ms-settings:windowsdefender',
            'antivirus': 'ms-settings:windowsdefender',
            'atualizacoes': 'ms-settings:windowsupdate-action',
            'update': 'ms-settings:windowsupdate-action',
            'rede': 'ms-settings:network',
            'som': 'ms-settings:sound',
            'audio': 'ms-settings:sound',
            'energia': 'ms-settings:powersleep',
            'bateria': 'ms-settings:powersleep',
            'notificacoes': 'ms-settings:notifications',
            'privacidade': 'ms-settings:privacy',
            'contas': 'ms-settings:yourinfo',
            'hora': 'ms-settings:dateandtime',
            'data': 'ms-settings:dateandtime',
            'acessibilidade': 'ms-settings:easeofaccess'
        }
        
        # 1. Verifica no mapeamento estrito
        if nome_processado in mapeamento_estrito:
            comando = mapeamento_estrito[nome_processado]
            self.logger.system(f"[DEBUG] Mapeamento estrito: '{nome_processado}' → '{comando}'", "APP")
            return self._executar_comando_direto(comando, app_name)
        
        # 2. Verifica se contém palavras-chave específicas
        for chave, comando in mapeamento_estrito.items():
            if chave in nome_processado:
                self.logger.system(f"[DEBUG] Palavra-chave encontrada: '{chave}' → '{comando}'", "APP")
                return self._executar_comando_direto(comando, app_name)
        
        # 3. Se não encontrou, tenta fallback inteligente
        self.logger.system(f"[DEBUG] Não encontrado no mapeamento, tentando fallback: '{nome_processado}'", "APP")
        return self._fallback_inteligente(nome_processado, app_name)
    
    def _extrair_palavras_chave(self, texto: str) -> List[str]:
        """Extrai palavras-chave ignorando preposições"""
        # Lista de preposições e palavras irrelevantes
        preposicoes = {'de', 'da', 'do', 'em', 'para', 'por', 'com', 'sem', 'sob', 'sobre', 'entre', 'até'}
        
        # Divide o texto em palavras
        palavras = texto.split()
        
        # Filtra apenas palavras-chave (não preposições)
        palavras_chave = [palavra for palavra in palavras if palavra not in preposicoes and len(palavra) > 1]
        
        # Se não encontrou palavras-chave, retorna o texto original
        if not palavras_chave:
            return [texto]
        
        return palavras_chave
    
    def _executar_comando_direto(self, comando: str, original_name: str) -> str:
        """Executa comando usando subprocess.Popen com caminho direto"""
        try:
            self.logger.system(f"[DEBUG] Executando comando direto: '{comando}'", "APP")
            
            if comando.startswith('ms-') or comando.startswith('ms-windows-'):
                # Deep Links Windows
                os.startfile(comando)
                self.logger.info(f"Deep Link executado: {comando}", "ACTIONS")
                return f"{original_name.title()} acessado, senhor."
            
            elif comando.endswith('.exe'):
                # Executável - tenta encontrar no PATH primeiro
                try:
                    # Tenta encontrar o executável no PATH do Windows
                    result = subprocess.run(['where', comando.split('\\')[-1]], 
                                          capture_output=True, text=True, timeout=5)
                    
                    if result.returncode == 0:
                        # Encontrou no PATH, executa com caminho completo
                        caminho_completo = result.stdout.strip().split('\n')[0]
                        subprocess.Popen([caminho_completo], shell=False)
                        self.logger.info(f"Executável encontrado no PATH: {caminho_completo}", "ACTIONS")
                        return f"{original_name.title()} acessado, senhor."
                    else:
                        # Não encontrou no PATH, tenta executar direto
                        subprocess.Popen([comando], shell=False)
                        self.logger.info(f"Executável executado diretamente: {comando}", "ACTIONS")
                        return f"{original_name.title()} acessado, senhor."
                        
                except subprocess.TimeoutExpired:
                    self.logger.warning("Timeout ao buscar executável no PATH", "ACTIONS")
                    # Tenta execução direta como fallback
                    subprocess.Popen([comando], shell=False)
                    self.logger.info(f"Executável executado por fallback: {comando}", "ACTIONS")
                    return f"{original_name.title()} acessado, senhor."
                    
                except Exception as e:
                    self.logger.error(e, f"Erro ao executar {comando}", "ACTIONS")
                    return f"❌ Erro ao acessar {original_name}: {e}"
            
            else:
                # Outros comandos
                os.startfile(comando)
                self.logger.info(f"Comando executado: {comando}", "ACTIONS")
                return f"{original_name.title()} acessado, senhor."
                
        except Exception as e:
            self.logger.error(e, f"Erro ao executar comando direto: {comando}", "ACTIONS")
            return f"❌ Erro ao acessar {original_name}: {e}"
    
    def _execute_hardcoded_command(self, command: str, original_name: str) -> str:
        """Executa comando hardcoded do dicionário"""
        try:
            self.logger.system(f"[DEBUG] Executando comando hardcoded: {command}", "APP")
            
            if command.startswith('start '):
                # Comando start do shell
                os.system(command)
            else:
                # Executável direto
                os.startfile(command)
            
            self.logger.info(f"Comando hardcoded executado com sucesso: {command}", "ACTIONS")
            return f"{original_name.title()} acessado, senhor."
            
        except Exception as e:
            self.logger.error(e, f"Erro ao executar comando hardcoded: {command}", "ACTIONS")
            return f"❌ Erro ao acessar {original_name}: {e}"
    
    def _execute_mapped_command(self, command: str, original_name: str) -> str:
        """Executa comando mapeado"""
        try:
            self.logger.system(f"[DEBUG] Executando comando mapeado: {command}", "APP")
            
            if command.startswith('ms-') or command == 'notepad.exe' or command == 'calc.exe' or command == 'cmd.exe':
                # Protocolos Windows e executáveis do sistema
                if command.endswith('.exe'):
                    # Executável do sistema
                    os.startfile(command)
                else:
                    # Protocolo Windows
                    os.startfile(command)
                
                self.logger.info(f"Comando executado com sucesso: {command}", "ACTIONS")
                return f"{original_name.title()} acessado, senhor."
            else:
                # Outros comandos
                os.startfile(command)
                self.logger.info(f"Comando executado com sucesso: {command}", "ACTIONS")
                return f"{original_name.title()} acessado, senhor."
                
        except Exception as e:
            self.logger.error(e, f"Erro ao executar comando mapeado: {command}", "ACTIONS")
            return f"❌ Erro ao acessar {original_name}: {e}"
    
    def _fallback_inteligente(self, app_name: str, original_name: str) -> str:
        """Fallback inteligente usando subprocess com verificação de sucesso"""
        try:
            self.logger.system(f"[DEBUG] Tentando fallback inteligente: '{app_name}'", "APP")
            
            # Tenta diferentes variações com subprocess.Popen
            variations = [
                app_name,
                app_name + '.exe',
                app_name.replace(' ', '') + '.exe',
                app_name.replace(' ', ''),
            ]
            
            for variation in variations:
                try:
                    self.logger.system(f"[DEBUG] Testando variação: '{variation}'", "APP")
                    
                    # Tenta encontrar no PATH primeiro
                    try:
                        result = subprocess.run(['where', variation], 
                                              capture_output=True, text=True, timeout=3)
                        
                        if result.returncode == 0:
                            caminho = result.stdout.strip().split('\n')[0]
                            process = subprocess.Popen([caminho], shell=False)
                            self.logger.info(f"App encontrado no PATH: {caminho}", "ACTIONS")
                            return f"{original_name.title()} acessado, senhor."
                    except:
                        pass
                    
                    # Se não encontrou no PATH, tenta execução direta
                    process = subprocess.Popen([variation], shell=False)
                    
                    # Verifica se o processo iniciou (espera um pouco)
                    try:
                        # Espera um curto período para verificar se o processo ainda está rodando
                        import time
                        time.sleep(0.5)
                        
                        # Verifica se o processo ainda está ativo
                        if process.poll() is None or process.returncode == 0:
                            self.logger.info(f"Executado com sucesso: {variation}", "ACTIONS")
                            return f"{original_name.title()} acessado, senhor."
                        else:
                            self.logger.warning(f"Processo falhou para: {variation}", "ACTIONS")
                            continue
                            
                    except:
                        continue
                        
                except Exception as e:
                    self.logger.warning(f"Falha na variação '{variation}': {e}", "APP")
                    continue
            
            # Se nada funcionou, tenta busca em pastas
            return self._fallback_search(app_name, original_name)
            
        except Exception as e:
            self.logger.error(e, f"Erro no fallback inteligente: {app_name}", "ACTIONS")
            return f"❌ Não consegui encontrar {original_name}, senhor."
    
    def _fallback_search(self, app_name: str, original_name: str) -> str:
        """Busca fallback em pastas comuns"""
        try:
            self.logger.system(f"[DEBUG] Iniciando busca fallback para: {app_name}", "APP")
            
            # Busca com where
            where_result = os.popen(f'where {app_name}').read().strip()
            if where_result:
                exe_path = where_result.split('\n')[0].strip()
                self.logger.system(f"[DEBUG] Encontrado com where: {exe_path}", "APP")
                os.startfile(exe_path)
                self.logger.info(f"Encontrado com where: {exe_path}", "ACTIONS")
                return f"{original_name.title()} acessado, senhor."
            
            # Busca em pastas conhecidas
            search_paths = [
                r"C:\Windows\System32",
                r"C:\Program Files",
                r"C:\Program Files (x86)",
                fr"C:\Users\{os.getenv('USERNAME')}\AppData\Local",
                fr"C:\Users\{os.getenv('USERNAME')}\AppData\Roaming"
            ]
            
            for path in search_paths:
                try:
                    pattern = os.path.join(path, f"*{app_name}*.exe")
                    matches = glob.glob(pattern)
                    if matches:
                        self.logger.system(f"[DEBUG] Encontrado em pasta: {matches[0]}", "APP")
                        os.startfile(matches[0])
                        self.logger.info(f"Encontrado em pasta: {matches[0]}", "ACTIONS")
                        return f"{original_name.title()} acessado, senhor."
                except Exception:
                    continue
            
            # Último recurso: busca no Google
            self.logger.system(f"[DEBUG] Último recurso: busca no Google para: {app_name}", "APP")
            import webbrowser
            search_url = f"https://www.google.com/search?q={app_name.replace(' ', '+')}"
            webbrowser.open(search_url)
            self.logger.info(f"Busca no Google realizada para: {app_name}", "ACTIONS")
            return f"Não encontrei {original_name} localmente. Buscando no Google, senhor."
            
        except Exception as e:
            self.logger.error(e, f"Erro na busca fallback: {app_name}", "ACTIONS")
            return f"❌ Erro ao buscar {original_name}: {e}"
    
    def _universal_app_search(self, app_name: str) -> str:
        """Busca universal de aplicativos usando os.startfile e protocolos do Windows"""
        app_name_lower = app_name.lower().strip()
        
        self.logger.system(f"Busca universal iniciada para: {app_name}", "APP")
        
        # Protocolos específicos do Windows (prioridade máxima)
        specific_protocols = {
            'configurações': 'ms-settings:',
            'configuracoes': 'ms-settings:',
            'settings': 'ms-settings:',
            'loja': 'ms-windows-store:',
            'store': 'ms-windows-store:',
            'microsoft store': 'ms-windows-store:',
            'calculadora': 'calc',
            'calculator': 'calc',
            'calc': 'calc',
            'painel de controle': 'control',
            'control panel': 'control',
            'notepad': 'notepad',
            'bloco de notas': 'notepad',
            'cmd': 'cmd',
            'prompt': 'cmd',
            'terminal': 'cmd',
            'powershell': 'powershell',
            'explorer': 'explorer',
            'task manager': 'taskmgr',
            'gerenciador de tarefas': 'taskmgr',
            # Deep Links Mark 12
            'atualizações': 'ms-settings:windowsupdate-action',
            'atualizacoes': 'ms-settings:windowsupdate-action',
            'windows update': 'ms-settings:windowsupdate-action',
            'update': 'ms-settings:windowsupdate-action',
            'atualizar': 'ms-settings:windowsupdate-action',
            'atualizar windows': 'ms-settings:windowsupdate-action',
            'windows defender': 'ms-settings:windowsdefender',
            'defender': 'ms-settings:windowsdefender',
            'antivírus': 'ms-settings:windowsdefender',
            'rede': 'ms-settings:network',
            'network': 'ms-settings:network',
            'conexões': 'ms-settings:network',
            'bluetooth': 'ms-settings:bluetooth',
            'som': 'ms-settings:sound',
            'áudio': 'ms-settings:sound',
            'audio': 'ms-settings:sound',
            'energia': 'ms-settings:powersleep',
            'power': 'ms-settings:powersleep',
            'bateria': 'ms-settings:powersleep',
            'notificações': 'ms-settings:notifications',
            'privacidade': 'ms-settings:privacy',
            'contas': 'ms-settings:yourinfo',
            'hora e data': 'ms-settings:dateandtime',
            'time': 'ms-settings:dateandtime',
            'data': 'ms-settings:dateandtime',
            'acessibilidade': 'ms-settings:easeofaccess'
        }
        
        # 1. Verifica se é um protocolo específico conhecido
        if app_name_lower in specific_protocols:
            protocol = specific_protocols[app_name_lower]
            try:
                self.logger.system(f"Usando os.startfile para protocolo: {protocol}", "APP")
                os.startfile(protocol)
                self.logger.info(f"Protocolo Windows executado com os.startfile: {protocol}", "ACTIONS")
                
                # Mensagem específica para cada tipo
                if app_name_lower in ['configurações', 'configuracoes', 'settings']:
                    return "Configurações acessadas, senhor."
                elif app_name_lower in ['loja', 'store', 'microsoft store']:
                    return "Microsoft Store acessada, senhor."
                elif app_name_lower in ['calculadora', 'calculator', 'calc']:
                    return "Calculadora acessada, senhor."
                else:
                    return f"{app_name.title()} acessado, senhor."
                    
            except Exception as e:
                self.logger.error(e, f"Protocolo falhou para {app_name}", "ACTIONS")
                return f"❌ Senhor, o sistema operacional recusou o protocolo. Verifique se o caminho está correto."
        
        # 2. Para outros apps, usa where para encontrar o caminho real (busca agressiva)
        try:
            self.logger.system(f"Buscando caminho com 'where {app_name_lower}'", "APP")
            where_result = os.popen(f'where {app_name_lower}').read().strip()
            
            if where_result:
                # Pega a primeira linha (caminho mais relevante)
                exe_path = where_result.split('\n')[0].strip()
                self.logger.system(f"Encontrado: {exe_path}", "APP")
                
                try:
                    os.startfile(exe_path)
                    self.logger.info(f"Aplicativo executado com os.startfile: {exe_path}", "ACTIONS")
                    return f"{app_name.title()} acessado, senhor."
                except Exception as e:
                    self.logger.error(e, f"Erro ao executar {app_name}", "ACTIONS")
                    return f"❌ Senhor, o sistema operacional recusou o protocolo. Verifique se o caminho está correto."
            else:
                self.logger.system(f"{app_name} não encontrado com 'where'", "APP")
                
        except Exception as e:
            self.logger.error(e, f"Erro no comando 'where'", "ACTIONS")
        
        # 2.1. Busca com variações do nome (busca agressiva)
        name_variations = [
            app_name_lower,
            app_name_lower.replace(' ', ''),
            app_name_lower.replace('-', ''),
            app_name_lower.replace('_', ''),
            app_name_lower + '.exe',
            app_name_lower.replace(' ', '') + '.exe'
        ]
        
        for variation in name_variations:
            try:
                self.logger.system(f"Tentando variação: 'where {variation}'", "APP")
                where_result = os.popen(f'where {variation}').read().strip()
                
                if where_result:
                    exe_path = where_result.split('\n')[0].strip()
                    self.logger.system(f"Encontrado com variação: {exe_path}", "APP")
                    
                    try:
                        os.startfile(exe_path)
                        self.logger.info(f"Aplicativo executado com variação: {exe_path}", "ACTIONS")
                        return f"{app_name.title()} acessado, senhor."
                    except Exception as e:
                        continue
                        
            except Exception:
                continue
        
        # 2.2. Caminhos absolutos conhecidos para aplicativos comuns
        known_paths = {
            'notepad': r'C:\Windows\System32\notepad.exe',
            'bloco de notas': r'C:\Windows\System32\notepad.exe',
            'calc': r'C:\Windows\System32\calc.exe',
            'calculadora': r'C:\Windows\System32\calc.exe',
            'calculator': r'C:\Windows\System32\calc.exe',
            'cmd': r'C:\Windows\System32\cmd.exe',
            'prompt': r'C:\Windows\System32\cmd.exe',
            'terminal': r'C:\Windows\System32\cmd.exe',
            'powershell': r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe',
            'explorer': r'C:\Windows\explorer.exe',
            'taskmgr': r'C:\Windows\System32\taskmgr.exe',
            'task manager': r'C:\Windows\System32\taskmgr.exe',
            'gerenciador de tarefas': r'C:\Windows\System32\taskmgr.exe',
            'mspaint': r'C:\Windows\System32\mspaint.exe',
            'paint': r'C:\Windows\System32\mspaint.exe',
            'wordpad': r'C:\Program Files\Windows NT\Accessories\wordpad.exe',
            'write': r'C:\Program Files\Windows NT\Accessories\wordpad.exe'
        }
        
        if app_name_lower in known_paths:
            known_path = known_paths[app_name_lower]
            if os.path.exists(known_path):
                try:
                    self.logger.system(f"Usando caminho conhecido: {known_path}", "APP")
                    os.startfile(known_path)
                    self.logger.info(f"Aplicativo executado com caminho conhecido: {known_path}", "ACTIONS")
                    return f"{app_name.title()} acessado, senhor."
                except Exception as e:
                    self.logger.error(e, f"Erro ao executar caminho conhecido: {known_path}", "ACTIONS")
        
        # 3. Se não encontrar com where, tenta busca direta em pastas comuns
        search_paths = [
            fr"C:\Program Files",
            fr"C:\Program Files (x86)",
            fr"C:\Users\{os.getenv('USERNAME')}\AppData\Local",
            fr"C:\Users\{os.getenv('USERNAME')}\AppData\Roaming",
            fr"C:\Users\{os.getenv('USERNAME')}\Desktop",
            "C:\\Windows\\System32"
        ]
        
        # Nomes possíveis de executáveis para buscar
        possible_names = [
            f"{app_name}.exe",
            f"{app_name_lower}.exe",
            f"{app_name.replace(' ', '')}.exe",
            f"{app_name_lower.replace(' ', '')}.exe",
            app_name,
            app_name_lower
        ]
        
        self.logger.system("Buscando em pastas do Windows...", "APP")
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
                
            for possible_name in possible_names:
                try:
                    # Busca recursiva com glob
                    pattern = os.path.join(search_path, "**", possible_name)
                    matches = glob.glob(pattern, recursive=True)
                    
                    if matches:
                        # Pega o primeiro match mais relevante
                        best_match = matches[0]
                        self.logger.system(f"Encontrado: {best_match}", "APP")
                        
                        try:
                            os.startfile(best_match)
                            self.logger.info(f"Aplicativo encontrado e executado: {best_match}", "ACTIONS")
                            return f"{app_name.title()} acessado, senhor."
                        except Exception as e:
                            self.logger.error(e, f"Erro ao executar {app_name}", "ACTIONS")
                            continue
                                
                except Exception as e:
                    continue
        
        # 4. Se for pasta, tenta abrir com explorer
        if any(keyword in app_name_lower for keyword in ['pasta', 'folder', 'downloads', 'documents', 'desktop', 'pictures', 'music', 'videos']):
            return self._open_special_folder(app_name)
        
        # 5. Busca por palavras-chave em nomes de arquivos
        self.logger.system("Busca por palavras-chave...", "APP")
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
                
            try:
                # Busca arquivos que contenham o nome do app
                pattern = os.path.join(search_path, "**", f"*{app_name_lower}*.exe")
                matches = glob.glob(pattern, recursive=True)
                
                for match in matches[:3]:  # Limita a 3 resultados mais relevantes
                    try:
                        os.startfile(match)
                        self.logger.info(f"Aplicativo encontrado por keyword: {match}", "ACTIONS")
                        return f"{app_name.title()} acessado, senhor."
                    except Exception:
                        continue
                        
            except Exception:
                continue
        
        # 6. Se nada funcionou, tenta busca no Google como último recurso
        try:
            self.logger.system(f"Tentando busca no Google para: {app_name}", "APP")
            search_url = f"https://www.google.com/search?q={app_name.replace(' ', '+')}"
            webbrowser.open(search_url)
            self.logger.info(f"Busca no Google realizada para: {app_name}", "ACTIONS")
            return f"Não encontrei {app_name} localmente. Buscando no Google, senhor."
        except Exception as e:
            self.logger.warning(f"Busca no Google falhou: {e}", "ACTIONS")
        
        # Se absolutamente nada funcionou
        self.logger.warning(f"Aplicativo não encontrado: {app_name}", "ACTIONS")
        return f"❌ Não consegui encontrar o {app_name} em seu sistema, senhor. Verifique se está instalado."
    
    def _open_special_folder(self, folder_name: str) -> str:
        """Abre pastas especiais do sistema"""
        folder_name_lower = folder_name.lower()
        
        special_folders = {
            'downloads': 'downloads',
            'documentos': 'documents',
            'documents': 'documents',
            'desktop': 'desktop',
            'área de trabalho': 'desktop',
            'imagens': 'pictures',
            'pictures': 'pictures',
            'música': 'music',
            'music': 'music',
            'vídeos': 'videos',
            'videos': 'videos'
        }
        
        if folder_name_lower in special_folders:
            folder_path = os.path.join(os.path.expanduser('~'), special_folders[folder_name_lower])
            try:
                os.startfile(folder_path)
                self.logger.info(f"Pasta aberta: {folder_path}", "ACTIONS")
                return f"Pasta {folder_name.title()} acessada, senhor."
            except Exception as e:
                self.logger.error(e, f"Erro ao abrir pasta {folder_name}", "ACTIONS")
                return f"❌ Erro ao abrir pasta {folder_name}."
        
        return "Pasta não reconhecida, senhor."
    
    def control_volume(self, action: str) -> str:
        """Controla o volume do sistema"""
        if not self.audio_available:
            return "❌ Controle de áudio não disponível."
        
        try:
            current_volume = self.volume.GetMasterVolumeLevelScalar()
            
            if action == "up":
                new_volume = min(1.0, current_volume + 0.1)
                self.volume.SetMasterVolumeLevelScalar(new_volume, None)
                self.logger.info(f"Volume aumentado: {current_volume:.1f} → {new_volume:.1f}", "ACTIONS")
                return f"Volume aumentado para {int(new_volume * 100)}%, senhor."
            
            elif action == "down":
                new_volume = max(0.0, current_volume - 0.1)
                self.volume.SetMasterVolumeLevelScalar(new_volume, None)
                self.logger.info(f"Volume diminuído: {current_volume:.1f} → {new_volume:.1f}", "ACTIONS")
                return f"Volume diminuído para {int(new_volume * 100)}%, senhor."
            
            elif action == "mute":
                self.volume.SetMute(1, None)
                self.logger.info("Volume silenciado", "ACTIONS")
                return "Volume silenciado, senhor."
            
            elif action == "unmute":
                self.volume.SetMute(0, None)
                self.logger.info("Volume ativado", "ACTIONS")
                return "Volume ativado, senhor."
            
        except Exception as e:
            self.logger.error(e, "Erro ao controlar volume", "ACTIONS")
            return f"❌ Erro ao controlar volume: {e}"
    
    def control_brightness(self, action: str) -> str:
        """Controla o brilho da tela"""
        try:
            if action == "up":
                sbc.set_brightness(sbc.get_brightness() + 10)
                self.logger.info("Brilho aumentado", "ACTIONS")
                return "Brilho aumentado, senhor."
            
            elif action == "down":
                sbc.set_brightness(max(0, sbc.get_brightness() - 10))
                self.logger.info("Brilho diminuído", "ACTIONS")
                return "Brilho diminuído, senhor."
            
            elif action == "max":
                sbc.set_brightness(100)
                self.logger.info("Brilho máximo", "ACTIONS")
                return "Brilho no máximo, senhor."
            
            elif action == "min":
                sbc.set_brightness(0)
                self.logger.info("Brilho mínimo", "ACTIONS")
                return "Brilho no mínimo, senhor."
            
        except Exception as e:
            self.logger.error(e, "Erro ao controlar brilho", "ACTIONS")
            return f"❌ Erro ao controlar brilho: {e}"
    
    def execute_power_command(self, action: str) -> str:
        """Executa comandos de energia do sistema (Mark 12)"""
        if action == "shutdown":
            return self._execute_shutdown()
        elif action == "restart":
            return self._execute_restart()
        elif action == "suspend":
            return self._execute_suspend()
        else:
            return f"❌ Comando de energia desconhecido: {action}"
    
    def _execute_shutdown(self) -> str:
        """Executa desligamento com aviso de 60 segundos"""
        self.logger.warning("🔌 COMANDO DE DESLIGAMENTO SOLICITADO", "ENERGIA")
        
        # Log de segurança
        log_entry = f"COMANDO_DESligAMENTO_SOLICITADO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.logger.info(log_entry, "ENERGIA")
        
        return "🔌 Senhor, os sistemas serão encerrados. Confirma o protocolo?"
    
    def _execute_restart(self) -> str:
        """Executa reinicialização com aviso de 60 segundos"""
        self.logger.warning("🔄 COMANDO DE REINICIALIZAÇÃO SOLICITADO", "ENERGIA")
        
        # Log de segurança
        log_entry = f"COMANDO_REINICIALIZACAO_SOLICITADO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.logger.info(log_entry, "ENERGIA")
        
        return "🔄 Senhor, os sistemas serão reiniciados. Confirma o protocolo?"
    
    def _execute_suspend(self) -> str:
        """Executa suspensão imediata"""
        self.logger.warning("😴 COMANDO DE SUSPENSÃO SOLICITADO", "ENERGIA")
        
        try:
            # Log de segurança
            log_entry = f"COMANDO_SUSPENSAO_EXECUTADO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.logger.info(log_entry, "ENERGIA")
            
            # Executa suspensão
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            return "😴 Sistema suspenso, senhor."
        except Exception as e:
            self.logger.error(e, "Erro ao suspender sistema", "ENERGIA")
            return f"❌ Erro ao suspender sistema: {e}"
    
    def confirm_power_action(self, action: str) -> str:
        """Confirma e executa ação de energia"""
        if action == "shutdown":
            try:
                self.logger.info("🔌 DESLIGAMENTO CONFIRMADO - EXECUTANDO", "ENERGIA")
                os.system('shutdown /s /t 60')
                return "🔌 Desligamento confirmado. O sistema será desligado em 60 segundos, senhor."
            except Exception as e:
                self.logger.error(e, "Erro ao executar desligamento", "ENERGIA")
                return f"❌ Erro ao executar desligamento: {e}"
                
        elif action == "restart":
            try:
                self.logger.info("🔄 REINICIALIZAÇÃO CONFIRMADA - EXECUTANDO", "ENERGIA")
                os.system('shutdown /r /t 60')
                return "🔄 Reinicialização confirmada. O sistema será reiniciado em 60 segundos, senhor."
            except Exception as e:
                self.logger.error(e, "Erro ao executar reinicialização", "ENERGIA")
                return f"❌ Erro ao executar reinicialização: {e}"
                
        else:
            return f"❌ Ação de energia não reconhecida: {action}"
    
    def execute_emergency_silence(self) -> str:
        """Executa o Protocolo Silêncio - fecha abas e silencia volume"""
        self.logger.info("🚨 PROTOCOLO SILÊNCIO ATIVADO", "EMERGÊNCIA")
        
        actions_performed = []
        errors = []
        
        # 1. Silenciar volume imediatamente
        try:
            if self.audio_available:
                self.volume.SetMute(1, None)
                actions_performed.append("Volume silenciado")
                self.logger.info("Volume silenciado no Protocolo Silêncio", "EMERGÊNCIA")
            else:
                errors.append("Controle de áudio não disponível")
        except Exception as e:
            errors.append(f"Erro ao silenciar volume: {e}")
            self.logger.error(e, "Erro no Protocolo Silêncio", "EMERGÊNCIA")
        
        # 2. Minimizar janelas abertas
        try:
            pyautogui.hotkey('win', 'd')
            actions_performed.append("Janelas minimizadas")
            self.logger.info("Janelas minimizadas no Protocolo Silêncio", "EMERGÊNCIA")
        except Exception as e:
            errors.append(f"Erro ao minimizar janelas: {e}")
            self.logger.error(e, "Erro no Protocolo Silêncio", "EMERGÊNCIA")
        
        # 3. Tentar fechar abas do navegador (Chrome, Firefox, Edge)
        browsers = ['chrome.exe', 'firefox.exe', 'msedge.exe']
        closed_browsers = []
        
        if self.wmi_available:
            try:
                c = wmi.WMI()
                for process in c.Win32_Process():
                    if process.name.lower() in browsers:
                        process.Terminate()
                        closed_browsers.append(process.name)
                
                if closed_browsers:
                    actions_performed.append(f"Navegadores fechados: {', '.join(closed_browsers)}")
                    self.logger.info(f"Navegadores fechados: {', '.join(closed_browsers)}", "EMERGÊNCIA")
            except Exception as e:
                errors.append(f"Erro ao fechar navegadores: {e}")
                self.logger.error(e, "Erro no Protocolo Silêncio", "EMERGÊNCIA")
        
        # 4. Win+D novamente para restaurar desktop
        try:
            pyautogui.hotkey('win', 'd')
            actions_performed.append("Desktop restaurado")
            self.logger.info("Desktop restaurado no Protocolo Silêncio", "EMERGÊNCIA")
        except Exception as e:
            errors.append(f"Erro ao restaurar desktop: {e}")
            self.logger.error(e, "Erro no Protocolo Silêncio", "EMERGÊNCIA")
        
        # Monta mensagem de resultado
        if actions_performed:
            result = f"🚨 Protocolo Silêncio executado: {', '.join(actions_performed)}"
            self.logger.success(f"Protocolo Silêncio executado: {', '.join(actions_performed)}", "EMERGÊNCIA")
        else:
            result = "🚨 Protocolo Silêncio executado (sem ações)"
        
        if errors:
            result += f"\n⚠️ Erros: {'; '.join(errors)}"
        
        return result
    
    # ==================== MÓDULO DE HARDWARE - MARK 13 ====================
    
    def set_volume(self, volume_percent: str) -> str:
        """Ajusta o volume do sistema em percentagem usando pycaw"""
        try:
            # Extrai número da string
            import re
            match = re.search(r'\d+', volume_percent)
            if not match:
                return "❌ Por favor, especifique um número de 0 a 100."
            
            volume = int(match.group())
            
            # Validação
            if volume < 0 or volume > 100:
                return "❌ O volume deve estar entre 0 e 100."
            
            if not AUDIO_AVAILABLE:
                return "❌ Biblioteca de áudio não disponível. Instale pycaw."
            
            # Obtém dispositivo de áudio padrão
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume_control = interface.QueryInterface(IAudioEndpointVolume)
            
            # Define o volume
            volume_control.SetMasterVolumeLevelScalar(volume / 100.0, None)
            
            self.logger.system(f"[HARDWARE] Volume ajustado para {volume}%", "ACTIONS")
            return f"🔊 Volume ajustado para {volume}%, senhor."
            
        except Exception as e:
            self.logger.error(e, "Erro ao ajustar volume", "HARDWARE")
            return f"❌ Erro ao ajustar volume: {e}"
    
    def get_system_status(self) -> str:
        """Retorna status completo do sistema (CPU, RAM, Disco)"""
        try:
            # Uso da CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Uso de Memória RAM
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            ram_used = memory.used / (1024**3)  # GB
            ram_total = memory.total / (1024**3)  # GB
            
            # Uso de Disco
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_used = disk.used / (1024**3)  # GB
            disk_total = disk.total / (1024**3)  # GB
            
            # Monta status
            status = f"""📊 **STATUS DO SISTEMA**
            
🖥️ **CPU**: {cpu_percent:.1f}%
🧠 **RAM**: {ram_percent:.1f}% ({ram_used:.1f}GB / {ram_total:.1f}GB)
💾 **Disco**: {disk_percent:.1f}% ({disk_used:.1f}GB / {disk_total:.1f}GB)
⏰ **Atualizado**: {datetime.now().strftime('%H:%M:%S')}"""
            
            # Registra no System Monitor
            self.logger.system(f"[HARDWARE] CPU: {cpu_percent:.1f}% | RAM: {ram_percent:.1f}% | Disco: {disk_percent:.1f}%", "ACTIONS")
            
            return status
            
        except Exception as e:
            self.logger.error(e, "Erro ao obter status do sistema", "HARDWARE")
            return f"❌ Erro ao obter status: {e}"
    
    def take_screenshot(self, filename: str = None) -> str:
        """Captura a tela e salva na pasta capturas"""
        try:
            # Cria pasta capturas se não existir
            capturas_dir = os.path.join(os.getcwd(), "capturas")
            os.makedirs(capturas_dir, exist_ok=True)
            
            # Gera nome do arquivo
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"captura_{timestamp}.png"
            elif not filename.endswith('.png'):
                filename += '.png'
            
            # Caminho completo
            filepath = os.path.join(capturas_dir, filename)
            
            # Captura a tela
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            self.logger.system(f"[HARDWARE] Screenshot salvo: {filepath}", "ACTIONS")
            return f"📸 Screenshot salvo em: {filepath}"
            
        except Exception as e:
            self.logger.error(e, "Erro ao capturar tela", "HARDWARE")
            return f"❌ Erro ao capturar tela: {e}"
    
    def generate_password(self, length: int = 16, include_symbols: bool = True) -> str:
        """Gera uma senha forte e segura"""
        try:
            # Define caracteres
            lowercase = string.ascii_lowercase
            uppercase = string.ascii_uppercase
            digits = string.digits
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_symbols else ""
            
            # Combina todos os caracteres
            all_chars = lowercase + uppercase + digits + symbols
            
            # Garante pelo menos um de cada tipo
            password = [
                random.choice(lowercase),
                random.choice(uppercase),
                random.choice(digits),
            ]
            
            if include_symbols:
                password.append(random.choice(symbols))
            
            # Preenche o resto
            remaining_length = length - len(password)
            password.extend(random.choices(all_chars, k=remaining_length))
            
            # Embaralha
            random.shuffle(password)
            
            # Converte para string
            final_password = ''.join(password)
            
            # Tenta copiar para clipboard
            try:
                import pyperclip
                pyperclip.copy(final_password)
                clipboard_msg = " (copiada para área de transferência)"
            except ImportError:
                clipboard_msg = ""
            
            self.logger.system(f"[UTILS] Senha gerada: {len(final_password)} caracteres", "ACTIONS")
            return f"🔐 **Senha forte gerada**{clipboard_msg}:\n`{final_password}`\n\n📏 **Comprimento**: {len(final_password)} caracteres\n🔒 **Segurança**: Alta"
            
        except Exception as e:
            self.logger.error(e, "Erro ao gerar senha", "UTILS")
            return f"❌ Erro ao gerar senha: {e}"
    
    def get_hardware_commands(self) -> Dict[str, str]:
        """Retorna dicionário de comandos de hardware disponíveis"""
        return {
            "volume": "Ajusta volume do sistema (ex: 'volume em 50')",
            "status do sistema": "Mostra uso de CPU, RAM e disco",
            "print": "Captura a tela e salva na pasta capturas",
            "screenshot": "Captura a tela e salva na pasta capturas",
            "gerar senha": "Gera uma senha forte e segura",
            "captura": "Captura a tela e salva na pasta capturas"
        }
    
    # ==================== MÓDULO DE PRODUTIVIDADE - MARK 13 FASE 2 ====================
    
    def translate_text(self, text: str, target_lang: str = 'en') -> str:
        """Traduz texto instantaneamente usando googletrans em thread separada"""
        def translate_thread():
            try:
                from googletrans import Translator
                translator = Translator()
                
                self.logger.system("[PROD] Iniciando tradução: '" + text[:50] + "...'", "ACTIONS")
                
                # Traduz para o inglês
                result = translator.translate(text, dest=target_lang)
                translated_text = result.text
                
                # Detecta idioma original
                original_lang = result.src
                
                self.logger.system(f"[PROD] Tradução concluída: {original_lang} → {target_lang}", "ACTIONS")
                
                # Atualiza resultado na interface através de callback
                if hasattr(self, 'translation_callback'):
                    self.translation_callback(f"🌍 **Tradução** ({original_lang} → {target_lang}):\n\n**Original:** {text}\n\n**Tradução:** {translated_text}")
                
            except Exception as e:
                self.logger.error(e, "Erro na tradução", "PROD")
                if hasattr(self, 'translation_callback'):
                    self.translation_callback(f"❌ Erro ao traduzir: {e}")
        
        try:
            # Executa em thread para não travar a interface
            thread = threading.Thread(target=translate_thread)
            thread.start()
            
            return "🔄 Traduzindo texto, aguarde..."
            
        except ImportError:
            return "❌ Biblioteca googletrans não disponível. Instale com: pip install googletrans==4.0.1"
    
    def set_reminder(self, time_str: str, task: str) -> str:
        """Define um lembrete rápido em thread separada"""
        def reminder_thread():
            try:
                # Extrai minutos da string
                match = re.search(r'(\d+)', time_str)
                if not match:
                    self.logger.error("Tempo inválido", "Erro no lembrete", "PROD")
                    return
                
                minutes = int(match.group())
                
                # Calcula tempo de disparo
                reminder_time = datetime.now() + timedelta(minutes=minutes)
                
                # Adiciona à lista de lembretes
                reminder_id = len(self.reminders) + 1
                self.reminders.append({
                    'id': reminder_id,
                    'task': task,
                    'time': reminder_time,
                    'minutes': minutes
                })
                
                self.logger.system(f"[PROD] Lembrete definido: '{task}' em {minutes} minutos", "ACTIONS")
                
                # Aguarda o tempo
                time.sleep(minutes * 60)
                
                # Dispara o lembrete
                self.trigger_reminder(reminder_id)
                
            except Exception as e:
                self.logger.error(e, "Erro no lembrete", "PROD")
        
        try:
            # Executa em thread
            thread = threading.Thread(target=reminder_thread)
            thread.start()
            
            return f"⏰ **Lembrete definido**: '{task}' em {time_str}"
            
        except Exception as e:
            self.logger.error(e, "Erro ao definir lembrete", "PROD")
            return f"❌ Erro ao definir lembrete: {e}"
    
    def trigger_reminder(self, reminder_id: int):
        """Dispara um lembrete específico"""
        try:
            # Encontra o lembrete
            reminder = None
            for r in self.reminders:
                if r['id'] == reminder_id:
                    reminder = r
                    break
            
            if not reminder:
                return
            
            # Remove da lista de ativos
            self.reminders = [r for r in self.reminders if r['id'] != reminder_id]
            
            # Log especial no System Monitor
            self.logger.warning(f"⏰ **LEMBRETE**: {reminder['task']} (definido há {reminder['minutes']} minutos)", "PROD")
            
            # Tenta mostrar notificação visual
            try:
                import pyautogui
                pyautogui.alert(f"⏰ Lembrete: {reminder['task']}", "J.A.R.V.I.S. - Lembrete")
            except:
                pass
            
        except Exception as e:
            self.logger.error(e, "Erro ao disparar lembrete", "PROD")
    
    def get_currency_rate(self, from_currency: str = 'USD', to_currency: str = 'BRL') -> str:
        """Obtém taxa de câmbio usando yfinance em thread separada"""
        def currency_thread():
            try:
                import yfinance as yf
                
                self.logger.system(f"[PROD] Buscando cotação: {from_currency}/{to_currency}", "ACTIONS")
                
                # Obtém cotação
                ticker = f"{from_currency}{to_currency}=X"
                data = yf.Ticker(ticker).history(period="1d")
                
                if not data.empty:
                    rate = data['Close'].iloc[-1]
                    
                    # Formatação brasileira
                    if to_currency == 'BRL':
                        formatted_rate = f"R$ {rate:.4f}"
                    else:
                        formatted_rate = f"{rate:.4f} {to_currency}"
                    
                    self.logger.system(f"[PROD] Cotação obtida: {from_currency}/{to_currency} = {formatted_rate}", "ACTIONS")
                    
                    # Atualiza através de callback
                    if hasattr(self, 'currency_callback'):
                        self.currency_callback(f"💱 **Cotação Atual**:\n\n**1 {from_currency} = {formatted_rate}**\n\n📊 **Atualizado:** {datetime.now().strftime('%H:%M:%S')}")
                else:
                    if hasattr(self, 'currency_callback'):
                        self.currency_callback(f"❌ Não foi possível obter cotação de {from_currency}/{to_currency}")
                        
            except Exception as e:
                self.logger.error(e, "Erro na cotação", "PROD")
                if hasattr(self, 'currency_callback'):
                    self.currency_callback(f"❌ Erro ao obter cotação: {e}")
        
        try:
            # Executa em thread
            thread = threading.Thread(target=currency_thread)
            thread.start()
            
            return "💱 Buscando cotação, aguarde..."
            
        except ImportError:
            return "❌ Biblioteca yfinance não disponível. Instale com: pip install yfinance"
    
    def get_weather(self, city: str = "Votorantim") -> str:
        """Obtém previsão do tempo usando OpenWeatherMap API em thread separada"""
        def weather_thread():
            try:
                # API key do OpenWeatherMap (gratuita)
                API_KEY = "bd5e378503939157ee9252cb5c08c2bb"
                BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
                
                self.logger.system(f"[PROD] Buscando clima para: {city}", "ACTIONS")
                
                # Requisição
                url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric&lang=pt_br"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extrai informações
                    temp = data['main']['temp']
                    feels_like = data['main']['feels_like']
                    humidity = data['main']['humidity']
                    description = data['weather'][0]['description']
                    city_name = data['name']
                    
                    # Formatação
                    weather_info = f"""🌤️ **Clima Atual - {city_name}**
                    
🌡️ **Temperatura:** {temp}°C (sensação de {feels_like}°C)
💧 **Umidade:** {humidity}%
☁️ **Condição:** {description.title()}
🕐 **Atualizado:** {datetime.now().strftime('%H:%M:%S')}"""
                    
                    self.logger.system(f"[PROD] Clima obtido: {temp}°C em {city_name}", "ACTIONS")
                    return weather_info
                else:
                    return f"❌ Não foi possível obter clima para {city}"
                    
            except Exception as e:
                self.logger.error(e, "Erro ao obter clima", "PROD")
                return f"❌ Erro ao obter clima: {e}"
        
        try:
            # Executa em thread
            thread = threading.Thread(target=weather_thread)
            thread.start()
            
            return f"🌤️ Buscando clima para {city}, aguarde..."
            
        except Exception as e:
            self.logger.error(e, "Erro ao iniciar busca de clima", "PROD")
            return f"❌ Erro ao buscar clima: {e}"
    
    def get_productivity_commands(self) -> Dict[str, str]:
        """Retorna dicionário de comandos de produtividade disponíveis"""
        return {
            "traduzir": "Traduz texto para inglês (ex: 'traduzir hello world')",
            "me lembre": "Define lembrete (ex: 'me lembre em 30 minutos de reunião')",
            "quanto está o dólar": "Mostra cotação atual USD/BRL",
            "tempo hoje": "Mostra previsão do tempo para Votorantim",
            "clima": "Mostra clima atual (ex: 'clima São Paulo')"
        }
    
    # ==================== MÓDULO WEB E SISTEMA AVANÇADO - MARK 13 FINAL ====================
    
    def get_weather_votorantim(self) -> str:
        """Obtém clima de Votorantim usando OpenWeatherMap API em thread separada"""
        def weather_thread():
            try:
                # API key do OpenWeatherMap (gratuita)
                API_KEY = "bd5e378503939157ee9252cb5c08c2bb"
                BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
                
                self.logger.system(f"[PROD] Buscando clima para: Votorantim", "ACTIONS")
                
                # Requisição com timeout
                url = f"{BASE_URL}?q=Votorantim,BR&appid={API_KEY}&units=metric&lang=pt_br"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extrai informações
                    temp = data['main']['temp']
                    feels_like = data['main']['feels_like']
                    humidity = data['main']['humidity']
                    description = data['weather'][0]['description']
                    city_name = data['name']
                    
                    weather_info = f"""🌤️ **Clima Atual - {city_name}**
                    
🌡️ **Temperatura:** {temp}°C (sensação de {feels_like}°C)
💧 **Umidade:** {humidity}%
☁️ **Condição:** {description.title()}
🕐 **Atualizado:** {datetime.now().strftime('%H:%M:%S')}"""
                    
                    self.logger.system(f"[PROD] Clima obtido: {temp}°C em {city_name}", "ACTIONS")
                    
                    # Atualiza através de callback
                    if hasattr(self, 'weather_callback'):
                        self.weather_callback(weather_info)
                else:
                    if hasattr(self, 'weather_callback'):
                        self.weather_callback(f"❌ Não foi possível obter clima para Votorantim")
                    
            except Exception as e:
                self.logger.error(e, "Erro ao obter clima", "PROD")
                if hasattr(self, 'weather_callback'):
                    self.weather_callback(f"❌ Erro ao obter clima: {e}")
        
        try:
            # Executa em thread
            thread = threading.Thread(target=weather_thread)
            thread.start()
            
            return f"🌤️ Buscando clima para Votorantim, aguarde..."
            
        except Exception as e:
            self.logger.error(e, "Erro ao iniciar busca de clima", "PROD")
            return f"❌ Erro ao buscar clima: {e}"
    
    def get_currency_final(self, currency: str) -> str:
        """Obtém cotação de moeda específica usando yfinance em thread separada"""
        def currency_thread():
            try:
                import yfinance as yf
                
                # Mapeamento de moedas
                currency_map = {
                    'dólar': 'USD',
                    'dolar': 'USD',
                    'euro': 'EUR',
                    'bitcoin': 'BTC',
                    'real': 'BRL',
                    'peso': 'MXN',
                    'libra': 'GBP'
                }
                
                # Normaliza o nome da moeda
                currency_lower = currency.lower()
                from_currency = currency_map.get(currency_lower, currency.upper())
                
                self.logger.system(f"[PROD] Buscando cotação: {from_currency}/BRL", "ACTIONS")
                
                # Obtém cotação
                ticker = f"{from_currency}BRL=X"
                data = yf.Ticker(ticker).history(period="1d")
                
                if not data.empty:
                    rate = data['Close'].iloc[-1]
                    
                    # Formatação brasileira
                    formatted_rate = f"R$ {rate:.4f}"
                    
                    self.logger.system(f"[PROD] Cotação obtida: {from_currency}/BRL = {formatted_rate}", "ACTIONS")
                    
                    # Atualiza através de callback
                    if hasattr(self, 'currency_callback'):
                        self.currency_callback(f"💱 **Cotação Atual - {from_currency.upper()}**:\n\n**1 {from_currency.upper()} = {formatted_rate}**\n\n📊 **Atualizado:** {datetime.now().strftime('%H:%M:%S')}")
                else:
                    if hasattr(self, 'currency_callback'):
                        self.currency_callback(f"❌ Não foi possível obter cotação de {from_currency}")
                    
            except Exception as e:
                self.logger.error(e, "Erro na cotação", "PROD")
                if hasattr(self, 'currency_callback'):
                    self.currency_callback(f"❌ Erro ao obter cotação: {e}")
        
        try:
            # Executa em thread
            thread = threading.Thread(target=currency_thread)
            thread.start()
            
            return f"💱 Buscando cotação de {currency}, aguarde..."
            
        except Exception as e:
            self.logger.error(e, "Erro ao iniciar busca de cotação", "PROD")
            return f"❌ Erro ao buscar cotação: {e}"
    
    def get_news_headlines(self) -> str:
        """Obtém as 3 principais manchetes do dia usando scraping do G1"""
        def news_thread():
            try:
                self.logger.system("[PROD] Buscando notícias principais...", "ACTIONS")
                
                # URL do G1
                url = "https://g1.globo.com/"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Busca manchetes principais
                    headlines = []
                    
                    # Tenta encontrar manchetes em diferentes seleções
                    selectors = [
                        '.feed-post-body-title',
                        '.feed-post-link',
                        'h2 a',
                        '.title a',
                        '[data-area="noticias"] h2 a'
                    ]
                    
                    for selector in selectors:
                        try:
                            elements = soup.select(selector)[:3]
                            for element in elements:
                                title = element.get_text(strip=True)
                                if title and len(title) > 10:
                                    headlines.append(f"📰 {title}")
                                    if len(headlines) >= 3:
                                        break
                            if len(headlines) >= 3:
                                break
                        except:
                            continue
                        
                        if len(headlines) >= 3:
                            break
                    
                    if not headlines:
                        headlines = ["📰 Não foi possível carregar as manchetes"]
                    
                    news_info = f"""📰 **Principais Notícias do Dia**
                    
{chr(10).join(headlines[:3])}

📊 **Fonte:** G1
🕐 **Atualizado:** {datetime.now().strftime('%H:%M:%S')}"""
                    
                    self.logger.system("[PROD] Notícias obtidas com sucesso", "ACTIONS")
                    
                    # Atualiza através de callback
                    if hasattr(self, 'news_callback'):
                        self.news_callback(news_info)
                else:
                    if hasattr(self, 'news_callback'):
                        self.news_callback("❌ Não foi possível carregar as notícias")
                    
            except Exception as e:
                self.logger.error(e, "Erro ao buscar notícias", "PROD")
                if hasattr(self, 'news_callback'):
                    self.news_callback(f"❌ Erro ao buscar notícias: {e}")
        
        try:
            # Executa em thread
            thread = threading.Thread(target=news_thread)
            thread.start()
            
            return "📰 Buscando notícias principais, aguarde..."
            
        except Exception as e:
            self.logger.error(e, "Erro ao iniciar busca de notícias", "PROD")
            return f"❌ Erro ao buscar notícias: {e}"
    
    def empty_recycle_bin(self) -> str:
        """Esvazia a lixeira do Windows"""
        try:
            self.logger.system("[PROD] Esvaziando lixeira...", "ACTIONS")
            
            # Caminho da lixeira
            import os
            recycle_bin = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', 'Recycle Bin')
            
            if os.path.exists(recycle_bin):
                # Limpa a lixeira
                import shutil
                shutil.rmtree(recycle_bin)
                
                self.logger.system("[PROD] Lixeira esvaziada com sucesso", "ACTIONS")
                return "🗑️ **Lixeira esvaziada** com sucesso!"
            else:
                return "❌ Lixeira não encontrada"
                
        except Exception as e:
            self.logger.error(e, "Erro ao esvaziar lixeira", "PROD")
            return f"❌ Erro ao esvaziar lixeira: {e}"
    
    def adjust_brightness(self, action: str) -> str:
        """Controla o brilho da tela"""
        try:
            self.logger.system(f"[PROD] Ajustando brilho: {action}", "ACTIONS")
            
            if action.lower() in ['aumentar', 'aumentar brilho', 'mais brilho', 'bright']:
                # Aumenta brilho
                current = sbc.get_brightness()
                new_brightness = min(100, current + 10)
                sbc.set_brightness(new_brightness)
                
                self.logger.system(f"[PROD] Brilho aumentado para {new_brightness}%", "ACTIONS")
                return f"💡 **Brilho aumentado** para {new_brightness}%"
                
            elif action.lower() in ['diminuir', 'diminuir brilho', 'menos brilho', 'dark']:
                # Diminui brilho
                current = sbc.get_brightness()
                new_brightness = max(0, current - 10)
                sbc.set_brightness(new_brightness)
                
                self.logger.system(f"[PROD] Brilho diminuído para {new_brightness}%", "ACTIONS")
                return f"🔅 **Brilho diminuído** para {new_brightness}%"
                
            else:
                return "❌ Comando inválido. Use 'aumentar brilho' ou 'diminuir brilho'"
                
        except Exception as e:
            self.logger.error(e, "Erro ao ajustar brilho", "PROD")
            return f"❌ Erro ao ajustar brilho: {e}"
    
    def get_top_processes(self) -> str:
        """Lista os 5 processos que mais consomem memória"""
        try:
            self.logger.system("[PROD] Listando processos mais consumidos...", "ACTIONS")
            
            # Obtém todos os processos
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    mem_info = proc.memory_info()
                    if mem_info:
                        memory_mb = mem_info.rss / (1024 * 1024)  # Convert to MB
                        processes.append({
                            'name': proc.info['name'],
                            'memory': memory_mb,
                            'pid': proc.info['pid']
                        })
                except:
                    continue
            
            # Ordena por consumo de memória (maior para menor)
            processes.sort(key=lambda x: x['memory'], reverse=True)
            
            # Pega os 5 maiores
            top_5 = processes[:5]
            
            process_info = f"""📊 **Top 5 Processos (Consumo de RAM)**
            
"""
            
            for i, proc in enumerate(top_5, 1):
                process_info += f"{i}. **{proc['name']}** - {proc['memory']:.1f} MB (PID: {proc['pid']})\n"
            
            process_info += f"""
📊 **Total RAM em uso:** {psutil.virtual_memory().percent:.1f}%
🕐 **Atualizado:** {datetime.now().strftime('%H:%M:%S')}"""
            
            self.logger.system("[PROD] Lista de processos obtida", "ACTIONS")
            return process_info
            
        except Exception as e:
            self.logger.error(e, "Erro ao listar processos", "PROD")
            return f"❌ Erro ao listar processos: {e}"
    
    def play_music(self, query: str) -> str:
        """Abre navegador com busca de música no YouTube/Spotify"""
        def music_thread():
            try:
                self.logger.system(f"[PROD] Buscando música: {query}", "ACTIONS")
                
                # Busca no YouTube
                search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                
                # Tenta abrir no navegador padrão
                import webbrowser
                webbrowser.open(search_url)
                
                self.logger.system(f"[PROD] Busca iniciada: {query}", "ACTIONS")
                
                return f"""🎵 **Buscando música**: {query}

🔍 **YouTube**: {search_url}

🎶 **Navegador aberto** com resultados da busca"""
                
            except Exception as e:
                self.logger.error(e, "Erro ao buscar música", "PROD")
                return f"❌ Erro ao buscar música: {e}"
        
        try:
            # Executa em thread
            thread = threading.Thread(target=music_thread)
            thread.start()
            
            return f"🎵 Buscando música: {query}, aguarde..."
            
        except Exception as e:
            self.logger.error(e, "Erro ao iniciar busca de música", "PROD")
            return f"❌ Erro ao buscar música: {e}"
    
    def start_pomodoro_timer(self, task: str = "Estudo") -> str:
        """Inicia um timer Pomodoro de 25 minutos"""
        def pomodoro_thread():
            try:
                self.logger.system(f"[PROD] Iniciando Pomodoro: {task}", "ACTIONS")
                
                # Timer de 25 minutos
                minutes = 25
                seconds = minutes * 60
                
                # Aguarda o tempo
                time.sleep(seconds)
                
                # Dispara o alarme
                self.logger.warning(f"⏰ **POMODORO**: {task} - 25 minutos concluídos!", "PROD")
                
                # Alerta visual
                try:
                    import pyautogui
                    pyautogui.alert(f"⏰ Pomodoro Concluído!", f"{task} - 25 minutos")
                except:
                    pass
                
                return f"⏰ **Pomodoro concluído**: {task}"
                
            except Exception as e:
                self.logger.error(e, "Erro no Pomodoro", "PROD")
                return f"❌ Erro no Pomodoro: {e}"
        
        try:
            # Executa em thread
            thread = threading.Thread(target=pomodoro_thread)
            thread.start()
            
            return f"⏰ **Pomodoro iniciado**: {task} - 25 minutos"
            
        except Exception as e:
            self.logger.error(e, "Erro ao iniciar Pomodoro", "PROD")
            return f"❌ Erro ao iniciar Pomodoro: {e}"
    
    def get_final_commands(self) -> Dict[str, str]:
        """Retorna dicionário de comandos finais disponíveis"""
        return {
            # Web
            "tempo hoje": "Mostra clima de Votorantim",
            "notícias": "Mostra 3 principais manchetes do dia",
            
            # Moedas
            "dólar": "Mostra cotação do dólar",
            "euro": "Mostra cotação do euro",
            "bitcoin": "Mostra cotação do bitcoin",
            
            # Sistema Avançado
            "limpar lixeira": "Esvazia a lixeira do Windows",
            "aumentar brilho": "Aumenta o brilho da tela",
            "diminuir brilho": "Diminui o brilho da tela",
            "processos": "Lista os 5 apps que mais consomem RAM",
            
            # Entretenimento
            "tocar": "Busca e abre música no YouTube",
            "pomodoro": "Inicia timer de estudo de 25 minutos"
        }
