import datetime

from django.test import TestCase

from .serializers import RefbookSerializer, ElementSerializer
from .models import Refbook, Version, Element


class RefbookModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Refbook.objects.create(code='1',
                               name='Специальности медработников',
                               description='Специальности по классификатору')

    def test_code_value(self):
        refbook = Refbook.objects.get(id=1)
        code_value = refbook.code
        self.assertEquals(code_value, '1')

    def test_name_value(self):
        refbook = Refbook.objects.get(id=1)
        name_value = refbook.name
        self.assertEquals(name_value, 'Специальности медработников')

    def test_code_max_length(self):
        refbook = Refbook.objects.get(id=1)
        max_length = refbook._meta.get_field('code').max_length
        self.assertEquals(max_length, 100)

    def test_name_max_length(self):
        refbook = Refbook.objects.get(id=1)
        max_length = refbook._meta.get_field('name').max_length
        self.assertEquals(max_length, 300)

    def test_object_str_name_is_field_name(self):
        refbook = Refbook.objects.get(id=1)
        expected_object_name = '%s %s' % (refbook.name, refbook.code)
        self.assertEquals(expected_object_name, str(refbook))


class VersionModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        refbook1 = Refbook.objects.create(code='1',
                                          name='Специальности медработников',
                                          description='Специальности по классификатору')
        refbook2 = Refbook.objects.create(code='2',
                                          name='Болезни',
                                          description='Список болезней по классификатору')
        Version.objects.bulk_create([Version(refbook=refbook1,
                                             version='0.1',
                                             date='2022-06-15'),
                                     Version(refbook=refbook1,
                                             version='0.2',
                                             date='2023-01-30'),
                                     Version(refbook=refbook2,
                                             version='1.0',
                                             date='2022-09-10')
                                     ])

    def test_version_value(self):
        version1 = Version.objects.get(id=1)
        version2 = Version.objects.get(id=3)
        version1_value = version1.version
        version2_value = version2.version
        self.assertEquals(version1_value,'0.1')
        self.assertEquals(version2_value,'1.0')

    def test_date_value(self):
        version1 = Version.objects.get(id=1)
        version2 = Version.objects.get(id=3)
        date1_value = version1.date
        date2_value = version2.date
        self.assertEquals(date1_value.strftime('%Y-%m-%d'), '2022-06-15')
        self.assertEquals(date2_value.strftime('%Y-%m-%d'), '2022-09-10')

    def test_refbook_id_value(self):
        version1 = Version.objects.get(id=1)
        version2 = Version.objects.get(id=3)
        refbook1_id_value = version1.refbook.id
        refbook2_id_value = version2.refbook.id
        self.assertEquals(refbook1_id_value, 1)
        self.assertEquals(refbook2_id_value, 2)

    def test_version_max_length(self):
        version = Version.objects.get(id=1)
        max_length = version._meta.get_field('version').max_length
        self.assertEquals(max_length, 50)

    def test_object_str_name_is_version(self):
        version = Version.objects.get(id=1)
        expected_object_name = '%s, версия %s' % (version.refbook, version.version)
        self.assertEquals(expected_object_name, str(version))


class ElementModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        refbook = Refbook.objects.create(code='1',
                                         name='Специальности медработников',
                                         description='Специальности по классификатору')
        version1 = Version.objects.create(refbook=refbook,
                                          version='0.1',
                                          date='2022-06-15')
        version2 = Version.objects.create(refbook=refbook,
                                          version='0.2',
                                          date='2023-01-30')
        Element.objects.bulk_create([Element(version=version1,
                                             code='1',
                                             value='Травматолог'),
                                     Element(version=version1,
                                             code='2',
                                             value='Хирург'),
                                     Element(version=version2,
                                             code='1',
                                             value='Травматолог'),
                                     Element(version=version2,
                                             code='2',
                                             value='Хирург')
                                     ])

    def test_code_value(self):
        element1 = Element.objects.get(id=1)
        element2 = Element.objects.get(id=2)
        element3 = Element.objects.get(id=3)
        element4 = Element.objects.get(id=4)
        element1_code = element1.code
        element2_code = element2.code
        element3_code = element3.code
        element4_code = element4.code
        self.assertEquals(element1_code,'1')
        self.assertEquals(element2_code,'2')
        self.assertEquals(element3_code,'1')
        self.assertEquals(element4_code,'2')

    def test_value_value(self):
        element1 = Element.objects.get(id=1)
        element2 = Element.objects.get(id=2)
        element3 = Element.objects.get(id=3)
        element4 = Element.objects.get(id=4)
        element1_value = element1.value
        element2_value = element2.value
        element3_value = element3.value
        element4_value = element4.value
        self.assertEquals(element1_value,'Травматолог')
        self.assertEquals(element2_value,'Хирург')
        self.assertEquals(element3_value,'Травматолог')
        self.assertEquals(element4_value,'Хирург')

    def test_code_max_length(self):
        element = Element.objects.get(id=1)
        max_length = element._meta.get_field('code').max_length
        self.assertEquals(max_length, 100)

    def test_value_max_length(self):
        element = Element.objects.get(id=1)
        max_length = element._meta.get_field('value').max_length
        self.assertEquals(max_length, 300)

    def test_object_str_name_is_value(self):
        element = Element.objects.get(id=1)
        expected_object_name = '%s. %s' % (element.code, element.value)
        self.assertEquals(expected_object_name, str(element))

    def test_equal_element_version_id(self):
        element1 = Element.objects.get(id=1)
        element2 = Element.objects.get(id=2)
        element3 = Element.objects.get(id=3)
        element4 = Element.objects.get(id=4)
        self.assertEquals(element1.version.id, 1)
        self.assertEquals(element2.version.id, 1)
        self.assertEquals(element3.version.id, 2)
        self.assertEquals(element4.version.id, 2)


class RefbookAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        refbook1 = Refbook.objects.create(code='1',
                                          name='Специальности медработников',
                                          description='Специальности по классификатору')
        refbook2 = Refbook.objects.create(code='2',
                                          name='Болезни',
                                          description='Список болезней по классификатору')
        Version.objects.bulk_create([Version(refbook=refbook1,
                                             version='0.1',
                                             date='2022-06-15'),
                                     Version(refbook=refbook1,
                                             version='0.2',
                                             date='2022-11-15'),
                                     Version(refbook=refbook2,
                                             version='1.0',
                                             date='2023-01-10'),
                                     Version(refbook=refbook2,
                                             version='2.0',
                                             date='2023-01-30')
                                     ])

    def test_get_refbooks_without_date(self):
        refbook1 = Refbook.objects.get(id=1)
        refbook2 = Refbook.objects.get(id=2)
        url = 'http://127.0.0.1:8000/api/refbooks/'
        response = self.client.get(url)
        serializer_data = {'refbooks': RefbookSerializer([refbook1, refbook2], many=True).data}
        self.assertEqual(serializer_data, response.data)

    def test_get_refbooks_with_date(self):
        date1 = '2022-12-01'
        queryset1 = Refbook.objects.filter(versions__date__lte=date1).order_by('code').distinct()
        url1 = 'http://127.0.0.1:8000/api/refbooks/?date={}'.format(date1)
        response1 = self.client.get(url1)
        serializer_data1 = {'refbooks': RefbookSerializer(queryset1, many=True).data}
        self.assertEqual(serializer_data1, response1.data)

        date2 = '2023-02-15'
        queryset2 = Refbook.objects.filter(versions__date__lte=date2).order_by('code').distinct()
        url2 = 'http://127.0.0.1:8000/api/refbooks/?date={}'.format(date2)
        response2 = self.client.get(url2)
        serializer_data2 = {'refbooks': RefbookSerializer(queryset2, many=True).data}
        self.assertEqual(serializer_data2, response2.data)

    def test_httpstatus_get_refbooks(self):
        url = 'http://127.0.0.1:8000/api/refbooks/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_httpstatus_get_refbooks_with_date(self):
        date = '2022-12-15'
        url = 'http://127.0.0.1:8000/api/refbooks/?date={}'.format(date)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_httpstatus_get_refbooks_with_uncorrect_date(self):
        date = '213213213'
        url = 'http://127.0.0.1:8000/api/refbooks/?date={}'.format(date)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)


class ElementsAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        refbook = Refbook.objects.create(code='1',
                                         name='Специальности медработников',
                                         description='Специальности по классификатору')
        refbook2 = Refbook.objects.create(code='2',
                                          name='Отделения',
                                          description='')
        version1 = Version.objects.create(refbook=refbook,
                                          version='0.1',
                                          date='2022-06-15')
        version2 = Version.objects.create(refbook=refbook,
                                          version='0.2',
                                          date='2022-11-11')
        version3 = Version.objects.create(refbook=refbook,
                                          version='0.3',
                                          date='2023-01-30')
        Version.objects.create(refbook=refbook2,
                               version='1.0',
                               date='2023-01-30')
        Element.objects.bulk_create([Element(version=version1,
                                             code='1',
                                             value='Травматолог'),
                                     Element(version=version1,
                                             code='2',
                                             value='Хирург'),
                                     Element(version=version2,
                                             code='1',
                                             value='Травматолог'),
                                     Element(version=version2,
                                             code='2',
                                             value='Хирург'),
                                     Element(version=version3,
                                             code='1',
                                             value='Хирург')
                                     ])

    def test_get_elements_with_version(self):
        refbook_id = 1
        version = '0.1'
        version_id = 1
        url = 'http://127.0.0.1:8000/api/refbooks/{}/elements/?version={}'.format(refbook_id, version)
        response = self.client.get(url)
        queryset = Element.objects.filter(version=version_id)
        serializer_data = {'elements': ElementSerializer(queryset, many=True).data}
        self.assertEqual(serializer_data, response.data)

    def test_get_elements_without_version(self):
        refbook_id = 1
        url = 'http://127.0.0.1:8000/api/refbooks/{}/elements/'.format(refbook_id)
        response = self.client.get(url)
        date_today = datetime.datetime.now()
        version = Version.objects.filter(refbook=refbook_id,
                                         date__lte=date_today).order_by('date').last()
        queryset = Element.objects.filter(version=version.id)
        serializer_data = {'elements': ElementSerializer(queryset, many=True).data}
        self.assertEqual(serializer_data, response.data)

    def test_get_null_array_of_elements_without_version(self):
        refbook_id = 2
        date_today = datetime.datetime.now()
        version = Version.objects.filter(refbook=refbook_id,
                                         date__lte=date_today).order_by('date').last()
        queryset = Element.objects.filter(version=version.id)
        serializer_data = {'elements': ElementSerializer(queryset, many=True).data}
        self.assertEqual(serializer_data, {'elements': []})

    def test_get_valid_element_with_version(self):
        code = '1'.replace('"', '')
        value = 'Хирург'.replace('"', '')
        refbook_id = 1
        version = '0.3'
        version_id = 3

        url = 'http://127.0.0.1:8000/api/refbooks/{}/check_element/?code={}&value={}&version={}'. \
            format(refbook_id, code, value, version)
        response = self.client.get(url)

        queryset = Element.objects.get(code=code,
                                       value=value,
                                       version=version_id)

        serializer_data = {'element': ElementSerializer(queryset).data}
        self.assertEqual(serializer_data, response.data)

    def test_get_valid_element_without_version(self):
        code = '1'.replace('"', '')
        value = 'Хирург'.replace('"', '')
        refbook_id = 1

        url = 'http://127.0.0.1:8000/api/refbooks/{}/check_element/?code={}&value={}'. \
            format(refbook_id, code, value)
        response = self.client.get(url)

        date_today = datetime.datetime.now()
        version = Version.objects.filter(refbook=refbook_id,
                                         date__lte=date_today).order_by('date').last()

        queryset = Element.objects.get(code=code,
                                       value=value,
                                       version=version.id)

        serializer_data = {'element': ElementSerializer(queryset).data}
        self.assertEqual(serializer_data, response.data)

    def test_httpstatus_get_elements_without_version(self):
        refbook_id = 1
        url = 'http://127.0.0.1:8000/api/refbooks/{}/elements/'.format(refbook_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_httpstatus_get_elements_with_version(self):
        refbook_id = 1
        version = '0.1'
        url = 'http://127.0.0.1:8000/api/refbooks/{}/elements/?version={}'.format(refbook_id, version)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_httpstatus_get_elements_with_uncorrect_refbookid(self):
        refbook_id = 9
        url = 'http://127.0.0.1:8000/api/refbooks/{}/elements/'.format(refbook_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_httpstatus_get_elements_with_uncorrect_version(self):
        refbook_id = 1
        version = '11.5'
        url = 'http://127.0.0.1:8000/api/refbooks/{}/elements/?version={}'.format(refbook_id, version)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_httpstatus_get_element_with_correct_code_and_value(self):
        code = '1'.replace('"', '')
        value = 'Хирург'.replace('"', '')
        refbook_id = 1
        version = '0.3'
        url = 'http://127.0.0.1:8000/api/refbooks/{}/check_element/?code={}&value={}&version={}'. \
            format(refbook_id, code, value, version)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_httpstatus_get_element_with_uncorrect_code_and_value(self):
        code = '9'.replace('"', '')
        value = 'Невролог'.replace('"', '')
        refbook_id = 1
        version = '0.3'
        url = 'http://127.0.0.1:8000/api/refbooks/{}/check_element/?code={}&value={}&version={}'. \
            format(refbook_id, code, value, version)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
