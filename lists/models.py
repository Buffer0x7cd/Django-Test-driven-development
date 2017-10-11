from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    '''Represent a to do item in database '''
    text = models.TextField(default='')
    item_list = models.ForeignKey(List, default=None)
