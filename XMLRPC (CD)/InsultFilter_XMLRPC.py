from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

# Implementa un servicio basado en el patrón de Work Queue (simula una cola de trabajo a través de llamadas XML-RPC).
# Permite que los clientes envíen textos que pueden o no contener insultos.
# Reemplaza los insultos en el texto por la palabra "CENSORED" y guarda el texto filtrado en una lista.
# Puede devolver la lista si se solicita.

# Lista de insultos prohibidos
insults = [
    "gilipollas", "retrasado", "imbécil", "idiotas", "subnormal", "cabrón",
    "capullo", "cretino", "estúpida", "estúpido", "basura"
]

# Lista de textos filtrados
filtered_texts = []

# Filtra el texto reemplazando insultos por 'CENSORED'
def filter_text(text):
    print(f"INSULTFILTER -> Texto recibido: {text}")
    words = text.split()
    filtered = ["CENSORED" if word.lower() in insults else word for word in words]
    result = " ".join(filtered)
    print(f"INSULTFILTER -> Texto filtrado: {result}")
    filtered_texts.append(result)
    print("INSULTFILTER -> Texto filtrado agregado.")
    return result

# Devuelve la lista de textos filtrados
def get_filtered_texts():
    print(f"INSULTFILTER -> Devolviendo {len(filtered_texts)} textos filtrados.")
    return filtered_texts

# Iniciar el servidor XMLRPC
with SimpleXMLRPCServer(('127.0.0.1', 8001), requestHandler=SimpleXMLRPCRequestHandler) as server:
    server.register_function(filter_text, 'filter_text')
    server.register_function(get_filtered_texts, 'get_filtered_texts')
    print("INSULTFILTER -> InsultFilter en ejecución en http://127.0.0.1:8001")
    server.serve_forever()
