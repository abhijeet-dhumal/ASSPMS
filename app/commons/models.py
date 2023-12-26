from django.db import models
from account.models import User

# Create your models here.


class TimeStampedModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        abstract = True
