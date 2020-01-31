from django.db import models

from app.models.person import Person


class Messages(models.Model):
    date = models.CharField(max_length=200, blank=False, null=False)
    message = models.CharField(max_length=1000, default='None')
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, default=27, related_name='sender')
    receiver = models.ForeignKey(Person, on_delete=models.CASCADE, default=27, related_name='receiver')

    def __str__(self):
        return str(self.message)+" envoyé par "+str(self.sender)+" à "+str(self.receiver)
