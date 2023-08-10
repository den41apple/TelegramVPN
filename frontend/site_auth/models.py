from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserGeneric, AbstractUser
from django.db import models


class User(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        null=False,
        on_delete=models.CASCADE,
    )
    telegram_chat_id = models.BigIntegerField(null=True)
    firezone_id = models.CharField(null=False, max_length=100, default="0000")
