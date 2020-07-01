from django.urls import path
from univ import views


urlpatterns = [
    path('', views.ScheduleList.as_view()),
    path('review/', views.ReviewList.as_view()),
]

