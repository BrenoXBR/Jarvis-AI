#!/usr/bin/env python3
"""
Corrige o encoding do arquivo .env para UTF-8 sem BOM
"""

def fix_env_encoding():
    """Converte .env para UTF-8 sem BOM"""
    try:
        # Lê o arquivo atual
        with open('.env', 'r', encoding='utf-8-sig') as f:  # utf-8-sig remove BOM se existir
            content = f.read()
        
        # Reescreve com UTF-8 puro (sem BOM)
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Arquivo .env convertido para UTF-8 sem BOM")
        
        # Verifica o conteúdo
        with open('.env', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"📄 Conteúdo do .env:")
            for line in lines:
                print(f"   {line.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao converter .env: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Corrigindo encoding do arquivo .env...")
    success = fix_env_encoding()
    
    if success:
        print("\n🎉 .env corrigido com sucesso!")
        print("💡 Dica: Se ainda tiver problemas, abra o .env no Bloco de Notas")
        print("   e salve como UTF-8 (sem BOM) manualmente.")
    else:
        print("\n❌ Falha ao corrigir .env")
    
    print("\nCorreção de encoding concluída. O programa será encerrado.")
