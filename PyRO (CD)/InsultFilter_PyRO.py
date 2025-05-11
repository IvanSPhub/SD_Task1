import Pyro4

# Implementa un servicio basado en el patrón de Work Queue.
# Permite que los clientes envíen textos que pueden o no contener insultos.
# Reemplaza los insultos en el texto por la palabra "CENSORED" y guarda el texto filtrado en una lista.
# Puede devolver la lista si se solicita.

# Lista de insultos que serán censurados
insults = [
    "gilipollas", "retrasado", "imbécil", "idiotas", "subnormal", "cabrón",
    "capullo", "cretino", "estúpida", "estúpido", "basura"
]

# Clase que implementa el servicio de filtrado
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class InsultFilter:
    def __init__(self):
        # Lista de textos filtrados
        self.filtered_texts = []

    # Filtra el texto reemplazando insultos por 'CENSORED'
    def filter_text(self, text):
        print(f"INSULTFILTER -> Texto recibido: {text}")
        words = text.split()
        filtered = ["CENSORED" if word.lower() in insults else word for word in words]
        result = " ".join(filtered)
        self.filtered_texts.append(result)
        print(f"INSULTFILTER -> Texto filtrado: {result}")
        print("INSULTFILTER -> Texto filtrado agregado.")
        return result

    # Devuelve la lista de textos filtrados
    def get_filtered_texts(self):
        print(f"INSULTFILTER -> Devolviendo {len(self.filtered_texts)} textos filtrados.")
        return self.filtered_texts

# Inicio del servidor Pyro
def main():
    daemon = Pyro4.Daemon() # Crea el servidor Pyro
    ns = Pyro4.locateNS() # Localiza el Name Server

    uri = daemon.register(InsultFilter) # Registra el objeto
    ns.register("insult.filter", uri) # Lo nombra en el Name Server

    print(f"INSULTFILTER -> Servidor corriendo. URI: {uri}")
    daemon.requestLoop() # Espera peticiones

if __name__ == "__main__":
    main()
