from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from importer_app.models import ProductFile, ProductInfo
from importer_app.serializers import (
    AttachmentSerializer,
    CreateProductSerializer,
    FetchProductsSerializer,
)
from importer_app.tasks import process_file_to_db, webhook_event


class ProductViewSet(viewsets.ViewSet):
    """
    A ViewSet for product CRUD operations, product_importer and bulk_delete operations.
    """

    def list(self, request):
        """
        The products lists with option for filtering and searching
        """
        try:
            paginator = PageNumberPagination()
            paginator.page = request.GET.get("page") or 1
            paginator.page_size = 10
            product_status = request.GET.get("status") or [1, 2]
            search_term = request.GET.get("search") or ""
            products_objects = ProductInfo.objects.filter(
                (Q(status__in=product_status))
                & (
                    Q(name__icontains=search_term)
                    | Q(sku__icontains=search_term)
                    | Q(description__icontains=search_term)
                )
            )
            result_page = paginator.paginate_queryset(products_objects, request)
            products = FetchProductsSerializer(result_page, many=True)
            return Response(
                {
                    "msg": "Products information retrived successfully!",
                    "data": products.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        API to create/update the product
        """
        try:
            product_data = CreateProductSerializer(data=request.data)
            if product_data.is_valid():
                product_data.save()
                webhook_event.delay(product_data.data)
                return Response(
                    {
                        "msg": "Product information operation performed successfully!",
                        "data": product_data.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "msg": "Error while performing operation!",
                        "data": product_data.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieve the product based on sku
        """
        try:
            products = FetchProductsSerializer(ProductInfo.objects.get(sku=pk))
            return Response(
                {
                    "msg": "Products information retrived successfully!",
                    "data": products.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        API to delete a product based on sku
        """
        try:
            ProductInfo.objects.get(sku=pk).delete()
            return Response(
                {"msg": "Product deleted successfully!"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "msg": "The following error occurred while deleting products "
                    + str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"])
    def upload_products(self, request):
        """
        Function to upload the products
        """
        file_form = AttachmentSerializer(data=request.data)
        if file_form.is_valid():
            files = request.FILES
            for file in files.values():
                file_obj = ProductFile.objects.create(file=file)
                process_file_to_db.delay(file_obj.id)
                return Response(file_form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_form._errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"])
    def bulk_delete(self, request):
        """
        API to delete all the products
        """
        try:
            ProductInfo.objects.all().delete()
            return Response(
                {"msg": "All products are deleted successfully!"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "msg": "The following error occurred while deleting products "
                    + str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
