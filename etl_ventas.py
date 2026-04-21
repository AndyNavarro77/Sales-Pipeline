import pandas as pd
import os
from sqlalchemy import create_engine
import random
from datetime import datetime

# -------------------------
# CONFIG
# -------------------------
DATA_PATH = "data/ventas.xlsx"

# -------------------------
# CONFIG DB
# -------------------------
DB_USER = "root"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "sales_pipeline"

# -------------------------
# GENERAR NUEVAS VENTAS
# -------------------------
def generar_nuevas_ventas():
    nuevos = []

    for _ in range(30):
        nuevos.append({
            "fecha": datetime.now(),
            "producto": random.choice(["Notebook", "Mouse", "Monitor"]),
            "categoria": "Tecnología",
            "cantidad": random.randint(1, 3),
            "precio_unitario": random.randint(50, 500),
            "canal": random.choice(["Online", "Tienda"]),
            "vendedor": random.choice(["Juan", "Ana", "Luis"]),
            "cliente_id": random.randint(1000, 2000)
        })

    return pd.DataFrame(nuevos)

# -------------------------
# EXTRAER (ACTUALIZA DATOS)
# -------------------------
def extraer_datos():
    try:
        df_existente = pd.read_excel(DATA_PATH)

        nuevos = generar_nuevas_ventas()

        df_total = pd.concat([df_existente, nuevos], ignore_index=True)

        df_total.to_excel(DATA_PATH, index=False)

        print(f"[INFO] Datos actualizados: {df_total.shape[0]} filas")

        return df_total

    except Exception as e:
        print("[ERROR] No se pudo leer/generar datos:", e)
        return None

# -------------------------
# TRANSFORMAR
# -------------------------
def transformar_datos(df):
    try:
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['revenue'] = df['cantidad'] * df['precio_unitario']
        df['producto'] = df['producto'].str.strip()
        df['categoria'] = df['categoria'].str.strip()

        print("[INFO] Transformación completada")
        return df

    except Exception as e:
        print("[ERROR] Error en transformación:", e)
        return None

# -------------------------
# AGREGACIONES
# -------------------------
def generar_agregaciones(df):
    try:
        return {
            "ventas_por_dia": df.groupby('fecha')['revenue'].sum().reset_index(),
            "ventas_por_producto": df.groupby('producto')['revenue'].sum().reset_index(),
            "ventas_por_vendedor": df.groupby('vendedor')['revenue'].sum().reset_index(),
            "ventas_por_canal": df.groupby('canal')['revenue'].sum().reset_index()
        }
    except Exception as e:
        print("[ERROR] Error en agregaciones:", e)
        return None

# -------------------------
# GUARDAR CSV
# -------------------------
def guardar_csv(df):
    df.to_csv("data/ventas_limpio.csv", index=False)
    print("[INFO] CSV guardado")

# -------------------------
# GUARDAR AGREGADOS
# -------------------------
def guardar_agregaciones(agregados):
    for k, v in agregados.items():
        v.to_csv(f"data/{k}.csv", index=False)
    print("[INFO] Agregados guardados")

# -------------------------
# ALERTAS
# -------------------------
def generar_alertas(df):
    try:
        alertas = []

        promedio = df['revenue'].mean()
        total = df['revenue'].sum()

        if total < promedio:
            alertas.append("⚠ Ventas por debajo del promedio")

        ventas_vendedor = df.groupby('vendedor')['revenue'].sum()

        for vendedor, valor in ventas_vendedor.items():
            if valor < promedio * 0.5:
                alertas.append(f"⚠ Bajo rendimiento: {vendedor}")

        if not alertas:
            alertas.append("OK")

        return alertas

    except Exception as e:
        print("[ERROR] Alertas:", e)
        return []

# -------------------------
# REPORTE DIARIO
# -------------------------
def generar_reporte(df):
    try:
        hoy = df['fecha'].dt.date.max()
        df_hoy = df[df['fecha'].dt.date == hoy]

        total = df_hoy['revenue'].sum()
        unidades = df_hoy['cantidad'].sum()

        top_vendedor = (
            df_hoy.groupby('vendedor')['revenue']
            .sum()
            .idxmax()
        )

        return {
            "fecha": str(hoy),
            "ventas": round(total, 2),
            "unidades": int(unidades),
            "top_vendedor": top_vendedor
        }

    except Exception as e:
        print("[ERROR] Reporte:", e)
        return {}

# -------------------------
# MYSQL
# -------------------------
def conectar_db():
    return create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

def cargar_a_mysql(df, agregados, engine):
    df.to_sql("ventas", con=engine, if_exists="append", index=False)

    for k, v in agregados.items():
        v.to_sql(k, con=engine, if_exists="replace", index=False)

    print("[INFO] Datos en MySQL")

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    df = extraer_datos()

    if df is not None:
        df = transformar_datos(df)

        if df is not None:
            guardar_csv(df)

            agregados = generar_agregaciones(df)

            if agregados:
                guardar_agregaciones(agregados)

                alertas = generar_alertas(df)
                reporte = generar_reporte(df)

                print("[REPORTE]:", reporte)
                print("[ALERTAS]:", alertas)

                engine = conectar_db()
                cargar_a_mysql(df, agregados, engine)

            print(df.head())