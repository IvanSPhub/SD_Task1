import Pyro4

# Clase observadora que se registrará en el InsultService (sujeto)
@Pyro4.expose
class Subscriber:
    # Método que recibe notificaciones de insultos del difusor de InsultService (insult_broadcaster)
    def update(self, insult):
        # Este método será llamado remotamente por el InsultService
        print(f"SUBSCRIBERSERVICE -> Insulto recibido de InsultService: {insult}")
        return "Notificación recibida."

def main():
    # Localiza el Name Server
    ns = Pyro4.locateNS()

    # Crea el objeto local y lo registra en el Daemon
    with Pyro4.Daemon() as daemon:
        subscriber = Subscriber()
        uri = daemon.register(subscriber)

        # Crea un proxy hacia InsultService
        insult_service = Pyro4.Proxy("PYRONAME:insult.service")

        # Se registra como suscriptor en InsultService
        response = insult_service.add_subscriber(str(uri))
        print(f"SUBSCRIBERSERVICE -> Registrado en InsultService: {response}")
        print(f"SUBSCRIBERSERVICE -> Esperando insultos en URI: {uri}")

        daemon.requestLoop()

if __name__ == "__main__":
    main()
