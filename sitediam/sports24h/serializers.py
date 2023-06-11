from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Seller, Forum, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:  # (1)
        model = Post
        fields = ('pk', 'owner', 'title', 'forum', 'text', 'likes_count', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('pk', 'user')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'user', 'post', 'text', 'created_at')
