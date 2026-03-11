"""
J.A.R.V.I.S. - Logger Module
Sistema de logging profissional para auditoria e debug
"""

import os
import sys
from datetime import datetime
from typing import Optional
import threading

class JarvisLogger:
    """Sistema de log profissional para o J.A.R.V.I.S."""
    
    def __init__(self):
        # Determina o diretório base
        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Arquivos de log
        self.log_file = os.path.join(self.base_path, 'jarvis_log.txt')
        self.error_file = os.path.join(self.base_path, 'ERRO_CRITICO.txt')
        self.system_log = os.path.join(self.base_path, 'system_log.txt')
        
        # Buffer para logs em tempo real
        self.log_buffer = []
        self.buffer_lock = threading.Lock()
        
        # Inicializa os arquivos de log
        self._init_log_files()
    
    def _init_log_files(self):
        """Inicializa todos os arquivos de log"""
        try:
            # Log principal
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    f.write("🤖 J.A.R.V.I.S. - LOG DE ATIVIDADES\n")
                    f.write("=" * 50 + "\n\n")
            
            # Log do sistema
            if not os.path.exists(self.system_log):
                with open(self.system_log, 'w', encoding='utf-8') as f:
                    f.write("🖥️ J.A.R.V.I.S. - SYSTEM MONITOR\n")
                    f.write("=" * 50 + "\n\n")
            
            # Arquivo de erro crítico
            if not os.path.exists(self.error_file):
                with open(self.error_file, 'w', encoding='utf-8') as f:
                    f.write("🤖 J.A.R.V.I.S. - REGISTRO DE ERROS CRÍTICOS\n")
                    f.write("=" * 50 + "\n\n")
                    
        except Exception as e:
            print(f"❌ Erro ao criar arquivos de log: {e}")
    
    def _write_to_buffer(self, message: str, log_type: str = "INFO"):
        """Adiciona mensagem ao buffer de logs em tempo real"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_message = f"[{timestamp}] {log_type}: {message}"
        
        with self.buffer_lock:
            self.log_buffer.append(formatted_message)
            # Mantém apenas as últimas 100 mensagens no buffer
            if len(self.log_buffer) > 100:
                self.log_buffer.pop(0)
    
    def get_buffer_logs(self, limit: int = 50) -> list:
        """Retorna as últimas mensagens do buffer"""
        with self.buffer_lock:
            return self.log_buffer[-limit:]
    
    def clear_buffer(self):
        """Limpa o buffer de logs"""
        with self.buffer_lock:
            self.log_buffer.clear()
    
    def log_info(self, message: str, module: str = "GERAL"):
        """Registra mensagem informativa"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] INFO [{module}]: {message}"
        
        try:
            # Escreve no arquivo de log principal
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
            
            # Adiciona ao buffer em tempo real
            self._write_to_buffer(message, "INFO")
            
        except Exception as e:
            print(f"❌ Erro ao registrar log: {e}")
    
    def log_error(self, error: Exception, context: str = "Desconhecido", module: str = "GERAL"):
        """Registra erro completo com traceback"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_msg = f"{type(error).__name__}: {str(error)}"
        
        # Tenta obter traceback
        try:
            import traceback
            tb = traceback.format_exc()
        except:
            tb = "Traceback não disponível"
        
        log_entry = f"[{timestamp}] ERROR [{module}]: {context}\n"
        log_entry += f"Erro: {error_msg}\n"
        log_entry += f"Traceback:\n{tb}\n"
        log_entry += "-" * 50 + "\n"
        
        try:
            # Escreve no arquivo de log principal
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
            
            # Escreve no arquivo de erros críticos
            with open(self.error_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {context}\n")
                f.write(f"Erro: {error_msg}\n")
                f.write(f"Módulo: {module}\n\n")
            
            # Adiciona ao buffer em tempo real
            self._write_to_buffer(f"ERRO em {module}: {context}", "ERROR")
            
        except Exception as e:
            print(f"❌ Erro ao registrar erro: {e}")
    
    def log_system(self, message: str, action: str = "SYSTEM"):
        """Registra ação do sistema em log específico"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {action}: {message}"
        
        try:
            # Escreve no log do sistema
            with open(self.system_log, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
            
            # Adiciona ao buffer em tempo real
            self._write_to_buffer(message, action)
            
        except Exception as e:
            print(f"❌ Erro ao registrar log do sistema: {e}")
    
    def log_warning(self, message: str, module: str = "GERAL"):
        """Registra mensagem de aviso"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] WARNING [{module}]: {message}"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
            
            # Adiciona ao buffer em tempo real
            self._write_to_buffer(message, "WARNING")
            
        except Exception as e:
            print(f"❌ Erro ao registrar aviso: {e}")
    
    def log_success(self, message: str, module: str = "GERAL"):
        """Registra mensagem de sucesso"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] SUCCESS [{module}]: {message}"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
            
            # Adiciona ao buffer em tempo real
            self._write_to_buffer(message, "SUCCESS")
            
        except Exception as e:
            print(f"❌ Erro ao registrar sucesso: {e}")
    
    # Métodos de alias para compatibilidade
    def info(self, message: str, module: str = "GERAL"):
        """Alias para log_info"""
        return self.log_info(message, module)
    
    def error(self, error: Exception, context: str = "Desconhecido", module: str = "GERAL"):
        """Alias para log_error"""
        return self.log_error(error, context, module)
    
    def warning(self, message: str, module: str = "GERAL"):
        """Alias para log_warning"""
        return self.log_warning(message, module)
    
    def system(self, message: str, action: str = "SYSTEM"):
        """Alias para log_system"""
        return self.log_system(message, action)
    
    def success(self, message: str, module: str = "GERAL"):
        """Alias para log_success"""
        return self.log_success(message, module)
