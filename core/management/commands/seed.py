"""
Comando de Django para poblar la base de datos con datos de prueba
Uso: python manage.py seed [--clear]
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from item.models import Category, Item
from conversation.models import Conversation, ConversationMessage
from decimal import Decimal
import random
from django.core.files.base import ContentFile
import io


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpia la base de datos antes de poblar',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('🗑️  Limpiando base de datos...'))
            self.clear_database()
            self.stdout.write(self.style.SUCCESS('✅ Base de datos limpiada'))

        self.stdout.write(self.style.HTTP_INFO('\n🌱 Iniciando seed...'))
        
        categories = self.create_categories()
        users = self.create_users()
        items = self.create_items(categories, users)
        self.create_conversations(items, users)
        
        self.print_summary(categories, users, items)
        self.stdout.write(self.style.SUCCESS('\n✅ Seed completado exitosamente!\n'))

    def clear_database(self):
        """Limpia los datos existentes"""
        ConversationMessage.objects.all().delete()
        Conversation.objects.all().delete()
        Item.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    def download_image_from_url(self, url):
        """Descarga una imagen desde una URL"""
        try:
            import requests
            from PIL import Image
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            img = Image.open(io.BytesIO(response.content))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            max_size = (800, 600)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=85)
            img_io.seek(0)
            
            return ContentFile(img_io.read(), name='product.jpg')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'    ⚠️  Error descargando imagen: {e}'))
            return None

    def create_categories(self):
        """Crea categorías"""
        self.stdout.write('\n📁 Creando categorías...')
        categories_list = [
            'Electronics', 'Furniture', 'Clothing', 'Books', 'Sports',
            'Toys', 'Home & Garden', 'Automotive', 'Music', 'Art'
        ]
        
        categories = {}
        for cat_name in categories_list:
            category, created = Category.objects.get_or_create(name=cat_name)
            categories[cat_name] = category
            if created:
                self.stdout.write(f'  ✓ {cat_name}')
        
        return categories

    def create_users(self):
        """Crea usuarios de prueba"""
        self.stdout.write('\n👥 Creando usuarios...')
        users_data = [
            {'username': 'john_seller', 'email': 'john@example.com'},
            {'username': 'mary_shop', 'email': 'mary@example.com'},
            {'username': 'mike_deals', 'email': 'mike@example.com'},
            {'username': 'sarah_market', 'email': 'sarah@example.com'},
            {'username': 'david_store', 'email': 'david@example.com'},
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['username'].split('_')[0].capitalize(),
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'  ✓ {user.username}')
            users.append(user)
        
        return users

    def create_items(self, categories, users):
        """Crea items de prueba"""
        self.stdout.write('\n📦 Creando items...')
        
        items_data = [
            {'name': 'iPhone 13 Pro', 'category': 'Electronics', 'price': '899.99', 'description': 'Excellent condition, barely used.', 'image_url': 'https://images.unsplash.com/photo-1632661674596-df8be070a5c5?w=500'},
            {'name': 'Samsung 4K TV 55"', 'category': 'Electronics', 'price': '549.00', 'description': 'Smart TV with HDR support.', 'image_url': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500'},
            {'name': 'MacBook Air M1', 'category': 'Electronics', 'price': '799.99', 'description': '8GB RAM, 256GB SSD.', 'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500'},
            {'name': 'Sony Headphones', 'category': 'Electronics', 'price': '249.99', 'description': 'Noise cancelling, wireless.', 'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500'},
            {'name': 'Modern Sofa', 'category': 'Furniture', 'price': '450.00', 'description': 'Gray fabric, 3-seater.', 'image_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500'},
            {'name': 'Oak Dining Table', 'category': 'Furniture', 'price': '350.00', 'description': 'Solid oak, seats 6.', 'image_url': 'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=500'},
            {'name': 'Office Chair', 'category': 'Furniture', 'price': '120.00', 'description': 'Ergonomic design.', 'image_url': 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=500'},
            {'name': 'Leather Jacket', 'category': 'Clothing', 'price': '150.00', 'description': 'Genuine leather, size M.', 'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500'},
            {'name': 'Nike Running Shoes', 'category': 'Clothing', 'price': '75.00', 'description': 'Size 10, barely used.', 'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500'},
            {'name': 'Python Book', 'category': 'Books', 'price': '35.00', 'description': 'Learn Python programming.', 'image_url': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500'},
            {'name': 'Mountain Bike', 'category': 'Sports', 'price': '350.00', 'description': '21-speed, aluminum frame.', 'image_url': 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=500'},
            {'name': 'Tennis Racket', 'category': 'Sports', 'price': '45.00', 'description': 'Wilson Pro Staff.', 'image_url': 'https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=500'},
            {'name': 'PlayStation 5', 'category': 'Toys', 'price': '499.00', 'description': 'Brand new, sealed.', 'image_url': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=500'},
            {'name': 'LEGO Set', 'category': 'Toys', 'price': '89.99', 'description': 'Star Wars collection.', 'image_url': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=500'},
            {'name': 'BBQ Grill', 'category': 'Home & Garden', 'price': '250.00', 'description': 'Gas grill, 4 burners.', 'image_url': 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=500'},
            {'name': 'Car Stereo', 'category': 'Automotive', 'price': '120.00', 'description': 'Bluetooth, touchscreen.', 'image_url': 'https://images.unsplash.com/photo-1563784462041-5f97ac9523dd?w=500'},
            {'name': 'Electric Guitar', 'category': 'Music', 'price': '280.00', 'description': 'Includes amp.', 'image_url': 'https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?w=500'},
            {'name': 'Oil Painting', 'category': 'Art', 'price': '200.00', 'description': 'Original artwork.', 'image_url': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=500'},
        ]
        
        items = []
        for item_data in items_data:
            category = categories[item_data['category']]
            user = random.choice(users)
            
            item = Item.objects.create(
                name=item_data['name'],
                description=item_data['description'],
                price=Decimal(item_data['price']),
                category=category,
                created_by=user,
                is_sold=random.choice([False, False, False, True])
            )
            
            if 'image_url' in item_data:
                image = self.download_image_from_url(item_data['image_url'])
                if image:
                    item.image.save(f'item_{item.id}.jpg', image, save=True)
            
            items.append(item)
            status = "🔴 VENDIDO" if item.is_sold else "🟢 DISPONIBLE"
            self.stdout.write(f'  ✓ {item.name} - ${item.price} - {status}')
        
        return items

    def create_conversations(self, items, users):
        """Crea conversaciones de prueba"""
        self.stdout.write('\n💬 Creando conversaciones...')
        
        available_items = [i for i in items if not i.is_sold]
        num_conversations = min(5, len(available_items))
        sample_items = random.sample(available_items, num_conversations)
        
        for item in sample_items:
            potential_buyers = [u for u in users if u != item.created_by]
            if not potential_buyers:
                continue
            
            buyer = random.choice(potential_buyers)
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(item.created_by, buyer)
            
            messages = [
                f"Hi! I'm interested in your {item.name}.",
                "Yes, it's still available!",
                "Can you tell me more about it?",
            ]
            
            for i, msg_content in enumerate(messages):
                sender = buyer if i % 2 == 0 else item.created_by
                ConversationMessage.objects.create(
                    conversation=conversation,
                    content=msg_content,
                    created_by=sender
                )
            
            self.stdout.write(f'  ✓ Conversación sobre: {item.name}')

    def print_summary(self, categories, users, items):
        """Imprime resumen"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📊 RESUMEN'))
        self.stdout.write('='*60)
        self.stdout.write(f'👥 Usuarios: {len(users)}')
        self.stdout.write(f'📁 Categorías: {len(categories)}')
        self.stdout.write(f'📦 Items: {len(items)}')
        self.stdout.write(f'🟢 Disponibles: {len([i for i in items if not i.is_sold])}')
        self.stdout.write(f'💬 Conversaciones: {Conversation.objects.count()}')
        self.stdout.write('='*60)
        self.stdout.write('\n🔑 Credenciales: username/password123')
