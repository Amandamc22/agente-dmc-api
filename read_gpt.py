import gspread
from oauth2client.service_account import ServiceAccountCredentials

def leer_hoja_gpt():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("agente-atco.json", scope)
    client = gspread.authorize(creds)

    # Abre el documento y la pestaña
    sheet = client.open("0. BASE GENERAL- Cotizador 2024/04/01 (Actualizar PVP)")
    worksheet = sheet.worksheet("GPT")

    # Obtiene todos los registros como una lista de diccionarios
    data = worksheet.get_all_records()
    return data
