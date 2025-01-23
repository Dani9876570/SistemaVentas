import tkinter as tk
from tkinter import font, Menu, messagebox
import pyodbc
from Productos import ProductoApp  # Importa la clase ProductoApp
from Categoria import CategoriaApp  # Importa la clase CategoriaApp desde la carpeta Categoria

# Conexión a la base de datos
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-I7SFIUG;'
    'DATABASE=SISTEMA_VENTA_PYTHON;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

def salir():
    # Cierra la aplicación
    root.destroy()

def abrir_ventana_categoria():
    # Ventana para Categoría
    categoria_ventana = tk.Toplevel(root)
    app = CategoriaApp(categoria_ventana)  # Crea una instancia de CategoriaApp

def abrir_ventana_producto():
    # Ventana para Producto
    producto_ventana = tk.Toplevel(root)
    app = ProductoApp(producto_ventana)  # Crea una instancia de ProductoApp

def abrir_ventana_venta():
    # Ventana para Registrar Venta
    venta_ventana = tk.Toplevel(root)
    venta_ventana.title("Registrar Venta")
    venta_ventana.geometry("400x300")
    venta_ventana.configure(bg='white')
    font_style = font.Font(family='Cambria', size=12, weight='bold')
    tk.Label(venta_ventana, text="Registrar Venta", bg='white', font=font_style).pack(pady=20)

def abrir_ventana_detalle_venta():
    # Ventana para Detalle de Venta
    detalle_venta_ventana = tk.Toplevel(root)
    detalle_venta_ventana.title("Detalle de Venta")
    detalle_venta_ventana.geometry("400x300")
    detalle_venta_ventana.configure(bg='white')
    font_style = font.Font(family='Cambria', size=12, weight='bold')
    tk.Label(detalle_venta_ventana, text="Detalles de Venta", bg='white', font=font_style).pack(pady=20)

# Función principal para iniciar el menú
def iniciar_menu():
    global root
    root = tk.Tk()
    root.title("Sistema de Gestión de Ventas")
    root.geometry("800x600")
    root.attributes('-fullscreen', True)  # Hace que la ventana ocupe toda la pantalla
    root.configure(bg='black')

    # Definir estilo de letra
    font_style = font.Font(family='Cambria', size=12, weight='bold')

    # Crear el menú
    menubar = Menu(root)
    root.config(menu=menubar)

    # Menú Mantenedor
    mantenedor_menu = Menu(menubar, tearoff=0)
    mantenedor_menu.add_command(label="Categoría", command=abrir_ventana_categoria)
    mantenedor_menu.add_command(label="Producto", command=abrir_ventana_producto)
    menubar.add_cascade(label="Mantenedor", menu=mantenedor_menu)

    # Menú Registro de Ventas
    registro_venta_menu = Menu(menubar, tearoff=0)
    registro_venta_menu.add_command(label="Registrar Venta", command=abrir_ventana_venta)
    menubar.add_cascade(label="Registrar Venta", menu=registro_venta_menu)

    # Menú Detalle de Venta
    detalle_venta_menu = Menu(menubar, tearoff=0)
    detalle_venta_menu.add_command(label="Detalle de Venta", command=abrir_ventana_detalle_venta)
    menubar.add_cascade(label="Detalle de Venta", menu=detalle_venta_menu)

    # Menú Salir
    menubar.add_command(label="Salir", command=salir)

    # Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()



