import pika
import time
import redis

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# Conexión a Redis para comprobar resultados
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Declarar las colas necesarias
channel.queue_declare(queue='insult_queue')  # Cola para InsultService
channel.queue_declare(queue='text_queue')    # Cola para InsultFilter
# Nombres de listas en Redis
INSULTS_LIST = "INSULTS"
RESULTS_LIST = "RESULTS"

# Lista de insultos para enviar
insults = [
    "Hablas más tonterías que un gilipollas con WiFi",
    "Tu lógica es tan estúpida que haría llorar a un retrasado",
    "Solo un imbécil como tú podría romper un 'Hello World'",
    "Eres tan capullo que los bugs huyen de tu código por vergüenza ajena",
    "Programas como un subnormal con las manos atadas",
    "Qué estúpido hay que ser para escribir eso y no borrarlo al instante",
    "Solo un cabrón sin alma escribiría esa basura de función",
    "Eres un cretino con teclado",
]

print("InsultClient enviando textos...")

# Enviar insultos a ambas colas cada 5 segundos
for insult in insults:
    # Enviar a insult_queue (InsultConsumer lo recibirá)
    channel.basic_publish(exchange='', routing_key='insult_queue', body=insult)
    print(f"Enviando texto a InsultConsumer (insult_queue): {insult}")
    # Enviar también a text_queue (InsultFilter lo procesará)
    channel.basic_publish(exchange='', routing_key='text_queue', body=insult)
    print(f"Enviando texto a InsultFilter (text_queue): {insult}")
    time.sleep(3)
# Recuperar y mostrar resultados desde Redis
time.sleep(3)
insults_stored = redis_client.lrange(INSULTS_LIST, 0, -1)
filtered_results = redis_client.lrange(RESULTS_LIST, 0, -1)
# Mostrar listas guardadas en Redis
print("\nInsultos almacenados por InsultConsumer (INSULTS):")
for i, insult in enumerate(insults_stored, 1):
    print(f"{i}. {insult}")

print("\nTextos filtrados almacenados por InsultFilter (RESULTS):")
for i, filtered in enumerate(filtered_results, 1):
    print(f"{i}. {filtered}")

# Cerrar conexión de RabbitMQ
connection.close()
