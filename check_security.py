#!/usr/bin/env python3
"""
Script de verificação de segurança para J.A.R.V.I.S. Mark 13
Verifica se há chaves de API expostas nos arquivos do projeto
"""

import os
import re
import sys
from pathlib import Path

# Padrões de chaves de API perigosas
API_PATTERNS = [
    r'AIza[0-9A-Za-z_-]{35}',  # Google Gemini API Key
    r'ghp_[a-zA-Z0-9]{36}',    # GitHub Personal Access Token
    r'sk-[a-zA-Z0-9]{48}',      # OpenAI API Key
    r'xoxb-[0-9]{13}-[0-9]{13}-[a-zA-Z0-9]{24}',  # Slack Bot Token
    r'[a-zA-Z0-9]{32}-[a-zA-Z0-9]{32}',  # Generic API Key pattern
]

# Arquivos para ignorar
IGNORE_EXTENSIONS = {'.pyc', '.pyo', '.log', '.exe', '.png', '.jpg'}
IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', '.vscode'}

def check_file_for_secrets(file_path):
    """Verifica se um arquivo contém chaves de API expostas"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        for i, pattern in enumerate(API_PATTERNS):
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"🚨 ALARME DE SEGURANÇA!")
                print(f"   Arquivo: {file_path}")
                print(f"   Padrão: {i+1}")
                print(f"   Matches: {len(matches)}")
                for match in matches[:3]:  # Mostra apenas os 3 primeiros
                    print(f"   Chave encontrada: {match[:10]}...")
                print()
                return True
    except Exception as e:
        pass  # Ignora erros de leitura
    
    return False

def scan_directory(directory):
    """Escaneia diretório em busca de chaves de API"""
    print("🔍 ESCANEANDO PROJETO EM BUSCA DE CHAVES DE API...")
    print("=" * 60)
    
    secrets_found = False
    directory = Path(directory)
    
    for file_path in directory.rglob('*'):
        # Ignora diretórios
        if any(part in IGNORE_DIRS for part in file_path.parts):
            continue
            
        # Ignora extensões
        if file_path.suffix in IGNORE_EXTENSIONS:
            continue
            
        # Ignora o próprio arquivo de segurança
        if file_path.name == 'check_security.py':
            continue
            
        # Verifica apenas arquivos de texto
        if file_path.is_file():
            if check_file_for_secrets(file_path):
                secrets_found = True
    
    print("=" * 60)
    if secrets_found:
        print("🚨 CHAVES DE API ENCONTRADAS! REMOVA IMEDIATAMENTE!")
        print("   Use: git filter-branch ou git filter-repo para limpar o histórico")
        return False
    else:
        print("✅ Nenhuma chave de API exposta encontrada nos arquivos atuais")
        print("✅ Projeto seguro para commit")
        return True

def check_git_history():
    """Verifica se há chaves de API no histórico do Git"""
    print("\n🔍 VERIFICANDO HISTÓRICO DO GIT...")
    print("=" * 60)
    
    try:
        import subprocess
        
        # Procura por padrões de API no histórico
        result = subprocess.run(
            ['git', 'log', '--all', '--full-history', '--source', '-S', 'AIza'],
            capture_output=True, text=True, cwd='.'
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print("🚨 POSSÍVEL CHAVE GEMINI NO HISTÓRICO DO GIT!")
            print("   Execute os comandos abaixo para limpar:")
            print("   1. git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all")
            print("   2. git push origin --force --all")
            print("   3. git push origin --force --tags")
            return False
        else:
            print("✅ Nenhuma chave Gemini encontrada no histórico recente")
            return True
            
    except Exception as e:
        print(f"⚠️ Não foi possível verificar o histórico do Git: {e}")
        return True

def main():
    """Função principal de verificação de segurança"""
    print("🛡️ J.A.R.V.I.S. Mark 13 - Verificação de Segurança")
    print("🔒 Protegendo suas chaves de API...")
    print()
    
    # Verifica arquivos atuais
    files_safe = scan_directory('.')
    
    # Verifica histórico do Git
    git_safe = check_git_history()
    
    print()
    print("=" * 60)
    if files_safe and git_safe:
        print("🎉 SEGURANÇA OK!")
        print("✅ Nenhuma chave de API exposta encontrada")
        print("✅ Projeto seguro para compartilhar no GitHub")
        sys.exit(0)
    else:
        print("🚨 PROBLEMAS DE SEGURANÇA DETECTADOS!")
        print("⚠️ Corrija os problemas antes de fazer commit")
        sys.exit(1)

if __name__ == "__main__":
    main()
