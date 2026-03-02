#!/usr/bin/env python3
"""
Cria pacote final do J.A.R.V.I.S. com ícone
"""

import os
import shutil

def create_final_package():
    """Cria pacote portátil completo com ícone"""
    print("🤖 Criando pacote final do J.A.R.V.I.S. com ícone...")
    
    # Remove pacote anterior se existir
    package_dir = "Jarvis_Portable_v1.0_Final"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    print(f"✅ Diretório criado: {package_dir}")
    
    # Copia executável com ícone
    if os.path.exists('dist/JarvisGUI.exe'):
        shutil.copy('dist/JarvisGUI.exe', package_dir)
        print("✅ Executável com ícone copiado")
    
    # Copia arquivos essenciais
    essential_files = ['.env', 'README.md', 'requirements.txt']
    
    for file_name in essential_files:
        if os.path.exists(file_name):
            shutil.copy(file_name, package_dir)
            print(f"✅ {file_name} copiado")
        else:
            print(f"⚠️ {file_name} não encontrado")
    
    # Copia ícone para visualização
    if os.path.exists('jarvis.ico'):
        shutil.copy('jarvis.ico', package_dir)
        print("✅ Ícone copiado")
    
    # Cria instruções atualizadas
    instructions = """🤖 J.A.R.V.I.S. - Assistente Inteligente v1.0 Final
🚀 Pacote Portátil com Ícone - Stark Industries

═══════════════════════════════════════════════════════════════

🎯 COMO USAR:

1️⃣ Execute o JarvisGUI.exe (com ícone do J.A.R.V.I.S.)
2️⃣ Aguarde a interface carregar (pode levar alguns segundos)
3️⃣ Configure sua API Key se necessário

═══════════════════════════════════════════════════════════════

📁 ARQUIVOS IMPORTANTES:

• JarvisGUI.exe → Programa principal (com ícone personalizado)
• jarvis.ico → Ícone do aplicativo
• .env → Configurações (NÃO COMPARTILHE ESTE ARQUIVO!)
• README.md → Documentação completa
• requirements.txt → Dependências (para desenvolvedores)

═══════════════════════════════════════════════════════════════

⚙️ CONFIGURAÇÃO INICIAL:

Se o Jarvis pedir API Key:

1. Abra o arquivo .env com Bloco de Notas
2. Substitua a chave existente pela sua:
   GEMINI_API_KEY=sua_chave_api_aqui
   
3. Para obter sua chave:
   • Acesse: https://makersuite.google.com/app/apikey
   • Faça login com sua conta Google
   • Crie uma nova API key
   • Copie e cole no arquivo .env

═══════════════════════════════════════════════════════════════

🔧 REQUISITOS DO SISTEMA:

✅ Windows 10 ou superior
✅ Conexão com internet
✅ Microfone (opcional, para comandos de voz)
✅ 100MB de espaço livre

═══════════════════════════════════════════════════════════════

🤖 FUNCIONALIDADES COMPLETAS:

📝 Chat com IA Gemini
   • Conversas naturais
   • Respostas contextuais
   • Memória de conversas

🎤 Comandos de Voz
   • Clique no botão 🎤 Ouvir
   • Fale seu comando
   • Jarvis responde por voz

👁️ Análise de Tela
   • Clique no botão 👁️
   • Captura e análise automática
   • Diagnóstico técnico

💾 Memória Persistente
   • Salva conversas
   • Aprende com o tempo
   • Contexto contínuo

🎨 Interface Stark Industries
   • Design cibernético elegante
   • Cores temáticas azul neon
   • Ícone personalizado do J.A.R.V.I.S.
   • Experiência imersiva

═══════════════════════════════════════════════════════════════

🚀 DICAS RÁPIDAS:

• Digite e pressione Enter para enviar mensagens
• Use o botão 🎤 para comandos de voz
• Use 👁️ para analisar erros de código
• A barra de progresso azul mostra processamento
• Todas as conversas são salvas automaticamente
• O ícone do J.A.R.V.I.S. aparece na barra de tarefas

═══════════════════════════════════════════════════════════════

⚠️ IMPORTANTE:

• NUNCA compartilhe o arquivo .env (contém sua API key)
• Mantenha sua conexão ativa para usar o Gemini
• O primeiro uso pode ser mais lento (carregamento)
• Feche outras aplicações pesadas para melhor performance

═══════════════════════════════════════════════════════════════

🆘 SUPORTE:

Se encontrar problemas:

1. Verifique sua conexão com internet
2. Confirme se a API key está correta
3. Reinicie o aplicativo
4. Verifique se o Windows está atualizado

═══════════════════════════════════════════════════════════════

🎉 VERSÃO FINAL COM RECURSOS COMPLETOS:

✅ Executável com ícone personalizado
✅ Interface Stark Industries completa
✅ Todas as funcionalidades integradas
✅ Pacote portátil independente
✅ Documentação completa

🏢 Powered by Stark Industries Technology
📅 Versão 1.0 Final - 2026
"""
    
    with open(os.path.join(package_dir, 'LEIA-ME.txt'), 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Instruções atualizadas criadas: LEIA-ME.txt")
    
    # Mostra estatísticas
    exe_size = os.path.getsize(os.path.join(package_dir, 'JarvisGUI.exe')) / (1024*1024)
    print(f"\n📊 ESTATÍSTICAS FINAIS:")
    print(f"   • Executável: {exe_size:.1f} MB")
    print(f"   • Arquivos totais: {len(os.listdir(package_dir))}")
    print(f"   • Com ícone personalizado: ✅")
    print(f"   • Pacote completo pronto!")
    
    print(f"\n🎉 PACOTE FINAL CRIADO EM: {package_dir}/")
    print("📦 Pronto para distribuir com ícone!")
    
    return package_dir

if __name__ == "__main__":
    create_final_package()
    print("\nPacote final criado. O programa será encerrado.")
