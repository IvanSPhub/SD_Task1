import Pyro4
import threading
import time
import random
import redis
import sys

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class InsultService:
    def __init__(self):
        self.redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        self.insult_list = "INSULTS"
        self.subscribers = []
        self.cached_insults = []
        self.running = True

        # Hilo para refrescar insultos
        self.refresh_thread = threading.Thread(target=self.refresh_insult_cache, daemon=True)
        self.refresh_thread.start()
        # Hilo para difundir insultos
        self.broadcast_thread = threading.Thread(target=self.insult_broadcaster, daemon=True)
        self.broadcast_thread.start()

    def refresh_insult_cache(self):
        while self.running:
            insults = self.redis_client.lrange(self.insult_list, 0, -1)
            self.cached_insults = insults

            if not insults:
                #print("[REFRESH] No hay insultos aún. Reintentando en 0.5s...")
                time.sleep(0.5)
            else:
                #print(f"[REFRESH] {len(insults)} insultos cacheados. Próxima actualización en 30s.")
                time.sleep(30)

    def add_insult(self, insult):
        existing = self.redis_client.lrange(self.insult_list, 0, -1)
        if insult not in existing:
            self.redis_client.rpush(self.insult_list, insult)
            print(f"INSULTSERVICE -> Insulto agregado: {insult}")
            return "Insulto agregado con éxito."
        return "El insulto ya existe."

    def get_insults(self):
        return self.cached_insults

    def insult_me(self):
        if self.cached_insults:
            insult = random.choice(self.cached_insults)
            #print(f"INSULTSERVICE -> Insulto enviado: {insult}")
            return insult
        else:
            return "No hay insultos disponibles."

    def add_subscriber(self, observer_uri):
        observer = Pyro4.Proxy(observer_uri)
        if observer_uri not in [obs._pyroUri for obs in self.subscribers]:
            self.subscribers.append(observer)
            print(f"INSULTSERVICE -> Suscriptor registrado: {observer_uri}")
            return "Suscriptor registrado correctamente."
        return "El suscriptor ya estaba registrado."

    def notify_subscribers(self, insult):
        print("INSULTSERVICE -> Notificando a los suscriptores...")
        for observer in self.subscribers:
            try:
                observer.update(insult)
            except Pyro4.errors.CommunicationError:
                print(f"INSULTSERVICE -> Error al notificar a {observer._pyroUri}")

    def insult_broadcaster(self):
        while self.running:
            if self.cached_insults and self.subscribers:
                insult = random.choice(self.cached_insults)
                print(f"INSULTSERVICE -> Difundiendo insulto: {insult}")
                self.notify_subscribers(insult)
            time.sleep(5)

def main():
    service_name = sys.argv[1] # Por ejemplo: insult.service.1000
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(InsultService)
    ns.register(service_name, uri)
    print(f"INSULTSERVICE -> Servidor corriendo. Nombre: {service_name}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()

# python -m Pyro4.naming
# docker run --name my-redis -d -p 6379:6379 redis
# docker exec -it my-redis redis-cli
# python InsultServiceStaticScaling_PyRO.py insult.service.1000
# python InsultServiceStaticScaling_PyRO.py insult.service.1001
# python InsultServiceStaticScaling_PyRO.py insult.service.1002