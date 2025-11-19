#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de prueba
Uso: python seed_data.py
"""
import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puddle.settings')
django.setup()

from django.contrib.auth.models import User
from item.models import Category, Item
from conversation.models import Conversation, ConversationMessage
from django.core.files.base import ContentFile
import io

# Datos de prueba
CATEGORIES = [
    'Electronics',
    'Furniture',
    'Clothing',
    'Books',
    'Sports',
    'Toys',
    'Home & Garden',
    'Automotive',
    'Music',
    'Art'
]

ITEMS_DATA = [
    # Electronics
    {'name': 'iPhone 13 Pro', 'category': 'Electronics', 'price': '899.99', 'description': 'Excellent condition, barely used. Includes original box and charger.', 'image_url': 'https://images.unsplash.com/photo-1632661674596-df8be070a5c5?w=500'},
    {'name': 'Samsung 4K TV 55"', 'category': 'Electronics', 'price': '549.00', 'description': 'Smart TV with HDR support. Perfect for gaming and movies.', 'image_url': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500'},
    {'name': 'MacBook Air M1', 'category': 'Electronics', 'price': '799.99', 'description': '8GB RAM, 256GB SSD. Like new condition.', 'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500'},
    {'name': 'Sony Headphones WH-1000XM4', 'category': 'Electronics', 'price': '249.99', 'description': 'Noise cancelling, wireless. Great sound quality.', 'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500'},
    {'name': 'iPad Pro 11"', 'category': 'Electronics', 'price': '699.00', 'description': '128GB, WiFi. Includes Apple Pencil.', 'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500'},
    
    # Furniture
    {'name': 'Modern Sofa', 'category': 'Furniture', 'price': '450.00', 'description': 'Gray fabric, 3-seater. Very comfortable and clean.', 'image_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500'},
    {'name': 'Oak Dining Table', 'category': 'Furniture', 'price': '350.00', 'description': 'Solid oak, seats 6 people. Minor scratches.', 'image_url': 'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=500'},
    {'name': 'Office Chair', 'category': 'Furniture', 'price': '120.00', 'description': 'Ergonomic design, adjustable height. Black leather.', 'image_url': 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=500'},
    {'name': 'Bookshelf', 'category': 'Furniture', 'price': '80.00', 'description': 'White wooden bookshelf, 5 shelves. Easy to assemble.', 'image_url': 'https://images.unsplash.com/photo-1594620302200-9a762244a156?w=500'},
    {'name': 'Queen Bed Frame', 'category': 'Furniture', 'price': '200.00', 'description': 'Metal frame, sturdy construction. Mattress not included.', 'image_url': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=500'},
    
    # Clothing
    {'name': 'Leather Jacket', 'category': 'Clothing', 'price': '150.00', 'description': 'Genuine leather, size M. Worn only a few times.', 'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500'},
    {'name': 'Nike Running Shoes', 'category': 'Clothing', 'price': '75.00', 'description': 'Size 10, barely used. Great for jogging.', 'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500'},
    {'name': 'Winter Coat', 'category': 'Clothing', 'price': '90.00', 'description': 'Warm and waterproof. Size L, dark blue.', 'image_url': 'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=500'},
    {'name': 'Designer Jeans', 'category': 'Clothing', 'price': '60.00', 'description': 'Levi\'s 501, size 32x32. Excellent condition.', 'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500'},
    
    # Books
    {'name': 'Python Programming Book', 'category': 'Books', 'price': '35.00', 'description': 'Learn Python the Hard Way. Great for beginners.', 'image_url': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500'},
    {'name': 'Harry Potter Collection', 'category': 'Books', 'price': '80.00', 'description': 'Complete set, hardcover. Like new.', 'image_url': 'https://images.unsplash.com/photo-1621351183012-e2f9972dd9bf?w=500'},
    {'name': 'The Great Gatsby', 'category': 'Books', 'price': '12.00', 'description': 'Classic novel, paperback. Good condition.', 'image_url': 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=500'},
    
    # Sports
    {'name': 'Mountain Bike', 'category': 'Sports', 'price': '350.00', 'description': '21-speed, aluminum frame. Well maintained.', 'image_url': 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=500'},
    {'name': 'Tennis Racket', 'category': 'Sports', 'price': '45.00', 'description': 'Wilson Pro Staff. Includes case.', 'image_url': 'https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=500'},
    {'name': 'Yoga Mat', 'category': 'Sports', 'price': '25.00', 'description': 'Thick, non-slip. Purple color.', 'image_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500'},
    {'name': 'Dumbbells Set', 'category': 'Sports', 'price': '120.00', 'description': 'Adjustable weights, 5-50 lbs. Complete set.', 'image_url': 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=500'},
    
    # Toys
    {'name': 'LEGO Star Wars Set', 'category': 'Toys', 'price': '89.99', 'description': 'Millennium Falcon, complete with all pieces.', 'image_url': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=500'},
    {'name': 'PlayStation 5', 'category': 'Toys', 'price': '499.00', 'description': 'Brand new, sealed. Disc version.', 'image_url': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=500'},
    {'name': 'Board Game Collection', 'category': 'Toys', 'price': '60.00', 'description': 'Monopoly, Scrabble, and Chess. All complete.', 'image_url': 'https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=500'},
    
    # Home & Garden
    {'name': 'Lawn Mower', 'category': 'Home & Garden', 'price': '180.00', 'description': 'Electric, cordless. Battery included.', 'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500'},
    {'name': 'Garden Tools Set', 'category': 'Home & Garden', 'price': '45.00', 'description': 'Shovel, rake, hoe, and more. Good condition.', 'image_url': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=500'},
    {'name': 'BBQ Grill', 'category': 'Home & Garden', 'price': '250.00', 'description': 'Gas grill, 4 burners. Stainless steel.', 'image_url': 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=500'},
    
    # Automotive
    {'name': 'Car Tires Set', 'category': 'Automotive', 'price': '300.00', 'description': 'All-season, 205/55R16. Used one season.', 'image_url': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=500'},
    {'name': 'Car Stereo', 'category': 'Automotive', 'price': '120.00', 'description': 'Bluetooth, touchscreen. Easy installation.', 'image_url': 'https://images.unsplash.com/photo-1563784462041-5f97ac9523dd?w=500'},
    
    # Music
    {'name': 'Electric Guitar', 'category': 'Music', 'price': '280.00', 'description': 'Fender Stratocaster copy. Includes amp.', 'image_url': 'https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?w=500'},
    {'name': 'Keyboard Piano', 'category': 'Music', 'price': '150.00', 'description': '61 keys, weighted. Perfect for beginners.', 'image_url': 'https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=500'},
    
    # Art
    {'name': 'Oil Painting', 'category': 'Art', 'price': '200.00', 'description': 'Original artwork, landscape. 24x36 inches.', 'image_url': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=500'},
    {'name': 'Art Supplies Set', 'category': 'Art', 'price': '75.00', 'description': 'Professional quality paints, brushes, and canvas.', 'image_url': 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=500'},
]

USERS_DATA = [
    {'username': 'john_seller', 'email': 'john@example.com', 'password': 'password123'},
    {'username': 'mary_shop', 'email': 'mary@example.com', 'password': 'password123'},
    {'username': 'mike_deals', 'email': 'mike@example.com', 'password': 'password123'},
    {'username': 'sarah_market', 'email': 'sarah@example.com', 'password': 'password123'},
    {'username': 'david_store', 'email': 'david@example.com', 'password': 'password123'},
]

def download_image_from_url(url):
    """Descarga una imagen desde una URL"""
    try:
        import requests
        from PIL import Image
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Abrir imagen y convertir a RGB
        img = Image.open(io.BytesIO(response.content))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Redimensionar si es muy grande
        max_size = (800, 600)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Guardar en memoria
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        
        return ContentFile(img_io.read(), name='product.jpg')
    except Exception as e:
        print(f"⚠️  Error descargando imagen: {e}")
        return None

def clear_database():
    """Limpia los datos existentes"""
    print("\n🗑️  Limpiando base de datos...")
    ConversationMessage.objects.all().delete()
    Conversation.objects.all().delete()
    Item.objects.all().delete()
    Category.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("✅ Base de datos limpiada")

def create_categories():
    """Crea las categorías"""
    print("\n📁 Creando categorías...")
    categories = {}
    for cat_name in CATEGORIES:
        category, created = Category.objects.get_or_create(name=cat_name)
        categories[cat_name] = category
        if created:
            print(f"  ✓ {cat_name}")
    return categories

def create_users():
    """Crea usuarios de prueba"""
    print("\n👥 Creando usuarios...")
    users = []
    for user_data in USERS_DATA:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['username'].split('_')[0].capitalize(),
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"  ✓ {user.username}")
        users.append(user)
    return users

def create_items(categories, users):
    """Crea items de prueba"""
    print("\n📦 Creando items...")
    items = []
    
    for item_data in ITEMS_DATA:
        category = categories[item_data['category']]
        user = random.choice(users)
        
        item = Item.objects.create(
            name=item_data['name'],
            description=item_data['description'],
            price=Decimal(item_data['price']),
            category=category,
            created_by=user,
            is_sold=random.choice([False, False, False, True])  # 25% vendidos
        )
        
        # Descargar imagen desde URL
        if 'image_url' in item_data:
            print(f"    📥 Descargando imagen...")
            image = download_image_from_url(item_data['image_url'])
            if image:
                item.image.save(f'item_{item.id}.jpg', image, save=True)
        
        items.append(item)
        status = "🔴 VENDIDO" if item.is_sold else "🟢 DISPONIBLE"
        print(f"  ✓ {item.name} - ${item.price} - {status}")
    
    return items

def create_conversations(items, users):
    """Crea conversaciones de prueba"""
    print("\n💬 Creando conversaciones...")
    
    # Crear algunas conversaciones aleatorias
    num_conversations = min(10, len(items))
    sample_items = random.sample([i for i in items if not i.is_sold], num_conversations)
    
    for item in sample_items:
        # Elegir un comprador diferente al vendedor
        potential_buyers = [u for u in users if u != item.created_by]
        if not potential_buyers:
            continue
            
        buyer = random.choice(potential_buyers)
        
        # Crear conversación
        conversation = Conversation.objects.create(item=item)
        conversation.members.add(item.created_by, buyer)
        
        # Crear algunos mensajes
        messages = [
            f"Hi! I'm interested in your {item.name}. Is it still available?",
            f"Yes, it's still available! It's in great condition.",
            "Can you tell me more about it?",
            f"Sure! {item.description}",
            "Sounds good! Can we meet to see it?",
        ]
        
        for i, msg_content in enumerate(messages[:random.randint(2, 5)]):
            sender = buyer if i % 2 == 0 else item.created_by
            ConversationMessage.objects.create(
                conversation=conversation,
                content=msg_content,
                created_by=sender
            )
        
        print(f"  ✓ Conversación sobre: {item.name}")

def print_summary(categories, users, items):
    """Imprime resumen de datos creados"""
    print("\n" + "="*60)
    print("📊 RESUMEN DE DATOS CREADOS")
    print("="*60)
    print(f"👥 Usuarios: {len(users)}")
    print(f"📁 Categorías: {len(categories)}")
    print(f"📦 Items totales: {len(items)}")
    print(f"🟢 Items disponibles: {len([i for i in items if not i.is_sold])}")
    print(f"🔴 Items vendidos: {len([i for i in items if i.is_sold])}")
    print(f"💬 Conversaciones: {Conversation.objects.count()}")
    print(f"💭 Mensajes: {ConversationMessage.objects.count()}")
    print("="*60)
    
    print("\n🔑 CREDENCIALES DE ACCESO:")
    print("-" * 60)
    for user_data in USERS_DATA:
        print(f"Usuario: {user_data['username']}")
        print(f"Password: {user_data['password']}")
        print("-" * 60)

def main():
    """Función principal"""
    print("\n" + "="*60)
    print("🌱 INICIANDO SEED DE BASE DE DATOS")
    print("="*60)
    
    try:
        # Preguntar si desea limpiar la BD
        response = input("\n⚠️  ¿Desea limpiar la base de datos antes de continuar? (s/n): ")
        if response.lower() == 's':
            clear_database()
        
        # Crear datos
        categories = create_categories()
        users = create_users()
        items = create_items(categories, users)
        create_conversations(items, users)
        
        # Mostrar resumen
        print_summary(categories, users, items)
        
        print("\n✅ SEED COMPLETADO EXITOSAMENTE!")
        print("\n💡 Tip: Puedes ejecutar este script nuevamente para agregar más datos")
        print("   o usar la opción de limpiar para empezar desde cero.\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
