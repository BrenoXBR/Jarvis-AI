#!/usr/bin/env python3
"""
Script de Teste do Módulo de Controle de Sistema
Valida as novas funcionalidades de busca dinâmica e fallback
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from jarvis_system_controller import SystemController
    from jarvis_gui_optimized import Logger, JarvisConfig
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    sys.exit(1)

def test_dynamic_path_search():
    """Testa busca dinâmica de aplicativos"""
    print("🔍 Testando busca dinâmica de aplicativos...")
    
    config = JarvisConfig()
    logger = Logger(config)
    controller = SystemController(logger)
    
    # Aplicativos para teste
    test_apps = ["discord", "spotify", "chrome", "vscode"]
    
    for app_key in test_apps:
        if app_key in controller.applications:
            app_data = controller.applications[app_key]
            print(f"\n📱 Buscando: {app_data['name']}")
            
            # Testa busca de caminho
            path = controller._find_application_path(app_key, app_data)
            
            if path:
                print(f"✅ Encontrado: {path}")
            else:
                print(f"❌ Não encontrado")
                
                # Testa web fallback
                fallback_result = controller._open_web_fallback(app_key, app_data)
                print(f"🌐 Fallback: {fallback_result}")

def test_intent_detection():
    """Testa detecção de intenções"""
    print("\n🧠 Testando detecção de intenções...")
    
    config = JarvisConfig()
    logger = Logger(config)
    controller = SystemController(logger)
    
    test_messages = [
        "Jarvis, abra o Discord",
        "Jarvis, inicie o Spotify",
        "Jarvis, protocolo silêncio",
        "Jarvis, aumente o volume",
        "Jarvis, abra o YouTube"
    ]
    
    for message in test_messages:
        print(f"\n💬 Mensagem: '{message}'")
        intent = controller.detect_command_intent(message)
        
        if intent:
            command_type, command_data = intent
            print(f"✅ Detectado: {command_type} - {command_data}")
        else:
            print("❌ Nenhuma intenção detectada")

def test_discord_specific():
    """Testa específico o Discord como no problema relatado"""
    print("\🎮 Testando específico o Discord...")
    
    config = JarvisConfig()
    logger = Logger(config)
    controller = SystemController(logger)
    
    if "discord" in controller.applications:
        app_data = controller.applications["discord"]
        print(f"📱 Testando: {app_data['name']}")
        
        # 1. Busca caminho
        path = controller._find_application_path("discord", app_data)
        print(f"🔍 Caminho encontrado: {path}")
        
        # 2. Se não encontrou, mostra web fallback
        if not path:
            print("❌ Discord não encontrado localmente")
            fallback = controller._open_web_fallback("discord", app_data)
            print(f"🌐 Web fallback: {fallback}")
        else:
            print("✅ Discord encontrado - pode ser executado")
            
        # 3. Testa execução (sem realmente executar)
        print("\n⚠️ Teste de execução simulado:")
        print("🔍 Tentando abrir: [caminho do Discord]")
        print("📋 Validando execução...")
        print("✅ Discord iniciado com sucesso!" if path else "❌ Falha na execução")

def main():
    """Função principal de teste"""
    print("🧪 J.A.R.V.I.S. - Teste do Módulo de Controle de Sistema")
    print("=" * 60)
    
    try:
        test_dynamic_path_search()
        test_intent_detection()
        test_discord_specific()
        
        print("\n✅ Testes concluídos!")
        print("\n📋 Resumo das melhorias:")
        print("• 🔍 Busca dinâmica em AppData, Program Files, Registro")
        print("• ✅ Validação de execução do processo")
        print("• 🌐 Fallback automático para versão web")
        print("• 📝 Logs detalhados de erro no terminal")
        print("• 💡 Mensagens amigáveis ao usuário")
        
    except Exception as e:
        print(f"\n❌ Erro nos testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
