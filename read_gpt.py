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

    # Ruta al archivo secreto en Render
    cred_path = "/etc/secrets/agente-atco.json"

    # 🔍 Diagnóstico temporal
    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"❌ El archivo no existe en la ruta: {cred_path}")

    try:
        with open(cred_path, 'r') as f:
            contenido = f.read()
        print("✅ Archivo leído correctamente.")
        print("🔐 Contenido parcial (primeros 200 caracteres):")
        print(contenido[:200])
    except Exception as e:
        raise Exception(f"❌ Error al leer el archivo: {e}")

    # Validar que sea un JSON válido
    try:
        json.loads(contenido)
        print("✅ El contenido es un JSON válido.")
    except Exception as e:
        raise Exception(f"❌ El archivo no contiene un JSON válido: {e}")

    # Autenticación con Google Sheets
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
    client = gspread.authorize(creds)

    # Abre el documento y la pestaña
    sheet = client.open("0. BASE GENERAL- Cotizador 2024/04/01 (Actualizar PVP)")
    worksheet = sheet.worksheet("GPT")

    # Obtiene todos los registros como lista de diccionarios
    datos = worksheet.get_all_records()

    # Procesar campos sensibles como stock y precio
    for item in datos:
        # STOCK
        try:
            valor_stock = str(item.get("STOCK", "")).strip().lower()
            if valor_stock in ("", "#n/a", "#ref!", "n/a"):
                item["STOCK"] = "N/D"
            else:
                item["STOCK"] = round(float(valor_stock), 2)
        except:
            item["STOCK"] = "N/D"

        # PRECIO
        try:
            valor_precio = str(item.get("PRECIO", "")).strip().lower()
            if valor_precio in ("", "#n/a", "#ref!", "n/a"):
                item["PRECIO"] = "N/D"
            else:
                item["PRECIO"] = round(float(valor_precio), 2)
        except:
            item["PRECIO"] = "N/D"

    return datos
