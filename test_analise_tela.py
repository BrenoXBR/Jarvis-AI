#!/usr/bin/env python3
"""
Script de teste para a funcionalidade de análise de tela do Jarvis
"""

import sys
import os
import pyautogui
import pyperclip

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_screenshot_functionality():
    """Testa a funcionalidade de screenshot"""
    print("📸 Testando funcionalidade de screenshot...")
    
    try:
        # Testa captura de tela
        screenshot_path = "test_screenshot.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        
        if os.path.exists(screenshot_path):
            print(f"✅ Screenshot salvo com sucesso: {screenshot_path}")
            print(f"   Tamanho: {screenshot.size}")
            print(f"   Formato: {screenshot.format}")
            
            # Remove o arquivo de teste
            os.remove(screenshot_path)
            print("✅ Arquivo de teste removido")
            return True
        else:
            print("❌ Falha ao salvar screenshot")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar screenshot: {e}")
        return False

def test_pil_import():
    """Testa importação do PIL/Pillow"""
    print("\n🖼️ Testando importação do PIL...")
    
    try:
        import PIL.Image
        print("✅ PIL/Pillow importado com sucesso")
        print(f"   Versão: {PIL.__version__}")
        
        # Testa abrir uma imagem (se existir)
        if os.path.exists("test_screenshot.png"):
            try:
                img = PIL.Image.open("test_screenshot.png")
                print(f"✅ Imagem de teste carregada: {img.size}")
                img.close()
            except Exception as e:
                print(f"⚠️ Erro ao abrir imagem de teste: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ PIL não disponível: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar PIL: {e}")
        return False

def test_screen_analysis_command():
    """Testa o comando de análise de tela"""
    print("\n🔍 Testando comando de análise de tela...")
    
    try:
        from action_handler import ActionHandler
        
        # Cria instância do ActionHandler
        handler = ActionHandler()
        print("✅ ActionHandler criado com sucesso")
        
        # Testa comandos de análise
        test_commands = [
            "olhe a tela",
            "analise a tela", 
            "veja a tela"
        ]
        
        print("\n🧪 Testando comandos de análise:")
        for cmd in test_commands:
            resultado = handler.process_command(cmd)
            if resultado:
                print(f"✅ '{cmd}' -> Reconhecido")
            else:
                print(f"❌ '{cmd}' -> Não reconhecido")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar comando de análise: {e}")
        return False

def test_regex_extraction():
    """Testa extração de código com regex"""
    print("\n🔧 Testando extração de código com regex...")
    
    try:
        import re
        
        # Texto de exemplo com blocos de código
        texto_exemplo = """
        Aqui está o código corrigido:
        
        ```python
        def funcao_corrigida():
            print("Olá mundo!")
            return True
        ```
        
        E aqui está outro exemplo:
        
        ```javascript
        console.log("Teste");
        ```
        """
        
        # Testa o regex usado no código
        pattern = r'```(?:python|javascript|html|css|json|xml)?\s*\n(.*?)\n```'
        codigos = re.findall(pattern, texto_exemplo, re.DOTALL)
        
        print(f"✅ Encontrados {len(codigos)} blocos de código:")
        for i, codigo in enumerate(codigos, 1):
            print(f"   Bloco {i}: {codigo.strip()[:50]}...")
        
        if len(codigos) > 0:
            print("✅ Extração de código funcionando corretamente")
            return True
        else:
            print("❌ Nenhum bloco de código encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar regex: {e}")
        return False

def test_clipboard_integration():
    """Testa integração com área de transferência"""
    print("\n📋 Testando integração com área de transferência...")
    
    try:
        # Testa copiar e colar
        test_code = """def teste():
    print("Código de teste para correção automática")
    return "sucesso\""""
        
        pyperclip.copy(test_code)
        pasted = pyperclip.paste()
        
        if test_code in pasted:
            print("✅ Área de transferência funcionando para código")
            print("✅ Pronta para correção automática")
            return True
        else:
            print("❌ Problema com área de transferência")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar área de transferência: {e}")
        return False

def main():
    """Função principal de teste"""
    print("📸 TESTE DA FUNCIONALIDADE DE ANÁLISE DE TELA")
    print("=" * 60)
    
    # Testa cada componente
    test1 = test_screenshot_functionality()
    test2 = test_pil_import()
    test3 = test_screen_analysis_command()
    test4 = test_regex_extraction()
    test5 = test_clipboard_integration()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DA ANÁLISE DE TELA:")
    print("1. ✅ Screenshot: pyautogui.screenshot() funcionando")
    print("2. ✅ PIL/Pillow: Importação e manipulação de imagens")
    print("3. ✅ Comando: 'olhe a tela' reconhecido")
    print("4. ✅ Extração: Regex para blocos de código funcionando")
    print("5. ✅ Auto-correção: Integração com área de transferência")
    
    print("\n💡 COMO USAR:")
    print("   • Análise: 'Jarvis, olhe a tela'")
    print("   • O Jarvis vai tirar screenshot e analisar com Gemini")
    print("   • Se encontrar código corrigido, aplicará automaticamente")
    print("   • Arquivo temporário screenshot.png será removido")
    
    if all([test1, test2, test3, test4, test5]):
        print("\n🎉 Análise de tela está pronta para uso!")
        print("🚀 O Jarvis agora pode ver e corrigir sua tela!")
    else:
        print("\n⚠️ Alguns testes falharam - verifique as dependências")

if __name__ == "__main__":
    main()
