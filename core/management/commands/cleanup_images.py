"""
Comando de Django para limpiar imágenes huérfanas
Uso: python manage.py cleanup_images [--dry-run]
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from item.models import Item
import os


class Command(BaseCommand):
    help = 'Limpia imágenes huérfanas del sistema de archivos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué archivos se eliminarían sin eliminarlos',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 Modo DRY RUN - No se eliminarán archivos'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  MODO REAL - Los archivos se eliminarán'))
        
        self.stdout.write('\n🧹 Buscando imágenes huérfanas...\n')
        
        # Obtener directorio de imágenes
        media_root = settings.MEDIA_ROOT
        images_dir = os.path.join(media_root, 'item_images')
        
        if not os.path.exists(images_dir):
            self.stdout.write(self.style.SUCCESS('✅ No hay directorio de imágenes'))
            return
        
        # Obtener todas las imágenes en la BD
        db_images = set()
        for item in Item.objects.exclude(image='').exclude(image=None):
            if item.image:
                # Obtener solo el nombre del archivo
                image_name = os.path.basename(item.image.name)
                db_images.add(image_name)
        
        self.stdout.write(f'📊 Imágenes en BD: {len(db_images)}')
        
        # Obtener todas las imágenes en el sistema de archivos
        fs_images = set()
        for filename in os.listdir(images_dir):
            file_path = os.path.join(images_dir, filename)
            if os.path.isfile(file_path):
                fs_images.add(filename)
        
        self.stdout.write(f'📁 Archivos en disco: {len(fs_images)}')
        
        # Encontrar imágenes huérfanas
        orphan_images = fs_images - db_images
        
        if not orphan_images:
            self.stdout.write(self.style.SUCCESS('\n✅ No hay imágenes huérfanas'))
            return
        
        self.stdout.write(f'\n🗑️  Imágenes huérfanas encontradas: {len(orphan_images)}\n')
        
        total_size = 0
        deleted_count = 0
        
        for image_name in orphan_images:
            file_path = os.path.join(images_dir, image_name)
            file_size = os.path.getsize(file_path)
            total_size += file_size
            
            size_mb = file_size / (1024 * 1024)
            self.stdout.write(f'  📄 {image_name} ({size_mb:.2f} MB)')
            
            if not dry_run:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    self.stdout.write(self.style.SUCCESS(f'     ✓ Eliminado'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'     ✗ Error: {e}'))
        
        total_size_mb = total_size / (1024 * 1024)
        
        self.stdout.write('\n' + '='*60)
        if dry_run:
            self.stdout.write(self.style.WARNING(f'📊 Se eliminarían {len(orphan_images)} archivos'))
            self.stdout.write(self.style.WARNING(f'💾 Espacio a liberar: {total_size_mb:.2f} MB'))
            self.stdout.write('\n💡 Ejecuta sin --dry-run para eliminar los archivos')
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Eliminados {deleted_count} archivos'))
            self.stdout.write(self.style.SUCCESS(f'💾 Espacio liberado: {total_size_mb:.2f} MB'))
        self.stdout.write('='*60 + '\n')
