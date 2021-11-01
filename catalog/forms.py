from django import forms
from django.db.models import Count

from catalog.models import Review, Rating, RatingStar

from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ReviewForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    captcha = ReCaptchaField()

    class Meta:
        model = Review
        fields = ('text', 'name', 'email', 'captcha')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control border', 'id': 'contactcomment'}),
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border'}),
        }


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.annotate(__count=Count('*')),
        widget=forms.RadioSelect(),
        empty_label=None,
    )

    class Meta:
        model = Rating
        fields = ('star',)
