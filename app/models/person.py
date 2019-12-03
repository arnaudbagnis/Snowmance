from django.contrib.auth.models import User
from django.db import models

from app.models.tag import Tag


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=200,
                                   blank=True,
                                   null=True,
                                   default=None)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.user
