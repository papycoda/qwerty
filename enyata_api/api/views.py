from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import Prefetch
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.pagination import PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer

    def list(self, request):
        # Try to get the paginated result from cache
        page = self.paginate_queryset(self.get_queryset().select_related("category"))

        if page is not None:
            # If pagination is applied, cache the paginated result
            key = f'products_page_{request.query_params.get("page", 1)}'
            cached_page = cache.get(key)

            if cached_page is None:
                serializer = self.get_serializer(page, many=True)
                cached_page = serializer.data
                cache.set(key, cached_page, 3600)
            return self.get_paginated_response(cached_page)

        # If pagination is not applied, fall back to the original non-paginated approach
        cached_products = cache.get("all_products")
        if cached_products is None:
            queryset = self.get_queryset().select_related("category")
            serializer = self.get_serializer(queryset, many=True)
            cached_products = serializer.data
            cache.set("all_products", cached_products, 3600)

        return Response(cached_products)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self._invalidate_cache()
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self._invalidate_cache()
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        self._invalidate_cache()
        return response

    def _invalidate_cache(self):
        cache.delete("all_products")
