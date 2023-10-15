"""
This module includs some utility functions used for various purposes in other apps, modules, classes or functions.
"""

from rest_framework.serializers import ModelSerializer
from typing import Any
from django.http import QueryDict


def remove_blank_or_null(data: QueryDict | dict) -> QueryDict | dict:
    """
    This functions removes the blank ("") or null (None) type values from the given QueryDict of data.

    ARGS: data: QuerydDict | dict
    RETURNS: cleaned_data: QueryDict
    """

    print(type(data))
    print(data)
    cleaned_data = {
        key: value
        for key, value in data.items()
        if "." in key or (value != "" and value is not None)
    }
    cleaned_data_ = QueryDict("", mutable=True)
    cleaned_data_.update(cleaned_data)
    return cleaned_data_


def get_nested_object_deserialized(
    data: dict, serializer_class: ModelSerializer
) -> Any:
    serializer: ModelSerializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    deserialized_instance = serializer.save()
    return deserialized_instance
