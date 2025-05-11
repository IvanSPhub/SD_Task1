import pika
import redis

# Implementa un servicio basado en el patrón de Work Queue.
# Permite que los clientes envíen textos que pueden o no contener insultos.
# Reemplaza los insultos en el texto por la palabra "CENSORED" y guarda el texto filtrado en una lista.
# Puede devolver la lista si se solicita.

# Conexión a RabbitMQ
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbit_connection.channel()

# Declarar la cola de trabajo
channel.queue_declare(queue='text_queue')

# Conexión a Redis para guardar los resultados filtrados
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
RESULTS_LIST = "RESULTS"

# Lista de insultos a censurar
insults = [
    "gilipollas", "retrasado", "imbécil", "idiotas", "subnormal", "cabrón",
    "capullo", "cretino", "estúpida", "estúpido", "basura"
]

print("InsultFilter esperando textos que filtrar...")

# Función de filtrado
def callback(ch, method, properties, body):
    text = body.decode()
    print(f"Texto recibido: {text}")
    # Censurar insultos
    words = text.split()
    filtered = ["CENSORED" if word.lower() in insults else word for word in words]
    result = " ".join(filtered)
    # Guardar resultado en Redis
    redis_client.rpush(RESULTS_LIST, result)
    print(f"Texto filtrado y guardado: {result}")
    # Confirmar recepción del mensaje
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Configurar la cola para reparto de trabajo
channel.basic_qos(prefetch_count=1)
# Escuchar la cola de textos
channel.basic_consume(queue='text_queue', on_message_callback=callback)

channel.start_consuming()

# Desde la terminal donde ejecutamos "docker exec -it my-redis redis-cli":
# get_filtered_texts() -> LRANGE RESULTS 0 -1
# filter_text()        -> RPUSH RESULTS "Texto limpio y sin insultos"

# Stress test (un solo nodo)
# docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
# docker run --name redis -d -p 6379:6379 redis
# Ejecutar InsultFilter_RabbitMQ.py en otra terminal
# Ejecutar StressTest_RabbitMQ.py en otra terminal

# Stress test (múltiples nodos)
# docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
# docker run --name redis -d -p 6379:6379 redis
# python InsultFilter_RabbitMQ.py
# python InsultFilter_RabbitMQ.py
# python InsultFilter_RabbitMQ.py
# Ejecutar StressTestStaticScaling_RabbitMQ.py en otra terminal