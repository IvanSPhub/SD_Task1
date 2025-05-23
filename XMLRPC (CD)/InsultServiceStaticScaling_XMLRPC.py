from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import threading
import time
import random
import redis
import sys

class QuietRequestHandler(SimpleXMLRPCRequestHandler):
    def log_message(self, format, *args):
        pass  # Desactiva los logs HTTP

# Obtener el puerto como argumento
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

# Conexión a Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
INSULT_LIST = "insult_list"

class InsultService:
    def __init__(self):
        self.subscribers = {}
        self.running = True
        self.cached_insults = []

        # Iniciar hilos en segundo plano
        self.updater_thread = threading.Thread(target=self.refresh_insult_cache, daemon=True)
        self.updater_thread.start()
        self.broadcaster_thread = threading.Thread(target=self.insult_broadcaster, daemon=True)
        self.broadcaster_thread.start()

    def add_insult(self, insult):
        existing = redis_client.lrange(INSULT_LIST, 0, -1)
        if insult not in existing:
            redis_client.rpush(INSULT_LIST, insult)
            print(f"INSULTSERVICE[{PORT}] -> Insulto agregado: {insult}")
            return f"Insulto agregado: {insult}"
        return "Insulto ya existente."

    def get_insults(self):
        return redis_client.lrange(INSULT_LIST, 0, -1)

    def insult_me(self):
        if self.cached_insults:
            #print("INSULTSERVICE -> Enviando insulto aleatorio...")
            insult = random.choice(self.cached_insults)
            return f"INSULTSERVICE[{PORT}] -> {insult}"
        else:
            return "No hay insultos disponibles."

    def add_subscriber(self, url):
        if url not in self.subscribers:
            self.subscribers[url] = xmlrpc.client.ServerProxy(url)
            print(f"INSULTSERVICE[{PORT}] -> Suscriptor agregado: {url}")
            return f"Suscriptor agregado: {url}"
        return "El suscriptor ya estaba registrado."

    def notify_subscribers(self, insult):
        for url, proxy in self.subscribers.items():
            try:
                proxy.notify(insult)
            except Exception as e:
                print(f"Error notificando a {url}: {e}")

    def insult_broadcaster(self):
        while self.running:
            if self.cached_insults and self.subscribers:
                insult = random.choice(self.cached_insults)
                print(f"INSULTSERVICE[{PORT}] -> Difundiendo insulto: {insult}")
                self.notify_subscribers(insult)
            time.sleep(5)
    
    def refresh_insult_cache(self):
        while self.running:
            # Actualiza la lista cacheada desde Redis
            self.cached_insults = redis_client.lrange(INSULT_LIST, 0, -1)

            if not self.cached_insults:
                #print(f"[REFRESH] No hay insultos aún. Reintentando en 0.5 segundos...")
                time.sleep(0.5)
            else:
                #print(f"[REFRESH] Caché actualizada con {len(self.cached_insults)} insultos. Próxima actualización en 30s.")
                time.sleep(30)

# Lanzar el servidor
server = SimpleXMLRPCServer(('127.0.0.1', PORT), requestHandler=QuietRequestHandler, allow_none=True)
service = InsultService()
server.register_instance(service)
print(f"INSULTSERVICE[{PORT}] -> Servidor corriendo en http://127.0.0.1:{PORT}")
server.serve_forever()

# Stress test (múltiples nodos)
# docker run --name my-redis -d -p 6379:6379 redis
# docker exec -it my-redis redis-cli
# python InsultServiceStaticScaling_XMLRPC.py 8000
# python InsultServiceStaticScaling_XMLRPC.py 8001
# python InsultServiceStaticScaling_XMLRPC.py 8002
# python StressTestStaticScaling_XMLRPC.py