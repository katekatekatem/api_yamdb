from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReadOnlyPermission


class ListModelCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnlyPermission,)
    search_fields = ('name',)
    lookup_field = 'slug'
