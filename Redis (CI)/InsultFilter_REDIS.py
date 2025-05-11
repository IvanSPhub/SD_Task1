import redis

# Implementa un servicio basado en el patrón de Work Queue.
# Permite que los clientes envíen textos que pueden o no contener insultos.
# Reemplaza los insultos en el texto por la palabra "CENSORED" y guarda el texto filtrado en una lista.
# Puede devolver la lista si se solicita.

# Conectar a Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Nombres de la cola de entrada y de la lista de resultados
queue_name = "text_queue"
filtered_list = "filtered_list"

# Lista de palabras a censurar
insult_words = [
    "gilipollas", "retrasado", "imbécil", "idiotas", "subnormal", "cabrón",
    "capullo", "cretino", "estúpida", "estúpido", "basura"
]

print("InsultFilter en ejecución... Esperando textos para filtrar.")

while True:
    # Esperar bloqueando hasta que llegue un mensaje
    message = client.blpop(queue_name, timeout=0)
    if message:
        text = message[1]
        print(f"Texto recibido: {text}")
        # Censurar insultos
        words = text.split()
        filtered = ["CENSORED" if word.lower() in insult_words else word for word in words]
        result = " ".join(filtered)
        # Guardar el texto filtrado
        client.rpush(filtered_list, result)
        print(f"Texto filtrado y guardado en la lista: {result}")

# Desde la terminal donde ejecutamos "docker exec -it my-redis redis-cli":
# get_filtered_texts() -> LRANGE filtered_list 0 -1
# filter_text()        -> RPUSH filtered_list "Texto limpio y sin insultos"

# Stress test (un solo nodo)
# docker run --name my-redis -d -p 6379:6379 redis
# docker exec -it my-redis redis-cli
# Ejecutar InsultFilter_REDIS.py en otra terminal
# Ejecutar StressTest_REDIS.py en otra terminal

# Stress test (múltiples nodos)
# docker run --name my-redis -d -p 6379:6379 redis
# docker exec -it my-redis redis-cli
# python InsultFilter_REDIS.py
# python InsultFilter_REDIS.py
# python InsultFilter_REDIS.py
# Ejecutar StressTestStaticScaling_REDIS.py en otra terminal
