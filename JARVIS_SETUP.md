# 🤖 J.A.R.V.I.S. - Guia de Instalação e Uso

## 📋 **Pré-requisitos**
- Python 3.8 ou superior
- Windows 10/11 (recomendado)
- Microfone (para comandos de voz)
- Webcam (para visão computacional)

## 🚀 **Instalação Rápida**

### 1. Clone/Download do Projeto
```bash
# Se estiver usando Git
git clone <repositório-jarvis>
cd jarvis

# Ou baixe os arquivos e extraia para uma pasta
```

### 2. Instale Dependências
```bash
# Instale todas as dependências
pip install -r requirements.txt

# OU instale manualmente os pacotes essenciais
pip install customtkinter google-generativeai Pillow
pip install SpeechRecognition pyttsx3 pyautogui
pip install python-dotenv pycaw screen-brightness-control
```

### 3. Configure a API Key do Gemini
1. Crie um arquivo `.env` na pasta do projeto
2. Adicione sua API key:
```env
GEMINI_API_KEY=sua_chave_api_gemini_aqui
```

**Para obter a API key:**
- Acesse: https://makersuite.google.com/app/apikey
- Faça login com sua conta Google
- Crie uma nova API key
- Copie e cole no arquivo `.env`

## 🎮 **Como Usar**

### Iniciar o J.A.R.V.I.S.
```bash
python jarvis_gui_optimized.py
```

### Comandos de Voz
- Clique no botão 🎤 **Ouvir** ou digite "Jarvis, ouvir"
- Fale claramente o comando
- Ex: "Jarvis, abra o Chrome"

### Comandos de Texto
Digite diretamente no campo de texto:
- "Jarvis, abra o YouTube"
- "Jarvis, aumente o volume"
- "Jarvis, que comandos você aceita?"

## 📱 **Comandos Disponíveis**

### 🚨 **Comando de Emergência**
```
"Jarvis, protocolo silêncio"
"Jarvis, silêncio total"
"Jarvis, emergência silêncio"
"Jarvis, fechar tudo e silenciar"
OU clique no botão 🚨 vermelho
```

### �️ **Aplicativos**
```
"Jarvis, abra o Chrome"
"Jarvis, inicie o VS Code"
"Jarvis, abra o Spotify"
"Jarvis, abra o Bloco de Notas"
"Jarvis, inicie o Firefox"
"Jarvis, abra o Discord"
```

### 🌐 **Links Rápidos**
```
"Jarvis, abra o YouTube"
"Jarvis, acesse o GitHub"
"Jarvis, abra o Portal da Faculdade"
"Jarvis, abra o Gmail"
"Jarvis, acesse o Netflix"
```

### 🔊 **Controle de Áudio**
```
"Jarvis, aumente o volume"
"Jarvis, diminua o volume"
"Jarvis, silencie o áudio"
"Jarvis, ative o som"
```

### ☀️ **Controle de Brilho**
```
"Jarvis, aumente o brilho"
"Jarvis, diminua o brilho"
"Jarvis, brilho máximo"
"Jarvis, brilho mínimo"
```

### 👁️ **Visão Computacional**
```
Clique no botão 👁️ ou digite:
"Jarvis, analise minha tela"
"Jarvis, veja o que está na tela"
```

### 🎤 **Comandos de Voz**
```
"Jarvis, ouvir" - Inicia escuta
"Jarvis, pare de ouvir" - Para escuta
```

## 🔧 **Recursos Avançados**

### Memória Persistente
O J.A.R.V.I.S. lembra conversas anteriores e comandos executados.

### Contexto Inteligente
Ele mantém o contexto da conversa para respostas mais coerentes.

### Detecção Automática
Detecta automaticamente se você quer executar um comando ou apenas conversar.

## 🛠️ **Solução de Problemas**

### Problemas Comuns

**"Módulo de controle de sistema não disponível"**
```bash
pip install pycaw screen-brightness-control
```

**"API Key não encontrada"**
- Verifique se o arquivo `.env` existe
- Confirme que a API key está correta
- Reinicie o programa

**"Sistema de voz não disponível"**
- Verifique se o microfone está conectado
- Teste com: `python -c "import speech_recognition; print('OK')"`

**"Visão computacional não disponível"**
- Verifique sua API key do Gemini
- Teste sua conexão com internet

### Logs e Erros
- `jarvis_log.txt` - Logs gerais do sistema
- `ERRO_CRITICO.txt` - Erros críticos (se ocorrerem)

## 📁 **Estrutura de Arquivos**
```
jarvis/
├── jarvis_gui_optimized.py      # Interface principal otimizada
├── jarvis_gui_integrada.py       # Versão original
├── jarvis_system_controller.py  # Módulo de controle de sistema
├── jarvis_memory.db             # Banco de dados de memória
├── .env                         # Variáveis de ambiente
├── requirements.txt             # Dependências
├── jarvis_log.txt              # Logs do sistema
└── ERRO_CRITICO.txt            # Erros críticos
```

## 🎯 **Dicas de Uso**

1. **Seja Específico**: "Abra o Chrome" é melhor que "Abra navegador"
2. **Use Voz Clara**: Fale em tom normal e claro
3. **Espere a Resposta**: Aguarde o processamento antes de novos comandos
4. **Contexto**: Ele lembra conversas anteriores

## 🔄 **Atualizações**

Para atualizar dependências:
```bash
pip install --upgrade -r requirements.txt
```

## 📞 **Suporte**

Se encontrar problemas:
1. Verifique os logs em `jarvis_log.txt`
2. Confirme se todas as dependências estão instaladas
3. Teste sua API key do Gemini

---

**J.A.R.V.I.S. - Seu assistente de IA pessoal** 🚀
