import csv
import os
from datetime import datetime

from django.core.management import call_command
from django.core.management.base import BaseCommand

from app.constants import STATE_CHOICES
from app.models import (
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


class Command(BaseCommand):
    help = 'Importar dados do data.csv para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file',
            type=str,
            required=True,
            help='Caminho para o arquivo CSV',
        )
        parser.add_argument(
            '--database',
            type=str,
            default='default',
            help='Banco de dados a ser usado',
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        database = options['database']
        # Run pending migrations
        self.stdout.write('Running migrations...')
        call_command('migrate', database=database, verbosity=0)
        self.stdout.write(self.style.SUCCESS('Migrations completed.'))
        if not os.path.exists(csv_file):
            self.stdout.write(
                self.style.ERROR(f'Arquivo {csv_file} não existe')
            )
            return

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                try:
                    # Criar hierarquia
                    empresa, _ = Empresa.objects.using(database).get_or_create(
                        nome=row['n0_empresa']
                    )
                    diretoria, _ = Diretoria.objects.using(
                        database
                    ).get_or_create(nome=row['n1_diretoria'], empresa=empresa)
                    gerencia, _ = Gerencia.objects.using(
                        database
                    ).get_or_create(
                        nome=row['n2_gerencia'],
                        empresa=empresa,
                        diretoria=diretoria,
                    )
                    coordenadoria, _ = Coordenadoria.objects.using(
                        database
                    ).get_or_create(
                        nome=row['n3_coordenacao'],
                        empresa=empresa,
                        gerencia=gerencia,
                    )
                    area, _ = Area.objects.using(database).get_or_create(
                        nome=row['n4_area'],
                        empresa=empresa,
                        cordenadoria=coordenadoria,
                    )

                    # Criar EmployeeLevel e EmployeeType
                    level, _ = EmployeeLevel.objects.using(
                        database
                    ).get_or_create(funcao=row['funcao'])
                    emp_type, _ = EmployeeType.objects.using(
                        database
                    ).get_or_create(cargo=row['cargo'])

                    # Criar Person
                    person, _ = Person.objects.using(database).get_or_create(
                        nome=row['nome'],
                        email=row['email'],
                        defaults={
                            'genero': row['genero'],
                            'geracao': row['geracao'],
                        },
                    )

                    # Mapear localidade para estado
                    estado = row['localidade']
                    for code, name in STATE_CHOICES:
                        if name.lower() == row['localidade'].lower():
                            estado = code
                            break

                    # Criar Employee
                    employee, _ = Employee.objects.using(
                        database
                    ).get_or_create(
                        pessoa=person,
                        defaults={
                            'empresa': empresa,
                            'email_corporativo': row['email_corporativo'],
                            'funcao': level,
                            'cargo': emp_type,
                            'area': area,
                            'estado': estado,
                            'tempo_de_empresa': row['tempo_de_empresa'],
                        },
                    )

                    # Analisar data
                    data_resposta = datetime.strptime(
                        row['Data da Resposta'], '%d/%m/%Y'
                    ).date()

                    # Criar SurveyResponse
                    SurveyResponse.objects.using(database).get_or_create(
                        employee=employee,
                        data_da_resposta=data_resposta,
                        defaults={
                            'interesse_no_cargo': int(
                                row['Interesse no Cargo']
                            ),
                            'comentarios_interesse_no_cargo': row[
                                'Comentários - Interesse no Cargo'
                            ]
                            or '',
                            'contribuicao': int(row['Contribuição']),
                            'comentarios_contribuicao': row[
                                'Comentários - Contribuição'
                            ]
                            or '',
                            'aprendizado_e_desenvolvimento': int(
                                row['Aprendizado e Desenvolvimento']
                            ),
                            'comentarios_aprendizado_e_desenvolvimento': row[
                                'Comentários - Aprendizado e Desenvolvimento'
                            ]
                            or '',
                            'feedback': int(row['Feedback']),
                            'comentarios_feedback': row[
                                'Comentários - Feedback'
                            ]
                            or '',
                            'interacao_com_gestor': int(
                                row['Interação com Gestor']
                            ),
                            'comentarios_interacao_com_gestor': row[
                                'Comentários - Interação com Gestor'
                            ]
                            or '',
                            'clareza_sobre_possibilidades_de_carreira': int(
                                row['Clareza sobre Possibilidades de Carreira']
                            ),
                            'comentarios_clareza_sobre_possibilidades_de_carreira': row[
                                'Comentários - Clareza sobre Possibilidades de Carreira'
                            ]
                            or '',
                            'expectativa_de_permanencia': int(
                                row['Expectativa de Permanência']
                            ),
                            'comentarios_expectativa_de_permanencia': row[
                                'Comentários - Expectativa de Permanência'
                            ]
                            or '',
                            'enps': int(row['eNPS']),
                            'aberta_enps': row['[Aberta] eNPS'] or '',
                        },
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Erro ao processar linha: {e}')
                    )
                    continue

        self.stdout.write(self.style.SUCCESS('Importação de dados concluída'))
