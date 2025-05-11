from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import threading
import time
import random

# Servicio que puede recibir insultos de forma remota y almacenarlos en una lista (add_insult).
# Ofrece mecanismos para:
# - Recuperar toda la lista de insultos (get_insults).
# - Difundir insultos aleatorios a los suscriptores cada 5 segundos (insult_broadcaster).
class InsultService:
    def __init__(self):
        self.insults = []  # Lista de insultos
        self.subscribers = {}  # Diccionario: clave=URL, valor=ServerProxy
        self.running = True

        # Iniciar el hilo (en segundo plano) para la difusión automática de insultos (broadcaster)
        self.broadcaster_thread = threading.Thread(target=self.insult_broadcaster, daemon=True)
        self.broadcaster_thread.start()

    # Función para agregar un insulto (evita duplicados)
    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.append(insult)
            print("INSULTSERVICE -> Insulto agregado:", insult)
            return f'INSULTSERVICE -> Insulto agregado: "{insult}"'
        return "INSULTSERVICE -> El insulto ya existe."

    # Función para obtener la lista de insultos
    def get_insults(self):
        return self.insults

    # Función para obtener un insulto aleatorio
    def insult_me(self):
        print("Enviando insulto aleatorio...")
        return random.choice(self.insults) if self.insults else "INSULTSERVICE -> No hay insultos disponibles."

    # Función para registrar suscriptores
    def add_subscriber(self, url):
        if url not in self.subscribers:
            proxy = xmlrpc.client.ServerProxy(url)
            self.subscribers[url] = proxy
            print("INSULTSERVICE -> Suscriptor agregado:", url)
            return f"INSULTSERVICE -> Suscriptor agregado: {url}"
        return "INSULTSERVICE -> El suscriptor ya está registrado."

    # Notificación a todos los suscriptores
    def notify_subscribers(self, insult):
        print("INSULTSERVICE -> Notificando a todos los suscriptores...")
        for url, proxy in self.subscribers.items():
            try:
                proxy.notify(insult)
            except Exception as e:
                print(f"INSULTSERVICE -> Error notificando a {url}: {e}")

    # Difusión de insultos cada 5 segundos
    def insult_broadcaster(self):
        while self.running:
            if self.insults and self.subscribers:
                insult = random.choice(self.insults)
                print(f"INSULTSERVICE -> Difundiendo insulto: {insult}")
                self.notify_subscribers(insult)
            time.sleep(5)

# Iniciar el servidor
server = SimpleXMLRPCServer(('localhost', 8000), requestHandler=SimpleXMLRPCRequestHandler)
service = InsultService()
server.register_instance(service)
print("INSULTSERVICE -> InsultService corriendo en http://localhost:8000")
server.serve_forever()

# Prueba unitaria
# Ejecutar en una terminal InsultService_XMLRPC.py
# Ejecutar en otra terminal InsultFilter_XMLRPC.py
# Ejecutar en otra terminal SubscriberService_XMLRPC.py
# Ejecutar en otra terminal InsultClient_XMLRPC.py

# Stress test (un solo nodo)
# Ejecutar en una terminal InsultService_XMLRPC.py
# Ejecutar en otra terminal StressTest_XMLRPC.py