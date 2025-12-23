from django.db import models

from .constants import STATE_CHOICES


# Modelos desenhados para escalar a solução de forma hierárquica
class Empresa(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Compania")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nome']

class Diretoria(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    nome = models.CharField(max_length=255, verbose_name="Diretoria")

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome}"

    class Meta:
        verbose_name = "Diretoria"
        verbose_name_plural = "Diretorias"
        ordering = ['nome']

class Gerencia(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Gerência")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    diretoria = models.ForeignKey(Diretoria, on_delete=models.CASCADE, verbose_name="Diretoria")

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome}"

    class Meta:
        verbose_name = "Gerência"
        verbose_name_plural = "Gerências"
        ordering = ['nome']

class Coordenadoria(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Coordenadoria")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    gerencia = models.ForeignKey(Gerencia, on_delete=models.CASCADE, verbose_name="Gerência")

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome}"

    class Meta:
        verbose_name = "Coordenadoria"
        verbose_name_plural = "Coordenadorias"
        ordering = ['nome']

class Area(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Área")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    cordenadoria = models.ForeignKey(Coordenadoria, on_delete=models.CASCADE, verbose_name="Coordenadoria")

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome}"

    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"
        ordering = ['nome']

class Person(models.Model):
    # Definindo escolhas para gênero e geração
    class GenderChoices(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMININO = "F", "Feminino"
        OUTRO = "O", "Outro"
    class GenerationChoices(models.TextChoices):
        BABY_BOOMERS = "Baby Boomers"
        GERACAO_X = "Geração X"
        MILLENNIALS = "Millennials"
        GERACAO_Z = "Geração Z"

    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(verbose_name="Email")
    genero = models.CharField(max_length=1, choices=GenderChoices.choices, verbose_name="Gênero")
    geracao = models.CharField(max_length=20, choices=GenerationChoices.choices, verbose_name="Geração")

    def __str__(self):
        return f"{self.nome} - {self.email}"

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ['nome']

class EmployeeLevel(models.Model):
    funcao = models.CharField(max_length=255, verbose_name="Função")

    def __str__(self):
        return self.funcao

    class Meta:
        verbose_name = "Função"
        verbose_name_plural = "Funções"
        ordering = ['funcao']

class EmployeeType(models.Model):
    cargo = models.CharField(max_length=255, verbose_name="Cargo")

    def __str__(self):
        return self.cargo

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['cargo']

class Employee(models.Model):
    pessoa = models.OneToOneField(Person, on_delete=models.CASCADE, verbose_name="Funcionário")

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    email_corporativo = models.EmailField(verbose_name="Email Corporativo")
    funcao = models.ForeignKey(EmployeeLevel, on_delete=models.CASCADE, verbose_name="Função")
    cargo = models.ForeignKey(EmployeeType, on_delete=models.CASCADE, verbose_name="Cargo")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="Área")
    estado = models.CharField(max_length=2, choices=STATE_CHOICES, verbose_name="Estado")
    tempo_de_empresa = models.CharField(max_length=20, verbose_name="Tempo de Empresa")

    def __str__(self):
        return f"[{self.empresa}] {self.pessoa.nome} - {self.pessoa.email}"

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['pessoa__nome']


class SurveyResponse(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Funcionário") # Relação com o funcionário que respondeu a pesquisa
    data_da_resposta = models.DateField(verbose_name="Respondido em")

    interesse_no_cargo = models.IntegerField(verbose_name="Interesse no cargo")
    comentarios_interesse_no_cargo = models.TextField(blank=True, verbose_name="Interesse no cargo - Comentários")

    contribuicao = models.IntegerField(verbose_name="Contribuição")
    comentarios_contribuicao = models.TextField(blank=True, verbose_name="Comentários - Contribuição")

    aprendizado_e_desenvolvimento = models.IntegerField(verbose_name="Aprendizado e Desenvolvimento")
    comentarios_aprendizado_e_desenvolvimento = models.TextField(blank=True, verbose_name="Comentários - Aprendizado e Desenvolvimento")

    feedback = models.IntegerField(verbose_name="Feedback")
    comentarios_feedback = models.TextField(blank=True, verbose_name="Comentários - Feedback")

    interacao_com_gestor = models.IntegerField(verbose_name="Interação com o Gestor")
    comentarios_interacao_com_gestor = models.TextField(blank=True, verbose_name="Comentários - Interação com o Gestor")

    clareza_sobre_possibilidades_de_carreira = models.IntegerField(verbose_name="Clareza sobre Possibilidades de Carreira")
    comentarios_clareza_sobre_possibilidades_de_carreira = models.TextField(blank=True, verbose_name="Comentários - Clareza sobre Possibilidades de Carreira")

    expectativa_de_permanencia = models.IntegerField(verbose_name="Expectativa de Permanência")
    comentarios_expectativa_de_permanencia = models.TextField(blank=True, verbose_name="Comentários - Expectativa de Permanência")

    enps = models.IntegerField(verbose_name="eNPS")
    aberta_enps = models.TextField(blank=True, verbose_name="Comentários - eNPS")

    def __str__(self):
        return f"{self.data_da_resposta} - {self.employee.pessoa.nome} ({self.employee.empresa.nome})"

    class Meta:
        verbose_name = "Resposta de Pesquisa"
        verbose_name_plural = "Respostas de Pesquisas"
        ordering = ['-data_da_resposta']

