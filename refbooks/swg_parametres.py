from drf_yasg import openapi

from .serializers import RefbookSerializer, ElementSerializer


REFBOOK_API_DESCRIPTION = '''
GET /api/refbooks/[?date=date]/
date - дата начала действия в формате ГГГГ-ММ-ДД.
Если дата указана, то возвращаются только те справочники, в которых имеются версии с датой начала
действия ранее или равной указанной. 
'''

ELEMENT_API_DESCRIPTION = '''
GET /api/refbooks/<id>/elements/[?version=version]/
version - версия справочника.
Если не указана, то возвращаются элементы текущей версии.
Текущая версия - та, дата начала действия которой позже всех остальных версий данного справочника, 
но не позже текущей даты.
'''

VALID_ELEMENT_API_DESCRIPTION = '''
GET api/refbooks/<id>/check_element/?code=code&value=value[&version=version]/
code - код элемента справочника.
value - значение элемента справочника.
version - версия справочника.
Если не указана, то проверяются элементы в текущей версии.
Текущая версия - та, дата начала действия которой позже всех остальных версий данного справочника, 
но не позже текущей даты.
'''



refbook_list_api_param = {'manual_parameters': [openapi.Parameter(name="date",
                                                                  type=openapi.TYPE_STRING,
                                                                  format=openapi.FORMAT_DATE,
                                                                  in_="query",
                                                                  description="Дата версии",
                                                                  ),
                                                ],
                          'operation_description': REFBOOK_API_DESCRIPTION,
                          'responses': {200: RefbookSerializer},
                          }

element_list_api_param = {'manual_parameters': [openapi.Parameter(name="version",
                                                                  type=openapi.TYPE_STRING,
                                                                  in_="query",
                                                                  description="Номер версии",
                                                                  ),
                                                openapi.Parameter(name="id",
                                                                  required=True,
                                                                  type=openapi.TYPE_INTEGER,
                                                                  in_="path",
                                                                  description="ID справочника",
                                                                  ),
                                                ],
                          'operation_description': ELEMENT_API_DESCRIPTION,
                          'responses': {200: ElementSerializer},
                          }

valid_element_api_param = {'manual_parameters': [openapi.Parameter(name="code",
                                                                   required=True,
                                                                   type=openapi.TYPE_STRING,
                                                                   in_="query",
                                                                   description="Код элемента",
                                                                   ),
                                                 openapi.Parameter(name="value",
                                                                   required=True,
                                                                   type=openapi.TYPE_STRING,
                                                                   in_="query",
                                                                   description="Значение элемента",
                                                                   ),
                                                 openapi.Parameter(name="version",
                                                                   type=openapi.TYPE_STRING,
                                                                   in_="query",
                                                                   description="Номер версии",
                                                                   ),
                                                 openapi.Parameter(name="id",
                                                                   required=True,
                                                                   type=openapi.TYPE_INTEGER,
                                                                   in_="path",
                                                                   description="ID справочника",
                                                                   ),
                                                 ],
                           'operation_description': VALID_ELEMENT_API_DESCRIPTION,
                           'responses': {200: ElementSerializer},
                           }
