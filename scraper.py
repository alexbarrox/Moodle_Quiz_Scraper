import time
import requests
from bs4 import BeautifulSoup

# ================= AJUSTE ESSES VALORES =================
# Cole aqui o Cookie completo que você copiou do seu navegador
COOKIE_SESSAO = "MoodleSession=COLE_AQUI_O_SEU_COOKIE_DE_SESSAO"

# Cabeçalho padrão para simular um navegador real
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": COOKIE_SESSAO
}

# URL base (repare que removemos o número final da página para preenchê-lo dinamicamente)
BASE_URL = "[https://ava.cenes.com.br/mod/quiz/attempt.php?attempt=949644&cmid=13945&page=](https://ava.cenes.com.br/mod/quiz/attempt.php?attempt=949644&cmid=13945&page=)"
# ========================================================

def extrair_questoes(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    questoes_da_pagina = []

    # Localiza cada bloco de questão no Moodle
    blocos_questoes = soup.find_all("div", class_="que")

    for bloco in blocos_questoes:
        dados_questao = {}

        # 1. Número da questão (ex: "Questão 1")
        info_bloco = bloco.find("span", class_="qno")
        numero_questao = info_bloco.get_text(strip=True) if info_bloco else "Questão n/a"
        dados_questao["numero"] = numero_questao

        # 2. Enunciado da questão
        enunciado_div = bloco.find("div", class_="qtext")
        if enunciado_div:
            enunciado = " ".join(enunciado_div.get_text(separator="\n", strip=True).split())
            dados_questao["enunciado"] = enunciado
        else:
            dados_questao["enunciado"] = "Não foi possível extrair o enunciado."

        # 3. Extração robusta de alternativas (múltiplas tentativas de classes)
        alternativas = []
        
        # Tentativa A: Procurar na div padrão de respostas do Moodle ("answer" ou "ablock")
        div_respostas = bloco.find("div", class_=lambda x: x and ("answer" in x or "ablock" in x))
        
        if div_respostas:
            # Estratégia 1: Moodle padrão (divs com r0, r1, ou flex-fill dentro da área de respostas)
            opcoes_divs = div_respostas.find_all("div", class_=lambda x: x and any(c in x for c in ["r0", "r1", "flex-fill", "d-flex"]))
            
            # Estratégia 2: Se não achou divs específicas, procura diretamente pelas tags <label>
            if not opcoes_divs:
                opcoes_divs = div_respostas.find_all("label")
                
            for opcao in opcoes_divs:
                texto_opcao = opcao.get_text(separator=" ", strip=True)
                if texto_opcao and texto_opcao not in alternativas:
                    alternativas.append(texto_opcao)
                    
        # Tentativa B de segurança: Se a div de respostas não foi encontrada, busca qualquer <label>
        if not alternativas:
            labels_fallback = bloco.find_all("label")
            for label in labels_fallback:
                texto_opcao = label.get_text(separator=" ", strip=True)
                if texto_opcao and texto_opcao not in alternativas:
                    alternativas.append(texto_opcao)

        dados_questao["alternativas"] = alternativas
        questoes_da_pagina.append(dados_questao)

    return questoes_da_pagina

def main():
    todas_as_questoes = []

    # Loop para percorrer as páginas (de 0 a 9)
    for pagina in range(0, 10):
        url = f"{BASE_URL}{pagina}"
        print(f"Acessando: {url} ...")

        try:
            resposta = requests.get(url, headers=HEADERS)

            # Se retornar 403 ou redirecionar para login, o cookie expirou ou está incorreto
            if "login" in resposta.url or resposta.status_code != 200:
                print(f"❌ Erro de autenticação na página {pagina}. Verifique se o seu cookie ainda é válido.")
                break

            questoes = extrair_questoes(resposta.text)

            if not questoes:
                print(f"⚠️ Nenhuma questão encontrada na página {pagina}. Verifique a estrutura da página.")
            else:
                print(f"✅ Sucesso! {len(questoes)} questão(ões) extraída(s).")
                todas_as_questoes.extend(questoes)

        except Exception as e:
            print(f"💥 Erro ao processar a página {pagina}: {e}")

        # Pausa amigável de 1.5 segundos para não sobrecarregar o servidor do AVA
        time.sleep(1.5)

    # --- EXIBIÇÃO DOS RESULTADOS ---
    print("\n" + "="*50)
    print(f"🏆 SCRAPING CONCLUÍDO. TOTAL DE QUESTÕES EXTRAÍDAS: {len(todas_as_questoes)}")
    print("="*50 + "\n")

    for q in todas_as_questoes:
        print(f"=== {q['numero']} ===")
        print(f"Enunciado: {q['enunciado']}")
        print("Opções:")
        for alt in q["alternativas"]:
            print(f"  - {alt}")
        print("-" * 50)

if __name__ == "__main__":
    main()