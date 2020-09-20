from django.utils.text import slugify
from rest_framework import serializers


class PackagesListSerializer(serializers.Serializer):
    name = serializers.CharField()
    link = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request', None)

    def get_link(self, obj):
        package_name = list(obj.values())[0]
        slugified_package_name = slugify(package_name)
        return f"http://{self.request.META['HTTP_HOST']}{self.request.path}{slugified_package_name}"


class PackageDetailsSerializer(serializers.Serializer):
    name = serializers.CharField()
    details = serializers.DictField()
