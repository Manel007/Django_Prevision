from django import forms
from .models import CropYield
from .models import Review
from django import forms
from .models import CropYield, Review

class YieldForm(forms.ModelForm):
    class Meta:
        model = CropYield
        fields = ['area', 'item', 'year', 'hg_per_ha_yield', 'average_rain_fall', 'pesticides_tonnes', 'avg_temp']
    
    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year < 2000 or year > 2100:
            raise forms.ValidationError('Year must be between 2000 and 2100.')
        return year

    def clean_hg_per_ha_yield(self):
        hg_per_ha_yield = self.cleaned_data.get('hg_per_ha_yield')
        if hg_per_ha_yield < 0:
            raise forms.ValidationError('Yield cannot be negative.')
        return hg_per_ha_yield

    def clean_average_rain_fall(self):
        average_rain_fall = self.cleaned_data.get('average_rain_fall')
        if average_rain_fall < 0:
            raise forms.ValidationError('Average rainfall cannot be negative.')
        return average_rain_fall

    def clean_pesticides_tonnes(self):
        pesticides_tonnes = self.cleaned_data.get('pesticides_tonnes')
        if pesticides_tonnes < 0:
            raise forms.ValidationError('Pesticides cannot be negative.')
        return pesticides_tonnes

    def clean_avg_temp(self):
        avg_temp = self.cleaned_data.get('avg_temp')
        if avg_temp < 0:
            raise forms.ValidationError('Temperature cannot be negative.')
        return avg_temp
class YieldPredictionForm(forms.Form):
    year = forms.IntegerField(label='Année', min_value=2000, max_value=2100)
    average_rain_fall = forms.FloatField(label='Précipitations moyennes (mm/an)')
    pesticides = forms.FloatField(label='Pesticides (tonnes)')
    avg_temp = forms.FloatField(label='Température moyenne (°C)')
from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'title', 'status']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
            'rating': forms.Select(choices=[
                (1, '1 Star'),
                (2, '2 Stars'),
                (3, '3 Stars'),
                (4, '4 Stars'),
                (5, '5 Stars')
            ]),
            'status': forms.Select(choices=[
                ('active', 'Active'),
                ('archived', 'Archived')
            ]),
        }
        labels = {
            'title': 'Review Title',
            'rating': 'Rating',
            'comment': 'Your Comment',
            'status': 'Status',
        }
        help_texts = {
            'title': 'Provide a short title for your review.',
            'rating': 'Rate this product from 1 to 5 stars.',
            'comment': 'Please provide your feedback.',
            'status': 'Select the status of your review.',
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating not in [1, 2, 3, 4, 5]:
            raise forms.ValidationError('Invalid rating. Please choose a value between 1 and 5.')
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if comment and len(comment) < 10:
            raise forms.ValidationError('Your comment must be at least 10 characters long.')
        return comment

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',  
                'placeholder': field.label,  
            })
            field.required = True  
            field.widget.attrs['required'] = 'required' 
        model = Review
        fields = ['rating', 'comment', 'title', 'status']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
            'rating': forms.Select(choices=[
                (1, '1 Star'),
                (2, '2 Stars'),
                (3, '3 Stars'),
                (4, '4 Stars'),
                (5, '5 Stars')
            ]),
            'status': forms.Select(choices=[
                ('active', 'Active'),
                ('archived', 'Archived')
            ]),
        }
        labels = {
            'title': 'Review Title',
            'rating': 'Rating',
            'comment': 'Your Comment',
            'status': 'Status',
        }
        help_texts = {
            'title': 'Provide a short title for your review.',
            'rating': 'Rate this product from 1 to 5 stars.',
            'comment': 'Please provide your feedback.',
            'status': 'Select the status of your review.',
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating not in [1, 2, 3, 4, 5]:
            raise forms.ValidationError('Invalid rating. Please choose a value between 1 and 5.')
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if comment and len(comment) < 10:
            raise forms.ValidationError('Your comment must be at least 10 characters long.')
    
        return comment

    class Meta:
        model = Review
        fields = ['rating', 'comment','title',  'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',  
                'placeholder': field.label,  
              
            })
            field.required = True 
            field.widget.attrs.setdefault('required', 'required')
