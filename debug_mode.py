#!/usr/bin/env python3
"""
Debug Mode para Jarvis
Sistema avançado de debugging com análise de erros e autocorreção inteligente
"""

import os
import subprocess
import sys
import time
import re
import json
from datetime import datetime
from pathlib import Path
import logging

class DebugMode:
    def __init__(self, workspace_path=None, max_attempts=3):
        """Inicializa o Debug Mode"""
        self.workspace_path = workspace_path or os.getcwd()
        self.max_attempts = max_attempts
        self.debug_log = []
        self.setup_logging()
        
    def setup_logging(self):
        """Configura o sistema de logging detalhado"""
        log_dir = os.path.join(self.workspace_path, 'jarvis_logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'debug_{datetime.now().strftime("%Y%m%d")}.log')
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('JarvisDebug')
        
    def analyze_error(self, error_output, language, original_code, task):
        """Analisa o erro e extrai informações relevantes"""
        error_analysis = {
            'error_type': 'unknown',
            'error_line': None,
            'error_message': '',
            'suggested_fix': None,
            'severity': 'medium',
            'language': language
        }
        
        # Padrões de erro por linguagem
        error_patterns = {
            'python': {
                'syntax': r'File ".*", line (\d+).*SyntaxError: (.+)',
                'name': r'NameError: name \'(.+)\' is not defined',
                'type': r'TypeError: (.+)',
                'import': r'ModuleNotFoundError: No module named \'(.+)\'',
                'index': r'IndexError: (.+)',
                'key': r'KeyError: (.+)',
                'value': r'ValueError: (.+)',
                'attribute': r'AttributeError: (.+)'
            },
            'cpp': {
                'syntax': r'error: expected (.+) before',
                'compile': r'error: (.+)',
                'linker': r'undefined reference to',
                'include': r'fatal error: (.+): No such file or directory',
                'type': r'error: invalid conversion from',
                'declaration': r'error: \'(.+)\' was not declared'
            },
            'javascript': {
                'syntax': r'SyntaxError: (.+)',
                'reference': r'ReferenceError: (.+) is not defined',
                'type': r'TypeError: (.+)',
                'module': r'Error: Cannot find module',
                'json': r'SyntaxError: Unexpected token'
            },
            'java': {
                'compile': r'(.+).java:(\d+): error: (.+)',
                'class': r'java.lang.ClassNotFoundException: (.+)',
                'null': r'NullPointerException',
                'array': r'ArrayIndexOutOfBoundsException',
                'cast': r'ClassCastException'
            },
            'rust': {
                'compile': r'error\[E\d+\]: (.+)',
                'borrow': r'error\[E0308\]: (.+)',
                'move': r'error\[E0382\]: (.+)',
                'lifetime': r'error\[E0495\]: (.+)'
            },
            'go': {
                'syntax': r'syntax error: (.+)',
                'undefined': r'undefined: (.+)',
                'import': r'cannot find package',
                'type': r'cannot use (.+) as type'
            },
            'c': {
                'compile': r'error: (.+)',
                'warning': r'warning: (.+)',
                'undefined': r'undefined reference to',
                'conflict': r'conflicting types for'
            },
            'cs': {
                'compile': r'CS\d+: (.+)',
                'missing': r'CS0103: The name \'(.+)\' does not exist',
                'type': r'CS0029: Cannot implicitly convert'
            }
        }
        
        patterns = error_patterns.get(language, {})
        
        for error_type, pattern in patterns.items():
            match = re.search(pattern, error_output, re.IGNORECASE)
            if match:
                error_analysis['error_type'] = error_type
                error_analysis['error_message'] = match.group(0)
                
                # Extrai linha do erro se disponível
                if match.groups() and len(match.groups()) > 0:
                    try:
                        if error_type in ['syntax', 'compile'] and language in ['python', 'java']:
                            error_analysis['error_line'] = int(match.group(1))
                    except ValueError:
                        pass
                        
                break
                
        # Determina severidade baseada no tipo de erro
        severity_mapping = {
            'syntax': 'high',
            'compile': 'high',
            'linker': 'high',
            'import': 'medium',
            'type': 'medium',
            'name': 'medium',
            'reference': 'medium',
            'undefined': 'high',
            'null': 'medium'
        }
        
        error_analysis['severity'] = severity_mapping.get(error_analysis['error_type'], 'medium')
        
        return error_analysis
        
    def search_solution(self, error_analysis, original_code, task, ai_model=None):
        """Pesquisa solução para o erro usando a API"""
        if not ai_model:
            return None, "API não disponível para pesquisa de solução, mestre."
            
        try:
            search_prompt = f"""
Você é um especialista em debugging e programação. Analise o seguinte erro e forneça uma solução detalhada:

LINGUAGEM: {error_analysis['language'].upper()}
TIPO DE ERRO: {error_analysis['error_type']}
SEVERIDADE: {error_analysis['severity']}
MENSAGEM DE ERRO: {error_analysis['error_message']}

TAREFA ORIGINAL: {task}

CÓDIGO COM ERRO:
```
{original_code}
```

SAÍDA COMPLETA DO ERRO:
```
{error_analysis['error_message']}
```

ANÁLISE NECESSÁRIA:
1. Identifique a causa raiz do erro
2. Explique por que o erro ocorreu
3. Forneça a correção exata do código
4. Sugira melhorias para evitar erros futuros
5. Retorne APENAS o código corrigido, sem explicações adicionais

IMPORTANTE:
- Corrija APENAS o erro específico, não altere outra lógica
- Mantenha a estrutura original do código
- Use boas práticas para {error_analysis['language'].upper()}
- Não inclua marcadores como ``` ou explicações

CÓDIGO CORRIGIDO:
"""
            
            response = ai_model.generate_content(search_prompt)
            fixed_code = response.text.strip()
            
            # Limpa o código
            fixed_code = self._clean_code_response(fixed_code)
            
            return fixed_code, None
            
        except Exception as e:
            self.logger.error(f"Erro na pesquisa de solução: {str(e)}")
            return None, f"Erro ao pesquisar solução: {str(e)}"
            
    def _clean_code_response(self, code):
        """Limpa a resposta da API para extrair apenas o código"""
        # Remove marcadores de código
        code = re.sub(r'```[\w]*\s*', '', code, flags=re.IGNORECASE)
        code = re.sub(r'```\s*$', '', code)
        
        # Remove explicações antes do código
        lines = code.split('\n')
        code_lines = []
        
        # Padrões que indicam início de código
        code_start_patterns = [
            '#!/usr/bin/env',
            '#include',
            'import ',
            'from ',
            'package main',
            'using ',
            'public class',
            'function ',
            'const ',
            'let ',
            'var ',
            'def ',
            'fn ',
            'int main(',
            'static void Main(',
            'console.',
            'print(',
            'System.out.',
            'fmt.',
            'std::',
            'cout',
            'printf'
        ]
        
        in_code = False
        for line in lines:
            if any(line.strip().startswith(pattern) for pattern in code_start_patterns):
                in_code = True
                
            if in_code:
                code_lines.append(line)
                
        return '\n'.join(code_lines) if code_lines else code
        
    def attempt_fix(self, project_path, language, error_output, original_code, task, ai_model=None):
        """Tenta corrigir o código com análise avançada"""
        self.logger.info(f"Iniciando tentativa de correção para {language}")
        
        # 1. Analisa o erro
        error_analysis = self.analyze_error(error_output, language, original_code, task)
        self.logger.info(f"Erro analisado: {error_analysis}")
        
        # 2. Adiciona ao log de debug
        debug_entry = {
            'timestamp': datetime.now().isoformat(),
            'language': language,
            'error_analysis': error_analysis,
            'original_code_snippet': original_code[:200] + "..." if len(original_code) > 200 else original_code
        }
        self.debug_log.append(debug_entry)
        
        # 3. Pesquisa solução
        fixed_code, search_error = self.search_solution(error_analysis, original_code, task, ai_model)
        
        if search_error:
            self.logger.error(f"Erro na pesquisa de solução: {search_error}")
            return None, search_error
            
        if not fixed_code:
            self.logger.error("Não foi possível gerar código corrigido")
            return None, "Não foi possível gerar código corrigido, mestre."
            
        # 4. Valida a correção
        validation_result = self.validate_fix(fixed_code, original_code, error_analysis)
        
        if not validation_result['valid']:
            self.logger.warning(f"Correção inválida: {validation_result['reason']}")
            return None, f"Correção gerada é inválida: {validation_result['reason']}"
            
        self.logger.info("Correção validada com sucesso")
        return fixed_code, None
        
    def validate_fix(self, fixed_code, original_code, error_analysis):
        """Valida se a correção é adequada"""
        validation = {
            'valid': True,
            'reason': '',
            'warnings': []
        }
        
        # Verifica se o código está vazio
        if not fixed_code.strip():
            validation['valid'] = False
            validation['reason'] = "Código corrigido está vazio"
            return validation
            
        # Verifica se o código é muito diferente (possível overcorrection)
        original_lines = len(original_code.split('\n'))
        fixed_lines = len(fixed_code.split('\n'))
        
        if abs(original_lines - fixed_lines) > original_lines * 0.5:
            validation['warnings'].append("Correção alterou significativamente o código original")
            
        # Verifica se o erro específico foi corrigido
        error_type = error_analysis['error_type']
        
        if error_type == 'syntax' and error_analysis['language'] == 'python':
            # Verifica se ainda há erros de sintaxe básicos
            if re.search(r':\s*$', fixed_code, re.MULTILINE):
                validation['warnings'].append("Ainda podem existir erros de sintaxe")
                
        return validation
        
    def debug_execution(self, project_path, language, original_code, task, ai_model=None, speak_callback=None):
        """Executa o processo completo de debugging"""
        self.logger.info(f"Iniciando debug mode para {language}")
        
        if speak_callback:
            speak_callback("Iniciando modo de depuração avançada, mestre.")
            
        debug_session = {
            'start_time': datetime.now(),
            'language': language,
            'task': task,
            'attempts': [],
            'final_result': None
        }
        
        current_code = original_code
        
        for attempt in range(1, self.max_attempts + 1):
            self.logger.info(f"Tentativa {attempt}/{self.max_attempts}")
            
            if speak_callback:
                speak_callback(f"Analisando erro, tentativa {attempt} de {self.max_attempts}.")
                
            # Executa o código atual
            result = self._execute_code(project_path, language, current_code)
            
            # Registra a tentativa
            attempt_info = {
                'attempt_number': attempt,
                'success': result['success'],
                'error_output': result.get('stderr', ''),
                'stdout': result.get('stdout', ''),
                'timestamp': datetime.now()
            }
            debug_session['attempts'].append(attempt_info)
            
            if result['success']:
                debug_session['final_result'] = 'success'
                self.logger.info("Código executado com sucesso!")
                
                if speak_callback:
                    speak_callback("Código corrigido e executado com sucesso, mestre!")
                    
                return {
                    'success': True,
                    'fixed_code': current_code,
                    'attempts': attempt,
                    'debug_session': debug_session
                }
                
            # Se falhou, tenta corrigir
            if attempt < self.max_attempts:
                if speak_callback:
                    speak_callback("Erro detectado. Analisando e corrigindo...")
                    
                fixed_code, fix_error = self.attempt_fix(
                    project_path, language, result['stderr'], current_code, task, ai_model
                )
                
                if fix_error:
                    self.logger.error(f"Erro na correção: {fix_error}")
                    if speak_callback:
                        speak_callback(f"Não foi possível corrigir o erro: {fix_error}")
                    break
                    
                if fixed_code:
                    # Salva o código corrigido
                    self._save_fixed_code(project_path, language, fixed_code)
                    current_code = fixed_code
                    
                    if speak_callback:
                        speak_callback("Código corrigido. Testando novamente...")
                else:
                    self.logger.error("Não foi possível gerar código corrigido")
                    break
            else:
                if speak_callback:
                    speak_callback("Número máximo de tentativas atingido, mestre.")
                    
        debug_session['final_result'] = 'failed'
        self.logger.error("Debug session falhou após todas as tentativas")
        
        return {
            'success': False,
            'fixed_code': current_code,
            'attempts': self.max_attempts,
            'last_error': result.get('stderr', ''),
            'debug_session': debug_session
        }
        
    def _execute_code(self, project_path, language, code):
        """Executa o código e retorna o resultado"""
        try:
            # Salva o código temporariamente
            temp_file = os.path.join(project_path, f'temp_debug.{self._get_extension(language)}')
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
                
            # Executa conforme a linguagem
            if language == 'python':
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=project_path
                )
            elif language == 'javascript':
                result = subprocess.run(
                    ['node', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=project_path
                )
            elif language == 'go':
                result = subprocess.run(
                    ['go', 'run', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=project_path
                )
            else:
                # Para linguagens compiladas, precisaria de lógica mais complexa
                # Por enquanto, retorna erro
                return {
                    'success': False,
                    'stderr': f'Execução direta não implementada para {language}',
                    'stdout': '',
                    'returncode': -1
                }
                
            # Remove arquivo temporário
            try:
                os.remove(temp_file)
            except:
                pass
                
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Timeout de execução (30s)',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': f'Erro na execução: {str(e)}',
                'returncode': -2
            }
            
    def _get_extension(self, language):
        """Retorna a extensão de arquivo para a linguagem"""
        extensions = {
            'python': '.py',
            'javascript': '.js',
            'java': '.java',
            'cpp': '.cpp',
            'c': '.c',
            'rust': '.rs',
            'go': '.go',
            'cs': '.cs'
        }
        return extensions.get(language, '.txt')
        
    def _save_fixed_code(self, project_path, language, fixed_code):
        """Salva o código corrigido no arquivo principal"""
        main_files = {
            'python': 'main.py',
            'javascript': 'index.js',
            'java': 'Main.java',
            'cpp': 'main.cpp',
            'c': 'main.c',
            'rust': 'main.rs',
            'go': 'main.go',
            'cs': 'Program.cs'
        }
        
        main_file = main_files.get(language, f'main.{self._get_extension(language)}')
        file_path = os.path.join(project_path, main_file)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_code)
            return True
        except Exception as e:
            self.logger.error(f"Erro ao salvar código corrigido: {str(e)}")
            return False
            
    def generate_debug_report(self, debug_session):
        """Gera um relatório detalhado da sessão de debug"""
        report = f"""
RELATÓRIO DE DEBUG - JARVIS
{'='*50}

DATA/HORA: {debug_session['start_time'].strftime('%Y-%m-%d %H:%M:%S')}
LINGUAGEM: {debug_session['language'].upper()}
TAREFA: {debug_session['task']}
RESULTADO FINAL: {debug_session['final_result'].upper()}

TENTATIVAS:
{'-'*30}
"""
        
        for i, attempt in enumerate(debug_session['attempts'], 1):
            status = "✅ SUCESSO" if attempt['success'] else "❌ FALHA"
            report += f"""
TENTATIVA {i}:
- Status: {status}
- Timestamp: {attempt['timestamp'].strftime('%H:%M:%S')}
- Saída: {attempt['stdout'][:100] if attempt['stdout'] else 'Nenhuma'}
- Erro: {attempt['error_output'][:200] if attempt['error_output'] else 'Nenhum'}
"""
            
        # Salva o relatório
        report_dir = os.path.join(self.workspace_path, 'jarvis_logs')
        os.makedirs(report_dir, exist_ok=True)
        
        report_file = os.path.join(report_dir, f'debug_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            return report_file, report
        except Exception as e:
            self.logger.error(f"Erro ao salvar relatório: {str(e)}")
            return None, report
