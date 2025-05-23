import Pyro4
import threading
import time
import random

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")  # Para mantener una única instancia
# Servicio que puede recibir insultos de forma remota y almacenarlos en una lista (add_insult).
# Ofrece mecanismos para:
# - Recuperar toda la lista de insultos (get_insults).
# - Difundir insultos aleatorios a los suscriptores cada 5 segundos (insult_broadcaster).
class InsultService:
    def __init__(self):
        self.insults = []  # Lista de insultos
        self.subscribers = []  # Lista de proxies a observadores

        # Iniciar hilo (en segundo plano) para la difusión automática de insultos (broadcaster)
        self.running = True
        self.thread = threading.Thread(target=self.insult_broadcaster, daemon=True)
        self.thread.start()

    # Función para agregar un insulto (evita duplicados)
    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.append(insult)
            print(f"INSULTSERVICE -> Insulto agregado: {insult}")
            return "Insulto agregado con éxito."
        return "El insulto ya existe."

    # Función para obtener la lista de insultos
    def get_insults(self):
        return self.insults

    # Función para obtener un insulto aleatorio
    def insult_me(self):
        #print("INSULTSERVICE -> Enviando insulto aleatorio...")
        return random.choice(self.insults) if self.insults else "No hay insultos disponibles."

    # Función para registrar suscriptores
    def add_subscriber(self, observer_uri):
        observer = Pyro4.Proxy(observer_uri)
        if observer_uri not in [obs._pyroUri for obs in self.subscribers]:
            self.subscribers.append(observer)
            print(f"INSULTSERVICE -> Suscriptor registrado: {observer_uri}")
            return "Suscriptor registrado correctamente."
        return "El suscriptor ya estaba registrado."

    # Notificación a todos los suscriptores
    def notify_subscribers(self, insult):
        print("INSULTSERVICE -> Notificando a los suscriptores...")
        for observer in self.subscribers:
            try:
                observer.update(insult)
            except Pyro4.errors.CommunicationError:
                print(f"INSULTSERVICE -> Error al notificar a {observer._pyroUri}")

    # Difusión de insultos cada 5 segundos
    def insult_broadcaster(self):
        while self.running:
            if self.insults and self.subscribers:
                insult = random.choice(self.insults)
                print(f"INSULTSERVICE -> Difundiendo insulto: {insult}")
                self.notify_subscribers(insult)
            time.sleep(5)

# --- Inicio del servidor Pyro ---
def main():
    daemon = Pyro4.Daemon()  # Crea el servidor Pyro
    ns = Pyro4.locateNS()  # Localiza el Name Server

    uri = daemon.register(InsultService)  # Registra el objeto
    ns.register("insult.service", uri)  # Lo nombra en el Name Server

    print(f"INSULTSERVICE -> Servidor corriendo. URI: {uri}")
    daemon.requestLoop()  # Espera peticiones

if __name__ == "__main__":
    main()

# Prueba unitaria
# 1. Ejecutar este comando en una terminal: python -m Pyro4.naming
# 2. Ejecutar InsultService_PyRO.py en una nueva terminal
# 3. Ejecutar InsultFilter_PyRO.py en otra terminal
# 4. Ejecutar SubscriberService_PyRO.py en otra terminal
# 5. Ejecutar InsultClient_PyRO.py en otra terminal

# Stress test (un solo nodo)
# python -m Pyro4.naming
# Ejecutar InsultService_PyRO.py en una nueva terminal
# Ejecutar StressTest_PyRO.py en una nueva terminal