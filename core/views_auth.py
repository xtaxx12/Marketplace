from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy


class CustomPasswordResetView(PasswordResetConfirmView):
    template_name = 'core/password_reset_confirm.html'

    def get_success_url(self):
        print("Redirigiendo a password_reset_complete")  # Mensaje de depuración
        return reverse_lazy('core:password_reset_complete')