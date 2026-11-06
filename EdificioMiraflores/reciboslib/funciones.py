import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:pgadmin1325@localhost:5432/edificiomiraflores_bd")

def fetch_ultimo_recibo():
    pd.read_sql("SELECT COALESCE(MAX(nro_recibo) + 1, 0) AS max_nro_recibo FROM recibos;", engine)["max_nro_recibo"].iloc[0]
    if nro_recibo == 0:
        nro_recibo = 962
    return nro_recibo

def lectura_planillas(url):
    df = pd.read_csv(
        url,
        sep=";",
        decimal=",",
        encoding="latin-1"
    )
    return df

def lectura_planillas_utf8(url):
    df = pd.read_csv(
        url,
        sep=",",
        decimal=".",
        encoding="UTF-8"
    )
    return df
