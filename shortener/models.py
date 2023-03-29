from django.db import models

# Create your models here.
class URL(models.Model):
    uid = models.IntegerField(primary_key=True)
    longURL = models.CharField(max_length=2048, unique=True)
    shortURL = models.CharField(max_length=50, unique=True)