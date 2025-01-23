import tkinter as tk  # Importa el módulo tkinter para crear la interfaz gráfica
from tkinter import ttk, messagebox  # Importa ttk para widgets mejorados y messagebox para mostrar mensajes
import pyodbc  # Importa pyodbc para conectarse a bases de datos SQL
import requests  # Importa requests para hacer solicitudes HTTP
class ProductoApp:
    def __init__(self, root):
        self.root = root  # Almacena la referencia a la ventana principal
        self.root.title("Registro de Productos")  # Establece el título de la ventana
        
        # Configurar la ventana para pantalla completa
        self.root.attributes('-fullscreen', True)  # Habilita el modo de pantalla completa
        self.root.bind("<Escape>", self.toggle_fullscreen)  # Permite salir del modo de pantalla completa al presionar Esc

         # Conexión a la base de datos SQL Server
        try:
            self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                        'SERVER=DESKTOP-I7SFIUG;'
                                        'DATABASE=SISTEMA_VENTA_PYTHON;'
                                        'Trusted_Connection=yes;')  # Conecta a la base de datos
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")  # Muestra un error si la conexión falla
            self.root.quit()  # Cierra la aplicación si no se puede conectar

           # Frame de control superior
        control_frame = tk.Frame(root, bg='black')  # Crea un marco para los botones de control
        control_frame.pack(side=tk.TOP, fill=tk.X)  # Empaqueta el marco en la parte superior de la ventana

        # Botón para salir
        self.exit_button = tk.Button(control_frame, text="Salir", command=self.root.quit, bg='black', fg='white')  # Crea un botón para salir
        self.exit_button.pack(side=tk.RIGHT, padx=5)  # Empaqueta el botón en el lado derecho del marco

        # Botón para maximizar
        self.maximize_button = tk.Button(control_frame, text="Maximizar", command=self.toggle_fullscreen, bg='black', fg='white')  # Crea un botón para maximizar
        self.maximize_button.pack(side=tk.RIGHT, padx=5)  # Empaqueta el botón en el lado derecho del marco

         # Frame para el formulario
        self.form_frame = tk.Frame(root, bg='black')  # Crea un marco para el formulario de entrada de datos
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)  # Empaqueta el marco en el lado izquierdo

        # Título del formulario
        title_label = tk.Label(self.form_frame, text="Detalle Producto", bg='black', fg='white', font=("Arial", 16))  # Crea una etiqueta para el título
        title_label.pack(pady=10)  # Empaqueta la etiqueta con un espacio vertical

        # Entradas de datos
        tk.Label(self.form_frame, text="Codigo", bg='black', fg='white').pack(pady=5)  # Etiqueta para el código
        self.codigo_entry = tk.Entry(self.form_frame)  # Campo de entrada para el código
        self.codigo_entry.pack(pady=5)  # Empaqueta el campo de entrada

        tk.Label(self.form_frame, text="Nombre", bg='black', fg='white').pack(pady=5)  # Etiqueta para el nombre
        self.nombre_entry = tk.Entry(self.form_frame)  # Campo de entrada para el nombre
        self.nombre_entry.pack(pady=5)  # Empaqueta el campo de entrada

        tk.Label(self.form_frame, text="Descripcion", bg='black', fg='white').pack(pady=5)  # Etiqueta para la descripción
        self.descripcion_entry = tk.Entry(self.form_frame)  # Campo de entrada para la descripción
        self.descripcion_entry.pack(pady=5)  # Empaqueta el campo de entrada

        tk.Label(self.form_frame, text="Precio", bg='black', fg='white').pack(pady=5)  # Etiqueta para el precio
        self.precio_entry = tk.Entry(self.form_frame)  # Campo de entrada para el precio
        self.precio_entry.pack(pady=5)  # Empaqueta el campo de entrada

        tk.Label(self.form_frame, text="Stock", bg='black', fg='white').pack(pady=5)  # Etiqueta para el stock
        self.stock_entry = tk.Entry(self.form_frame)  # Campo de entrada para el stock
        self.stock_entry.pack(pady=5)  # Empaqueta el campo de entrada

        tk.Label(self.form_frame, text="Categoria", bg='black', fg='white').pack(pady=5)  # Etiqueta para la categoría
        self.categoria_var = tk.StringVar()  # Variable para almacenar la categoría seleccionada
        self.categoria_combo = ttk.Combobox(self.form_frame, textvariable=self.categoria_var, state="readonly")  # Combobox para seleccionar la categoría
        self.categoria_combo.pack(pady=5)  # Empaqueta el combobox
        self.load_categorias()  # Carga las categorías desde la base de dato

        tk.Label(self.form_frame, text="Estado", bg='black', fg='white').pack(pady=5)  # Etiqueta para el estado
        self.estado_var = tk.StringVar(value="Activo")  # Variable para el estado, por defecto "Activo"
        self.estado_combo = ttk.Combobox(self.form_frame, textvariable=self.estado_var, values=["Activo", "Inactivo"], state="readonly")  # Combobox para seleccionar el estado
        self.estado_combo.pack(pady=5)  # Empaqueta el combobox



    # Botones
        button_frame = tk.Frame(self.form_frame, bg='black')  # Crea un marco para los botones de acción
        button_frame.pack(pady=20)  # Empaqueta el marco con un espacio vertical

        self.save_button = tk.Button(button_frame, text="Guardar", command=self.save_producto, bg='green', fg='white')  # Botón para guardar un producto
        self.save_button.grid(row=0, column=0, padx=5)  # Coloca el botón en la cuadrícula

        self.edit_button = tk.Button(button_frame, text="Editar", command=self.edit_producto, bg='orange', fg='black')  # Botón para editar un producto
        self.edit_button.grid(row=0, column=1, padx=5)  # Coloca el botón en la cuadrícula

        self.delete_button = tk.Button(button_frame, text="Eliminar", command=self.delete_producto, bg='red', fg='white')  # Botón para eliminar un producto
        self.delete_button.grid(row=0, column=2, padx=5)  # Coloca el botón en la cuadrícula

        self.clear_button = tk.Button(button_frame, text="Limpiar", command=self.clear_form, bg='gray', fg='white')  # Botón para limpiar el formulario
        self.clear_button.grid(row=0, column=3, padx=5)  # Coloca el botón en la cuadrícula

        self.update_price_button = tk.Button(button_frame, text="Actualizar Precio", command=self.update_precio, bg='blue', fg='white')  # Botón para actualizar precios
        self.update_price_button.grid(row=0, column=4, padx=5)  # Coloca el botón en la cuadrícula



               # Frame de búsqueda
        search_frame = tk.Frame(root)  # Crea un marco para las funciones de búsqueda
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)  # Empaqueta el marco en la parte superior

        tk.Label(search_frame, text="Buscar por:", bg='black', fg='white').pack(side=tk.LEFT, padx=5)  # Etiqueta para la búsqueda
        self.search_column = ttk.Combobox(search_frame, values=["Codigo", "Nombre", "Descripcion", "Precio", "Stock", "Categoria"], state="readonly")  # Combobox para seleccionar la columna de búsqueda
        self.search_column.pack(side=tk.LEFT, padx=5)  # Empaqueta el combobox
        self.search_column.current(0)  # Establece el valor por defecto

        self.search_entry = tk.Entry(search_frame)  # Campo de entrada para el texto de búsqueda
        self.search_entry.pack(side=tk.LEFT, padx=5)  # Empaqueta el campo de entrada

        self.search_button = tk.Button(search_frame, text="Buscar", command=self.search_producto, bg='blue', fg='white')  # Botón para ejecutar la búsqueda
        self.search_button.pack(side=tk.LEFT, padx=5)  # Empaqueta el botón

        self.clear_search_button = tk.Button(search_frame, text="Limpiar", command=self.clear_search, bg='gray', fg='white')  # Botón para limpiar la búsqueda
        self.clear_search_button.pack(side=tk.LEFT, padx=5)  # Empaqueta el botón
 # Frame para la tabla
        self.table_frame = tk.Frame(root)  # Crea un marco para mostrar la tabla de productos
        self.table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)  # Empaqueta el marco en el lado derecho

        title_table = tk.Label(self.table_frame, text="Lista de Productos", font=("Arial", 16))  # Título de la tabla
        title_table.pack(pady=10)  # Empaqueta la etiqueta con un espacio vertical



         # Definir columnas de la tabla
        self.producto_tree = ttk.Treeview(self.table_frame, columns=("Codigo", "Nombre", "Descripcion", "Precio", "Stock", "Categoria", "Estado"), show='headings')  # Crea un Treeview para mostrar productos

        # Ajustar ancho de columnas
        self.producto_tree.column("Codigo", width=80)  # Ajusta el ancho de la columna Código
        self.producto_tree.column("Nombre", width=150)  # Ajusta el ancho de la columna Nombre
        self.producto_tree.column("Descripcion", width=200)  # Ajusta el ancho de la columna Descripción
        self.producto_tree.column("Precio", width=80)  # Ajusta el ancho de la columna Precio
        self.producto_tree.column("Stock", width=60)  # Ajusta el ancho de la columna Stock
        self.producto_tree.column("Categoria", width=100)  # Ajusta el ancho de la columna Categoría
        self.producto_tree.column("Estado", width=80)  # Ajusta el ancho de la columna Estado


        # Encabezados de columnas
        self.producto_tree.heading("Codigo", text="Codigo")  # Establece el encabezado para la columna Código
        self.producto_tree.heading("Nombre", text="Nombre")  # Establece el encabezado para la columna Nombre
        self.producto_tree.heading("Descripcion", text="Descripcion")  # Establece el encabezado para la columna Descripción
        self.producto_tree.heading("Precio", text="Precio")  # Establece el encabezado para la columna Precio
        self.producto_tree.heading("Stock", text="Stock")  # Establece el encabezado para la columna Stock
        self.producto_tree.heading("Categoria", text="Categoria")  # Establece el encabezado para la columna Categoría
        self.producto_tree.heading("Estado", text="Estado")  # Establece el encabezado para la columna Estado

        self.producto_tree.pack(fill=tk.BOTH, expand=True)  # Empaqueta el Treeview para que llene el espacio disponible

        self.producto_tree.bind('<Double-1>', self.load_producto)  # Asocia un evento de doble clic para cargar un producto
 # Cargar productos al iniciar
        self.load_productos()  # Llama a la función para cargar productos desde la base de datos

    def toggle_fullscreen(self, event=None):
        current_state = self.root.attributes("-fullscreen")  # Obtiene el estado actual de pantalla completa
        self.root.attributes("-fullscreen", not current_state)  # Cambia el estado de pantalla completa

    def load_categorias(self):
        cursor = self.conn.cursor()  # Crea un cursor para ejecutar consultas
        cursor.execute("SELECT IdCategoria, Descripcion FROM CATEGORIA WHERE Estado = 1")  # Consulta para obtener categorías activas
        self.categorias = cursor.fetchall()  # Guarda todas las categorías en una lista
        self.categoria_combo['values'] = [f"{row.IdCategoria}: {row.Descripcion}" for row in self.categorias]  # Establece las categorías en el combobox

    def load_productos(self):
        # Limpiar el Treeview
        for item in self.producto_tree.get_children():  # Itera sobre todos los elementos en el Treeview
            self.producto_tree.delete(item)  # Elimina cada elemento

         # Cargar productos de la base de datos
        cursor = self.conn.cursor()  # Crea un cursor para ejecutar consultas
        cursor.execute("SELECT Codigo, Nombre, Descripcion, Precio, Stock, IdCategoria, Estado FROM PRODUCTO")  # Consulta para obtener productos
        productos = cursor.fetchall()  # Guarda todos los productos en una lista
        
         # Usar un conjunto para verificar duplicados
        seen = set()  # Conjunto para rastrear productos ya vistos
        
        for row in productos:
            if row[0] not in seen:  # Solo agregar productos no vistos
                seen.add(row[0])  # Agrega el código del producto al conjunto
                categoria_descripcion = next((cat[1] for cat in self.categorias if cat[0] == row[5]), "Desconocida")  # Obtiene la descripción de la categoría
                estado = "Activo" if row[6] else "Inactivo"  # Determina el estado del producto
                self.producto_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], categoria_descripcion, estado))  # Inserta el producto en el Treeview
                
                
                #Actualizacion al precio dolar
    def update_precio(self):
        try:
            response = requests.get("https://dolarapi.com/v1/dolares/oficial")  # Realiza una solicitud para obtener el precio oficial del dólar
            data = response.json()  # Convierte la respuesta a formato JSON
            oficial_price = data['venta']  # Extrae el precio de venta

            for item in self.producto_tree.get_children():  # Itera sobre los productos en el Treeview
                values = self.producto_tree.item(item)['values']  # Obtiene los valores del producto
                current_price = float(values[3])  # Convierte el precio actual a float
                new_price = current_price * oficial_price / 1061.5  # Calcula el nuevo precio con el tipo de cambio
                
                # Actualizar el precio en la base de datos
                cursor = self.conn.cursor()  # Crea un cursor para ejecutar consultas
                cursor.execute("UPDATE PRODUCTO SET Precio=? WHERE Codigo=?", (round(new_price, 2), values[0]))  # Actualiza el precio del producto
                self.conn.commit()  # Confirma la transacción

                self.producto_tree.item(item, values=(values[0], values[1], values[2], round(new_price, 2), values[4], values[5], values[6]))  # Actualiza el Treeview con el nuevo precio

            messagebox.showinfo("Actualizar Precio", "Precios actualizados según el valor del dólar.")  # Muestra un mensaje de éxito
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar los precios: {e}")  # Muestra un error si la actualización falla



    def save_producto(self):
        codigo = self.codigo_entry.get()  # Obtiene el código del producto del campo de entrada
        nombre = self.nombre_entry.get()  # Obtiene el nombre del producto del campo de entrada
        descripcion = self.descripcion_entry.get()  # Obtiene la descripción del producto del campo de entrada

        # Verificar que Precio y Stock sean números
        try:
            precio = float(self.precio_entry.get())  # Convierte el precio a float
            stock = int(self.stock_entry.get())  # Convierte el stock a int
        except ValueError:
            messagebox.showwarning("Advertencia", "Precio y Stock deben ser números.")  # Muestra un aviso si la conversión falla
            return


      
        try:
            categoria_id = int(self.categoria_var.get().split(":")[0])  # Extrae el IdCategoria del combobox
        except (IndexError, ValueError):
            messagebox.showwarning("Advertencia", "Seleccione una categoría válida.")  # Muestra un aviso si no se selecciona una categoría válida
            return

        estado = self.estado_var.get()  # Obtiene el estado seleccionado

        if not (codigo and nombre and descripcion):  # Verifica que todos los campos obligatorios estén llenos
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")  # Muestra un aviso si faltan campos
            return

        try:
            cursor = self.conn.cursor()  # Crea un cursor para ejecutar consultas

            # Verificar si el producto ya existe
            cursor.execute("SELECT COUNT(*) FROM PRODUCTO WHERE Codigo=?", (codigo,))  # Consulta para verificar existencia
            exists = cursor.fetchone()[0]  # Obtiene el conteo

            if exists:
                # Actualizar el producto existente
                cursor.execute("UPDATE PRODUCTO SET Nombre=?, Descripcion=?, Precio=?, Stock=?, IdCategoria=?, Estado=? WHERE Codigo=?",
                               (nombre, descripcion, precio, stock, categoria_id, estado == "Activo", codigo))  # Actualiza el producto
                messagebox.showinfo("Editar", "Producto actualizado exitosamente.")  # Muestra un mensaje de éxito
            else:
                # Insertar un nuevo producto
                cursor.execute("INSERT INTO PRODUCTO (Codigo, Nombre, Descripcion, Precio, Stock, IdCategoria, Estado) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (codigo, nombre, descripcion, precio, stock, categoria_id, estado == "Activo"))  # Inserta un nuevo producto
                messagebox.showinfo("Guardar", "Producto guardado exitosamente.")  # Muestra un mensaje de éxito

            self.update_precio()
            self.conn.commit()  # Confirma la transacción
            self.clear_form()  # Limpia el formulario

            self.load_productos()  
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto: {e}")
            
# Función que carga los datos de un producto seleccionado en los campos de entrada para su visualización
    def load_producto(self, event):
        selected_item = self.producto_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un producto para cargar.")
            return
        selected_item = selected_item[0]
        item = self.producto_tree.item(selected_item)
        values = item['values']
          # Inserta el código del producto en el campo correspondiente
        self.codigo_entry.delete(0, tk.END)
        self.codigo_entry.insert(0, values[0])
        # Inserta el nombre del producto en el campo correspondiente
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, values[1])
        # Inserta la descripción del producto en el campo correspondiente
        self.descripcion_entry.delete(0, tk.END)
        self.descripcion_entry.insert(0, values[2])
        # Inserta el precio del producto en el campo correspondiente
        self.precio_entry.delete(0, tk.END)
        self.precio_entry.insert(0, values[3])
        # Inserta el stock del producto en el campo correspondiente
        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, values[4])
        # Configura la categoría seleccionada en el combo box
        self.categoria_combo.set(f"{values[5]}: {values[5]}")
        # Configura el estado del producto en el combo box
        self.estado_combo.set("Activo" if values[6] == "Activo" else "Inactivo")
        
     # Función que permite editar un producto seleccionado
    def edit_producto(self):
        selected_item = self.producto_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar.")
            return
        
        selected_item = selected_item[0]
        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()

         # Verifica que el precio y el stock sean números válidos

        try:
            precio = float(self.precio_entry.get())
            stock = int(self.stock_entry.get())
        except ValueError:
            messagebox.showwarning("Advertencia", "Precio y Stock deben ser números.")
            return

        # Asegura que el IdCategoria sea un entero válido
        try:
            categoria_id = int(self.categoria_var.get().split(":")[0])  # Extraer IdCategoria
        except (IndexError, ValueError):
            messagebox.showwarning("Advertencia", "Seleccione una categoría válida.")
            return

        estado = self.estado_var.get()

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE PRODUCTO SET Nombre=?, Descripcion=?, Precio=?, Stock=?, IdCategoria=?, Estado=? WHERE Codigo=?",
                           (nombre, descripcion, precio, stock, categoria_id, estado == "Activo", codigo))
            self.conn.commit()
            messagebox.showinfo("Editar", "Producto actualizado exitosamente.")
            self.clear_form()
            self.load_productos()  # Asegúrate de que esto esté aquí
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar el producto: {e}")
            
    # Función que elimina un producto seleccionado
    def delete_producto(self):
        selected_item = self.producto_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
            return
        
        selected_item = selected_item[0]
        item = self.producto_tree.item(selected_item)
        cursor = self.conn.cursor()
        
         # Elimina el producto de la base de datos
        cursor.execute("DELETE FROM PRODUCTO WHERE Codigo=?", (item['values'][0],))
        self.conn.commit()
        messagebox.showinfo("Eliminar", "Producto eliminado exitosamente.")
        self.clear_form()
        self.load_productos()  

    
     # Función que realiza una búsqueda de productos en la base de datos

    def search_producto(self):
        search_text = self.search_entry.get()
        column = self.search_column.get()

        if not search_text:
            messagebox.showwarning("Advertencia", "Ingrese texto para buscar.")
            return

        # Limpia el Treeview antes de buscar
        for item in self.producto_tree.get_children():
            self.producto_tree.delete(item)

        cursor = self.conn.cursor()
        query = f"SELECT Codigo, Nombre, Descripcion, Precio, Stock, IdCategoria, Estado FROM PRODUCTO WHERE {column} LIKE ?"
        cursor.execute(query, ('%' + search_text + '%',))
        productos = cursor.fetchall()
        
        # Usar un conjunto para verificar duplicados
        seen = set()
        
        for row in productos:
            if row[0] not in seen:  # Solo agregar productos no vistos
                seen.add(row[0])
                categoria_descripcion = next((cat[1] for cat in self.categorias if cat[0] == row[5]), "Desconocida")
                estado = "Activo" if row[6] else "Inactivo"
                self.producto_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], categoria_descripcion, estado))
    
    # Función que limpia el campo de búsqueda y vuelve a cargar todos los productos en la interfaz
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_productos()

# Función que limpia todos los campos del formulario de entrada de datos
    def clear_form(self):
        self.codigo_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.categoria_combo.set('')
        self.estado_combo.set("Activo")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductoApp(root)
    root.mainloop()