from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from .models import NewsContent
from .serializers import NewsContentSerializer


class IsReporter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reporter == request.user


class NewsContentViewSet(viewsets.ModelViewSet):
    serializer_class = NewsContentSerializer
    permission_classes = (IsReporter,)

    # Ensure a user sees only own News Content objects.
    def get_queryset(self):
        user = self.request.userNewsContentSerializer
        if user.is_authenticated:
            return NewsContent.objects.filter(reporter=user)
        raise PermissionDenied()

    # Set user as owner of a NewsContents object.
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
