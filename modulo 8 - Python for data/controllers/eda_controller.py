import base64
import io
import pandas as pd
import plotly.express as px

import matplotlib
matplotlib.use("Agg")   # backend sin interfaz gráfica

import matplotlib.pyplot as plt
import seaborn as sns



def _fix_plotly(fig, height: int = 260):
    """
    Ajustes comunes para todas las figuras Plotly.
    - Altura controlada
    - Anchura 100% del contenedor (autosize = True)
    """
    fig.update_layout(
        autosize=True,                      # ← antes False, ahora se adapta a la tarjeta
        height=height,
        margin=dict(l=20, r=20, t=50, b=40),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig



def _matplotlib_to_base64():
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=110)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


# ======================
# Numéricas (Matplotlib / Seaborn)
# ======================

def get_age_distribution_image(df: pd.DataFrame):
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 4))
    sns.histplot(df["age"], kde=True, bins=20, color="#2563eb")
    plt.title("Distribución de la edad de los clientes")
    plt.xlabel("Edad (años)")
    plt.ylabel("Número de clientes")

    img_b64 = _matplotlib_to_base64()

    media = df["age"].mean()
    texto = (
        f"La mayoría de clientes se concentra entre los 30 y los 50 años, "
        f"con una edad media cercana a los {media:.1f} años."
    )
    return img_b64, texto


def get_income_distribution_image(df: pd.DataFrame):
    if "Income" not in df.columns:
        return None, "No se dispone de la variable de ingresos en el dataset."
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 4))
    sns.histplot(df["Income"], kde=True, bins=25, color="#059669")
    plt.title("Distribución del nivel de ingresos")
    plt.xlabel("Ingreso anual estimado")
    plt.ylabel("Número de clientes")

    img_b64 = _matplotlib_to_base64()

    media = df["Income"].mean()
    texto = (
        "Los ingresos presentan una distribución asimétrica: la mayoría de clientes se mueve en "
        f"rangos medios, pero existen algunos con ingresos elevados. El ingreso medio ronda los {media:,.0f}."
    )
    return img_b64, texto


def get_numwebvisits_distribution_image(df: pd.DataFrame):
    if "NumWebVisitsMonth" not in df.columns:
        return None, "No se dispone de visitas web mensuales en el dataset."
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 4))
    sns.countplot(x="NumWebVisitsMonth", data=df, color="#7c3aed")
    plt.title("Número de visitas web mensuales")
    plt.xlabel("Visitas web en el último mes")
    plt.ylabel("Número de clientes")

    img_b64 = _matplotlib_to_base64()

    media = df["NumWebVisitsMonth"].mean()
    texto = (
        f"La mayoría de clientes realiza pocas visitas web al mes, con una media aproximada de {media:.1f} visitas. "
        "Esto sugiere un uso moderado de los canales digitales."
    )
    return img_b64, texto


def get_kidteen_distribution_image(df: pd.DataFrame):
    cols = [c for c in ["Kidhome", "Teenhome"] if c in df.columns]
    if not cols:
        return None, "No se dispone de información sobre menores en el hogar."
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 4))
    melted = df[cols].melt(var_name="Tipo", value_name="Número")
    melted["Tipo"] = melted["Tipo"].map({"Kidhome": "Niños", "Teenhome": "Adolescentes"})
    sns.countplot(data=melted, x="Número", hue="Tipo")
    plt.title("Distribución de menores en el hogar")
    plt.xlabel("Número de menores en el hogar")
    plt.ylabel("Número de clientes")

    img_b64 = _matplotlib_to_base64()

    texto = (
        "La mayoría de los clientes convive con un número reducido de niños y adolescentes, "
        "lo que indica hogares de tamaño pequeño o medio y una estructura familiar bastante homogénea."
    )
    return img_b64, texto


# ======================
# Categóricas / financieras (Plotly)
# ======================

def get_marital_distribution_figure(df: pd.DataFrame):
    counts = df["marital"].value_counts(normalize=True).reset_index()
    counts.columns = ["marital", "proporcion"]
    mapping = {
        "married": "Casado/a",
        "single": "Soltero/a",
        "divorced": "Divorciado/a",
        "unknown": "Desconocido",
    }
    counts["marital_es"] = counts["marital"].map(mapping).fillna(counts["marital"])
    fig = px.bar(
        counts,
        x="marital_es",
        y="proporcion",
        title="Estado civil de los clientes",
        text=counts["proporcion"].map(lambda v: f"{v*100:.1f}%"),
    )
    fig.update_yaxes(tickformat=".0%")
    fig = _fix_plotly(fig)

    top_row = counts.iloc[0]
    texto = (
        f"El estado civil predominante es **{top_row['marital_es']}**, "
        f"que representa aproximadamente el {top_row['proporcion']*100:.1f}% de los clientes."
    )
    return fig, texto


def get_job_distribution_figure(df: pd.DataFrame):
    counts = df["job"].value_counts().reset_index()
    counts.columns = ["job", "count"]
    fig = px.bar(
        counts,
        x="job",
        y="count",
        title="Sector laboral / tipo de ocupación",
    )
    fig.update_xaxes(tickangle=40)
    fig = _fix_plotly(fig, height=430)

    top_row = counts.iloc[0]
    texto = (
        f"El grupo laboral más frecuente es **{top_row['job']}**, "
        "lo que indica que este perfil profesional tiene un peso relevante en la base de clientes."
    )
    return fig, texto


def get_education_distribution_figure(df: pd.DataFrame):
    counts = df["education"].value_counts(normalize=True).reset_index()
    counts.columns = ["education", "proporcion"]
    mapping = {
        "basic.4y": "Básica (4 años)",
        "basic.6y": "Básica (6 años)",
        "basic.9y": "Básica (9 años)",
        "high.school": "Secundaria",
        "university.degree": "Universitaria",
        "professional.course": "Formación profesional",
        "illiterate": "Analfabeto",
        "unknown": "Desconocido",
    }
    counts["education_es"] = counts["education"].map(mapping).fillna(counts["education"])
    fig = px.bar(
        counts,
        x="education_es",
        y="proporcion",
        title="Nivel educativo de los clientes",
        text=counts["proporcion"].map(lambda v: f"{v*100:.1f}%"),
    )
    fig.update_xaxes(tickangle=40)
    fig.update_yaxes(tickformat=".0%")
    fig = _fix_plotly(fig, height=430)

    top_row = counts.iloc[0]
    texto = (
        f"El nivel educativo más frecuente es **{top_row['education_es']}**, "
        "lo que sugiere una base de clientes con formación mayoritariamente media o superior."
    )
    return fig, texto


def _map_yes_no_unknown(series: pd.Series, tipo: str):
    if tipo == "housing":
        mapping = {
            "yes": "Con hipoteca",
            "no": "Sin hipoteca",
            "unknown": "Desconocido",
        }
    elif tipo == "loan":
        mapping = {
            "yes": "Con préstamo personal",
            "no": "Sin préstamo personal",
            "unknown": "Desconocido",
        }
    elif tipo == "default":
        mapping = {
            "yes": "Con historial de impago",
            "no": "Sin historial de impago",
            "unknown": "Desconocido",
        }
    else:
        mapping = {"yes": "Sí", "no": "No", "unknown": "Desconocido"}
    return series.map(mapping).fillna(series)


def get_binary_financial_figure(df: pd.DataFrame, col: str, titulo: str):
    counts = df[col].value_counts(normalize=True).reset_index()
    counts.columns = [col, "proporcion"]
    counts["label_es"] = _map_yes_no_unknown(counts[col], col)
    fig = px.bar(
        counts,
        x="label_es",
        y="proporcion",
        title=titulo,
        text=counts["proporcion"].map(lambda v: f"{v*100:.1f}%"),
    )
    fig.update_yaxes(tickformat=".0%")
    fig = _fix_plotly(fig)

    top_row = counts.iloc[0]
    texto = (
        f"La categoría dominante es **{top_row['label_es']}**, "
        f"con aproximadamente el {top_row['proporcion']*100:.1f}% de los clientes."
    )
    return fig, texto


def get_target_distribution_figure(df: pd.DataFrame):
    counts = df["y"].value_counts(normalize=True).reset_index()
    counts.columns = ["y", "proporcion"]
    mapping = {"yes": "Contrató el depósito", "no": "No contrató el depósito"}
    counts["y_es"] = counts["y"].map(mapping).fillna(counts["y"])
    fig = px.bar(
        counts,
        x="y_es",
        y="proporcion",
        title="Resultado de la campaña (variable objetivo)",
        text=counts["proporcion"].map(lambda v: f"{v*100:.1f}%"),
    )
    fig.update_yaxes(tickformat=".0%")
    fig = _fix_plotly(fig)

    prop_yes = counts.loc[counts["y"] == "yes", "proporcion"].iloc[0]
    texto = (
        f"Solo alrededor del {prop_yes*100:.1f}% de los clientes terminó contratando "
        "el depósito, lo que confirma un fuerte desbalance en la variable objetivo."
    )
    return fig, texto


# ======================
# Mapa geográfico
# ======================

def get_geo_density_figure(df: pd.DataFrame):
    """
    En lugar de un mapa de densidad, se muestra un diagrama de dispersión
    de las coordenadas (longitude, latitude) con alta transparencia para
    visualizar la concentración de puntos sin saturar la figura.
    """
    if "latitude" not in df.columns or "longitude" not in df.columns:
        return None, (
            "El dataset no contiene las columnas 'latitude' y 'longitude' "
            "necesarias para representar las coordenadas."
        )

    geo_df = df.dropna(subset=["latitude", "longitude"]).copy()
    if geo_df.empty:
        return None, "No hay coordenadas válidas para representar en el gráfico."

    fig = px.scatter(
        geo_df,
        x="longitude",
        y="latitude",
        opacity=0.15,  # transparencia alta
        title="Dispersión de coordenadas de los clientes",
    )

    # Ejes con nombres claros
    fig.update_xaxes(title="Longitud")
    fig.update_yaxes(title="Latitud")

    # Usamos el helper común para compactar la figura
    fig = _fix_plotly(fig, height=500)

    texto = (
        "Cada punto representa un cliente según sus coordenadas (longitud, latitud). "
        "Las zonas donde se observa mayor concentración de puntos indican áreas con "
        "más clientes, pero sin apoyarse en un mapa de fondo. Es útil para detectar "
        "patrones o agrupaciones generales en los datos geográficos."
    )
    return fig, texto

# ======================
# Estadísticos y textos globales
# ======================
def get_descriptive_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tabla descriptiva profesional:
    - Traducción de nombres de columnas
    - Eliminación de columnas no deseadas
    - Redondeo
    - Reordenación de filas
    """
    # Traducción de nombres
    traduccion = {
        "age": "Edad",
        "duration": "Duración",
        "campaign": "Nº campaña",
        "pdays": "Días desde último contacto",
        "previous": "Nº contactos previos",
        "emp.var.rate": "Tasa empleo",
        "cons.price.idx": "Índice precios",
        "cons.conf.idx": "Índice confianza",
        "euribor3m": "Euribor 3m",
        "nr.employed": "Nº empleados",
        "Income": "Ingresos",
        "Kidhome": "Niños en hogar",
        "Teenhome": "Adolescentes",
        "NumWebVisitsMonth": "Visitas web/mes",
    }

    # Columnas a eliminar (no queremos que aparezcan en la tabla)
    eliminar = [
        "latitude",
        "longitude",
        "Dt_Customer",
        "y_bin",
        "pdays",        # Días desde último contacto
        "previous",     # Nº contactos previos
    ]

    # Filtrar numéricas y aplicar limpieza
    num_df = df.select_dtypes(include="number").drop(columns=eliminar, errors="ignore")

    # Aplicar traducción de nombres
    num_df = num_df.rename(columns=traduccion)

    # Describe
    desc = num_df.describe()

    # Reorden
    orden_filas = ["mean", "std", "min", "25%", "50%", "75%", "max"]
    desc = desc.loc[orden_filas]

    # Redondeo
    desc = desc.round(2)

    # Convertir índice en columna
    desc = desc.reset_index().rename(columns={"index": "Estadístico"})

    return desc

    """
    Tabla descriptiva profesional:
    - Traducción de nombres de columnas
    - Eliminación de columnas no deseadas
    - Redondeo
    - Reordenación de filas
    """
    # Traducción de nombres
    traduccion = {
        "age": "Edad",
        "duration": "Duración",
        "campaign": "Nº campaña",
        "pdays": "Días desde último contacto",
        "previous": "Nº contactos previos",
        "emp.var.rate": "Tasa empleo",
        "cons.price.idx": "Índice precios",
        "cons.conf.idx": "Índice confianza",
        "euribor3m": "Euribor 3m",
        "nr.employed": "Nº empleados",
        "Income": "Ingresos",
        "Kidhome": "Niños en hogar",
        "Teenhome": "Adolescentes",
        "NumWebVisitsMonth": "Visitas web/mes",
    }

    # Columnas a eliminar
    eliminar = [
        "latitude", "longitude", "Dt_Customer", "y_bin"
    ]

    # Filtrar numéricas y aplicar limpieza
    num_df = df.select_dtypes(include="number").drop(columns=eliminar, errors="ignore")

    # Aplicar traducción de nombres
    num_df = num_df.rename(columns=traduccion)

    # Describe
    desc = num_df.describe()

    # Reorden
    orden_filas = ["mean", "std", "min", "25%", "50%", "75%", "max"]
    desc = desc.loc[orden_filas]

    # Redondeo
    desc = desc.round(2)

    # Convertir índice en columna
    desc = desc.reset_index().rename(columns={"index": "Estadístico"})

    return desc

    # Estadísticos descriptivos por defecto
    desc = df.describe()

    # Eliminar la fila "count" del índice si existe
    desc = desc.drop(index="count", errors="ignore")

    # Redondear todos los valores numéricos a 2 decimales
    numeric_cols = desc.select_dtypes(include="number").columns
    desc[numeric_cols] = desc[numeric_cols].round(2)

    # Pasar el índice a columna con un nombre más profesional
    desc = desc.reset_index().rename(columns={"index": "Estadístico"})

    return desc


def generate_summary_metrics(df: pd.DataFrame) -> dict:
    total = len(df)
    n_vars = df.shape[1]

    pos_rate = df["y_bin"].mean() * 100 if "y_bin" in df.columns else None
    avg_age = df["age"].mean() if "age" in df.columns else None
    avg_income = df["Income"].mean() if "Income" in df.columns else None

    housing_yes = (df["housing"] == "yes").mean() * 100 if "housing" in df.columns else None
    loan_yes = (df["loan"] == "yes").mean() * 100 if "loan" in df.columns else None

    return {
        "total_registros": int(total),
        "total_variables": int(n_vars),
        "tasa_conversion": pos_rate,
        "edad_media": avg_age,
        "ingreso_medio": avg_income,
        "porc_housing_yes": housing_yes,
        "porc_loan_yes": loan_yes,
    }


def generate_dataset_info_text(df: pd.DataFrame) -> str:
    m = generate_summary_metrics(df)

    num_demo = ", ".join([c for c in ["age", "Income", "Kidhome", "Teenhome"] if c in df.columns])
    num_digital = ", ".join([c for c in ["NumWebVisitsMonth"] if c in df.columns])
    num_campaign = ", ".join([c for c in ["duration", "campaign", "pdays", "previous"] if c in df.columns])
    num_econ = ", ".join([c for c in ["cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"] if c in df.columns])
    num_geo = ", ".join([c for c in ["latitude", "longitude"] if c in df.columns])

    cat_list = [c for c in ["marital", "job", "education", "housing",
                            "loan", "default", "contact", "poutcome", "y"]
                if c in df.columns]
    cat_str = ", ".join(cat_list)

    date_list = [c for c in ["Dt_Customer", "date"] if c in df.columns]
    date_str = ", ".join(date_list)


def generate_conclusions_text(df: pd.DataFrame) -> str:
    m = generate_summary_metrics(df)

    conv = m["tasa_conversion"]
    edad = m["edad_media"]
    inc = m["ingreso_medio"]
    housing = m["porc_housing_yes"]
    loan = m["porc_loan_yes"]

   
