from django.urls import path

from univ import views


urlpatterns = [
    path('', views.UnivList.as_view()),
    path('offline/', views.OfflineScheduleList.as_view()),
]
