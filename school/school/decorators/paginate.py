from functools import wraps
from django.db.models import QuerySet
from rest_framework.response import Response

def paginate(serializer_class):

    def _paginate(func):

        @wraps(func)
        def inner(self, *args, **kwargs):
            queryset = func(self, *args, **kwargs)
            assert isinstance(queryset, (list, QuerySet)), "apply_pagination expects a List or a QuerySet"

            page = self.paginate_queryset(queryset)

            if page:
                serializer = serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data)
            
        return inner

    return _paginate