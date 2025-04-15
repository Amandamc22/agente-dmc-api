def buscar_productos(clave_busqueda, datos):
    clave_busqueda = clave_busqueda.lower().strip()
    coincidencias = []

    for item in datos:
        nombres = [
            item.get("NOMBRE", "").lower(),
            item.get("NOMBRE WEB", "").lower(),
            item.get("ALIAS", "").lower(),
        ]

        if any(clave_busqueda in nombre for nombre in nombres):
            coincidencias.append(item)

    return coincidencias


def responder_varias_coincidencias(coincidencias, tipo_dato):
    claves = {
        "precio": "PRECIO",
        "stock": "STOCK",
        "descripcion": "DESCRIPCION",
        "rendimiento": "RENDIMIENTO"
    }

    clave = claves.get(tipo_dato)
    if not clave:
        return f"❌ No puedo responder sobre '{tipo_dato}'."

    respuesta = [f"✅ Se encontraron varias presentaciones con su {tipo_dato}:\n"]

    for producto in coincidencias:
        print(f"🧾 Producto: {producto}")
        for k, v in producto.items():
            print(f" - clave: '{k}' → valor: {v}")

        valor = next(
            (v for k, v in producto.items() if k.strip().lower() == clave.strip().lower()),
            "N/D"
        )
        respuesta.append(f"- {producto.get('NOMBRE', 'Sin nombre')}: {valor}")

    return "\n".join(respuesta)
