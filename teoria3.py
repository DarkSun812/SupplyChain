import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Parámetros del sistema
lambda_1 = 10  # Tasa de llegada al primer nodo
mu_1 = 15      # Tasa de servicio del primer nodo
capacidad_1 = 100  # Capacidad máxima del primer nodo

lambda_2 = 12  # Tasa de llegada al segundo nodo
mu_2 = 18     # Tasa de servicio del segundo nodo
capacidad_2 = 150  # Capacidad máxima del segundo nodo

# Función de derivación para resolver el sistema de ecuaciones diferenciales
def deriv(X, t):
    L1, L2 = X
    dL1_dt = lambda_1 - mu_1 * min(L1, capacidad_1)
    dL2_dt = lambda_2 - mu_2 * min(L2, capacidad_2)
    return [dL1_dt, dL2_dt]

# Condición inicial
X0 = [0, 0]  # Inicialmente ambas colas están vacías

# Tiempo de simulación
t = np.linspace(0, 100)

# Resolver el sistema de ecuaciones diferenciales
sol = odeint(deriv, X0, t)

# Graficar los resultados
plt.figure(figsize=(12, 6))

plt.subplot(121)
plt.plot(t, sol[:, 0], label='Cola 1')
plt.plot(t, sol[:, 1], label='Cola 2')
plt.xlabel('Tiempo')
plt.ylabel('Longitud de la cola')
plt.title('Simulación de la cadena de suministro')
plt.legend()

plt.subplot(122)
plt.plot(t, sol[:, 0]/capacidad_1, label='Utilización de Nodo 1')
plt.plot(t, sol[:, 1]/capacidad_2, label='Utilización de Nodo 2')
plt.xlabel('Tiempo')
plt.ylabel('Proporción de capacidad utilizada')
plt.title('Utilización de los nodos')
plt.legend()

plt.tight_layout()
plt.show()
