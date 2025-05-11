import pika
import redis
import time
from multiprocessing import Pool, cpu_count

# Configuración
NUM_MESSAGES = 1000
TEXT_QUEUE = "text_queue"
RESULTS_LIST = "RESULTS"

# Texto ofensivo de prueba
insult = "Tu lógica es tan estúpida que haría llorar a un retrasado"

# Enviar un mensaje a RabbitMQ
def send_message(index):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=TEXT_QUEUE)

    # Enviar el insulto en cada mensaje
    channel.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=insult)
    connection.close()

# Lanzar el test
if __name__ == "__main__":
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    redis_client.delete(RESULTS_LIST)  # Limpiar resultados anteriores

    print(f"Enviando {NUM_MESSAGES} mensajes a RabbitMQ...")

    start = time.time()
    with Pool(processes=min(cpu_count(), NUM_MESSAGES)) as pool:
        pool.map(send_message, range(NUM_MESSAGES))

    # Esperar a que se procesen todos los mensajes
    print("Esperando a que los InsultFilter procesen todos los mensajes...")
    while True:
        processed = redis_client.llen(RESULTS_LIST)
        if processed >= NUM_MESSAGES:
            break
        time.sleep(0.1)

    end = time.time()
    total_time = end - start

    # Resultados
    print("---- RESULTADOS ----")
    print(f"Número de mensajes: {NUM_MESSAGES}")
    print(f"Tiempo total: {total_time:.2f} segundos")
    print(f"Tiempo medio por mensaje: {total_time / NUM_MESSAGES:.4f} segundos")

# ---- RESULTADOS ----
# Número de mensajes: 1000
# Nodos: 1
# Tiempo total: 21.91 segundos
# Tiempo medio por mensaje: 0.0219 segundos
# Speedup = T1/TN = 21.91s / 21.91s = 1.00

# ---- RESULTADOS ----
# Número de mensajes: 1000
# Nodos: 2
# Tiempo total: 20.62 segundos
# Tiempo medio por mensaje: 0.0206 segundos
# Speedup = T1/TN = 21.91s / 20.62s = 1.06

# ---- RESULTADOS ----
# Número de mensajes: 1000
# Nodos: 3
# Tiempo total: 20.12 segundos
# Tiempo medio por mensaje: 0.0201 segundos
# Speedup = T1/TN = 21.91s / 20.12s = 1.09