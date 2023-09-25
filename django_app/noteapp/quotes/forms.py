from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, Textarea, Select, ModelChoiceField, CharField
from .models import Quote
from tags.models import Tag
from authors.models import Author


class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['tags', 'author', 'quote']


    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    author = ModelChoiceField(
        queryset=Author.objects.all(),
        widget=Select,
        required=True,
    )
    quote = CharField(
        widget=Textarea,
    )