from django.shortcuts import render, redirect, get_object_or_404
from django.db import models

from item.models import Category, Item

from .forms import SignupForm

from django.contrib.auth import logout

from django.core.mail import send_mail

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })
def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })
    
    
def logout_view(request):
    """
    Cierra la sesión del usuario y lo redirige a la página de inicio.
    """
    logout(request)
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })
    
    
def enviar_correo(request):
    enviado_correctamente = False  # Variable que va a determinar si se envió el correo correctamente , nos servira para el if del template
    if request.method == "POST":
        email = request.POST.get(
            "email", ""
        )  # Obtenemos el correo electrónico ingresado por el usuario en home.html
        # Ahora enviamos el correo electrónico
        subject = "Gracias por ponerte en contacto con nosotros"
        message = f"Hola,\n\nGracias por ponerte en contacto con nosotros. Pronto te responderemos.\n\nAtentamente,\nJoel Rojas"
        from_email = email  # le mandamos la variable email para que envie el mensaje al correo ingresado por el usuario como remitente
        recipient_list = [email]
        try:
            send_mail(subject, message, from_email, recipient_list)
            enviado_correctamente = True  # Actualizamos el valor de la variable a True si se envió correctamente
        except Exception as e:
            pass  # No es necesario hacer nada aquí, la variable seguirá siendo False

    # Enviamos el valor de "enviado_correctamente" como parte del contexto para usarlo en el if
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })
    


# ============================================
# VISTAS DE NOTIFICACIONES
# ============================================

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification
from .notifications import mark_as_read, mark_all_as_read, delete_notification, get_unread_count

@login_required
def notifications_list(request):
    """Vista para listar todas las notificaciones del usuario"""
    notifications = Notification.objects.filter(recipient=request.user)[:50]
    unread_count = get_unread_count(request.user)
    
    return render(request, 'core/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def mark_notification_read(request, notification_id):
    """Marca una notificación como leída"""
    if request.method == 'POST':
        success = mark_as_read(notification_id)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': success})
        
        # Si la notificación tiene un link, redirigir allí
        try:
            notification = Notification.objects.get(id=notification_id)
            if notification.link:
                return redirect(notification.link)
        except Notification.DoesNotExist:
            pass
    
    return redirect('core:notifications')

@login_required
def mark_all_notifications_read(request):
    """Marca todas las notificaciones como leídas"""
    if request.method == 'POST':
        count = mark_all_as_read(request.user)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'count': count})
    
    return redirect('core:notifications')

@login_required
def delete_notification_view(request, notification_id):
    """Elimina una notificación"""
    if request.method == 'POST':
        success = delete_notification(notification_id)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': success})
    
    return redirect('core:notifications')

@login_required
def get_notifications_count(request):
    """API endpoint para obtener el contador de notificaciones no leídas"""
    count = get_unread_count(request.user)
    return JsonResponse({'count': count})


# ============================================
# VISTAS DE FAVORITOS
# ============================================

from .models import Favorite

@login_required
def favorites_list(request):
    """Vista para listar todos los favoritos del usuario"""
    favorites = Favorite.objects.filter(user=request.user).select_related('item')
    
    return render(request, 'core/favorites.html', {
        'favorites': favorites
    })

@login_required
def toggle_favorite(request, item_id):
    """Agregar o quitar un item de favoritos"""
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)
        
        if not created:
            # Si ya existía, lo eliminamos
            favorite.delete()
            is_favorite = False
            message = 'Eliminado de favoritos'
        else:
            is_favorite = True
            message = 'Agregado a favoritos'
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            favorites_count = Favorite.objects.filter(user=request.user).count()
            return JsonResponse({
                'success': True,
                'is_favorite': is_favorite,
                'message': message,
                'favorites_count': favorites_count
            })
        
        # Si no es AJAX, redirigir a la página anterior
        return redirect(request.META.get('HTTP_REFERER', 'core:index'))
    
    return redirect('core:index')

@login_required
def get_favorites_count(request):
    """API endpoint para obtener el contador de favoritos"""
    count = Favorite.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})

@login_required
def check_favorite(request, item_id):
    """API endpoint para verificar si un item está en favoritos"""
    is_favorite = Favorite.objects.filter(user=request.user, item_id=item_id).exists()
    return JsonResponse({'is_favorite': is_favorite})


# ============================================
# VISTAS DE CALIFICACIONES
# ============================================

from .models import Rating
from .forms_rating import RatingForm

@login_required
def add_rating(request, item_id):
    """Vista para agregar o editar una calificación"""
    item = get_object_or_404(Item, id=item_id)
    
    # Verificar si el usuario ya calificó este item
    existing_rating = Rating.objects.filter(user=request.user, item=item).first()
    
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=existing_rating)
        
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.item = item
            rating.save()
            
            # Si es una petición AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                avg_rating = item.ratings.aggregate(models.Avg('rating'))['rating__avg']
                count = item.ratings.count()
                return JsonResponse({
                    'success': True,
                    'message': 'Calificación guardada exitosamente',
                    'avg_rating': round(avg_rating, 1) if avg_rating else 0,
                    'count': count
                })
            
            return redirect('item:detail', pk=item_id)
    else:
        form = RatingForm(instance=existing_rating)
    
    return render(request, 'core/add_rating.html', {
        'form': form,
        'item': item,
        'existing_rating': existing_rating
    })

@login_required
def delete_rating(request, rating_id):
    """Vista para eliminar una calificación"""
    rating = get_object_or_404(Rating, id=rating_id, user=request.user)
    item_id = rating.item.id
    
    if request.method == 'POST':
        rating.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Calificación eliminada'})
        
        return redirect('item:detail', pk=item_id)
    
    return redirect('item:detail', pk=item_id)

def get_item_ratings(request, item_id):
    """API endpoint para obtener las calificaciones de un item"""
    item = get_object_or_404(Item, id=item_id)
    ratings = Rating.objects.filter(item=item).select_related('user')
    
    avg_rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
    
    ratings_data = [{
        'id': r.id,
        'user': r.user.username,
        'rating': r.rating,
        'review': r.review,
        'created_at': r.created_at.strftime('%d/%m/%Y'),
        'is_owner': r.user == request.user if request.user.is_authenticated else False
    } for r in ratings]
    
    return JsonResponse({
        'avg_rating': round(avg_rating, 1) if avg_rating else 0,
        'count': ratings.count(),
        'ratings': ratings_data
    })
