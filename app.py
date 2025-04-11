from fastapi import FastAPI, Request
from pydantic import BaseModel
from consulta_agente import buscar_productos
from interprete import interpretar_consulta
from read_gpt import leer_hoja_gpt

app = FastAPI()

class Pregunta(BaseModel):
    consulta: str

@app.post("/consultar")
async def consultar(pregunta: Pregunta):
    datos = leer_hoja_gpt()
    resultado = interpretar_consulta(pregunta.consulta)

    if not resultado:
        return {"respuesta": "❌ No entendí la consulta. Intenta de nuevo."}

    producto_clave = resultado.get("producto")
    tipo_dato = resultado.get("dato")

    coincidencias = buscar_productos(producto_clave, datos)
    if not coincidencias:
        return {"respuesta": f"❌ No encontré el producto '{producto_clave}'."}

    if len(coincidencias) == 1:
        producto = coincidencias[0]
        valor = producto.get(tipo_dato.upper(), "N/D")
        return {"respuesta": f"{tipo_dato.capitalize()} del producto '{producto['NOMBRE']}': {valor}"}
    else:
        respuestas = []
        for p in coincidencias:
            valor = p.get(tipo_dato.upper(), "N/D")
            respuestas.append(f"- {p['NOMBRE']}: {valor}")
        return {"respuesta": f"Se encontraron varias presentaciones de '{producto_clave}' con su {tipo_dato}:\n" + "\n".join(respuestas)}
