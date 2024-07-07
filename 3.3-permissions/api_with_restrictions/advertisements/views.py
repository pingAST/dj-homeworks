from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Advertisement
from .serializers import AdvertisementSerializer, AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AdvertisementFilter
    filter_fields = ['creator', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']

    def validate_open_advertisements_count(self, request):
        user = self.request.user
        open_advertisements_count = Advertisement.objects.filter(creator=user, status='OPEN').count()
        if open_advertisements_count >= 10:
            raise ValidationError("У вас не может быть более 10 открытых рекламных объявлений.")
        return open_advertisements_count

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []

    def create(self, request, *args, **kwargs):
        self.validate_open_advertisements_count(request)
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        advertisement = self.get_object()
        if advertisement.creator != self.request.user:
            raise PermissionDenied("Вам не разрешается редактировать это объявление.")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        advertisement = self.get_object()
        if advertisement.creator != self.request.user:
            raise PermissionDenied("Вы не имеете права удалять эту рекламу.")
        return super().destroy(request, *args, **kwargs)
