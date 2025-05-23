import pika
import redis
import time

# Conexiones
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbit_connection.channel()
channel.queue_declare(queue='text_queue')

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
RESULTS_LIST = "RESULTS"

# Limpiar resultados anteriores
redis_client.delete(RESULTS_LIST)

# Mensaje ofensivo para filtrar
message = "Tu lógica es tan estúpida que haría llorar a un retrasado"

NUM_MESSAGES = 50000
print(f"Enviando {NUM_MESSAGES} mensajes a text_queue...")

start = time.time()

# Enviar mensajes a la cola
for i in range(NUM_MESSAGES):
    channel.basic_publish(exchange='', routing_key='text_queue', body=message)
    if i % 10000 == 0 or i == NUM_MESSAGES - 1:
        print(f"[{i}] Mensaje enviado")
end_send = time.time()

# Esperar a que Redis tenga todos los resultados
print("Esperando a que InsultFilter procese todos los mensajes...")
while True:
    processed = redis_client.llen(RESULTS_LIST)
    if processed >= NUM_MESSAGES:
        break
    time.sleep(0.1)

end = time.time()

print("\n---- RESULTADOS ----")
print(f"Mensajes enviados: {NUM_MESSAGES}")
print(f"Tiempo total de envío: {end_send - start:.2f} segundos")
print(f"Tiempo total hasta que todos fueron filtrados: {end - start:.2f} segundos")
print(f"Tiempo medio por mensaje (envío + filtrado): {(end - start)/NUM_MESSAGES:.4f} segundos")

# ---- RESULTADOS ----
# Mensajes enviados: 50000
# Tiempo total de envío: 16.40 segundos
# Tiempo total hasta que todos fueron filtrados: 194.84 segundos
# Tiempo medio por mensaje (envío + filtrado): 0.0039 segundos