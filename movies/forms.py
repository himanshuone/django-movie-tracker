from django import forms
from .models import Movie


class MovieForm(forms.ModelForm):
    """Form for adding/editing movies"""
    
    class Meta:
        model = Movie
        fields = ['name', 'year', 'imdb_link', 'poster_url', 'poster_image', 'rating', 'notes', 'tags', 'watch_again']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter movie name'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2023',
                'min': '1888',  # First movie ever made
                'max': '2030'
            }),
            'imdb_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.imdb.com/title/tt...'
            }),
            'poster_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://... (optional)'
            }),
            'poster_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1.0 - 10.0',
                'step': '0.1',
                'min': '0',
                'max': '10'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Your thoughts about this movie...'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Action, Drama, Sci-Fi (comma separated)'
            }),
            'watch_again': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
    
    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year and (year < 1888 or year > 2030):
            raise forms.ValidationError("Please enter a valid year.")
        return year
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 0 or rating > 10):
            raise forms.ValidationError("Rating must be between 0 and 10.")
        return rating


class CSVUploadForm(forms.Form):
    """Form for uploading CSV files"""
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: Name, Year, IMDb, Poster, Rating, Notes',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )
    
    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')
        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError("Please upload a CSV file.")
            if file.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("File size must be under 5MB.")
        return file
