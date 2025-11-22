from dash import Dash
from views.layout import serve_layout
from models.data_model import load_data


# 1) Primero definimos la app
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "EDA – Campaña Depósitos a Plazo"
server = app.server

app.layout = serve_layout


if __name__ == "__main__":
    # 2) Antes de arrancar el servidor, garantizamos que el merged esté listo
    print("[INFO] Inicializando datos...")
    _ = load_data()   # aquí se genera o carga merged_dataset.csv

    # 3) Ahora sí, arrancamos el servidor Dash
    print("[INFO] Datos listos. Iniciando servidor Dash...")
    app.run(debug=True)
