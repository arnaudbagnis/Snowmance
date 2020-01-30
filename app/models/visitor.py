from django.db import models

from app.models.category import Category
from app.models.person import Person


class Visitor(models.Model):
    date = models.CharField(max_length=200, blank=False, null=False)
    visitor = models.ForeignKey(Person, on_delete=models.CASCADE, default=27, related_name='visitors')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, default=27, related_name='persons')

    def __str__(self):
        return str(self.visitor) + " a regardé " + str(self.person)+" le "+str(self.date)
