import xmlrpc.client
import time

# Conexión al servicio
proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:8000")
# Añadimos un texto
proxy.add_insult("Tu código es una vergüenza para la humanidad")

# Número de peticiones
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

print("\n---- RESULTADOS ----")
print(f"Número de peticiones: {NUM_REQUESTS}")
print(f"Errores: {errores}")
print(f"Tiempo total: {total_time:.2f} segundos")
print(f"Tiempo medio por petición: {total_time / NUM_REQUESTS:.4f} segundos")

# ---- RESULTADOS ----
# Número de peticiones: 50000
# Errores: 0
# Tiempo total: 56.00 segundos
# Tiempo medio por petición: 0.0011 segundos