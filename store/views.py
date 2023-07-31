from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    # def get(self, request):
    #     queryset = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)
    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'product cannot be deleted'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    # def get(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    #
    # def put(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = ProductSerializer(product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')
    ).all()
    serializer_class = CollectionSerializer

class CollectionDetail(RetrieveUpdateDestroyAPIView):

    queryset = Collection.objects.annotate(
        products_count=Count('products')
    ).all()

    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = Collection.objects.annotate(
            products_count=Count('products')
        ).get(pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it has more than one product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get(self, request, pk):
    #     collection = Collection.objects.annotate(
    #         products_count=Count('products')
    #     ).get(pk=pk)
    #
    #     serializer = CollectionSerializer(collection)
    #     return Response(serializer.data)
    #
    # def put(self, request, pk):
    #     collection = Collection.objects.annotate(
    #         products_count=Count('products')
    #     ).get(pk=pk)
    #     serializer = CollectionSerializer(collection, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def delete(self, request, pk):
    #     collection = Collection.objects.annotate(
    #         products_count=Count('products')
    #     ).get(pk=pk)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def get(self, request):
    #     query_set = Collection.objects.annotate(
    #         products_count=Count('products')
    #     ).all()
    #     serializer = CollectionSerializer(query_set, many=True)
    #     return Response(serializer.data)

    # This function des not allowed
    # def post(self, request):
    #     serializer = CollectionSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'POST'])
# def products_list(request):
#     if request.method == 'GET':
#         query_set = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(query_set, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def collections_list(request):
#     if request.method == 'GET':
#         query_set = Collection.objects.annotate(
#             products_count=Count('products')
#         ).all()
#         serializer = CollectionSerializer(query_set, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     if request.method == 'GET':
#         collection = Collection.objects.annotate(
#             products_count=Count('products')
#         ).get(pk=pk)
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)







