import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

class CategoriaApp:
    def __init__(self, root):
        # Inicializa la ventana principal y configura su título y tamaño
        self.root = root
        self.root.title("Gestión de Categorías")
        self.root.geometry("800x600")

        # Conexión a la base de datos SQL Server
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                    'SERVER=DESKTOP-I7SFIUG;'
                                    'DATABASE=SISTEMA_VENTA_PYTHON;'
                                    'Trusted_Connection=yes;')

        # Tamaño de la ventana
        window_width = 800
        window_height = 600

        # Obtener las dimensiones de la pantalla para centrar la ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcular la posición x, y para centrar la ventana
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Ajustar la geometría de la ventana
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # Frame para el formulario
        self.form_frame = tk.Frame(root, bg='black')
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        # Título del formulario
        title_label = tk.Label(self.form_frame, text="Detalle Categoría", bg='black', fg='white', font=("Arial", 16))
        title_label.pack(pady=10)

        # Campo de entrada para la descripción
        tk.Label(self.form_frame, text="Descripción", bg='black', fg='white').pack(pady=5)
        self.description_entry = tk.Entry(self.form_frame)
        self.description_entry.pack(pady=5)

        # Campo de selección para el estado (Activo/Inactivo)
        tk.Label(self.form_frame, text="Estado", bg='black', fg='white').pack(pady=5)
        self.estado_var = tk.StringVar(value="Activo")
        self.estado_combo = ttk.Combobox(self.form_frame, textvariable=self.estado_var, values=["Activo", "Inactivo"], state="readonly")
        self.estado_combo.pack(pady=5)

        # Botones para guardar, editar, eliminar, limpiar y salir
        button_frame = tk.Frame(self.form_frame, bg='black')
        button_frame.pack(pady=20)

        self.save_button = tk.Button(button_frame, text="Guardar", command=self.save_categoria, bg='green', fg='white')
        self.save_button.grid(row=0, column=0, padx=5)

        self.edit_button = tk.Button(button_frame, text="Editar", command=self.edit_categoria, bg='orange', fg='black')
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(button_frame, text="Eliminar", command=self.delete_categoria, bg='red', fg='white')
        self.delete_button.grid(row=0, column=2, padx=5)

        self.clear_button = tk.Button(button_frame, text="Limpiar", command=self.clear_form, bg='gray', fg='white')
        self.clear_button.grid(row=0, column=3, padx=5)

        self.exit_button = tk.Button(button_frame, text="Salir", command=self.root.quit, bg='black', fg='white')
        self.exit_button.grid(row=0, column=4, padx=5)

        # Frame para la tabla de categorías
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_table = tk.Label(self.table_frame, text="Lista de Categorías", font=("Arial", 16))
        title_table.pack(pady=10)

        # Configuración de la tabla (Treeview) para mostrar las categorías
        self.categoria_tree = ttk.Treeview(self.table_frame, columns=("IdCategoria", "Descripción", "Estado"), show='headings')
        self.categoria_tree.heading("IdCategoria", text="ID")
        self.categoria_tree.heading("Descripción", text="Descripción")
        self.categoria_tree.heading("Estado", text="Estado")
        self.categoria_tree.pack(fill=tk.BOTH, expand=True)

        # Enlaza el evento de doble clic para cargar la categoría seleccionada
        self.categoria_tree.bind('<Double-1>', self.load_categoria)

        # Campo de búsqueda
        search_frame = tk.Frame(self.table_frame)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Buscar por:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(search_frame, text="Buscar", command=self.search_categoria, bg='blue', fg='white')
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.clear_search_button = tk.Button(search_frame, text="Limpiar", command=self.clear_search, bg='gray', fg='white')
        self.clear_search_button.pack(side=tk.LEFT, padx=5)

        # Carga las categorías al inicio
        self.load_categorias()

    def load_categorias(self):
        """Carga las categorías de la base de datos en la tabla."""
        for row in self.categoria_tree.get_children():
            self.categoria_tree.delete(row)  # Limpia la tabla
        cursor = self.conn.cursor()
        cursor.execute("SELECT IdCategoria, Descripcion, Estado FROM CATEGORIA")
        for categoria in cursor.fetchall():
            estado = "Activo" if categoria[2] else "Inactivo"
            self.categoria_tree.insert("", "end", values=(categoria[0], categoria[1], estado))  # Inserta los datos

    def save_categoria(self):
        """Guarda una nueva categoría en la base de datos."""
        description = self.description_entry.get()
        estado = 1 if self.estado_var.get() == "Activo" else 0
        if description:
            try:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO CATEGORIA (Descripcion, Estado) VALUES (?, ?)", (description, estado))
                self.conn.commit()
                self.load_categorias()  # Recarga las categorías
                self.clear_form()  # Limpia el formulario
                print("Categoría guardada.")
            except Exception as e:
                messagebox.showerror("Error", str(e))  # Muestra error si falla
        else:
            messagebox.showwarning("Advertencia", "La descripción no puede estar vacía.")

    def edit_categoria(self):
        """Edita la categoría seleccionada en la base de datos."""
        selected_item = self.categoria_tree.selection()
        if selected_item:
            categoria_id = self.categoria_tree.item(selected_item)['values'][0]
            description = self.description_entry.get()
            estado = 1 if self.estado_var.get() == "Activo" else 0
            if description:
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("UPDATE CATEGORIA SET Descripcion = ?, Estado = ? WHERE IdCategoria = ?", (description, estado, categoria_id))
                    self.conn.commit()
                    self.load_categorias()  # Recarga las categorías
                    self.clear_form()  # Limpia el formulario
                    print("Categoría editada.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))  # Muestra error si falla
            else:
                messagebox.showwarning("Advertencia", "La descripción no puede estar vacía.")
        else:
            messagebox.showwarning("Advertencia", "Selecciona una categoría para editar.")

    def load_categoria(self, event):
        """Carga la categoría seleccionada en el formulario para editarla."""
        selected_item = self.categoria_tree.selection()[0]  # Obtiene el item seleccionado
        categoria = self.categoria_tree.item(selected_item)['values']
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, categoria[1])  # Carga la descripción
        self.estado_var.set("Activo" if categoria[2] == "Activo" else "Inactivo")  # Carga el estado

    def delete_categoria(self):
        """Elimina la categoría seleccionada de la base de datos."""
        selected_item = self.categoria_tree.selection()
        if selected_item:
            categoria_id = self.categoria_tree.item(selected_item)['values'][0]
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM CATEGORIA WHERE IdCategoria = ?", (categoria_id,))
                self.conn.commit()
                self.load_categorias()  # Recarga las categorías
                print("Categoría eliminada.")
            except Exception as e:
                messagebox.showerror("Error", str(e))  # Muestra error si falla
        else:
            messagebox.showwarning("Advertencia", "Selecciona una categoría para eliminar.")

    def search_categoria(self):
        """Busca categorías en la base de datos según el término de búsqueda."""
        search_term = self.search_entry.get()
        for row in self.categoria_tree.get_children():
            self.categoria_tree.delete(row)  # Limpia la tabla
        cursor = self.conn.cursor()
        cursor.execute("SELECT IdCategoria, Descripcion, Estado FROM CATEGORIA WHERE Descripcion LIKE ?", ('%' + search_term + '%',))
        for categoria in cursor.fetchall():
            estado = "Activo" if categoria[2] else "Inactivo"
            self.categoria_tree.insert("", "end", values=(categoria[0], categoria[1], estado))  # Inserta los resultados

    def clear_search(self):
        """Limpia el campo de búsqueda y recarga todas las categorías."""
        self.search_entry.delete(0, tk.END)
        self.load_categorias()

    def clear_form(self):
        """Limpia el formulario de entrada."""
        self.description_entry.delete(0, tk.END)
        self.estado_var.set("Activo")  # Restablece el estado a 'Activo'

if __name__ == "__main__":
    root = tk.Tk()
    app = CategoriaApp(root)  # Crea una instancia de la aplicación
    root.mainloop()  # Inicia el bucle principal de la interfaz