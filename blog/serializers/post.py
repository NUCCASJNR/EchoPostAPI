#!/usr/bin/env python3

"""Contains serializers relating to posts"""


from rest_framework import serializers
from blog.models.post import BlogPost
from datetime import datetime


class CreateBlogPostSerialzer(serializers.ModelSerializer):
        title = serializers.CharField(required=True)
        content = serializers.CharField(required=True)
        image = serializers.ImageField(required=False)
        
        class Meta:
            model = BlogPost
            fields = ['title', 'content', 'image']
            read_only_fields = ('id', 'created_at', 'updated_at')


# class BlogPostSerializer(serializers.ModelSerializer):
#     """serializer for viewing blog/blogs"""
#     title = serializers.CharField(required=False)
#     content = serializers.CharField(required=False)
#     image = serializers.ImageField(required=False)
#     created_at = serializers.DateTimeField(required=False)
#     updated_at = serializers.DateTimeField(required=False)
    
#     class Meta:
#         model = BlogPost
#         fields = ['title', 'content', 'image', 'created_at', 'updated_at']
#         read_only_fields = ('id', 'user_id')

class BlogPostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        read_only_fields = ('id', 'user_id', 'created_at')
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        
        # Manually update 'updated_at'
        instance.updated_at = datetime.now()

        instance.save()
        return instance