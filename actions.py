"""
J.A.R.V.I.S. - System Actions Module
Funções de controle do Windows e aplicações
"""

import os
import subprocess
import webbrowser
import glob
import shutil
from datetime import datetime
from typing import Optional, Dict, List
import pyautogui
import screen_brightness_control as sbc
import re
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
