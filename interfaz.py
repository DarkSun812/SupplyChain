import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


# Inicializar constantes del modelo
constants = {
    'alpha': 0.5,
    'beta': 0.1,
    'gamma': 0.8,
    'delta': 0.05,
    'epsilon': 0.02,
    'rho': 0.7,
    'sigma': 0.03,
    'mu': 0.01,
    'nu': 0.15,
    'T': 0.5
}

# Clase para el tooltip
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window is not None:  # Si ya hay una ventana de tooltip, no hace nada
            return
        x = self.widget.winfo_rootx() + 20  # Calcula la posición x para el tooltip
        y = self.widget.winfo_rooty() + 20  # Calcula la posición y para el tooltip
        self.tooltip_window = tk.Toplevel(self.widget)  # Crea una nueva ventana para el tooltip
        self.tooltip_window.wm_overrideredirect(True)  # Elimina el borde de la ventana del tooltip
        self.tooltip_window.wm_geometry(f"+{x}+{y}")  # Establece la geometría de la ventana del tooltip
        label = tk.Label(self.tooltip_window, text=self.text, background="lightyellow", relief="solid", borderwidth=1)  # Crea una etiqueta para el tooltip
        label.pack()  # Empaqueta la etiqueta en la ventana del tooltip

    def hide_tooltip(self, event=None):
        if self.tooltip_window:  # Si la ventana del tooltip existe
            self.tooltip_window.destroy()  # Destruye la ventana del tooltip
            self.tooltip_window = None  # Reinicia la ventana del tooltip a None

# Función que calcula las derivadas de las variables de estado
def equations(state, t, constants):
    P, I, D, O = state
    for key in constants:
        constants[key] = float(entries[key].get())
        
    # Ajusta las constantes según el tiempo
    if t < 6 or t >= 20:
        constants['mu'] = 0.00000000000001  # Ajusta mu
        constants['nu'] = 0.00000000000001  # Ajusta nu
        constants['alpha'] = 0.00000000000001  # Ajusta alpha
        constants['delta'] = 0.00000000000001  # Ajusta delta
        constants['gamma'] = 0.00000000000001  # Ajusta gamma
        constants['rho'] = 0.00000000000001  # Ajusta rho
        constants['sigma'] = 0.00000000000001  # Ajusta sigma
    elif t > 10 and t < 14:
        constants['mu'] = constants['mu'] * 2 + constants['mu']  # Tasa de generación de pedidos
        constants['T'] = constants['T'] * 1.5 + constants['T']  # Ajusta T

    # Calcula las derivadas
    dPdt = constants['alpha'] * ((D / P) / (1 + constants['T'])) - constants['beta'] * P  # Derivada de P
    dIdt = constants['gamma'] * P - constants['delta'] * I - constants['epsilon'] * O  # Derivada de I
    dDdt = constants['rho'] * ((I / D) / (1 + constants['T'])) - constants['sigma'] * D  # Derivada de D
    dOdt = constants['mu'] * D - (constants['nu'] * O / (1 + constants['T']))  # Derivada de O
    return [dPdt, dIdt, dDdt, dOdt]  # Retorna las derivadas

def generar_grafico():
    for key in constants:
        constants[key] = float(entries[key].get())
    
    t = np.arange(0, 24, 0.25)  # Crea un array de tiempo de 0 a 24 con pasos de 0.25
    state0 = [1, 20, 1, 0]  # Estado inicial
    sol = odeint(equations, state0, t, args=(constants,))  # Resuelve las ecuaciones diferenciales

    # Define funciones para cambiar la demanda basada en el tiempo
    def normal_demand(t):
        return 20 + 5 * np.sin(np.pi * (t % 24) / 6)  # Demanda normal con variabilidad

    def peak_demand(t):
        return 40 + 10 * np.sin(np.pi * (t % 24) / 6)  # Mayor demanda entre 10am y 2pm

    # Aplica demanda variable
    for i in range(len(t)):
        if 6 <= t[i] < 8 or 10 <= t[i] < 14:
            sol[i, 2] += (peak_demand(t[i]) - normal_demand(t[i]))  # Ajusta la demanda en picos
        else:
            sol[i, 2] += (normal_demand(t[i]) - normal_demand(t[i]))  # Ajusta la demanda normal
        
    # Actualiza los gráficos
    axs[0, 0].cla()  # Limpia el gráfico de producción e inventario
    axs[0, 0].plot(t, sol[:, 0], label='Producción')  # Grafica la producción
    axs[0, 0].plot(t, sol[:, 1], label='Inventario')  # Grafica el inventario
    axs[0, 0].legend()  # Muestra la leyenda
    axs[0, 0].set_title('Producción e Inventario')  # Establece el título

    axs[0, 1].cla()  # Limpia el gráfico de demanda
    axs[0, 1].plot(t, sol[:, 2], label='Demanda')  # Grafica la demanda
    axs[0, 1].set_title('Demanda')  # Establece el título

    axs[1, 0].cla()  # Limpia el gráfico de pedidos pendientes
    axs[1, 0].plot(t, sol[:, 3], label='Pedidos pendientes')  # Grafica los pedidos pendientes
    axs[1, 0].set_title('Pedidos pendientes')  # Establece el título

    wait_times = sol[:, 3] / constants['nu'] * constants['T']  # Calcula los tiempos de espera
    axs[1, 1].cla()  # Limpia el gráfico de tiempo de espera
    axs[1, 1].plot(t, wait_times, label='Tiempo de espera')  # Grafica el tiempo de espera
    axs[1, 1].set_title('Tiempo de espera')  # Establece el título

    plt.tight_layout()  # Ajusta el diseño para que no se superpongan los gráficos
    canvas.draw()  # Dibuja el canvas con los nuevos gráficos

# Crear la ventana principal de Tkinter
root = tk.Tk() # Inicializa la ventana principal root.title("Simulación de Producción y Demanda") # Establece el título de la ventana
root.title("Simulación de Producción y Demanda")

# Crear inputs para los parámetros
entries = {}
param_names = list(constants.keys())
descriptions = {
    'alpha': 'Coeficiente de producción',
    'beta': 'Tasa de desgaste',
    'gamma': 'Coeficiente de conversión',
    'delta': 'Tasa de desgaste del inventario',
    'epsilon': 'Tasa de pérdida de pedidos pendientes',
    'rho': 'Factor que relaciona la demanda con el inventario',
    'sigma': 'Factor de saturación de la demanda',
    'mu': 'Tasa de generación de pedidos',
    'nu': 'Tasa de cumplimiento de pedidos',
    'T': 'Tiempo promedio de servicio en la cola'
}

for i, param in enumerate(param_names):
    ttk.Label(root, text=param).grid(column=0, row=i)
    entry = ttk.Entry(root)
    entry.grid(column=1, row=i)
    entry.insert(0, constants[param])  # Establecer valor por defecto
    entries[param] = entry
    ToolTip(entry, descriptions[param])  # Agregar tooltip

# Botón para generar el gráfico
generar_button = ttk.Button(root, text="Generar Gráfico", command=generar_grafico)
generar_button.grid(column=0, row=len(param_names), columnspan=2)

# Crear una figura con subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 6))

# Crear un canvas para mostrar la figura de Matplotlib
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=2, row=0, rowspan=len(param_names) + 1)

# Generar gráfico inicial
generar_grafico()

# Iniciar el bucle principal de Tkinter
root.mainloop()
