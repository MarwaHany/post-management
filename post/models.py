from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    Body = models.TextField(null=True, blank=True)
    Author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Body

class Post(models.Model):
    Title = models.CharField(max_length=255)
    Author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Body = models.TextField(null=True, blank=True)
    Comments = models.ManyToManyField(Comment)

   # display an instance of the model when necessary
    def __str__(self):
        return self.Title
