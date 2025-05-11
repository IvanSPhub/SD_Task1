import pika
import redis
import time
import random

# Conexión a RabbitMQ
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbit_connection.channel()
# Declarar un exchange tipo fanout para difusión
channel.exchange_declare(exchange='insult_exchange', exchange_type='fanout')
# Conexión a Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
INSULTS_LIST = "INSULTS"

print("InsultBroadcaster en ejecución...")
while True:
    # Obtenemos todos los insultos almacenados en Redis
    stored_insults = redis_client.lrange(INSULTS_LIST, 0, -1)

    if stored_insults:
        # Elegimos un insulto aleatorio para difundir
        insult = random.choice(stored_insults)
        # Publicamos el insulto en el exchange tipo 'fanout' (envía a TODOS los queues vinculados)
        channel.basic_publish(exchange='insult_exchange', routing_key='', body=insult)
        print(f"Difundiendo insulto: {insult}")
    else:
        print("No hay insultos en Redis para difundir.")
        time.sleep(5)

    time.sleep(5)
