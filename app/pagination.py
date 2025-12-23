from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Paginação personalizada com validação de número de página"""

    def paginate_queryset(self, queryset, request, view=None):
        # Obter o número da página solicitado
        page_number_param = request.query_params.get(self.page_query_param, 1)

        try:
            requested_page_number = int(page_number_param)
        except ValueError:
            raise ValidationError({"detail": "Número de página inválido. Deve ser um número inteiro."})

        if requested_page_number <= 0:
            raise ValidationError({"detail": "Número de página deve ser maior que 0."})

        # Chamar o método pai para obter a página
        page = super().paginate_queryset(queryset, request, view)

        # Verificar se a página solicitada é válida
        if page is not None:
            total_pages = self.page.paginator.num_pages
            if requested_page_number > total_pages:
                raise ValidationError({"detail": f"Número de página {requested_page_number} excede o total de páginas disponíveis ({total_pages})."})

        return page
