from django.urls import path
from . import views, views_auth

urlpatterns = [
    path('', views.home, name='home'),
    path('select-language/', views.select_language, name='select_language'),
    
    # Auth
    path('signup/', views_auth.signup_view, name='signup'),
    path('login/', views_auth.login_view, name='login'),
    path('logout/', views_auth.logout_view, name='logout'),

    path('api/validate/', views.validate_answer, name='validate_answer'),
    path('api/word/<int:word_id>/status/', views.update_word_status, name='update_word_status'),
    path('alphabet/', views.roadmap, name='roadmap'), 
    path('stories/', views.stories_list, name='stories_list'),
    path('stories/<slug:slug>/', views.story_detail, name='story_detail'),
    path('api/lookup/', views.lookup_word, name='lookup_word'),
    path('revision/', views.revision_list, name='revision_list'),
    path('practice/<str:mode>/', views.practice, name='practice'),
    path('api/practice/<str:mode>/', views.practice_data, name='practice_data'),
    
    # Grammar
    path('grammar/gender/', views.grammar_practice, name='grammar_practice'),
    path('api/grammar/gender_data/', views.get_grammar_gender_data, name='get_grammar_gender_data'),

    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('api/lesson/<int:lesson_id>/', views.lesson_data, name='lesson_data'),
]
