from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView,PasswordResetConfirmView
from django.urls import reverse_lazy


#mi error fue no haber creado una clase personalizada para los tres url
class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'core/password_reset_email.html'
    success_url = reverse_lazy('core:password_reset_done')
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'core/password_reset_confirm.html'
    success_url = reverse_lazy('core:password_reset_complete')  

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'core/password_reset_complete.html'  # ✅ Solo necesita el template