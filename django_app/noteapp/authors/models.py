from django.db import models

# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=150, null=False)
    born_date = models.CharField(max_length=150, null=False)
    born_location = models.CharField(max_length=150, null=False)
    description = models.CharField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fullname', 'born_date', 'born_location', 'description'], name='authors')
        ]

    def __str__(self):
        return str(self.fullname)