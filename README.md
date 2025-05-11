0. Funcionamiento de los scripts de demostración
- XMLRPC:
    Ejecutar InsultService_XMLRPC.py en una terminal
    Ejecutar InsultFilter_XMLRPC.py en otra terminal
    Ejecutar SubscriberService_XMLRPC.py en otra terminal
    Ejecutar InsultClient_XMLRPC.py en otra terminal
- PyRO:
    Ejecutar este comando en una terminal: 
     python -m Pyro4.naming
    Ejecutar InsultService_PyRO.py en una otra terminal
    Ejecutar InsultFilter_PyRO.py en otra terminal
    Ejecutar SubscriberService_PyRO.py en otra terminal
    Ejecutar InsultClient_PyRO.py en otra terminal
- Redis:
    Ejecutar estos comandos en una terminal:
     docker run --name my-redis -d -p 6379:6379 redis
     docker exec -it my-redis redis-cli
    Ejecutar InsultConsumer_REDIS.py en otra terminal
    Ejecutar InsultBroadcaster_REDIS.py en otra terminal
    Ejecutar SubscriberService_REDIS.py en otra terminal
    Ejecutar InsultFilter_REDIS.py en otra terminal
    Ejecutar InsultClient_REDIS.py en otra terminal
- RabbitMQ:
    Ejecutar estos comandos en una terminal:
     docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
     docker run --name redis -d -p 6379:6379 redis
    Ejecutar InsultConsumer_RabbitMQ.py en otra terminal
    Ejecutar InsultBroadcaster_RabbitMQ.py en otra terminal
    Ejecutar InsultReciever_RabbitMQ.py en otra terminal
    Ejecutar InsultFilter_RabbitMQ.py en otra terminal
    Ejecutar InsultClient_RabbitMQ.py en otra terminal

1. Análisis de rendimiento en un solo nodo
- XMLRPC:
    Ejecutar InsultService_XMLRPC.py en una terminal
    Ejecutar StressTest_XMLRPC.py en otra terminal
- PyRO:
    Ejecutar este comando en una terminal: 
     python -m Pyro4.naming
    Ejecutar InsultService_PyRO.py en otra terminal
    Ejecutar StressTest_PyRO.py en otra terminal
- Redis:
    Ejecutar estos comandos en una terminal:
     docker run --name my-redis -d -p 6379:6379 redis
     docker exec -it my-redis redis-cli
    Ejecutar InsultFilter_REDIS.py en otra terminal
    Ejecutar StressTest_REDIS.py en otra terminal
- RabbitMQ:
    Ejecutar estos comandos en una terminal:
     docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
     docker run --name redis -d -p 6379:6379 redis
    Ejecutar InsultFilter_RabbitMQ.py en otra terminal
    Ejecutar StressTest_RabbitMQ.py en otra terminal

2. Análisis de escalado estático con múltiples nodos
- XMLRPC:
    Ejecutar estos comandos en una terminal:
     docker run --name my-redis -d -p 6379:6379 redis
     docker exec -it my-redis redis-cli
    Ejecutar en otra terminal: python InsultServiceStaticScaling_XMLRPC.py 8000
    Ejecutar en otra terminal: python InsultServiceStaticScaling_XMLRPC.py 8001
    Ejecutar en otra terminal: python InsultServiceStaticScaling_XMLRPC.py 8002
    Ejecutar en otra terminal: python StressTestStaticScaling_XMLRPC.py
- PyRO:
    Ejecutar este comando en una terminal: 
     python -m Pyro4.naming
    Ejecutar estos comandos en otra terminal:
     docker run --name my-redis -d -p 6379:6379 redis
     docker exec -it my-redis redis-cli
    Ejecutar en otra terminal: python InsultServiceStaticScaling_PyRO.py insult.service.1000
    Ejecutar en otra terminal: python InsultServiceStaticScaling_PyRO.py insult.service.1001
    Ejecutar en otra terminal: python InsultServiceStaticScaling_PyRO.py insult.service.1002
- Redis:
    Ejecutar estos comandos en una terminal:
     docker run --name my-redis -d -p 6379:6379 redis
     docker exec -it my-redis redis-cli
    Ejecutar en otra terminal: python InsultFilter_REDIS.py
    Ejecutar en otra terminal: python InsultFilter_REDIS.py
    Ejecutar en otra terminal: python InsultFilter_REDIS.py
    Ejecutar StressTestStaticScaling_REDIS.py en otra terminal
- RabbitMQ:
    Ejecutar estos comandos en una terminal:
     docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
     docker run --name redis -d -p 6379:6379 redis
    Ejecutar en otra terminal: python InsultFilter_RabbitMQ.py
    Ejecutar en otra terminal: python InsultFilter_RabbitMQ.py
    Ejecutar en otra terminal: python InsultFilter_RabbitMQ.py
    Ejecutar StressTestStaticScaling_RabbitMQ.py en otra terminal

3. Análisis de escalado dinámico con múltiples nodos
- RabbitMQ:
    Ejecutar estos comandos en una terminal:
     docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
     docker run --name redis -d -p 6379:6379 redis
    Ejecutar DynamicScaling_RabbitMQ.py en otra terminal
    Ejecutar StressTestDynamicScaling_RabbitMQ.py en otra terminal