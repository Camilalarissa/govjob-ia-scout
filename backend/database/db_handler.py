import sqlite3
import os

#  caminho  para o banco de dados 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "concursos.db")

def init_db():
    """Inicializa o banco de dados e cria a tabela se não existir."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS editais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            resumo_ia TEXT,
            data_coleta DATETIME DEFAULT CURRENT_TIMESTAMP,
            lido INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def salvar_vagas(vagas):
    """Salva novas vagas no banco, ignorando links duplicados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    novas_vagas = 0
    
    for vaga in vagas:
        try:
            # O 'OR IGNORE' garante que links já existentes não gerem erro nem duplicatas
            cursor.execute('''
                INSERT OR IGNORE INTO editais (titulo, link) 
                VALUES (?, ?)
            ''', (vaga['titulo'], vaga['link']))
            
            # Verifica se uma nova linha foi realmente inserida
            if cursor.rowcount > 0:
                novas_vagas += 1
        except Exception as e:
            print(f"Erro ao salvar vaga: {e}")
            
    conn.commit()
    conn.close()
    return novas_vagas

if __name__ == "__main__":
    init_db()
    print(f"Banco de dados inicializado em: {DB_PATH}")