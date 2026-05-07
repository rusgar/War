import os
import sys

def run_app_1():
    # Este script ejecuta el comando 'streamlit run app_1.py' desde Python
    # Es útil para entornos que requieren un punto de entrada .py estándar
    try:
        print("Iniciando la aplicación de Streamlit...")
        os.system("streamlit run app_1.py")
    except KeyboardInterrupt:
        print("\nAplicación detenida por el usuario.")
    except Exception as e:
        print(f"Error al intentar ejecutar Streamlit: {e}")

if __name__ == "__main__":
    run_app_1()
