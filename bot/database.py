import sqlite3
import json
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_name='retroauto.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Таблица игроков
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                collected_stickers TEXT DEFAULT '[]',
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица сессий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                is_active BOOLEAN DEFAULT FALSE,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_player(self, user_id: int, username: str, first_name: str, last_name: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO players (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        
        conn.commit()
        conn.close()

    def get_player(self, user_id: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM players WHERE user_id = ?', (user_id,))
        player = cursor.fetchone()
        
        conn.close()
        
        if player:
            return {
                'user_id': player[0],
                'username': player[1],
                'first_name': player[2],
                'last_name': player[3],
                'collected_stickers': json.loads(player[4]),
                'registered_at': player[5]
            }
        return None

    def add_sticker_to_player(self, user_id: int, sticker_id: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        player = self.get_player(user_id)
        if player:
            collected_stickers = player['collected_stickers']
            if sticker_id not in collected_stickers:
                collected_stickers.append(sticker_id)
                
                cursor.execute('''
                    UPDATE players 
                    SET collected_stickers = ? 
                    WHERE user_id = ?
                ''', (json.dumps(collected_stickers), user_id))
                
                conn.commit()
        
        conn.close()

    def get_all_players(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM players')
        players = []
        
        for player in cursor.fetchall():
            players.append({
                'user_id': player[0],
                'username': player[1],
                'first_name': player[2],
                'last_name': player[3],
                'collected_stickers': json.loads(player[4]),
                'registered_at': player[5]
            })
        
        conn.close()
        return players

    def start_game_session(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Деактивируем все предыдущие сессии
        cursor.execute('UPDATE game_sessions SET is_active = FALSE')
        
        # Создаем новую активную сессию
        cursor.execute('INSERT INTO game_sessions (is_active) VALUES (TRUE)')
        
        conn.commit()
        conn.close()

    def end_game_session(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE game_sessions SET is_active = FALSE, ended_at = CURRENT_TIMESTAMP')
        
        conn.commit()
        conn.close()

    def is_game_active(self) -> bool:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT is_active FROM game_sessions WHERE is_active = TRUE')
        result = cursor.fetchone()
        
        conn.close()
        return result is not None

# Глобальный экземпляр базы данных
db = Database()
