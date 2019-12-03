from django.db import models


class Category(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True, default=None)

    def __str__(self):
        if self.description is not None:
            return self.description[:80]

