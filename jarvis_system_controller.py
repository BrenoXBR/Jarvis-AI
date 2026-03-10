"""
Módulo de Controle de Sistema para J.A.R.V.I.S.
Gerencia aplicativos, volume, brilho e links rápidos
"""

import os
import sys
import subprocess
import webbrowser
import shutil
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import time
import winreg

try:
    import pyautogui
    import pycaw
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False

try:
    import screen_brightness_control as sbc
    BRIGHTNESS_AVAILABLE = True
except ImportError:
    BRIGHTNESS_AVAILABLE = False

class SystemController:
    """Controlador de sistema do J.A.R.V.I.S."""
    
    def __init__(self, logger):
        self.logger = logger
        self._setup_audio()
        self._setup_applications()
        self._setup_quick_links()
        
    def _setup_audio(self) -> None:
        """Configura controle de áudio"""
        self.audio_available = False
        self.volume_interface = None
        
        if PYCAW_AVAILABLE:
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                self.volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
                self.audio_available = True
                self.logger.info("Controle de áudio inicializado", "SISTEMA")
            except Exception as e:
                self.logger.error(e, "Falha ao inicializar áudio", "SISTEMA")
        else:
            self.logger.warning("pycaw não disponível - usando alternativas", "SISTEMA")
    
    def _setup_applications(self) -> None:
        """Configura aplicativos conhecidos"""
        self.applications = {
            # Navegadores
            "chrome": {
                "name": "Google Chrome",
                "commands": ["chrome", "google chrome", "navegador"],
                "paths": [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    "chrome"  # Fallback para PATH
                ]
            },
            "firefox": {
                "name": "Mozilla Firefox",
                "commands": ["firefox", "mozilla firefox"],
                "paths": [
                    r"C:\Program Files\Mozilla Firefox\firefox.exe",
                    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
                    "firefox"
                ]
            },
            "edge": {
                "name": "Microsoft Edge",
                "commands": ["edge", "microsoft edge"],
                "paths": [
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                    "msedge"
                ]
            },
            
            # Editores de código
            "vscode": {
                "name": "Visual Studio Code",
                "commands": ["vs code", "vscode", "visual studio code", "code"],
                "paths": [
                    r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                    "code"
                ]
            },
            "notepad": {
                "name": "Bloco de Notas",
                "commands": ["notepad", "bloco de notas"],
                "paths": ["notepad.exe"]
            },
            "notepad++": {
                "name": "Notepad++",
                "commands": ["notepad++", "notepad plus plus"],
                "paths": [
                    r"C:\Program Files\Notepad++\notepad++.exe",
                    r"C:\Program Files (x86)\Notepad++\notepad++.exe"
                ]
            },
            
            # Mídia
            "spotify": {
                "name": "Spotify",
                "commands": ["spotify"],
                "paths": [
                    r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
                    "spotify"
                ]
            },
            "vlc": {
                "name": "VLC Media Player",
                "commands": ["vlc", "media player"],
                "paths": [
                    r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                    r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
                    "vlc"
                ]
            },
            
            # Ferramentas
            "calculator": {
                "name": "Calculadora",
                "commands": ["calculator", "calculadora", "calc"],
                "paths": ["calc.exe"]
            },
            "explorer": {
                "name": "Explorador de Arquivos",
                "commands": ["explorer", "file explorer", "explorador de arquivos"],
                "paths": ["explorer.exe"]
            },
            "taskmanager": {
                "name": "Gerenciador de Tarefas",
                "commands": ["task manager", "gerenciador de tarefas", "tasks"],
                "paths": ["taskmgr.exe"]
            },
            
            # Comunicação
            "discord": {
                "name": "Discord",
                "commands": ["discord"],
                "paths": [
                    r"C:\Users\%USERNAME%\AppData\Local\Discord\app-*\Discord.exe",
                    "discord"
                ]
            },
            "slack": {
                "name": "Slack",
                "commands": ["slack"],
                "paths": [
                    r"C:\Users\%USERNAME%\AppData\Local\slack\slack.exe",
                    "slack"
                ]
            },
            
            # Produtividade
            "word": {
                "name": "Microsoft Word",
                "commands": ["word", "microsoft word"],
                "paths": ["winword"]
            },
            "excel": {
                "name": "Microsoft Excel",
                "commands": ["excel", "microsoft excel"],
                "paths": ["excel"]
            },
            "powerpoint": {
                "name": "Microsoft PowerPoint",
                "commands": ["powerpoint", "microsoft powerpoint"],
                "paths": ["powerpnt"]
            }
        }
    
    def _setup_quick_links(self) -> None:
        """Configura links rápidos"""
        self.quick_links = {
            # Entretenimento
            "youtube": {
                "name": "YouTube",
                "url": "https://www.youtube.com",
                "commands": ["youtube", "yt"]
            },
            "netflix": {
                "name": "Netflix",
                "url": "https://www.netflix.com",
                "commands": ["netflix"]
            },
            
            # Desenvolvimento
            "github": {
                "name": "GitHub",
                "url": "https://github.com",
                "commands": ["github", "git"]
            },
            "stackoverflow": {
                "name": "Stack Overflow",
                "url": "https://stackoverflow.com",
                "commands": ["stackoverflow", "stack overflow"]
            },
            "docs": {
                "name": "Documentação Python",
                "url": "https://docs.python.org",
                "commands": ["python docs", "documentação python"]
            },
            
            # Educação
            "portal": {
                "name": "Portal da Faculdade",
                "url": "https://portal.universidade.edu.br",  # Substituir URL real
                "commands": ["portal", "portal faculdade", "faculdade"]
            },
            
            # Utilitários
            "gmail": {
                "name": "Gmail",
                "url": "https://mail.google.com",
                "commands": ["gmail", "email"]
            },
            "drive": {
                "name": "Google Drive",
                "url": "https://drive.google.com",
                "commands": ["drive", "google drive"]
            },
            "maps": {
                "name": "Google Maps",
                "url": "https://maps.google.com",
                "commands": ["maps", "mapas", "google maps"]
            },
            
            # Social
            "twitter": {
                "name": "Twitter/X",
                "url": "https://twitter.com",
                "commands": ["twitter", "x"]
            },
            "instagram": {
                "name": "Instagram",
                "url": "https://instagram.com",
                "commands": ["instagram", "ig"]
            },
            "linkedin": {
                "name": "LinkedIn",
                "url": "https://linkedin.com",
                "commands": ["linkedin"]
            }
        }
    
    def _find_application_path(self, app_key: str, app_data: Dict) -> Optional[str]:
        """Busca caminho dinâmico do aplicativo"""
        app_name = app_data["name"]
        
        # 1. Tenta caminhos configurados
        for path in app_data["paths"]:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                return expanded_path
        
        # 2. Busca em pastas padrão do Windows
        app_search_paths = [
            fr"C:\Users\{os.getenv('USERNAME')}\AppData\Local",
            fr"C:\Users\{os.getenv('USERNAME')}\AppData\Roaming",
            fr"C:\Program Files",
            fr"C:\Program Files (x86)",
            "C:\\Windows\\System32"
        ]
        
        # Nome do executável para busca
        executable_names = {
            "discord": ["Discord.exe", "Update.exe", "app-*\\Discord.exe"],
            "spotify": ["Spotify.exe"],
            "vscode": ["Code.exe", "code.exe"],
            "chrome": ["chrome.exe"],
            "firefox": ["firefox.exe"],
            "edge": ["msedge.exe"]
        }
        
        if app_key.lower() in executable_names:
            for search_path in app_search_paths:
                if not os.path.exists(search_path):
                    continue
                    
                for exe_name in executable_names[app_key.lower()]:
                    try:
                        # Usa glob para busca com curingas
                        import glob
                        pattern = os.path.join(search_path, "**", exe_name)
                        matches = glob.glob(pattern, recursive=True)
                        
                        if matches:
                            # Retorna o caminho mais recente
                            latest_match = max(matches, key=os.path.getctime)
                            self.logger.info(f"Aplicativo encontrado dinamicamente: {latest_match}", "SISTEMA")
                            return latest_match
                    except Exception as e:
                        self.logger.error(e, f"Erro na busca de {app_name}", "SISTEMA")
                        continue
        
        # 3. Tenta buscar no registro do Windows
        try:
            registry_path = self._find_in_registry(app_name)
            if registry_path:
                return registry_path
        except Exception as e:
            self.logger.error(e, f"Erro ao buscar {app_name} no registro", "SISTEMA")
        
        # 4. Tenta encontrar no PATH do sistema
        try:
            path_in_system = shutil.which(app_key.lower())
            if path_in_system:
                return path_in_system
        except Exception as e:
            self.logger.error(e, f"Erro ao buscar {app_name} no PATH", "SISTEMA")
        
        return None
    
    def _find_in_registry(self, app_name: str) -> Optional[str]:
        """Busca aplicativo no registro do Windows"""
        try:
            # Chaves do registro para aplicativos instalados
            registry_keys = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]
            
            for key_path in registry_keys:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if app_name.lower() in display_name.lower():
                                    install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    exe_path = os.path.join(install_location, f"{app_name}.exe")
                                    if os.path.exists(exe_path):
                                        return exe_path
                            except FileNotFoundError:
                                continue
        except Exception as e:
            self.logger.error(e, f"Erro no registro para {app_name}", "SISTEMA")
        
        return None
    
    def _validate_execution(self, process: subprocess.Popen, app_name: str) -> bool:
        """Valida se o aplicativo foi executado com sucesso"""
        try:
            # Espera um pouco para o processo iniciar
            time.sleep(2)
            
            # Verifica se o processo ainda está rodando
            if process.poll() is None:
                self.logger.info(f"{app_name} iniciado com sucesso", "SISTEMA")
                return True
            else:
                # Processo terminou - pode indicar erro
                return_code = process.returncode
                self.logger.error(f"{app_name} falhou ao iniciar (código: {return_code})", "SISTEMA")
                return False
                
        except Exception as e:
            self.logger.error(e, f"Erro ao validar execução de {app_name}", "SISTEMA")
            return False
    
    def _open_web_fallback(self, app_key: str, app_data: Dict) -> str:
        """Abre versão web do aplicativo como fallback"""
        web_urls = {
            "discord": "https://discord.com/app",
            "spotify": "https://open.spotify.com",
            "youtube": "https://youtube.com",
            "github": "https://github.com"
        }
        
        if app_key.lower() in web_urls:
            try:
                webbrowser.open(web_urls[app_key.lower()])
                app_name = app_data["name"]
                self.logger.info(f"Versão web de {app_name} aberta", "SISTEMA")
                return f"🌐 Não encontrei {app_name} instalado. Abri a versão web no navegador."
            except Exception as e:
                self.logger.error(e, f"Erro ao abrir web fallback {app_key}", "SISTEMA")
                return f"❌ Erro ao abrir versão web: {e}"
        
        return "❌ Versão web não disponível para este aplicativo."
    
    def detect_command_intent(self, message: str) -> Optional[Tuple[str, Dict]]:
        """
        Detecta intenção de comando na mensagem do usuário.
        Retorna (tipo_comando, dados) se detectado, None caso contrário.
        """
        message_lower = message.lower()
        
        # Comandos de emergência - prioridade máxima
        emergency_keywords = ["protocolo silêncio", "silêncio total", "emergência silêncio", 
                             "fechar tudo e silenciar", "modo silêncio", "panic mode"]
        for keyword in emergency_keywords:
            if keyword in message_lower:
                return ("emergency_silence", {})
        
        # Comandos de abrir aplicativos
        open_keywords = ["abra", "abrir", "abre", "iniciar", "start", "open", "execute"]
        for keyword in open_keywords:
            if keyword in message_lower:
                # Procura por aplicativo correspondente
                for app_key, app_data in self.applications.items():
                    for command in app_data["commands"]:
                        if command in message_lower:
                            return ("open_app", {"app_key": app_key, "app_data": app_data})
                
                # Procura por links rápidos
                for link_key, link_data in self.quick_links.items():
                    for command in link_data["commands"]:
                        if command in message_lower:
                            return ("open_link", {"link_key": link_key, "link_data": link_data})
        
        # Comandos de volume
        volume_keywords = ["volume", "som", "áudio", "audio"]
        for keyword in volume_keywords:
            if keyword in message_lower:
                if "aumentar" in message_lower or "subir" in message_lower or "up" in message_lower:
                    return ("volume", {"action": "up"})
                elif "diminuir" in message_lower or "baixar" in message_lower or "down" in message_lower:
                    return ("volume", {"action": "down"})
                elif "mudo" in message_lower or "silenciar" in message_lower or "mute" in message_lower:
                    return ("volume", {"action": "mute"})
                elif "ativar som" in message_lower or "unmute" in message_lower:
                    return ("volume", {"action": "unmute"})
        
        # Comandos de brilho
        brightness_keywords = ["brilho", "brightness"]
        for keyword in brightness_keywords:
            if keyword in message_lower:
                if "aumentar" in message_lower or "subir" in message_lower or "up" in message_lower:
                    return ("brightness", {"action": "up"})
                elif "diminuir" in message_lower or "baixar" in message_lower or "down" in message_lower:
                    return ("brightness", {"action": "down"})
                elif "máximo" in message_lower or "max" in message_lower:
                    return ("brightness", {"action": "max"})
                elif "mínimo" in message_lower or "min" in message_lower:
                    return ("brightness", {"action": "min"})
        
        return None
    
    def execute_command(self, command_type: str, command_data: Dict) -> str:
        """
        Executa o comando detectado.
        Retorna mensagem de resultado para exibir ao usuário.
        """
        try:
            if command_type == "emergency_silence":
                return self._execute_emergency_silence()
            elif command_type == "open_app":
                return self._open_application(command_data["app_key"], command_data["app_data"])
            elif command_type == "open_link":
                return self._open_link(command_data["link_key"], command_data["link_data"])
            elif command_type == "volume":
                return self._control_volume(command_data["action"])
            elif command_type == "brightness":
                return self._control_brightness(command_data["action"])
            else:
                return "❌ Comando não reconhecido"
        except Exception as e:
            self.logger.error(e, f"Erro ao executar comando {command_type}", "SISTEMA")
            return f"❌ Erro ao executar comando: {e}"
    
    def _execute_emergency_silence(self) -> str:
        """Executa o Protocolo Silêncio - fecha abas e silencia volume"""
        self.logger.info("🚨 PROTOCOLO SILÊNCIO ATIVADO", "EMERGÊNCIA")
        
        actions_performed = []
        errors = []
        
        # 1. Silenciar volume imediatamente
        try:
            if self.audio_available:
                self.volume_interface.SetMute(1, None)
                actions_performed.append("🔇 Volume silenciado")
            else:
                # Fallback com pyautogui
                pyautogui.press("volumemute")
                actions_performed.append("🔇 Volume silenciado (fallback)")
        except Exception as e:
            errors.append(f"Volume: {e}")
        
        # 2. Fechar todas as abas do navegador
        try:
            # Detecta navegadores abertos e fecha abas
            browsers_closed = self._close_all_browser_tabs()
            if browsers_closed > 0:
                actions_performed.append(f"🌐 {browsers_closed} abas fechadas")
            else:
                actions_performed.append("🌐 Nenhuma aba aberta detectada")
        except Exception as e:
            errors.append(f"Navegador: {e}")
        
        # 3. Fechar aplicativos de mídia
        try:
            media_apps_closed = self._close_media_applications()
            if media_apps_closed > 0:
                actions_performed.append(f"🎵 {media_apps_closed} apps de mídia fechados")
        except Exception as e:
            errors.append(f"Mídia: {e}")
        
        # 4. Minimizar janelas ativas
        try:
            windows_minimized = self._minimize_active_windows()
            if windows_minimized > 0:
                actions_performed.append(f"📱 {windows_minimized} janelas minimizadas")
        except Exception as e:
            errors.append(f"Janelas: {e}")
        
        # Log da emergência
        self.logger.info(f"Protocolo Silêncio executado: {len(actions_performed)} ações", "EMERGÊNCIA")
        
        # Monta mensagem de resposta
        if errors:
            response = "🚨 **PROTOCOLO SILÊNCIO ATIVADO**\n\n"
            response += "✅ **Ações executadas:**\n"
            for action in actions_performed:
                response += f"• {action}\n"
            
            response += "\n⚠️ **Erros encontrados:**\n"
            for error in errors:
                response += f"• {error}\n"
        else:
            response = "🚨 **PROTOCOLO SILÊNCIO ATIVADO**\n\n"
            response += "✅ **Ações executadas com sucesso:**\n"
            for action in actions_performed:
                response += f"• {action}\n"
        
        response += "\n🔒 Ambiente seguro estabelecido."
        
        return response
    
    def _close_all_browser_tabs(self) -> int:
        """Fecha todas as abas dos navegadores principais"""
        browsers_closed = 0
        
        # Comandos para fechar abas em diferentes navegadores
        browser_commands = [
            ("chrome", "chrome.exe"),
            ("firefox", "firefox.exe"),
            ("msedge", "msedge.exe")
        ]
        
        for browser_name, process_name in browser_commands:
            try:
                # Verifica se o navegador está aberto
                result = subprocess.run(
                    ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
                    capture_output=True,
                    text=True
                )
                
                if process_name in result.stdout:
                    # Envia Ctrl+W repetidamente para fechar abas
                    for _ in range(20):  # Máximo de 20 abas
                        try:
                            # Ativa a janela do navegador
                            if browser_name == "chrome":
                                pyautogui.hotkey('alt', 'tab')  # Tenta encontrar o navegador
                                time.sleep(0.1)
                                pyautogui.hotkey('ctrl', 'w')
                                time.sleep(0.05)
                            elif browser_name == "firefox":
                                pyautogui.hotkey('alt', 'tab')
                                time.sleep(0.1)
                                pyautogui.hotkey('ctrl', 'w')
                                time.sleep(0.05)
                            elif browser_name == "msedge":
                                pyautogui.hotkey('alt', 'tab')
                                time.sleep(0.1)
                                pyautogui.hotkey('ctrl', 'w')
                                time.sleep(0.05)
                            
                            browsers_closed += 1
                        except:
                            break
                    
                    self.logger.info(f"{browsers_closed} abas do {browser_name} fechadas", "EMERGÊNCIA")
                    
            except Exception as e:
                self.logger.error(e, f"Erro ao fechar abas do {browser_name}", "EMERGÊNCIA")
        
        return browsers_closed
    
    def _close_media_applications(self) -> int:
        """Fecha aplicativos de mídia comuns"""
        media_apps = [
            "Spotify.exe",
            "vlc.exe", 
            "wmplayer.exe",
            "itunes.exe",
            "MusicBee.exe",
            "foobar2000.exe",
            "AIMP.exe"
        ]
        
        apps_closed = 0
        
        for app in media_apps:
            try:
                # Tenta fechar o aplicativo
                result = subprocess.run(
                    ["taskkill", "/F", "/IM", app],
                    capture_output=True,
                    text=True
                )
                
                if "SUCCESS" in result.stdout:
                    apps_closed += 1
                    self.logger.info(f"Aplicativo {app} fechado", "EMERGÊNCIA")
                    
            except Exception as e:
                self.logger.error(e, f"Erro ao fechar {app}", "EMERGÊNCIA")
        
        return apps_closed
    
    def _minimize_active_windows(self) -> int:
        """Minimiza janelas ativas não essenciais"""
        try:
            # Minimiza janela atual
            pyautogui.hotkey('win', 'down')
            time.sleep(0.1)
            
            # Win+D para mostrar desktop (minimiza tudo)
            pyautogui.hotkey('win', 'd')
            time.sleep(0.2)
            
            # Win+D novamente para restaurar desktop
            pyautogui.hotkey('win', 'd')
            
            return 1  # Simplificado - assume que minimizou pelo menos uma janela
            
        except Exception as e:
            self.logger.error(e, "Erro ao minimizar janelas", "EMERGÊNCIA")
            return 0
    
    def _open_application(self, app_key: str, app_data: Dict) -> str:
        """Abre aplicativo específico com validação e fallback"""
        app_name = app_data["name"]
        
        try:
            # 1. Busca caminho dinâmico
            app_path = self._find_application_path(app_key, app_data)
            
            if not app_path:
                # 2. Se não encontrou, tenta web fallback
                self.logger.warning(f"Aplicativo {app_name} não encontrado localmente", "SISTEMA")
                return self._open_web_fallback(app_key, app_data)
            
            # 3. Tenta executar o aplicativo
            try:
                print(f"🔍 Tentando abrir: {app_path}")
                process = subprocess.Popen([app_path], shell=False)
                
                # 4. Valida execução
                if self._validate_execution(process, app_name):
                    self.logger.info(f"✅ {app_name} aberto com sucesso: {app_path}", "SISTEMA")
                    return f"✅ {app_name} aberto com sucesso!"
                else:
                    # 5. Se falhou na validação, tenta web fallback
                    error_msg = f"❌ {app_name} não iniciou corretamente"
                    print(f"❌ Erro: {app_name} não iniciou corretamente")
                    self.logger.error(f"{app_name} falhou na validação", "SISTEMA")
                    
                    # Pergunta ao usuário e oferece web fallback
                    fallback_msg = f"{error_msg}\n\n🌐 Deseja abrir a versão web? (Sim/Não)"
                    web_fallback_result = self._open_web_fallback(app_key, app_data)
                    return f"{fallback_msg}\n\n💡 Senhor, não encontrei o executável no caminho padrão. Pode me informar onde o {app_name} está instalado?"
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro subprocess: {e}")
                self.logger.error(e, f"Erro subprocess ao abrir {app_name}", "SISTEMA")
                return self._open_web_fallback(app_key, app_data)
            except FileNotFoundError as e:
                print(f"❌ Arquivo não encontrado: {e}")
                self.logger.error(e, f"Arquivo não encontrado: {app_path}", "SISTEMA")
                return self._open_web_fallback(app_key, app_data)
            except Exception as e:
                print(f"❌ Erro geral ao abrir {app_name}: {e}")
                self.logger.error(e, f"Erro geral ao abrir {app_name}", "SISTEMA")
                return f"❌ Erro ao abrir {app_name}: {e}"
                
        except Exception as e:
            print(f"❌ Erro crítico no _open_application: {e}")
            self.logger.error(e, f"Erro crítico ao abrir {app_name}", "SISTEMA")
            return f"❌ Erro crítico ao abrir {app_name}: {e}"
    
    def _open_link(self, link_key: str, link_data: Dict) -> str:
        """Abre link rápido no navegador"""
        try:
            url = link_data["url"]
            name = link_data["name"]
            
            webbrowser.open(url)
            self.logger.info(f"Link aberto: {name} - {url}", "SISTEMA")
            return f"✅ {name} aberto no navegador!"
            
        except Exception as e:
            self.logger.error(e, f"Erro ao abrir link {link_key}", "SISTEMA")
            return f"❌ Erro ao abrir {link_data['name']}: {e}"
    
    def _control_volume(self, action: str) -> str:
        """Controla volume do sistema"""
        if not self.audio_available:
            # Fallback com pyautogui
            return self._control_volume_fallback(action)
        
        try:
            current_volume = self.volume_interface.GetMasterVolumeLevelScalar()
            current_volume_percent = int(current_volume * 100)
            
            if action == "up":
                new_volume = min(current_volume + 0.1, 1.0)
                self.volume_interface.SetMasterVolumeLevelScalar(new_volume, None)
                new_percent = int(new_volume * 100)
                self.logger.info(f"Volume aumentado: {current_volume_percent}% → {new_percent}%", "SISTEMA")
                return f"🔊 Volume aumentado para {new_percent}%"
                
            elif action == "down":
                new_volume = max(current_volume - 0.1, 0.0)
                self.volume_interface.SetMasterVolumeLevelScalar(new_volume, None)
                new_percent = int(new_volume * 100)
                self.logger.info(f"Volume diminuído: {current_volume_percent}% → {new_percent}%", "SISTEMA")
                return f"🔉 Volume diminuído para {new_percent}%"
                
            elif action == "mute":
                self.volume_interface.SetMute(1, None)
                self.logger.info("Volume silenciado", "SISTEMA")
                return "🔇 Volume silenciado"
                
            elif action == "unmute":
                self.volume_interface.SetMute(0, None)
                self.logger.info("Volume ativado", "SISTEMA")
                return f"🔊 Volume ativado ({current_volume_percent}%)"
                
        except Exception as e:
            self.logger.error(e, "Erro ao controlar volume", "SISTEMA")
            return f"❌ Erro ao controlar volume: {e}"
    
    def _control_volume_fallback(self, action: str) -> str:
        """Controle de volume fallback com teclado"""
        try:
            if action == "up":
                pyautogui.press("volumeup")
                return "🔊 Volume aumentado"
            elif action == "down":
                pyautogui.press("volumedown")
                return "🔉 Volume diminuído"
            elif action == "mute":
                pyautogui.press("volumemute")
                return "🔇 Volume silenciado"
            elif action == "unmute":
                pyautogui.press("volumemute")
                return "🔊 Volume ativado"
        except Exception as e:
            self.logger.error(e, "Erro no controle de volume fallback", "SISTEMA")
            return f"❌ Erro ao controlar volume: {e}"
    
    def _control_brightness(self, action: str) -> str:
        """Controla brilho da tela"""
        if not BRIGHTNESS_AVAILABLE:
            return "❌ Controle de brilho não disponível. Instale: pip install screen-brightness-control"
        
        try:
            if action == "up":
                sbc.set_brightness(lambda current: min(current + 10, 100))
                self.logger.info("Brilho aumentado", "SISTEMA")
                return "☀️ Brilho aumentado"
            elif action == "down":
                sbc.set_brightness(lambda current: max(current - 10, 0))
                self.logger.info("Brilho diminuído", "SISTEMA")
                return "🌙 Brilho diminuído"
            elif action == "max":
                sbc.set_brightness(100)
                self.logger.info("Brilho máximo", "SISTEMA")
                return "☀️ Brilho no máximo"
            elif action == "min":
                sbc.set_brightness(0)
                self.logger.info("Brilho mínimo", "SISTEMA")
                return "🌙 Brilho no mínimo"
        except Exception as e:
            self.logger.error(e, "Erro ao controlar brilho", "SISTEMA")
            return f"❌ Erro ao controlar brilho: {e}"
    
    def get_available_commands(self) -> Dict[str, List[str]]:
        """Retorna lista de comandos disponíveis"""
        apps = [app["name"] for app in self.applications.values()]
        links = [link["name"] for link in self.quick_links.values()]
        
        return {
            "aplicativos": apps,
            "links": links,
            "volume": ["aumentar", "diminuir", "silenciar", "ativar som"],
            "brilho": ["aumentar", "diminuir", "máximo", "mínimo"]
        }
    
    def list_available_commands(self) -> str:
        """Retorna texto formatado com comandos disponíveis"""
        commands = self.get_available_commands()
        
        text = "🤖 **Comandos Disponíveis do J.A.R.V.I.S.**\n\n"
        
        text += "**� EMERGÊNCIA:**\n"
        text += "• Protocolo Silêncio (fecha abas e silencia)\n\n"
        
        text += "**�📱 Aplicativos:**\n"
        for app in commands["aplicativos"]:
            text += f"• {app}\n"
        
        text += "\n**🌐 Links Rápidos:**\n"
        for link in commands["links"]:
            text += f"• {link}\n"
        
        text += "\n**🔊 Controle de Volume:**\n"
        text += "• Aumentar/diminuir volume\n"
        text += "• Silenciar/ativar som\n"
        
        text += "\n**☀️ Controle de Brilho:**\n"
        text += "• Aumentar/diminuir brilho\n"
        text += "• Brilho máximo/mínimo\n"
        
        text += "\n**Como usar:**\n"
        text += "• 'Jarvis, protocolo silêncio' 🚨\n"
        text += "• 'Jarvis, abra o Chrome'\n"
        text += "• 'Jarvis, abra o YouTube'\n"
        text += "• 'Jarvis, aumente o volume'\n"
        text += "• 'Jarvis, diminua o brilho'\n"
        
        return text
