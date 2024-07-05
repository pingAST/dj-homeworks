from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        deleted_product_data = ProductSerializer(instance).data
        self.perform_destroy(instance)
        return Response({"message": "Продукт успешно удален", "deleted_product": deleted_product_data},
                        status=status.HTTP_200_OK)


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['positions__product__id']
    search_fields = ['positions__product__title', 'positions__product__description']

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('products', None)
        search_query = self.request.query_params.get('search', None)

        if product_id:
            queryset = queryset.filter(positions__product__id=product_id)

        if search_query:
            queryset = queryset.filter(positions__product__title__icontains=search_query) | queryset.filter(positions__product__description__icontains=search_query)

        return queryset
