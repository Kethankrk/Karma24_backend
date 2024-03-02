from django.db import models

# models.py
from django.db import models


class UploadedFile(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to="uploads/")
