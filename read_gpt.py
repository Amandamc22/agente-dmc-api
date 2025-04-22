import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

def leer_hoja_gpt():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Leer desde la variable de entorno
    cred_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")

    if not cred_json:
        raise Exception("❌ No se encontró la variable 'GOOGLE_SHEETS_CREDENTIALS'.")

    try:
        cred_data = json.loads(cred_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_data, scope)
        print("✅ Credenciales cargadas desde variable de entorno.")
    except Exception as e:
        raise Exception(f"❌ Error al procesar la credencial JSON desde variable: {e}")

    client = gspread.authorize(creds)

    sheet = client.open("0. BASE GENERAL- Cotizador 2024/04/01 (Actualizar PVP)")
    worksheet = sheet.worksheet("GPT")

    datos = worksheet.get_all_records()

    for item in datos:
        try:
            valor_stock = str(item.get("STOCK", "")).strip().lower()
            if valor_stock in ("", "#n/a", "#ref!", "n/a"):
                item["STOCK"] = "N/D"
            else:
                item["STOCK"] = round(float(valor_stock), 2)
        except:
            item["STOCK"] = "N/D"

        try:
            valor_precio = str(item.get("PRECIO", "")).strip().lower()
            if valor_precio in ("", "#n/a", "#ref!", "n/a"):
                item["PRECIO"] = "N/D"
            else:
                item["PRECIO"] = round(float(valor_precio), 2)
        except:
            item["PRECIO"] = "N/D"

    return datos
