# -*- coding: utf-8 -*-

from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Scripts(models.Model):
    title = models.CharField('Title',max_length=200)
    contents = models.TextField()
    pub_date = models.DateTimeField('PubDate',default=timezone.now())
    user=models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title
        
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <  now

    was_published_recently.admin_order_field = 'PubDate'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Recently PubDate?'


class Tag(models.Model):
    tag_title = models.CharField('Tag',max_length=100)
    scripts = models.ManyToManyField(Scripts)
    
    def __unicode__(self):
        return self.tag_title