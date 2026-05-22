from django.urls import path

from .views import vista

urlpatterns = [
    path('', view=vista, name='vista_temp'),

]