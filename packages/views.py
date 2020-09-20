import os
import requests
from django.urls import reverse
from django.utils.text import slugify
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
        package = (next(item for item in packages if slugify(item['name']) == slug))
        depends_on_list = package.get('details', None).get('depends', None)
        if depends_on_list:
            dependency_url_list = self.extract_and_create_urls(depends_on_list)
            self.update_depends_on_list(package, 'depends', dependency_url_list)
        reverse_depends_on_list = package.get('details', None).get('reverse_depends', None)
        if reverse_depends_on_list:
            dependency_url_list = self.extract_and_create_urls(reverse_depends_on_list)
            self.update_depends_on_list(package, 'reverse_depends', dependency_url_list)
        return Response(package)

    def extract_and_create_urls(self, dependencies_list):
        result = []
        for dependency in dependencies_list:
            package_name = dependency.split(' (')[0]
            slug_url = reverse('details', kwargs={'slug': slugify(package_name)})
            package_url = f"http://{self.request.META['HTTP_HOST']}{slug_url}"
            result.append(package_url)
        return result

    def update_depends_on_list(self, package, which_dependency, dependencies_list):
        package['details'][which_dependency] = dependencies_list
