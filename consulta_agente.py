import unicodedata

def normalizar(texto):
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

def buscar_productos(consulta, data):
    consulta_norm = normalizar(consulta)
    resultados = []

    for item in data:
        nombre = normalizar(item.get("NOMBRE", ""))
        nombre_web = normalizar(item.get("NOMBRE WEB", ""))
        alias = normalizar(item.get("ALIAS", ""))
        codigo = normalizar(item.get("CODIGO", ""))

        if (consulta_norm in nombre or
            consulta_norm in nombre_web or
            consulta_norm in alias or
            consulta_norm in codigo):
            resultados.append(item)

    return resultados
