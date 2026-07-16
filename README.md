# Moodle Quiz Scraper 🎓🕷️

Este é um script em Python desenvolvido para automatizar a extração (scraping) de questões e alternativas de questionários da plataforma Moodle (como o AVA Cenes). 
Ele percorre as páginas de uma tentativa de simulado/prova de forma sequencial, extraindo os enunciados e as opções de resposta de maneira organizada.

## 🚀 Funcionalidades

- **Extração inteligente:** Captura o número da questão, o enunciado completo e todas as alternativas de múltipla escolha.
- **Seletor Robusto:** Utiliza múltiplos fallbacks no BeautifulSoup para garantir a extração das alternativas mesmo em temas customizados do Moodle (varrendo classes como `answer`, `ablock`, `r0`, `r1` e tags `<label>`).
- **Navegação Controlada:** Respeita o servidor do AVA utilizando pequenos intervalos (`time.sleep`) entre as requisições de página.

## 📋 Pré-requisitos

Antes de rodar o projeto, você precisará ter o Python 3 instalado em sua máquina e as seguintes bibliotecas:

## ⚙️ Como Configurar e Executar
Como as tentativas de questionários ficam atrás de uma área logada, o script precisa simular a sua sessão ativa para conseguir ler as páginas.

1. Capturando o seu Cookie de Sessão (MoodleSession)
Abra o navegador, faça login no seu AVA e acesse a página do questionário.

Pressione F12 (ou clique com o botão direito e selecione Inspecionar) para abrir as Ferramentas de Desenvolvedor.

Vá até a aba Rede (Network).

Atualize a página (F5).

Clique na primeira requisição que aparecer na lista (geralmente com o nome attempt.php?...).

No painel de detalhes à direita, clique na aba Cabeçalhos (Headers) e procure pela seção Cabeçalhos de Requisição (Request Headers).

Copie o valor inteiro do campo Cookie (você precisará especificamente do parâmetro MoodleSession=XXXXXXXX...).

## 2. Configurando o Código
Abra o arquivo do script e altere as variáveis de configuração no topo do arquivo:

Python
# Cole o cookie completo extraído do seu navegador
COOKIE_SESSAO = "MoodleSession=COLE_AQUI_O_SEU_COOKIE_DE_SESSAO"

# Ajuste a URL base mantendo a estrutura até o parâmetro "&page="
BASE_URL = "[https://ava.cenes.com.br/mod/quiz/attempt.php?attempt=949644&cmid=13945&page=](https://ava.cenes.com.br/mod/quiz/attempt.php?attempt=949644&cmid=13945&page=)"

## 3. Executando o Script
Com as dependências instaladas e as configurações feitas, basta rodar o script no terminal:

Bash
python scraper.py
O script irá varrer as páginas configuradas (por padrão, de 0 a 9), exibindo o progresso no terminal e imprimindo as questões formatadas ao final.

## 🛠️ Tecnologias Utilizadas
Python - Linguagem base.

Requests - Para realizar as requisições HTTP simulando o navegador.

BeautifulSoup4 - Para realizar o parsing e a extração dos dados do HTML do Moodle.

## ⚠️ Aviso Legal (Disclaimer)
Este projeto foi desenvolvido estritamente para fins de estudo acadêmico, facilitação de revisões pessoais e automação de rotinas de estudo. Use-o com responsabilidade e respeito aos termos de uso da sua instituição de ensino.

Desenvolvido por Alexander Barros ☕


```bash
pip install requests beautifulsoup4


