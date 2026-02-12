import logging

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger(__name__)

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

class LoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        username = self.request.POST.get('username', "Desconocido")
        ip = self.request.META.get('REMOTE_ADDR', 'sin_ip')
        logger.error(f'Intento de inicio de sesión fallido para ${username}')
        messages.error(self.request, 'El usuario y la contraseña no coinciden')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')

class Error404View(TemplateView):
    template_name = '404.html'

    def error404(self, context, **response_kwargs):
        response_kwargs.setdefault('status', 404)
        return super().render_to_response(context, **response_kwargs)

def error_404_view(request, exception):
    return Error404View.as_view(template_name='404.html')(request)
