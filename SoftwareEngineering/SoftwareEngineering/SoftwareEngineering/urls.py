from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
 
from . import views
 
urlpatterns = [
    path('', views.index, name='home'),
    path('ask.html', views.ask),
    path('answerrecord.html', views.answerrecord),
    path('answertest.html', views.answertest),
    path('post_question/', views.post_question),
    path('answer_test/', views.answer_test),
    
]