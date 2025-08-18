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
from django.core.exceptions import FieldDoesNotExist
from django.db.models.constants import LOOKUP_SEP


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

            field_path = key.split(LOOKUP_SEP)[0]

            try:
                field_obj = model._meta.get_field(field_path)
            except FieldDoesNotExist as e:
                return Response({
                    "error": str(e),
                    "message": f"فیلد ارسالی معتبر نیست : {key}",
                    "detail": f"فیلد ارسالی وجود ندارد : {key}"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Handle relation fields
            if isinstance(field_obj, (ForeignKey, OneToOneField, ManyToManyField)):
                related_model = field_obj.related_model
                related_fields = [
                    f.name for f in related_model._meta.get_fields()
                    if isinstance(f, (CharField, TextField, IntegerField)) and f.name != 'id'
                ]
                sub_query = Q()
                for sub_field in related_fields:
                    sub_query |= Q(
                        **{f"{key}__{sub_field}__{like}": value})
                query_search &= sub_query
            else:
                # Detect appropriate lookup
                if isinstance(field_obj, (CharField, TextField)):
                    query_search &= Q(**{f"{key}__{like}": value})
                else:
                    # For other fields like int, bool, datetime: exact match
                    query_search &= Q(**{key: value})

        founds = model.objects.filter(query_search).distinct()

        if query_params.get('limit'):
            if query_params.get('limit').lower() == 'none':
                return Response(serializer(founds, many=True).data, status=status.HTTP_200_OK)
            paginator.page_size = query_params.get('limit')

        paginated_founds = paginator.paginate_queryset(founds, request=request)
        serialize_found = serializer(paginated_founds, many=True)
        return paginator.get_paginated_response(serialize_found.data)
