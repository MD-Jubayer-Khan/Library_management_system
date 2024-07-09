from django import forms
from .models import Review

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your amount'
        })
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
