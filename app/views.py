from rest_framework import viewsets

from .models import (Area, Coordenadoria, Diretoria, Employee, EmployeeLevel,
                     EmployeeType, Empresa, Gerencia, Person, SurveyResponse)
from .serializers import (AreaSerializer, CoordenadoriaSerializer,
                          DiretoriaSerializer, EmployeeLevelSerializer,
                          EmployeeSerializer, EmployeeTypeSerializer,
                          EmpresaSerializer, GerenciaSerializer,
                          PersonSerializer, SurveyResponseSerializer)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class DiretoriaViewSet(viewsets.ModelViewSet):
    queryset = Diretoria.objects.all()
    serializer_class = DiretoriaSerializer


class GerenciaViewSet(viewsets.ModelViewSet):
    queryset = Gerencia.objects.all()
    serializer_class = GerenciaSerializer


class CoordenadoriaViewSet(viewsets.ModelViewSet):
    queryset = Coordenadoria.objects.all()
    serializer_class = CoordenadoriaSerializer


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class EmployeeLevelViewSet(viewsets.ModelViewSet):
    queryset = EmployeeLevel.objects.all()
    serializer_class = EmployeeLevelSerializer


class EmployeeTypeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeType.objects.all()
    serializer_class = EmployeeTypeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class SurveyResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer
