import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def suma(a, b):
    """
    Función que suma dos números.

    Args:
        a (int, float): Primer número.
        b (int, float): Segundo número.

    Returns:
        int, float: La suma de los dos números.
    """
    return a + b

def excluir_nombres(df):
    nombres_excluir = ["CIDAL", "LAVANDERIA", "GIMNASIO"]
    df = df[
        ~df["NOMBRE Y APELLIDO"].str.contains(
            "|".join(nombres_excluir),
            case=False,
            na=False
        )
    ]
    return df

def pagado_vs_porpagar(df):
    #Lo que se deberia pagar sin CIDAL ni espacios comunes como lavanderia ni gimnacio
    total_a_pagar = round(df["TOTAL"].sum(), 2)
    total_pagado = 0
    for indice, fila in df.iterrows():
        if fila["PAGO?"].strip() == "S" or fila["PAGO?"].strip() == "s":
            total_pagado += round(fila["TOTAL"], 2)
        else:
            pago_str = str(fila["PAGO?"]).strip()
            if len(pago_str) > 0:
                pago_str = pago_str.replace(",", ".")
                total_pagado += round(float(pago_str), 2)
    return round(total_a_pagar, 2), round(total_pagado, 2)

# Funciones ingresos vs egresos por mes
def convertir_float(valor):
    if pd.isna(valor):
        return 0.0

    valor = str(valor).strip()
    valor = valor.replace(" ", "")

    if "," in valor and "." in valor:
        # Ejemplo: 29,328.87
        valor = valor.replace(",", "")
    elif "," in valor:
        # Ejemplo: 193,29
        valor = valor.replace(",", ".")

    return abs(float(valor))

def ingresos_vs_egresos(df):
    ingreso = round(df[df["Ingreso"] == "x"]["Monto"].sum(), 2)
    egreso = round(df[df["Egreso"] == "x"]["Monto"].sum(), 2)
    return ingreso, egreso

def colorear_valor(valor):
    if valor < 0:
        return "color: red; font-weight: bold"
    elif valor > 0:
        return "color: green; font-weight: bold"
    return "color: black"

def deglos_ingresos_egresos(df_mes):
    df_ingresos = df_mes[df_mes["Ingreso"] == "x"]  
    resultado_ingresos = (
        df_ingresos.groupby("Descripcion", as_index=False)["Monto"]
          .sum()
    )
    resultado_ingresos = resultado_ingresos.set_index("Descripcion")

    df_egresos = df_mes[df_mes["Egreso"] == "x"]  
    
    resultado_egresos = (
        df_egresos.groupby("Descripcion", as_index=False)["Monto"]
          .sum()
    )
    
    resultado_egresos = resultado_egresos.set_index("Descripcion")

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Barra de ingresos
    base = 0
    for categoria, monto in resultado_ingresos["Monto"].items():
        ax.bar("Ingresos", monto, bottom=base, label=categoria)
        base += monto
    
    # Barra de egresos
    base = 0
    for categoria, monto in resultado_egresos["Monto"].items():
        ax.bar("Egresos", monto, bottom=base, label=categoria)
        base += monto
    
    ax.set_title("Ingresos y egresos del edificio")
    ax.set_ylabel("Monto (Bs)")
    ax.legend(title="Categorías", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()
    
    tabla = pd.concat(
    [
        resultado_ingresos["Monto"].rename("Ingresos (Bs)"),
        resultado_egresos["Monto"].rename("Egresos (Bs)")
        
    ],axis=1).fillna(0)

    tabla["Saldo"] = tabla["Ingresos (Bs)"] - tabla["Egresos (Bs)"]
    
    tabla.index.name = "Descripción"
    
    # Agregar fila de totales
    tabla.loc["TOTAL"] = tabla.sum()
    
    display(tabla.style
        .format("{:,.2f}")
        .map(colorear_valor, subset=["Saldo"])
        .set_caption("RESUMEN ECONÓMICO DEL EDIFICIO")
        .set_properties(**{"text-align": "right"})
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#34495e"),
                ("color", "white"),
                ("text-align", "center")
            ]},
            {"selector": "caption", "props": [
                ("font-size", "16px"),
                ("font-weight", "bold")
            ]}
        ])
    )