import datetime
import time

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import Refbook, Version, Element
from .serializers import RefbookSerializer, ElementSerializer
from .swg_parametres import refbook_list_api_param, element_list_api_param, valid_element_api_param


class RefbookListAPIView(ListAPIView):
    @swagger_auto_schema(**refbook_list_api_param)
    def get(self, request, *args, **kwargs):
        queryset = Refbook.objects.order_by('code')

        date = self.request.query_params.get('date', None)
        if date:
            try:
                time.strptime(date, '%Y-%m-%d')
            except ValueError:
                content = {'detail': 'Некорректный формат даты: {}. '
                                     'Значение должно быть в формате YYYY-MM-DD'.format(date)}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                queryset = queryset.filter(versions__date__lte=date).distinct()

        serializer = RefbookSerializer(queryset, many=True)
        return Response({'refbooks': serializer.data})


class ElementListAPIView(ListAPIView):
    @swagger_auto_schema(**element_list_api_param)
    def get(self, request, *args, **kwargs):
        refbook_id_param = self.kwargs.get('id')
        version_param = self.request.query_params.get('version', None)

        try:
            self.get_refbook(refbook_id_param)
        except:
            content = {'detail': 'Справочник с идентификатором {} не найден'.format(refbook_id_param)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            version = self.get_version(refbook_id_param, version_param)
            if version is None:
                content = {'detail': 'У справочника отсутствует версия на текущую дату'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        except:
            content = {'detail': 'Версия {} отсутствует в справочнике {}'.format(version_param, refbook_id_param)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        queryset = Element.objects.filter(version=version).order_by('code')
        serializer = ElementSerializer(queryset, many=True)
        return Response({'elements': serializer.data})

    def get_refbook(self, refbook_id):
        return Refbook.objects.get(id=refbook_id)

    def get_version(self, refbook_id, version):
        if version:
            return Version.objects.get(refbook=refbook_id, version=version)
        else:
            date_today = datetime.datetime.now()
            return Version.objects.filter(refbook=refbook_id,
                                          date__lte=date_today).order_by('date').last()


class ValidElementsAPIView(ListAPIView):
    @swagger_auto_schema(**valid_element_api_param)
    def get(self, request, *args, **kwargs):
        refbook_id_param = self.kwargs.get('id')
        code_param = self.request.query_params.get('code', None)
        value_param = self.request.query_params.get('value', None)
        version_param = self.request.query_params.get('version', None)

        try:
            self.get_refbook(refbook_id_param)
        except:
            content = {'detail': 'Справочник с идентификатором {} не найден'.format(refbook_id_param)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            version = self.get_version(refbook_id_param, version_param)
            if version is None:
                content = {'detail': 'У справочника отсутствует версия на текущую дату'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        except:
            content = {'detail': 'Версия {} отсутствует в справочнике {}'.format(version_param, refbook_id_param)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            queryset = Element.objects.get(code=code_param, value=value_param, version=version)
        except:
            content = {'detail': 'Элемент с указанными параметрами code={} '
                                 'и value={} не найден'.format(code_param, value_param)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        serializer = ElementSerializer(queryset)
        return Response({'element': serializer.data})

    def get_refbook(self, refbook_id):
        return Refbook.objects.get(id=refbook_id)

    def get_version(self, refbook_id, version):
        if version:
            return Version.objects.get(refbook=refbook_id, version=version)
        else:
            date_today = datetime.datetime.now()
            return Version.objects.filter(refbook=refbook_id,
                                          date__lte=date_today).order_by('date').last()
