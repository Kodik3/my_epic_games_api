from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList
from abstracts.mixins import ResponseMixin


class UserPageNumberPaginator(PageNumberPagination):
    """
    Пагинатор для вывода данных о пользователях.

    Параметры:
        - page_size_query_param (str): Параметр запроса для указания размера страницы.

        - page_query_param (str): Параметр запроса для указания номера страницы.

        - max_page_size (int): Максимально допустимый количество элементов на страницу.

        - page_size (int): Количество элементов на страницу по умолчанию.

    Пример запроса:
        /user/?page=2&size=10
    """
    page_size_query_param: str = 'size'
    page_query_param: str = "p"

    page_size: int = 10
    max_page_size: int = page_size

    def get_paginated_response(self, data: ReturnList) -> Response:
        response: Response = Response(
                {
                    'pagination': {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link(),
                        'pages': self.page.paginator.num_pages,
                        'count': self.page.paginator.count
                    },
                    'results': data
                }
            )
        return response
    
class UserLimitOffsetPaginator(LimitOffsetPagination):
    offset: int = 0
    limit: int = 2

    def get_paginated_response(self, data: ReturnList) -> Response:
        response: Response = Response(
                {
                    'pagination': {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link()
                    },
                    'results': data
                }
            )
        return response
