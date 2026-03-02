#!/usr/bin/env python3
"""
Cria pacote portátil final do J.A.R.V.I.S.
"""

import os
import shutil

def create_portable_package():
    """Cria pacote portátil completo"""
    print("📦 Criando pacote portátil do J.A.R.V.I.S.")
    
    # Cria diretório
    package_dir = "Jarvis_Portable_v1.0"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    print(f"✅ Diretório criado: {package_dir}")
    
    # Copia executável
    if os.path.exists('dist/JarvisGUI.exe'):
        shutil.copy('dist/JarvisGUI.exe', package_dir)
        print("✅ Executável copiado")
    
    # Copia arquivos essenciais
    essential_files = ['.env', 'README.md', 'requirements.txt']
    
    for file_name in essential_files:
        if os.path.exists(file_name):
            shutil.copy(file_name, package_dir)
            print(f"✅ {file_name} copiado")
        else:
            print(f"⚠️ {file_name} não encontrado")
    
    # Cria instruções detalhadas
    instructions = """🤖 J.A.R.V.I.S. - Assistente Inteligente v1.0
🚀 Pacote Portátil - Stark Industries

═══════════════════════════════════════════════════════════════

🎯 COMO USAR:

1️⃣ Execute o JarvisGUI.exe
2️⃣ Aguarde a interface carregar (pode levar alguns segundos)
3️⃣ Configure sua API Key se necessário

═══════════════════════════════════════════════════════════════

📁 ARQUIVOS IMPORTANTES:

• JarvisGUI.exe → Programa principal
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
   • Experiência imersiva

═══════════════════════════════════════════════════════════════

🚀 DICAS RÁPIDAS:

• Digite e pressione Enter para enviar mensagens
• Use o botão 🎤 para comandos de voz
• Use 👁️ para analisar erros de código
• A barra de progresso azul mostra processamento
• Todas as conversas são salvas automaticamente

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

🎉 Desenvolvido com ❤️ por Windsurf
🏢 Powered by Stark Industries Technology
📅 Versão 1.0 - 2026
"""
    
    with open(os.path.join(package_dir, 'LEIA-ME.txt'), 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Instruções criadas: LEIA-ME.txt")
    
    # Mostra estatísticas
    exe_size = os.path.getsize(os.path.join(package_dir, 'JarvisGUI.exe')) / (1024*1024)
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • Executável: {exe_size:.1f} MB")
    print(f"   • Arquivos totais: {len(os.listdir(package_dir))}")
    print(f"   • Pacote completo pronto!")
    
    print(f"\n🎉 PACOTE CRIADO EM: {package_dir}/")
    print("📦 Pronto para distribuir!")
    
    return package_dir

if __name__ == "__main__":
    create_portable_package()
    print("\nPacote portátil criado. O programa será encerrado.")
