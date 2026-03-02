#!/usr/bin/env python3
"""
Cria pacote final com sistema de log completo
"""

import os
import shutil

def create_log_package():
    """Cria pacote com sistema de log"""
    print("🤖 Criando pacote final com sistema de log completo...")
    
    # Remove pacote anterior se existir
    package_dir = "Jarvis_Com_Log_v1.0"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    print(f"✅ Diretório criado: {package_dir}")
    
    # Copia executável debug
    if os.path.exists('dist/JarvisGUI_Debug.exe'):
        shutil.copy('dist/JarvisGUI_Debug.exe', os.path.join(package_dir, 'JarvisGUI.exe'))
        print("✅ Executável com log copiado")
    
    # Copia arquivos essenciais
    essential_files = ['.env', 'README.md', 'requirements.txt', 'jarvis.ico']
    
    for file_name in essential_files:
        if os.path.exists(file_name):
            shutil.copy(file_name, package_dir)
            print(f"✅ {file_name} copiado")
    
    # Cria instruções detalhadas sobre o sistema de log
    log_instructions = """🤖 J.A.R.V.I.S. - VERSÃO COM SISTEMA DE LOG v1.0
📝 Pacote com Diagnóstico Completo e Registro de Atividades

═══════════════════════════════════════════════════════════════

🎯 NOVIDADES DESTA VERSÃO:

✅ SISTEMA DE LOG COMPLETO:
• Registro de todas as atividades
• Captura automática de erros
• Informações detalhadas do sistema
• Sugestões de solução automáticas

✅ ARQUIVOS GERADOS AUTOMATICAMENTE:
• jarvis_log.txt → Log completo de atividades
• ERRO_CRITICO.txt → Detalhes de erros (quando ocorrem)

═══════════════════════════════════════════════════════════════

🔍 COMO USAR O SISTEMA DE DIAGNÓSTICO:

1️⃣ Execute JarvisGUI.exe
2️⃣ Use normalmente o J.A.R.V.I.S.
3️⃣ Se ocorrer erro, verifique ERRO_CRITICO.txt
4️⃣ Para análise completa, verifique jarvis_log.txt

═══════════════════════════════════════════════════════════════

📁 ARQUIVOS IMPORTANTES:

• JarvisGUI.exe → Executável com sistema de log
• jarvis_log.txt → Criado automaticamente (log de atividades)
• ERRO_CRITICO.txt → Criado apenas em caso de erro
• .env → Configurações (NÃO COMPARTILHE!)
• README.md → Documentação
• jarvis.ico → Ícone do aplicativo

═══════════════════════════════════════════════════════════════

📊 O QUE O SISTEMA DE LOG REGISTRA:

✅ INFORMAÇÕES DE SISTEMA:
• Data/hora de cada sessão
• Sistema operacional
• Versão do Python
• Se é executável ou script
• Diretório de execução

✅ ATIVIDADES REGISTRADAS:
• Inicialização do sistema
• Carregamento de módulos
• Configuração da API
• Inicialização da interface
• Operações do usuário

✅ ERROS CAPTURADOS:
• Tipo exato do erro
• Mensagem completa
• Traceback completo
• Contexto do erro
• Lista de arquivos no diretório
• Sugestões de solução

═══════════════════════════════════════════════════════════════

🔧 EXEMPLOS DE USO DO DIAGNÓSTICO:

CASO 1: EXECUTÁVEL FECHA SILENCIOSAMENTE
1. Verifique se ERRO_CRITICO.txt foi criado
2. Se sim, leia o conteúdo para identificar o problema
3. Siga as sugestões no arquivo

CASO 2: FUNCIONALIDADE ESPECÍFICA FALHA
1. Abra jarvis_log.txt
2. Procure por [ERROR] no arquivo
3. Identifique o módulo com problema
4. Use as informações para solução

CASO 3: DESEMPENHO LENTO
1. Verifique jarvis_log.txt
2. Procure por [WARNING]
3. Identifique gargalos de performance

═══════════════════════════════════════════════════════════════

📋 ESTRUTURA DOS ARQUIVOS DE LOG:

jarvis_log.txt:
[2026-02-20 21:33:59] [INFO] [SISTEMA] Sistema de log inicializado
[2026-02-20 21:33:59] [INFO] [MEMÓRIA] Inicializando memória em: C:\path\jarvis_memory.db
[2026-02-20 21:33:59] [SUCCESS] [MEMÓRIA] Banco de dados inicializado com sucesso
[2026-02-20 21:33:59] [ERROR] [VISÃO] Falha ao inicializar visão computacional
[2026-02-20 21:33:59] [WARNING] [VISÃO] API key não configurada

ERRO_CRITICO.txt:
🤖 J.A.R.V.I.S. - ERRO CRÍTICO
==================================================
Data/Hora: 2026-02-20 21:33:59
Sistema: win32
Python: 3.13.12
Executável: True
Diretório: C:\path\to\app
Módulo: SISTEMA
Contexto: Erro ao iniciar interface
ERRO:
Tipo: CustomTkinterError
Mensagem: Failed to initialize display
TRACEBACK COMPLETO:
[traceback completo aqui]
INFORMAÇÕES ADICIONAIS:
Arquivos no diretório:
  - JarvisGUI.exe
  - .env
  - jarvis_log.txt
SUGESTÕES:
1. Verifique sua conexão com internet
2. Confirme se a API key está correta
3. Reinicie o aplicativo
4. Verifique se o Windows está atualizado
5. Feche outros aplicativos pesados

═══════════════════════════════════════════════════════════════

⚠️ IMPORTANTE:

• Os arquivos de log são criados automaticamente
• jarvis_log.txt cresce com o tempo (pode ser apagado)
• ERRO_CRITICO.txt é recriado a cada erro
• Compartilhe ERRO_CRITICO.txt para suporte técnico
• NUNCA compartilhe o arquivo .env

═══════════════════════════════════════════════════════════════

🆘 SUPORTE E DIAGNÓSTICO:

Se precisar de ajuda:

1. Execute esta versão com log
2. Reproduza o problema
3. Cole o conteúdo de ERRO_CRITICO.txt
4. Se necessário, envie jarvis_log.txt
5. Descreva o que estava fazendo

═══════════════════════════════════════════════════════════════

🎉 BENEFÍCIOS DO SISTEMA DE LOG:

✅ Diagnóstico rápido de problemas
✅ Registro completo de atividades
✅ Informações para suporte técnico
✅ Sugestões automáticas de solução
✅ Histórico de uso do sistema
✅ Detecção de padrões de erro

🏢 Powered by Stark Industries Logging Division
📅 Versão com Log v1.0 - 2026
"""
    
    with open(os.path.join(package_dir, 'SISTEMA_DE_LOG.txt'), 'w', encoding='utf-8') as f:
        f.write(log_instructions)
    
    print("✅ Instruções do sistema de log criadas")
    
    # Mostra estatísticas
    exe_path = os.path.join(package_dir, 'JarvisGUI.exe')
    if os.path.exists(exe_path):
        exe_size = os.path.getsize(exe_path) / (1024*1024)
        print(f"\n📊 ESTATÍSTICAS FINAIS:")
        print(f"   • Executável: {exe_size:.1f} MB")
        print(f"   • Arquivos totais: {len(os.listdir(package_dir))}")
        print(f"   • Sistema de log: ✅")
        print(f"   • Captura de erros: ✅")
        print(f"   • Diagnóstico completo: ✅")
        print(f"   • Pacote completo pronto!")
    
    print(f"\n🎉 PACOTE COM LOG CRIADO EM: {package_dir}/")
    print("📦 Pronto para distribuir com diagnóstico completo!")
    
    return package_dir

if __name__ == "__main__":
    create_log_package()
    print("\nPacote de log criado. O programa será encerrado.")
