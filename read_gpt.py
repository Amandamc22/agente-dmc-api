import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

def leer_hoja_gpt():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Leer el contenido de la variable de entorno
    cred_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
    if not cred_json:
        raise Exception("❌ No se encontró la variable 'GOOGLE_SHEETS_CREDENTIALS'.")

    try:
        # Convertir string JSON a diccionario
        cred_data = json.loads(cred_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_data, scope)
    except Exception as e:
        raise Exception(f"❌ Error al procesar la credencial JSON: {e}")

    client = gspread.authorize(creds)

    # Abre el documento y la pestaña
    sheet = client.open("0. BASE GENERAL- Cotizador 2024/04/01 (Actualizar PVP)")
    worksheet = sheet.worksheet("GPT")

    # Devuelve todos los registros como lista de diccionarios
    return worksheet.get_all_records()
