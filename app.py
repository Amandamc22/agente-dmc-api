from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Pregunta(BaseModel):
    consulta: str

@app.post("/consultar")
async def consultar(pregunta: Pregunta):
    try:
        print("🟡 INICIO de endpoint /consultar")
        print("🔹 Consulta recibida:", pregunta.consulta)

        from read_gpt import leer_hoja_gpt
        from interprete import interpretar_consulta
        from consulta_agente import buscar_productos

        datos = leer_hoja_gpt()
        print(f"📥 Datos cargados: {len(datos)} registros")
        print("📋 Primeros 2 items:", datos[:2])

        resultado = interpretar_consulta(pregunta.consulta)
        print("🧠 Interpretación:", resultado)

        if not resultado:
            print("⚠️ No se pudo interpretar la consulta.")
            return {"respuesta": "❌ No entendí la consulta. Intenta de nuevo."}

        producto_clave = resultado.get("producto")
        tipo_dato = resultado.get("dato")
        print("🔎 Buscando producto:", producto_clave, "| Dato:", tipo_dato)

        claves = {
            "precio": "PRECIO",
            "stock": "STOCK",
            "descripcion": "DESCRIPCION",
            "rendimiento": "RENDIMIENTO"
        }

        clave = claves.get(tipo_dato.lower())
        if not clave:
            return {"respuesta": f"❌ El tipo de dato '{tipo_dato}' no es válido."}

        coincidencias = buscar_productos(producto_clave, datos)
        print(f"🔍 Coincidencias encontradas: {len(coincidencias)}")

        if not coincidencias:
            print("⚠️ No se encontró ninguna coincidencia.")
            return {"respuesta": f"❌ No encontré el producto '{producto_clave}'."}

        if len(coincidencias) == 1:
            producto = coincidencias[0]
            valor = producto.get(clave, "N/D")
            print("✅ Coincidencia única:", producto["NOMBRE"], "| Valor:", valor)
            return {"respuesta": f"{tipo_dato.capitalize()} del producto '{producto['NOMBRE']}': {valor}"}
        else:
            respuestas = []
            for p in coincidencias:
                valor = p.get(clave, "N/D")
                print(f"📦 {p['NOMBRE']} → {clave}: {valor}")
                respuestas.append(f"- {p['NOMBRE']}: {valor}")
            print("✅ Respuesta múltiple lista.")
            return {
                "respuesta": f"Se encontraron varias presentaciones de '{producto_clave}' con su {tipo_dato}:\n"
                             + "\n".join(respuestas)
            }

    except Exception as e:
        print("❌ ERROR GLOBAL en el endpoint consultar():", str(e))
        return {"respuesta": f"❌ Error interno global: {str(e)}"}
