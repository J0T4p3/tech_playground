# URLs do projeto
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.views import (AreaViewSet, CoordenadoriaViewSet, DiretoriaViewSet,
                       EmpresaViewSet, FuncionarioViewSet, GerenciaViewSet,
                       NivelFuncionarioViewSet, PessoaViewSet,
                       RespostaPesquisaViewSet, TipoFuncionarioViewSet)

# Roteador para a API
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'diretorias', DiretoriaViewSet)
router.register(r'gerencias', GerenciaViewSet)
router.register(r'coordenadorias', CoordenadoriaViewSet)
router.register(r'areas', AreaViewSet)
router.register(r'pessoas', PessoaViewSet)
router.register(r'niveis-funcionario', NivelFuncionarioViewSet)
router.register(r'tipos-funcionario', TipoFuncionarioViewSet)
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'respostas-pesquisa', RespostaPesquisaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
