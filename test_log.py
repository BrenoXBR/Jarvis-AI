#!/usr/bin/env python3
"""
Teste do sistema de log do J.A.R.V.I.S.
"""

import sys
import os
from datetime import datetime

# Adiciona o diretório atual ao path para importar o logger
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa o logger do Jarvis
try:
    from jarvis_gui_integrada import JarvisLogger
    print("✅ Logger importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar logger: {e}")
    sys.exit(1)

def test_logger():
    """Testa o sistema de log"""
    print("🧪 TESTANDO SISTEMA DE LOG...")
    
    # Cria instância do logger
    logger = JarvisLogger()
    
    # Testa diferentes tipos de log
    logger.log_info("Teste de mensagem informativa", "TESTE")
    logger.log_success("Teste de mensagem de sucesso", "TESTE")
    logger.log_warning("Teste de mensagem de aviso", "TESTE")
    
    # Testa erro simulado
    try:
        # Simula um erro
        raise ValueError("Este é um erro de teste para verificar o sistema de log")
    except Exception as e:
        logger.log_error(e, "Erro simulado durante teste", "TESTE")
    
    print("✅ Logs criados com sucesso!")
    
    # Verifica se os arquivos foram criados
    if os.path.exists(logger.log_file):
        print(f"✅ Arquivo de log criado: {logger.log_file}")
        size = os.path.getsize(logger.log_file)
        print(f"📊 Tamanho: {size} bytes")
    
    if os.path.exists(logger.error_file):
        print(f"✅ Arquivo de erro criado: {logger.error_file}")
        size = os.path.getsize(logger.error_file)
        print(f"📊 Tamanho: {size} bytes")
        
        # Mostra conteúdo do arquivo de erro
        print("\n📄 CONTEÚDO DO ARQUIVO DE ERRO:")
        print("=" * 50)
        with open(logger.error_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    
    print("\n🎉 TESTE DO SISTEMA DE LOG CONCLUÍDO!")

if __name__ == "__main__":
    test_logger()
    print("\nTeste concluído. O programa será encerrado.")
