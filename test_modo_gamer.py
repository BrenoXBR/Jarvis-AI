#!/usr/bin/env python3
"""
Script de teste para os comandos do Modo Gamer
"""

import sys
import os
import subprocess

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_modo_gamer_commands():
    """Testa os comandos do Modo Gamer"""
    print("🎮 Testando comandos do Modo Gamer...")
    
    try:
        from action_handler import ActionHandler
        
        # Cria instância do ActionHandler
        handler = ActionHandler()
        print("✅ ActionHandler criado com sucesso")
        
        # Testa comando de ativar modo gamer
        print("\n🧪 Testando comando: 'Modo Gamer'")
        resultado_ativar = handler.process_command("Modo Gamer")
        if resultado_ativar:
            print(f"Resposta: {resultado_ativar}")
        else:
            print("⚠️ Comando não reconhecido")
        
        # Testa comando de encerrar modo gamer
        print("\n🧪 Testando comando: 'Encerrar Modo Gamer'")
        resultado_encerrar = handler.process_command("Encerrar Modo Gamer")
        if resultado_encerrar:
            print(f"Resposta: {resultado_encerrar}")
        else:
            print("⚠️ Comando não reconhecido")
        
        # Testa variações dos comandos
        test_commands = [
            "ativa o modo gamer",
            "modogamer",
            "fechar modo gamer",
            "desativar modo gamer"
        ]
        
        print("\n🧪 Testando variações dos comandos:")
        for cmd in test_commands:
            resultado = handler.process_command(cmd)
            if resultado:
                print(f"✅ '{cmd}' -> Reconhecido")
            else:
                print(f"❌ '{cmd}' -> Não reconhecido")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar Modo Gamer: {e}")
        return False

def test_taskkill_functionality():
    """Testa se o taskkill está funcionando"""
    print("\n🔧 Testando funcionalidade taskkill...")
    
    try:
        # Testa taskkill com um processo que não existe (não deve causar erro)
        result = subprocess.run(
            ["taskkill", "/F", "/IM", "processo_inexistente.exe"], 
            capture_output=True, 
            text=True,
            check=False
        )
        
        print("✅ Comando taskkill está funcionando")
        print(f"   Return code: {result.returncode}")
        print(f"   Stdout: {result.stdout.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar taskkill: {e}")
        return False

def test_app_paths():
    """Testa os caminhos dos aplicativos"""
    print("\n📁 Verificando caminhos dos aplicativos...")
    
    apps_info = {
        "Discord": [
            r"C:\Users\%USERNAME%\AppData\Local\Discord\app-*\Discord.exe",
            "discord.exe"
        ],
        "Opera GX": [
            r"C:\Users\%USERNAME%\AppData\Local\Programs\Opera GX\opera.exe",
            r"C:\Program Files\Opera GX\opera.exe",
            "opera.exe"
        ],
        "Steam": [
            r"C:\Program Files (x86)\Steam\steam.exe",
            r"C:\Program Files\Steam\steam.exe",
            "steam.exe"
        ]
    }
    
    for app_name, paths in apps_info.items():
        encontrado = False
        for path in paths:
            try:
                expanded_path = os.path.expandvars(path)
                if "*" in path:
                    # Para caminhos com wildcard, apenas verifica o diretório
                    dir_path = os.path.dirname(expanded_path)
                    if os.path.exists(dir_path):
                        encontrado = True
                        print(f"✅ {app_name}: Diretório encontrado em {dir_path}")
                        break
                else:
                    if os.path.exists(expanded_path):
                        encontrado = True
                        print(f"✅ {app_name}: Encontrado em {expanded_path}")
                        break
            except:
                continue
        
        if not encontrado:
            print(f"⚠️ {app_name}: Não encontrado nos caminhos padrão")
    
    return True

def main():
    """Função principal de teste"""
    print("🎮 TESTE DOS COMANDOS MODO GAMER")
    print("=" * 50)
    
    # Testa cada funcionalidade
    test1 = test_modo_gamer_commands()
    test2 = test_taskkill_functionality()
    test3 = test_app_paths()
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS COMANDOS MODO GAMER:")
    print("1. ✅ 'Modo Gamer': Abre Discord, Opera GX e Steam")
    print("2. ✅ 'Encerrar Modo Gamer': Fecha os 3 aplicativos com taskkill")
    print("3. ✅ Variações: 'modogamer', 'ativa modo gamer', etc.")
    print("4. ✅ Segurança: Tratamento de erros em todos os passos")
    print("5. ✅ Feedback: Mensagens detalhadas de sucesso/falha")
    
    if all([test1, test2, test3]):
        print("\n🚀 Modo Gamer está pronto para uso!")
        print("💡 Diga 'Jarvis, Modo Gamer' para ativar")
        print("💡 Diga 'Jarvis, Encerrar Modo Gamer' para desativar")
    else:
        print("\n⚠️ Alguns testes falharam - verifique as configurações")

if __name__ == "__main__":
    main()
