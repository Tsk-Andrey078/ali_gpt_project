from django.db import models

# Create your models here.
class CompanySell(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField()
    status = models.CharField(default=None, blank=True, null=True)
    date_add = models.DateTimeField(auto_now_add=True)

class threads(models.Model):
    id = models.AutoField(primary_key=True)
    thread_id = models.CharField(max_length=255, unique=True)
    user_id = models.CharField(max_length=255, unique=True)
    last_message_id = models.BigIntegerField()
    