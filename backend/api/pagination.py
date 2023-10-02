from rest_framework.pagination import PageNumberPagination

from django.conf import settings as conf_settings


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = conf_settings.REST_FRAMEWORK['PAGE_SIZE']
