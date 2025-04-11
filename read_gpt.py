import gspread
from oauth2client.service_account import ServiceAccountCredentials

def leer_hoja_gpt():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # ✅ Leer directamente desde el archivo agente-atco.json
    creds = ServiceAccountCredentials.from_json_keyfile_name("agente-atco.json", scope)
    client = gspread.authorize(creds)

    # Abre el documento y la pestaña
    sheet = client.open("0. BASE GENERAL- Cotizador 2024/04/01 (Actualizar PVP)")
    worksheet = sheet.worksheet("GPT")

    # Devuelve todos los registros como lista de diccionarios
    return worksheet.get_all_records()
