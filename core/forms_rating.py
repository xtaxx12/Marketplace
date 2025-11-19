from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.RadioSelect(choices=Rating.RATING_CHOICES),
            'review': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escribe tu opinión sobre este producto (opcional)...',
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-200'
            })
        }
        labels = {
            'rating': 'Calificación',
            'review': 'Reseña'
        }
