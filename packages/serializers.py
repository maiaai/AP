from rest_framework import serializers


class PackagesListSerializer(serializers.Serializer):
    name = serializers.CharField()
    link = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request', None)

    def get_link(self, obj):
        package_name = list(obj.values())[0]
        return f"http://{self.request.META['HTTP_HOST']}{self.request.path}{package_name}"


class PackageDetailsSerializer(serializers.Serializer):
    name = serializers.CharField()
    details = serializers.DictField()
