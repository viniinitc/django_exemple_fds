from django.db import models

import datetime
from django.utils import timezone

class question(models.Model):
    title = models.CharField(max_length=200, null = False)
    details = models.TextField(null=False)
    trying = models.TextField()
    cdate = models.DateTimeField("Posted on ")
    user = models.CharField(max_length=200, null=False, default="anonymous")

    def __str__(self):
        return "[" + str(self.id) + "] " + self.title
    
    def detstring(self):
        return "id: " + str(self.id) + "; title: " + self.title + "; details: " + self.details + "; try: " + self.trying + "; posted on: " + str(self.cdate) + "; user: " + self.user

    def recently(self):
        return self.cdate >= timezone.now() - datetime.timedelta(days=1)

class answer(models.Model):
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    votes = models.IntegerField(default=0)
    cdate = models.DateTimeField("Posted on ")
    user = models.CharField(max_length=200, null=False, default="anonymous")

    def __str__(self):
        return "[" + str(self.id) + "] " + self.text
        
    def recently(self):
        return self.cdate >= timezone.now() - datetime.timedelta(days=1)
    
# Create your models here.
