from read_gpt import leer_hoja_gpt
from consulta_agente import buscar_productos, responder_varias_coincidencias
from interprete import interpretar_consulta

def responder_consulta(producto, tipo_dato):
    claves = {
        "precio": "PRECIO",
        "stock": "STOCK",
        "descripcion": "DESCRIPCION",
        "rendimiento": "RENDIMIENTO"
    }

    clave = claves.get(tipo_dato)
    if not clave:
        return "❌ No se puede responder esa consulta."

    # DEPURACIÓN EN CONSOLA
    print(f"🔍 Clave solicitada: {clave}")
    print(f"🧾 Producto actual: {producto}")
    print(f"🔑 Claves disponibles: {list(producto.keys())}")

    for k, v in producto.items():
        if k.strip().lower() == clave.strip().lower():
            print(f"✅ ¡Match encontrado! clave: '{k}' → valor: {v}")
            return f"✅ {tipo_dato.capitalize()} del producto '{producto.get('NOMBRE', 'Producto sin nombre')}': {v}"

    print("❌ No se encontró la clave solicitada")
    return f"❌ No se encontró el dato '{tipo_dato}' para el producto '{producto.get('NOMBRE', 'Producto sin nombre')}'."

def main():
    datos = leer_hoja_gpt()
    print("🤖 Agente de Consulta en lenguaje natural listo.")

    while True:
        consulta = input("\n💬 Escribe tu consulta (o escribe 'salir'):\n> ")
        if consulta.lower() == "salir":
            break

        resultado = interpretar_consulta(consulta)

        if not resultado:
            print("❌ No entendí la consulta. Intenta de nuevo.")
            continue

        producto_clave = resultado.get("producto")
        tipo_dato = resultado.get("dato")

        if not producto_clave or not tipo_dato:
            print("❌ La consulta está incompleta.")
            continue

        coincidencias = buscar_productos(producto_clave, datos)

        if not coincidencias:
            print(f"❌ No encontré el producto '{producto_clave}'.")
            continue

        if len(coincidencias) == 1:
            print(responder_consulta(coincidencias[0], tipo_dato))
        else:
            print(responder_varias_coincidencias(coincidencias, tipo_dato))

if __name__ == "__main__":
    main()
