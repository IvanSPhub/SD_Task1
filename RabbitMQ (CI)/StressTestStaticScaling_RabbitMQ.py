import pika
import redis
import time

# Configuración
NUM_MESSAGES = 50000
TEXT_QUEUE = "text_queue"
RESULTS_LIST = "RESULTS"
INSULT = "Tu lógica es tan estúpida que haría llorar a un retrasado"

# Conectar a RabbitMQ
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbit_connection.channel()
channel.queue_declare(queue=TEXT_QUEUE)

# Conectar a Redis y limpiar la lista de resultados
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
redis_client.delete(RESULTS_LIST)

# Enviar mensajes uno a uno desde un solo hilo
print(f"Enviando {NUM_MESSAGES} mensajes a RabbitMQ (cola: {TEXT_QUEUE})...")
start = time.time()

for i in range(NUM_MESSAGES):
    channel.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=INSULT)
    if i % 10000 == 0 or i == NUM_MESSAGES - 1:
        print(f"[{i}] Mensaje enviado")

end_send = time.time()

# Esperar a que todos los mensajes hayan sido procesados por InsultFilter
print("Esperando a que los InsultFilter procesen todos los mensajes...")

while True:
    processed = redis_client.llen(RESULTS_LIST)
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
# Nodos: 1
# Tiempo total de envío: 16.55 segundos
# Tiempo total hasta que todos fueron filtrados: 191.34 segundos
# Tiempo medio por mensaje (envío + filtrado): 0.0038 segundos
# Speedup = T1/TN = 191.34s / 191.34s = 1.00

# ---- RESULTADOS ----
# Número de mensajes: 50000
# Nodos: 2
# Tiempo total de envío: 17.60 segundos
# Tiempo total hasta que todos fueron filtrados: 116.38 segundos
# Tiempo medio por mensaje (envío + filtrado): 0.0023 segundos
# Speedup = T1/TN = 191.34s / 116.38s = 1.64

# ---- RESULTADOS ----
# Número de mensajes: 50000
# Nodos: 3
# Tiempo total de envío: 18.00 segundos
# Tiempo total hasta que todos fueron filtrados: 83.04 segundos
# Tiempo medio por mensaje (envío + filtrado): 0.0017 segundos
# Speedup = T1/TN = 191.34s / 83.04s = 2.30