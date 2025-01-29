from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'core/password_reset_email.html'  # Plantilla para el correo electrónico
    template_name = 'core/password_reset.html'  # Plantilla para el formulario de restablecimiento
    success_url = reverse_lazy('core:password_reset_done')  # URL a la que redirigir después de enviar el correo