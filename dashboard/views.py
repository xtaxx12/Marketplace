from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from item.models import Item

@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user).select_related('category')

    # Paginación
    paginator = Paginator(items, 10)  # 10 items por página
    page = request.GET.get('page')
    
    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    return render(request, 'dashboard/index.html', {
        'items': items_page,
    })
