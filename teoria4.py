import numpy as np
from matplotlib import pyplot as plt

def simulacion_cadena_suministro(alpha, beta, gamma, delta, epsilon, rho, sigma, mu, nu, t_max, dt):
    t = np.arange(0, t_max, dt)
    n = len(t)
    
    P = np.zeros(n)
    I = np.zeros(n)
    D = np.zeros(n)
    O = np.zeros(n)
    
    # Condiciones iniciales
    P[0] = 100
    I[0] = 50
    D[0] = 80
    O[0] = 20
    
    for i in range(1, n):
        P[i] = P[i-1] + dt * (alpha * (D[i-1] / P[i-1]) - beta * P[i-1])
        I[i] = I[i-1] + dt * (gamma * P[i-1] - delta * I[i-1] - epsilon * O[i-1])
        D[i] = D[i-1] + dt * (rho * (I[i-1] / D[i-1]) - sigma * D[i-1])
        O[i] = O[i-1] + dt * (mu * D[i-1] - nu * O[i-1])
    
    return t, P, I, D, O

# Ejemplo de uso
t, P, I, D, O = simulacion_cadena_suministro(
    alpha=0.5, beta=0.1, gamma=0.8, delta=0.05, epsilon=0.2,
    rho=0.3, sigma=0.15, mu=0.4, nu=0.25,
    t_max=100, dt=0.1
)

plt.figure(figsize=(12, 6))
plt.plot(t, P, label='Producción')
plt.plot(t, I, label='Inventario')
plt.plot(t, D, label='Demanda')
plt.plot(t, O, label='Pedidos Pendientes')
plt.xlabel('Tiempo')
plt.ylabel('Valor')
plt.title('Simulación de Cadena de Suministro')
plt.legend()
plt.show()
