from django.db import models


class Listdata(models.Model):
    task = models.CharField(max_length=50)
    information = models.CharField(max_length=50)
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    priority = models.CharField(max_length=50)
    user = models.CharField(max_length=50)

