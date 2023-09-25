from django.db import models

# Create your models here.
class Tag(models.Model):
    tagname = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return str(self.tagname)