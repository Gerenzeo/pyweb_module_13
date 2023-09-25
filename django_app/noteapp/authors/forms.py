from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, Textarea
from .models import Author

class AuthorForm(ModelForm):
    fullname = CharField(min_length=2, max_length=150, required=True, widget=TextInput())
    born_date = DateField(widget=DateInput(attrs={'type': 'date'}))
    born_location = CharField(min_length=2, max_length=150, required=True, widget=TextInput())
    description = CharField(min_length=2, required=True, widget=Textarea())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
