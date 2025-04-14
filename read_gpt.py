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
        # STOCK
        try:
            valor_stock = str(item.get("STOCK", "")).strip().lower()
            if valor_stock in ("", "#n/a", "#ref!", "n/a"):
                item["STOCK"] = "N/D"
            else:
                item["STOCK"] = round(float(valor_stock), 2)
        except:
            item["STOCK"] = "N/D"

        # PVP
        try:
            valor_pvp = str(item.get("PVP", "")).strip().lower()
            if valor_pvp in ("", "#n/a", "#ref!", "n/a"):
                item["PVP"] = "N/D"
            else:
                item["PVP"] = round(float(valor_pvp), 2)
        except:
            item["PVP"] = "N/D"

    return datos
