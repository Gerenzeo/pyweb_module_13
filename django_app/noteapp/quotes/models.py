from django.db import models

from authors.models import Author
from tags.models import Tag

class Quote(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.CharField(max_length=300)

    def __str__(self):
        return f"Author:{self.author} / {self.quote[:15]}"