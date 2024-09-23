from django.db import models

# Create your models here.
class CompanySell(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True)

    