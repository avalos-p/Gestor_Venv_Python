import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from pathlib import Path

from src_gestor.proyectos import GestorProyectos
from src_gestor.entornos import GestorEntornos

"""
Interfaz Gráfica del Gestor de Entornos Virtuales, con ventana principal y los componentes visuales
"""

class GestorInterfaz:
    """Interfaz gráfica principal"""

    def __init__(self):
        self.ventana = tk.Tk()
        self.configurar_ventana()

        # Variables de estado
        self.proyecto_actual = tk.StringVar()
        self.entorno_actual = tk.StringVar()
        self.libreria_a_instalar = tk.StringVar()

        # Inicializa los gestores
        self.directorio_base = Path.cwd()
        self.gestor_proyectos = GestorProyectos(self.directorio_base)
        self.gestor_entornos = GestorEntornos(
            self.gestor_proyectos.directorio_proyectos,
            self.escribir_en_consola,
            self.cambiar_estado
        )

        # Para seguimiento responsive
        self.ancho_ventana = 1100
        self.alto_ventana = 750
        self.modo_compacto = False

        # Configurar la interfaz
        self.crear_interfaz()
        self.actualizar_proyectos()

    def configurar_ventana(self):
        """Configura las propiedades básicas de la ventana"""
        self.ventana.title("Gestor de Entornos Virtuales Python")
        self.ventana.geometry("1100x750")
        self.ventana.configure(bg='#f5f5f5')
        self.ventana.minsize(800, 600)

        # Permite que la ventana se redimensione
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)

        # Detecta cuando se redimensiona la ventana
        self.ventana.bind('<Configure>', self.al_redimensionar)

    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        self.configurar_estilos()
        self.crear_contenedor_principal()
        self.crear_encabezado()
        self.crear_seccion_proyectos()
        self.crear_seccion_estado()
        self.crear_seccion_entornos()
        self.crear_seccion_librerias()
        self.crear_consola()
        self.crear_barra_estado()

    def configurar_estilos(self):
        """Define los estilos visuales de la aplicación"""
        estilo = ttk.Style()
        estilo.theme_use('clam')

        # Colores y fuentes del tema
        estilo.configure('Titulo.TLabel', font=('Segoe UI', 18, 'bold'), foreground='#2c3e50')
        estilo.configure('Encabezado.TLabel', font=('Segoe UI', 11, 'bold'), foreground='#34495e')
        estilo.configure('Estado.TLabel', font=('Segoe UI', 9), foreground='#7f8c8d')
        estilo.configure('Activo.TLabel', font=('Segoe UI', 9, 'bold'), foreground='#27ae60')
        estilo.configure('Inactivo.TLabel', font=('Segoe UI', 9), foreground='#e74c3c')
        estilo.configure('Boton.TButton', font=('Segoe UI', 9), padding=6)
        estilo.configure('BotonAccion.TButton', font=('Segoe UI', 10, 'bold'))
        estilo.configure('Tarjeta.TLabelframe', background='#ffffff', borderwidth=1, relief='solid')
        estilo.configure('Tarjeta.TLabelframe.Label', font=('Segoe UI', 10, 'bold'), foreground='#2c3e50')

    def crear_contenedor_principal(self):
        """Crea el contenedor principal con scroll"""
        # Canvas principal con barras de desplazamiento
        self.canvas_principal = tk.Canvas(self.ventana, bg='#f5f5f5', highlightthickness=0)
        barra_vertical = ttk.Scrollbar(self.ventana, orient="vertical", command=self.canvas_principal.yview)
        barra_horizontal = ttk.Scrollbar(self.ventana, orient="horizontal", command=self.canvas_principal.xview)
        self.marco_desplazable = ttk.Frame(self.canvas_principal)

        # Función para actualizar el área de scroll
        def configurar_scroll(event=None):
            self.canvas_principal.configure(scrollregion=self.canvas_principal.bbox("all"))
            ancho_canvas = self.canvas_principal.winfo_width()
            if ancho_canvas > 1:
                self.canvas_principal.itemconfig(self.ventana_canvas, width=ancho_canvas)

        self.marco_desplazable.bind("<Configure>", configurar_scroll)

        # Crea la ventana dentro del canvas
        self.ventana_canvas = self.canvas_principal.create_window((0, 0), window=self.marco_desplazable, anchor="nw")
        self.canvas_principal.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)

        # Manejo del redimensionado del canvas
        def al_configurar_canvas(event):
            ancho_canvas = event.width
            self.canvas_principal.itemconfig(self.ventana_canvas, width=ancho_canvas)
            configurar_scroll()

        self.canvas_principal.bind('<Configure>', al_configurar_canvas)

        # Posiciona canvas y barras de scroll
        self.canvas_principal.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        # Configura las proporciones
        self.ventana.grid_rowconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)

        # Soporte para rueda del ratón
        def con_rueda(event):
            delta = event.delta
            if delta == 0 and event.num in (4, 5):  # Sistema X11
                delta = 120 if event.num == 4 else -120
            self.canvas_principal.yview_scroll(int(-1*(delta/120)), "units")

        def con_rueda_horizontal(event):
            delta = event.delta
            if delta == 0 and event.num in (4, 5):
                delta = 120 if event.num == 4 else -120
            self.canvas_principal.xview_scroll(int(-1*(delta/120)), "units")

        self.canvas_principal.bind_all("<MouseWheel>", con_rueda)
        self.canvas_principal.bind_all("<Button-4>", con_rueda)
        self.canvas_principal.bind_all("<Button-5>", con_rueda)
        self.canvas_principal.bind_all("<Shift-MouseWheel>", con_rueda_horizontal)

        # Configura el marco principal
        self.marco_desplazable.columnconfigure(0, weight=1)
        self.marco_desplazable.rowconfigure(0, weight=1)

        self.contenedor = ttk.Frame(self.marco_desplazable, padding="20")
        self.contenedor.grid(row=0, column=0, sticky="nsew")
        self.contenedor.columnconfigure(0, weight=1)

        self.configurar_proporciones()

    def configurar_proporciones(self):
        """Configura las proporciones de las secciones según el modo"""
        if self.modo_compacto:
            # En modo compacto, más espacio para proyectos, menos para consola
            self.contenedor.rowconfigure(2, weight=3)  # Proyectos
            self.contenedor.rowconfigure(3, weight=1)  # Estado
            self.contenedor.rowconfigure(4, weight=1)  # Entornos
            self.contenedor.rowconfigure(5, weight=1)  # Librerías
            self.contenedor.rowconfigure(6, weight=2)  # Consola
        else:
            # Modo normal
            self.contenedor.rowconfigure(2, weight=2)  # Proyectos
            self.contenedor.rowconfigure(3, weight=1)  # Estado
            self.contenedor.rowconfigure(4, weight=1)  # Entornos
            self.contenedor.rowconfigure(5, weight=1)  # Librerías
            self.contenedor.rowconfigure(6, weight=3)  # Consola

    def crear_encabezado(self):
        """Crea la sección del encabezado"""
        marco_encabezado = ttk.Frame(self.contenedor)
        marco_encabezado.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        marco_encabezado.columnconfigure(1, weight=1)

        titulo = ttk.Label(marco_encabezado, text="🐍 Gestor de Entornos Virtuales", style='Titulo.TLabel')
        titulo.grid(row=0, column=0, sticky="w")

        subtitulo = ttk.Label(marco_encabezado, text=f"📁 {self.directorio_base}", style='Estado.TLabel')
        subtitulo.grid(row=1, column=0, sticky="w", pady=(5, 0))

        ttk.Separator(self.contenedor, orient='horizontal').grid(row=1, column=0, sticky='ew', pady=(0, 20))

    def crear_seccion_proyectos(self):
        """Crea la sección de gestión de proyectos"""
        tarjeta_proyectos = ttk.LabelFrame(self.contenedor, text="  📂 Proyectos  ", style='Tarjeta.TLabelframe', padding=15)
        tarjeta_proyectos.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        tarjeta_proyectos.columnconfigure(0, weight=1)
        tarjeta_proyectos.rowconfigure(1, weight=1)

        # Formulario para crear proyecto
        marco_crear = ttk.Frame(tarjeta_proyectos)
        marco_crear.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        marco_crear.columnconfigure(1, weight=1)

        ttk.Label(marco_crear, text="Nuevo proyecto:", style='Encabezado.TLabel').grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.entrada_proyecto = ttk.Entry(marco_crear, font=('Segoe UI', 10))
        self.entrada_proyecto.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        ttk.Button(marco_crear, text="+ Crear", command=self.crear_proyecto, style='BotonAccion.TButton').grid(row=0, column=2, sticky="e")

        # Árbol de proyectos
        marco_arbol = ttk.Frame(tarjeta_proyectos)
        marco_arbol.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        marco_arbol.columnconfigure(0, weight=1)
        marco_arbol.rowconfigure(0, weight=1)

        scroll_arbol = ttk.Scrollbar(marco_arbol, orient="vertical")
        scroll_arbol.grid(row=0, column=1, sticky="ns")

        self.arbol_proyectos = ttk.Treeview(marco_arbol, yscrollcommand=scroll_arbol.set)
        self.arbol_proyectos.grid(row=0, column=0, sticky="nsew")
        scroll_arbol.config(command=self.arbol_proyectos.yview)

        self.arbol_proyectos.heading('#0', text='Estructura de Proyectos → Entornos Virtuales')
        self.arbol_proyectos.bind('<<TreeviewSelect>>', self.al_seleccionar_arbol)

        # Botones de acción
        marco_acciones = ttk.Frame(tarjeta_proyectos)
        marco_acciones.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        marco_acciones.columnconfigure((0,1,2,3), weight=1)

        self.botones_accion = {
            'eliminar': ttk.Button(marco_acciones, text="🗑️ Eliminar", command=self.eliminar_seleccionado, style='Boton.TButton'),
            'actualizar': ttk.Button(marco_acciones, text="🔄 Actualizar", command=self.actualizar_proyectos, style='Boton.TButton'),
            'carpeta': ttk.Button(marco_acciones, text="📁 Abrir Carpeta", command=self.abrir_carpeta, style='Boton.TButton'),
            'terminal': ttk.Button(marco_acciones, text="💻 Terminal", command=self.abrir_terminal, style='Boton.TButton')
        }

        self.botones_accion['eliminar'].grid(row=0, column=0, padx=(0,5), sticky="ew")
        self.botones_accion['actualizar'].grid(row=0, column=1, padx=(0,5), sticky="ew")
        self.botones_accion['carpeta'].grid(row=0, column=2, padx=(0,5), sticky="ew")
        self.botones_accion['terminal'].grid(row=0, column=3, sticky="ew")

    def crear_seccion_estado(self):
        """Crea la sección de estado actual"""
        tarjeta_estado = ttk.LabelFrame(self.contenedor, text="  🎯 Selección Actual  ", style='Tarjeta.TLabelframe', padding=15)
        tarjeta_estado.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        tarjeta_estado.columnconfigure(1, weight=1)

        ttk.Label(tarjeta_estado, text="Proyecto:", style='Encabezado.TLabel').grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.etiqueta_proyecto = ttk.Label(tarjeta_estado, text="Ninguno", style='Inactivo.TLabel')
        self.etiqueta_proyecto.grid(row=0, column=1, sticky="w")

        ttk.Label(tarjeta_estado, text="Entorno:", style='Encabezado.TLabel').grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(5, 0))
        self.etiqueta_entorno = ttk.Label(tarjeta_estado, text="Ninguno", style='Inactivo.TLabel')
        self.etiqueta_entorno.grid(row=1, column=1, sticky="w", pady=(5, 0))

    def crear_seccion_entornos(self):
        """Crea la sección de gestión de entornos virtuales"""
        tarjeta_entornos = ttk.LabelFrame(self.contenedor, text="  🐍 Entornos Virtuales  ", style='Tarjeta.TLabelframe', padding=15)
        tarjeta_entornos.grid(row=4, column=0, sticky="ew", pady=(0, 15))
        tarjeta_entornos.columnconfigure(1, weight=1)

        marco_crear_venv = ttk.Frame(tarjeta_entornos)
        marco_crear_venv.grid(row=0, column=0, sticky="ew")
        marco_crear_venv.columnconfigure(1, weight=1)

        ttk.Label(marco_crear_venv, text="Nuevo entorno:", style='Encabezado.TLabel').grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.entrada_entorno = ttk.Entry(marco_crear_venv, font=('Segoe UI', 10))
        self.entrada_entorno.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        ttk.Button(marco_crear_venv, text="+ Crear Entorno", command=self.crear_entorno, style='BotonAccion.TButton').grid(row=0, column=2, sticky="e")

    def crear_seccion_librerias(self):
        """Crea la sección de gestión de librerías"""
        tarjeta_libs = ttk.LabelFrame(self.contenedor, text="  📦 Gestión de Librerías  ", style='Tarjeta.TLabelframe', padding=15)
        tarjeta_libs.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        tarjeta_libs.columnconfigure(1, weight=1)

        # Formulario para instalar librería
        marco_instalar = ttk.Frame(tarjeta_libs)
        marco_instalar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        marco_instalar.columnconfigure(1, weight=1)

        ttk.Label(marco_instalar, text="Instalar:", style='Encabezado.TLabel').grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.entrada_libreria = ttk.Entry(marco_instalar, width=30, font=('Segoe UI', 10), textvariable=self.libreria_a_instalar)
        self.entrada_libreria.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        ttk.Button(marco_instalar, text="📥 Instalar", command=self.instalar_libreria, style='BotonAccion.TButton').grid(row=0, column=2, sticky="e")

        # Botones para requirements
        marco_req = ttk.Frame(tarjeta_libs)
        marco_req.grid(row=1, column=0, sticky="ew")
        marco_req.columnconfigure((0,1,2), weight=1)

        self.botones_req = {
            'desde_req': ttk.Button(marco_req, text="📄 Desde requirements.txt", command=self.instalar_desde_requirements, style='Boton.TButton'),
            'crear_req': ttk.Button(marco_req, text="💾 Crear requirements.txt", command=self.crear_requirements, style='Boton.TButton'),
            'ver_paquetes': ttk.Button(marco_req, text="📋 Ver instaladas", command=self.mostrar_paquetes, style='Boton.TButton')
        }

        self.botones_req['desde_req'].grid(row=0, column=0, padx=(0, 5), sticky="ew")
        self.botones_req['crear_req'].grid(row=0, column=1, padx=(0, 5), sticky="ew")
        self.botones_req['ver_paquetes'].grid(row=0, column=2, sticky="ew")

    def crear_consola(self):
        """Crea la consola de salida"""
        tarjeta_consola = ttk.LabelFrame(self.contenedor, text="  🖥️ Consola  ", style='Tarjeta.TLabelframe', padding=15)
        tarjeta_consola.grid(row=6, column=0, sticky="nsew", pady=(0, 15))
        tarjeta_consola.columnconfigure(0, weight=1)
        tarjeta_consola.rowconfigure(0, weight=1)

        # Área de texto de la consola
        self.salida_consola = scrolledtext.ScrolledText(
            tarjeta_consola,
            wrap=tk.WORD,
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white',
            selectbackground='#404040',
            font=('Consolas', 9),
            relief=tk.FLAT,
            borderwidth=0
        )
        self.salida_consola.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Configurar colores para diferentes tipos de mensaje
        self.salida_consola.tag_configure("exito", foreground="#4ade80")
        self.salida_consola.tag_configure("error", foreground="#f87171")
        self.salida_consola.tag_configure("advertencia", foreground="#fbbf24")
        self.salida_consola.tag_configure("info", foreground="#60a5fa")
        self.salida_consola.tag_configure("comando", foreground="#a78bfa")

        # Mensaje inicial
        self.salida_consola.insert(tk.END, "Gestor iniciado - Listo para usar\n", "exito")
        self.salida_consola.insert(tk.END, f"📁 Base: {self.directorio_base}\n", "info")
        self.salida_consola.insert(tk.END, f"📂 Proyectos: {self.gestor_proyectos.directorio_proyectos}\n\n", "info")
        self.salida_consola.config(state=tk.DISABLED)

        # Botones de la consola
        marco_botones_consola = ttk.Frame(tarjeta_consola)
        marco_botones_consola.grid(row=1, column=0, sticky="ew")

        ttk.Button(marco_botones_consola, text=" Limpiar", command=self.limpiar_consola, style='Boton.TButton').grid(row=0, column=0, padx=(0, 5), sticky="w")
        ttk.Button(marco_botones_consola, text=" Guardar Log", command=self.guardar_log, style='Boton.TButton').grid(row=0, column=1, sticky="w")

    def crear_barra_estado(self):
        """Crea la barra de estado en la parte inferior"""
        self.variable_estado = tk.StringVar(value="✅ Listo")
        barra_estado = ttk.Label(self.contenedor, textvariable=self.variable_estado, style='Estado.TLabel', relief=tk.SUNKEN, padding=(10, 5))
        barra_estado.grid(row=7, column=0, sticky="ew", pady=(15, 0))

    # Métodos para manejar eventos de la interfaz

    def al_redimensionar(self, event):
        """Maneja el evento de redimensionado de ventana"""
        if event.widget != self.ventana:
            return

        nuevo_ancho = event.width
        nuevo_alto = event.height

        # Evita procesar cambios muy pequeños
        if abs(nuevo_ancho - self.ancho_ventana) < 10 and abs(nuevo_alto - self.alto_ventana) < 10:
            return

        self.ancho_ventana = nuevo_ancho
        self.alto_ventana = nuevo_alto

        # Determina si debe cambiar a modo compacto
        modo_anterior = self.modo_compacto
        self.modo_compacto = nuevo_ancho < 950 or nuevo_alto < 700

        # Solo actualiza si cambió el modo
        if modo_anterior != self.modo_compacto:
            self.actualizar_modo_responsive()

    def actualizar_modo_responsive(self):
        """Actualiza la interfaz según el modo responsive"""
        self.configurar_proporciones()

        if self.modo_compacto:
            self.aplicar_textos_compactos()
            try:
                self.salida_consola.configure(height=8)
            except:
                pass
        else:
            self.aplicar_textos_normales()
            try:
                self.salida_consola.configure(height=12)
            except:
                pass

        self.actualizar_region_scroll()

    def aplicar_textos_compactos(self):
        """Aplica textos cortos para modo compacto"""
        try:
            self.botones_accion['eliminar'].config(text="🗑️")
            self.botones_accion['actualizar'].config(text="🔄")
            self.botones_accion['carpeta'].config(text="📁")
            self.botones_accion['terminal'].config(text="💻")

            self.botones_req['desde_req'].config(text="📄 Desde req.")
            self.botones_req['crear_req'].config(text="💾 Crear req.")
            self.botones_req['ver_paquetes'].config(text="📋 Ver paquetes")
        except:
            pass

    def aplicar_textos_normales(self):
        """Aplica textos completos para modo normal"""
        try:
            self.botones_accion['eliminar'].config(text="🗑️ Eliminar")
            self.botones_accion['actualizar'].config(text="Actualizar")
            self.botones_accion['carpeta'].config(text=" Abrir Carpeta")
            self.botones_accion['terminal'].config(text=" Terminal")

            self.botones_req['desde_req'].config(text=" Desde requirements.txt")
            self.botones_req['crear_req'].config(text=" Crear requirements.txt")
            self.botones_req['ver_paquetes'].config(text=" Ver instaladas")
        except:
            pass

    def actualizar_region_scroll(self):
        """Actualiza la región de scroll del canvas"""
        try:
            self.ventana.after_idle(lambda: self.canvas_principal.configure(scrollregion=self.canvas_principal.bbox("all")))
        except:
            pass

    def escribir_en_consola(self, mensaje, etiqueta='normal'):
        """Escribe un mensaje en la consola"""
        self.salida_consola.config(state=tk.NORMAL)

        # Determina automáticamente la etiqueta según el contenido
        if mensaje.startswith("✓"):
            etiqueta = "exito"
        elif mensaje.startswith("✗"):
            etiqueta = "error"
        elif mensaje.startswith("⚠"):
            etiqueta = "advertencia"
        elif mensaje.startswith("$"):
            etiqueta = "comando"
        elif mensaje.startswith(("📁", "📂", "🐍")):
            etiqueta = "info"

        self.salida_consola.insert(tk.END, f"{mensaje}\n", etiqueta)
        self.salida_consola.see(tk.END)
        self.salida_consola.config(state=tk.DISABLED)
        self.ventana.update_idletasks()

    def limpiar_consola(self):
        """Limpia el contenido de la consola"""
        self.salida_consola.config(state=tk.NORMAL)
        self.salida_consola.delete(1.0, tk.END)
        self.salida_consola.insert(tk.END, "Consola limpiada\n\n", "exito")
        self.salida_consola.config(state=tk.DISABLED)

    def guardar_log(self):
        """Guarda el contenido de la consola en un archivo"""
        try:
            ruta_archivo = filedialog.asksaveasfilename(
                title="Guardar log",
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Archivos de log", "*.log"), ("Todos los archivos", "*.*")]
            )

            if ruta_archivo:
                contenido = self.salida_consola.get(1.0, tk.END)
                with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                    archivo.write(contenido)

                self.escribir_en_consola(f"Log guardado: {ruta_archivo}", "exito")
                messagebox.showinfo("Éxito", "Log guardado exitosamente")

        except Exception as e:
            self.escribir_en_consola(f"✗ Error guardando log: {str(e)}", "error")

    def cambiar_estado(self, mensaje):
        """Cambia el texto de la barra de estado"""
        self.variable_estado.set(mensaje)

    # Métodos para gestión de proyectos

    def crear_proyecto(self):
        """Crea un nuevo proyecto"""
        nombre = self.entrada_proyecto.get().strip()

        if not nombre:
            messagebox.showwarning("Advertencia", "Ingresa un nombre para el proyecto")
            return

        exito, mensaje = self.gestor_proyectos.crear_proyecto(nombre)

        if exito:
            self.escribir_en_consola(f"✓ {mensaje}", "exito")
            self.actualizar_proyectos()
            self.entrada_proyecto.delete(0, tk.END)
        else:
            self.escribir_en_consola(f"✗ {mensaje}", "error")
            messagebox.showwarning("Error", mensaje)

    def actualizar_proyectos(self):
        """Actualiza el árbol de proyectos"""
        # Limpia el árbol actual
        for item in self.arbol_proyectos.get_children():
            self.arbol_proyectos.delete(item)

        self.estructura_proyectos = {}

        proyectos = self.gestor_proyectos.obtener_proyectos()

        for proyecto in proyectos:
            # Agrega el proyecto al árbol
            id_proyecto = self.arbol_proyectos.insert('', tk.END, text=f" {proyecto['nombre']}", open=True)

            self.estructura_proyectos[id_proyecto] = {
                'tipo': 'proyecto',
                'nombre': proyecto['nombre'],
                'ruta': proyecto['ruta']
            }

            # Agrega los entornos virtuales
            for entorno in proyecto['entornos']:
                id_entorno = self.arbol_proyectos.insert(id_proyecto, tk.END, text=f"  🐍 {entorno['nombre']}")

                self.estructura_proyectos[id_entorno] = {
                    'tipo': 'entorno',
                    'proyecto': proyecto['nombre'],
                    'nombre': entorno['nombre'],
                    'ruta': entorno['ruta']
                }

            # Agrega otras carpetas
            for carpeta in proyecto['carpetas']:
                id_carpeta = self.arbol_proyectos.insert(id_proyecto, tk.END, text=f" {carpeta['nombre']}")

                self.estructura_proyectos[id_carpeta] = {
                    'tipo': 'carpeta',
                    'proyecto': proyecto['nombre'],
                    'nombre': carpeta['nombre'],
                    'ruta': carpeta['ruta']
                }

    def al_seleccionar_arbol(self, event):
        """Maneja la selección de elementos en el árbol"""
        seleccion = self.arbol_proyectos.selection()
        if not seleccion:
            return

        id_item = seleccion[0]
        if id_item in self.estructura_proyectos:
            info = self.estructura_proyectos[id_item]

            if info['tipo'] == 'proyecto':
                self.proyecto_actual.set(info['nombre'])
                self.etiqueta_proyecto.config(text=info['nombre'], style='Activo.TLabel')
                self.entorno_actual.set("")
                self.etiqueta_entorno.config(text="Ninguno", style='Inactivo.TLabel')
                self.variable_estado.set(f" {info['nombre']}")

            elif info['tipo'] == 'entorno':
                self.proyecto_actual.set(info['proyecto'])
                self.etiqueta_proyecto.config(text=info['proyecto'], style='Activo.TLabel')
                self.entorno_actual.set(info['nombre'])
                self.etiqueta_entorno.config(text=info['nombre'], style='Activo.TLabel')
                self.variable_estado.set(f" {info['proyecto']} / {info['nombre']}")

    def eliminar_seleccionado(self):
        """Elimina el elemento seleccionado"""
        seleccion = self.arbol_proyectos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un elemento")
            return

        id_item = seleccion[0]
        if id_item not in self.estructura_proyectos:
            return

        info = self.estructura_proyectos[id_item]

        if info['tipo'] == 'proyecto':
            mensaje = f"¿Eliminar proyecto '{info['nombre']}' y todos sus entornos?"
        elif info['tipo'] == 'entorno':
            mensaje = f"¿Eliminar entorno '{info['nombre']}'?"
        else:
            mensaje = f"¿Eliminar carpeta '{info['nombre']}'?"

        if messagebox.askyesno("Confirmar", mensaje):
            if info['tipo'] == 'proyecto':
                exito, resultado = self.gestor_proyectos.eliminar_proyecto(info['nombre'])
            elif info['tipo'] == 'entorno':
                exito, resultado = self.gestor_entornos.eliminar_entorno(info['proyecto'], info['nombre'])
            else:
                # Para carpetas usa shutil directamente
                try:
                    import shutil
                    shutil.rmtree(info['ruta'])
                    exito, resultado = True, f"Carpeta '{info['nombre']}' eliminada"
                except Exception as e:
                    exito, resultado = False, f"Error: {str(e)}"

            if exito:
                self.escribir_en_consola(f"✓ {resultado}", "exito")
                self.actualizar_proyectos()

                # Limpia la selección actual si es necesario
                if info['tipo'] == 'proyecto' and self.proyecto_actual.get() == info['nombre']:
                    self.proyecto_actual.set("")
                    self.etiqueta_proyecto.config(text="Ninguno", style='Inactivo.TLabel')
                    self.entorno_actual.set("")
                    self.etiqueta_entorno.config(text="Ninguno", style='Inactivo.TLabel')
                elif info['tipo'] == 'entorno' and self.entorno_actual.get() == info['nombre']:
                    self.entorno_actual.set("")
                    self.etiqueta_entorno.config(text="Ninguno", style='Inactivo.TLabel')
            else:
                self.escribir_en_consola(f"✗ {resultado}", "error")

    def abrir_carpeta(self):
        """Abre la carpeta del elemento seleccionado"""
        seleccion = self.arbol_proyectos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un elemento")
            return

        id_item = seleccion[0]
        if id_item not in self.estructura_proyectos:
            return

        info = self.estructura_proyectos[id_item]

        if info['tipo'] == 'proyecto':
            exito, mensaje = self.gestor_proyectos.abrir_carpeta_proyecto(info['nombre'])
        else:
            # Para entornos y carpetas, abre directamente la ruta
            from src_gestor.utilidades import SistemaOperativo
            sistema = SistemaOperativo()
            exito = sistema.abrir_carpeta(info['ruta'])
            mensaje = "Carpeta abierta" if exito else "No se pudo abrir la carpeta"

        if exito:
            self.escribir_en_consola(f"✓ {mensaje}", "exito")
        else:
            self.escribir_en_consola(f"✗ {mensaje}", "error")

    def abrir_terminal(self):
        """Abre terminal en el elemento seleccionado"""
        seleccion = self.arbol_proyectos.selection()

        if seleccion:
            id_item = seleccion[0]
            if id_item in self.estructura_proyectos:
                info = self.estructura_proyectos[id_item]

                if info['tipo'] == 'entorno':
                    exito, mensaje = self.gestor_entornos.abrir_terminal_con_entorno(info['proyecto'], info['nombre'])
                elif info['tipo'] == 'proyecto':
                    exito, mensaje = self.gestor_proyectos.abrir_terminal_proyecto(info['nombre'])
                else:
                    from src_gestor.utilidades import SistemaOperativo
                    sistema = SistemaOperativo()
                    exito = sistema.abrir_terminal(info['ruta'])
                    mensaje = "Terminal abierto" if exito else "No se pudo abrir terminal"
        elif self.proyecto_actual.get():
            exito, mensaje = self.gestor_proyectos.abrir_terminal_proyecto(self.proyecto_actual.get())
        else:
            messagebox.showwarning("Advertencia", "Selecciona un proyecto o entorno")
            return

        if exito:
            self.escribir_en_consola(f"✓ {mensaje}", "exito")
        else:
            self.escribir_en_consola(f"✗ {mensaje}", "error")

    # Métodos para gestión de entornos virtuales

    def crear_entorno(self):
        """Crea un nuevo entorno virtual"""
        if not self.proyecto_actual.get():
            messagebox.showwarning("Advertencia", "Selecciona un proyecto primero")
            return

        nombre = self.entrada_entorno.get().strip()

        if not nombre:
            messagebox.showwarning("Advertencia", "Ingresa un nombre para el entorno")
            return

        exito, mensaje = self.gestor_entornos.crear_entorno(
            self.proyecto_actual.get(),
            nombre,
            self.actualizar_proyectos
        )

        if exito:
            self.escribir_en_consola(f"✓ {mensaje}", "exito")
            self.entrada_entorno.delete(0, tk.END)
        else:
            self.escribir_en_consola(f"✗ {mensaje}", "error")
            messagebox.showwarning("Error", mensaje)

    # Métodos para gestión de librerías

    def instalar_libreria(self):
        """Instala una librería en el entorno actual"""
        if not self.proyecto_actual.get():
            messagebox.showwarning("Advertencia", "Selecciona un proyecto")
            return

        if not self.entorno_actual.get():
            messagebox.showwarning("Advertencia", "Selecciona un entorno virtual")
            return

        libreria = self.libreria_a_instalar.get().strip()
        if not libreria:
            messagebox.showwarning("Advertencia", "Ingresa el nombre de la librería")
            return

        exito, mensaje = self.gestor_entornos.instalar_libreria(
            self.proyecto_actual.get(),
            self.entorno_actual.get(),
            libreria
        )

        if exito:
            self.escribir_en_consola(f"✓ {mensaje}", "exito")
            self.libreria_a_instalar.set("")
        else:
            self.escribir_en_consola(f"✗ {mensaje}", "error")

    def instalar_desde_requirements(self):
        """Instala librerías desde un archivo requirements.txt"""
        if not self.proyecto_actual.get():
            messagebox.showwarning("Advertencia", "Selecciona un proyecto")
            return

        if not self.entorno_actual.get():
            messagebox.showwarning("Advertencia", "Selecciona un entorno virtual")
            return

        ruta_proyecto = self.gestor_proyectos.obtener_ruta_proyecto(self.proyecto_actual.get())
        requirements_default = ruta_proyecto / "requirements.txt"

        if requirements_default.exists():
            usar_default = messagebox.askyesno(
                "Requirements encontrado",
                f"¿Usar requirements.txt del proyecto?\n\n{requirements_default}"
            )
            if usar_default:
                ruta_archivo = str(requirements_default)
            else:
                ruta_archivo = filedialog.askopenfilename(
                    title="Seleccionar requirements.txt",
                    filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
                )
        else:
            ruta_archivo = filedialog.askopenfilename(
                title="Seleccionar requirements.txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )

        if ruta_archivo:
            exito, mensaje = self.gestor_entornos.instalar_desde_requirements(
                self.proyecto_actual.get(),
                self.entorno_actual.get(),
                ruta_archivo
            )

            if exito:
                self.escribir_en_consola(f"✓ {mensaje}", "exito")
            else:
                self.escribir_en_consola(f"✗ {mensaje}", "error")

    def crear_requirements(self):
        """Crea un archivo requirements.txt"""
        if not self.proyecto_actual.get():
            messagebox.showwarning("Advertencia", "Selecciona un proyecto")
            return

        if not self.entorno_actual.get():
            messagebox.showwarning("Advertencia", "Selecciona un entorno virtual")
            return

        ruta_proyecto = self.gestor_proyectos.obtener_ruta_proyecto(self.proyecto_actual.get())

        ruta_archivo = filedialog.asksaveasfilename(
            title="Guardar requirements.txt",
            initialdir=str(ruta_proyecto),
            initialfile="requirements.txt",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )

        if ruta_archivo:
            exito, mensaje = self.gestor_entornos.crear_requirements(
                self.proyecto_actual.get(),
                self.entorno_actual.get(),
                ruta_archivo
            )

            if exito:
                self.escribir_en_consola(f"✓ {mensaje}", "exito")
                messagebox.showinfo("Éxito", "requirements.txt guardado")
            else:
                self.escribir_en_consola(f"✗ {mensaje}", "error")

    def mostrar_paquetes(self):
        """Muestra los paquetes instalados en el entorno actual"""
        if not self.proyecto_actual.get():
            messagebox.showwarning("Advertencia", "Selecciona un proyecto")
            return

        if not self.entorno_actual.get():
            messagebox.showwarning("Advertencia", "Selecciona un entorno virtual")
            return

        exito, mensaje = self.gestor_entornos.listar_paquetes(
            self.proyecto_actual.get(),
            self.entorno_actual.get()
        )

        if exito:
            self.escribir_en_consola(f"✓ {mensaje}", "exito")
        else:
            self.escribir_en_consola(f"✗ {mensaje}", "error")

    def ejecutar(self):
        """Inicia la aplicación"""
        self.ventana.mainloop()