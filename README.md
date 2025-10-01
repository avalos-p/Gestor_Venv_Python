# Gestor de Entornos Virtuales Python

Una aplicación con interfaz gráfica para gestionar proyectos Python y sus entornos virtuales de manera organizada y sencilla.

## Características principales

- **Gestión de proyectos**: Crea y organiza proyectos Python con estructura predefinida
- **Entornos virtuales**: Crea, elimina y gestiona múltiples entornos por proyecto
- **Instalación de librerías**: Instala paquetes directamente desde la interfaz
- **Requirements.txt**: Genera y utiliza archivos de dependencias automáticamente
- **Terminales integradas**: Abre terminales con entornos activados
- **Multiplataforma**: Compatible con Windows y Linux
- **Interfaz responsiva**: Se adapta al tamaño de la ventana

## Estructura del proyecto

```
gestor/
├── main.py          # Punto de entrada principal
├── interfaz.py      # Interfaz gráfica completa
├── proyectos.py     # Gestión de proyectos
├── entornos.py      # Manejo de entornos virtuales
├── utilidades.py    # Funciones auxiliares del sistema
├── __init__.py      # Configuración del paquete
└── README.md        # Este archivo
```

## Instalación y uso

### Requisitos

- Python 3.6 o superior
- tkinter (incluido en la mayoría de instalaciones de Python)

### Ejecución

```bash
cd gestor
python main.py
```

## Funcionalidades detalladas

### Gestión de proyectos

- Crear nuevos proyectos con estructura básica
- Eliminar proyectos completos
- Abrir carpetas en el explorador del sistema
- Generar archivos README.md y .gitignore automáticamente

### Entornos virtuales

- Crear entornos virtuales usando venv
- Eliminar entornos cuando ya no se necesiten
- Abrir terminales con el entorno activado
- Visualizar la estructura en árbol jerárquico

### Gestión de dependencias

- Instalar librerías con pip directamente
- Crear archivos requirements.txt desde el entorno
- Instalar dependencias desde requirements.txt existentes
- Ver lista de paquetes instalados

### Interfaz responsiva

- Modo normal para pantallas grandes
- Modo compacto para ventanas pequeñas
- Botones que se adaptan al espacio disponible
- Scroll automático para contenido extenso

## Arquitectura del código

### Separación de responsabilidades

- **main.py**: Solo inicia la aplicación
- **interfaz.py**: Maneja toda la parte visual y eventos
- **proyectos.py**: Lógica de creación y gestión de proyectos
- **entornos.py**: Operaciones con entornos virtuales
- **utilidades.py**: Funciones auxiliares multiplataforma

### Patrones utilizados

- **Separación de capas**: UI, lógica de negocio y utilidades
- **Callbacks**: Para comunicación asíncrona entre módulos
- **Factory methods**: Para crear componentes según el sistema operativo
- **Observer**: Para actualizar la interfaz cuando cambian los datos

## Personalización

### Modificar estilos

Los estilos visuales se configuran en `interfaz.py` en el método `configurar_estilos()`:

```python
def configurar_estilos(self):
    estilo = ttk.Style()
    estilo.configure('Titulo.TLabel', font=('Segoe UI', 18, 'bold'))
    # Agregar más configuraciones...
```

### Añadir nuevas funcionalidades

1. **Para nueva lógica de proyectos**: Modificar `proyectos.py`
2. **Para operaciones de entornos**: Modificar `entornos.py`
3. **Para nuevos elementos de UI**: Modificar `interfaz.py`
4. **Para funciones del sistema**: Modificar `utilidades.py`

## Solución de problemas

### Error: "No module named tkinter"

En algunos sistemas Linux, instalar tkinter:

```bash
sudo apt-get install python3-tk
```

### Error: "Permission denied" al crear entornos

Verificar permisos de escritura en la carpeta del proyecto.

### Terminal no se abre correctamente

El gestor intenta varios terminales en Linux. Si falla, verificar que esté instalado alguno:

```bash
sudo apt-get install gnome-terminal
# o
sudo apt-get install konsole
```

## Contribuciones

Para contribuir al proyecto:

1. Mantener la separación de módulos existente
2. Escribir comentarios en español claro y natural
3. Seguir las convenciones de nomenclatura establecidas
4. Probar en Windows y Linux cuando sea posible

## Licencia

Este proyecto es de uso libre.
