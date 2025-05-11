import redis
import time
from multiprocessing import Pool

# Configuración
NUM_REQUESTS = 1000
NUM_WORKERS = 3  # Cambiar a 1, 2 o 3 para probar distintos nodos
QUEUE_NAME = "text_queue"
FILTERED_LIST = "filtered_list"

# Texto ofensivo de prueba
insult = "Tu lógica es tan estúpida que haría llorar a un retrasado"

# Enviar texto a Redis
def send_text(i):
    client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    client.rpush(QUEUE_NAME, insult)

# Main stress test
if __name__ == "__main__":
    # Limpiar lista de resultados antes de empezar
    client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    client.delete(FILTERED_LIST)

    print(f"Lanzando {NUM_REQUESTS} peticiones con {NUM_WORKERS} workers...")
    start = time.time()

    with Pool(processes=NUM_WORKERS) as pool:
        pool.map(send_text, range(NUM_REQUESTS))

    # Esperar a que se procesen todos
    print("Esperando a que InsultFilter procese todos los mensajes...")
    while True:
        if client.llen(FILTERED_LIST) >= NUM_REQUESTS:
            break
        time.sleep(0.1)

    end = time.time()
    total_time = end - start

    # Resultados
    print("---- RESULTADOS ----")
    print(f"Número de peticiones: {NUM_REQUESTS}")
    print(f"Workers (nodos): {NUM_WORKERS}")
    print(f"Tiempo total: {total_time:.2f} segundos")
    print(f"Tiempo medio por petición: {total_time / NUM_REQUESTS:.4f} segundos")

# ---- RESULTADOS ----
# Número de peticiones: 1000
# Workers (nodos): 1
# Tiempo total: 10.45 segundos
# Tiempo medio por petición: 0.0105 segundos
# Speedup = T1/TN = 10.45s / 10.45s = 1.00

# ---- RESULTADOS ----
# Número de peticiones: 1000
# Workers (nodos): 2
# Tiempo total: 7.74 segundos
# Tiempo medio por petición: 0.0077 segundos
# Speedup = T1/TN = 10.45s / 7.74s = 1.35

# ---- RESULTADOS ----      
# Número de peticiones: 1000
# Workers (nodos): 3
# Tiempo total: 7.55 segundos
# Tiempo medio por petición: 0.0075 segundos
# Speedup = T1/TN = 10.45s / 7.55s = 1.38