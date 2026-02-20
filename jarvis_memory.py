#!/usr/bin/env python3
"""
Sistema de Memória Persistente do Jarvis
Armazena e recupera informações importantes sobre o usuário
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import re

class JarvisMemory:
    """Sistema de memória persistente para Jarvis"""
    
    def __init__(self, db_path=None):
        """Inicializa o sistema de memória"""
        if db_path is None:
            db_path = os.path.join(os.getcwd(), 'jarvis_memory.db')
            
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Inicializa o banco de dados SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Cria tabela de memória
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fact TEXT NOT NULL,
                    category TEXT NOT NULL,
                    data TEXT NOT NULL,
                    importance INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    access_count INTEGER DEFAULT 1
                )
            ''')
            
            # Cria tabela de contexto de conversa
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_context (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    jarvis_response TEXT NOT NULL,
                    context_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Cria tabela de preferências do usuário
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    preference_key TEXT UNIQUE NOT NULL,
                    preference_value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Cria índices para performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_memory_category ON memory(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_memory_importance ON memory(importance)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversation_session ON conversation_context(session_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_preferences_key ON user_preferences(preference_key)')
            
            conn.commit()
            conn.close()
            
            print("✅ Banco de dados de memória inicializado")
            
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")
            
    def store_fact(self, fact: str, category: str, importance: int = 1):
        """Armazena um fato importante sobre o usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verifica se o fato já existe
            cursor.execute('''
                SELECT id FROM memory 
                WHERE fact = ? AND category = ?
            ''', (fact, category))
            
            if cursor.fetchone():
                # Atualiza fato existente
                cursor.execute('''
                    UPDATE memory 
                    SET importance = ?, last_accessed = CURRENT_TIMESTAMP, access_count = access_count + 1
                    WHERE fact = ? AND category = ?
                ''', (importance, fact, category))
            else:
                # Insere novo fato
                cursor.execute('''
                    INSERT INTO memory (fact, category, importance)
                    VALUES (?, ?, ?)
                ''', (fact, category, importance))
                
            conn.commit()
            conn.close()
            
            print(f"🧠 Fato armazenado: [{category}] {fact}")
            
        except Exception as e:
            print(f"Erro ao armazenar fato: {e}")
            
    def store_conversation(self, session_id: str, user_input: str, jarvis_response: str, context_data: Dict = None):
        """Armazena contexto da conversa"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            context_json = json.dumps(context_data) if context_data else None
            
            cursor.execute('''
                INSERT INTO conversation_context (session_id, user_input, jarvis_response, context_data)
                VALUES (?, ?, ?, ?)
            ''', (session_id, user_input, jarvis_response, context_json))
                
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Erro ao armazenar conversa: {e}")
            
    def extract_user_info(self, text: str) -> List[Tuple[str, str, int]]:
        """Extrai informações importantes do texto do usuário"""
        facts = []
        
        # Padrões para extração de informações
        patterns = [
            # Nome
            (r'meu nome (?:é|é)\s+([A-Za-zÀ-ÿ\s]+)', 'nome', 3),
            (r'chamo-me\s+([A-Za-zÀ-ÿ\s]+)', 'nome', 3),
            (r'eu sou\s+([A-Za-zÀ-ÿ\s]+)', 'nome', 3),
            
            # Trabalho/projeto
            (r'estou trabalhando (?:no|em)\s+(.+?)(?:\s+projeto)?', 'trabalho', 2),
            (r'meu projeto (?:atual|principal) (?:é|é)\s+(.+)', 'projeto', 2),
            (r'estou desenvolvendo\s+(.+)', 'projeto', 2),
            
            # Preferências
            (r'(?:eu|gosto de|prefiro)\s+(.+)', 'preferencia', 2),
            (r'odeio\s+(.+)', 'preferencia', 2),
            (r'não gosto de\s+(.+)', 'preferencia', 2),
            
            # Informações pessoais
            (r'mor (?:em|na)\s+(.+)', 'localizacao', 2),
            (r'tenho\s+(\d+)\s+anos', 'idade', 2),
            (r'estudo\s+(.+)', 'estudo', 2),
            
            # Contexto técnico
            (r'usando\s+(.+)', 'tecnologia', 2),
            (r'programando (?:em|com)\s+(.+)', 'tecnologia', 2),
            (r'trabalhando com\s+(.+)', 'tecnologia', 2),
            
            # Estado emocional/situação
            (r'estou\s+(.+)', 'estado', 2),
            (r'estou (?:me sentindo|sentindo-me)\s+(.+)', 'estado', 2),
        ]
        
        for pattern, category, importance in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                fact = match if isinstance(match, str) else ' '.join(match)
                facts.append((fact.strip(), category, importance))
                
        return facts
        
    def auto_extract_and_store(self, text: str, session_id: str = None):
        """Extrai e armazena informações automaticamente"""
        facts = self.extract_user_info(text)
        
        for fact, category, importance in facts:
            self.store_fact(fact, category, importance)
            
        return facts
        
    def search_memory(self, query: str, category: str = None, limit: int = 10) -> List[Dict]:
        """Busca informações na memória"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Constrói query de busca
            if category:
                cursor.execute('''
                    SELECT fact, category, importance, created_at, access_count
                    FROM memory 
                    WHERE category = ? AND fact LIKE ?
                    ORDER BY importance DESC, last_accessed DESC
                    LIMIT ?
                ''', (category, f'%{query}%', limit))
            else:
                cursor.execute('''
                    SELECT fact, category, importance, created_at, access_count
                    FROM memory 
                    WHERE fact LIKE ?
                    ORDER BY importance DESC, last_accessed DESC
                    LIMIT ?
                ''', (f'%{query}%', limit))
                
            results = []
            for row in cursor.fetchall():
                results.append({
                    'fact': row[0],
                    'category': row[1],
                    'importance': row[2],
                    'created_at': row[3],
                    'access_count': row[4]
                })
                
            conn.close()
            return results
            
        except Exception as e:
            print(f"❌ Erro ao buscar memória: {e}")
            return []
            
    def get_recent_context(self, session_id: str = None, hours: int = 24) -> List[Dict]:
        """Obtém contexto recente de conversas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            since_date = datetime.now() - timedelta(hours=hours)
            
            if session_id:
                cursor.execute('''
                    SELECT user_input, jarvis_response, context_data, created_at
                    FROM conversation_context 
                    WHERE session_id = ? AND created_at >= ?
                    ORDER BY created_at DESC
                    LIMIT 10
                ''', (session_id, since_date))
            else:
                cursor.execute('''
                    SELECT user_input, jarvis_response, context_data, created_at
                    FROM conversation_context 
                    WHERE created_at >= ?
                    ORDER BY created_at DESC
                    LIMIT 20
                ''', (since_date,))
                
            results = []
            for row in cursor.fetchall():
                context_data = json.loads(row[2]) if row[2] else {}
                results.append({
                    'user_input': row[0],
                    'jarvis_response': row[1],
                    'context_data': context_data,
                    'created_at': row[3]
                })
                
            conn.close()
            return results
            
        except Exception as e:
            print(f"❌ Erro ao obter contexto: {e}")
            return []
            
    def get_user_preferences(self) -> Dict[str, str]:
        """Obtém todas as preferências do usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT preference_key, preference_value FROM user_preferences')
            results = dict(cursor.fetchall())
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"❌ Erro ao obter preferências: {e}")
            return {}
            
    def set_preference(self, key: str, value: str):
        """Define uma preferência do usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_preferences (preference_key, preference_value)
                VALUES (?, ?)
            ''', (key, value))
                
            conn.commit()
            conn.close()
            
            print(f"⚙️ Preferência definida: {key} = {value}")
            
        except Exception as e:
            print(f"❌ Erro ao definir preferência: {e}")
            
    def get_context_for_prompt(self, session_id: str = None) -> str:
        """Gera contexto para incluir no prompt da IA"""
        context_parts = []
        
        # Informações importantes do usuário
        important_facts = self.search_memory("", limit=5)
        if important_facts:
            context_parts.append("INFORMAÇÕES IMPORTANTES DO USUÁRIO:")
            for fact in important_facts:
                context_parts.append(f"- {fact['fact']} ({fact['category']})")
                
        # Contexto recente de conversa
        recent_context = self.get_recent_context(session_id, hours=6)
        if recent_context:
            context_parts.append("\nCONVERSA RECENTE:")
            for conv in recent_context[:3]:  # Últimas 3 interações
                context_parts.append(f"Usuário: {conv['user_input'][:50]}...")
                context_parts.append(f"Jarvis: {conv['jarvis_response'][:50]}...")
                
        # Preferências do usuário
        preferences = self.get_user_preferences()
        if preferences:
            context_parts.append("\nPREFERÊNCIAS DO USUÁRIO:")
            for key, value in preferences.items():
                context_parts.append(f"- {key}: {value}")
                
        return "\n".join(context_parts) if context_parts else ""
        
    def cleanup_old_data(self, days: int = 30):
        """Limpa dados antigos do banco"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Limpa conversas antigas
            cursor.execute('''
                DELETE FROM conversation_context 
                WHERE created_at < ?
            ''', (cutoff_date,))
            
            # Limpa fatos com baixa importância e antigos
            cursor.execute('''
                DELETE FROM memory 
                WHERE importance < 3 AND created_at < ?
            ''', (cutoff_date,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            print(f"🧹 Limpeza concluída: {deleted_count} registros antigos removidos")
            return deleted_count
            
        except Exception as e:
            print(f"❌ Erro na limpeza: {e}")
            return 0
            
    def get_memory_stats(self) -> Dict:
        """Obtém estatísticas da memória"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Total de fatos por categoria
            cursor.execute('''
                SELECT category, COUNT(*) as count
                FROM memory
                GROUP BY category
            ''')
            stats['facts_by_category'] = dict(cursor.fetchall())
            
            # Total de conversas
            cursor.execute('SELECT COUNT(*) as count FROM conversation_context')
            stats['total_conversations'] = cursor.fetchone()[0]
            
            # Preferências salvas
            cursor.execute('SELECT COUNT(*) as count FROM user_preferences')
            stats['total_preferences'] = cursor.fetchone()[0]
            
            conn.close()
            return stats
            
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas: {e}")
            return {}

class MemoryManager:
    """Gerenciador de memória para integração com o Jarvis"""
    
    def __init__(self, db_path=None):
        self.memory = JarvisMemory(db_path)
        
    def process_user_input(self, text: str, session_id: str = None) -> str:
        """Processa entrada do usuário e extrai informações"""
        # Extrai e armazena informações automaticamente
        facts = self.memory.auto_extract_and_store(text, session_id)
        
        if facts:
            fact_list = ", ".join([f"{fact} ({category})" for fact, category, _ in facts])
            return f"🧠 Informações armazenadas: {fact_list}"
        
        return ""
        
    def get_context_for_ai(self, session_id: str = None) -> str:
        """Obtém contexto formatado para a IA"""
        return self.memory.get_context_for_prompt(session_id)
        
    def search_user_info(self, query: str) -> List[Dict]:
        """Busca informações do usuário"""
        return self.memory.search_memory(query)
        
    def set_user_preference(self, key: str, value: str):
        """Define preferência do usuário"""
        self.memory.set_preference(key, value)
        
    def get_user_preference(self, key: str) -> Optional[str]:
        """Obtém preferência específica"""
        preferences = self.memory.get_user_preferences()
        return preferences.get(key)
        
    def store_conversation(self, session_id: str, user_input: str, jarvis_response: str, context: Dict = None):
        """Armazena conversa"""
        self.memory.store_conversation(session_id, user_input, jarvis_response, context)
        
    def cleanup_memory(self, days: int = 30):
        """Limpa memória antiga"""
        return self.memory.cleanup_old_data(days)
        
    def get_stats(self) -> Dict:
        """Obtém estatísticas da memória"""
        return self.memory.get_memory_stats()
