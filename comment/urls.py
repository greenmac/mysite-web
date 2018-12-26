from django.urls import path
from . import views

urlpatterns = [
    path('update_comment', views.updateComment, name='update_comment')
]