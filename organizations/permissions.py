from typing import Any

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from .models import Organization


class IsOrganizationOwner(BasePermission):
    """
    Check if given user is owner of given organization.
    Assume user and organization both exist.
    """

    def __init__(self, organization: Organization, user: get_user_model()) -> None:
        self.user = user
        self.organization = organization
        super().__init__()

    def has_permission(self, request: Request, view):
        return self.organization.owner.id == self.user.id

    def has_object_permission(self, request: Request, view, obj: Organization | Any):
        return (
            self.has_permission(request=request, view=view)
            if type(obj) is not Organization
            else obj.owner.id == self.user.id
        )
