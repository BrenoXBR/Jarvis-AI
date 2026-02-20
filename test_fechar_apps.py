#!/usr/bin/env python3
"""
Script de teste para a função de fechar aplicativos do Jarvis
"""

import sys
import os
import subprocess

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_taskkill_commands():
    """Testa os comandos taskkill diretamente"""
    print("🔧 Testando comandos taskkill diretamente...")
    
    # Lista de processos para testar
    test_processes = [
        "notepad.exe",
        "Discord.exe", 
        "discord.exe",
        "opera.exe",
        "steam.exe"
    ]
    
    for process in test_processes:
        comando = ["taskkill", "/F", "/IM", process]
        comando_str = " ".join(comando)
        
        print(f"\n🧪 Testando: {comando_str}")
        
        try:
            result = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                check=False
            )
            
            print(f"   Return code: {result.returncode}")
            print(f"   Stdout: {result.stdout.strip()}")
            print(f"   Stderr: {result.stderr.strip()}")
            
            if result.returncode == 0:
                print(f"   ✅ {process} fechado com sucesso")
            elif "not found" in result.stdout.lower() or "not found" in result.stderr.lower():
                print(f"   ⚠️ {process} não encontrado (normal se não está rodando)")
            else:
                print(f"   ❌ Erro ao fechar {process}")
                
        except Exception as e:
            print(f"   ❌ Erro ao executar comando: {e}")

def test_encerrar_modo_gamer():
    """Testa a função encerrar_modo_gamer"""
    print("\n🎮 Testando função encerrar_modo_gamer...")
    
    try:
        from action_handler import ActionHandler
        
        # Cria instância do ActionHandler
        handler = ActionHandler()
        print("✅ ActionHandler criado com sucesso")
        
        # Executa a função
        print("\n🧪 Executando encerrar_modo_gamer():")
        resultado = handler.encerrar_modo_gamer()
        
        print(f"\n📋 Resultado: {resultado}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar encerrar_modo_gamer: {e}")
        return False

def test_process_mapping():
    """Testa o mapeamento de processos"""
    print("\n📋 Testando mapeamento de processos...")
    
    # Mapeamento usado na função
    processos_gamer = {
        "Discord": ["Discord.exe", "discord.exe"],
        "Opera GX": ["opera.exe", "opera_gx.exe"], 
        "Steam": ["steam.exe", "Steam.exe"]
    }
    
    print("✅ Mapeamento de processos:")
    for app_name, process_list in processos_gamer.items():
        print(f"   {app_name}: {process_list}")
    
    return True

def test_debug_info():
    """Mostra informações de debug do sistema"""
    print("\n🔍 Informações de debug do sistema...")
    
    try:
        # Lista processos em execução
        result = subprocess.run(
            ["tasklist", "/FO", "CSV"],
            capture_output=True,
            text=True,
            check=False
        )
        
        lines = result.stdout.split('\n')
        
        # Procura por processos gamer
        gamer_processes = []
        for line in lines:
            line_lower = line.lower()
            if any(proc in line_lower for proc in ['discord', 'opera', 'steam', 'notepad']):
                gamer_processes.append(line.strip())
        
        if gamer_processes:
            print("✅ Processos gamer encontrados:")
            for proc in gamer_processes[:5]:  # Limita a 5 resultados
                print(f"   {proc}")
        else:
            print("⚠️ Nenhum processo gamer encontrado em execução")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao obter informações de debug: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🔧 TESTE DA FUNÇÃO DE FECHAR APLICATIVOS")
    print("=" * 60)
    
    # Testa cada componente
    test1 = test_process_mapping()
    test2 = test_taskkill_commands()
    test3 = test_debug_info()
    test4 = test_encerrar_modo_gamer()
    
    print("\n" + "=" * 60)
    print("📋 MELHORIAS IMPLEMENTADAS:")
    print("1. ✅ Mapeamento de processos: Nomes corretos para cada app")
    print("2. ✅ Comando forçado: taskkill /F /IM para fechamento garantido")
    print("3. ✅ Debug completo: Comando exeto, return code, stdout, stderr")
    print("4. ✅ Verificação de erro: Trata 'not found' e outros erros")
    print("5. ✅ Feedback detalhado: Mostra exatamente o que aconteceu")
    
    print("\n💡 COMO DEBUGAR:")
    print("   • Execute 'Jarvis, encerrar modo gamer'")
    print("   • Observe os comandos exatos executados")
    print("   • Verifique se os nomes dos processos estão corretos")
    print("   • Confirme se os apps estão realmente em execução")
    
    if all([test1, test2, test3, test4]):
        print("\n🎉 Função de fechar aplicativos aprimorada!")
        print("🚀 Agora com debug completo e mapeamento preciso!")
    else:
        print("\n⚠️ Verifique os logs acima para identificar problemas")

if __name__ == "__main__":
    main()
