from google import genai
import os
import sqlite3
from dotenv import load_dotenv

# 1. Carrega a chave
load_dotenv()
CHAVE_API = os.getenv("GEMINI_API_KEY")

# 2. Configura o novo Cliente 
client = genai.Client(api_key=CHAVE_API)

def obter_concursos_nao_lidos():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "database", "concursos.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, link FROM editais WHERE lido = 0 LIMIT 5")
    vagas = cursor.fetchall()
    conn.close()
    return vagas

def processar_resumos():
    vagas = obter_concursos_nao_lidos()
    
    if not vagas:
        print("✅ Tudo atualizado!")
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "database", "concursos.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for id_vaga, titulo, link in vagas:
        print(f"🤖 IA analisando: {titulo}...")
        
        prompt = f"Resuma as datas e requisitos deste concurso em 3 tópicos curtos: {titulo} - {link}"
        
        try:
            # Gemini 2.5 Flash 
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            
            resumo = response.text
            
            cursor.execute("UPDATE editais SET resumo_ia = ?, lido = 1 WHERE id = ?", (resumo, id_vaga))
            conn.commit()
            print("✨ Resumo salvo com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro: {e}")

    conn.close()

if __name__ == "__main__":
    processar_resumos()