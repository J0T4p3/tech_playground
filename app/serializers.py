# Serializadores para a API REST
from rest_framework import serializers

from .models import (
    Area,
    Coordenadoria,
    Diretoria,
    Employee,
    EmployeeLevel,
    EmployeeType,
    Empresa,
    Gerencia,
    Person,
    SurveyResponse,
)


class SerializadorEmpresa(serializers.ModelSerializer):
    """Serializador para o modelo Empresa"""

    class Meta:
        model = Empresa
        fields = ['nome']


class SerializadorDiretoria(serializers.ModelSerializer):
    """Serializador para o modelo Diretoria"""

    empresa = serializers.StringRelatedField()

    class Meta:
        model = Diretoria
        fields = ['empresa', 'nome']


class SerializadorGerencia(serializers.ModelSerializer):
    """Serializador para o modelo Gerencia"""

    empresa = serializers.StringRelatedField()
    diretoria = serializers.StringRelatedField()

    class Meta:
        model = Gerencia
        fields = ['nome', 'empresa', 'diretoria']


class SerializadorCoordenadoria(serializers.ModelSerializer):
    """Serializador para o modelo Coordenadoria"""

    empresa = serializers.StringRelatedField()
    gerencia = serializers.StringRelatedField()

    class Meta:
        model = Coordenadoria
        fields = ['nome', 'empresa', 'gerencia']


class SerializadorArea(serializers.ModelSerializer):
    """Serializador para o modelo Area"""

    empresa = serializers.StringRelatedField()
    cordenadoria = serializers.StringRelatedField()

    class Meta:
        model = Area
        fields = ['nome', 'empresa', 'cordenadoria']


class SerializadorPessoa(serializers.ModelSerializer):
    """Serializador para o modelo Pessoa"""

    class Meta:
        model = Person
        fields = ['nome', 'email', 'genero', 'geracao']


class SerializadorNivelFuncionario(serializers.ModelSerializer):
    """Serializador para o modelo Nível Funcionário"""

    class Meta:
        model = EmployeeLevel
        fields = ['funcao']


class SerializadorTipoFuncionario(serializers.ModelSerializer):
    """Serializador para o modelo Tipo Funcionário"""

    class Meta:
        model = EmployeeType
        fields = ['cargo']


class SerializadorFuncionario(serializers.ModelSerializer):
    """Serializador para o modelo Funcionário"""

    pessoa = SerializadorPessoa()
    empresa = serializers.StringRelatedField()
    area = serializers.StringRelatedField()
    funcao = serializers.StringRelatedField()
    cargo = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = [
            'pessoa',
            'empresa',
            'email_corporativo',
            'funcao',
            'cargo',
            'area',
            'estado',
            'tempo_de_empresa',
        ]


class SerializadorRespostaPesquisa(serializers.ModelSerializer):
    """Serializador para o modelo Resposta Pesquisa"""

    funcionario = serializers.StringRelatedField()

    class Meta:
        model = SurveyResponse
        fields = [
            'funcionario',
            'data_da_resposta',
            'interesse_no_cargo',
            'comentarios_interesse_no_cargo',
            'contribuicao',
            'comentarios_contribuicao',
            'aprendizado_e_desenvolvimento',
            'comentarios_aprendizado_e_desenvolvimento',
            'feedback',
            'comentarios_feedback',
            'interacao_com_gestor',
            'comentarios_interacao_com_gestor',
            'clareza_sobre_possibilidades_de_carreira',
            'comentarios_clareza_sobre_possibilidades_de_carreira',
            'expectativa_de_permanencia',
            'comentarios_expectativa_de_permanencia',
            'enps',
            'aberta_enps',
        ]
