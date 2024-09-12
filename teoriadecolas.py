import simpy
import numpy as np
import matplotlib.pyplot as plt

# Parámetros del Modelo
ARRIVAL_RATE = 10  # Tasa de llegada de pedidos (pedidos/hora)
SERVICE_RATE = 6  # Tasa de servicio (entregas/hora)
NUM_SERVERS = 3  # Número de camiones/servidores

# Simulación del Sistema de Colas
env = simpy.Environment()
store = simpy.Resource(env, capacity=NUM_SERVERS)

def customer_arrival(env):
    while True:
        # Llegada de un nuevo pedido
        yield env.timeout(np.random.exponential(1/ARRIVAL_RATE))
        with store.request() as req:
            # Esperar a que un servidor esté disponible
            start = env.now
            yield req
            # Tiempo de servicio (entrega)
            yield env.timeout(np.random.exponential(1/SERVICE_RATE))
            # Registrar el tiempo de espera
            wait_times.append(env.now - start)

# Ejecutar la simulación
wait_times = []
env.process(customer_arrival(env))
env.run(until=1000)

# Calcular y graficar métricas
utilization = sum(wait_times) / (NUM_SERVERS * env.now)

plt.figure(figsize=(10, 6))
plt.hist(wait_times, bins=20, edgecolor='black')
plt.xlabel('Tiempo de Espera (horas)')
plt.ylabel('Frecuencia')
plt.title('Distribución de Tiempos de Espera')
plt.show()

print(f'Utilización de los Servidores: {utilization:.2f}')
