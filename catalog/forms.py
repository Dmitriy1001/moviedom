from django import forms

from catalog.models import Review, Rating, RatingStar


class ReviewForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Review
        fields = ('text', 'name', 'email')


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None,
    )

    class Meta:
        model = Rating
        fields = ('star',)