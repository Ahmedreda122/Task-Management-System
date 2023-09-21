from django.db import models

# Create your models here.
class Task(models.Model):
  ID = models.BigAutoField(auto_created = True, primary_key=True, verbose_name="ID")
  description = models.TextField(max_length=255)
  deadline = models.DateTimeField(null=True, blank=True)
  active = models.BooleanField(default=True)
  priority = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True)