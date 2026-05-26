from django.urls import path
from formtools.wizard.views import WizardView

from .views import (
    CasoListView, CasoCreateView,
    CasoUpdateView, CasoDeleteView, CasoCloseView
)
from .wizards import CreateCasoWizard, FORMS, CONDITIONS

urlpatterns = [
    path('expediente/', CasoListView.as_view(), name='expediente_list'),
    path('expediente/nuevo/', CasoCreateView.as_view(), name='expediente_create'),
    path('expediente/<int:pk>/editar/', CasoUpdateView.as_view(), name='expediente_update'),
    path('expediente/<int:pk>/cerrar/', CasoCloseView.as_view(), name='expediente_cerrar'),
    path('expediente/<int:pk>/eliminar/', CasoDeleteView.as_view(), name='expediente_delete'),
    path('expediente/denuncia/wizard', CreateCasoWizard.as_view(FORMS, condition_dict=CONDITIONS), name='expediente_wizard'),
]
