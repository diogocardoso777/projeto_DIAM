from django.conf import settings
from django.db import models

# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=50)


class Team(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)


class Sport(models.Model):
    name = models.CharField(max_length=50)


class Forum(models.Model):
    name = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthdate = models.DateField()
    country = models.ForeignKey("Country", on_delete=models.CASCADE, null=True)
    favorite_team = models.ForeignKey("Team", on_delete=models.CASCADE, null=True)
    favorite_sport = models.ForeignKey("Sport", on_delete=models.CASCADE, null=True)
    nr_commented_posts = models.IntegerField(default=0)
    nr_liked_posts = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    points = models.IntegerField(default=0)


class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthdate = models.DateField()
    country = models.ForeignKey("Country", on_delete=models.CASCADE, null=True)
    nr_published_posts = models.IntegerField(default=0)
    nr_received_likes = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)


class Moderator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthdate = models.DateField()
    country = models.ForeignKey("Country", on_delete=models.CASCADE, null=True)


class Follows(models.Model):
    following_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follows')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed')
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['following_user', 'followed_user'], name='my_model_pk1')
        ]


class FollowsForum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forum = models.ForeignKey("Forum", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'forum'], name='my_model_pk2')
        ]


class Likes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='my_model_pk3')
        ]


class Message(models.Model):
    sent_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent')
    received_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received')
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)


class Post(models.Model):
    owner = models.ForeignKey("Seller", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)
    forum = models.ForeignKey("Forum", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    is_active = models.BooleanField(default=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    size = models.CharField(max_length=10)
    photo = models.CharField(max_length=100, default="PREENCHER")
    created_at = models.DateTimeField(default=datetime.now)


class ShoppingCart(models.Model):
    client = models.OneToOneField("Client", on_delete=models.CASCADE, primary_key=True)
    product_list = models.ManyToManyField("Product")


class Review(models.Model):
    summary = models.CharField(max_length=50)
    text = models.TextField()
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=datetime.now)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:50]}"