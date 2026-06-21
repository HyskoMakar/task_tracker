from django.core.exceptions import PermissionDenied

class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.creator != self.request.user:
            raise PermissionDenied("You do not have permission to access this task.")
        return super().dispatch(request, *args, **kwargs)