from django.contrib.auth.models import User
from django.db import models


class ExternGoogleUser(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, primary_key=True)
    extern_id = models.CharField(null=False, unique=True, max_length=30)
