from django.contrib.auth.models import User
from django.db import models

# from app.models.gender import Gender
from app.models.category import Category
from app.models.tag import Tag


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=200,
                                   blank=True,
                                   null=True,
                                   default=None)
    avatar = models.CharField(max_length=1000, default='None')
    tags = models.ManyToManyField(Tag, related_name='Persons')
    hobby = models.ForeignKey(Tag, on_delete=models.CASCADE, default=27, related_name='+')
    personality = models.ForeignKey(Tag, on_delete=models.CASCADE, default=27, related_name='+')
    way_of_life = models.ForeignKey(Tag, on_delete=models.CASCADE, default=27, related_name='+')

    def __str__(self):
        return str(self.user)
