from rest_framework import serializers

from .models import (Area, Coordenadoria, Diretoria, Employee, EmployeeLevel,
                     EmployeeType, Empresa, Gerencia, Person, SurveyResponse)


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class DiretoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diretoria
        fields = '__all__'


class GerenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gerencia
        fields = '__all__'


class CoordenadoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenadoria
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class EmployeeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLevel
        fields = '__all__'


class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeType
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = '__all__'
