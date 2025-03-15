from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Класс для настройки пагинации."""
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 6
