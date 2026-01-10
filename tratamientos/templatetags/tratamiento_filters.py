from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def currency(value):
    """
    Formatea un número como moneda con comas para miles y punto para decimales.
    Ejemplo: 1234.56 -> 1,234.56
    """
    if value is None:
        return "0.00"
    
    try:
        # Convertir a Decimal para manejar precisión
        if isinstance(value, str):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            value = Decimal(str(value))
        
        # Formatear con 2 decimales
        value = value.quantize(Decimal('0.01'))
        
        # Convertir a string y separar parte entera y decimal
        str_value = str(value)
        if '.' in str_value:
            integer_part, decimal_part = str_value.split('.')
        else:
            integer_part = str_value
            decimal_part = '00'
        
        # Agregar comas a la parte entera (de derecha a izquierda)
        if integer_part.startswith('-'):
            sign = '-'
            integer_part = integer_part[1:]
        else:
            sign = ''
        
        # Formatear con comas
        integer_formatted = '{:,}'.format(int(integer_part))
        
        return f"{sign}{integer_formatted}.{decimal_part}"
    
    except (ValueError, TypeError, AttributeError):
        return "0.00"
