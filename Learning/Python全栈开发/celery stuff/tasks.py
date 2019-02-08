from celery import Celery

app = Celery('tasks',
             broker='redis://127.0.0.1',
             backend='redis://127.0.0.1')

@app.task
def add(x, y):
    return x + y