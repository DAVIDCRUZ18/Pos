# Funciones de validación reutilizables

def validar_email(email):
    """Valida formato de email"""
    import re
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def validar_documento(documento, tipo='CC'):
    """Valida documento de identidad"""
    return documento.isdigit() and len(documento) >= 6

def validar_telefono(telefono):
    """Valida número de teléfono"""
    return telefono.isdigit() and len(telefono) >= 7

def validar_precio(precio):
    """Valida que el precio sea válido"""
    try:
        return float(precio) > 0
    except:
        return False

def validar_stock(stock):
    """Valida cantidad de stock"""
    try:
        return int(stock) >= 0
    except:
        return False

def limpiar_texto(texto):
    """Limpia y formatea texto"""
    return texto.strip().title()