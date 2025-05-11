import Pyro4
import time

# Cliente que envía insultos nuevos al InsultService
def main():
    # Crear proxies a InsultService e InsultFilter
    insult_service = Pyro4.Proxy("PYRONAME:insult.service")
    insult_filter = Pyro4.Proxy("PYRONAME:insult.filter")

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
    
    # Enviar insultos al servicio y filtrarlos
    for insult in insults_to_add:
        print("INSULTCLIENT -> Enviando texto a InsultService y InsultFilter:", insult)
        # Filtrar el texto
        filtered = insult_filter.filter_text(insult)
        print("INSULTFILTER -> Texto filtrado y agregado:", filtered)
        # Añadir insulto al servicio (ya filtrado o no)
        response = insult_service.add_insult(insult)
        print("INSULTSERVICE -> Insulto agregado:", response)
        time.sleep(3)  # Esperar 3 segundos antes del siguiente
    print("\n--- DEMOSTRACIÓN: Recuperando listas ---")
    print("Lista completa de insultos almacenados en InsultService:")
    print(insult_service.get_insults())
    print("\nLista completa de textos filtrados en InsultFilter:")
    print(insult_filter.get_filtered_texts())

if __name__ == "__main__":
    main()
