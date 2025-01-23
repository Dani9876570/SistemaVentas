import tkinter as tk
from tkinter import messagebox, font
import pyodbc
from Menu import iniciar_menu  # Importa la función iniciar_menu desde Menu.py

# Conexión a la base 
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'  # Especifica el controlador ODBC
    'SERVER=DESKTOP-I7SFIUG;'  # Nombre del servidor SQL Server
    'DATABASE=SISTEMA_VENTA_PYTHON;'  # Nombre de la base de datos
    'Trusted_Connection=yes;'  # Utiliza autenticación integrada de Windows
)
cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL

def abrir_ventana_registro():
    # Crea una nueva ventana para registrar un usuario
    registro_ventana = tk.Toplevel(root)
    registro_ventana.title("Registrar Usuario")
    registro_ventana.geometry("400x300")
    registro_ventana.resizable(False, False)
    
    # Cambiar el color de fondo de la ventana de registro
    registro_ventana.configure(bg='white')

    # Centrando la ventana de registro en la pantalla
    window_width = 400
    window_height = 300
    screen_width = registro_ventana.winfo_screenwidth()
    screen_height = registro_ventana.winfo_screenheight()
    position_top = int(screen_height/2 - window_height/2)
    position_right = int(screen_width/2 - window_width/2)
    registro_ventana.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Definir estilo de letra
    font_style = font.Font(family='Cambria', size=12, weight='bold')

    # Etiquetas y campos de entrada para los datos de registro
    tk.Label(registro_ventana, text="Documento", bg='white', font=font_style).grid(row=0, column=0, padx=10, pady=10)
    tk.Label(registro_ventana, text="Nombre Completo", bg='white', font=font_style).grid(row=1, column=0, padx=10, pady=10)
    tk.Label(registro_ventana, text="Clave", bg='white', font=font_style).grid(row=2, column=0, padx=10, pady=10)
    tk.Label(registro_ventana, text="Verificar Clave", bg='white', font=font_style).grid(row=3, column=0, padx=10, pady=10)

    # Campos de entrada para los datos de registro con borde más visible
    entry_documento_reg = tk.Entry(registro_ventana, relief='solid', bd=2)
    entry_documento_reg.grid(row=0, column=1, padx=10, pady=10)
    entry_nombre_completo_reg = tk.Entry(registro_ventana, relief='solid', bd=2)
    entry_nombre_completo_reg.grid(row=1, column=1, padx=10, pady=10)
    entry_clave_reg = tk.Entry(registro_ventana, show='*',  relief='solid', bd=2)
    entry_clave_reg.grid(row=2, column=1, padx=10, pady=10)
    entry_verificar_clave_reg = tk.Entry(registro_ventana, show='*', relief='solid', bd=2)
    entry_verificar_clave_reg.grid(row=3, column=1, padx=10, pady=10)

    def registrar():
        # Obtiene los valores ingresados en los campos de entrada
        documento = entry_documento_reg.get()
        nombre_completo = entry_nombre_completo_reg.get()
        clave = entry_clave_reg.get()
        verificar_clave = entry_verificar_clave_reg.get()
        estado = 1  # Asumimos que el estado es activo al registrar

        # Verifica que las claves coincidan
        if clave != verificar_clave:
            messagebox.showerror("Error", "Las claves no coinciden")
            return

        try:
            # Inserta los datos del nuevo usuario en la base de datos
            cursor.execute(
                "INSERT INTO USUARIO (Documento, NombreCompleto, Clave, Estado) VALUES (?, ?, ?, ?)",
                documento, nombre_completo, clave, estado
            )
            conn.commit()  # Guarda los cambios en la base de datos
            messagebox.showinfo("Registro", "Usuario registrado exitosamente")
            registro_ventana.destroy()  # Cierra la ventana de registro
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar usuario: {e}")

    # Botones para confirmar o cancelar el registro
    btn_confirmar = tk.Button(registro_ventana, text="Confirmar", command=registrar, font=font_style)
    btn_confirmar.grid(row=4, column=0, padx=10, pady=10)
    btn_cancelar = tk.Button(registro_ventana, text="Cancelar", command=registro_ventana.destroy, font=font_style)
    btn_cancelar.grid(row=4, column=1, padx=10, pady=10)

def acceder():
    # Obtiene los valores ingresados en los campos de entrada
    documento = entry_documento.get()
    clave = entry_clave.get()

    try:
        # Ejecuta una consulta para verificar el usuario y la clave
        cursor.execute(
            "SELECT * FROM USUARIO WHERE Documento = ? AND Clave = ?", documento, clave
        )
        usuario = cursor.fetchone()  # Obtiene el primer resultado de la consulta

        if usuario:
            messagebox.showinfo("Acceso", f"Bienvenido {usuario.NombreCompleto}")
            root.destroy()  # Cierra la ventana de login
            iniciar_menu()  # Abre el menú principal
        else:
            messagebox.showerror("Error", "Documento o clave incorrectos")
    except Exception as e:
        messagebox.showerror("Error", f"Error al acceder: {e}")

def salir():
    # Cierra la aplicación
    root.destroy()

# Interfaz gráfica principal
root = tk.Tk()
root.title("Sistema de Venta - Login")
root.geometry("400x300")
root.resizable(False, False)

# Cambiar el color de fondo de la ventana de inicio
root.configure(bg='black')

# Centrando la ventana en la pantalla
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height/2 - window_height/2)
position_right = int(screen_width/2 - window_width/2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Definir estilo de letra
font_style = font.Font(family='Cambria', size=12, weight='bold')

# Marco para centrar todos los elementos en la ventana principal
frame_center = tk.Frame(root, bg='black')
frame_center.place(relx=0.5, rely=0.5, anchor='center')

# Etiquetas y campos de entrada para el login
tk.Label(frame_center, text="Documento", bg='black', fg='white', font=font_style).grid(row=0, column=0, padx=10, pady=10)
tk.Label(frame_center, text="Clave", bg='black', fg='white', font=font_style).grid(row=1, column=0, padx=10, pady=10)
entry_documento = tk.Entry(frame_center, relief='solid', bd=2)
entry_documento.grid(row=0, column=1, padx=10, pady=10)
entry_clave = tk.Entry(frame_center, show='*', relief='solid', bd=2)
entry_clave.grid(row=1, column=1, padx=10, pady=10)

# Marco para los botones dentro del marco central
frame_buttons = tk.Frame(frame_center, bg='black')
frame_buttons.grid(row=2, columnspan=2, pady=20)

# Botones de la ventana principal
btn_registrar = tk.Button(frame_buttons, text="Registrar", command=abrir_ventana_registro, font=font_style)
btn_registrar.grid(row=0, column=0, padx=10)
btn_acceder = tk.Button(frame_buttons, text="Acceder", command=acceder, font=font_style)
btn_acceder.grid(row=0, column=1, padx=10)
btn_salir = tk.Button(frame_buttons, text="Salir", command=salir, font=font_style)
btn_salir.grid(row=0, column=2, padx=10)

root.mainloop()  # Inicia el bucle principal de la interfaz gráfica

# Cierra la conexión cuando la aplicación se cierra
conn.close()
