import xmlrpc.client
import time

# InsultClient envía nuevos insultos a InsultService cada 5 segundos.

# Conectamos con InsultService
insult_service = xmlrpc.client.ServerProxy("http://127.0.0.1:8000")
insult_filter = xmlrpc.client.ServerProxy("http://127.0.0.1:8001")
# Registramos al cliente como suscriptor en InsultService
print("INSULTCLIENT -> Registrando suscriptor en InsultService...")
print(insult_service.add_subscriber("http://127.0.0.1:8002"))

# Lista de insultos para agregar
insults_to_add = [
    "Hablas más tonterías que un gilipollas con WiFi",
    "Tu lógica es tan estúpida que haría llorar a un retrasado",
    "Solo un imbécil como tú podría romper un 'Hello World'",
    "Eres tan capullo que los bugs huyen de tu código por vergüenza ajena",
    "Programas como un subnormal con las manos atadas",
    "Qué estúpido hay que ser para escribir eso y no borrarlo al instante",
    "Solo un cabrón sin alma escribiría esa basura de función",
    "Eres un cretino con teclado",
]

# Enviar insultos al servidor
for insult in insults_to_add:
    print("INSULTCLIENT -> Enviando texto a InsultService y InsultFilter:", insult)
    response = insult_service.add_insult(insult)
    filtered = insult_filter.filter_text(insult)
    print(response)
    print("INSULTFILTER -> Texto filtrado y agregado:", filtered)
    time.sleep(3) # Esperar 3 segundos antes de enviar otro
print("\n--- DEMOSTRACIÓN: Recuperando listas ---")
print("Lista completa de insultos almacenados en InsultService:")
print(insult_service.get_insults())
print("\nLista completa de textos filtrados en InsultFilter:")
print(insult_filter.get_filtered_texts())
