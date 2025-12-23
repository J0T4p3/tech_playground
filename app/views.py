# Conjuntos de visões para a API REST (somente leitura)
from rest_framework import viewsets

from .models import (Area, Coordenadoria, Diretoria, Employee, EmployeeLevel,
                     EmployeeType, Empresa, Gerencia, Person, SurveyResponse)
from .serializers import (SerializadorArea, SerializadorCoordenadoria,
                          SerializadorDiretoria, SerializadorEmpresa,
                          SerializadorFuncionario, SerializadorGerencia,
                          SerializadorNivelFuncionario, SerializadorPessoa,
                          SerializadorRespostaPesquisa,
                          SerializadorTipoFuncionario)


class EmpresaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Empresa"""
    queryset = Empresa.objects.all()
    serializer_class = SerializadorEmpresa


class DiretoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Diretoria"""
    queryset = Diretoria.objects.all()
    serializer_class = SerializadorDiretoria


class GerenciaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Gerencia"""
    queryset = Gerencia.objects.all()
    serializer_class = SerializadorGerencia


class CoordenadoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Coordenadoria"""
    queryset = Coordenadoria.objects.all()
    serializer_class = SerializadorCoordenadoria


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Area"""
    queryset = Area.objects.all()
    serializer_class = SerializadorArea


class PessoaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Person"""
    queryset = Person.objects.all()
    serializer_class = SerializadorPessoa


class NivelFuncionarioViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para EmployeeLevel"""
    queryset = EmployeeLevel.objects.all()
    serializer_class = SerializadorNivelFuncionario


class TipoFuncionarioViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para EmployeeType"""
    queryset = EmployeeType.objects.all()
    serializer_class = SerializadorTipoFuncionario


class FuncionarioViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Employee"""
    queryset = Employee.objects.all()
    serializer_class = SerializadorFuncionario


class RespostaPesquisaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para SurveyResponse"""
    queryset = SurveyResponse.objects.all()
    serializer_class = SerializadorRespostaPesquisa
