#!/usr/bin/env python3
"""
Code Generator para Jarvis
Sistema para gerar, criar e testar scripts Python automaticamente
"""

import os
import subprocess
import sys
import time
import re
from datetime import datetime
from pathlib import Path

class CodeGenerator:
    def __init__(self, workspace_path=None):
        """Inicializa o Code Generator"""
        self.workspace_path = workspace_path or os.getcwd()
        self.script_counter = 0
        
    def interpret_code_request(self, command):
        """Interpreta se o comando é uma solicitação para criar código"""
        command_lower = command.lower()
        
        # Padrões para detectar solicitações de código
        code_patterns = [
            r'crie um script em python para',
            r'crie um script python para',
            r'crie um programa em python para',
            r'crie um código em python para',
            r'gere um script em python para',
            r'gere um código python para',
            r'faça um script em python para',
            r'faça um programa python para',
            r'escreva um script em python para',
            r'escreva um código python para'
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, command_lower):
                # Extrai a tarefa do comando
                task = self._extract_task(command, pattern)
                return task
                
        return None
        
    def _extract_task(self, command, pattern):
        """Extrai a tarefa do comando usando regex"""
        # Remove o padrão e limpa o texto
        task = re.sub(pattern, '', command, flags=re.IGNORECASE).strip()
        
        # Remove palavras desnecessárias no início
        task = re.sub(r'^(que|o|a|os|as)\s+', '', task, flags=re.IGNORECASE)
        
        return task if task else None
        
    def generate_code(self, task, ai_model=None):
        """Gera código Python para a tarefa especificada"""
        if not ai_model:
            return self._generate_basic_code(task)
            
        try:
            # Prompt especializado para geração de código
            code_prompt = f"""
Você é um programador Python especialista. Gere um script Python completo e funcional para a seguinte tarefa:

TAREFA: {task}

REQUISITOS:
1. Código Python 3 completo e funcional
2. Comente o código de forma clara e concisa
3. Inclua tratamento de erros básico
4. Use boas práticas de programação
5. Se necessário, inclua imports no início
6. Adicione uma função main() se apropriado
7. O código deve ser executável diretamente

IMPORTANTE:
- Retorne APENAS o código Python, sem explicações adicionais
- Não inclua marcadores como ```python ou ```
- O código deve estar pronto para salvar em um arquivo .py

Exemplo de formato esperado:
#!/usr/bin/env python3
\"\"\"
Descrição do script
\"\"\"

import os

def main():
    # código aqui
    pass

if __name__ == "__main__":
    main()
"""
            
            response = ai_model.generate_content(code_prompt)
            code = response.text.strip()
            
            # Limpa o código para remover possíveis marcadores
            code = self._clean_code(code)
            
            return code
            
        except Exception as e:
            print(f"Erro ao gerar código com IA: {e}")
            return self._generate_basic_code(task)
            
    def _clean_code(self, code):
        """Limpa o código removendo marcadores indesejados"""
        # Remove marcadores de código
        code = re.sub(r'```python\s*', '', code, flags=re.IGNORECASE)
        code = re.sub(r'```\s*$', '', code)
        
        # Remove explicações antes do código
        lines = code.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            # Procura pelo início do código (#!/usr/bin/env python3 ou import)
            if line.startswith('#!/usr/bin/env python3') or line.startswith('import') or line.startswith('from'):
                in_code = True
                
            if in_code:
                code_lines.append(line)
                
        return '\n'.join(code_lines) if code_lines else code
        
    def _generate_basic_code(self, task):
        """Gera um código básico quando a IA não está disponível"""
        return f'''#!/usr/bin/env python3
"""
Script gerado automaticamente para: {task}
"""

import os
import sys

def main():
    """Função principal do script"""
    print("Script gerado para: {task}")
    print("Este é um template básico.")
    print("Configure a API Gemini para geração avançada de código.")
    
    # TODO: Implementar a lógica para: {task}
    
if __name__ == "__main__":
    main()
'''
        
    def create_script_file(self, code, task):
        """Cria um arquivo Python com o código gerado"""
        try:
            # Gera nome de arquivo baseado na tarefa
            filename = self._generate_filename(task)
            filepath = os.path.join(self.workspace_path, filename)
            
            # Salva o código no arquivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
                
            return filepath, filename
            
        except Exception as e:
            return None, f"Erro ao criar arquivo: {str(e)}"
            
    def _generate_filename(self, task):
        """Gera um nome de arquivo baseado na tarefa"""
        # Remove caracteres especiais e substitui espaços por underscores
        clean_task = re.sub(r'[^\w\s]', '', task)
        clean_task = re.sub(r'\s+', '_', clean_task)
        
        # Limita o tamanho do nome
        clean_task = clean_task[:30]
        
        # Adiciona timestamp e contador
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.script_counter += 1
        
        filename = f"jarvis_script_{clean_task}_{timestamp}_{self.script_counter}.py"
        
        return filename
        
    def test_script(self, filepath):
        """Testa a execução do script gerado"""
        try:
            print(f"🧪 Testando script: {filepath}")
            
            # Executa o script e captura a saída
            result = subprocess.run(
                [sys.executable, filepath],
                capture_output=True,
                text=True,
                timeout=30,  # Timeout de 30 segundos
                cwd=self.workspace_path
            )
            
            success = result.returncode == 0
            
            return {
                'success': success,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Script excedeu o tempo limite de 30 segundos',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': f'Erro ao executar script: {str(e)}',
                'returncode': -2
            }
            
    def format_test_result(self, result, filename):
        """Formata o resultado do teste para exibição"""
        if result['success']:
            message = f"✅ Script '{filename}' executado com sucesso, mestre."
            if result['stdout']:
                message += f" Saída: {result['stdout'][:200]}"
        else:
            message = f"❌ Erro ao executar '{filename}', mestre."
            if result['stderr']:
                message += f" Erro: {result['stderr'][:200]}"
                
        return message
        
    def get_user_authorization(self, filename):
        """Solicita autorização do usuário para executar o script"""
        # Em um ambiente real, isso seria via voz
        # Por enquanto, retorna True para automação
        print(f"🤔 Deseja executar o script '{filename}'? (s/n)")
        print("📝 Para automação, assumindo 'sim'...")
        return True
        
    def process_code_request(self, command, ai_model=None):
        """Processa uma solicitação completa de geração de código"""
        # 1. Interpreta a solicitação
        task = self.interpret_code_request(command)
        if not task:
            return None
            
        print(f"💡 Gerando código para: {task}")
        
        # 2. Gera o código
        code = self.generate_code(task, ai_model)
        if not code:
            return "Não consegui gerar o código, mestre."
            
        # 3. Cria o arquivo
        filepath, filename_or_error = self.create_script_file(code, task)
        if not filepath:
            return filename_or_error
            
        print(f"📄 Script criado: {filename_or_error}")
        
        # 4. Solicita autorização e testa
        if self.get_user_authorization(filename_or_error):
            test_result = self.test_script(filepath)
            message = self.format_test_result(test_result, filename_or_error)
            return message
        else:
            return f"Script '{filename_or_error}' criado mas não executado por sua solicitação, mestre."
