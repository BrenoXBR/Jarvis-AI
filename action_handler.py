#!/usr/bin/env python3
"""
Action Handler para Jarvis - Versão Mínima Funcional
"""

import os
import pyautogui
import time
import pyperclip
import psutil  # Para verificar processos
import subprocess  # Para executar comandos do sistema
import google.generativeai as genai
from dotenv import load_dotenv

# Configurações de segurança do PyAutoGUI
pyautogui.FAILSAFE = True  # Fail-safe: mover mouse para canto superior esquerdo para
pyautogui.PAUSE = 0.5  # Pausa entre comandos para evitar sobrecarga

class ActionHandler:
    def __init__(self, workspace_path=None):
        """Inicializa o Action Handler"""
        self.workspace_path = workspace_path or os.path.expanduser("~/Desktop")
        
        # Configura a API do Gemini
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            print("🤖 API do Gemini configurada com sucesso")
        
        # Contador de segurança para evitar loops infinitos
        self.command_count = 0
        self.max_commands_per_session = 10
        
    def _is_process_active(self, process_name):
        """Verifica se um processo está ativo"""
        try:
            for proc in psutil.process_iter(['name']):
                if process_name.lower() in proc.info['name'].lower():
                    return True
            return False
        except:
            return False
    
    def _verify_window_focus(self, app_name):
        """Verifica se o aplicativo está em foco (simplificado)"""
        # Verificação básica se o processo está rodando
        process_names = {
            'bloco de notas': 'notepad',
            'notepad': 'notepad',
            'calculadora': 'calculator'
        }
        
        if app_name in process_names:
            return self._is_process_active(process_names[app_name])
        return True  # Se não souber, assume que está ok
    def gerar_e_colar_codigo(self, command, ai_model=None):
        """Gera código com Gemini e cola no aplicativo especificado"""
        try:
            # Verificação de segurança
            self.command_count += 1
            if self.command_count > self.max_commands_per_session:
                return "Limite de comandos atingido por segurança, mestre. Reinicie o Jarvis para continuar."
            
            command_lower = command.lower()
            
            # Verifica se é um comando para gerar código
            if any(word in command_lower for word in ['escreva um código', 'gere um código', 'crie um código', 'gerar código', 'escrever código']):
                # Mapeamento simples de aplicativos
                app_mapping = {
                    'bloco de notas': 'notepad.exe',
                    'notepad': 'notepad.exe',
                    'calculadora': 'calc.exe'
                }
                
                # Encontra o aplicativo
                app_to_open = 'notepad.exe'
                app_display = 'bloco de notas'
                for app_name, exe_name in app_mapping.items():
                    if f'no {app_name}' in command_lower:
                        app_to_open = exe_name
                        app_display = app_name
                        break
                
                # Extrai o tipo de código solicitado
                tipo_codigo = command_lower
                prefixes = ['escreva um código de ', 'gere um código de ', 'crie um código de ']
                for prefix in prefixes:
                    if tipo_codigo.startswith(prefix):
                        tipo_codigo = tipo_codigo[len(prefix):]
                        break
                
                # Remove referências ao aplicativo
                tipo_codigo = tipo_codigo.replace(' no bloco de notas', '').replace(' no notepad', '').strip()
                
                if not tipo_codigo:
                    tipo_codigo = "hello world"
                
                # Gera o código com Gemini
                if ai_model:
                    try:
                        prompt = f"Gere um código {tipo_codigo} simples e funcional."
                        response = ai_model.generate_content(prompt)
                        codigo_gerado = response.text if response and hasattr(response, 'text') else f"# Código {tipo_codigo}"
                    except Exception as e:
                        codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                else:
                    codigo_gerado = f"# Código {tipo_codigo}\nprint('Hello, World!')"
                
                codigo_gerado = codigo_gerado.strip()
                
                # Copia o código para a área de transferência
                try:
                    pyperclip.copy(codigo_gerado)
                except Exception as clip_error:
                    return f"Erro ao copiar código: {str(clip_error)}, mestre."
                
                # Abre o aplicativo
                try:
                    os.startfile(app_to_open)
                except Exception as open_error:
                    return f"Erro ao abrir {app_display}: {str(open_error)}, mestre."
                
                # Aguarda a janela carregar completamente
                print(f"⏳ Aguardando {app_display} carregar...")
                time.sleep(3)  # Delay de segurança aumentado para 3 segundos
                
                # Verifica se o processo está ativo antes de colar
                if not self._verify_window_focus(app_display):
                    return f"Não consegui verificar que {app_display} está ativo, mestre."
                
                # Cola o código
                try:
                    pyautogui.hotkey('ctrl', 'v')
                except Exception as paste_error:
                    # Tenta digitar como fallback
                    try:
                        pyautogui.write(codigo_gerado, interval=0.01)
                    except:
                        return f"Não consegui colar o código, mestre."
                
                return f"Código {tipo_codigo} gerado e colado no {app_display}, mestre."
            
            return None
            
        except KeyboardInterrupt:
            print("\n🛑 Interrupção detectada durante geração de código!")
            print("Cancelando operação de colar código...")
            return "Operação cancelada pelo usuário, mestre."
        except Exception as e:
            return f"Erro ao processar: {str(e)}, mestre."
    
    def ativar_modo_gamer(self):
        """Ativa o Modo Gamer abrindo Discord, Opera GX e Steam"""
        try:
            print("🎮 Ativando Modo Gamer...")
            
            # Lista de aplicativos para abrir
            apps_gamer = [
                ("Discord", "discord.exe"),
                ("Opera GX", "opera.exe"),  # Opera GX usa o mesmo executável
                ("Steam", "steam.exe")
            ]
            
            apps_abertos = []
            apps_falharam = []
            
            for nome_app, exe_name in apps_gamer:
                try:
                    # Tenta abrir o aplicativo
                    if nome_app == "Opera GX":
                        # Para Opera GX, tenta caminhos específicos
                        opera_paths = [
                            r"C:\Users\%USERNAME%\AppData\Local\Programs\Opera GX\opera.exe",
                            r"C:\Program Files\Opera GX\opera.exe",
                            "opera.exe"
                        ]
                        
                        opera_aberto = False
                        for path in opera_paths:
                            try:
                                expanded_path = os.path.expandvars(path)
                                if os.path.exists(expanded_path):
                                    os.startfile(expanded_path)
                                    apps_abertos.append(nome_app)
                                    opera_aberto = True
                                    break
                            except:
                                continue
                        
                        if not opera_aberto:
                            # Tenta como comando
                            subprocess.run(["start", "opera"], shell=True, check=False)
                            apps_abertos.append(nome_app)
                    else:
                        # Para Discord e Steam
                        os.startfile(exe_name)
                        apps_abertos.append(nome_app)
                    
                    print(f"✅ {nome_app} aberto com sucesso")
                    time.sleep(1)  # Pequena pausa entre aberturas
                    
                except Exception as e:
                    print(f"❌ Erro ao abrir {nome_app}: {e}")
                    apps_falharam.append(nome_app)
            
            # Monta mensagem de resposta
            if apps_abertos:
                mensagem = f"🎮 Modo Gamer ativado! Abertos: {', '.join(apps_abertos)}"
                if apps_falharam:
                    mensagem += f". Falhas: {', '.join(apps_falharam)}"
                return mensagem + ". Prepare-se para a ação, mestre!"
            else:
                return "❌ Não consegui abrir nenhum aplicativo gamer. Verifique se eles estão instalados, mestre."
                
        except Exception as e:
            return f"❌ Erro ao ativar Modo Gamer: {str(e)}, mestre."
    
    def encerrar_modo_gamer(self):
        """Encerra o Modo Gamer fechando Discord, Opera GX e Steam"""
        try:
            print("🛑 Encerrando Modo Gamer...")
            
            # Mapeamento completo de processos para fechar
            mapeamento_processos = {
                'discord': 'discord.exe',
                'Discord': 'Discord.exe',
                'opera': 'opera.exe',
                'opera gx': 'opera.exe',
                'steam': 'steam.exe',
                'Steam': 'Steam.exe',
                'bloco de notas': 'notepad.exe'
            }
            
            processos_fechados = []
            processos_falharam = []
            
            # Tenta fechar cada processo conhecido
            for nome_comum, nome_processo in mapeamento_processos.items():
                try:
                    print(f"🔧 Tentando fechar: {nome_comum} -> {nome_processo}")
                    
                    # Usa os.system com taskkill forçado
                    comando = f'taskkill /F /IM "{nome_processo}"'
                    print(f"🔧 Executando: {comando}")
                    
                    resultado = os.system(comando)
                    
                    # Verifica o resultado (0 = sucesso, 1 = processo não encontrado)
                    if resultado == 0:
                        processos_fechados.append(nome_comum)
                        print(f"✅ {nome_comum} ({nome_processo}) fechado com sucesso")
                    else:
                        print(f"⚠️ {nome_comum} ({nome_processo}) não encontrado ou já fechado")
                        
                except Exception as e:
                    print(f"❌ Erro ao fechar {nome_comum}: {e}")
                    processos_falharam.append(nome_comum)
            
            # Monta mensagem de resposta
            if processos_fechados:
                mensagem = f"🛑 Modo Gamer encerrado! Fechados: {', '.join(processos_fechados)}"
                if processos_falharam:
                    mensagem += f". Falhas: {', '.join(processos_falharam)}"
                return mensagem + ". Modo gamer desativado, mestre!"
            else:
                return "ℹ️ Nenhum aplicativo gamer estava em execução, mestre."
                
        except Exception as e:
            return f"❌ Erro ao encerrar Modo Gamer: {str(e)}, mestre."
    
    def executar_comando_git(self, mensagem_commit):
        """Executa comandos Git usando atalhos do teclado"""
        try:
            print("🔧 Executando comandos Git...")
            
            # Abre o terminal do Windsurf (Ctrl+J)
            print("📝 Abrindo terminal do Windsurf...")
            pyautogui.hotkey('ctrl', 'j')
            time.sleep(1)  # Espera o terminal abrir
            
            # Digita git add .
            print("➕ Adicionando arquivos ao staging...")
            pyautogui.write('git add .', interval=0.1)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1)
            
            # Digita git commit
            print("💾 Criando commit...")
            pyautogui.write('git commit -m "', interval=0.1)
            pyautogui.write(mensagem_commit, interval=0.05)
            pyautogui.write('"', interval=0.1)
            time.sleep(0.5)
            pyautogui.press('enter')
            
            return f"✅ Comandos Git executados! Commit '{mensagem_commit}' criado com sucesso, mestre."
            
        except Exception as e:
            return f"❌ Erro ao executar comandos Git: {str(e)}, mestre."
    
    def explicar_erro_com_gemini(self, ai_model=None):
        """Usa o Gemini para explicar um erro de programação"""
        try:
            print("🔍 Analisando erro com IA...")
            
            # Lê o conteúdo da área de transferência
            try:
                erro_codigo = pyperclip.paste()
                if not erro_codigo or len(erro_codigo.strip()) < 10:
                    return "⚠️ Não encontrei um erro válido na área de transferência. Copie o erro primeiro, mestre."
                
                print(f"📋 Erro detectado: {len(erro_codigo)} caracteres")
                
            except Exception as clip_error:
                return f"❌ Erro ao ler área de transferência: {str(clip_error)}, mestre."
            
            # Usa o Gemini para explicar o erro
            if ai_model:
                try:
                    prompt = f"""
Analise este erro de programação e forneça uma explicação didática para um estudante:

ERRO:
```
{erro_codigo}
```

Forneça:
1. O que significa este erro em termos simples
2. Causas comuns que provocam este erro
3. Como corrigir (com exemplos de código)
4. Dicas para evitar no futuro

Use linguagem clara e educativa, como se estivesse ensinando programação.
"""
                    
                    response = ai_model.generate_content(prompt)
                    explicacao = response.text if response and hasattr(response, 'text') else "Não consegui gerar explicação, mestre."
                    
                    # Formata a resposta para melhor visualização
                    explicacao_formatada = f"""
🔍 ANÁLISE DE ERRO - J.A.R.V.I.S.

{'='*50}

{explicacao}

{'='*50}

💡 Dica: Sempre leia as mensagens de erro com atenção!
"""
                    
                    print(explicacao_formatada)
                    return "Análise do erro concluída! Verifique o terminal para a explicação detalhada, mestre."
                    
                except Exception as gemini_error:
                    return f"❌ Erro ao consultar Gemini: {str(gemini_error)}, mestre."
            else:
                return "⚠️ IA não disponível para análise de erro, mestre."
                
        except Exception as e:
            return f"❌ Erro ao processar solicitação: {str(e)}, mestre."
    
    def analisar_tela(self, ai_model=None):
        """Tira screenshot da tela e envia para Gemini analisar"""
        temp_file = 'temp_screen.png'
        
        try:
            print("📸 Analisando tela...")
            
            # Tira screenshot com pyautogui
            try:
                screenshot = pyautogui.screenshot(temp_file)
                print(f"✅ Screenshot salvo como {temp_file}")
            except Exception as screenshot_error:
                return f"❌ Erro ao capturar tela: {str(screenshot_error)}, mestre."
            
            # Envia para Gemini analisar
            if ai_model:
                try:
                    import google.generativeai as genai
                    
                    # Configura o modelo com suporte a visão
                    vision_model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # Carrega a imagem explicitamente
                    import PIL.Image
                    image = PIL.Image.open(temp_file)
                    
                    # Prompt para análise
                    prompt = """
Analise esta captura de tela do ambiente de desenvolvimento e identifique:

1. **Erros visíveis**: Mensagens de erro, warnings, problemas de sintaxe
2. **Problemas de código**: Bugs lógicos, variáveis não definidas, etc.
3. **Sugestões de melhoria**: Otimizações, boas práticas
4. **Correções específicas**: Código exato para corrigir problemas encontrados

Se encontrar erros de código, forneça o código corrigido completo.
Seja específico e prático, como um mentor de programação.
"""
                    
                    print("🤖 Enviando imagem para Gemini...")
                    # ANEXA EXPLICITAMENTE a imagem à chamada da API
                    response = vision_model.generate_content([prompt, image])
                    analise = response.text if response and hasattr(response, 'text') else "Não consegui analisar a tela, mestre."
                    
                    # Formata a resposta
                    analise_formatada = f"""
🔍 ANÁLISE DE TELA - J.A.R.V.I.S.

{'='*60}

{analise}

{'='*60}

💡 Dica: Mantenha seu ambiente de desenvolvimento organizado!
"""
                    
                    print(analise_formatada)
                    
                    # Verifica se há código para aplicar automaticamente
                    if "```" in analise and "corrigido" in analise.lower():
                        print("🔧 Detectado código para correção automática...")
                        self._aplicar_correcao_automatica(analise)
                    
                    return "Análise de tela concluída! Verifique o terminal para detalhes, mestre."
                    
                except Exception as gemini_error:
                    return f"❌ Erro ao analisar com Gemini: {str(gemini_error)}, mestre."
            else:
                return "⚠️ IA não disponível para análise de tela, mestre."
                
        except Exception as e:
            return f"❌ Erro ao analisar tela: {str(e)}, mestre."
        
        finally:
            # OBRIGATÓRIO: Remove o arquivo temporário para economizar memória
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    print(f"🗑️ Arquivo temporário {temp_file} removido para economizar memória")
            except Exception as cleanup_error:
                print(f"⚠️ Erro ao remover arquivo temporário: {cleanup_error}")
                # Tenta força bruta se falhar
                try:
                    import subprocess
                    subprocess.run(['del', temp_file], shell=True, check=False)
                    print(f"🗑️ Arquivo removido com força bruta")
                except:
                    print(f"❌ Não foi possível remover {temp_file}")
    
    def _aplicar_correcao_automatica(self, analise_texto):
        """Aplica correção automática se houver código na análise"""
        try:
            print("🔧 Aplicando correção automática...")
            
            # Extrai código entre blocos de código markdown
            import re
            codigo_correcoes = re.findall(r'```(?:python|javascript|html|css|json|xml)?\s*\n(.*?)\n```', 
                                       analise_texto, re.DOTALL)
            
            if codigo_correcoes:
                # Pega o último bloco de código (geralmente a versão corrigida)
                codigo_final = codigo_correcoes[-1].strip()
                
                # Copia para área de transferência
                pyperclip.copy(codigo_final)
                print("✅ Código corrigido copiado para área de transferência")
                
                # Tenta colar automaticamente na IDE
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'a')  # Seleciona tudo
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'v')  # Cola o código corrigido
                print("✅ Código corrigido aplicado automaticamente!")
                
                return True
            else:
                print("⚠️ Nenhum código para correção automática encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao aplicar correção automática: {e}")
            return False
    
    def menu_comandos(self):
        """Exibe menu organizado de todos os comandos disponíveis"""
        menu = """
🤖 MENU DE COMANDOS - J.A.R.V.I.S.

{'='*60}

📚 COMANDOS DE ESTUDO E PRODUTIVIDADE:
• 'Modo Estudo' - Abre Windsurf, música ambiente e dicas_do_dia.md
• 'Estudar [assunto]' - Gera plano de estudos personalizado
• 'Revisar [tópico]' - Cria resumo para revisão
• 'Dicas do dia' - Abre arquivo com dicas diárias

🎮 COMANDOS DO MODO GAMER:
• 'Modo Gamer' - Abre Steam, Epic Games, Discord, OBS
• 'Encerrar Modo Gamer' - Fecha todos os aplicativos gamer
• 'Abrir [jogo]' - Abre jogo específico se instalado

👁️ COMANDOS DE VISÃO COMPUTACIONAL:
• 'Olhe a tela' - Captura e analisa sua tela
• 'Analise a tela' - Identifica erros e problemas
• 'Veja a tela' - Diagnóstico completo do ambiente

💻 COMANDOS DE DESENVOLVIMENTO:
• 'Git Commit [mensagem]' - Faz commit automático
• 'Git Status' - Mostra status do repositório
• 'Git Push' - Envia alterações para o repositório
• 'Criar projeto [nome]' - Inicia novo projeto

🔧 COMANDOS DE AUTOMAÇÃO:
• 'Gerar código [descrição]' - Gera código automaticamente
• 'Corrigir erro' - Analisa e corrige erros na tela
• 'Otimizar código' - Sugere melhorias no código atual
• 'Compilar projeto' - Compila o projeto atual

🎵 COMANDOS DE ENTRETENIMENTO:
• 'Festa em casa' - Abre player de música e aumenta volume
• 'Tocar música [estilo]' - Abre música por estilo/gênero
• 'Parar música' - Para a reprodução atual

⚙️ COMANDOS DO SISTEMA:
• 'Como está o sistema?' - Status do Jarvis
• 'Limpar área de trabalho' - Organiza e limpeza
• 'Protocolo de encerramento' - Desliga o Jarvis
• 'Reiniciar sistema' - Reinicia o Jarvis

📝 COMANDOS DE TEXTO E DOCUMENTAÇÃO:
• 'Resumir [texto]' - Cria resumo automático
• 'Explicar erro' - Analisa erros de programação
• 'Documentar código' - Gera documentação automática
• 'Criar README' - Gera arquivo README.md

🌐 COMANDOS DE INTERNET:
• 'Pesquisar [termo]' - Pesquisa na web
• 'Abrir [site]' - Abre site específico
• 'Tempo agora' - Mostra previsão do tempo

💡 DICAS ESPECIAIS:
• Use comandos específicos para melhores resultados
• O Jarvis aprende com suas preferências
• Combine comandos para automação avançada
• Peça ajuda se precisar de exemplos

{'='*60}
Digite qualquer comando acima ou peça ajuda específica!
"""
        return menu.strip()
    
    def ativar_modo_estudo(self):
        """Ativa o Modo Estudo: abre Windsurf, música ambiente e dicas_do_dia.md"""
        try:
            print("📚 Ativando Modo Estudo...")
            
            # 1. Abre o Windsurf
            try:
                print("🌊 Abrindo Windsurf...")
                os.startfile("windsurf://")
                time.sleep(2)
                print("✅ Windsurf aberto com sucesso")
            except Exception as windsurf_error:
                print(f"⚠️ Erro ao abrir Windsurf: {windsurf_error}")
                # Tenta alternativa
                try:
                    os.startfile("https://windsurf.ai")
                    print("✅ Windsurf aberto via navegador")
                except:
                    print("❌ Não foi possível abrir Windsurf")
            
            # 2. Abre música ambiente (YouTube)
            try:
                print("🎵 Abrindo música ambiente...")
                # Playlist de estudo foco
                study_playlist = "https://www.youtube.com/watch?v=5qap5aO4i9A&list=PLofht4PTVXV3xJ-6o9QeYjF51i1cMq9h"
                os.startfile(study_playlist)
                time.sleep(3)
                print("✅ Música ambiente iniciada")
            except Exception as music_error:
                print(f"⚠️ Erro ao abrir música: {music_error}")
                # Tenta Spotify
                try:
                    os.startfile("spotify:")
                    print("✅ Spotify aberto como alternativa")
                except:
                    print("❌ Não foi possível abrir música")
            
            # 3. Abre o arquivo dicas_do_dia.md
            try:
                print("📝 Abrindo dicas_do_dia.md...")
                dicas_file = "dicas_do_dia.md"
                
                # Verifica se o arquivo existe
                if os.path.exists(dicas_file):
                    os.startfile(dicas_file)
                    print("✅ Arquivo dicas_do_dia.md aberto")
                else:
                    # Cria o arquivo se não existir
                    print("📝 Criando arquivo dicas_do_dia.md...")
                    dicas_content = """# Dicas do Dia - Estudo e Produtividade

## 📚 Dicas de Estudo

### 🎯 Foco e Concentração
- Use a técnica Pomodoro: 25min estudo + 5min pausa
- Elimine distrações: silencie notificações
- Ambiente organizado = mente organizada

### 🧠 Técnicas de Aprendizagem
- **Repetição espaçada**: revise em 1 dia, 3 dias, 1 semana
- **Mapas mentais**: conecte ideias visualmente
- **Ensine o que aprendeu**: solidifica o conhecimento

### 💻 Programação Eficiente
- **Code Review**: revise seu próprio código
- **Documente enquanto programa**: anote decisões importantes
- **Pequenos commits**: mudanças incrementais

### 🌟 Dica do Dia
*Atualizado diariamente com novas dicas de produtividade*

---
*Gerado por J.A.R.V.I.S. - Seu assistente de estudos*
"""
                    with open(dicas_file, 'w', encoding='utf-8') as f:
                        f.write(dicas_content)
                    
                    time.sleep(1)
                    os.startfile(dicas_file)
                    print("✅ Arquivo dicas_do_dia.md criado e aberto")
                    
            except Exception as dicas_error:
                print(f"⚠️ Erro ao abrir dicas_do_dia.md: {dicas_error}")
            
            # 4. Ajusta o volume para nível de estudo
            try:
                print("🔊 Ajustando volume para nível de estudo...")
                import pyautogui
                # Reduz um pouco o volume para não atrapalhar
                pyautogui.press('volumedown')
                pyautogui.press('volumedown')
                print("✅ Volume ajustado para estudo")
            except Exception as volume_error:
                print(f"⚠️ Erro ao ajustar volume: {volume_error}")
            
            return """
📚 MODO ESTUDO ATIVADO COM SUCESSO!

✅ Windsurf aberto para desenvolvimento
🎵 Música ambiente iniciada (Study Focus)
📝 Arquivo dicas_do_dia.md aberto para revisão
🔊 Volume ajustado para concentração

💡 Dicas para melhor estudo:
• Use fones de ouvido para melhor foco
• Faça pausas a cada 50 minutos
• Mantenha-se hidratado
• Anote dúvidas para resolver depois

Bons estudos, mestre! J.A.R.V.I.S. está aqui para ajudar.
"""
            
        except Exception as e:
            return f"❌ Erro ao ativar Modo Estudo: {str(e)}, mestre."
        
    def modo_debugger_assistido(self):
        """Modo Debugger Assistido: analisa traceback de erro no terminal"""
        try:
            print("🐛 Iniciando Modo Debugger Assistido...")
            
            # 1. Tira print focado no terminal
            temp_file = 'temp_screen.png'
            try:
                print("📸 Capturando tela para análise de erro...")
                import pyautogui
                screenshot = pyautogui.screenshot(temp_file)
                print(f"✅ Screenshot capturado: {temp_file}")
            except Exception as screenshot_error:
                return f"❌ Erro ao capturar tela: {str(screenshot_error)}, mestre."
            
            # 2. Envia para Gemini com prompt específico para análise de erro
            try:
                import google.generativeai as genai
                import PIL.Image
                
                # Carrega a imagem
                image = PIL.Image.open(temp_file)
                
                # Prompt específico para análise de traceback
                prompt_debugger = """
Você é um especialista em debugging de código Python. Analise esta captura de tela e:

1. **IDENTIFIQUE O ERRO**: Localize o traceback/mensagem de erro
2. **DIAGNÓSTICO**: Explique a causa raiz do erro de forma clara
3. **SOLUÇÃO**: Forneça o código exato para corrigir o problema
4. **PREVENÇÃO**: Dê dicas para evitar erros similares no futuro

**IMPORTANTE**:
- Seja específico e prático
- Forneça o código corrigido completo
- Explique de forma didática, como um mentor
- Foque em erros Python (SyntaxError, NameError, TypeError, etc.)

Analise a imagem e ajude o programador a resolver este erro.
"""
                
                print("🔍 Enviando para análise especializada de erro...")
                vision_model = genai.GenerativeModel('gemini-2.5-flash')
                response = vision_model.generate_content([prompt_debugger, image])
                
                analise_erro = response.text if response and hasattr(response, 'text') else "Não consegui analisar o erro, mestre."
                
                # Formata a resposta
                resultado = f"""
🐛 ANÁLISE DE ERRO - DEBUGGER ASSISTIDO

{'='*60}

{analise_erro}

{'='*60}

💡 Dicas Rápidas:
• Verifique a sintaxe linha por linha
• Use print() para debugar variáveis
• Teste pequenos trechos isoladamente
• Consulte a documentação quando necessário

🔧 Se o erro persistir, peça para "olhe a tela" para análise mais detalhada.
"""
                
                print(resultado)
                
                # Salva no JSON de memória
                self._salvar_erro_resolvido(analise_erro)
                
                return "Análise de erro concluída! Verifique o terminal para diagnóstico completo, mestre."
                
            except Exception as gemini_error:
                return f"❌ Erro ao analisar com Gemini: {str(gemini_error)}, mestre."
                
        except Exception as e:
            return f"❌ Erro no Modo Debugger Assistido: {str(e)}, mestre."
        
        finally:
            # HIGIENE DE DADOS: Remove o arquivo temporário
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    print(f"🗑️ Arquivo temporário {temp_file} removido para economizar memória")
            except Exception as cleanup_error:
                print(f"⚠️ Erro ao remover arquivo temporário: {cleanup_error}")
    
    def _salvar_erro_resolvido(self, analise):
        """Salva análise de erro no JSON de memória"""
        try:
            import json
            import datetime
            
            # Carrega dados existentes
            memoria_file = 'memoria_jarvis.json'
            dados = {}
            
            if os.path.exists(memoria_file):
                with open(memoria_file, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
            
            # Adiciona novo erro resolvido
            if 'erros_resolvidos' not in dados:
                dados['erros_resolvidos'] = []
            
            erro_entry = {
                'data': datetime.datetime.now().isoformat(),
                'tipo': 'debugging',
                'analise': analise[:500] + '...' if len(analise) > 500 else analise,
                'tags': ['erro', 'debug', 'python', 'traceback']
            }
            
            dados['erros_resolvidos'].append(erro_entry)
            
            # Mantém apenas os últimos 50 erros
            if len(dados['erros_resolvidos']) > 50:
                dados['erros_resolvidos'] = dados['erros_resolvidos'][-50:]
            
            # Salva no arquivo
            with open(memoria_file, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            print("💾 Erro resolvido salvo na memória de longo prazo")
            
        except Exception as e:
            print(f"⚠️ Erro ao salvar erro na memória: {e}")
    
    def buscar_dica_memoria(self, termo_busca):
        """Busca dicas no JSON de memória de longo prazo"""
        try:
            import json
            
            memoria_file = 'memoria_jarvis.json'
            
            if not os.path.exists(memoria_file):
                return "Ainda não tenho dicas salvas na memória, mestre. Vamos construir esse conhecimento juntos!"
            
            with open(memoria_file, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            resultados = []
            termo_lower = termo_busca.lower()
            
            # Busca em erros resolvidos
            if 'erros_resolvidos' in dados:
                for erro in dados['erros_resolvidos']:
                    if (termo_lower in erro.get('analise', '').lower() or 
                        any(termo_lower in tag.lower() for tag in erro.get('tags', []))):
                        resultados.append({
                            'tipo': 'Erro Resolvido',
                            'data': erro.get('data', ''),
                            'conteudo': erro.get('analise', '')[:200] + '...',
                            'tags': erro.get('tags', [])
                        })
            
            # Busca em dicas gerais
            if 'dicas_importantes' in dados:
                for dica in dados['dicas_importantes']:
                    if (termo_lower in dica.get('conteudo', '').lower() or 
                        any(termo_lower in tag.lower() for tag in dica.get('tags', []))):
                        resultados.append({
                            'tipo': 'Dica Importante',
                            'data': dica.get('data', ''),
                            'conteudo': dica.get('conteudo', '')[:200] + '...',
                            'tags': dica.get('tags', [])
                        })
            
            if not resultados:
                return f"Não encontrei dicas sobre '{termo_busca}' na memória, mestre. Quer que eu salve esta informação para futuras consultas?"
            
            # Formata resultados
            resposta = f"🧠 ENCONTRADOS {len(resultados)} RESULTADOS NA MEMÓRIA:\n\n"
            
            for i, resultado in enumerate(resultados[:5], 1):  # Limita a 5 resultados
                resposta += f"📌 {i}. {resultado['tipo']}\n"
                resposta += f"   📅 Data: {resultado['data'][:10]}\n"
                resposta += f"   📝 Conteúdo: {resultado['conteudo']}\n"
                resposta += f"   🏷️ Tags: {', '.join(resultado['tags'])}\n\n"
            
            if len(resultados) > 5:
                resposta += f"... e mais {len(resultados) - 5} resultados.\n"
            
            resposta += "💡 Dica: Use 'salvar dica: [sua dica]' para guardar informações importantes!"
            
            return resposta
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar na memória: {str(e)}, mestre.")
    
    def salvar_dica_memoria(self, dica):
        """Salva uma dica importante no JSON de memória"""
        try:
            import json
            import datetime
            
            memoria_file = 'memoria_jarvis.json'
            dados = {}
            
            # Carrega dados existentes
            if os.path.exists(memoria_file):
                with open(memoria_file, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
            
            # Adiciona nova dica
            if 'dicas_importantes' not in dados:
                dados['dicas_importantes'] = []
            
            dica_entry = {
                'data': datetime.datetime.now().isoformat(),
                'conteudo': dica,
                'tags': ['dica', 'importante', 'usuario'],
                'categoria': 'geral'
            }
            
            dados['dicas_importantes'].append(dica_entry)
            
            # Mantém apenas as últimas 100 dicas
            if len(dados['dicas_importantes']) > 100:
                dados['dicas_importantes'] = dados['dicas_importantes'][-100:]
            
            # Salva no arquivo
            with open(memoria_file, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            print("💾 Dica salva na memória de longo prazo")
            return "✅ Dica salva com sucesso na memória, mestre!"
            
        except Exception as e:
            print(f"⚠️ Erro ao salvar dica: {e}")
            return f"❌ Erro ao salvar dica: {str(e)}, mestre."
    
    def process_command(self, command, ai_model=None):
        """Processa um comando e executa a ação correspondente"""
        
        # Verifica se é comando do Modo Gamer
        command_lower = command.lower()
        
        # Verifica se é comando de menu
        if any(keyword in command_lower for keyword in ['menu', 'comandos', 'ajuda', 'o que você sabe fazer']):
            return self.menu_comandos()
        
        # Verifica se é comando do Modo Estudo
        if "modo estudo" in command_lower or "modostudo" in command_lower:
            return self.ativar_modo_estudo()
        
        # Verifica se é comando do Modo Debugger Assistido
        if "por que falhou" in command_lower or "debugger" in command_lower:
            return self.modo_debugger_assistido()
        
        # Verifica se é comando de busca na memória
        if "lembra daquela dica" in command_lower or "busca dica" in command_lower:
            # Extrai termo de busca
            termo = command_lower.replace("lembra daquela dica", "").replace("busca dica", "").strip()
            if termo:
                return self.buscar_dica_memoria(termo)
            else:
                return "Por favor, especifique o que você quer lembrar, mestre. Ex: 'lembra daquela dica python'"
        
        # Verifica se é comando para salvar dica
        if command_lower.startswith("salvar dica:"):
            dica = command[12:].strip()  # Remove "salvar dica:" do início
            if dica:
                return self.salvar_dica_memoria(dica)
            else:
                return "Por favor, forneça a dica para salvar, mestre. Ex: 'salvar dica: Sempre use try/except'"
        
        if "modo gamer" in command_lower or "modogamer" in command_lower:
            if "encerrar" in command_lower or "fechar" in command_lower or "desativar" in command_lower:
                return self.encerrar_modo_gamer()
            else:
                return self.ativar_modo_gamer()
        
        # Verifica se é comando Git
        if command_lower.startswith("git:"):
            mensagem_commit = command[4:].strip()  # Remove "git:" do início
            if mensagem_commit:
                return self.git_commit(mensagem_commit)
            else:
                return "Por favor, forneça uma mensagem para o commit, mestre."
        
        # Verifica se é comando de análise de tela
        if any(keyword in command_lower for keyword in ['olhe a tela', 'analise a tela', 'veja a tela']):
            return self.analisar_tela(ai_model)
        
        # Verifica se é comando para gerar código
        if any(word in command_lower for word in ['escreva um código', 'gere um código', 'crie um código', 'gerar código', 'escrever código']):
            return self.gerar_e_colar_codigo(command, ai_model)
        
        # Verifica se é comando para explicar erro
        if any(word in command_lower for word in ['explique o erro', 'qual o erro', 'corrija o erro']):
            return self.explicar_erro(command, ai_model)
        
        return None  # Retorna None se não encontrar comando correspondente
