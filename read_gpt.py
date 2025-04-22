import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
import tempfile

def leer_hoja_gpt():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Leer desde variable de entorno
    cred_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")

    if not cred_json:
        raise Exception("❌ No se encontró la variable 'GOOGLE_SHEETS_CREDENTIALS'.")

    try:
        print("🔐 Fragmento de cred_json (200 caracteres):")
        print(cred_json[:200])

        # Guardar en archivo temporal
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as temp_file:
            temp_file.write(cred_json)
            temp_file.flush()
            temp_path = temp_file.name

        print(f"📁 Archivo temporal creado: {temp_path}")

        # Autenticación usando el archivo temporal
        creds = ServiceAccountCredentials.from_json_keyfile_name(temp_path, scope)
        print("✅ Credenciales cargadas desde archivo temporal.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise Exception(f"❌ Error al procesar la credencial desde archivo temporal: {e}")

    try:
        client = gspread.authorize(creds)
        sheet = client.open("0. BASE GENERAL- Cotizador 2024/04/01 (Actualizar PVP)")
        worksheet = sheet.worksheet("GPT")
        datos = worksheet.get_all_records()
        print(f"📄 Datos obtenidos desde la hoja: {len(datos)} registros")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise Exception(f"❌ Error al acceder a Google Sheets: {e}")

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
