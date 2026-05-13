import requests
import sys
import os
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.database.db_handler import salvar_vagas, init_db

def rastrear_concursos():
    # URL do PCI Concursos 
    url = "https://www.pciconcursos.com.br/concursos/"
    
    try:
        # 1. Conecta ao site
        resposta = requests.get(url)
        # O site  
        resposta.encoding = 'utf-8' 
        
        # 2. Transforma o HTML 
        sopa = BeautifulSoup(resposta.text, 'html.parser')
        
        # 3. No PCI
        concursos = sopa.find_all('div', class_='ca')
        
        print(f"Analisando {len(concursos)} editais encontrados...\n")
        
        vagas_encontradas = []

        for item in concursos:
            texto_vaga = item.get_text().lower()
            
            # 4. Filtros Estratégicos (Suas palavras-chave)
            if "física" in texto_vaga or "médio" in texto_vaga:
                # Extraindo o link e o título
                link = item.find('a')['href'] if item.find('a') else "Link não encontrado"
                titulo = item.find('a').get_text() if item.find('a') else "Sem título"
                
                vagas_encontradas.append({
                    "titulo": titulo,
                    "link": link
                })

        return vagas_encontradas

    except Exception as e:
        print(f" Erro na coleta: {e}")
        return []

# Testando o robô
if __name__ == "__main__":
    init_db()
    resultados = rastrear_concursos()

    if resultados:
        # 3. Salva no banco e recebe quantos são novos
        novos = salvar_vagas(resultados)
        print(f" Processo concluído!")
        print(f"Total analisado: {len(resultados)}")
        print(f" Novos editais salvos: {novos}")
    else:
        print("Poxa, nenhuma vaga relevante encontrada hoje.")