#!/usr/bin/env python3
"""
Protocolo de Limpeza do Jarvis
Sistema de encerramento limpo e organizado
"""

import os
import shutil
import tempfile
import glob
import time
from datetime import datetime
from pathlib import Path

class JarvisCleanup:
    """Sistema de limpeza e encerramento do Jarvis"""
    
    def __init__(self, workspace_path=None):
        """Inicializa o sistema de limpeza"""
        self.workspace_path = workspace_path or os.getcwd()
        self.cleanup_log = []
        
    def init_cleanup_protocol(self, log_callback=None):
        """Inicia o protocolo de limpeza completo"""
        cleanup_steps = [
            ("Iniciando limpeza de sistema...", self._log_cleanup),
            ("Fechando interface gráfica...", self._cleanup_gui),
            ("Limpando arquivos temporários...", self._cleanup_temp_files),
            ("Limpando logs de erro...", self._cleanup_error_logs),
            ("Limpando caches de visão...", self._cleanup_vision_cache),
            ("Limpando projetos temporários...", self._cleanup_temp_projects),
            ("Finalizando processos...", self._cleanup_processes),
            ("Protocolo de encerramento concluído.", self._log_cleanup)
        ]
        
        results = []
        
        for message, action in cleanup_steps:
            if log_callback:
                log_callback(message, "INFO")
                
            try:
                result = action()
                results.append((message, result, True))
            except Exception as e:
                results.append((message, str(e), False))
                
        return results
        
    def _log_cleanup(self, message=""):
        """Registra mensagem de limpeza"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.cleanup_log.append(log_entry)
        print(f"🧹 {log_entry}")
        return message
        
    def _cleanup_gui(self):
        """Fecha interface gráfica"""
        try:
            # Fecha instâncias PyQt6
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'python' in proc.info['name'].lower():
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        if any('jarvis' in cmd.lower() for cmd in cmdline):
                            proc.terminate()
                            self._log_cleanup(f"Processo GUI {proc.info['pid']} encerrado")
                except:
                    pass
                    
            return "Interface gráfica encerrada"
        except ImportError:
            # Fallback se psutil não estiver disponível
            return "Interface gráfica será encerrada ao final"
        except Exception as e:
            return f"Erro ao fechar GUI: {e}"
            
    def _cleanup_temp_files(self):
        """Limpa arquivos temporários do sistema"""
        temp_patterns = [
            os.path.join(tempfile.gettempdir(), 'jarvis_*'),
            os.path.join(self.workspace_path, '*.tmp'),
            os.path.join(self.workspace_path, '*_temp*'),
            os.path.join(self.workspace_path, 'temp_*'),
            os.path.join(self.workspace_path, '*.cache')
        ]
        
        cleaned_count = 0
        cleaned_size = 0
        
        for pattern in temp_patterns:
            files = glob.glob(pattern)
            for file_path in files:
                try:
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        os.remove(file_path)
                        cleaned_count += 1
                        cleaned_size += size
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        cleaned_count += 1
                        cleaned_size += self._get_dir_size(file_path)
                except Exception as e:
                    self._log_cleanup(f"Erro ao remover {file_path}: {e}")
                    
        size_mb = cleaned_size / (1024 * 1024)
        return f"Arquivos temporários: {cleaned_count} arquivos, {size_mb:.2f} MB"
        
    def _cleanup_error_logs(self):
        """Limpa logs de erro antigos"""
        log_patterns = [
            os.path.join(self.workspace_path, 'jarvis_logs', '*error*.log'),
            os.path.join(self.workspace_path, '*error*.log'),
            os.path.join(self.workspace_path, 'debug_*error*.log')
        ]
        
        cleaned_count = 0
        
        for pattern in log_patterns:
            files = glob.glob(pattern)
            for file_path in files:
                try:
                    # Mantém apenas logs dos últimos 7 dias
                    file_time = os.path.getmtime(file_path)
                    days_old = (time.time() - file_time) / (24 * 3600)
                    
                    if days_old > 7:
                        os.remove(file_path)
                        cleaned_count += 1
                except Exception as e:
                    self._log_cleanup(f"Erro ao remover log {file_path}: {e}")
                    
        return f"Logs de erro: {cleaned_count} arquivos removidos"
        
    def _cleanup_vision_cache(self):
        """Limpa cache do sistema de visão"""
        vision_temp = os.path.join(tempfile.gettempdir(), 'jarvis_vision')
        
        if os.path.exists(vision_temp):
            try:
                files = glob.glob(os.path.join(vision_temp, '*'))
                count = len(files)
                shutil.rmtree(vision_temp)
                os.makedirs(vision_temp, exist_ok=True)
                return f"Cache de visão: {count} arquivos limpos"
            except Exception as e:
                return f"Erro ao limpar cache de visão: {e}"
        else:
            return "Cache de visão: já limpo"
            
    def _cleanup_temp_projects(self):
        """Limpa projetos temporários gerados"""
        temp_project_patterns = [
            os.path.join(self.workspace_path, '*_temp_*'),
            os.path.join(self.workspace_path, 'temp_*'),
            os.path.join(self.workspace_path, '*_project_*'),
            os.path.join(self.workspace_path, 'debug_*')
        ]
        
        cleaned_count = 0
        
        for pattern in temp_project_patterns:
            paths = glob.glob(pattern)
            for path in paths:
                try:
                    if os.path.isdir(path):
                        # Verifica se é diretório temporário
                        dir_name = os.path.basename(path)
                        if any(marker in dir_name.lower() for marker in ['temp', 'debug', 'test']):
                            shutil.rmtree(path)
                            cleaned_count += 1
                except Exception as e:
                    self._log_cleanup(f"Erro ao remover projeto {path}: {e}")
                    
        return f"Projetos temporários: {cleaned_count} diretórios removidos"
        
    def _cleanup_processes(self):
        """Finaliza processos relacionados ao Jarvis"""
        try:
            import psutil
            
            jarvis_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if any(keyword in cmd.lower() for keyword in ['jarvis', 'python.*jarvis']):
                        jarvis_processes.append(proc.info['pid'])
                except:
                    pass
                    
            # Termina processos gentilmente
            for pid in jarvis_processes:
                try:
                    proc = psutil.Process(pid)
                    proc.terminate()
                    self._log_cleanup(f"Processo {pid} finalizado")
                except:
                    pass
                    
            return f"Processos finalizados: {len(jarvis_processes)}"
        except ImportError:
            return "Finalização de processos requer psutil"
        except Exception as e:
            return f"Erro ao finalizar processos: {e}"
            
    def _get_dir_size(self, path):
        """Calcula tamanho de diretório"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        pass
        except:
            pass
        return total_size
        
    def generate_cleanup_report(self, results):
        """Gera relatório detalhado da limpeza"""
        report = f"""
RELATÓRIO DE LIMPEZA - JARVIS
{'='*50}
Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Workspace: {self.workspace_path}

DETALHES DA LIMPEZA:
{'-'*30}
"""
        
        for message, result, success in results:
            status = "✅" if success else "❌"
            report += f"{status} {message}\n"
            if result and result != message:
                report += f"   → {result}\n"
                
        report += f"\nLOG COMPLETO:\n{'-'*30}\n"
        for entry in self.cleanup_log:
            report += f"{entry}\n"
            
        # Salva relatório
        report_file = os.path.join(
            self.workspace_path, 
            f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            return report_file, report
        except Exception as e:
            return None, report

class CleanupCommandHandler:
    """Manipulador de comandos de limpeza"""
    
    def __init__(self, workspace_path=None):
        self.cleanup = JarvisCleanup(workspace_path)
        
    def process_cleanup_command(self, command, log_callback=None):
        """Processa comandos de limpeza"""
        command_lower = command.lower()
        
        # Protocolo de encerramento completo
        if any(phrase in command_lower for phrase in [
            "protocolo de encerramento", "limpar área de trabalho",
            "limpeza completa", "encerrar sistema", "shutdown limpo"
        ]):
            return self._execute_full_cleanup(log_callback)
            
        # Limpeza específica
        elif "limpar logs" in command_lower:
            return self.cleanup._cleanup_error_logs()
            
        elif "limpar temporários" in command_lower:
            return self.cleanup._cleanup_temp_files()
            
        elif "limpar cache" in command_lower:
            return self.cleanup._cleanup_vision_cache()
            
        return None
        
    def _execute_full_cleanup(self, log_callback=None):
        """Executa protocolo completo de limpeza"""
        if log_callback:
            log_callback("Iniciando Protocolo de Encerramento...", "WARNING")
            
        # Executa limpeza completa
        results = self.cleanup.init_cleanup_protocol(log_callback)
        
        # Gera relatório
        report_file, report_content = self.cleanup.generate_cleanup_report(results)
        
        if report_file:
            if log_callback:
                log_callback(f"Relatório salvo: {report_file}", "SUCCESS")
                
        return "Protocolo de encerramento concluído com sucesso."
