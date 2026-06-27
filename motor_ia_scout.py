import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client, Client
from google import genai

# 1. Carregar Variáveis
load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analisar_com_ia(texto_edital):
    """Usa o Gemini para ler o conteúdo interno do edital e procurar Física."""
    prompt = f"""
    Analise o texto deste edital de concurso público. 
    1. Verifique se o concurso tem vagas explícitas para a área de "Física" (Professor de Física, Licenciatura em Física, Bacharelado em Física).
    2. Identifique o Órgão (ex: Prefeitura de X, Secretaria Y).
    3. Identifique o Salário máximo ou oferecido.
    
    Retorne rigorosamente APENAS um JSON válido, sem formatação markdown, com esta estrutura:
    {{"confirmado_fisica": true ou false, "orgao": "Nome", "salario": "Valor ou Não informado"}}
    
    Texto do edital:
    {texto_edital}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        resultado_limpo = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(resultado_limpo)
    except Exception as e:
        return {"confirmado_fisica": False, "orgao": "Desconhecido", "salario": "Não informado"}

def rastrear_e_salvar():
    url = "https://www.pciconcursos.com.br/concursos/"
    print("🔍 A iniciar o rastreio profundo no PCI Concursos...")
    
    try:
        resposta = requests.get(url)
        resposta.encoding = 'utf-8'
        sopa = BeautifulSoup(resposta.text, 'html.parser')
        concursos = sopa.find_all('div', class_='ca')
        
        print(f"Encontrados {len(concursos)} editais na capa. A filtrar oportunidades na educação...\n")
        
        vagas_salvas = 0
        
        for item in concursos:
            resumo_vaga = item.get_text().lower()
            
            # Pré-filtro: Procura qualquer coisa relacionada a ensino para investigar a fundo
            if "professor" in resumo_vaga or "educação" in resumo_vaga or "física" in resumo_vaga or "docente" in resumo_vaga:
                link_tag = item.find('a')
                if not link_tag:
                    continue
                    
                link = link_tag['href']
                titulo = link_tag.get_text()
                
                # Validação no Supabase para não ler o mesmo edital duas vezes
                busca = supabase.table("concursos_fisica").select("id").eq("link_edital", link).execute()
                if len(busca.data) > 0:
                    continue
                
                print(f"📖 A entrar no link do edital: {titulo[:50]}...")
                
                # --- O CLIQUE VIRTUAL ---
                try:
                    resp_edital = requests.get(link, timeout=10)
                    resp_edital.encoding = 'utf-8'
                    sopa_edital = BeautifulSoup(resp_edital.text, 'html.parser')
                    
                    # Extraímos os primeiros 8000 caracteres para não ultrapassar o limite da IA
                    texto_interno = sopa_edital.get_text()[:8000] 
                    
                    print(f"🤖 IA a escanear as vagas e requisitos...")
                    dados_ia = analisar_com_ia(texto_interno)
                    
                    if dados_ia.get("confirmado_fisica"):
                        novo_concurso = {
                            "titulo": titulo,
                            "orgao": dados_ia.get("orgao", titulo),
                            "salario": str(dados_ia.get("salario", "Não informado")),
                            "link_edital": link
                        }
                        
                        supabase.table("concursos_fisica").insert(novo_concurso).execute()
                        print(f"✅ VAGA DE FÍSICA GUARDADA! Órgão: {novo_concurso['orgao']}\n")
                        vagas_salvas += 1
                    else:
                        print("❌ Nenhuma vaga de Física encontrada. Descartado.\n")
                        
                except Exception as erro_link:
                    print(f"⚠️ Não foi possível abrir o link: {erro_link}\n")

        print(f"\n🎉 Rastreio finalizado! {vagas_salvas} novas vagas exclusivas adicionadas à base.")

    except Exception as e:
        print(f"❌ Erro crítico: {e}")

if __name__ == "__main__":
    rastrear_e_salvar()