from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from decimal import Decimal
import os

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_sold', 'created_at']),
            models.Index(fields=['category', 'is_sold']),
            models.Index(fields=['created_by', 'created_at']),
            models.Index(fields=['is_sold', 'category', 'created_at']),
            models.Index(fields=['name']),
        ]
    
    def clean(self):
        """Validación personalizada del modelo"""
        super().clean()
        if self.price is not None and self.price <= 0:
            raise ValidationError({'price': 'El precio debe ser mayor a 0'})
        if self.price is not None and self.price > Decimal('99999999.99'):
            raise ValidationError({'price': 'El precio no puede exceder 99,999,999.99'})
    
    def save(self, *args, **kwargs):
        """Override save para ejecutar validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Override delete para eliminar la imagen antes de eliminar el item"""
        # Eliminar la imagen si existe
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.name


# Signals para manejo automático de imágenes

@receiver(pre_delete, sender=Item)
def delete_item_image_on_delete(sender, instance, **kwargs):
    """
    Elimina la imagen del sistema de archivos cuando se elimina un Item.
    Este signal se ejecuta antes de eliminar el objeto de la BD.
    """
    if instance.image:
        try:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
        except Exception as e:
            # Log del error pero no interrumpir la eliminación
            print(f"Error eliminando imagen: {e}")


@receiver(pre_save, sender=Item)
def delete_old_image_on_update(sender, instance, **kwargs):
    """
    Elimina la imagen antigua cuando se actualiza con una nueva imagen.
    Esto previene que se acumulen imágenes huérfanas.
    """
    if not instance.pk:
        # Es un nuevo item, no hay imagen antigua
        return
    
    try:
        old_item = Item.objects.get(pk=instance.pk)
    except Item.DoesNotExist:
        # El item no existe aún, no hay imagen antigua
        return
    
    # Si la imagen cambió, eliminar la antigua
    if old_item.image and old_item.image != instance.image:
        try:
            if os.path.isfile(old_item.image.path):
                os.remove(old_item.image.path)
        except Exception as e:
            # Log del error pero no interrumpir el guardado
            print(f"Error eliminando imagen antigua: {e}")