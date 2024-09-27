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
        if self.tooltip_window is not None:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

# Función que calcula las derivadas de las variables de estado
def equations(state, t, constants):
    P, I, D, O = state
    dPdt = constants['alpha'] * ((D / P) / (1 + constants['T'])) - constants['beta'] * P
    dIdt = constants['gamma'] * P - constants['delta'] * I - constants['epsilon'] * O
    dDdt = constants['rho'] * ((I / D) / (1 + constants['T'])) - constants['sigma'] * D
    dOdt = constants['mu'] * D - (constants['nu'] * O / (1 + constants['T']))
    return [dPdt, dIdt, dDdt, dOdt]

def generar_grafico():
    for key in constants:
        constants[key] = float(entries[key].get())
    
    t = np.arange(0, 24, 0.25)
    state0 = [1, 20, 1, 0]
    sol = odeint(equations, state0, t, args=(constants,))

    axs[0, 0].cla()
    axs[0, 0].plot(t, sol[:, 0], label='Producción')
    axs[0, 0].plot(t, sol[:, 1], label='Inventario')
    axs[0, 0].legend()
    axs[0, 0].set_title('Producción e Inventario')

    axs[0, 1].cla()
    axs[0, 1].plot(t, sol[:, 2], label='Demanda')
    axs[0, 1].set_title('Demanda')

    axs[1, 0].cla()
    axs[1, 0].plot(t, sol[:, 3], label='Pedidos pendientes')
    axs[1, 0].set_title('Pedidos pendientes')

    wait_times = sol[:, 3] / constants['nu'] * constants['T']
    axs[1, 1].cla()
    axs[1, 1].plot(t, wait_times, label='Tiempo de espera')
    axs[1, 1].set_title('Tiempo de espera')

    plt.tight_layout()
    canvas_plot.draw()

# Función para agregar nuevos intervalos
def agregar_intervalo():
    row = len(scrollable_frame.grid_slaves())  # Obtener la fila donde se agregarán los nuevos intervalos
    ttk.Label(scrollable_frame, text=f"Intervalo {row+1}:").grid(column=0, row=row)
    interval_entry = ttk.Entry(scrollable_frame)
    interval_entry.grid(column=1, row=row)
    percentage_entry = ttk.Entry(scrollable_frame)
    percentage_entry.grid(column=2, row=row)
    percentage_entry.insert(0, "0")  # Valor por defecto

# Crear la ventana principal de Tkinter
root = tk.Tk()
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

# Crear el menú de la izquierda
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

# Crear un marco para el nuevo menú a la derecha
right_frame = ttk.Frame(root)
right_frame.grid(column=3, row=0, rowspan=len(param_names) + 1, padx=10)

# Parte superior: selección de días
ttk.Label(right_frame, text="Cantidad de días:").grid(column=0, row=0)
days_entry = ttk.Entry(right_frame)
days_entry.grid(column=1, row=0)
days_entry.insert(0, "1")  # Valor por defecto

# Parte inferior: scroll para intervalos de tiempo
scroll_frame = ttk.Frame(right_frame)
scroll_frame.grid(column=0, row=1)

# Crear un canvas y scrollbar
canvas = tk.Canvas(scroll_frame, width=300, height=200)
scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

# Configurar el canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Agregar el canvas y scrollbar al marco
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Botón para agregar nuevos intervalos
agregar_button = ttk.Button(right_frame, text="Agregar Intervalo", command=agregar_intervalo)
agregar_button.grid(column=0, row=2, columnspan=2)

# Crear una figura con subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 6))  # Ajustar el tamaño de la figura

# Crear un canvas para mostrar la figura de Matplotlib
canvas_plot = FigureCanvasTkAgg(fig, master=root)
canvas_plot.get_tk_widget().grid(column=2, row=0, rowspan=len(param_names) + 1)  # Mover a la columna 1

# Generar gráfico inicial
generar_grafico()

# Iniciar el bucle principal de Tkinter
root.mainloop()
