from django.urls import path
from . import views, views_auth

urlpatterns = [
    path('', views.home, name='home'),
    
    # Auth
    path('signup/', views_auth.signup_view, name='signup'),
    path('login/', views_auth.login_view, name='login'),
    path('logout/', views_auth.logout_view, name='logout'),

    path('api/word/<int:word_id>/status/', views.update_word_status, name='update_word_status'),
    # path('alphabet/', views.roadmap, name='roadmap'), # Removed per user request
    path('vocabulary/', views.vocabulary, name='vocabulary'),
    path('revision/', views.revision_list, name='revision_list'),
    path('practice/<str:mode>/', views.practice, name='practice'),
    path('api/practice/<str:mode>/', views.practice_data, name='practice_data'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('api/lesson/<int:lesson_id>/', views.lesson_data, name='lesson_data'),
]
