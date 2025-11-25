"""
Standard pagination classes for TTMS and PTMS APIs.
"""

from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Standard pagination for all API endpoints.
    Page size can be overridden via query parameter.
    """
    page_size = 100
    page_size_query_param = 'page_size'
    page_size_query_description = 'Number of results to return per page.'
    max_page_size = 1000


class SmallPagination(PageNumberPagination):
    """
    Smaller page size for list endpoints.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    page_size_query_description = 'Number of results to return per page.'
    max_page_size = 500


class LargePagination(PageNumberPagination):
    """
    Larger page size for export/bulk operations.
    """
    page_size = 500
    page_size_query_param = 'page_size'
    page_size_query_description = 'Number of results to return per page.'
    max_page_size = 5000
