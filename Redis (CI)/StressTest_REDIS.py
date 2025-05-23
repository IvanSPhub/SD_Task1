import redis
import time

# Configuración de Redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)
queue_name = "text_queue"
filtered_list = "filtered_list"

# Texto ofensivo de prueba
insult = "Tu lógica es tan estúpida que haría llorar a un retrasado"

# Número total de mensajes y tamaño del lote
NUM_MESSAGES = 50000
BATCH_SIZE = 1000

# Limpiar resultados previos
client.delete(filtered_list)

print("Iniciando stress test en Redis (InsultFilter - 1 nodo)...")

start_time = time.time()

# Enviar mensajes a la cola usando pipeline
for i in range(0, NUM_MESSAGES, BATCH_SIZE):
    pipe = client.pipeline()
    for j in range(BATCH_SIZE):
        if i + j >= NUM_MESSAGES:
            break
        pipe.rpush(queue_name, insult)
    pipe.execute()
    print(f"[{i + BATCH_SIZE}] mensajes enviados")

end_send = time.time()

# Esperar a que InsultFilter procese todos los mensajes
print("Esperando a que InsultFilter procese todos los mensajes...")
while True:
    processed = client.llen(filtered_list)
    if processed >= NUM_MESSAGES:
        break
    time.sleep(0.1)

end_time = time.time()

# Resultados
print("\n---- RESULTADOS ----")
print(f"Mensajes enviados: {NUM_MESSAGES}")
print(f"Tiempo total de envío: {end_send - start_time:.2f} segundos")
print(f"Tiempo total hasta que todos fueron filtrados: {end_time - start_time:.2f} segundos")
print(f"Tiempo medio por mensaje (envío + filtrado): {(end_time - start_time)/NUM_MESSAGES:.4f} segundos")

# ---- RESULTADOS ----
# Mensajes enviados: 50000
# Tiempo total de envío: 1.76 segundos
# Tiempo total hasta que todos fueron filtrados: 162.88 segundos
# Tiempo medio por mensaje (envío + filtrado): 0.0033 segundos