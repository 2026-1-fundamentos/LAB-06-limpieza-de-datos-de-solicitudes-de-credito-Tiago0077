"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import os


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    def normalize_text(series = pd.Series):
        
        s = series.astype("string").str.lower()
        s = s.str.replace("_", " ", regex=False).str.replace("-", " ", regex=False)
        s = s.str.replace(r"\s+", " ", regex=True)
        return s


    def parse_fecha(valor):

        if pd.isna(valor):
            return pd.NaT
        valor = str(valor).strip()
        for fmt in ("%d/%m/%Y", "%Y/%m/%d"):
            try:
                return pd.to_datetime(valor, format=fmt)
            except ValueError:
                continue
        return pd.to_datetime(valor, errors="coerce", dayfirst=True)


    def clean_monto(valor):

        if pd.isna(valor):
            return None
        valor = str(valor)
        valor = valor.replace("$", "").replace(",", "").replace(".00", "").strip()
        valor = valor.replace(" ", "")
        try:
            return float(valor)
        except ValueError:
            return None 

    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    text_cols = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for col in text_cols:
        df[col] = normalize_text(df[col])

    df["monto_del_credito"] = df["monto_del_credito"].apply(clean_monto)

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(parse_fecha)
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].dt.strftime("%Y-%m-%d")

    df = df.dropna(subset=["tipo_de_emprendimiento", "barrio"])

    df = df.drop_duplicates()

    df["monto_del_credito"] = df["monto_del_credito"].astype(int)

    df = df.reset_index(drop=True)

    os.makedirs("files/output", exist_ok=True)

    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)      
    

pregunta_01()


