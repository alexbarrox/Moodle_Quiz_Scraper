# Moodle Quiz Scraper 🎓🕷️

Este é um script em Python desenvolvido para automatizar a extração (scraping) de questões e alternativas de questionários da plataforma Moodle (como o AVA Cenes). 
Ele percorre as páginas de uma tentativa de simulado/prova de forma sequencial, extraindo os enunciados e as opções de resposta de maneira organizada.

## 🚀 Funcionalidades

- **Extração inteligente:** Captura o número da questão, o enunciado completo e todas as alternativas de múltipla escolha.
- **Seletor Robusto:** Utiliza múltiplos fallbacks no BeautifulSoup para garantir a extração das alternativas mesmo em temas customizados do Moodle (varrendo classes como `answer`, `ablock`, `r0`, `r1` e tags `<label>`).
- **Navegação Controlada:** Respeita o servidor do AVA utilizando pequenos intervalos (`time.sleep`) entre as requisições de página.

## 📋 Pré-requisitos

Antes de rodar o projeto, você precisará ter o Python 3 instalado em sua máquina e as seguintes bibliotecas:

```bash
pip install requests beautifulsoup4
