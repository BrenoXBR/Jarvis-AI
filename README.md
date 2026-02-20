# 🤖 J.A.R.V.I.S. - Assistente Pessoal para Desenvolvedores

O J.A.R.V.I.S. é um assistente virtual inteligente desenvolvido em Python, integrado à API do Google Gemini 1.5 Flash. Criado originalmente para otimizar a rotina de estudos de programação, o projeto evoluiu para um ecossistema que ouve, fala e **enxerga** a tela do usuário através de visão computacional.

## 🚀 Funcionalidades Principais

* **👁️ Visão Computacional:** O Jarvis consegue capturar e analisar a tela do Windows em tempo real. Se você tiver um erro visual ou precisar que ele leia algo, ele processa a imagem e responde imediatamente.
* **🐞 Modo Debugger Assistido:** Ao encontrar um erro no terminal, você pode pedir para o Jarvis analisar. Ele captura o print, lê o **Traceback** e sugere a correção de forma didática.
* **🧠 Memória de Longo Prazo:** Utiliza persistência de dados em arquivos JSON para lembrar dicas de código, erros resolvidos e preferências do usuário, mantendo o contexto mesmo após ser reiniciado.
* **🎮 Modo Gamer & Produtividade:** Automação via comandos de voz/texto para abrir ou encerrar pacotes de softwares (como Discord, Steam e Opera GX) de uma só vez.
* **📂 Integração com Git:** Automação de comandos `git add` e `git commit` diretamente pelo assistente para agilizar o fluxo de trabalho.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Cérebro IA:** Google Gemini API (Modelo 1.5 Flash)
* **Automação de Sistema:** `PyAutoGUI` & `PyperClip`
* **Processamento de Imagem:** `Pillow` (PIL)
* **Síntese de Voz:** `pyttsx3`
* **Ambiente de Desenvolvimento:** Windsurf IDE

## 📦 Como Instalar e Rodar

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/BrenoXBR/Jarvis-AI.git](https://github.com/BrenoXBR/Jarvis-AI.git)
   ```
2. **Instale as dependências necessárias:**

  ```bash
pip install pyautogui pillow google-generativeai python-dotenv pyttsx3 pyperclip
  ```

3. **Configure sua API Key:**
Crie um arquivo .env na raiz do projeto e adicione sua chave:

  ```Snippet de código

GEMINI_API_KEY=SUA_CHAVE_AQUI
  ```
Inicie o Jarvis:

  ```Bash

python main.py
  ```

##  📝 Notas de Desenvolvimento
**Este projeto foi construído com foco em aprendizado contínuo. A cada erro corrigido pelo "Modo Debugger", o Jarvis armazena a solução em sua memória local, tornando-se um mentor cada vez mais personalizado para o desenvolvedor.**

**Desenvolvido por Breno - Estudante de Programação e entusiasta de IA.**
