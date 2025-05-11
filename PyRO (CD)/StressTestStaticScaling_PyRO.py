import Pyro4
import time
import multiprocessing

# Nombres de los servicios registrados en el Name Server
SERVER_NAMES = [
    "insult.service.1000",
    "insult.service.1001",
    "insult.service.1002"
]

NUM_REQUESTS = 1000
INSULT = "Tu código es una vergüenza para la humanidad"

# Tarea a ejecutar en paralelo
def send_request(uri):
    try:
        proxy = Pyro4.Proxy(uri)
        return proxy.insult_me()
    except Exception as e:
        return f"ERROR: {e}"

def main():
    print(f"Realizando {NUM_REQUESTS} peticiones en paralelo usando {len(SERVER_NAMES)} servidores con multiprocessing...")
    # Buscar los URIs en el Name Server
    ns = Pyro4.locateNS()
    uris = [ns.lookup(name) for name in SERVER_NAMES]

    # Añadir el insulto a uno de los servidores (solo una vez)
    Pyro4.Proxy(uris[0]).add_insult(INSULT)

    # Crear Round Robin para distribuir las peticiones
    server_uris = [uris[i % len(uris)] for i in range(NUM_REQUESTS)]

    start = time.time()

    with multiprocessing.Pool() as pool:
        results = pool.map(send_request, server_uris)

    end = time.time()
    total_time = end - start

    print("\n---- RESULTADOS ----")
    print(f"Número de peticiones: {NUM_REQUESTS}")
    print(f"Errores: {sum(1 for r in results if 'ERROR' in str(r))}")
    print(f"Servidores usados: {len(SERVER_NAMES)}")
    print(f"Tiempo total: {total_time:.2f} segundos")
    print(f"Tiempo medio por petición: {total_time / NUM_REQUESTS:.4f} segundos")

if __name__ == "__main__":
    main()

# ---- RESULTADOS ----
# Número de peticiones: 1000
# Errores: 0
# Servidores usados: 1
# Tiempo total: 3.38 segundos
# Tiempo medio por petición: 0.0034 segundos
# Speedup = T1/TN = 3.38s / 3.38s = 1.00

# ---- RESULTADOS ----
# Número de peticiones: 1000
# Errores: 0
# Servidores usados: 2
# Tiempo total: 3.31 segundos
# Tiempo medio por petición: 0.0033 segundos
# Speedup = T1/TN = 3.38s / 3.31s = 1.02

# ---- RESULTADOS ----
# Número de peticiones: 1000 
# Errores: 0
# Servidores usados: 3       
# Tiempo total: 3.15 segundos
# Tiempo medio por petición: 0.0032 segundos
# Speedup = T1/TN = 3.38s / 3.15s = 1.07