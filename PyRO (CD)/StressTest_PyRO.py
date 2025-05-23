import Pyro4
import time

# Localizar el Name Server y obtener el proxy
ns = Pyro4.locateNS()
uri = ns.lookup("insult.service")
proxy = Pyro4.Proxy(uri)

# Añadimos un insulto
proxy.add_insult("Tu código es una vergüenza para la humanidad")

# Configurar número de peticiones
NUM_REQUESTS = 50000
errores = 0

start = time.time()

for i in range(NUM_REQUESTS):
    try:
        # Pedimos un insulto aleatorio
        result = proxy.insult_me()
        if i % 10000 == 0 or i == NUM_REQUESTS - 1:
            print(f"[{i}] -> Insulto aleatorio recibido: {result}")
    except Exception as e:
        errores += 1
        print(f"Error en petición {i}: {e}")

end = time.time()
total_time = end - start

# Resultados
print("\n---- RESULTADOS ----")
print(f"Número de peticiones: {NUM_REQUESTS}")
print(f"Errores: {errores}")
print(f"Tiempo total: {total_time:.2f} segundos")
print(f"Tiempo medio por petición: {total_time / NUM_REQUESTS:.4f} segundos")

# ---- RESULTADOS ----
# Número de peticiones: 50000
# Errores: 0
# Tiempo total: 18.12 segundos
# Tiempo medio por petición: 0.0004 segundos