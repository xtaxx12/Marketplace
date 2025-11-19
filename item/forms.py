from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation

from .models import Item

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }
    
    def clean_price(self):
        """Validación personalizada del precio"""
        price = self.cleaned_data.get('price')
        
        if price is None:
            raise ValidationError('El precio es requerido')
        
        if price <= 0:
            raise ValidationError('El precio debe ser mayor a 0')
        
        if price > Decimal('99999999.99'):
            raise ValidationError('El precio no puede exceder 99,999,999.99')
        
        # Validar que tenga máximo 2 decimales
        if price.as_tuple().exponent < -2:
            raise ValidationError('El precio solo puede tener hasta 2 decimales')
        
        return price
    
    def clean_image(self):
        """Validación de la imagen"""
        image = self.cleaned_data.get('image')
        
        if image:
            # Validar tamaño (máximo 5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('La imagen no puede superar 5MB')
            
            # Validar tipo de archivo
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = image.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise ValidationError(f'Formato no válido. Use: {", ".join(valid_extensions)}')
        
        return image

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'is_sold')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }
    
    def clean_price(self):
        """Validación personalizada del precio"""
        price = self.cleaned_data.get('price')
        
        if price is None:
            raise ValidationError('El precio es requerido')
        
        if price <= 0:
            raise ValidationError('El precio debe ser mayor a 0')
        
        if price > Decimal('99999999.99'):
            raise ValidationError('El precio no puede exceder 99,999,999.99')
        
        # Validar que tenga máximo 2 decimales
        if price.as_tuple().exponent < -2:
            raise ValidationError('El precio solo puede tener hasta 2 decimales')
        
        return price
    
    def clean_image(self):
        """Validación de la imagen"""
        image = self.cleaned_data.get('image')
        
        if image:
            # Validar tamaño (máximo 5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('La imagen no puede superar 5MB')
            
            # Validar tipo de archivo
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = image.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise ValidationError(f'Formato no válido. Use: {", ".join(valid_extensions)}')
        
        return image