from read_gpt import leer_hoja_gpt
from consulta_agente import buscar_productos
from interprete import interpretar_consulta

def responder_consulta(producto, tipo_dato):
    claves = {
        "precio": "PVP",
        "stock": "STOCK",
        "descripcion": "DESCRIPCION",
        "rendimiento": "RENDIMIENTO"
    }

    clave = claves.get(tipo_dato)
    if not clave or clave not in producto:
        return "❌ No se puede responder esa consulta."

    return f"✅ {tipo_dato.capitalize()} del producto '{producto['NOMBRE']}': {producto[clave]}"

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
            print(f"✅ Se encontraron varias presentaciones de '{producto_clave}' con su {tipo_dato}:\n")
            for item in coincidencias:
                clave_valor = item.get(tipo_dato.upper(), "N/D")
                print(f"- {item['NOMBRE']}: {clave_valor}")

if __name__ == "__main__":
    main()
