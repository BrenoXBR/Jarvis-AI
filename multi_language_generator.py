#!/usr/bin/env python3
"""
Multi-Language Code Generator para Jarvis
Sistema para gerar, compilar e executar código em múltiplas linguagens
"""

import os
import subprocess
import sys
import time
import re
import shutil
from datetime import datetime
from pathlib import Path
import json
from debug_mode import DebugMode

class MultiLanguageGenerator:
    def __init__(self, workspace_path=None):
        """Inicializa o gerador multi-linguagem"""
        self.workspace_path = workspace_path or os.getcwd()
        self.script_counter = 0
        self.language_configs = self._load_language_configs()
        self.installed_tools = self._detect_installed_tools()
        self.debug_mode = DebugMode(workspace_path=self.workspace_path)
        
    def _load_language_configs(self):
        """Carrega configurações para cada linguagem"""
        return {
            'python': {
                'extensions': ['.py'],
                'main_file': 'main.py',
                'compiler': None,
                'interpreter': 'python',
                'run_command': 'python {file}',
                'compile_command': None,
                'build_dir': None,
                'template': '''#!/usr/bin/env python3
"""
{description}
"""

def main():
    """Função principal"""
    print("Executando programa em Python...")
    # TODO: Implementar lógica aqui
    pass

if __name__ == "__main__":
    main()
'''
            },
            'cpp': {
                'extensions': ['.cpp', '.cc', '.cxx'],
                'main_file': 'main.cpp',
                'compiler': 'g++',
                'interpreter': None,
                'run_command': './{executable}',
                'compile_command': 'g++ -std=c++17 -o {executable} {file}',
                'build_dir': 'build',
                'template': '''#include <iostream>
#include <string>

/*
 * {description}
 */

int main() {
    std::cout << "Executando programa em C++..." << std::endl;
    
    // TODO: Implementar lógica aqui
    
    return 0;
}
'''
            },
            'javascript': {
                'extensions': ['.js', '.mjs'],
                'main_file': 'index.js',
                'compiler': None,
                'interpreter': 'node',
                'run_command': 'node {file}',
                'compile_command': None,
                'build_dir': None,
                'template': '''/**
 * {description}
 */

console.log("Executando programa em JavaScript...");

// TODO: Implementar lógica aqui
'''
            },
            'java': {
                'extensions': ['.java'],
                'main_file': 'Main.java',
                'compiler': 'javac',
                'interpreter': 'java',
                'run_command': 'java {class_name}',
                'compile_command': 'javac {file}',
                'build_dir': None,
                'template': '''/**
 * {description}
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("Executando programa em Java...");
        
        // TODO: Implementar lógica aqui
    }
}
'''
            },
            'rust': {
                'extensions': ['.rs'],
                'main_file': 'main.rs',
                'compiler': 'rustc',
                'interpreter': None,
                'run_command': './{executable}',
                'compile_command': 'rustc -o {executable} {file}',
                'build_dir': None,
                'template': '''/*
 * {description}
 */

fn main() {
    println!("Executando programa em Rust...");
    
    // TODO: Implementar lógica aqui
}
'''
            },
            'go': {
                'extensions': ['.go'],
                'main_file': 'main.go',
                'compiler': None,
                'interpreter': 'go',
                'run_command': 'go run {file}',
                'compile_command': None,
                'build_dir': None,
                'template': '''package main

import "fmt"

/*
 * {description}
 */

func main() {
    fmt.Println("Executando programa em Go...")
    
    // TODO: Implementar lógica aqui
}
'''
            },
            'c': {
                'extensions': ['.c'],
                'main_file': 'main.c',
                'compiler': 'gcc',
                'interpreter': None,
                'run_command': './{executable}',
                'compile_command': 'gcc -o {executable} {file}',
                'build_dir': None,
                'template': '''#include <stdio.h>
#include <stdlib.h>

/*
 * {description}
 */

int main() {
    printf("Executando programa em C...\\n");
    
    // TODO: Implementar lógica aqui
    
    return 0;
}
'''
            },
            'cs': {
                'extensions': ['.cs'],
                'main_file': 'Program.cs',
                'compiler': 'dotnet',
                'interpreter': 'dotnet',
                'run_command': 'dotnet run',
                'compile_command': 'dotnet build',
                'build_dir': None,
                'template': '''using System;

/*
 * {description}
 */

class Program {
    static void Main(string[] args) {
        Console.WriteLine("Executando programa em C#...");
        
        // TODO: Implementar lógica aqui
    }
}
'''
            }
        }
        
    def _detect_installed_tools(self):
        """Detecta quais compiladores/interpretadores estão instalados"""
        tools = {}
        
        for lang, config in self.language_configs.items():
            tools[lang] = {
                'compiler_available': False,
                'interpreter_available': False
            }
            
            # Verifica compilador
            if config['compiler']:
                tools[lang]['compiler_available'] = shutil.which(config['compiler']) is not None
                
            # Verifica interpretador
            if config['interpreter']:
                tools[lang]['interpreter_available'] = shutil.which(config['interpreter']) is not None
                
        return tools
        
    def detect_language_from_command(self, command):
        """Detecta a linguagem de programação mencionada no comando"""
        command_lower = command.lower()
        
        # Mapeamento de palavras-chave para linguagens
        language_keywords = {
            'python': ['python', '.py'],
            'cpp': ['c++', 'cpp', '.cpp', 'c plus plus'],
            'javascript': ['javascript', 'js', 'node', '.js', 'nodejs'],
            'java': ['java', '.java'],
            'rust': ['rust', '.rs', 'rust lang'],
            'go': ['go', 'golang', '.go'],
            'c': ['c linguagem', '.c', 'c programming'],
            'cs': ['c#', 'csharp', '.cs', 'c sharp']
        }
        
        for lang, keywords in language_keywords.items():
            for keyword in keywords:
                if keyword in command_lower:
                    return lang
                    
        # Padrão para Python se não detectar outra linguagem
        return 'python'
        
    def interpret_code_request(self, command):
        """Interpreta se o comando é uma solicitação para criar código"""
        command_lower = command.lower()
        
        # Padrões para detectar solicitações de código
        code_patterns = [
            r'crie um (?:script|programa|código) em (\w+|\w+\s*\+\s*\w+|\w+\s*\#\s*\w+) para',
            r'gere um (?:script|programa|código) em (\w+|\w+\s*\+\s*\w+|\w+\s*\#\s*\w+) para',
            r'faça um (?:script|programa|código) em (\w+|\w+\s*\+\s*\w+|\w+\s*\#\s*\w+) para',
            r'escreva um (?:script|programa|código) em (\w+|\w+\s*\+\s*\w+|\w+\s*\#\s*\w+) para',
            r'crie um (?:script|programa|código) para',
            r'gere um (?:script|programa|código) para',
            r'faça um (?:script|programa|código) para',
            r'escreva um (?:script|programa|código) para'
        ]
        
        for pattern in code_patterns:
            match = re.search(pattern, command_lower)
            if match:
                # Extrai a linguagem se especificada
                if len(match.groups()) > 0:
                    language_specified = match.group(1)
                    detected_lang = self._normalize_language_name(language_specified)
                else:
                    detected_lang = self.detect_language_from_command(command)
                
                # Extrai a tarefa
                task = self._extract_task(command, pattern)
                
                return {
                    'language': detected_lang,
                    'task': task,
                    'original_command': command
                }
                
        return None
        
    def _normalize_language_name(self, lang_name):
        """Normaliza nomes de linguagens"""
        lang_mapping = {
            'c++': 'cpp',
            'c plus plus': 'cpp',
            'javascript': 'javascript',
            'js': 'javascript',
            'nodejs': 'javascript',
            'c#': 'cs',
            'csharp': 'cs',
            'c sharp': 'cs',
            'golang': 'go'
        }
        
        return lang_mapping.get(lang_name.lower(), lang_name.lower())
        
    def _extract_task(self, command, pattern):
        """Extrai a tarefa do comando usando regex"""
        # Remove o padrão e limpa o texto
        task = re.sub(pattern, '', command, flags=re.IGNORECASE).strip()
        
        # Remove palavras desnecessárias no início
        task = re.sub(r'^(que|o|a|os|as)\s+', '', task, flags=re.IGNORECASE)
        
        return task if task else None
        
    def generate_code(self, language, task, ai_model=None):
        """Gera código para a linguagem e tarefa especificadas"""
        if not ai_model:
            return self._generate_basic_code(language, task)
            
        try:
            config = self.language_configs.get(language)
            if not config:
                return f"Linguagem {language} não suportada, mestre."
                
            # Prompt especializado para geração de código
            code_prompt = f"""
Você é um programador especialista em {language.upper()}. Gere um código completo e funcional para a seguinte tarefa:

LINGUAGEM: {language.upper()}
TAREFA: {task}

REQUISITOS:
1. Código {language.upper()} completo e funcional
2. Comente o código de forma clara e concisa
3. Inclua tratamento de erros básico se apropriado
4. Use boas práticas de programação para {language.upper()}
5. Se necessário, inclua imports/includes no início
6. O código deve ser executável diretamente
7. Use o arquivo principal: {config['main_file']}

IMPORTANTE:
- Retorne APENAS o código, sem explicações adicionais
- Não inclua marcadores como ```{language} ou ```
- O código deve estar pronto para salvar em um arquivo
- Para linguagens compiladas, inclua uma função main() adequada
"""
            
            response = ai_model.generate_content(code_prompt)
            code = response.text.strip()
            
            # Limpa o código para remover possíveis marcadores
            code = self._clean_code(code, language)
            
            return code
            
        except Exception as e:
            print(f"Erro ao gerar código com IA: {e}")
            return self._generate_basic_code(language, task)
            
    def _clean_code(self, code, language):
        """Limpa o código removendo marcadores indesejados"""
        # Remove marcadores de código
        code = re.sub(rf'```{language}\s*', '', code, flags=re.IGNORECASE)
        code = re.sub(r'```\s*$', '', code)
        
        # Remove explicações antes do código
        lines = code.split('\n')
        code_lines = []
        in_code = False
        
        # Padrões para identificar início do código por linguagem
        start_patterns = {
            'python': ['#!/usr/bin/env python3', 'import ', 'from ', 'def '],
            'cpp': ['#include', 'using namespace', 'int main('],
            'javascript': ['//', '/*', 'const ', 'let ', 'var ', 'function ', 'console.'],
            'java': ['import ', 'public class', 'public static void main'],
            'rust': ['use ', 'fn main(', 'fn '],
            'go': ['package main', 'import ', 'func main('],
            'c': ['#include', 'int main('],
            'cs': ['using ', 'namespace ', 'class ', 'static void Main']
        }
        
        patterns = start_patterns.get(language, ['#', '/*', '//', 'import', 'using'])
        
        for line in lines:
            if any(line.strip().startswith(pattern) for pattern in patterns):
                in_code = True
                
            if in_code:
                code_lines.append(line)
                
        return '\n'.join(code_lines) if code_lines else code
        
    def _generate_basic_code(self, language, task):
        """Gera um código básico quando a IA não está disponível"""
        config = self.language_configs.get(language)
        if not config:
            return f"Linguagem {language} não suportada, mestre."
            
        template = config['template']
        return template.format(description=f"Código gerado para: {task}")
        
    def create_project_structure(self, language, code, task):
        """Cria a estrutura de pastas e arquivos para o projeto"""
        try:
            config = self.language_configs.get(language)
            if not config:
                return None, f"Linguagem {language} não suportada, mestre."
                
            # Gera nome do projeto
            project_name = self._generate_project_name(language, task)
            project_path = os.path.join(self.workspace_path, project_name)
            
            # Cria diretório do projeto
            os.makedirs(project_path, exist_ok=True)
            
            # Cria diretório de build se necessário
            if config['build_dir']:
                build_path = os.path.join(project_path, config['build_dir'])
                os.makedirs(build_path, exist_ok=True)
                
            # Salva o arquivo principal
            main_file = os.path.join(project_path, config['main_file'])
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(code)
                
            return project_path, project_name
            
        except Exception as e:
            return None, f"Erro ao criar estrutura do projeto: {str(e)}"
            
    def _generate_project_name(self, language, task):
        """Gera um nome para o projeto"""
        # Remove caracteres especiais e substitui espaços por underscores
        clean_task = re.sub(r'[^\w\s]', '', task)
        clean_task = re.sub(r'\s+', '_', clean_task)
        clean_task = clean_task[:20]
        
        # Adiciona timestamp e contador
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.script_counter += 1
        
        return f"{language}_project_{clean_task}_{timestamp}_{self.script_counter}"
        
    def compile_and_run(self, project_path, language, ai_model=None):
        """Compila e executa o código na linguagem especificada"""
        config = self.language_configs.get(language)
        if not config:
            return {
                'success': False,
                'stdout': '',
                'stderr': f"Linguagem {language} não suportada",
                'returncode': -1
            }
            
        tools = self.installed_tools.get(language, {})
        
        # Verifica se as ferramentas necessárias estão disponíveis
        if config['compiler'] and not tools.get('compiler_available', False):
            return {
                'success': False,
                'stdout': '',
                'stderr': f"Compilador {config['compiler']} não encontrado. Instale-o para compilar {language}.",
                'returncode': -1
            }
            
        if config['interpreter'] and not tools.get('interpreter_available', False):
            return {
                'success': False,
                'stdout': '',
                'stderr': f"Interpretador {config['interpreter']} não encontrado. Instale-o para executar {language}.",
                'returncode': -1
            }
            
        try:
            # Para linguagens compiladas
            if config['compile_command']:
                return self._compile_and_run_compiled(project_path, config, language)
            else:
                return self._run_interpreted(project_path, config, language)
                
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': f'Erro ao executar: {str(e)}',
                'returncode': -2
            }
            
    def _compile_and_run_compiled(self, project_path, config, language):
        """Compila e executa linguagens compiladas"""
        main_file = os.path.join(project_path, config['main_file'])
        executable_name = f"program_{language}"
        
        if config['build_dir']:
            executable_path = os.path.join(project_path, config['build_dir'], executable_name)
        else:
            executable_path = os.path.join(project_path, executable_name)
            
        # Comando de compilação
        compile_cmd = config['compile_command'].format(
            file=main_file,
            executable=executable_path
        )
        
        print(f"🔨 Compilando: {compile_cmd}")
        
        # Compila
        compile_result = subprocess.run(
            compile_cmd.split(),
            capture_output=True,
            text=True,
            timeout=30,
            cwd=project_path
        )
        
        if compile_result.returncode != 0:
            return {
                'success': False,
                'stdout': compile_result.stdout,
                'stderr': compile_result.stderr,
                'returncode': compile_result.returncode,
                'compile_error': True
            }
            
        # Executa
        run_cmd = config['run_command'].format(executable=executable_path)
        print(f"🚀 Executando: {run_cmd}")
        
        run_result = subprocess.run(
            run_cmd.split(),
            capture_output=True,
            text=True,
            timeout=30,
            cwd=project_path
        )
        
        return {
            'success': run_result.returncode == 0,
            'stdout': run_result.stdout,
            'stderr': run_result.stderr,
            'returncode': run_result.returncode
        }
        
    def _run_interpreted(self, project_path, config, language):
        """Executa linguagens interpretadas"""
        main_file = os.path.join(project_path, config['main_file'])
        
        # Comando de execução
        run_cmd = config['run_command'].format(file=main_file)
        print(f"🚀 Executando: {run_cmd}")
        
        result = subprocess.run(
            run_cmd.split(),
            capture_output=True,
            text=True,
            timeout=30,
            cwd=project_path
        )
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
        
    def attempt_code_fix(self, project_path, language, error_output, original_code, ai_model=None):
        """Tenta corrigir o código com base nos erros"""
        if not ai_model:
            return None, "Correção automática requer IA, mestre."
            
        try:
            fix_prompt = f"""
Corrija o seguinte código em {language.upper()} que está apresentando erros:

LINGUAGEM: {language.upper()}
ERRO: {error_output}

CÓDIGO ORIGINAL:
```{language}
{original_code}
```

REQUISITOS:
1. Corrija todos os erros de sintaxe e lógica
2. Mantenha a funcionalidade original pretendida
3. Use boas práticas de programação para {language.upper()}
4. Retorne APENAS o código corrigido, sem explicações
5. Não inclua marcadores como ```{language}```

CÓDIGO CORRIGIDO:
"""
            
            response = ai_model.generate_content(fix_prompt)
            fixed_code = response.text.strip()
            
            # Limpa o código
            fixed_code = self._clean_code(fixed_code, language)
            
            return fixed_code, None
            
        except Exception as e:
            return None, f"Erro ao corrigir código: {str(e)}"
            
    def format_result_message(self, result, project_name, language, attempt=1):
        """Formata o resultado para exibição"""
        if result['success']:
            message = f"✅ Projeto '{project_name}' em {language.upper()} executado com sucesso, mestre."
            if result['stdout']:
                message += f" Saída: {result['stdout'][:200]}"
        else:
            if result.get('compile_error'):
                message = f"Erro de compilacao em {language.upper()} (tentativa {attempt}), mestre."
            else:
                message = f"Erro ao executar {language.upper()} (tentativa {attempt}), mestre."
                
            if result['stderr']:
                message += f" Erro: {result['stderr'][:300]}"
                
        return message
        
    def process_multi_language_request(self, command, ai_model=None, speak_callback=None):
        """Processa uma solicitação completa de geração de código multi-linguagem com debug mode"""
        # 1. Interpreta a solicitação
        request = self.interpret_code_request(command)
        if not request:
            return None
            
        language = request['language']
        task = request['task']
        
        print(f"💡 Gerando código em {language.upper()} para: {task}")
        
        # 2. Verifica se a linguagem é suportada
        if language not in self.language_configs:
            return f"Linguagem {language} não suportada, mestre. Linguagens disponíveis: {', '.join(self.language_configs.keys())}"
            
        # 3. Verifica se as ferramentas estão instaladas
        tools = self.installed_tools.get(language, {})
        if not (tools.get('compiler_available') or tools.get('interpreter_available')):
            return f"Ferramentas para {language.upper()} não encontradas, mestre. Instale o compilador/interpretador necessário."
            
        # 4. Gera o código
        code = self.generate_code(language, task, ai_model)
        if not code or "não suportada" in code:
            return code
            
        # 5. Cria a estrutura do projeto
        project_path, project_name = self.create_project_structure(language, code, task)
        if not project_path:
            return project_name
            
        print(f"📁 Projeto criado: {project_name}")
        
        # 6. Executa com Debug Mode avançado
        debug_result = self.debug_mode.debug_execution(
            project_path, language, code, task, ai_model, speak_callback
        )
        
        if debug_result['success']:
            # Gera relatório de debug
            report_file, report_content = self.debug_mode.generate_debug_report(debug_result['debug_session'])
            
            message = f"✅ Projeto '{project_name}' em {language.upper()} executado com sucesso após {debug_result['attempts']} tentativas, mestre."
            
            if report_file:
                message += f" Relatório detalhado salvo em: {report_file}"
                
            return message
        else:
            # Gera relatório mesmo em caso de falha
            report_file, report_content = self.debug_mode.generate_debug_report(debug_result['debug_session'])
            
            message = f"Nao foi possivel executar o projeto '{project_name}' apos {debug_result['attempts']} tentativas, mestre."
            
            if debug_result.get('last_error'):
                message += f" Último erro: {debug_result['last_error'][:200]}"
                
            if report_file:
                message += f" Relatório de debug salvo em: {report_file}"
                
            message += " Verifique o log detalhado para mais informações."
            
            return message
