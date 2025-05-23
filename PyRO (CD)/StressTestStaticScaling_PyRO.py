import Pyro4
import time
from multiprocessing import Pool, cpu_count

SERVER_NAMES = [
    "insult.service.1000",
    #"insult.service.1001",
    #"insult.service.1002"
]

NUM_REQUESTS = 50000

# Variables globales
uris = []
proxies = []

# Se ejecuta una vez por proceso al iniciar el pool
def init_worker(server_uris):
    global proxies
    proxies = [Pyro4.Proxy(uri) for uri in server_uris]

# Función que hace una petición a uno de los proxies
def send_request(i):
    global proxies
    try:
        proxy = proxies[i % len(proxies)]
        return proxy.insult_me()
    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    print(f"Realizando {NUM_REQUESTS} peticiones en paralelo usando {len(SERVER_NAMES)} servidores...")

    # Obtener URIs una vez
    ns = Pyro4.locateNS()
    uris = [ns.lookup(name) for name in SERVER_NAMES]

    # Añadir tres insultos a Redis (cualquiera de los servidores lo hará, ya que todos comparten Redis)
    Pyro4.Proxy(uris[0]).add_insult("Tu código es una vergüenza para la humanidad")
    Pyro4.Proxy(uris[0]).add_insult("Eres un cretino con teclado")
    Pyro4.Proxy(uris[0]).add_insult("Solo un cabrón sin alma escribiría esa basura de función")

    time.sleep(6)

    start = time.time()

    # Número de procesos
    num_proc = min(cpu_count(), len(uris) * 4)

    with Pool(processes=num_proc, initializer=init_worker, initargs=(uris,)) as pool:
        results = pool.map(send_request, range(NUM_REQUESTS))

    end = time.time()
    total_time = end - start

    errores = sum(1 for r in results if isinstance(r, str) and r.startswith("ERROR"))

    print("\n---- RESULTADOS ----")
    print(f"Número de peticiones: {NUM_REQUESTS}")
    print(f"Errores: {errores}")
    print(f"Servidores usados: {len(SERVER_NAMES)}")
    print(f"Tiempo total: {total_time:.2f} segundos")
    print(f"Tiempo medio por petición: {total_time / NUM_REQUESTS:.4f} segundos")

# ---- RESULTADOS ----
# Número de peticiones: 50000
# Errores: 0
# Servidores usados: 1
# Tiempo total: 10.99 segundos
# Tiempo medio por petición: 0.0002 segundos
# Speedup = T1/TN = 10.99s / 10.99s = 1.00

# ---- RESULTADOS ----
# Número de peticiones: 50000
# Errores: 0
# Servidores usados: 2
# Tiempo total: 7.04 segundos
# Tiempo medio por petición: 0.0001 segundos
# Speedup = T1/TN = 10.99s / 7.04s = 1.56

# ---- RESULTADOS ----
# Número de peticiones: 50000
# Errores: 0
# Servidores usados: 3
# Tiempo total: 6.42 segundos
# Tiempo medio por petición: 0.0001 segundos
# Speedup = T1/TN = 10.99s / 6.42s = 1.71