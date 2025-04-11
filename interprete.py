import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def interpretar_consulta(consulta):
    prompt = f"""
Eres un asistente técnico de productos industriales. Tu tarea es analizar una consulta del usuario y responder en formato JSON indicando:
- El producto o código mencionado
- El tipo de dato que desea: puede ser "precio", "stock", "descripcion" o "rendimiento".

Consulta: "{consulta}"

Ejemplo de respuesta:
{{ "producto": "B1111-2", "dato": "stock" }}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.1
    )

    mensaje = response.choices[0].message.content

    try:
        return eval(mensaje)
    except:
        return None
