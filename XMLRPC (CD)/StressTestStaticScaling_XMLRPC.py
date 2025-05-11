import xmlrpc.client
import time
from multiprocessing import Pool, cpu_count

# Lista de servidores (puertos distintos)
servers = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002"
]

# Crear proxies para cada servidor
proxies = [xmlrpc.client.ServerProxy(url) for url in servers]

# Número de peticiones totales
NUM_REQUESTS = 1000
errores = 0

# Añadir un insulto para que los servidores lo compartan vía Redis
proxies[0].add_insult("Tu código es una vergüenza para la humanidad")

# Función para hacer la petición a uno de los servidores
def make_request(i):
    # Elegir servidor por Round Robin
    index = i % len(servers)
    try:
        proxy = xmlrpc.client.ServerProxy(servers[index])
        return proxy.insult_me()
    except Exception as e:
        return None

# Ejecutar las peticiones en paralelo
if __name__ == "__main__":
    print(f"Realizando {NUM_REQUESTS} peticiones en paralelo usando {len(proxies)} servidores con multiprocessing...")

    start = time.time()
    with Pool(processes=min(cpu_count(), len(servers) * 2)) as pool:
        results = pool.map(make_request, range(NUM_REQUESTS))
    end = time.time()

    # Resultados
    errores = results.count(None)
    print("---- RESULTADOS ----")
    print(f"Número de peticiones: {NUM_REQUESTS}")
    print(f"Errores: {errores}")
    print(f"Servidores usados: {len(servers)}")
    print(f"Tiempo total: {end - start:.2f} segundos")
    print(f"Tiempo medio por petición: {(end - start) / NUM_REQUESTS:.4f} segundos")

# ---- RESULTADOS ----
# Número de peticiones: 1000
# Errores: 0
# Servidores usados: 1
# Tiempo total: 1023.98 segundos
# Tiempo medio por petición: 1.0240 segundos
# Speedup = T1/TN = 1023.98s / 1023.98s = 1.00

# ---- RESULTADOS ----
# Número de peticiones: 1000
# Errores: 0
# Servidores usados: 2
# Tiempo total: 518.03 segundos
# Tiempo medio por petición: 0.5180 segundos
# Speedup = T1/TN = 1023.98s / 518.03s = 1.98

# ---- RESULTADOS ----
# Número de peticiones: 1000
# Errores: 0
# Servidores usados: 3
# Tiempo total: 346.21 segundos
# Tiempo medio por petición: 0.3462 segundos
# Speedup = T1/TN = 1023.98s / 346.21s = 2.96