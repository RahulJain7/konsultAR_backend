from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 25


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 25


class LargeOffsetPagination(LimitOffsetPagination):
    default_limit = 25
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100
