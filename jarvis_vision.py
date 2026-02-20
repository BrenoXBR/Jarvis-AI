#!/usr/bin/env python3
"""
Sistema de Visão do Jarvis
Captura de tela e análise com IA multimodal
"""

import os
import time
import tempfile
from datetime import datetime
import pyautogui
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai
from dotenv import load_dotenv

class JarvisVision:
    """Sistema de visão computacional do Jarvis"""
    
    def __init__(self, api_key=None):
        """Inicializa o sistema de visão"""
        load_dotenv()
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.temp_dir = os.path.join(tempfile.gettempdir(), 'jarvis_vision')
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Inicializa modelo vision
        if self.api_key and self.api_key != 'sua_api_key_aqui':
            try:
                genai.configure(api_key=self.api_key)
                self.vision_model = genai.GenerativeModel('gemini-pro-vision')
                self.vision_enabled = True
            except Exception as e:
                print(f"Erro ao inicializar visão: {e}")
                self.vision_enabled = False
        else:
            self.vision_enabled = False
            
    def capture_screen(self, region=None, add_overlay=False):
        """Captura a tela ou região específica"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screen_{timestamp}.png"
            filepath = os.path.join(self.temp_dir, filename)
            
            if region:
                # Captura região específica (left, top, width, height)
                screenshot = pyautogui.screenshot(region=region)
            else:
                # Captura tela inteira
                screenshot = pyautogui.screenshot()
                
            if add_overlay:
                # Adiciona overlay informativo
                screenshot = self._add_overlay(screenshot, timestamp)
                
            # Salva imagem
            screenshot.save(filepath, 'PNG')
            
            return filepath, screenshot
            
        except Exception as e:
            print(f"Erro ao capturar tela: {e}")
            return None, None
            
    def _add_overlay(self, image, timestamp):
        """Adiciona overlay informativo à imagem"""
        try:
            # Converte para modo RGBA se necessário
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
                
            # Cria layer para overlay
            overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Tenta usar fonte padrão, fallback para padrão
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
                
            # Adiciona informações
            timestamp_text = f"Jarvis Vision - {timestamp}"
            draw.text((10, 10), timestamp_text, fill=(0, 255, 255, 200), font=font)
            
            # Combina imagens
            combined = Image.alpha_composite(image, overlay)
            return combined
            
        except Exception as e:
            print(f"⚠️ Erro ao adicionar overlay: {e}")
            return image
            
    def analyze_image(self, image_path, question="O que você vê nesta imagem?"):
        """Analisa imagem com o modelo de visão"""
        if not self.vision_enabled:
            return "Sistema de visão não disponível. Configure a API key do Gemini Vision."
            
        if not os.path.exists(image_path):
            return "Imagem não encontrada."
            
        try:
            # Carrega imagem
            image = Image.open(image_path)
            
            # Prepara prompt
            prompt = f"""
Você é J.A.R.V.I.S., o assistente do Homem de Ferra.
Analise esta imagem e responda à pergunta do usuário.

PERGUNTA: {question}

INSTRUÇÕES:
- Seja técnico e preciso como o J.A.R.V.I.S.
- Se for código, identifique erros e sugira correções
- Se for interface, descreva o que está acontecendo
- Seja direto e objetivo
- Responda em português

Análise:
"""
            
            # Envia para o modelo
            response = self.vision_model.generate_content([
                prompt,
                image
            ])
            
            return response.text
            
        except Exception as e:
            return f"Erro ao analisar imagem: {str(e)}"
            
    def capture_and_analyze(self, question="O que você vê na minha tela?"):
        """Captura tela e analisa em uma operação"""
        # Captura tela
        image_path, screenshot = self.capture_screen(add_overlay=True)
        
        if not image_path:
            return "Não foi possível capturar a tela."
            
        # Analisa imagem
        analysis = self.analyze_image(image_path, question)
        
        # Limpa arquivo temporário
        try:
            os.remove(image_path)
        except:
            pass
            
        return analysis
        
    def get_active_window_region(self):
        """Obtém a região da janela ativa"""
        try:
            # Obtém posição da janela ativa
            active_window = pyautogui.getActiveWindow()
            if active_window:
                return (
                    active_window.left,
                    active_window.top,
                    active_window.width,
                    active_window.height
                )
        except:
            pass
            
        return None
        
    def capture_active_window(self, question="O que há nesta janela?"):
        """Captura apenas a janela ativa"""
        region = self.get_active_window_region()
        
        if region:
            image_path, screenshot = self.capture_screen(region=region, add_overlay=True)
        else:
            image_path, screenshot = self.capture_screen(add_overlay=True)
            
        if not image_path:
            return "Não foi possível capturar a janela ativa."
            
        # Analisa imagem
        analysis = self.analyze_image(image_path, question)
        
        # Limpa arquivo temporário
        try:
            os.remove(image_path)
        except:
            pass
            
        return analysis
        
    def cleanup_temp_files(self):
        """Limpa arquivos temporários de visão"""
        try:
            import glob
            temp_files = glob.glob(os.path.join(self.temp_dir, "*.png"))
            temp_files.extend(glob.glob(os.path.join(self.temp_dir, "*.jpg")))
            
            for file_path in temp_files:
                try:
                    os.remove(file_path)
                except:
                    pass
                    
            return len(temp_files)
        except Exception as e:
            print(f"Erro ao limpar arquivos temporários: {e}")
            return 0

class VisionCommandHandler:
    """Manipulador de comandos de visão"""
    
    def __init__(self, api_key=None):
        self.vision = JarvisVision(api_key)
        
    def process_vision_command(self, command):
        """Processa comandos relacionados à visão"""
        command_lower = command.lower()
        
        # Comandos de captura e análise
        if any(phrase in command_lower for phrase in [
            "o que tem na minha tela", "o que você vê", "analise minha tela",
            "o que tem de errado", "erro no código", "problema na tela"
        ]):
            return self._handle_screen_analysis(command)
            
        elif any(phrase in command_lower for phrase in [
            "janela ativa", "nesta janela", "analise janela"
        ]):
            return self._handle_window_analysis(command)
            
        elif "tirar screenshot" in command_lower or "capturar tela" in command_lower:
            return self._handle_screenshot()
            
        return None
        
    def _handle_screen_analysis(self, command):
        """Lida com análise de tela completa"""
        # Extrai a pergunta específica se houver
        question = command
        
        # Adiciona contexto se for sobre código
        if any(word in command_lower for word in ["código", "erro", "bug", "problema"]):
            question = "Analise esta imagem e identifique possíveis erros de código ou problemas. Se houver erros, aponte-os e sugira correções."
            
        return self.vision.capture_and_analyze(question)
        
    def _handle_window_analysis(self, command):
        """Lida com análise de janela ativa"""
        question = "Analise esta janela ativa e descreva o que está acontecendo."
        return self.vision.capture_active_window(question)
        
    def _handle_screenshot(self):
        """Lida com captura de tela simples"""
        image_path, screenshot = self.vision.capture_screen(add_overlay=True)
        
        if image_path:
            # Move para área de trabalho
            import shutil
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            if not os.path.exists(desktop):
                desktop = os.path.expanduser("~")
                
            filename = f"jarvis_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            dest_path = os.path.join(desktop, filename)
            
            shutil.move(image_path, dest_path)
            
            return f"Screenshot salvo na área de trabalho como {filename}"
        else:
            return "Não foi possível capturar a tela."
