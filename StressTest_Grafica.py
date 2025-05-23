import matplotlib.pyplot as plt

# Resultados simulados
sistemas = ["XMLRPC", "PyRO", "Redis", "RabbitMQ"]
tiempos = [56.00, 18.12, 162.88, 194.84]  # Sustituye tiempos totales

# Crear gráfica
plt.figure(figsize=(10, 6))
plt.bar(sistemas, tiempos, color=["skyblue", "lightgreen", "orange", "salmon"])
plt.title("Comparativa de rendimiento en un solo nodo (con 50000 mensajes)")
plt.ylabel("Tiempo (segundos)")
plt.xlabel("Tecnología")
plt.grid(axis="y")

for i, tiempo in enumerate(tiempos):
    plt.text(i, tiempo + 0.1, f"{tiempo:.2f}", ha='center')

plt.savefig("stress_test.png")
# Mostrar la gráfica
plt.tight_layout()
plt.show()
