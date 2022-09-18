from uuid import uuid1
from django.db import models
from django.db.models.deletion import CASCADE
from hacker_news_generated_data.models import NewsBaseClass




def createID():
    id = uuid1().int >> 64
    return id

class User(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.TextField(serialize=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name


class UserPosts(NewsBaseClass):
    id = models.BigAutoField(primary_key=True, unique=True, default=createID)
    by = models.ForeignKey(to=User, on_delete=CASCADE)

    def __str__(self) -> str:
        return super().title