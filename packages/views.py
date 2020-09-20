import os
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PackagesListSerializer
from deb_parse.parser import Parser


def parse_packages():
    local_file_path = '/var/lib/dpkg/sta1tus'
    remote_file_path = 'https://gist.githubusercontent.com/beetlerom/1c2d8519fd8957a123a829a1597e97de/raw/bf6905370d4e1a84576c8d1ca171ee7ddd33fb71/status'
    if os.path.exists(local_file_path):
        with open(local_file_path, "r") as f:
            pkgs = f.read()
            packages = Parser(pkgs)
    else:
        r = requests.get(remote_file_path)
        packages = Parser(r.text)
    return packages


class PackageList(APIView):
    def get(self, request):
        parsed_packages = parse_packages()
        packages = parsed_packages.clean_pkg_info
        context = {'request': request}
        serializer = PackagesListSerializer(data=packages, many=True, context=context)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageDetails(APIView):
    def get(self, request, slug):
        parsed_packages = parse_packages()
        packages = parsed_packages.clean_pkg_info
        package = ((next(item for item in packages if item['name'] == slug)), None)
        return Response(package)
