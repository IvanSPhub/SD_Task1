import redis

# SubscriberService/InsultReciever
# Conectar a Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Nombre del canal al que se suscribe
insult_channel = "insult_channel"

# Crear el objeto pubsub y suscribirse al canal
pubsub = client.pubsub()
pubsub.subscribe(insult_channel)

print(f"SubscriberService suscrito al canal '{insult_channel}'. Esperando insultos...")

# Escuchar mensajes de manera continua
for message in pubsub.listen():
    if message["type"] == "message":
        insult = message["data"]
        print(f"Insulto recibido del broadcaster: {insult}")
