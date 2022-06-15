from rest_framework import status, viewsets
from rest_framework.response import Response

from importer_app.models import ProductWebHook
from importer_app.serializers import CreateWebHookSerializer, FetchWebHooksSerializer


class WebhooksViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for webhook operations
    """

    def list(self, request):
        """
        API to list webhooks
        """
        try:
            webhooks = FetchWebHooksSerializer(
                ProductWebHook.objects.all().order_by("-created_date"), many=True
            )
            return Response(
                {
                    "msg": "Webhooks retrived successfully!",
                    "data": webhooks.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        API to create/update the webhooks
        """
        try:

            webhook = CreateWebHookSerializer(data=request.data)
            if webhook.is_valid():
                webhook.save()
                return Response(
                    {"msg": "Webhook created successfully!", "data": webhook.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "msg": "Error while performing operation!",
                        "data": webhook.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
