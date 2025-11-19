"""
Utilidades para crear y gestionar notificaciones
"""
from .models import Notification

def create_notification(recipient, notification_type, title, message, link=None, sender=None):
    """
    Crea una nueva notificación
    
    Args:
        recipient: Usuario que recibirá la notificación
        notification_type: Tipo de notificación ('message', 'item_sold', 'new_conversation', 'system')
        title: Título de la notificación
        message: Mensaje de la notificación
        link: URL opcional a la que redirigir
        sender: Usuario que genera la notificación (opcional)
    """
    return Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link
    )

def create_message_notification(recipient, sender, conversation_id):
    """Crea una notificación de nuevo mensaje"""
    return create_notification(
        recipient=recipient,
        sender=sender,
        notification_type='message',
        title='Nuevo mensaje',
        message=f'{sender.username} te ha enviado un mensaje',
        link=f'/inbox/{conversation_id}/'
    )

def create_new_conversation_notification(recipient, sender, item_name, conversation_id):
    """Crea una notificación de nueva conversación"""
    return create_notification(
        recipient=recipient,
        sender=sender,
        notification_type='new_conversation',
        title='Nueva conversación',
        message=f'{sender.username} está interesado en tu artículo "{item_name}"',
        link=f'/inbox/{conversation_id}/'
    )

def mark_as_read(notification_id):
    """Marca una notificación como leída"""
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return True
    except Notification.DoesNotExist:
        return False

def mark_all_as_read(user):
    """Marca todas las notificaciones de un usuario como leídas"""
    return Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)

def get_unread_count(user):
    """Obtiene el número de notificaciones no leídas"""
    return Notification.objects.filter(recipient=user, is_read=False).count()

def delete_notification(notification_id):
    """Elimina una notificación"""
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
        return True
    except Notification.DoesNotExist:
        return False
