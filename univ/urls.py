from django.urls import path

from univ import views


urlpatterns = [
    path('', views.UnivList.as_view()),
]
