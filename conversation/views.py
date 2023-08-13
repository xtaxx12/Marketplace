from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from item.models import Category, Item
from django.http import Http404
from .forms import ConversationMessageForm
from .models import Conversation
from .models import Conversation, ConversationMessage

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/new.html', {
        'form': form
    })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })
    

def eliminar_conversacion(request, conversation_id):
    # Obtener la conversación
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    # Verificar si el usuario actual es miembro de la conversación
    if request.user in conversation.members.all():
        # Eliminar todos los mensajes de la conversación
        conversation.messages.all().delete()

        # Eliminar la conversación
        conversation.delete()

    # Redirigir a la lista de conversaciones
    return redirect('conversation/new.html')


def eliminar_conversation(request,conversation_id):
    # Obtener la conversación del usuario actual
    conversation = get_object_or_404(Conversation, id=conversation_id, members=request.user)
    # Obtener todos los mensajes asociados con la conversación
    mensajes = conversation.messages.all()

    # Verificar si hay mensajes en la conversación
    if mensajes.exists():
        # Supongamos que quieres eliminar el primer mensaje, puedes hacer lo siguiente:
        mensaje_a_eliminar = mensajes.first()
        mensaje_a_eliminar.delete()
     
    # Aquí, se supone que tienes un formulario (variable form) para agregar nuevos mensajes a la conversación.
    form = ConversationMessageForm(request.POST)
    if form.is_valid():
        conversation_message = form.save(commit=False)
        conversation_message.conversation = conversation
        conversation_message.created_by = request.user
        conversation_message.save()

        conversation.save()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })
    