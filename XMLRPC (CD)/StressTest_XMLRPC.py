import xmlrpc.client
import time

# Conexión al servicio
proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
proxy.add_insult("Tu código es una vergüenza para la humanidad")

# Número de peticiones
NUM_REQUESTS = 1000
errores = 0

start = time.time()

for i in range(NUM_REQUESTS):
    try:
        result = proxy.insult_me()
        if i % 10 == 0 or i == NUM_REQUESTS - 1:
            print(f"[{i}] -> {result}")
    except Exception as e:
        errores += 1
        print(f"Error en petición {i}: {e}")

end = time.time()
total_time = end - start

print("\n---- RESULTADOS ----")
print(f"Número de peticiones: {NUM_REQUESTS}")
print(f"Errores: {errores}")
print(f"Tiempo total: {total_time:.2f} segundos")
print(f"Tiempo medio por petición: {total_time / NUM_REQUESTS:.4f} segundos")

# ---- RESULTADOS ----
# Número de peticiones: 1000    
# Errores: 0
# Tiempo total: 2038.45 segundos
# Tiempo medio por petición: 2.0384 segundos