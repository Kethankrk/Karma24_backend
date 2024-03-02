from django.db import models


from core.models import Workspace


class UploadedFile(models.Model):
    name = models.CharField(max_length=50)
    workspace = models.ForeignKey(
        Workspace, on_delete=models.SET_NULL, related_name="files", null=True
    )
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return self.name
