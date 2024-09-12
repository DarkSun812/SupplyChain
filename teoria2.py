import random
import matplotlib.pyplot as plt

class Tienda:
    def __init__(self, nombre, llegada_media):
        self.nombre = nombre
        self.llegada_media = llegada_media
        self.pedidos_en_cola = []

    def generar_pedido(self):
        return random.expovariate(1/self.llegada_media)

class Distribuidor:
    def __init__(self, capacidad_cola, servicio_media, inventario_inicial):
        self.capacidad_cola = capacidad_cola
        self.servicio_media = servicio_media
        self.pedidos_en_cola = []
        self.pedidos_procesados = []
        self.tiempo_actual = 0
        self.inventario = inventario_inicial  # Cantidad de productos disponibles

    def procesar_pedido(self):
        if self.inventario > 0:
            self.tiempo_actual += 1
            self.inventario -= 1  # Reducir el inventario al procesar un pedido
            return self.servicio_media
        else:
            print("No hay inventario disponible para procesar el pedido.")
            return None

def simular_dia(tiendas, distribuidor, duracion_simulacion):
    n = distribuidor.capacidad_cola
    for _ in range(duracion_simulacion):
        for tienda in tiendas:
            llegada = tienda.generar_pedido()
            print(distribuidor.tiempo_actual)
            print(llegada)
            tiempo_llegada = distribuidor.tiempo_actual + llegada
            
            if len(distribuidor.pedidos_en_cola) < n:
                distribuidor.pedidos_en_cola.append(tienda.nombre)
                print(f"Tienda {tienda.nombre} aceptada por el distribuidor")
            else:
                print(f"Tienda {tienda.nombre} rechazado por falta de capacidad en el distribuidor")
            
            print(f'tiempo_llegada: {tiempo_llegada}, tiempo_actual: {distribuidor.tiempo_actual}')
            if tiempo_llegada <= distribuidor.tiempo_actual:
                servicio = distribuidor.procesar_pedido()
                if servicio is not None:
                    distribuidor.pedidos_procesados.append(servicio)
        
        distribuidor.tiempo_actual += 1

def calcular_mertricas(distribuidor):
    lambda_val = len(distribuidor.pedidos_en_cola) / distribuidor.tiempo_actual
    mu_val = 1/distribuidor.servicio_media
    rho = lambda_val / mu_val
    
    if rho >= 1:
        print("El sistema es inestable (charmap >= 1). No se pueden calcular métricas.")
        return None, None, None, None, None, None
    
    wq = rho / ((1-rho)**2) * (mu_val/(mu_val-lambda_val))
    p0 = 1 - rho
    pn = rho**distribuidor.capacidad_cola
    ws = rho / (mu_val*(1-rho))
    w = ws + wq
    
    return rho, wq, p0, pn, ws, w

def visualizar_resultados(rho, wq, p0, pn, ws, w):
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 2, 1)
    plt.bar(['charmap', 'Wq', 'P0', 'Pn'], [rho, wq, p0, pn])
    plt.title('Probabilidades y Tiempos Promedio')
    plt.xlabel('Estado del Sistema')
    plt.ylabel('Valor')

    plt.subplot(2, 2, 2)
    plt.bar(['Ws', 'W'], [ws, w])
    plt.title('Tiempos Promedio de Servicio y Total')
    plt.xlabel('Tipo de Tiempo')
    plt.ylabel('Duración')

    plt.subplot(2, 2, 3)
    plt.plot([0, rho], [0, wq], label='Wq')
    plt.plot([0, rho], [wq, wq+ws*rho], label='Ws')
    plt.plot([0, rho], [wq+ws*rho, w], label='Total W')
    plt.title('Curva de Tiempos Promedio de Espera')
    plt.xlabel('charmap')
    plt.ylabel('Tiempo Promedio de Espera')
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.scatter(rho, wq, label=f'Wq={wq:.2f}')
    plt.scatter(rho, ws, label=f'Ws={ws:.2f}')
    plt.scatter(rho, w, label=f'W={w:.2f}')
    plt.title('Relación entre charmap y Tiempos Promedio de Espera')
    plt.xlabel('charmap')
    plt.ylabel('Tiempo Promedio de Espera')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Configurar parámetros
lambda_valores = [0.5, 1, 1.5, 2, 2.5]
mu_valores = [1, 1.5, 2, 2.5, 3]

for lambda_valor in lambda_valores:
    for mu_valor in mu_valores:
        rho = lambda_valor / mu_valor
        
        tiendas = [
            Tienda("Tienda A", lambda_valor),
            Tienda("Tienda B", lambda_valor),
            Tienda("Tienda C", lambda_valor)
        ]
        
        distribuidor = Distribuidor(capacidad_cola=3, servicio_media=mu_valor, inventario_inicial=2000)
        
        simular_dia(tiendas, distribuidor, duracion_simulacion=10)
        
        rho, wq, p0, pn, ws, w = calcular_mertricas(distribuidor)
        
        if rho is not None:
            print(f"\nSimulación con Lambda={lambda_valor}, Mu={mu_valor}:")
            print(f"charmap = {rho:.4f}")
            print(f"Wq = {wq:.2f}")
            print(f"P0 = {p0:.4f}")
            print(f"Pn = {pn:.4f}")
            print(f"Ws = {ws:.2f}")
            print(f"W = {w:.2f}\n")

            visualizar_resultados(rho, wq, p0, pn, ws, w)
