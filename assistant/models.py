from django.db import models

# Create your models here.
class PDFContent(models.Model):
    thread_id = models.CharField(max_length=255, unique=True)
    content = models.TextField()