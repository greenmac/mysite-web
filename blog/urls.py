from django.urls import path
from . import views

# start with blog
urlpatterns = [
    # http://localhost:8000/blog/
    path('', views.blogList, name='blog_list'),
    path('<int:blog_pk>', views.blogDetail, name='blog_detail'),
    path('type/<int:blog_type_pk>', views.blogsWithType, name='blogs_with_type'),
    path('date/<int:year>/<int:month>', views.blogWithDate, name='blog_with_date'),
]