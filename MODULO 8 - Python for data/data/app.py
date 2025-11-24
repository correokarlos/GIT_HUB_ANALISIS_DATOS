from dash import Dash, Input, Output
from views.layout import serve_layout
from models.data_model import load_data
from controllers import eda_controller as ec

# Inicializar app
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "EDA – Campaña Depósitos"
app.layout = serve_layout

# Cargar datos una sola vez antes de arrancar el servidor
df_global = load_data()

# ======================================================
# CALLBACK: filtro de edad → gráfico + texto conversión
# ======================================================
@app.callback(
    [Output("graph-conv-age", "figure"),
     Output("text-conv-age", "children")],
    [Input("filtro-edad-conv", "value")],
)
def actualizar_conversion_edad(rango_edad):
    """
    Filtra el dataframe global por rango de edad y recalcula:
    - Gráfico de conversión por rangos de edad
    - Texto explicativo
    """
    # Seguridad básica
    if not rango_edad or len(rango_edad) != 2:
        df_filtrado = df_global
    else:
        edad_min, edad_max = rango_edad
        df_filtrado = df_global[
            (df_global["age"] >= edad_min) & (df_global["age"] <= edad_max)
        ]

    fig, texto = ec.get_conversion_by_age_figure(df_filtrado)
    return fig, texto

if __name__ == "__main__":
    # 2) Antes de arrancar el servidor, garantizamos que el merged esté listo
    print("[INFO] Inicializando datos...")
    _ = load_data()   # aquí se genera o carga merged_dataset.csv

    # 3) Ahora sí, arrancamos el servidor Dash
    print("[INFO] Datos listos. Iniciando servidor Dash...")
    app.run(debug=True)
