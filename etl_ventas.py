import pandas as pd
import os
import smtplib
from email.message import EmailMessage
from sqlalchemy import create_engine
import random
from datetime import datetime
from dotenv import load_dotenv

# -------------------------
# CONFIG
# -------------------------
DATA_PATH = "data/ventas.xlsx"

# -------------------------
# CONFIG DB & EMAIL
# -------------------------
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# -------------------------
# GENERATE NEW SALES
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
# EXTRACT
# -------------------------
def extraer_datos():
    try:
        df_existente = pd.read_excel(DATA_PATH)
        nuevos = generar_nuevas_ventas()
        df_total = pd.concat([df_existente, nuevos], ignore_index=True)
        df_total.to_excel(DATA_PATH, index=False)
        print(f"[INFO] Data updated: {df_total.shape[0]} rows")
        return df_total
    except Exception as e:
        print("[ERROR] Could not read/generate data:", e)
        return None

# -------------------------
# TRANSFORM
# -------------------------
def transformar_datos(df):
    try:
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['revenue'] = df['cantidad'] * df['precio_unitario']
        df['producto'] = df['producto'].str.strip()
        df['categoria'] = df['categoria'].str.strip()
        print("[INFO] Transformation complete")
        return df
    except Exception as e:
        print("[ERROR] Transformation error:", e)
        return None

# -------------------------
# AGGREGATIONS
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
        print("[ERROR] Aggregation error:", e)
        return None

# -------------------------
# SAVE CSV
# -------------------------
def guardar_csv(df):
    df.to_csv("data/ventas_limpio.csv", index=False)
    print("[INFO] CSV saved")

def guardar_agregaciones(agregados):
    for k, v in agregados.items():
        v.to_csv(f"data/{k}.csv", index=False)
    print("[INFO] Aggregations saved")

# -------------------------
# ALERT ENGINE
# -------------------------
def generar_alertas(df):
    try:
        alertas = []
        promedio = df['revenue'].mean()
        total = df['revenue'].sum()

        if total < promedio:
            alertas.append("⚠ Sales below average threshold")

        ventas_vendedor = df.groupby('vendedor')['revenue'].sum()
        for vendedor, valor in ventas_vendedor.items():
            if valor < promedio * 0.5:
                alertas.append(f"⚠ Low performance detected: {vendedor}")

        if not alertas:
            alertas.append("OK")

        return alertas
    except Exception as e:
        print("[ERROR] Alert engine:", e)
        return []

# -------------------------
# DAILY REPORT
# -------------------------
def generar_reporte(df):
    try:
        hoy = df['fecha'].dt.date.max()
        df_hoy = df[df['fecha'].dt.date == hoy]

        total = df_hoy['revenue'].sum()
        unidades = df_hoy['cantidad'].sum()
        ticket_promedio = total / unidades if unidades > 0 else 0

        top_vendedor = (
            df_hoy.groupby('vendedor')['revenue'].sum().idxmax()
        )

        top_producto = (
            df_hoy.groupby('producto')['revenue'].sum().idxmax()
        )

        ventas_canal = df_hoy.groupby('canal')['revenue'].sum()
        canal_online = ventas_canal.get('Online', 0)
        canal_tienda = ventas_canal.get('Tienda', 0)
        pct_online = (canal_online / total * 100) if total > 0 else 0
        pct_tienda = (canal_tienda / total * 100) if total > 0 else 0

        return {
            "fecha": str(hoy),
            "revenue": round(float(total), 2),
            "unidades": int(unidades),
            "ticket_promedio": round(float(ticket_promedio), 2),
            "top_vendedor": top_vendedor,
            "top_producto": top_producto,
            "canal_online": round(float(canal_online), 2),
            "canal_tienda": round(float(canal_tienda), 2),
            "pct_online": round(float(pct_online), 1),
            "pct_tienda": round(float(pct_tienda), 1),
            "total_records": len(df)
        }
    except Exception as e:
        print("[ERROR] Daily report:", e)
        return {}

# -------------------------
# EMAIL REPORT
# -------------------------
def enviar_reporte_mail(reporte, alertas):
    try:
        fecha = reporte.get("fecha", "N/A")
        revenue = f"${reporte.get('revenue', 0):,.0f}".replace(",", ".")
        unidades = reporte.get("unidades", 0)
        ticket = f"${reporte.get('ticket_promedio', 0):,.0f}".replace(",", ".")
        top_vendedor = reporte.get("top_vendedor", "N/A")
        top_producto = reporte.get("top_producto", "N/A")
        canal_online = f"${reporte.get('canal_online', 0):,.0f}".replace(",", ".")
        canal_tienda = f"${reporte.get('canal_tienda', 0):,.0f}".replace(",", ".")
        pct_online = reporte.get("pct_online", 0)
        pct_tienda = reporte.get("pct_tienda", 0)
        total_records = reporte.get("total_records", 0)
        fecha_hora = datetime.now().strftime("%m/%d/%Y · %I:%M %p")

        alertas_sin_ok = [a for a in alertas if a != "OK"]
        if alertas_sin_ok:
            alert_html = f"""
            <div style="background:#FAEEDA;border:1px solid #EF9F27;border-radius:8px;padding:12px 14px;font-size:13px;color:#633806;margin-top:16px;">
              {'<br>'.join(alertas_sin_ok)}
            </div>"""
        else:
            alert_html = """
            <div style="background:#EAF3DE;border:1px solid #639922;border-radius:8px;padding:12px 14px;font-size:13px;color:#27500A;margin-top:16px;">
              &#10003; All systems normal — no performance alerts triggered.
            </div>"""

        html = f"""
        <html><body style="margin:0;padding:0;font-family:Arial,sans-serif;background:#f4f4f4;">
        <div style="max-width:600px;margin:20px auto;background:#ffffff;border-radius:10px;overflow:hidden;border:1px solid #e0e0e0;">

          <div style="background:#0C447C;padding:22px 26px;">
            <h1 style="color:#E6F1FB;font-size:17px;font-weight:600;margin:0 0 4px;">Sales Pipeline Report — Daily Summary</h1>
            <p style="color:#85B7EB;font-size:12px;margin:0;">Automated daily report · {fecha_hora}</p>
          </div>

          <div style="padding:22px 26px;">
            <p style="font-size:13px;color:#555;margin:0 0 16px;">Hi Andrés, the pipeline ran successfully. Here is today's sales summary:</p>

            <table width="100%" cellspacing="0" cellpadding="0" style="margin-bottom:16px;">
              <tr>
                <td width="25%" style="padding:4px;">
                  <div style="background:#f5f5f5;border-radius:8px;padding:10px 12px;">
                    <p style="font-size:11px;color:#888;margin:0 0 3px;">Today's Revenue</p>
                    <p style="font-size:19px;font-weight:600;color:#3B6D11;margin:0;">{revenue}</p>
                  </div>
                </td>
                <td width="25%" style="padding:4px;">
                  <div style="background:#f5f5f5;border-radius:8px;padding:10px 12px;">
                    <p style="font-size:11px;color:#888;margin:0 0 3px;">Units Sold</p>
                    <p style="font-size:19px;font-weight:600;color:#185FA5;margin:0;">{unidades}</p>
                  </div>
                </td>
                <td width="25%" style="padding:4px;">
                  <div style="background:#f5f5f5;border-radius:8px;padding:10px 12px;">
                    <p style="font-size:11px;color:#888;margin:0 0 3px;">Avg. Ticket</p>
                    <p style="font-size:19px;font-weight:600;color:#BA7517;margin:0;">{ticket}</p>
                  </div>
                </td>
                <td width="25%" style="padding:4px;">
                  <div style="background:#f5f5f5;border-radius:8px;padding:10px 12px;">
                    <p style="font-size:11px;color:#888;margin:0 0 3px;">Top Rep</p>
                    <p style="font-size:19px;font-weight:600;color:#993C1D;margin:0;">{top_vendedor}</p>
                  </div>
                </td>
              </tr>
            </table>

            <table width="100%" style="font-size:13px;border-collapse:collapse;margin-bottom:4px;">
              <tr style="border-top:1px solid #eee;">
                <td style="padding:7px 4px;color:#888;">Online channel</td>
                <td style="padding:7px 4px;text-align:right;font-weight:600;">{canal_online} ({pct_online}%)</td>
              </tr>
              <tr style="border-top:1px solid #eee;">
                <td style="padding:7px 4px;color:#888;">In-store channel</td>
                <td style="padding:7px 4px;text-align:right;font-weight:600;">{canal_tienda} ({pct_tienda}%)</td>
              </tr>
              <tr style="border-top:1px solid #eee;">
                <td style="padding:7px 4px;color:#888;">Top product</td>
                <td style="padding:7px 4px;text-align:right;font-weight:600;">{top_producto}</td>
              </tr>
              <tr style="border-top:1px solid #eee;">
                <td style="padding:7px 4px;color:#888;">Total records processed</td>
                <td style="padding:7px 4px;text-align:right;font-weight:600;">{total_records:,}</td>
              </tr>
              <tr style="border-top:1px solid #eee;">
                <td style="padding:7px 4px;color:#888;">Database</td>
                <td style="padding:7px 4px;text-align:right;font-weight:600;">MySQL · sales_pipeline</td>
              </tr>
            </table>

            {alert_html}
          </div>

          <div style="padding:10px 26px;background:#f9f9f9;border-top:1px solid #eee;font-size:11px;color:#aaa;">
            <span>Automated pipeline · Task Scheduler</span>&nbsp;&nbsp;|&nbsp;&nbsp;
            <span>Andrés Navarro · github.com/AndyNavarro77</span>
          </div>

        </div>
        </body></html>
        """

        msg = EmailMessage()
        msg['Subject'] = f"📊 Sales Report — Revenue: {revenue} | Units: {unidades} | Top Rep: {top_vendedor}"
        msg['From'] = EMAIL_REMITENTE
        msg['To'] = EMAIL_REMITENTE
        msg.set_content("This email requires an HTML-compatible email client.")
        msg.add_alternative(html, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("[INFO] Email report sent successfully.")
    except Exception as e:
        print(f"[ERROR] Email error: {e}")

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
    print("[INFO] Data loaded into MySQL")

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

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

                print("[REPORT]:", reporte)
                print("[ALERTS]:", alertas)

                engine = conectar_db()
                cargar_a_mysql(df, agregados, engine)
                enviar_reporte_mail(reporte, alertas)

            print(df.head())
        print("[INFO] Pipeline completed successfully.")
    else:
        print("[ERROR] Pipeline could not be executed.")