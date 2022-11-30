from rest_framework import mixins
from rest_framework.status import HTTP_403_FORBIDDEN


class RootViewMixin(mixins.ListModelMixin):

    def check_permissions(self, request):
        if self.action == 'list':
            self.permission_denied(
                request,
                message="List endpoint is forbidden",
                code=HTTP_403_FORBIDDEN
            )
        return super().get_permissions()
        # ListModelMixin is added only to allow this view to appear in Api Root view
