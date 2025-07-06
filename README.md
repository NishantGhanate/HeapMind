fastapi dev main.py

uvicorn main:app --reload


Features
- Reliable service event stream


### Create .env file
```
# postgres
DB_USER=postgres
DB_PASS=passowrd
DB_HOST=localhost
DB_PORT=5432
DB_NAME=heap_mind

# Rabbit broker
RABBIT_URL="amqp://guest:guest@localhost/"
```

Create almebic migrations init [if no migrations exists]
> alembic init -t async migrations

Generate migration models
> alembic revision --autogenerate -m "init"

Migrate models
> alembic upgrade head


Run Rabbit-mq docker
```
> docker run -d --hostname rabbit --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
Then access the RabbitMQ dashboard:
URL: http://localhost:15672
User: guest
Pass: guest
```
Run Redis

> docker run -d --name redis -p 6379:6379 redis:7-alpine

Celery worker
> celery -A app.core.celery_app worker --loglevel=info

on windows
> celery -A app.core.celery_app worker --loglevel=info --pool=solo


Celery monitor via flower [pip install flower] [http://localhost:5555]
> celery -A app.core.celery_app flower --broker=amqp://guest:guest@localhost:5672//

Or use docker for flower

> docker run -d -p 5555:5555 \
    --name=flower \
    -e CELERY_BROKER_URL=redis://host.docker.internal:6379/0 \
    mher/flower

TIPS:
- Register your models into migrations/env.py
- Import SQl model into script.py.mako
