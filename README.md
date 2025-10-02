# Gestor de Entornos Virtuales Python

Una aplicación con interfaz gráfica para gestionar proyectos Python y sus entornos virtuales de manera organizada y sencilla.

## Características principales

- **Gestión de proyectos**: Crea y organiza proyectos Python
- **Entornos virtuales**: Crea, elimina y gestiona múltiples entornos por proyecto
- **Instalación de librerías**: Instala paquetes directamente desde la interfaz
- **Requirements.txt**: Genera y utiliza archivos de dependencias automáticamente
- **Terminales integradas**: Abre terminales con entornos activados
- **Multiplataforma**: Compatible con Windows y Linux

## Estructura del proyecto

```
gestor/
├── main.py              # El archivo que ejecuta el programa
src_gestor/
    ├── interfaz.py      # Interfaz gráfica
    ├── proyectos.py     # Gestión de proyectos
    ├── entornos.py      # Manejo de entornos virtuales
    └── utilidades.py    # Funciones auxiliares
    
```

## Instalación y uso

### Requisitos

- Python 3.6 o superior

### Ejecución

```bash
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

## Licencia
The Unlicense
