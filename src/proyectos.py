import shutil
from pathlib import Path
from src.utilidades import SistemaOperativo, validar_nombre, crear_gitignore, crear_readme

"""
Gestión de Proyectos y directorios
"""

class GestorProyectos:
    """Maneja la creación y administración de proyectos"""

    def __init__(self, directorio_base):
        self.directorio_base = Path(directorio_base)
        self.directorio_proyectos = self.directorio_base / "projects"
        self.sistema = SistemaOperativo()

        # Asegura que existe el directorio de proyectos
        self.directorio_proyectos.mkdir(exist_ok=True)

    def crear_proyecto(self, nombre):
        """Crea un nuevo proyecto con su estructura básica"""
        if not nombre.strip():
            return False, "El nombre del proyecto no puede estar vacío"

        if not validar_nombre(nombre):
            return False, "El nombre solo puede contener letras, números, guiones y guiones bajos"

        ruta_proyecto = self.directorio_proyectos / nombre

        if ruta_proyecto.exists():
            return False, f"Ya existe un proyecto llamado '{nombre}'"

        try:
            # Crea la estructura del proyecto
            ruta_proyecto.mkdir(parents=True)
            # (ruta_proyecto / "venvs").mkdir()
            # (ruta_proyecto / "src").mkdir()

            # Crea archivos básicos del proyecto
            crear_readme(ruta_proyecto, nombre)
            crear_gitignore(ruta_proyecto)

            return True, f"Proyecto '{nombre}' creado exitosamente"

        except Exception as e:
            return False, f"Error al crear el proyecto: {str(e)}"

    def eliminar_proyecto(self, nombre):
        """Elimina un proyecto completo"""
        ruta_proyecto = self.directorio_proyectos / nombre

        if not ruta_proyecto.exists():
            return False, f"El proyecto '{nombre}' no existe"

        try:
            shutil.rmtree(ruta_proyecto)
            return True, f"Proyecto '{nombre}' eliminado"

        except Exception as e:
            return False, f"Error al eliminar el proyecto: {str(e)}"

    def obtener_proyectos(self):
        """Devuelve una lista de todos los proyectos disponibles"""
        proyectos = []

        try:
            for directorio in self.directorio_proyectos.iterdir():
                if directorio.is_dir():
                    info_proyecto = {
                        'nombre': directorio.name,
                        'ruta': directorio,
                        'entornos': self._obtener_entornos_proyecto(directorio),
                        'carpetas': self._obtener_carpetas_proyecto(directorio)
                    }
                    proyectos.append(info_proyecto)

        except Exception:
            pass

        return proyectos

    def _obtener_entornos_proyecto(self, ruta_proyecto):
        """Obtiene los entornos virtuales de un proyecto"""
        entornos = []
        directorio_venvs = ruta_proyecto / "venvs"

        if directorio_venvs.exists():
            for venv_dir in directorio_venvs.iterdir():
                if venv_dir.is_dir() and (venv_dir / "pyvenv.cfg").exists():
                    entornos.append({
                        'nombre': venv_dir.name,
                        'ruta': venv_dir
                    })

        return entornos

    def _obtener_carpetas_proyecto(self, ruta_proyecto):
        """Obtiene las carpetas adicionales de un proyecto"""
        carpetas = []

        for subdirectorio in ruta_proyecto.iterdir():
            if (subdirectorio.is_dir() and
                subdirectorio.name not in ['venvs', '__pycache__', '.git']):
                carpetas.append({
                    'nombre': subdirectorio.name,
                    'ruta': subdirectorio
                })

        return carpetas

    def abrir_carpeta_proyecto(self, nombre):
        """Abre la carpeta de un proyecto en el explorador"""
        ruta_proyecto = self.directorio_proyectos / nombre

        if not ruta_proyecto.exists():
            return False, f"El proyecto '{nombre}' no existe"

        exito = self.sistema.abrir_carpeta(ruta_proyecto)
        if exito:
            return True, "Carpeta abierta en el explorador"
        else:
            return False, "No se pudo abrir la carpeta"

    def abrir_terminal_proyecto(self, nombre):
        """Abre una terminal en la carpeta del proyecto"""
        ruta_proyecto = self.directorio_proyectos / nombre

        if not ruta_proyecto.exists():
            return False, f"El proyecto '{nombre}' no existe"

        exito = self.sistema.abrir_terminal(ruta_proyecto)
        if exito:
            return True, "Terminal abierto en el proyecto"
        else:
            return False, "No se pudo abrir la terminal"

    def obtener_ruta_proyecto(self, nombre):
        """Devuelve la ruta completa de un proyecto"""
        return self.directorio_proyectos / nombre

    def proyecto_existe(self, nombre):
        """Verifica si existe un proyecto con el nombre dado"""
        return (self.directorio_proyectos / nombre).exists()