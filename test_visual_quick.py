#!/usr/bin/env python3
"""
Teste rápido da automação de análise de tela
"""

import sys
import os
sys.path.insert(0, '.')

def test_visual_automation():
    print("👁️ Testando automação de análise de tela...")
    
    try:
        from jarvis_threads import AIWorker
        
        worker = AIWorker()
        
        # Testa comando visual
        test_command = "olhe minha tela agora"
        print(f"📝 Testando comando: {test_command}")
        
        # Verifica se a captura automática está implementada
        import inspect
        source = inspect.getsource(worker._process_command)
        
        if "pyautogui.screenshot(temp_file)" in source:
            print("✅ Captura automática implementada")
        else:
            print("❌ Captura automática não encontrada")
        
        if "generate_content([prompt, image])" in source:
            print("✅ Imagem anexada à API")
        else:
            print("❌ Imagem não anexada à API")
        
        if "os.remove(temp_file)" in source:
            print("✅ Limpeza de memória implementada")
        else:
            print("❌ Limpeza de memória não implementada")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_visual_automation()
