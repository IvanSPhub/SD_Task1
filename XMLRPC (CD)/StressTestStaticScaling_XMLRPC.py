import xmlrpc.client
import time
from multiprocessing import Pool, cpu_count

# Lista de servidores disponibles (cada uno ejecutando un SimpleXMLRPCServer en un puerto distinto)
servers = [
    "http://127.0.0.1:8000",
    #"http://127.0.0.1:8001",
    #"http://127.0.0.1:8002"
]

NUM_REQUESTS = 50000  # Número total de peticiones a repartir entre servidores

# Añadir tres insultos a Redis (cualquiera de los servidores lo hará, ya que todos comparten Redis)
xmlrpc.client.ServerProxy(servers[0]).add_insult("Tu código es una vergüenza para la humanidad")
xmlrpc.client.ServerProxy(servers[0]).add_insult("Eres un cretino con teclado")
xmlrpc.client.ServerProxy(servers[0]).add_insult("Solo un cabrón sin alma escribiría esa basura de función")

time.sleep(5)

# Este diccionario se usa para guardar conexiones persistentes a cada servidor
proxies = {}

# Esta función se ejecuta una vez por proceso
def init_worker():
    global proxies
    # Creamos un proxy persistente a cada servidor (uno por URL)
    proxies = {url: xmlrpc.client.ServerProxy(url) for url in servers}

# Esta es la función que hace cada petición (se ejecutará 50.000 veces en paralelo)
def make_request(i):
    try:
        # Selecciona el servidor correspondiente según el índice (Round Robin)
        index = i % len(servers)
        url = servers[index]
        # Usa el proxy para enviar la petición
        return proxies[url].insult_me()
    except Exception as e:
        return None

# Punto de entrada principal
if __name__ == "__main__":
    print(f"Realizando {NUM_REQUESTS} peticiones usando {len(servers)} servidores...")

    start = time.time()
    # Crea un Pool de procesos con una cantidad proporcional a CPUs y servidores
    with Pool(processes=min(cpu_count(), len(servers) * 4), initializer=init_worker) as pool:
        # Ejecuta todas las peticiones en paralelo
        results = pool.map(make_request, range(NUM_REQUESTS))
    end = time.time()

    errores = results.count(None)  # Cuenta las respuestas fallidas

    print("\n---- RESULTADOS ----")
    print(f"Número de peticiones: {NUM_REQUESTS}")
    print(f"Errores: {errores}")
    print(f"Servidores usados: {len(servers)}")
    print(f"Tiempo total: {end - start:.2f} segundos")
    print(f"Tiempo medio por petición: {(end - start) / NUM_REQUESTS:.4f} segundos")

# ---- RESULTADOS ----
# Número de peticiones: 50000
# Errores: 0
# Servidores usados: 1
# Tiempo total: 35.57 segundos
# Tiempo medio por petición: 0.0007 segundos
# Speedup = T1/TN = 35.57s / 35.57s = 1.00

# ---- RESULTADOS ----
# Número de peticiones: 50000
# Errores: 0
# Servidores usados: 2
# Tiempo total: 24.32 segundos
# Tiempo medio por petición: 0.0005 segundos
# Speedup = T1/TN = 35.57s / 24.32s = 1.46

# ---- RESULTADOS ----
# Número de peticiones: 50000 
# Errores: 0
# Servidores usados: 3        
# Tiempo total: 21.56 segundos
# Tiempo medio por petición: 0.0004 segundos
# Speedup = T1/TN = 35.57s / 21.56s = 1.65