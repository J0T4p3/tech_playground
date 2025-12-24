from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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


class BaseTestCase(TestCase):
    """Base test case with test data fixtures"""

    @classmethod
    def setUpTestData(cls):
        # Create hierarchical company structure
        cls.empresa1 = Empresa.objects.create(nome='Empresa A')
        cls.empresa2 = Empresa.objects.create(nome='Empresa B')

        cls.diretoria1 = Diretoria.objects.create(
            empresa=cls.empresa1, nome='Diretoria Financeira'
        )
        cls.diretoria2 = Diretoria.objects.create(
            empresa=cls.empresa1, nome='Diretoria Operacional'
        )

        cls.gerencia1 = Gerencia.objects.create(
            nome='Gerência Contábil',
            empresa=cls.empresa1,
            diretoria=cls.diretoria1,
        )
        cls.gerencia2 = Gerencia.objects.create(
            nome='Gerência de Produção',
            empresa=cls.empresa1,
            diretoria=cls.diretoria2,
        )

        cls.coordenadoria1 = Coordenadoria.objects.create(
            nome='Coordenadoria Fiscal',
            empresa=cls.empresa1,
            gerencia=cls.gerencia1,
        )
        cls.coordenadoria2 = Coordenadoria.objects.create(
            nome='Coordenadoria de Qualidade',
            empresa=cls.empresa1,
            gerencia=cls.gerencia2,
        )

        cls.area1 = Area.objects.create(
            nome='Área de Auditoria',
            empresa=cls.empresa1,
            cordenadoria=cls.coordenadoria1,
        )
        cls.area2 = Area.objects.create(
            nome='Área de Controle',
            empresa=cls.empresa1,
            cordenadoria=cls.coordenadoria2,
        )

        # Create people
        cls.person1 = Person.objects.create(
            nome='João Silva',
            email='joao.silva@email.com',
            genero='M',
            geracao='Millennials',
        )
        cls.person2 = Person.objects.create(
            nome='Maria Santos',
            email='maria.santos@email.com',
            genero='F',
            geracao='Geração Z',
        )

        # Create employee levels and types
        cls.level1 = EmployeeLevel.objects.create(funcao='Analista')
        cls.level2 = EmployeeLevel.objects.create(funcao='Gerente')

        cls.type1 = EmployeeType.objects.create(cargo='CLT')
        cls.type2 = EmployeeType.objects.create(cargo='PJ')

        # Create employees
        cls.employee1 = Employee.objects.create(
            pessoa=cls.person1,
            empresa=cls.empresa1,
            email_corporativo='joao.silva@empresa.com',
            funcao=cls.level1,
            cargo=cls.type1,
            area=cls.area1,
            estado='SP',
            tempo_de_empresa='2 anos',
        )
        cls.employee2 = Employee.objects.create(
            pessoa=cls.person2,
            empresa=cls.empresa1,
            email_corporativo='maria.santos@empresa.com',
            funcao=cls.level2,
            cargo=cls.type2,
            area=cls.area2,
            estado='RJ',
            tempo_de_empresa='5 anos',
        )

        # Create survey responses
        cls.survey1 = SurveyResponse.objects.create(
            employee=cls.employee1,
            data_da_resposta='2023-01-15',
            interesse_no_cargo=8,
            contribuicao=7,
            aprendizado_e_desenvolvimento=9,
            feedback=6,
            interacao_com_gestor=8,
            clareza_sobre_possibilidades_de_carreira=7,
            expectativa_de_permanencia=9,
            enps=8,
        )
        cls.survey2 = SurveyResponse.objects.create(
            employee=cls.employee2,
            data_da_resposta='2023-01-20',
            interesse_no_cargo=9,
            contribuicao=8,
            aprendizado_e_desenvolvimento=8,
            feedback=7,
            interacao_com_gestor=9,
            clareza_sobre_possibilidades_de_carreira=8,
            expectativa_de_permanencia=8,
            enps=9,
        )


class EmpresaAPITestCase(APITestCase, BaseTestCase):
    """Test cases for EmpresaViewSet"""

    def test_list_empresas(self):
        url = reverse('empresa-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        # Check ordering by nome
        self.assertEqual(response.data['results'][0]['nome'], 'Empresa A')

    def test_retrieve_empresa(self):
        url = reverse('empresa-detail', kwargs={'pk': self.empresa1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Empresa A')


class DiretoriaAPITestCase(APITestCase, BaseTestCase):
    """Test cases for DiretoriaViewSet"""

    def test_list_diretorias(self):
        url = reverse('diretoria-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_diretoria(self):
        url = reverse('diretoria-detail', kwargs={'pk': self.diretoria1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Diretoria Financeira')
        self.assertEqual(response.data['empresa'], 'Empresa A')


class GerenciaAPITestCase(APITestCase, BaseTestCase):
    """Test cases for GerenciaViewSet"""

    def test_list_gerencias(self):
        url = reverse('gerencia-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_gerencia(self):
        url = reverse('gerencia-detail', kwargs={'pk': self.gerencia1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Gerência Contábil')


class CoordenadoriaAPITestCase(APITestCase, BaseTestCase):
    """Test cases for CoordenadoriaViewSet"""

    def test_list_coordenadorias(self):
        url = reverse('coordenadoria-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_coordenadoria(self):
        url = reverse(
            'coordenadoria-detail', kwargs={'pk': self.coordenadoria1.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Coordenadoria Fiscal')


class AreaAPITestCase(APITestCase, BaseTestCase):
    """Test cases for AreaViewSet"""

    def test_list_areas(self):
        url = reverse('area-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_area(self):
        url = reverse('area-detail', kwargs={'pk': self.area1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Área de Auditoria')


class PessoaAPITestCase(APITestCase, BaseTestCase):
    """Test cases for PessoaViewSet"""

    def test_list_pessoas(self):
        url = '/api/pessoas/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_pessoa(self):
        url = f'/api/pessoas/{self.person1.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'João Silva')


class NivelFuncionarioAPITestCase(APITestCase, BaseTestCase):
    """Test cases for NivelFuncionarioViewSet"""

    def test_list_niveis_funcionario(self):
        url = '/api/niveis-funcionario/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_nivel_funcionario(self):
        url = f'/api/niveis-funcionario/{self.level1.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['funcao'], 'Analista')


class TipoFuncionarioAPITestCase(APITestCase, BaseTestCase):
    """Test cases for TipoFuncionarioViewSet"""

    def test_list_tipos_funcionario(self):
        url = '/api/tipos-funcionario/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_tipo_funcionario(self):
        url = f'/api/tipos-funcionario/{self.type1.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cargo'], 'CLT')


class FuncionarioAPITestCase(APITestCase, BaseTestCase):
    """Test cases for FuncionarioViewSet"""

    def test_list_funcionarios(self):
        url = '/api/funcionarios/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_funcionario(self):
        url = f'/api/funcionarios/{self.employee1.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pessoa']['nome'], 'João Silva')


class RespostaPesquisaAPITestCase(APITestCase, BaseTestCase):
    """Test cases for RespostaPesquisaViewSet"""

    def test_list_respostas_pesquisa(self):
        url = '/api/respostas-pesquisa/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_resposta_pesquisa(self):
        url = f'/api/respostas-pesquisa/{self.survey1.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['interesse_no_cargo'], 8)


class PaginationAndOrderingTestCase(APITestCase, BaseTestCase):
    """Test cases for pagination and ordering"""

    def test_pagination(self):
        # Create more data for pagination
        for i in range(15):
            Empresa.objects.create(nome=f'Empresa {i+3}')

        url = reverse('empresa-list')
        response = self.client.get(url, {'page': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

    def test_ordering(self):
        url = reverse('empresa-list')
        response = self.client.get(url, {'ordering': 'nome'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be ordered by nome ascending

    def test_invalid_page(self):
        url = reverse('empresa-list')
        response = self.client.get(url, {'page': 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ErrorHandlingTestCase(APITestCase, BaseTestCase):
    """Test cases for error handling"""

    def test_retrieve_nonexistent(self):
        url = reverse('empresa-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)


class ModelValidationTestCase(TestCase):
    """Test cases for model validators"""

    def test_validate_stripped(self):
        from .models import validate_stripped

        # Valid stripped string
        validate_stripped('test')

        # Invalid unstripped string
        with self.assertRaises(ValidationError):
            validate_stripped(' test ')

    def test_empresa_creation(self):
        empresa = Empresa.objects.create(nome='Test Company')
        self.assertEqual(str(empresa), 'Test Company')

    def test_person_creation(self):
        person = Person.objects.create(
            nome='Test Person',
            email='test@example.com',
            genero='M',
            geracao='Millennials',
        )
        self.assertEqual(str(person), 'Test Person - test@example.com')

    def test_duplicate_person_email(self):
        # Create first person
        Person.objects.create(
            nome='Person 1',
            email='duplicate@example.com',
            genero='M',
            geracao='Millennials',
        )
        # Try to create second with same email
        with self.assertRaises(ValidationError) as cm:
            person2 = Person(
                nome='Person 2',
                email='duplicate@example.com',
                genero='F',
                geracao='Geração Z',
            )
            person2.full_clean()  # This should raise ValidationError
        self.assertIn(
            'Este email já está em uso por outra pessoa.', str(cm.exception)
        )

    def test_duplicate_employee_email_corporativo(self):
        # Create necessary objects
        empresa = Empresa.objects.create(nome='Test Empresa')
        person = Person.objects.create(
            nome='Test Person',
            email='person@example.com',
            genero='M',
            geracao='Millennials',
        )
        level = EmployeeLevel.objects.create(funcao='Test Level')
        type_ = EmployeeType.objects.create(cargo='Test Type')
        diretoria = Diretoria.objects.create(
            empresa=empresa, nome='Test Diretoria'
        )
        gerencia = Gerencia.objects.create(
            nome='Test Gerencia', empresa=empresa, diretoria=diretoria
        )
        coordenadoria = Coordenadoria.objects.create(
            nome='Test Coordenadoria', empresa=empresa, gerencia=gerencia
        )
        area = Area.objects.create(
            nome='Test Area', empresa=empresa, cordenadoria=coordenadoria
        )

        # Create first employee
        Employee.objects.create(
            pessoa=person,
            empresa=empresa,
            email_corporativo='corp@example.com',
            funcao=level,
            cargo=type_,
            area=area,
            estado='SP',
            tempo_de_empresa='1 ano',
        )
        # Try to create second with same email_corporativo
        person2 = Person.objects.create(
            nome='Test Person 2',
            email='person2@example.com',
            genero='F',
            geracao='Geração Z',
        )
        with self.assertRaises(ValidationError) as cm:
            employee2 = Employee(
                pessoa=person2,
                empresa=empresa,
                email_corporativo='corp@example.com',
                funcao=level,
                cargo=type_,
                area=area,
                estado='RJ',
                tempo_de_empresa='2 anos',
            )
            employee2.full_clean()  # This should raise ValidationError
        self.assertIn(
            'Este email corporativo já está em uso por outro funcionário.',
            str(cm.exception),
        )
