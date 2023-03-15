from django.urls import path

from .views import RefbookListAPIView, ElementListAPIView, ValidElementsAPIView


urlpatterns = [
    path('', RefbookListAPIView.as_view()),
    path('<int:id>/elements/', ElementListAPIView.as_view()),
    path('<int:id>/check_element/', ValidElementsAPIView.as_view()),
]
