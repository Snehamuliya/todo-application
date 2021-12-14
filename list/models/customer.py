from django.db import models


class Insertdata(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    mobile = models.IntegerField()
    username = models.CharField(max_length=50)
    password = models.CharField