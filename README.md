<img src="https://i.imgur.com/4tuAMcX.png" alt="FastAPI Logo">

# [FastAPI do zero](https://fastapidozero.dunossauro.com/) com @Dunossauro

Projeto do curso de FastAPI do [Eduardo Mendes @dunossauro](https://github.com/dunossauro/fastapi-do-zero) do canal [Live de Python](https://www.youtube.com/@Dunossauro).


## 📘 Descrição do Projeto

Etapas de criação de uma API REST utilizando o FastAPI.  
Será feito a implementação e publicação do projeto final.  
O objetivo é aplicar todos os conceitos aprendidos ao longo do curso para desenvolver uma API completa e funcional utilizando FastAPI.

## 🚀 Este projeto está usando:

#### Dependências de Projeto:
- Python 3.11 ou superior **(recomendação do autor)**
- [Fastapi 0.111.0](https://pypi.org/project/fastapi/) (Web Framework de alto desempenho para construir API's)

#### Dependências de Desenvolvimento:
- [Poetry 1.8.3](https://python-poetry.org/) (Gerenciador de pacotes do Python)
- [Taskipy 1.13.0](https://pypi.org/project/taskipy/) (Executor de tarefas para projetos python)
- [Ruff 0.4.9](https://pypi.org/project/ruff/) (Um linter Python e formatador de código extremamente rápido, escrito em Rust.)
- [Pytest 8.2.2](https://pypi.org/project/pytest/) (Criar testes simples e poderosos com Python)
- [Pytest-Cov 5.0.0](https://pypi.org/project/pytest-cov/) (Um plugin para produzir relatórios de cobertura de testes)
- [Factory-boy 3.3.0](https://pypi.org/project/factory-boy/) (Uma biblioteca que permite criar objetos de modelo de teste de forma rápida e fácil.)
- [Freezegun 1.5.1](https://pypi.org/project/freezegun/) (Um biblioteca que permite "congelar" o tempo em um ponto específico ou avançá-lo conforme necessário durante os testes)


#### ⚠️ Opcional Dependência de Desenvolvimento:
- [ignr 2.2](https://pypi.org/project/ignr/) (Plugin para gerar um arquivo .gitignore baseado na linguagem que voce definir.)

## 🖥️ Instalação

1. Clone o repositório 🔗:

```bash
git clone https://github.com/devfabiopedro/fastapi_zero.git
cd fastapi_zero
```

2. Crie um ambiente virtual com o Poetry 🏡:

```bash
poetry shell
```

3. Instale as dependências do projeto 💾:

```bash
poetry install
```

## 🛠️ Uso
A partir do seu prompt de comando ou terminal você pode executar o comando:
#### **task --list** (Lista todos os comandos)  
- **task run** (Inicia o servidor local Uvicorn e executa o projeto)
- **task lint** (O Ruff faz a checagem de Lint e exibe os erros)
- **task format** (O Ruff faz a formatação do seu documento adequadamente)
- **task test** (Executa os testes unitários escritos com Pytest)
- **task post-test** (Gera o arquivo coverage html e exibe no navegador a sua cobertura de testes)