from django.conf import settings
from django.core.files import base
from rest_framework import serializers

from .helper import get_file_mime_type
from .models import ProductFile, ProductInfo, ProductWebHook


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, allow_null=False)

    class Meta:
        model = ProductFile
        fields = ["file"]

    def validate(self, attrs):
        super(AttachmentSerializer, self).validate(self)
        if "file" not in attrs:
            raise serializers.ValidationError("No file found")
        try:
            fp_uploaded_file = base.File(attrs["file"])
            fp_uploaded_file.seek(0)
            file_mime = get_file_mime_type(fp_uploaded_file)
            if file_mime in settings.ATTACHMENT_SUPPORTED_FILE_FORMATS.keys():
                if (
                    self.cleaned_data["file"].size
                    > settings.ATTACHMENT_MAX_FILE_UPLOAD_SIZE
                ):
                    raise serializers.ValidationError(
                        "The File size must not exceed {} bytes.".format(
                            settings.ATTACHMENT_MAX_FILE_UPLOAD_SIZE
                        )
                    )
            else:
                raise serializers.ValidationError(
                    "This File type ({}) is not supported.".format(file_mime)
                )
        except AttributeError:
            pass

        return attrs


class FetchFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, allow_null=False)

    class Meta:
        model = ProductFile
        fields = ("id", "file", "created_date")


class FetchProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ("name", "sku", "description", "status", "created_date")


class CreateProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_null=False, max_length=250)
    sku = serializers.CharField(required=True, allow_null=False, max_length=250)
    description = serializers.CharField(required=False, allow_null=True)
    status = serializers.IntegerField(max_value=2, min_value=1)

    class Meta:
        model = ProductInfo
        fields = ("name", "sku", "description", "status")

    def create(self, validated_data):
        product, created = ProductInfo.objects.update_or_create(
            sku=validated_data["sku"].lower(),
            defaults={
                "name": validated_data["name"],
                "description": validated_data["description"],
                "status": validated_data["status"],
            },
        )
        return product


class CreateWebHookSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    url = serializers.URLField(max_length=300)

    class Meta:
        model = ProductWebHook
        fields = ("name", "url")

    def create(self, validated_data):
        webhook, created = ProductWebHook.objects.update_or_create(
            name=validated_data["name"],
            url=validated_data["url"],
        )
        return webhook


class FetchWebHooksSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    url = serializers.URLField(max_length=300)

    class Meta:
        model = ProductWebHook
        fields = ("name", "url", "created_date")
