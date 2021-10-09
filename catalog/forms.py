from django import forms

from catalog.models import Review


class ReviewForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Review
        fields = ('text', 'name', 'email')