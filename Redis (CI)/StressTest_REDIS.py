import redis
import time

# Configuración de Redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)
queue_name = "text_queue"
filtered_list = "filtered_list"

# Texto ofensivo de prueba
insult = "Tu lógica es tan estúpida que haría llorar a un retrasado"

# Número de peticiones a realizar
NUM_MESSAGES = 1000

# Limpiar resultados previos
client.delete(filtered_list)

print("Iniciando stress test en Redis (InsultFilter)...")

start_time = time.time()

# Enviar mensajes a la cola
for i in range(NUM_MESSAGES):
    client.rpush(queue_name, insult)
    if i % 10 == 0 or i == NUM_MESSAGES - 1:
        print(f"[{i}] Mensaje enviado")

# Esperar procesamiento
print("Esperando a que InsultFilter procese todos los mensajes...")
while True:
    processed = client.llen(filtered_list)
    if processed >= NUM_MESSAGES:
        break
    time.sleep(0.1)

end_time = time.time()

# Resultados
total_time = end_time - start_time
print("\n---- RESULTADOS ----")
print(f"Mensajes enviados: {NUM_MESSAGES}")
print(f"Mensajes procesados: {client.llen(filtered_list)}")
print(f"Tiempo total: {total_time:.2f} segundos")
print(f"Tiempo medio por mensaje: {total_time / NUM_MESSAGES:.4f} segundos")

# ---- RESULTADOS ----
# Mensajes enviados: 1000
# Mensajes procesados: 1000
# Tiempo total: 4.35 segundos
# Tiempo medio por mensaje: 0.0043 segundos