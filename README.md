# [FastAPI do zero](https://fastapidozero.dunossauro.com/)

Projeto do curso de FastAPI do [Eduardo Mendes @dunossauro](https://github.com/dunossauro/fastapi-do-zero) do canal [Live de Python](https://www.youtube.com/@Dunossauro).

 
## Descrição do Projeto

Etapas de criação de uma API REST utilizando o FastAPI.  
Será feito a implementação e publicação do projeto final.  
O objetivo é aplicar todos os conceitos aprendidos ao longo do curso para desenvolver uma API completa e funcional utilizando FastAPI.

## Este projeto está usando:

#### Dependências de Projeto:
- Python 3.11 ou superior **(recomendação do autor)**
- [Fastapi 0.111.0](https://pypi.org/project/fastapi/) (Web Framework para construir API's)

#### Dependências de Desenvolvimento:
- [Poetry 1.8.3](https://python-poetry.org/) (Gerenciador de pacotes do Python)
- [Taskipy 1.13.0](https://pypi.org/project/taskipy/) (Um task runner para linhas de comandos Python)
- [Ruff 0.4.9](https://pypi.org/project/taskipy/) (Um task runner para linhas de comandos Python)
- [Pytest 8.2.2](https://pypi.org/project/pytest/) (Um  Framework para criar testes unitários.)
- [Pytest-Cov 5.0.0](https://pypi.org/project/pytest-cov/) (Um plugin para produzir relatórios de cobertura de testes unitários)

#### Opcional Dependência de Desenvolvimento:
- [ignr 2.2](https://pypi.org/project/ignr/) (Plugin para gerar um arquivo .gitignore baseado na linguagem que voce definir.)

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/devfabiopedro/fastapi_zero.git
cd fastapi_zero
```

2. Crie um ambiente virtual com o Poetry:

```bash
poetry shell
```

3. Instale as dependências do projeto:

```bash
poetry install
```

## Uso
Iniciar o servidor ou executar tarefas com Taskipy

```
abra o seu arquivo pyproject.toml
```
copie e cole estas chaves no seu arquivo **pyproject.toml**

```
[tool.ruff]
line-length = 79
extend-exclude = ['migrations']

[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']

[tool.ruff.format]
preview = true
quote-style = 'single'

[tool.pytest.ini_options]
pythonpath = "."
addopts = '-p no:warnings'

[tool.taskipy.tasks]
run = 'fastapi dev fastapi_zero/app.py'
lint = 'ruff check . && ruff check . --diff'
format = 'ruff check . --fix && ruff format .'
pre_test = 'task lint'
test = 'pytest -s -x --cov=fastapi_zero -vv'
post_test = 'coverage html'
```
Estas chaves deve ficar **acima** da chave abaixo:
```
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Salve as alterações do seu arquivo **pyproject.toml**

A partir do seu prompt de comandos ou console de comandos do seu editor você pode executar o comando:
- **task --list** (Lista todos os comandos que você criou)
- **task run** (Executa o projeto)
- **task lint** (O Ruff faz a checagem de Lint e exibe os erros)     
- **task format** (O Ruff faz a formatação do seu documento adequadamente)
- **task pre_test** (Faz uma verificação de sintaxe)
- **task test** (Executa os testes unitários escritos com pytest)
- **task post_test** (Gera o arquivo coverage html e exibe no navegador a sua cobertura de testes)