from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    """
    Formatea un precio Decimal con separadores de miles y 2 decimales
    Ejemplo: 1234.56 -> $1,234.56
    """
    if value is None:
        return '$0.00'
    
    try:
        # Convertir a Decimal si no lo es
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        
        # Formatear con separadores de miles y 2 decimales
        return '${:,.2f}'.format(value)
    except (ValueError, TypeError):
        return '$0.00'

@register.filter(name='format_price_simple')
def format_price_simple(value):
    """
    Formatea un precio sin el símbolo de dólar
    Ejemplo: 1234.56 -> 1,234.56
    """
    if value is None:
        return '0.00'
    
    try:
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        
        return '{:,.2f}'.format(value)
    except (ValueError, TypeError):
        return '0.00'
