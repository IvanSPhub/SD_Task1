import redis
import time

# Configuración
NUM_MESSAGES = 50000
QUEUE_NAME = "text_queue"
FILTERED_LIST = "filtered_list"
INSULT = "Tu lógica es tan estúpida que haría llorar a un retrasado"
BATCH_SIZE = 1000  # Número de mensajes por lote

# Conexión a Redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Limpiar resultados anteriores
client.delete(FILTERED_LIST)

print(f"Enviando {NUM_MESSAGES} mensajes a Redis en lotes de {BATCH_SIZE}...")

start = time.time()

# Enviar mensajes en lotes usando pipeline
for i in range(0, NUM_MESSAGES, BATCH_SIZE):
    pipe = client.pipeline()
    for j in range(BATCH_SIZE):
        if i + j >= NUM_MESSAGES:
            break
        pipe.rpush(QUEUE_NAME, INSULT)
    pipe.execute()
    print(f"[{i + BATCH_SIZE}] mensajes enviados")

end_send = time.time()

# Esperar a que se procesen todos los mensajes
print("Esperando a que InsultFilter procese todos los mensajes...")
while True:
    processed = client.llen(FILTERED_LIST)
    if processed >= NUM_MESSAGES:
        break
    time.sleep(0.1)

end_total = time.time()

# Mostrar resultados
print("\n---- RESULTADOS ----")
print(f"Número de mensajes: {NUM_MESSAGES}")
print(f"Tiempo total de envío: {end_send - start:.2f} segundos")
print(f"Tiempo total hasta que todos fueron filtrados: {end_total - start:.2f} segundos")
print(f"Tiempo medio por mensaje (envío + filtrado): {(end_total - start) / NUM_MESSAGES:.4f} segundos")

# ---- RESULTADOS ----
# Número de mensajes: 50000
# Workers (nodos): 2
# Tiempo total de envío: 1.42 segundos
# Tiempo total hasta que todos fueron filtrados: 164.23 segundos
# Tiempo medio por mensaje (envío + filtrado): 0.0033 segundos
# Speedup = T1/TN = 164.23s / 164.23s = 1.00

# ---- RESULTADOS ----
# Número de mensajes: 50000
# Workers (nodos): 2
# Tiempo total de envío: 1.65 segundos
# Tiempo total hasta que todos fueron filtrados: 94.19 segundos
# Tiempo medio por mensaje (envío + filtrado): 0.0019 segundos
# Speedup = T1/TN = 164.23s / 94.19s = 1.74

# ---- RESULTADOS ----
# Número de mensajes: 50000
# Workers (nodos): 3
# Tiempo total de envío: 2.01 segundos
# Tiempo total hasta que todos fueron filtrados: 71.15 segundos
# Tiempo medio por mensaje (envío + filtrado): 0.0014 segundos
# Speedup = T1/TN = 164.23s / 71.15s = 2.31