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

    # Leer la credencial desde archivo secreto (Render)
    creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/agente-atco.json", scope)
    client = gspread.authorize(creds)

    # Abre el documento y la pestaña
    sheet = client.open("0. BASE GENERAL- Cotizador 2024/04/01 (Actualizar PVP)")
    worksheet = sheet.worksheet("GPT")

    # Obtiene todos los registros como lista de diccionarios
    datos = worksheet.get_all_records()

    # Procesar campos sensibles como stock y precio
    for item in datos:
        # Convertir STOCK correctamente (coma decimal -> punto)
        try:
            stock_raw = str(item.get("STOCK", "")).strip().replace(",", ".")
            item["STOCK"] = round(float(stock_raw), 2)  # redondeo a 2 decimales
        except:
            item["STOCK"] = "N/D"

        # Convertir PVP a número limpio
        try:
            precio_raw = str(item.get("PVP", "")).replace("$", "").replace(",", "").strip()
            item["PVP"] = round(float(precio_raw), 2)
        except:
            item["PVP"] = "N/D"

    return datos
