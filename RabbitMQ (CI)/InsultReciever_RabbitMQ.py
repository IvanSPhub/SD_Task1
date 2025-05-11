import pika

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar el exchange fanout (por si no existe)
channel.exchange_declare(exchange='insult_exchange', exchange_type='fanout')

# Crear una cola temporal (nombre aleatorio, se borra al cerrar)
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Enlazar la cola temporal al exchange
channel.queue_bind(exchange='insult_exchange', queue=queue_name)

print("InsultReciever esperando insultos...")

# Función para manejar los mensajes
def callback(ch, method, properties, body):
    print(f"Insulto recibido: {body.decode()}")

# Consumir mensajes de la cola
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
