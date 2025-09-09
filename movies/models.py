from django.db import models
from django.urls import reverse


class Movie(models.Model):
    name = models.CharField(max_length=255, verbose_name='Movie Name')
    year = models.PositiveIntegerField(verbose_name='Release Year')
    imdb_link = models.URLField(max_length=500, verbose_name='IMDb Link')
    poster_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='Poster URL')
    poster_image = models.ImageField(upload_to='posters/', blank=True, null=True, verbose_name='Poster Image')
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name='My Rating')
    notes = models.TextField(blank=True, null=True, verbose_name='Notes')
    tags = models.CharField(max_length=500, blank=True, null=True, verbose_name='Tags/Genres', 
                           help_text='Comma-separated tags or genres')
    watch_again = models.BooleanField(default=False, verbose_name='Would Watch Again', 
                                     help_text='Tick if this movie is worth watching again')
    date_added = models.DateTimeField(auto_now_add=True)
    tmdb_id = models.IntegerField(null=True, blank=True, help_text="The Movie Database ID")
    
    class Meta:
        ordering = ['-date_added']
        unique_together = ['name', 'year']  # Prevent duplicate movies
    
    def __str__(self):
        return f"{self.name} ({self.year})"
    
    def get_poster(self):
        """Return poster URL (uploaded image or manual URL)"""
        # First priority: uploaded image
        if self.poster_image:
            return self.poster_image.url
        
        # Second priority: manual poster URL
        if self.poster_url:
            return self.poster_url
        
        # Don't fetch from TMDB during template rendering
        # This should be done during movie creation/import
        return None
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
