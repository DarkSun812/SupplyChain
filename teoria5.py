import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Constantes del modelo
alpha = 0.5  # Coeficiente de producción
beta = 0.1  # Tasa de desgaste
gamma = 0.8  # Coeficiente de conversión
delta = 0.05  # Tasa de desgaste del inventario
epsilon = 0.02  # Tasa de pérdida de pedidos pendientes
rho = 0.7     # Factor que relaciona la demanda con el inventario
sigma = 0.03  # Factor de saturación de la demanda
mu = 0.01    # Tasa de generación de pedidos
nu = 0.15    # Tasa de cumplimiento de pedidos
T = 0.5      # Tiempo promedio de servicio en la cola

# Función que calcula las derivadas de las variables de estado
def equations(state, t):

    alpha = 0.5  # Coeficiente de producción
    beta = 0.1  # Tasa de desgaste
    gamma = 0.8  # Coeficiente de conversión
    delta = 0.05  # Tasa de desgaste del inventario
    epsilon = 0.02  # Tasa de pérdida de pedidos pendientes
    rho = 0.7     # Factor que relaciona la demanda con el inventario
    sigma = 0.03  # Factor de saturación de la demanda
    mu = 0.01    # Tasa de generación de pedidos
    nu = 0.15    # Tasa de cumplimiento de pedidos
    T = 0.5      # Tiempo promedio de servicio en la cola

    if t<6 or t>=20:
        mu = 0
        nu= 0
        alpha= 0
        delta = 0
        gamma = 0
        rho = 0
        sigma = 0
    elif t>10 and t<14:
        mu = 0.05    # Tasa de generación de pedidos
        T=0.9
    else:
        alpha = 0.5  # Coeficiente de producción
        delta = 0.05  # Tasa de desgaste del inventario
        mu = 0.01    # Tasa de generación de pedidos
        nu = 0.15    # Tasa de cumplimiento de pedidos
       
    P, I, D, O = state  # Desempacotar el vector de estado
    
    # Calcular la derivada de la producción
    dPdt = alpha * ((D / P) / (1 + T)) - beta * P  # Modelo de producción con teoría de colas
    
    # Calcular la derivada del inventario
    dIdt = gamma * P - delta * I - epsilon * O  # Modelo de inventario
    
    # Calcular la derivada de la demanda
    dDdt = rho * ((I / D) / (1 + T)) - sigma * D  # Modelo de demanda con teoría de colas
    
    # Calcular la derivada de los pedidos pendientes
    dOdt = mu * D - (nu * O / (1 + T))  # Modelo de pedidos pendientes con teoría de colas
    # T = (mu * D - nu * O - dOdt) / dOdt
    # T = (mu * D - nu * O - dOdt) / dOdt
    return [dPdt, dIdt, dDdt, dOdt]

# Parámetros para la simulación
start_time = 0  # 00:00 horas
end_time = 24   # 24:00 horas
time_step = 0.25  # 15 minutos
total_steps = int((end_time - start_time) / time_step)
t = np.arange(start_time, end_time, time_step)

# Convertir la lista a un np.arange

    

# Estado inicial
state0 = [1, 20, 1, 0]  # Inicialización del estado (producción, inventario, demanda, pedidos pendientes)

# Resolver el sistema de ecuaciones diferenciales
sol = odeint(equations, state0, t)

# Calcular la longitud de la cola
queue_length = sol[:, 3] / nu

# Calcular los tiempos de espera.
wait_times = queue_length * T

# Definir funciones para cambiar la demanda basada en el tiempo
def normal_demand(t):
    return 20 + 5 * np.sin(np.pi * (t % 24) / 6)  # Demandas normales con un poco de variabilidad

def peak_demand(t):
    return 40 + 10 * np.sin(np.pi * (t % 24) / 6)  # Mayor demanda entre 10am y 2pm

# Aplicar demanda variable
for i in range(len(t)):
    if 6 <= t[i] < 8 or 10 <= t[i] < 14:
        sol[i, 2] += (peak_demand(t[i]) - normal_demand(t[i]))
    else:
        sol[i, 2] += (normal_demand(t[i]) - normal_demand(t[i]))

# Crear una figura con subplots
plt.figure(figsize=(14, 6))

# Subplot 1: Producción e Inventario
plt.subplot(221)
plt.plot(t, sol[:, 0], label='Producción')
plt.plot(t, sol[:, 1], label='Inventario')
plt.legend()
plt.title('Producción e Inventario')

# Subplot 2: Demanda
plt.subplot(222)
plt.plot(t, sol[:, 2], label='Demanda')
plt.title('Demanda')

# Subplot 3: Pedidos pendientes
plt.subplot(223)
plt.plot(t, sol[:, 3], label='Pedidos pendientes')
plt.title('Pedidos pendientes')

# Subplot 4: Tiempos de espera
plt.subplot(224)
plt.plot(t, wait_times, label='Tiempo de espera')
plt.title('Tiempo de espera')

# Subplot 5: Longitud de la cola
# plt.subplot(235)
# plt.plot(t, queue_length, label='Longitud de la cola')
# plt.title('Longitud de la cola')

# Ajustar el espacio entre los subplots
plt.tight_layout()

# Mostrar la gráfica
plt.show()

# Imprimir resultados finales
print("Simulación final:")
print(f"Producción final: {sol[-1, 0]:.2f}")
print(f"Inventario final: {sol[-1, 1]:.2f}")
print(f"Demanda final: {sol[-1, 2]:.2f}")
print(f"Pedidos pendientes final: {sol[-1, 3]:.2f}")
print(f"Promedio de tiempo de espera: {np.mean(wait_times):.2f} unidades de tiempo")
print(f"Maxima longitud de la cola: {np.max(queue_length):.2f}")

# # Gráfica adicional: Comparación de demanda
# plt.figure(figsize=(10, 6))
# plt.plot(t, normal_demand(t), label='Demanda normal')
# plt.plot(t, peak_demand(t), label='Demanda máxima')
# plt.xlabel('Tiempo (horas)')
# plt.ylabel('Demanda')
# plt.title('Comparación de demanda normal y máxima')
# plt.legend()
# plt.show()
