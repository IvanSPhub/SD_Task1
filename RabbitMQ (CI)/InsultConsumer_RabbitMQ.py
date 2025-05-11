import pika
import redis

# Saca insultos de la cola y los guarda en insult_list
# add_insult() y get_insults()
# Conexión a RabbitMQ
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbit_connection.channel()
channel.queue_declare(queue='insult_queue')  # Asegura que la cola existe

# Conexión a Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
INSULTS_LIST = "INSULTS"  # Lista en Redis donde se guardan los insultos

print("InsultConsumer esperando a recibir insultos...")

# Función que maneja cada mensaje recibido
def callback(ch, method, properties, body):
    # Convertimos el cuerpo del mensaje (bytes) a string
    insult = body.decode()
    # Obtenemos todos los insultos almacenados actualmente en Redis
    stored_insults = redis_client.lrange(INSULTS_LIST, 0, -1)

    if insult not in stored_insults:
        # Si el insulto no está en Redis, lo agregamos al final de la lista
        redis_client.rpush(INSULTS_LIST, insult)
        print(f"Insulto nuevo agregado a Redis: {insult}")
    else:
        print(f"Insulto duplicado ignorado: {insult}")
    # Confirmamos a RabbitMQ que ya procesamos este mensaje,
    # así puede eliminarlo de la cola (importante para evitar reprocesos)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Configura cómo se distribuyen los mensajes si hay varios consumidores escuchando
# Esto limita el número de mensajes no confirmados a 1 por consumidor
channel.basic_qos(prefetch_count=1)  # ¡¡Equilibrar carga si hay múltiples consumidores!!
# Cada vez que llega un mensaje a la cola 'insult_queue', se llama a 'callback'
channel.basic_consume(queue='insult_queue', on_message_callback=callback)
# Inicia el bucle de escucha permanente
channel.start_consuming()


# Ejecutar en la terminal:
# docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
# docker run --name redis -d -p 6379:6379 redis
# Ejecutar InsultConsumer.py en otra terminal (2. extrae los textos de la cola y los almacena en insult_list)
# Ejecutar InsultBroadcaster.py en otra terminal (3. difunde los textos de insult_list por insult_channel)
# Ejecutar InsultReciever.py en otra terminal (4. recibe los textos difundidos una vez suscrito)
# Ejecutar InsultFilter.py en otra terminal (2. extrae los textos de la cola, los filtra y los almacena en filtered_list)
# Ejecutar InsultClient.py en otra terminal (1. envía textos a insult_queue y text_queue)
# Abre tu navegador y ve a: http://localhost:15672 guest guest

# Desde la terminal donde ejecutamos "docker run --name redis -d -p 6379:6379 redis":
# get_insults() -> LRANGE INSULTS 0 -1
# add_insult()  -> RPUSH INSULTS "Insulto nuevo desde la terminal"
