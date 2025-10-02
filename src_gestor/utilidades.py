import subprocess
import threading
import platform
import sys
import os
from pathlib import Path

"""
Utilidades del Gestor de Entornos Virtuales
Funciones auxiliares para el funcionamiento del sistema
"""

class SistemaOperativo:
    """Maneja las diferencias entre sistemas operativos"""

    def __init__(self):
        self.nombre = platform.system()

    def obtener_python(self):
        """Devuelve la ruta del ejecutable de Python actual"""
        return sys.executable

    def obtener_python_venv(self, ruta_venv):
        """Devuelve la ruta del Python dentro de un entorno virtual"""
        if self.nombre == "Windows":
            return ruta_venv / "Scripts" / "python.exe"
        else:
            return ruta_venv / "bin" / "python"

    def obtener_pip_venv(self, ruta_venv):
        """Devuelve la ruta del pip dentro de un entorno virtual"""
        if self.nombre == "Windows":
            return ruta_venv / "Scripts" / "pip.exe"
        else:
            return ruta_venv / "bin" / "pip"

    def abrir_carpeta(self, ruta):
        """Abre una carpeta en el explorador del sistema"""
        try:
            if self.nombre == "Windows":
                os.startfile(ruta)
            elif self.nombre == "Darwin":
                subprocess.run(["open", str(ruta)])
            else:
                subprocess.run(["xdg-open", str(ruta)])
            return True
        except Exception:
            return False

    def abrir_terminal(self, ruta):
        """Abre una terminal en la ruta especificada"""
        try:
            if self.nombre == "Windows":
                subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', f'cd /d "{ruta}"'], shell=True)
            else:
                # Prueba varios terminales comunes en Linux
                terminales = ['gnome-terminal', 'konsole', 'xterm']
                for terminal in terminales:
                    try:
                        subprocess.Popen([terminal, '--working-directory', str(ruta)])
                        break
                    except FileNotFoundError:
                        continue
            return True
        except Exception:
            return False

class EjecutorComandos:
    """Ejecuta comandos del sistema de forma asíncrona"""

    def __init__(self, callback_salida=None, callback_estado=None):
        self.callback_salida = callback_salida
        self.callback_estado = callback_estado

    def ejecutar(self, comando, directorio_trabajo=None, callback_exito=None):
        """Ejecuta un comando en un hilo separado"""
        def _ejecutar():
            try:
                if self.callback_estado:
                    self.callback_estado("Ejecutando...")

                if self.callback_salida:
                    self.callback_salida(f"$ {' '.join(comando)}", "comando")

                proceso = subprocess.Popen(
                    comando,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1,
                    cwd=directorio_trabajo
                )

                # Lee la salida línea por línea
                for linea in iter(proceso.stdout.readline, ''):
                    if linea and self.callback_salida:
                        self.callback_salida(linea.rstrip())

                proceso.wait()

                if proceso.returncode == 0:
                    if self.callback_salida:
                        self.callback_salida("✓ Comando completado exitosamente", "exito")
                    if callback_exito:
                        # Programa el callback para ejecutarse en el hilo principal
                        threading.Timer(0.1, callback_exito).start()
                else:
                    if self.callback_salida:
                        self.callback_salida(f"✗ Error en comando (código {proceso.returncode})", "error")

            except Exception as e:
                if self.callback_salida:
                    self.callback_salida(f"✗ Error: {str(e)}", "error")
            finally:
                if self.callback_estado:
                    self.callback_estado("Listo")

        hilo = threading.Thread(target=_ejecutar, daemon=True)
        hilo.start()

def validar_nombre(nombre):
    """Valida que un nombre solo contenga caracteres permitidos"""
    return nombre.replace('_', '').replace('-', '').isalnum()