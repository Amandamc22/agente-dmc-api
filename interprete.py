import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def interpretar_consulta(consulta):
    prompt = f"""
Eres un asistente técnico de productos industriales. Tu tarea es analizar una consulta del usuario y responder en formato JSON con estas dos claves:

- "producto": nombre, marca o código del producto mencionado
- "dato": uno de estos valores obligatorios: "precio", "stock", "descripcion", "rendimiento" (en minúscula)

Ejemplo de respuesta:
{{ "producto": "Belzona 1111", "dato": "precio" }}

Consulta del usuario:
"{consulta}"
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.1
    )

    mensaje = response.choices[0].message.content.strip()

    try:
        return json.loads(mensaje)
    except Exception as e:
        print("❌ Error al interpretar JSON:", e)
        print("🧾 Respuesta completa del modelo:", mensaje)
        return None
