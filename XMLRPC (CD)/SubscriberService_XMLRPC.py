from xmlrpc.server import SimpleXMLRPCServer

# InsultService (Sujeto) notifica a SubscriberService (Observador) cada vez que difunde un insulto.

# Método que recibe notificaciones de insultos del difusor de InsultService (insult_broadcaster)
def notify(insult):
    print(f"SUBSCRIBERSERVICE -> Insulto recibido de InsultService: {insult}")
    return "Notificación recibida."

# Iniciar el servidor de suscriptor
with SimpleXMLRPCServer(("127.0.0.1", 8002)) as server:
    server.register_function(notify, 'notify')

    print(f"SUBSCRIBERSERVICE -> SubscriberService corriendo en http://127.0.0.1:8002")
    server.serve_forever()
