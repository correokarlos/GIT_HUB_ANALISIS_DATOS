import pandas as pd
from sqlalchemy import create_engine

# ============= CONFIGURACIÓN =============

# Rutas a los ficheros de datos
CSV_PATH = "bank-additional.csv"
EXCEL_PATH = "customer-details.xlsx"

# Parámetros de conexión a PostgreSQL
PG_USER = "postgres"
PG_PASSWORD = "admin"
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DB_NAME = "bank_marketing"   # BD YA EXISTENTE

# =========================================


def get_db_engine():
    """
    Conexión directa a la BD de trabajo.
    IMPORTANTE: la BD debe existir previamente.
    """
    url = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"
    return create_engine(url)


def load_bank_additional() -> pd.DataFrame:
    """
    Carga el CSV bank-additional.csv.
    """
    print("Cargando bank-additional.csv...")
    df = pd.read_csv(CSV_PATH)
    return df


def load_customer_details() -> pd.DataFrame:
    """
    Carga TODAS las hojas del Excel customer-details.xlsx y las concatena.
    """
    print("Cargando customer-details.xlsx (todas las hojas)...")
    xls = pd.ExcelFile(EXCEL_PATH)
    frames = []

    for sheet in xls.sheet_names:
        print(f" - Leyendo hoja: {sheet}")
        tmp = pd.read_excel(EXCEL_PATH, sheet_name=sheet)
        frames.append(tmp)

    df = pd.concat(frames, ignore_index=True)

    # Eliminamos columnas técnicas típicas
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    return df


def main():
    # 1. Crear engine contra la BD (YA EXISTENTE)
    engine = get_db_engine()
    print(f"Conectado a la base de datos existente: {PG_DB_NAME}")

    # 2. Cargar datos en memoria
    df_bank = load_bank_additional()
    df_cust = load_customer_details()

    # 3. Volcar a PostgreSQL
    print("Volcando tabla bank_additional...")
    df_bank.to_sql("bank_additional", engine, if_exists="replace", index=False)

    print("Volcando tabla customer_details...")
    df_cust.to_sql("customer_details", engine, if_exists="replace", index=False)


    print("Proceso completado.")
    print(f"Base de datos utilizada (NO creada): {PG_DB_NAME}")
    print("Tablas creadas/actualizadas: bank_additional, customer_details")


if __name__ == "__main__":
    main()
