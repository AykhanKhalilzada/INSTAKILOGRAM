from django import forms
from .helpers.helpers import MAX_USERNAME_LENGTH, MAX_TEXT_LENGTH

class SearchPageForm(forms.Form):
    search_query = forms.CharField(help_text='Enter a username', max_length=MAX_USERNAME_LENGTH, min_length=1)

class NewPostForm(forms.Form):
    post = forms.ImageField()
    caption = forms.CharField(max_length=MAX_TEXT_LENGTH, required=False)
    location_url = forms.URLField(label='Location URL', required=False)