import pika
import time
from multiprocessing.dummy import Pool as ThreadPool

# Configuración
TEXT_QUEUE = "text_queue"
NUM_MESSAGES = 25000
INSULT = "Tu lógica es tan estúpida que haría llorar a un retrasado"
THREADS = 5         # Número de threads a usar
BATCH_SIZE = 55       # Mensajes por conexión
NUM_BATCHES = NUM_MESSAGES // BATCH_SIZE

# Enviar un lote de mensajes con una sola conexión
def send_batch(batch_id):
    try:
        # time.sleep(1)  # Para ralentizar
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=TEXT_QUEUE)

        for _ in range(BATCH_SIZE):
            channel.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=INSULT)
        
        connection.close()

        if batch_id % 10 == 0:
            print(f"[StressTest] Batch {batch_id} enviado ({BATCH_SIZE} mensajes)")
    except Exception as e:
        print(f"[StressTest] Error en batch {batch_id}: {e}")

# Lanzar el stress test
if __name__ == "__main__":
    print(f"Enviando {NUM_MESSAGES} mensajes a RabbitMQ en {NUM_BATCHES} batches con {THREADS} threads...")
    start = time.time()

    with ThreadPool(THREADS) as pool:
        pool.map(send_batch, range(NUM_BATCHES))

    end = time.time()
    total_time = end - start

    print("---- RESULTADOS DEL ENVÍO ----")
    print(f"Mensajes enviados: {NUM_MESSAGES}")
    print(f"Tiempo total de envío: {total_time:.2f} segundos")
    print(f"Tiempo medio por mensaje: {total_time / NUM_MESSAGES:.4f} segundos")
    print(f"Tasa de llegada estimada (λ): {NUM_MESSAGES / total_time:.2f} msg/s")
