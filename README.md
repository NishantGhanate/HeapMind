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


TIPS:
- Register your models into migrations/env.py
- Import SQl model into script.py.mako
