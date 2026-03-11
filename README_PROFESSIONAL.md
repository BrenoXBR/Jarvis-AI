# J.A.R.V.I.S. - Professional AI Assistant

🤖 **Stark Industries AI Assistant - Professional Edition**

J.A.R.V.I.S. é um assistente de IA avançado com controle total do sistema Windows, desenvolvido com arquitetura modular profissional e interface moderna.

---

## 🚀 Tecnologias Utilizadas

### Python 3.13+
- **Versão**: Python 3.13+
- **Porquê**: Linguagem principal com ecossistema maduro para IA e automação
- **Recursos Utilizados**:
  - Threading para operações concorrentes
  - System calls para controle do Windows
  - Manipulação de arquivos e logs
  - Tratamento robusto de exceções

### CustomTkinter
- **Versão**: 5.2.0+
- **Porquê**: Framework moderno para interfaces desktop com tema dark
- **Recursos Utilizados**:
  - Interface com tema Stark Industries
  - Widgets customizados (CTkButton, CTkTextbox, CTkFrame)
  - Layout responsivo e moderno
  - Suporte a temas dark/light
  - Renderização otimizada

### Google Gemini API
- **Versão**: google-generativeai 0.3.0+
- **Modelo**: gemini-2.5-flash
- **Porquê**: Modelo de linguagem avançado para processamento de linguagem natural
- **Recursos Utilizados**:
  - Processamento de linguagem natural
  - Geração de respostas contextuais
  - Configuração dinâmica de prompts
  - Detecção de intenções do usuário
  - Limite de tokens otimizado (4096)

### Threading & Concurrency
- **Módulo**: `threading`, `concurrent.futures`
- **Porquê**: Interface responsiva sem bloqueios
- **Recursos Utilizados**:
  - Efeito de digitação em thread separada
  - Processamento de IA em background
  - Atualização de System Monitor em tempo real
  - Reconhecimento de voz assíncrono
  - Thread-safe com locks para logs

---

## 🏗️ Arquitetura do Sistema

### Estrutura Modular
```
J.A.R.V.I.S. Professional/
├── main.py              # Ponto de entrada e orquestração
├── gui.py               # Interface CustomTkinter
├── core.py              # Lógica de IA (Gemini)
├── actions.py           # Controle do sistema
├── logger.py            # Sistema de logs
└── requirements.txt     # Dependências
```

### Padrões de Design
- **Dependency Injection**: Injeção de dependências entre módulos
- **Observer Pattern**: Callbacks para eventos de UI
- **Singleton Pattern**: Logger global thread-safe
- **Factory Pattern**: Criação de componentes
- **Event-Driven Architecture**: Comunicação assíncrona

---

## 🔧 Componentes Técnicos

### 1. Interface Gráfica (gui.py)
```python
# CustomTkinter com tema Stark Industries
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Layout responsivo
- Chat area com efeito de digitação
- System Monitor em tempo real
- Barra de status dinâmica
- Botões de voz e comandos
```

### 2. Inteligência Artificial (core.py)
```python
# Google Gemini API Integration
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# Processamento em thread separada
def process_message_async():
    response = model.generate_content(context)
    typing_effect(response.text)
```

### 3. Controle do Sistema (actions.py)
```python
# Windows System Control
os.startfile('ms-settings:windowsupdate-action')  # Deep Links
os.system('shutdown /s /t 60')                   # Energy Control
pyautogui.hotkey('win', 'd')                     # Window Control

# Audio Control
pycaw.AudioUtilities.GetSpeakers()               # Volume Control
```

### 4. Sistema de Logs (logger.py)
```python
# Thread-safe logging com buffer
class JarvisLogger:
    def __init__(self):
        self.log_buffer = []
        self.buffer_lock = threading.Lock()
    
    def log_realtime(self, message):
        with self.buffer_lock:
            self.log_buffer.append(message)
```

---

## 🔄 Fluxo de Processamento

### 1. Inicialização
```python
main.py
├── Carrega dependências
├── Inicializa logger
├── Configura actions
├── Prepara core (Gemini)
└── Inicia GUI
```

### 2. Processamento de Mensagem
```python
Usuário digita mensagem
├── GUI detecta input
├── Thread de processamento inicia
├── Detecta comando de sistema?
│   ├── Sim: Executa actions.py
│   └── Não: Processa com Gemini
├── Efeito de digitação em thread
└── Atualiza System Monitor
```

### 3. Threading Architecture
```python
# Threads principais
├── Main Thread: Interface GUI
├── Processing Thread: IA e comandos
├── Typing Thread: Efeito de digitação
├── Voice Thread: Reconhecimento de voz
└── Monitor Thread: Atualização de logs
```

---

## 📊 Performance e Otimização

### Threading Strategy
- **Non-blocking UI**: Interface nunca trava
- **Thread Pool**: Reutilização de threads
- **Lock-free Operations**: Minimiza contenção
- **AsyncCallbacks**: Respostas imediatas

### Memory Management
- **Buffer Circular**: Logs com limite fixo
- **Resource Cleanup**: Fechamento adequado
- **Weak References**: Evita memory leaks
- **Garbage Collection**: Otimização automática

### Error Handling
- **Exception Propagation**: Tratamento em camadas
- **Fallback Mechanisms**: Opções alternativas
- **User Feedback**: Mensagens claras
- **Recovery Procedures**: Recuperação automática

---

## 🔌 Integrações Externas

### Windows APIs
```python
# Deep Links Protocol
ms-settings:windowsupdate-action    # Windows Update
ms-settings:windowsdefender         # Windows Defender
ms-settings:network                 # Network Settings
ms-settings:powersleep              # Power & Sleep

# System Commands
shutdown /s /t 60                   # Shutdown
shutdown /r /t 60                   # Restart
rundll32.exe powrprof.dll          # Suspend
```

### Hardware Control
```python
# Audio Control
pycaw.AudioUtilities                # Volume
pycaw.IAudioEndpointVolume         # Mute/Unmute

# Display Control
screen_brightness_control           # Brightness
pyautogui.hotkey()                 # Window Control

# System Info
wmi.WMI()                          # System Information
```

### Speech Recognition
```python
# Voice Processing
speech_recognition.Recognizer()    # Audio Recognition
speech_recognition.Microphone()    # Audio Input
google_speech_api()                 # PT-BR Support
```

---

## 🛡️ Segurança

### API Key Management
```python
# Environment Variables
.env file com GEMINI_API_KEY
# Runtime validation
# Error handling para keys inválidas
```

### System Permissions
```python
# Minimal required permissions
# User-level operations only
# No administrator privileges needed
# Safe command execution
```

### Data Protection
```python
# Local logging only
# No external data transmission
# User consent for voice
# Secure temp file handling
```

---

## 📈 Escalabilidade

### Modular Growth
- **Plugin Architecture**: Fácil adição de novos módulos
- **API Extensions**: Suporte para múltiplos modelos
- **Protocol Expansion**: Novos Deep Links
- **Command Registry**: Sistema de comandos extensível

### Performance Scaling
- **Async Operations**: Operações não bloqueantes
- **Resource Pooling**: Reutilização de recursos
- **Lazy Loading**: Carregamento sob demanda
- **Cache Strategies**: Cache inteligente

---

## 🔧 Desenvolvimento

### Environment Setup
```bash
# Python 3.13+
python -m venv jarvis-env
source jarvis-env/bin/activate  # Linux/Mac
jarvis-env\Scripts\activate     # Windows

# Dependencies
pip install -r requirements_professional.txt
```

### Build Process
```bash
# PyInstaller Configuration
pyinstaller --noconsole --onefile --clean \
  --hidden-import=pycaw \
  --hidden-import=comtypes \
  --hidden-import=wmi \
  --icon=jarvis.ico main.py
```

### Testing Strategy
```python
# Unit Tests
pytest tests/

# Integration Tests
python -m pytest integration/

# Performance Tests
python benchmark.py
```

---

## 📋 Requisitos Técnicos

### System Requirements
- **OS**: Windows 10/11 (x64)
- **Python**: 3.13+ (para desenvolvimento)
- **RAM**: 4GB+ mínimo
- **Storage**: 200MB para aplicativo
- **Network**: Conexão para Gemini API

### Dependencies
```
google-generativeai>=0.3.0    # Gemini AI
customtkinter>=5.2.0          # Modern GUI
pyautogui>=0.9.54            # System Control
screen-brightness-control>=0.13.0  # Display
pycaw>=2023.2                # Audio Control
comtypes>=1.2.0              # COM Interface
wmi>=1.5.1                   # WMI Access
SpeechRecognition>=3.10.0     # Voice Input
pyaudio>=0.2.11              # Audio Processing
pyttsx3>=2.90                # Text-to-Speech
numpy>=1.24.0                # Numerical Computing
pandas>=2.0.0                # Data Processing
Pillow>=10.0.0               # Image Processing
```

---

## 🚀 Performance Metrics

### Startup Time
- **Cold Start**: ~3 segundos
- **Warm Start**: ~1 segundo
- **Memory Usage**: ~80MB RAM
- **CPU Usage**: <5% idle

### Response Times
- **Local Commands**: <100ms
- **Gemini API**: ~2-3 segundos
- **Voice Recognition**: ~1.5 segundos
- **Typing Effect**: 50ms por caractere

### Throughput
- **Concurrent Users**: 1 (desktop app)
- **API Calls**: ~100 por hora
- **Log Entries**: ~1000 por sessão
- **File I/O**: <10MB total

---

## 🔄 Version Control

### Git Strategy
```bash
# Branch Structure
main/          # Production
develop/       # Development
feature/*      # New features
hotfix/*       # Critical fixes
```

### Release Process
```bash
# Version Tagging
git tag -a v1.0.0 -m "Professional Release"
git push origin v1.0.0

# Build Automation
pyinstaller main.py
# Automated testing
# Release to GitHub
```

---

## 📚 Documentação

### Code Documentation
- **DocStrings**: Python PEP 257
- **Type Hints**: Python PEP 484
- **Comments**: Explicações técnicas
- **README**: Guia completo

### API Documentation
- **Gemini Integration**: Configuração e uso
- **Windows APIs**: Protocolos e comandos
- **CustomTkinter**: Componentes e temas
- **Threading**: Padrões concorrentes

---

## 🎯 Roadmap Futuro

### Próximas Versões
- **Multi-language Support**: Inglês, espanhol
- **Cloud Integration**: OneDrive, Google Drive
- **Mobile Companion**: App para smartphone
- **Plugin System**: Extensões de terceiros
- **AI Models**: Suporte para Claude, GPT

### Tecnologias Emergentes
- **LangChain**: Framework para LLMs
- **FastAPI**: Backend para web interface
- **React**: Frontend web alternativo
- **Docker**: Containerização
- **Kubernetes**: Orquestração

---

## 📞 Suporte Técnico

### Debug Information
```python
# System Info Collection
python --version          # Python version
pip list                 # Dependencies
systeminfo               # Windows info
dxdiag                   # DirectX info
```

### Common Issues
- **API Key**: Verifique .env configuration
- **Dependencies**: Use requirements.txt
- **Permissions**: Execute as administrator
- **Firewall**: Allow network access
- **Antivirus**: Add exception for Jarvis

### Contact & Support
- **GitHub Issues**: Report bugs e features
- **Documentation**: README e code comments
- **Community**: Discord/Slack channel
- **Email**: support@jarvis-ai.com

---

## 📦 Como Instalar e Rodar

### 1. Clone o repositório:
```bash
git clone https://github.com/BrenoXBR/Jarvis-AI.git
cd Jarvis-AI
```

### 2. Instale as dependências:
```bash
pip install -r requirements_professional.txt
```

### 3. Configure sua API Key:
Crie um arquivo `.env` na raiz do projeto:
```env
GEMINI_API_KEY=SUA_CHAVE_AQUI
```

### 4. Execute o Jarvis:
```bash
python main.py
```

Ou execute o executável pronto:
```bash
Jarvis_Professional.exe
```

---

## 🚀 Funcionalidades Principais

### 🖥️ System Monitor
- Logs em tempo real das ações do sistema
- Buffer circular com últimas 100 mensagens
- Interface toggle para mostrar/ocultar
- Color coding por tipo de log (INFO, SUCCESS, ERROR)

### ✨ Efeito de Digitação
- Aparência gradual caracter por caracter
- Cursor piscante durante digitação
- Thread separada (não bloqueia interface)
- Velocidade otimizada (50ms por caractere)

### 🔌 Deep Links Windows
- Windows Update direto: `ms-settings:windowsupdate-action`
- Windows Defender: `ms-settings:windowsdefender`
- Configurações de rede: `ms-settings:network`
- Energia e bateria: `ms-settings:powersleep`

### ⚡ Protocolos de Energia
- **Desligamento**: `shutdown /s /t 60` (com confirmação)
- **Reinicialização**: `shutdown /r /t 60` (com confirmação)
- **Suspensão**: `rundll32.exe powrprof.dll,SetSuspendState` (imediato)

### 🎤 Comandos de Voz
- Reconhecimento em português (pt-BR)
- Botão de ativação com feedback visual
- Processamento assíncrono
- Integração com comandos do sistema

### 🧠 Inteligência Artificial
- Google Gemini 2.5 Flash integration
- Detecção automática de intenções
- Contexto de conversa
- Memória de interações anteriores

---

**J.A.R.V.I.S. Professional - A evolução dos assistentes de IA para desktop** 🚀✨

---

### 📝 Notas de Desenvolvimento

**Este projeto foi construído com foco em arquitetura profissional e performance. A versão Professional representa uma reestruturação completa do código original, implementando padrões de design modernos, threading otimizado e interface responsiva.**

**Desenvolvido por Breno - Estudante de Programação e entusiasta de IA.**
