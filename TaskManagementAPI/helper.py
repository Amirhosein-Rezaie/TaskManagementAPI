from rest_framework.request import Request
from django.db.models import Model
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import (
    ForeignKey, OneToOneField, ManyToManyField,
    CharField, IntegerField, TextField
)
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import FieldDoesNotExist, FieldError


# set limit of paginators in class and function base views
def limit_paginate(request: Request, pagination_class: PageNumberPagination):
    """
    get limit from query params and return
    """
    if request.query_params.get('limit'):
        return request.query_params.get('limit')
    return pagination_class.page_size


# functions
def dynamic_search(
    request: Request, model: Model, serializer: ModelSerializer,
    pagination_class: PageNumberPagination
):
    """
    a function that you can have dynamic search
    """

    # variables
    like = "istartswith"
    out_query_params = ['limit', 'page']
    paginator = pagination_class
    equal_to_fields = ['id']

    query_params = request.query_params
    if query_params:
        query_search = Q()

        for key, value in query_params.items():
            if key in out_query_params:
                continue

            if not value:
                return Response(
                    {
                        "error": "value for search is empty",
                        "message": "مقدار برای جست و جو وجود ندارد"
                    },
                    status=status.HTTP_400_BAD_REQUEST)

            search_items = key.split('-')
            field_name = search_items[0]

            try:
                field_obj = model._meta.get_field(field_name)

                if isinstance(field_obj, (ForeignKey, ManyToManyField, OneToOneField)):
                    try:
                        sub_field_name = search_items[1]
                        if sub_field_name.lower() not in equal_to_fields:
                            query_search &= Q(
                                **{f"{field_name}__{sub_field_name}__{like}": value}
                            )
                        else:
                            query_search &= Q(
                                **{f"{field_name}__{sub_field_name}": value}
                            )
                    except IndexError:
                        return Response(
                            data={
                                "error": "Set second field for foreign fields",
                                "message": "برای کلید های خارجی حتما فیلد دوم تعیین کنید"
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    if field_name.lower() not in equal_to_fields:
                        query_search &= Q(
                            **{f"{field_name}__{like}": value}
                        )
                    else:
                        query_search &= Q(
                            **{f"{field_name}": value}
                        )
            except (FieldDoesNotExist, FieldError):
                return Response(
                    data={
                        "error": "Not found field",
                        "message": "فیلد مورد نظر یافت نشد"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        founds = model.objects.filter(query_search)
        limit_paginate(request=request, pagination_class=paginator)
        paginated_founds = paginator.paginate_queryset(founds, request)
        serialize_found = serializer(paginated_founds, many=True)
        return paginator.get_paginated_response(serialize_found.data)
