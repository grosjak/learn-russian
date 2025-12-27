from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('alphabet/', views.roadmap, name='roadmap'), # Removed per user request
    path('vocabulary/', views.vocabulary, name='vocabulary'),
    path('practice/<str:mode>/', views.practice, name='practice'),
    path('api/practice/<str:mode>/', views.practice_data, name='practice_data'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('api/lesson/<int:lesson_id>/', views.lesson_data, name='lesson_data'),
]
