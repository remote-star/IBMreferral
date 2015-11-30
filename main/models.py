from django.db import models

# Create your models here.
class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.URLField()
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    bonus = models.BooleanField()
    
    def __str__(self):
        return self.name