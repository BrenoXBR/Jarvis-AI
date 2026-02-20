#!/usr/bin/env python3
"""
Mobile Bridge para Jarvis - Conexão com Telegram
Permite controle remoto via Telegram com segurança máxima
"""

import asyncio
import logging
import os
import tempfile
from datetime import datetime
from typing import Optional
import speech_recognition as sr
import pyautogui
from PIL import Image
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MobileBridge:
    """Ponte móvel para Jarvis via Telegram"""
    
    def __init__(self, token: str, jarvis_instance=None):
        self.token = token
        self.jarvis_instance = jarvis_instance
        self.authorized_chat_id = None
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configuração inicial do reconhecimento
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
        # Carrega chat_id autorizado se existir
        self.load_authorized_chat()
        
    def load_authorized_chat(self):
        """Carrega o chat_id autorizado do arquivo"""
        try:
            auth_file = os.path.join(os.getcwd(), 'telegram_auth.json')
            if os.path.exists(auth_file):
                with open(auth_file, 'r') as f:
                    data = json.load(f)
                    self.authorized_chat_id = data.get('chat_id')
                    logger.info(f"Chat autorizado carregado: {self.authorized_chat_id}")
        except Exception as e:
            logger.error(f"Erro ao carregar chat autorizado: {e}")
            
    def save_authorized_chat(self, chat_id: int):
        """Salva o chat_id autorizado"""
        try:
            auth_file = os.path.join(os.getcwd(), 'telegram_auth.json')
            data = {'chat_id': chat_id}
            with open(auth_file, 'w') as f:
                json.dump(data, f)
            self.authorized_chat_id = chat_id
            logger.info(f"Chat autorizado salvo: {chat_id}")
        except Exception as e:
            logger.error(f"Erro ao salvar chat autorizado: {e}")
            
    def is_authorized(self, chat_id: int) -> bool:
        """Verifica se o chat está autorizado"""
        if self.authorized_chat_id is None:
            # Primeiro usuário a enviar mensagem se torna autorizado
            self.save_authorized_chat(chat_id)
            return True
        return chat_id == self.authorized_chat_id
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - inicialização do bot"""
        chat_id = update.effective_chat.id
        
        if not self.is_authorized(chat_id):
            await update.message.reply_text(
                "⚠️ Acesso não autorizado. Este bot está vinculado a apenas um usuário."
            )
            return
            
        if self.authorized_chat_id == chat_id:
            await update.message.reply_text(
                "🤖 Jarvis Mobile Bridge ativado!\n\n"
                "Comandos disponíveis:\n"
                "/start - Inicializa o bot\n"
                "/print - Captura tela do PC\n"
                "/status - Status do sistema\n"
                "\nEnvie comandos de texto ou áudio para controlar o Jarvis!"
            )
        else:
            # Primeiro usuário a usar o bot
            self.save_authorized_chat(chat_id)
            await update.message.reply_text(
                "🔐 Dispositivo autorizado com sucesso!\n\n"
                "Você agora é o único usuário autorizado a controlar o Jarvis remotamente.\n\n"
                "Comandos disponíveis:\n"
                "/start - Inicializa o bot\n"
                "/print - Captura tela do PC\n"
                "/status - Status do sistema\n"
                "\nEnvie comandos de texto ou áudio para controlar o Jarvis!"
            )
            
    async def print_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /print - captura tela"""
        chat_id = update.effective_chat.id
        
        if not self.is_authorized(chat_id):
            await update.message.reply_text("⚠️ Acesso não autorizado.")
            return
            
        try:
            print("📸 Comando /print recebido do Telegram")
            await update.message.reply_text("📸 Capturando tela do PC...")
            
            # Captura a tela
            print("🖥️ Capturando screenshot com pyautogui...")
            screenshot = pyautogui.screenshot()
            print("✅ Screenshot capturado com sucesso")
            
            # Salva em arquivo temporário
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_file = os.path.join(tempfile.gettempdir(), f"jarvis_screenshot_{timestamp}.png")
            screenshot.save(temp_file, 'PNG')
            print(f"💾 Imagem salva em: {temp_file}")
            
            # Envia a imagem
            with open(temp_file, 'rb') as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=f"📸 Screenshot capturado em {datetime.now().strftime('%H:%M:%S')}"
                )
            print("📤 Imagem enviada para o Telegram")
                
            # Remove arquivo temporário
            os.remove(temp_file)
            print("🗑️ Arquivo temporário removido")
            
        except Exception as e:
            await update.message.reply_text(f"Erro ao capturar tela: {str(e)}")
            
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status - status do sistema"""
        chat_id = update.effective_chat.id
        
        if not self.is_authorized(chat_id):
            await update.message.reply_text("⚠️ Acesso não autorizado.")
            return
            
        try:
            # Status básico do sistema
            status_msg = f"""
🤖 **Status Jarvis Mobile Bridge**

📅 **Data/Hora:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
🔐 **Chat Autorizado:** {self.authorized_chat_id}
📱 **Seu Chat ID:** {chat_id}
🎤 **Reconhecimento de Voz:** ✅ Ativo
📸 **Captura de Tela:** ✅ Ativa
🤖 **Jarvis Conectado:** {'Sim' if self.jarvis_instance else 'Não'}

**Comandos Disponíveis:**
/start - Inicialização
/print - Capturar tela
/status - Este status
            """
            
            await update.message.reply_text(status_msg, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Erro ao obter status: {str(e)}")
            
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Processa mensagens de texto"""
        chat_id = update.effective_chat.id
        message_text = update.message.text
        
        if not self.is_authorized(chat_id):
            await update.message.reply_text("⚠️ Acesso não autorizado.")
            return
            
        try:
            # Envia confirmação
            await update.message.reply_text("🔄 Processando comando...")
            
            # Processa comando com Jarvis se disponível
            if self.jarvis_instance:
                # Simula comando de voz para Jarvis
                response = await self.process_jarvis_command(message_text)
                await update.message.reply_text(f"🤖 Jarvis: {response}")
            else:
                # Resposta padrão se Jarvis não estiver conectado
                await update.message.reply_text(
                    f"📝 Comando recebido: '{message_text}'\n"
                    "⚠️ Jarvis não está conectado. Inicie o Jarvis primeiro."
                )
                
        except Exception as e:
            await update.message.reply_text(f"Erro ao processar comando: {str(e)}")
            
    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Processa mensagens de áudio"""
        chat_id = update.effective_chat.id
        
        if not self.is_authorized(chat_id):
            await update.message.reply_text("⚠️ Acesso não autorizado.")
            return
            
        try:
            # Envia confirmação
            await update.message.reply_text("🎤 Processando áudio...")
            
            # Baixa o arquivo de áudio
            voice_file = await update.message.voice.get_file()
            voice_path = os.path.join(tempfile.gettempdir(), f"voice_{chat_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ogg")
            await voice_file.download_to_drive(voice_path)
            
            # Transcreve o áudio
            transcribed_text = await self.transcribe_audio(voice_path)
            
            if transcribed_text:
                await update.message.reply_text(f"📝 Transcrição: '{transcribed_text}'")
                
                # Processa comando com Jarvis
                if self.jarvis_instance:
                    response = await self.process_jarvis_command(transcribed_text)
                    await update.message.reply_text(f"🤖 Jarvis: {response}")
                else:
                    await update.message.reply_text(
                        f"📝 Comando transcrevido: '{transcribed_text}'\n"
                        "⚠️ Jarvis não está conectado. Inicie o Jarvis primeiro."
                    )
            else:
                await update.message.reply_text("Nao foi possivel transcrever o audio.")
                
            # Remove arquivo temporário
            os.remove(voice_path)
            
        except Exception as e:
            await update.message.reply_text(f"Erro ao processar audio: {str(e)}")
            
    async def transcribe_audio(self, audio_path: str) -> Optional[str]:
        """Transcreve áudio usando reconhecimento de fala"""
        try:
            # Converte OGG para WAV se necessário (simplificação)
            # Na prática, você precisaria de uma biblioteca como pydub
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                
            # Usa Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language='pt-BR')
            return text
            
        except sr.UnknownValueError:
            logger.error("Não foi possível entender o áudio")
            return None
        except sr.RequestError as e:
            logger.error(f"Erro no serviço de reconhecimento: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao transcrever áudio: {e}")
            return None
            
    async def process_jarvis_command(self, command: str) -> str:
        """Processa comando com Jarvis (simulação)"""
        try:
            if self.jarvis_instance and hasattr(self.jarvis_instance, 'process_command'):
                # Se Jarvis tiver método de processamento
                return await asyncio.get_event_loop().run_in_executor(
                    None, self.jarvis_instance.process_command, command
                )
            else:
                # Resposta simulada baseada em comandos conhecidos
                command_lower = command.lower()
                
                if "horas" in command_lower:
                    return f"São {datetime.now().strftime('%H:%M')}, mestre."
                elif "data" in command_lower:
                    return f"Hoje é {datetime.now().strftime('%d/%m/%Y')}."
                elif "status" in command_lower:
                    return "Sistema operacional em 100%, mestre."
                elif "print" in command_lower:
                    return "Screenshot capturado com sucesso!"
                else:
                    return f"Comando '{command}' recebido e processado, mestre."
                    
        except Exception as e:
            return f"Erro ao processar comando: {str(e)}"
            
    def setup_handlers(self, application: Application):
        """Configura os handlers do bot"""
        # Comandos
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("print", self.print_command))
        application.add_handler(CommandHandler("status", self.status_command))
        
        # Mensagens
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
        application.add_handler(MessageHandler(filters.VOICE, self.handle_voice_message))
        
        # Configura comandos do bot
        commands = [
            BotCommand("start", "Inicia o Jarvis Mobile Bridge"),
            BotCommand("print", "Captura tela do PC"),
            BotCommand("status", "Status do sistema"),
        ]
        application.bot.set_my_commands(commands)
        
    async def start_bot(self):
        """Inicia o bot Telegram"""
        try:
            # Cria a aplicação
            application = Application.builder().token(self.token).build()
            
            # Configura handlers
            self.setup_handlers(application)
            
            logger.info("Jarvis Mobile Bridge iniciado!")
            
            # Inicia o bot com await
            await application.initialize()
            await application.start()
            
        except Exception as e:
            logger.error(f"Erro ao iniciar bot: {e}")
            
    def run(self):
        """Executa o bot (síncrono para compatibilidade)"""
        try:
            asyncio.run(self.start_bot())
        except KeyboardInterrupt:
            logger.info("Bot interrompido pelo usuário")
        except Exception as e:
            logger.error(f"Erro ao executar bot: {e}")

class JarvisMobileBridge:
    """Interface principal para integração com Jarvis"""
    
    def __init__(self, jarvis_instance=None):
        from dotenv import load_dotenv
        load_dotenv()
        self.token = os.getenv('TELEGRAM_TOKEN', '8258052958:AAHuP3qcBdE7Kn9TIRgPggI2ddiSDJFRxEU')
        self.bridge = MobileBridge(self.token, jarvis_instance)
        
    def start(self):
        """Inicia o bridge móvel"""
        print("🤖 Iniciando Jarvis Mobile Bridge...")
        print("📱 Conectando ao Telegram...")
        print(f"🔐 Token: {self.token[:10]}...")
        print("⚠️ Apenas o primeiro usuário será autorizado!")
        print("🎤 Pronto para receber comandos de texto e áudio")
        print("📸 Comando /print disponível para capturar tela")
        print("-" * 50)
        
        # Inicia o bot em um loop de eventos separado
        asyncio.run(self.bridge.start_bot())

def main():
    """Função principal para teste independente"""
    bridge = JarvisMobileBridge()
    bridge.start()

if __name__ == "__main__":
    main()
