def buscar_productos(clave_producto, datos):
    coincidencias = []

    clave_lower = clave_producto.lower()

    for item in datos:
        campos = [
            item.get("NOMBRE", ""),
            item.get("NOMBRE WEB", ""),
            item.get("ALIAS", ""),
            item.get("CODIGO", "")
        ]
        campos_texto = " ".join([str(c).lower() for c in campos])

        if clave_lower in campos_texto:
            coincidencias.append(item)

    return coincidencias


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


def responder_varias_coincidencias(productos, tipo_dato):
    claves = {
        "precio": "PVP",
        "stock": "STOCK",
        "descripcion": "DESCRIPCION",
        "rendimiento": "RENDIMIENTO"
    }

    clave = claves.get(tipo_dato)
    if not clave:
        return "❌ Tipo de dato no reconocido."

    respuesta = f"Se encontraron varias presentaciones con su {tipo_dato}:\n"
    for item in productos:
        nombre = item.get("NOMBRE", "Sin nombre")
        valor = item.get(clave, "N/D")
        respuesta += f"• {nombre}: {valor}\n"

    return respuesta
