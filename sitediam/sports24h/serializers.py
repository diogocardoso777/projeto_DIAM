from rest_framework import serializers
from .models import Post, Seller, Forum, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:  # (1)
        model = Post
        fields = ('pk', 'owner', 'title', 'forum', 'text', 'likes_count', 'created_at')

#
# class SellerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Seller
#         fields = ('pk', 'questao', 'opcao_texto', 'votos')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'user', 'post', 'text', 'created_at')
