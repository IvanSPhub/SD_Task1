import redis
import multiprocessing
import time
import os
import math
import requests
import pika
import matplotlib.pyplot as plt

# Configuración
# Nombre de la cola en RabbitMQ desde donde los workers consumen mensajes
TEXT_QUEUE = "text_queue"
# Lista en Redis donde se guardan los textos filtrados
RESULTS_LIST = "RESULTS"

# Número máximo de workers
MAX_WORKERS = 40
# Tiempo de respuesta deseado para procesar un mensaje (en segundos)
TARGET_RESPONSE_TIME = 1.0
# Capacidad estimada de cada worker (mensajes que puede procesar por segundo)
CAPACITY_PER_WORKER = 250

# Cada cuántos ciclos imprimir el log aunque no haya cambios (evita spam)
UNCHANGED_LIMIT = 100

# Función para obtener el backlog real desde RabbitMQ vía HTTP API
def get_rabbitmq_backlog():
    try:
        url = "http://localhost:15672/api/queues/%2F/text_queue"
        auth = ("guest", "guest")  # Usuario y contraseña por defecto
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            data = response.json()
            return data["messages"]  # backlog real
        else:
            print(f"[Autoscaler] Error HTTP {response.status_code} al consultar RabbitMQ")
            return 0
    except Exception as e:
        print(f"[Autoscaler] Error al conectar con RabbitMQ API: {e}")
        return 0

# Función que representa un "InsultFilter". Se ejecuta como un proceso independiente (multiprocessing)
def insult_filter_worker():
    # Lista de insultos a censurar
    insults = [
        "gilipollas", "retrasado", "imbécil", "idiotas", "subnormal", "cabrón",
        "capullo", "cretino", "estúpida", "estúpido", "basura"
    ]

    # Conexión a Redis para guardar los resultados filtrados
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    # Conectarse a RabbitMQ y declarar la cola
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=TEXT_QUEUE)

    # Callback que se ejecuta cada vez que llega un mensaje a la cola (función de filtrado)
    def callback(ch, method, properties, body):
        text = body.decode()
        # Censurar insultos
        words = text.split()
        filtered = ["CENSORED" if word.lower() in insults else word for word in words]
        result = " ".join(filtered)
        # Guardar resultado en Redis
        redis_client.rpush(RESULTS_LIST, result)
        # Confirmar recepción del mensaje
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Prefetch = 1 para que cada worker procese un mensaje a la vez (ideal en work queues)
    channel.basic_qos(prefetch_count=1)
    # Iniciar el consumo de mensajes
    channel.basic_consume(queue=TEXT_QUEUE, on_message_callback=callback)
    # print(f"[Worker {os.getpid()}] Iniciado y escuchando mensajes...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass # Permitir cerrar con Ctrl+C

# Autoscaler principal
if __name__ == "__main__":
    # Conectarse a Redis para obtener info de la cola (backlog)
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    # Lista de procesos (workers) activos
    workers = []
    current_workers = len(workers)
    previous_backlog = 0
    previous_time = time.time()
    previous_log = ""
    unchanged_count = 0
    # Datos para la gráfica
    tiempos = []
    backlogs = []
    n_workers = []
    start_time = time.time()

    print("[Autoscaler] Supervisando la carga... (Ctrl+C para detener)")

    try:
        while True:
            # Leer el tamaño actual de la cola de RabbitMQ
            current_backlog = get_rabbitmq_backlog()
            # Estimar la tasa de llegada (mensajes/segundo)
            current_time = time.time()
            delta_backlog = current_backlog - previous_backlog
            delta_time = current_time - previous_time
            if delta_time < 0.5:
                delta_time = 1.0
            arrival_rate = delta_backlog / delta_time if delta_time > 0 else 0.1
            arrival_rate = max(arrival_rate, 0.1)  # Evitar valores negativos o 0 (así hay 1 worker mínimo)
            # Fórmula escalado dinámico basado en la cola de espera (backlog)
            # N = ceil((B + (λ * Tr)) / C)
            required_workers = min(MAX_WORKERS, math.ceil((current_backlog + arrival_rate * TARGET_RESPONSE_TIME) / CAPACITY_PER_WORKER))

            # LOG de métricas internas
            log = (
                f"\n[Autoscaler] Estado actual:\n"
                f"  ▸ Mensajes en cola (backlog actual): {current_backlog}\n"
                f"  ▸ Tasa de llegada estimada (λ): {arrival_rate:.2f} msg/s\n"
                f"  ▸ Workers requeridos (N): {required_workers}\n"
                f"  ▸ Workers activos: {current_workers}"
            )

            if log != previous_log or unchanged_count >= UNCHANGED_LIMIT:
                print(log)
                previous_log = log
                unchanged_count = 0
            else:
                unchanged_count += 1

            # Escalado
            # Si se necesitan más workers que los actuales → lanzar nuevos
            if required_workers > current_workers:
                for _ in range(required_workers - current_workers):
                    p = multiprocessing.Process(target=insult_filter_worker)
                    p.start()
                    workers.append(p)
                    # print(f"[Autoscaler] + Lanzado nuevo worker (Total: {len(workers)})")
            # Si sobran workers → eliminarlos
            elif required_workers < current_workers:
                for _ in range(current_workers - required_workers):
                    p = workers.pop()
                    p.terminate()
                    # print(f"[Autoscaler] - Finalizado un worker (Total: {len(workers)})")
            
            # Ajustar el número de workers
            current_workers = len(workers)
            
            # Registro de métricas para la gráfica
            tiempos.append(current_time - start_time)
            backlogs.append(current_backlog)
            n_workers.append(current_workers)
            
            previous_backlog = current_backlog
            previous_time = current_time

    except KeyboardInterrupt:
        print("\n[Autoscaler] Deteniendo todos los workers...")
        for p in workers:
            p.terminate()
        for p in workers:
            p.join()
        print("[Autoscaler] Finalizado.")
    
    # Generar la gráfica
    try:
        fig, ax1 = plt.subplots(figsize=(12, 6))

        ax1.set_xlabel("Tiempo (s)")
        ax1.set_ylabel("Número de mensajes", color="blue")
        ax1.plot(tiempos, backlogs, label="Backlog", color="blue")
        ax1.tick_params(axis='y', labelcolor="blue")

        ax2 = ax1.twinx()
        ax2.set_ylabel("Workers activos", color="red")
        ax2.plot(tiempos, n_workers, label="Workers activos", color="red")
        ax2.tick_params(axis='y', labelcolor="red")

        fig.tight_layout()
        fig.legend(loc="upper right")
        plt.grid(True)
        plt.savefig("escalado_dinamico.png")
        print("\n[Autoscaler] Gráfica guardada como 'escalado_dinamico.png'")
        plt.show()

    except Exception as e:
        print(f"[Autoscaler] Error al generar la gráfica: {e}")

# Stress test dinámico (múltiples nodos)
# docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
# docker run --name redis -d -p 6379:6379 redis
# python DynamicScaling_RabbitMQ.py
# Ejecutar StressTestDynamicScaling_RabbitMQ.py en otra terminal
# Abre tu navegador y ve a: http://localhost:15672 guest guest