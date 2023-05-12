from django.conf import settings
from django.db import models
from django.db.models import F

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


class Size(models.Model):
    name = models.CharField(max_length=20)


class Forum(models.Model):
    name = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthdate = models.DateField()
    photo = models.ImageField(upload_to="users", default="default-user-icon.png")
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
    photo = models.ImageField(upload_to="users", default="default-user-icon.png")
    country = models.ForeignKey("Country", on_delete=models.CASCADE, null=True)
    nr_published_posts = models.IntegerField(default=0)
    nr_received_likes = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)


class Moderator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthdate = models.DateField()
    photo = models.ImageField(upload_to="users", default="default-user-icon.png")
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
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, default=1)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=True,
                                  blank=True)
    content = models.TextField()
    sent_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.sender.username} -> {self.recipient.username}: {self.content[:30]}'


from django.db.models import F

class Post(models.Model):
    owner = models.ForeignKey("Seller", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    forum = models.ForeignKey("Forum", on_delete=models.CASCADE)
    text = models.TextField()
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        # Check if the post is being created, not updated.
        if self._state.adding:
            super().save(*args, **kwargs)  # Save the post first.

            # Get the owner's User instance.
            owner_user = User.objects.get(id=self.owner.user_id)

            # Get all the followers of the owner's user.
            followers = Follows.objects.filter(followed_user=owner_user)

            # For each follower, create a new message.
            for follower in followers:
                Message.objects.create(
                    sender=owner_user,
                    recipient=follower.following_user,
                    content=f"New post from {owner_user.username}"
                )
        else:
            super().save(*args, **kwargs)  # Save the post without creating messages.


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)


class Product(models.Model):
    owner = models.ForeignKey("Seller", on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    size = models.ForeignKey("Size", on_delete=models.CASCADE, default=1)
    forum = models.ForeignKey("Forum", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="products", default="default-product-image.png")
    created_at = models.DateTimeField(default=datetime.now)
    is_active = models.BooleanField(default=True)


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
