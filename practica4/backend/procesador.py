import xml.etree.ElementTree as ET

POSITIVAS = {"bueno", "excelente", "satisfecho", "cool"}
NEGATIVAS = {"malo", "pésimo", "triste", "molesto", "decepcionado"}

def procesar_mensaje_texto(mensaje):
    """Procesa un mensaje de texto y genera un XML."""
    texto = mensaje.lower()
    positivo = sum(1 for palabra in POSITIVAS if palabra in texto)
    negativo = sum(1 for palabra in NEGATIVAS if palabra in texto)

    sentimiento = "neutro"
    if positivo > negativo:
        sentimiento = "positivo"
    elif negativo > positivo:
        sentimiento = "negativo"

    # Genera el XML de salida
    root = ET.Element("respuesta")
    ET.SubElement(root, "mensaje").text = mensaje
    ET.SubElement(root, "sentimiento").text = sentimiento

    return ET.tostring(root, encoding='unicode')
def resetear_datos():
    """Resetea los datos almacenados borrando el contenido del archivo XML."""
    try:
        with open("mensajes.xml", "w") as archivo:
            archivo.write("<lista_respuestas></lista_respuestas>")
        print("Datos reseteados correctamente.")
    except Exception as e:
        print(f"Error al resetear datos: {e}")

# Funciones adicionales
def procesar_mensaje_texto(mensaje):
    texto = mensaje.lower()
    # Simulación de procesamiento de texto
    return f"<mensaje>{mensaje}</mensaje>"
def obtener_resumen(empresa=None, fecha=None, fecha_inicio=None, fecha_fin=None):
    """Genera un resumen ficticio basado en filtros."""
    return {
        "empresa": empresa or "Todas",
        "fecha": fecha or "N/A",
        "total_mensajes": 20,
        "positivos": 8,
        "negativos": 7,
        "neutros": 5
    }

def procesar_mensaje_texto(mensaje):
    """Procesa un mensaje y genera un XML."""
    root = ET.Element("mensaje")
    root.text = mensaje
    return ET.tostring(root, encoding='unicode')

def resetear_datos():
    """Resetea los datos guardados borrando el archivo XML."""
    with open("mensajes.xml", "w") as archivo:
        archivo.write("<lista_respuestas></lista_respuestas>")

def prueba_de_mensaje(mensaje_xml):
    """Procesa un mensaje XML y devuelve una respuesta."""
    root = ET.fromstring(mensaje_xml)
    fecha = root.find(".//fecha").text if root.find(".//fecha") else "N/A"
    red_social = root.find(".//red_social").text if root.find(".//red_social") else "Desconocido"
    usuario = root.find(".//usuario").text if root.find(".//usuario") else "Anónimo"

    return f"""
    <respuesta>
        <fecha>{fecha}</fecha>
        <red_social>{red_social}</red_social>
        <usuario>{usuario}</usuario>
    </respuesta>
    """