import subprocess
import shutil
from pathlib import Path
from src.utilidades import SistemaOperativo, EjecutorComandos, validar_nombre

"""
Creación, eliminación y manejo de entornos virtuales de Python
"""

class GestorEntornos:
    """Maneja la creación y administración de entornos virtuales"""

    def __init__(self, directorio_proyectos, callback_salida=None, callback_estado=None):
        self.directorio_proyectos = Path(directorio_proyectos)
        self.sistema = SistemaOperativo()
        self.ejecutor = EjecutorComandos(callback_salida, callback_estado)

    def crear_entorno(self, nombre_proyecto, nombre_entorno, callback_exito=None):
        """Crea un nuevo entorno virtual en el proyecto especificado"""
        if not nombre_entorno.strip():
            return False, "El nombre del entorno no puede estar vacío"

        if not validar_nombre(nombre_entorno):
            return False, "El nombre solo puede contener letras, números, guiones y guiones bajos"

        ruta_proyecto = self.directorio_proyectos / nombre_proyecto
        if not ruta_proyecto.exists():
            return False, f"El proyecto '{nombre_proyecto}' no existe"

        ruta_entorno = ruta_proyecto / "venvs" / nombre_entorno

        if ruta_entorno.exists():
            return False, f"Ya existe un entorno llamado '{nombre_entorno}'"

        # Comando para crear el entorno virtual
        comando = [self.sistema.obtener_python(), "-m", "venv", str(ruta_entorno)]
        self.ejecutor.ejecutar(comando, callback_exito=callback_exito)

        return True, f"Creando entorno '{nombre_entorno}'..."

    def eliminar_entorno(self, nombre_proyecto, nombre_entorno):
        """Elimina un entorno virtual"""
        ruta_entorno = self.directorio_proyectos / nombre_proyecto / "venvs" / nombre_entorno

        if not ruta_entorno.exists():
            return False, f"El entorno '{nombre_entorno}' no existe"

        try:
            shutil.rmtree(ruta_entorno)
            return True, f"Entorno '{nombre_entorno}' eliminado"

        except Exception as e:
            return False, f"Error al eliminar el entorno: {str(e)}"

    def instalar_libreria(self, nombre_proyecto, nombre_entorno, libreria):
        """Instala una librería en el entorno virtual especificado"""
        if not libreria.strip():
            return False, "Debes especificar el nombre de la librería"

        pip_path = self._obtener_pip_entorno(nombre_proyecto, nombre_entorno)
        if not pip_path.exists():
            return False, f"El entorno '{nombre_entorno}' no existe o no es válido"

        comando = [str(pip_path), "install", libreria]
        self.ejecutor.ejecutar(comando)

        return True, f"Instalando '{libreria}'..."

    def instalar_desde_requirements(self, nombre_proyecto, nombre_entorno, archivo_requirements):
        """Instala librerías desde un archivo requirements.txt"""
        pip_path = self._obtener_pip_entorno(nombre_proyecto, nombre_entorno)
        if not pip_path.exists():
            return False, f"El entorno '{nombre_entorno}' no existe o no es válido"

        if not Path(archivo_requirements).exists():
            return False, f"El archivo '{archivo_requirements}' no existe"

        comando = [str(pip_path), "install", "-r", archivo_requirements]
        self.ejecutor.ejecutar(comando)

        return True, f"Instalando desde {archivo_requirements}..."

    def crear_requirements(self, nombre_proyecto, nombre_entorno, ruta_destino):
        """Crea un archivo requirements.txt con las librerías instaladas"""
        pip_path = self._obtener_pip_entorno(nombre_proyecto, nombre_entorno)
        if not pip_path.exists():
            return False, f"El entorno '{nombre_entorno}' no existe o no es válido"

        try:
            resultado = subprocess.run(
                [str(pip_path), "freeze"],
                capture_output=True,
                text=True,
                check=True
            )

            with open(ruta_destino, 'w') as archivo:
                archivo.write(resultado.stdout)

            return True, f"Requirements guardado en {ruta_destino}"

        except Exception as e:
            return False, f"Error al crear requirements: {str(e)}"

    def listar_paquetes(self, nombre_proyecto, nombre_entorno):
        """Lista los paquetes instalados en un entorno virtual"""
        pip_path = self._obtener_pip_entorno(nombre_proyecto, nombre_entorno)
        if not pip_path.exists():
            return False, f"El entorno '{nombre_entorno}' no existe o no es válido"

        comando = [str(pip_path), "list"]
        self.ejecutor.ejecutar(comando)

        return True, f"Listando paquetes de '{nombre_entorno}'..."

    def abrir_terminal_con_entorno(self, nombre_proyecto, nombre_entorno):
        """Abre una terminal con el entorno virtual activado"""
        ruta_proyecto = self.directorio_proyectos / nombre_proyecto
        ruta_entorno = ruta_proyecto / "venvs" / nombre_entorno

        if not ruta_entorno.exists():
            return False, f"El entorno '{nombre_entorno}' no existe"

        try:
            if self.sistema.nombre == "Windows":
                # Crea un script temporal para activar el entorno
                script_path = ruta_entorno / "activar_terminal.bat"
                with open(script_path, 'w') as archivo:
                    archivo.write(f'@echo off\n')
                    archivo.write(f'cd /d "{ruta_proyecto}"\n')
                    archivo.write(f'call "{ruta_entorno}\\Scripts\\activate.bat"\n')
                    archivo.write(f'echo Entorno {nombre_entorno} activado en {nombre_proyecto}\n')
                    archivo.write(f'echo Usa "deactivate" para salir del entorno\n')

                subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', str(script_path)], shell=True)

            else:
                # Script para sistemas Unix
                script_path = ruta_entorno / "activar_terminal.sh"
                with open(script_path, 'w') as archivo:
                    archivo.write('#!/bin/bash\n')
                    archivo.write(f'cd "{ruta_proyecto}"\n')
                    archivo.write(f'source "{ruta_entorno}/bin/activate"\n')
                    archivo.write(f'echo "Entorno {nombre_entorno} activado en {nombre_proyecto}"\n')
                    archivo.write('echo "Usa \'deactivate\' para salir del entorno"\n')
                    archivo.write('bash\n')

                # Hace el script ejecutable
                import os
                os.chmod(script_path, 0o755)

                # Intenta abrir con diferentes terminales
                terminales = ['gnome-terminal', 'konsole', 'xterm']
                for terminal in terminales:
                    try:
                        subprocess.Popen([terminal, '--', 'bash', str(script_path)])
                        break
                    except FileNotFoundError:
                        continue

            return True, f"Terminal abierto con entorno '{nombre_entorno}'"

        except Exception as e:
            return False, f"Error al abrir terminal: {str(e)}"

    def _obtener_pip_entorno(self, nombre_proyecto, nombre_entorno):
        """Obtiene la ruta del pip del entorno virtual"""
        ruta_entorno = self.directorio_proyectos / nombre_proyecto / "venvs" / nombre_entorno
        return self.sistema.obtener_pip_venv(ruta_entorno)

    def entorno_existe(self, nombre_proyecto, nombre_entorno):
        """Verifica si existe un entorno virtual específico"""
        ruta_entorno = self.directorio_proyectos / nombre_proyecto / "venvs" / nombre_entorno
        return ruta_entorno.exists() and (ruta_entorno / "pyvenv.cfg").exists()

    def obtener_ruta_entorno(self, nombre_proyecto, nombre_entorno):
        """Devuelve la ruta completa de un entorno virtual"""
        return self.directorio_proyectos / nombre_proyecto / "venvs" / nombre_entorno