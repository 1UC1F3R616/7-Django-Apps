from django.db import models
from django.core.validators import MaxLengthValidator
from django.urls import reverse

class Paste(models.Model):
    text = models.TextField(validators=[MaxLengthValidator(2000)])
    name = models.CharField(max_length=40, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or str(self.id)
    
    def get_absolute_url(self):
        return reverse('pastebin_paste_detail', args=[self.id])