import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Carrega as chaves secretas do arquivo .env
load_dotenv()

URL_SUPABASE = os.getenv("SUPABASE_URL")
CHAVE_SUPABASE = os.getenv("SUPABASE_KEY")

try:
    # 2. Estabelece a conexão com a nuvem
    supabase: Client = create_client(URL_SUPABASE, CHAVE_SUPABASE)
    
    # 3. Faz uma requisição de teste para listar os concursos (deve retornar vazio, mas sem erros)
    resposta = supabase.table("concursos_fisica").select("*").execute()
    
    print("✅ Sucesso Absoluto!")
    print("A sua aplicação Python está conectada ao Supabase.")
    print("Dados atuais na tabela de concursos:", resposta.data)

except Exception as e:
    print("❌ Ops! Algo deu errado na conexão:")
    print(e)