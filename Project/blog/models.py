from django import db
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default="default.jpg", upload_to="profile_images")

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title = models.CharField(max_length=150)
    description = models.TextField("Description", max_length=1000)
    image = models.ImageField(upload_to="images", blank=True, default=None)
    is_published = models.BooleanField(default=False)
    on_published = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name="liked", blank=True, default=None)

    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all().count()


LIKE_CHOICES = (
    ("Like", "Like"),
    ("Unlike", "Unlike"),
)


class Like(models.Model):
    user = models.ForeignKey(User, db_column="user", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default="Like", max_length=10)

    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(max_length=150)
    date_added = models.DateTimeField(auto_now_add=True)
