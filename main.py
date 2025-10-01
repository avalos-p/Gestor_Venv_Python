from src_gestor.interfaz import GestorInterfaz
"""
Gestor de Entornos Virtuales - Compatible con Windows y Linux
"""


def main():
    # Inicia la aplicación del gestor
    app = GestorInterfaz()
    app.ejecutar()

if __name__ == "__main__":
    main()