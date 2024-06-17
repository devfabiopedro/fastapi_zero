from fastapi import FastAPI

app = FastAPI(title='FastAPI do Zero')


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/page1')
def page1():
    return {'message': 'Lendo Página 1'}