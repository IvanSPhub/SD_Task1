import matplotlib.pyplot as plt

# Datos de speedup
sistemas = ["XMLRPC", "PyRO", "Redis", "RabbitMQ"]
speedups = {
    "XMLRPC": [1.00, 1.98, 2.96],
    "PyRO": [1.00, 1.02, 1.07],
    "Redis": [1.00, 1.35, 1.38],
    "RabbitMQ": [1.00, 1.06, 1.09]
}

# Eje X: número de nodos
nodos = [1, 2, 3]

# Crear gráfica
plt.figure(figsize=(10, 6))
for sistema in sistemas:
    plt.plot(nodos, speedups[sistema], marker="o", label=sistema)

plt.title("Speedup comparativo (con 1000 mensajes)")
plt.xlabel("Número de nodos")
plt.ylabel("Speedup")
plt.xticks(nodos)
plt.grid(True)
plt.legend()
plt.savefig("speedup_escalado_estatico.png")
plt.tight_layout()
plt.show()
