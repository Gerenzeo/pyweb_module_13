from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, Textarea
from .models import Tag

class TagForm(ModelForm):
    tagname = CharField(min_length=2, max_length=50, required=True)

    class Meta:
        model = Tag
        fields = ['tagname']