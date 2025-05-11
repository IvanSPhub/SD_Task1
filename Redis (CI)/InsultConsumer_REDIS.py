import redis

# Saca insultos de la cola y los guarda en insult_list
# add_insult() y get_insults()
# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

queue_name = "insult_queue"
insult_list = "insult_list"

print("InsultConsumer esperando a recibir insultos...")

while True:
    # Extrae un insulto de la cola (espera hasta que haya uno)
    insult = client.blpop(queue_name, timeout=0)
    if insult:
        insult_text = insult[1]
        # Verificar si ya existe en la lista para evitar duplicados
        existing = client.lrange(insult_list, 0, -1)
        if insult_text not in existing:
            client.rpush(insult_list, insult_text) # Almacena el insulto en la lista
            print(f"Insulto guardado en la lista: {insult_text}")
        else:
            print(f"Insulto duplicado ignorado: {insult_text}")

# Ejecutar en la terminal:
# docker run --name my-redis -d -p 6379:6379 redis
# docker exec -it my-redis redis-cli
# Ejecutar InsultConsumer_REDIS.py en otra terminal (2. extrae los textos de la cola y los almacena en insult_list)
# Ejecutar InsultBroadcaster_REDIS.py en otra terminal (3. difunde los textos de insult_list por insult_channel)
# Ejecutar SubscriberService_REDIS.py en otra terminal (4. recibe los textos difundidos una vez suscrito)
# Ejecutar InsultFilter_REDIS.py en otra terminal (2. extrae los textos de la cola, los filtra y los almacena en filtered_list)
# Ejecutar InsultClient_REDIS.py en otra terminal (1. envía textos a insult_queue y text_queue)

# Desde la terminal donde ejecutamos "docker exec -it my-redis redis-cli":
# get_insults() -> LRANGE insult_list 0 -1
# add_insult()  -> RPUSH insult_list "Insulto nuevo desde la terminal"

