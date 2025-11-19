from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from item.models import Category, Item
from .forms import ConversationMessageForm
from .models import Conversation, ConversationMessage
from core.notifications import create_message_notification, create_new_conversation_notification

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations.exists():
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
            
            # Crear notificación para el vendedor
            create_new_conversation_notification(
                recipient=item.created_by,
                sender=request.user,
                item_name=item.name,
                conversation_id=conversation.id
            )

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {'form': form})

@login_required
def inbox(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    conversations = Conversation.objects.filter(members__in=[request.user.id]).select_related('item')

    # Paginación
    paginator = Paginator(conversations, 15)  # 15 conversaciones por página
    page = request.GET.get('page')
    
    try:
        conversations_page = paginator.page(page)
    except PageNotAnInteger:
        conversations_page = paginator.page(1)
    except EmptyPage:
        conversations_page = paginator.page(paginator.num_pages)

    return render(request, 'conversation/inbox.html', {'conversations': conversations_page})

@login_required
def detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, members=request.user)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()
            
            # Crear notificación para el otro usuario
            for member in conversation.members.all():
                if member != request.user:
                    create_message_notification(
                        recipient=member,
                        sender=request.user,
                        conversation_id=conversation.id
                    )

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {'conversation': conversation, 'form': form})

@login_required
def eliminar_mensaje(request, message_id):
    message = get_object_or_404(ConversationMessage, pk=message_id, created_by=request.user)

    if request.method == 'POST':
        message.delete()
        return redirect('conversation:detail', pk=message.conversation.id)

    return redirect('conversation:detail', pk=message.conversation.id)
