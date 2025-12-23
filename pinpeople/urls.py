from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.views import (AreaViewSet, CoordenadoriaViewSet, DiretoriaViewSet,
                       EmployeeLevelViewSet, EmployeeTypeViewSet,
                       EmployeeViewSet, EmpresaViewSet, GerenciaViewSet,
                       PersonViewSet, SurveyResponseViewSet)

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'diretorias', DiretoriaViewSet)
router.register(r'gerencias', GerenciaViewSet)
router.register(r'coordenadorias', CoordenadoriaViewSet)
router.register(r'areas', AreaViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'employee-levels', EmployeeLevelViewSet)
router.register(r'employee-types', EmployeeTypeViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'survey-responses', SurveyResponseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
