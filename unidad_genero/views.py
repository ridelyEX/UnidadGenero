from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

class Error404View(TemplateView):
    template_name = '404.html'

    def error404(self, context, **response_kwargs):
        response_kwargs.setdefault('status', 404)
        return super().render_to_response(context, **response_kwargs)

def error_404_view(request, exception):
    return Error404View.as_view(template_name='404.html')(request)
