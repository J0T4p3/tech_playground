from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Paginação personalizada com validação de número de página e tamanho de página"""

    def paginate_queryset(self, queryset, request, view=None):
        # Obter o número da página solicitado
        page_number_param = request.query_params.get(self.page_query_param, 1)

        try:
            requested_page_number = int(page_number_param)
        except ValueError:
            raise ValidationError({"detail": "Número de página inválido. Deve ser um número inteiro."})

        if requested_page_number <= 0:
            raise ValidationError({"detail": "Número de página deve ser maior que 0."})

        # Calcular o offset e verificar se excede o total de itens
        total_count = queryset.count()
        offset = (requested_page_number - 1) * self.page_size
        if offset >= total_count and total_count > 0:
            raise ValidationError({"detail": f"Número de página {requested_page_number} excede o total de itens disponíveis."})

        # Chamar o método pai para obter a página
        page = super().paginate_queryset(queryset, request, view)

        # Verificar se a página solicitada é válida
        if page is not None:
            total_pages = self.page.paginator.num_pages
            if requested_page_number > total_pages:
                raise ValidationError({"detail": f"Número de página {requested_page_number} excede o total de páginas disponíveis ({total_pages})."})

        return page
