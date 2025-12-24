# Conjuntos de visões para a API REST (somente leitura)
from django.http import Http404
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

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
from .serializers import (
    SerializadorArea,
    SerializadorCoordenadoria,
    SerializadorDiretoria,
    SerializadorEmpresa,
    SerializadorFuncionario,
    SerializadorGerencia,
    SerializadorNivelFuncionario,
    SerializadorPessoa,
    SerializadorRespostaPesquisa,
    SerializadorTipoFuncionario,
)


class BaseReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Base ViewSet com tratamento de erros aprimorado"""

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='page',
                type=int,
                description='Número da página (deve ser > 0)',
                required=False,
            ),
            OpenApiParameter(
                name='ordering',
                type=str,
                description='Campo de ordenação (ex.: nome, -nome)',
                required=False,
            ),
        ],
        responses={
            200: None,  # Will be auto-generated
            400: OpenApiResponse(
                description='Requisição Inválida - Paginação inválida (número da página <=0) ou parâmetros de ordenação'
            ),
            404: OpenApiResponse(
                description='Não Encontrado - Página não encontrada'
            ),
            500: OpenApiResponse(
                description='Erro Interno do Servidor - Erro inesperado do servidor'
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except Http404:
            return Response({'detail': 'Página não encontrada.'}, status=404)
        except Exception as e:
            return Response(
                {'detail': 'Erro interno do servidor.'}, status=500
            )

    @extend_schema(
        responses={
            200: None,  # Will be auto-generated
            400: OpenApiResponse(
                description='Requisição Inválida - Parâmetros de entrada inválidos'
            ),
            404: OpenApiResponse(
                description='Não Encontrado - Objeto não encontrado'
            ),
            500: OpenApiResponse(
                description='Erro Interno do Servidor - Erro inesperado do servidor'
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except Http404:
            return Response({'detail': 'Objeto não encontrado.'}, status=404)
        except Exception as e:
            return Response(
                {'detail': 'Erro interno do servidor.'}, status=500
            )


@extend_schema_view(
    list=extend_schema(
        operation_id='list_empresas',
        summary='Listar Empresas',
        description='Retorna uma lista paginada de empresas. Campos disponíveis para ordenação: nome.',
    ),
    retrieve=extend_schema(
        operation_id='retrieve_empresa',
        summary='Detalhes da Empresa',
        description='Retorna os detalhes de uma empresa específica.',
    ),
)
class EmpresaViewSet(BaseReadOnlyModelViewSet):
    """Conjunto de visões para Empresa"""

    queryset = Empresa.objects.all()
    serializer_class = SerializadorEmpresa
    ordering_fields = ['nome']


@extend_schema_view(
    list=extend_schema(
        operation_id='list_diretorias',
        summary='Listar Diretorias',
        description='Retorna uma lista paginada de diretorias. Campos disponíveis para ordenação: nome, empresa.',
    ),
    retrieve=extend_schema(
        operation_id='retrieve_diretoria',
        summary='Detalhes da Diretoria',
        description='Retorna os detalhes de uma diretoria específica.',
    ),
)
class DiretoriaViewSet(BaseReadOnlyModelViewSet):
    """Conjunto de visões para Diretoria"""

    queryset = Diretoria.objects.all()
    serializer_class = SerializadorDiretoria
    ordering_fields = ['nome', 'empresa']


@extend_schema_view(
    list=extend_schema(
        operation_id='list_gerencias',
        summary='Listar Gerências',
        description='Retorna uma lista paginada de gerências. Campos disponíveis para ordenação: nome, empresa, diretoria.',
    ),
    retrieve=extend_schema(
        operation_id='retrieve_gerencia',
        summary='Detalhes da Gerência',
        description='Retorna os detalhes de uma gerência específica.',
    ),
)
class GerenciaViewSet(BaseReadOnlyModelViewSet):
    """Conjunto de visões para Gerencia"""

    queryset = Gerencia.objects.all()
    serializer_class = SerializadorGerencia
    ordering_fields = ['nome', 'empresa', 'diretoria']


@extend_schema_view(
    list=extend_schema(
        operation_id='list_coordenadorias',
        summary='Listar Coordenadorias',
        description='Retorna uma lista paginada de coordenadorias. Campos disponíveis para ordenação: nome, empresa, gerencia.',
    ),
    retrieve=extend_schema(
        operation_id='retrieve_coordenadoria',
        summary='Detalhes da Coordenadoria',
        description='Retorna os detalhes de uma coordenadoria específica.',
    ),
)
class CoordenadoriaViewSet(BaseReadOnlyModelViewSet):
    """Conjunto de visões para Coordenadoria"""

    queryset = Coordenadoria.objects.all()
    serializer_class = SerializadorCoordenadoria
    ordering_fields = ['nome', 'empresa', 'gerencia']


@extend_schema_view(
    list=extend_schema(
        operation_id='list_areas',
        summary='Listar Áreas',
        description='Retorna uma lista paginada de áreas. Campos disponíveis para ordenação: nome, empresa, cordenadoria.',
    ),
    retrieve=extend_schema(
        operation_id='retrieve_area',
        summary='Detalhes da Área',
        description='Retorna os detalhes de uma área específica.',
    ),
)
class AreaViewSet(BaseReadOnlyModelViewSet):
    """Conjunto de visões para Area"""

    queryset = Area.objects.all()
    serializer_class = SerializadorArea
    ordering_fields = ['nome', 'empresa', 'cordenadoria']


@extend_schema_view(
    list=extend_schema(
        operation_id='list_pessoas',
        summary='Listar Pessoas',
        description='Retorna uma lista paginada de pessoas. Campos disponíveis para ordenação: nome, email, genero, geracao.',
    ),
    retrieve=extend_schema(
        operation_id='retrieve_pessoa',
        summary='Detalhes da Pessoa',
        description='Retorna os detalhes de uma pessoa específica.',
    ),
)
class PessoaViewSet(BaseReadOnlyModelViewSet):
    """Conjunto de visões para Pessoa"""

    queryset = Person.objects.all()
    serializer_class = SerializadorPessoa
    ordering_fields = ['nome', 'email', 'genero', 'geracao']


@extend_schema_view(
    list=extend_schema(
        operation_id='list_niveis_funcionario',
        summary='Listar Níveis de Funcionário',
        description='Retorna uma lista paginada de níveis de funcionário. Campos disponíveis para ordenação: funcao.',
    ),
    retrieve=extend_schema(
        operation_id='retrieve_nivel_funcionario',
        summary='Detalhes do Nível de Funcionário',
        description='Retorna os detalhes de um nível de funcionário específico.',
    ),
)
class NivelFuncionarioViewSet(BaseReadOnlyModelViewSet):
    """Conjunto de visões para Nível de Funcionário"""

    queryset = EmployeeLevel.objects.all()
    serializer_class = SerializadorNivelFuncionario
    ordering_fields = ['funcao']


@extend_schema_view(
    list=extend_schema(
        operation_id='list_tipos_funcionario',
        summary='Listar Tipos de Funcionário',
        description='Retorna uma lista paginada de tipos de funcionário. Campos disponíveis para ordenação: cargo.',
    ),
    retrieve=extend_schema(
        operation_id='retrieve_tipo_funcionario',
        summary='Detalhes do Tipo de Funcionário',
        description='Retorna os detalhes de um tipo de funcionário específico.',
    ),
)
class TipoFuncionarioViewSet(BaseReadOnlyModelViewSet):
    """Conjunto de visões para Tipo de Funcionário"""

    queryset = EmployeeType.objects.all()
    serializer_class = SerializadorTipoFuncionario
    ordering_fields = ['cargo']


@extend_schema_view(
    list=extend_schema(
        operation_id='list_funcionarios',
        summary='Listar Funcionários',
        description='Retorna uma lista paginada de funcionários. Campos disponíveis para ordenação: pessoa__nome, empresa, funcao, cargo, area, estado.',
    ),
    retrieve=extend_schema(
        operation_id='retrieve_funcionario',
        summary='Detalhes do Funcionário',
        description='Retorna os detalhes de um funcionário específico.',
    ),
)
class FuncionarioViewSet(BaseReadOnlyModelViewSet):
    """Conjunto de visões para Funcionário"""

    queryset = Employee.objects.all()
    serializer_class = SerializadorFuncionario
    ordering_fields = [
        'pessoa__nome',
        'empresa',
        'funcao',
        'cargo',
        'area',
        'estado',
    ]


@extend_schema_view(
    list=extend_schema(
        operation_id='list_respostas_pesquisa',
        summary='Listar Respostas de Pesquisa',
        description='Retorna uma lista paginada de respostas de pesquisa. Campos disponíveis para ordenação: employee__pessoa__nome, data_da_resposta.',
    ),
    retrieve=extend_schema(
        operation_id='retrieve_resposta_pesquisa',
        summary='Detalhes da Resposta de Pesquisa',
        description='Retorna os detalhes de uma resposta de pesquisa específica.',
    ),
)
class RespostaPesquisaViewSet(BaseReadOnlyModelViewSet):
    """Conjunto de visões para Resposta de Pesquisa"""

    queryset = SurveyResponse.objects.all()
    serializer_class = SerializadorRespostaPesquisa
    ordering_fields = ['employee__pessoa__nome', 'data_da_resposta']
