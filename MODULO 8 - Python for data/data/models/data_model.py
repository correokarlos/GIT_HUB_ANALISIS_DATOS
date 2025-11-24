from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================
BASE_PATH = Path(__file__).resolve().parents[1] / "data"
BANK_PATH = BASE_PATH / "bank-additional.csv"
CUSTOMER_PATH = BASE_PATH / "customer-details.xlsx"
MERGED_PATH = BASE_PATH / "merged_dataset.csv"

# ============================================================
# CONFIGURACIÓN POSTGRES (AJUSTAR A TU ENTORNO)
# ============================================================
PG_USER = "postgres"
PG_PASSWORD = "admin"
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DB_NAME = "bank_marketing"   # BD existente donde están las tablas originales

# Cache en memoria
_DATA_CACHE = None


# -------------------------------------------------------------------
# 1. Carga de datos desde FICHEROS
# -------------------------------------------------------------------
def _load_raw_bank_from_files() -> pd.DataFrame:
    """Carga el CSV bank-additional.csv desde /data."""
    return pd.read_csv(BANK_PATH)


def _load_raw_customers_from_files() -> pd.DataFrame:
    """Carga TODAS las hojas de customer-details.xlsx y las concatena."""
    xls = pd.ExcelFile(CUSTOMER_PATH)
    frames = []

    for sheet in xls.sheet_names:
        tmp = pd.read_excel(CUSTOMER_PATH, sheet_name=sheet)
        frames.append(tmp)

    df = pd.concat(frames, ignore_index=True)

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    return df


# -------------------------------------------------------------------
# 2. Carga de datos desde POSTGRES
# -------------------------------------------------------------------
def _get_pg_engine():
    url = (
        f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}"
        f"@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"
    )
    return create_engine(url)


def _load_raw_from_postgres() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga las tablas originales desde PostgreSQL:
    - bank_additional
    - customer_details
    """
    print("[INFO] Cargando datos desde PostgreSQL...")
    engine = _get_pg_engine()

    df_bank = pd.read_sql_table("bank_additional", con=engine)
    df_cust = pd.read_sql_table("customer_details", con=engine)

    return df_bank, df_cust


# -------------------------------------------------------------------
# 3. Fusión bank + customers
# -------------------------------------------------------------------
def _merge_bank_and_customers(df_bank: pd.DataFrame,
                              df_cust: pd.DataFrame) -> pd.DataFrame:
    """
    Une el CSV bancario y el Excel/tabla de clientes usando el identificador común.
    - En bank-additional la clave es 'id_'
    - En customer-details la clave original suele ser 'ID'
    """
    if "ID" in df_cust.columns:
        df_cust = df_cust.rename(columns={"ID": "id_"})

    merged = df_bank.merge(
        df_cust,
        on="id_",
        how="inner",
        suffixes=("", "_cust"),
    )
    return merged


# -------------------------------------------------------------------
# 4. Limpieza y transformación común
# -------------------------------------------------------------------
def _clean_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()

    # Eliminar columnas técnicas
    cols_to_drop = [c for c in df.columns if c.startswith("Unnamed:")]
    cols_to_drop += ["ID", "id_"]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns],
                 errors="ignore")

    # Conversión coma→punto
    num_comma_cols = ["cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"]
    for col in num_comma_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .replace(
                    {
                        "nan": np.nan,
                        "None": np.nan,
                        "none": np.nan,
                        "": np.nan,
                    }
                )
            )
            # Conversión robusta a float
            df[col] = pd.to_numeric(df[col], errors="coerce")


    # Fechas
    if "Dt_Customer" in df.columns:
        df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], errors="coerce")

    if "date" in df.columns:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

    # Binarias financieras
    bin_cols = ["default", "housing", "loan"]
    for col in bin_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).replace({"0.0": "no", "1.0": "yes"})
            df[col] = df[col].replace({"nan": np.nan}).fillna("unknown")

    # Edad
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df["age"] = df["age"].fillna(df["age"].median())


    # Categóricas
    for col in ["job", "marital", "education"]:
        if col in df.columns:
            df[col] = df[col].fillna("unknown")

    # Macroeconómicas
    for col in ["cons.price.idx", "euribor3m"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Variable objetivo binaria
    if "y" in df.columns:
        df["y"] = df["y"].astype(str).str.lower()
        df["y_bin"] = df["y"].map({"no": 0, "yes": 1}).astype(int)

    return df


# -------------------------------------------------------------------
# 5. Construcción de merged_dataset desde FICHEROS
# -------------------------------------------------------------------
def _build_merged_from_files() -> pd.DataFrame:
    print("[INFO] Generando merged_dataset a partir de CSV + Excel...")
    df_bank = _load_raw_bank_from_files()
    df_cust = _load_raw_customers_from_files()
    merged_raw = _merge_bank_and_customers(df_bank, df_cust)
    clean_df = _clean_data(merged_raw)

    clean_df.to_csv(MERGED_PATH, index=False)
    print(f"[INFO] merged_dataset.csv generado en: {MERGED_PATH}")
    return clean_df


# -------------------------------------------------------------------
# 6. Construcción de merged_dataset desde POSTGRES
# -------------------------------------------------------------------
def _build_merged_from_postgres() -> pd.DataFrame:
    print("[INFO] Generando merged_dataset a partir de la BD PostgreSQL...")
    df_bank, df_cust = _load_raw_from_postgres()
    merged_raw = _merge_bank_and_customers(df_bank, df_cust)
    clean_df = _clean_data(merged_raw)

    clean_df.to_csv(MERGED_PATH, index=False)
    print(f"[INFO] merged_dataset.csv generado desde PostgreSQL en: {MERGED_PATH}")
    return clean_df


# -------------------------------------------------------------------
# 7. Punto de entrada: load_data()
# -------------------------------------------------------------------
def load_data() -> pd.DataFrame:
    """
    Lógica solicitada:

    1) Si _DATA_CACHE ya está cargado → devolverlo directamente.
    2) Si merged_dataset.csv EXISTE:
         - Leerlo, limpiar ligeramente y devolverlo.
    3) Si merged_dataset.csv NO existe:
         - Preguntar al usuario en consola:
             [1] Generar desde CSV + Excel
             [2] Generar desde BD PostgreSQL
         - Ejecutar la opción elegida
         - Guardar merged_dataset.csv
         - Devolver el DataFrame limpio.
    """
    global _DATA_CACHE

    # 1) Cache en memoria
    if _DATA_CACHE is not None:
        return _DATA_CACHE

    # 2) merged_dataset.csv existe → usarlo
    if MERGED_PATH.exists():
        print(f"[INFO] Usando merged_dataset existente: {MERGED_PATH}")
        raw_merged = pd.read_csv(MERGED_PATH)
        df = _clean_data(raw_merged)
        _DATA_CACHE = df
        return df

    # 3) merged_dataset.csv NO existe → preguntar al usuario
    print("\n[AVISO] El archivo 'merged_dataset.csv' no existe en la carpeta /data.")
    print("¿Cómo desea generarlo?")
    print("  [1] A partir de los ficheros originales (bank-additional.csv + customer-details.xlsx)")
    print("  [2] A partir de la base de datos PostgreSQL (tablas bank_additional y customer_details)")
    opcion = None
    while opcion not in ("1", "2"):
        opcion = input("Seleccione una opción (1/2): ").strip()

    if opcion == "1":
        df = _build_merged_from_files()
    else:
        df = _build_merged_from_postgres()

    _DATA_CACHE = df
    return df
