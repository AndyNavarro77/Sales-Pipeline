import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# -------------------------
# CONFIG
# -------------------------
NUM_REGISTROS = 5000

productos = {
    "Notebook": "Tecnología",
    "Mouse": "Tecnología",
    "Teclado": "Tecnología",
    "Silla": "Hogar",
    "Mesa": "Hogar",
    "Auriculares": "Tecnología",
    "Monitor": "Tecnología",
    "Lámpara": "Hogar"
}

precios_base = {
    "Notebook": 1200,
    "Mouse": 20,
    "Teclado": 50,
    "Silla": 150,
    "Mesa": 300,
    "Auriculares": 80,
    "Monitor": 400,
    "Lámpara": 60
}

canales = ["Online", "Tienda"]
vendedores = ["Juan", "Ana", "Luis", "Sofía", "Carlos"]

# -------------------------
# GENERAR DATOS
# -------------------------
data = []

fecha_inicio = datetime(2024, 1, 1)

for i in range(NUM_REGISTROS):
    fecha = fecha_inicio + timedelta(days=random.randint(0, 180))

    producto = random.choice(list(productos.keys()))
    categoria = productos[producto]

    cantidad = np.random.randint(1, 5)

    # variación de precio
    precio = precios_base[producto] * random.uniform(0.9, 1.1)

    canal = random.choice(canales)

    # vendedores con distinto rendimiento
    vendedor = random.choices(
        vendedores,
        weights=[30, 25, 20, 15, 10]  # Juan vende más
    )[0]

    cliente_id = random.randint(1000, 2000)

    data.append([
        fecha,
        producto,
        categoria,
        cantidad,
        round(precio, 2),
        canal,
        vendedor,
        cliente_id
    ])

# -------------------------
# DATAFRAME
# -------------------------
df = pd.DataFrame(data, columns=[
    "fecha",
    "producto",
    "categoria",
    "cantidad",
    "precio_unitario",
    "canal",
    "vendedor",
    "cliente_id"
])

# -------------------------
# GUARDAR EXCEL
# -------------------------
df.to_excel("data/ventas.xlsx", index=False)

print("Excel generado con éxito")
print(df.head())