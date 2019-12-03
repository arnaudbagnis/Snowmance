from django.db import models

from app.models.category import Category


class Tag(models.Model):
    description = models.CharField(max_length=200,
                                   blank=True,
                                   null=True,
                                   default=None)
    categories = models.ManyToManyField(Category)

    # def __str__(self):
    #     result = self.categories
    #     if self.description is not None:
    #         result += ' ' + self.description[:80]
    #     return result
