from django.shortcuts import render, redirect

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
    
    