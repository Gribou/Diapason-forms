from rest_framework.permissions import BasePermission, IsAuthenticated
from django.contrib.auth.models import Group


class GroupRestricted(IsAuthenticated):
    '''
        Authenticated users can only access forms related to their groups
        'All access' users can access everything.
        This should not be used for Draft views which should be accessible to anonymous users
    '''

    def has_object_permission(self, request, view, obj):
        related_groups = list(
            Group.objects.filter(
                permissions__codename='all_access').values_list(
                    'pk', flat=True))
        if obj.assigned_to_group:
            related_groups.append(obj.assigned_to_group.pk)
        return request.user.is_authenticated and request.user.groups.filter(
            pk__in=related_groups).exists()


class IsOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class FeatureActivated(BasePermission):

    def has_permission(self, request, view):
        return self.is_feature_activated() and super().has_permission(request, view)
