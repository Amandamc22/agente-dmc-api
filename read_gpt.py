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
        # Convertir stock a número flotante o 'N/D'
        try:
            stock_raw = str(item.get("STOCK", "")).replace(",", ".")
            item["STOCK"] = float(stock_raw)
        except:
            item["STOCK"] = "N/D"

        # Convertir precio a número flotante limpio si es posible
        try:
            precio_raw = str(item.get("PVP", "")).replace("$", "").replace(",", "").strip()
            item["PVP"] = float(precio_raw)
        except:
            item["PVP"] = "N/D"

    return datos
