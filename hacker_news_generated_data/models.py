import json
from django.db import models

# Create your models here.
class News(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length = 40, null=True)
    by = models.CharField(max_length=200, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    dead = models.BooleanField(blank=True, default=False, null=True)
    parent = models.IntegerField(unique=True, blank=True, null=True)
    poll = models.IntegerField(unique=True, blank=True, null=True)
    url = models.URLField(blank=True, unique=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    descendants = models.IntegerField(blank=True, null=True)

    kids = models.TextField(blank=True, null=True)
    def set_kids(self, i):
        self.kids = json.dumps(i)

    def get_kids(self, i):
        return json.loads(self.kids)

    parts = models.TextField(blank=True, null=True)
    def set_parts(self, i):
        self.parts = json.dumps(i)

    def get_parts(self, i):
        return json.loads(self.parts)

    def __str__(self) -> str:
        return self.title

class relations(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    parent = models.ForeignKey(to=News, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length = 40, blank=True, null=True)
    by = models.CharField(max_length=200, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, unique=True, null=True)
    descendants = models.IntegerField(blank=True, null=True)

    kids = models.TextField(blank=True, null=True)
    def set_kids(self, i):
        self.kids = json.dumps(i)

    def get_kids(self, i):
        return json.loads(self.kids)

    parts = models.TextField(blank=True, null=True)
    def set_parts(self, i):
        self.parts = json.dumps(i)

    def get_parts(self, i):
        return json.loads(self.parts)
    
    def __str__(self) -> str:
        return self.title
    