from django.db import models

# Create your models here.

class Item(models.Model):
    '''Represent a to do item in database '''
    text = models.TextField(default='')
