from rest_framework.pagination import PageNumberPagination


class MyLimitPaginator(PageNumberPagination):
    max_limit: int = 10
    page_query_param: str = "p"
    max_page_size: int = 100
    