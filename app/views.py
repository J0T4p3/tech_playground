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
    ordering_fields = ['nome']


class DiretoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Diretoria"""
    queryset = Diretoria.objects.all()
    serializer_class = SerializadorDiretoria
    ordering_fields = ['nome', 'empresa']


class GerenciaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Gerencia"""
    queryset = Gerencia.objects.all()
    serializer_class = SerializadorGerencia
    ordering_fields = ['nome', 'empresa', 'diretoria']


class CoordenadoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Coordenadoria"""
    queryset = Coordenadoria.objects.all()
    serializer_class = SerializadorCoordenadoria
    ordering_fields = ['nome', 'empresa', 'gerencia']


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Area"""
    queryset = Area.objects.all()
    serializer_class = SerializadorArea
    ordering_fields = ['nome', 'empresa', 'cordenadoria']


class PessoaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Person"""
    queryset = Person.objects.all()
    serializer_class = SerializadorPessoa
    ordering_fields = ['nome', 'email', 'genero', 'geracao']


class NivelFuncionarioViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para EmployeeLevel"""
    queryset = EmployeeLevel.objects.all()
    serializer_class = SerializadorNivelFuncionario
    ordering_fields = ['funcao']


class TipoFuncionarioViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para EmployeeType"""
    queryset = EmployeeType.objects.all()
    serializer_class = SerializadorTipoFuncionario
    ordering_fields = ['cargo']


class FuncionarioViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para Employee"""
    queryset = Employee.objects.all()
    serializer_class = SerializadorFuncionario
    ordering_fields = ['pessoa__nome', 'empresa', 'funcao', 'cargo', 'area', 'estado']


class RespostaPesquisaViewSet(viewsets.ReadOnlyModelViewSet):
    """Conjunto de visões para SurveyResponse"""
    queryset = SurveyResponse.objects.all()
    serializer_class = SerializadorRespostaPesquisa
    ordering_fields = ['employee__pessoa__nome', 'data_da_resposta']
