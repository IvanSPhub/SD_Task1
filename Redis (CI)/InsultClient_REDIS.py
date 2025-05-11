import redis
import time

# Cliente/Producer que envía insultos
# Conectar a Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Colas donde enviar los textos
insult_queue = "insult_queue"
text_queue = "text_queue"
# Nombres de listas en Redis
insult_list = "insult_list"
filtered_list = "filtered_list"

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

for insult in insults:
    # Enviar texto a la cola insult_queue (InsultService)
    client.rpush(insult_queue, insult)
    print(f"Enviando texto a InsultConsumer (insult_queue): {insult}")
    # Enviar texto a la cola text_queue (InsultFilter)
    client.rpush(text_queue, insult)
    print(f"Enviando texto a InsultFilter (text_queue): {insult}")
    time.sleep(3)
# Obtener resultados desde Redis
time.sleep(3)
insult_list_contents = client.lrange(insult_list, 0, -1)
filtered_list_contents = client.lrange(filtered_list, 0, -1)

# Mostrar listas guardadas en Redis
print("\nInsultos almacenados en insult_list:")
for i, insult in enumerate(insult_list_contents, 1):
    print(f"{i}. {insult}")

print("\nTextos filtrados en filtered_texts:")
for i, text in enumerate(filtered_list_contents, 1):
    print(f"{i}. {text}")
