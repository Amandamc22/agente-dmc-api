import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("agente-atco.json", scope)
client = gspread.authorize(creds)

# 2. Acceder a la hoja usando el ID de la URL
spreadsheet = client.open_by_key("1A0JDwDvZuGUvuzbtyj_Y4LLPuUOoJzVZ5peYU3UT_64")

# 3. Seleccionar la pestaña GPT
sheet = spreadsheet.worksheet("GPT")

# 4. Leer todos los datos como lista de diccionarios
datos = sheet.get_all_records()

# 5. Imprimir los valores de la columna PVP
print("Valores de la columna PVP desde la pestaña 'GPT':\n")
for i, item in enumerate(datos):
    print(f"{i+1}. PVP: {item.get('PVP', 'No encontrado')}")
