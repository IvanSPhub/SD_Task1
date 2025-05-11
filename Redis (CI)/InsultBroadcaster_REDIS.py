import redis
import time
import random

# Publica insultos en insult_channel cada 5 segundos 
# insult_broadcaster()
# Conectar con Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Lista donde están almacenados los insultos
insult_list = "insult_list"
# Nombre del canal de publicación al que se suscriben los receptores (subscribers)
insult_channel = "insult_channel"

print("InsultBroadcaster en ejecución...")

while True:
    # Obtener todos los insultos guardados en la lista
    stored_insults = client.lrange(insult_list, 0, -1)
    
    if stored_insults:
        # Elegir un insulto aleatorio de la lista
        insult = random.choice(stored_insults)
        # Publicar ese insulto en el canal (modo pub/sub)
        client.publish(insult_channel, insult)
        print(f"Difundiendo insulto por insult_channel: {insult}")
    else:
        print("No hay insultos que difundir.")
        time.sleep(5)
    
    time.sleep(5)
