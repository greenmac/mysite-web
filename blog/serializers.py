from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        # fields = ('id', 'title', 'blog_type', 'content', 'author', 'read_details', 'created_time')