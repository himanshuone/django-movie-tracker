from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model - includes all fields"""
    poster = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'name', 'year', 'imdb_link', 'poster_url', 
            'poster_image', 'poster', 'rating', 'notes', 'tags', 
            'tags_list', 'watch_again', 'date_added'
        ]
        read_only_fields = ['id', 'date_added']
    
    def get_poster(self, obj):
        """Return the best available poster URL"""
        return obj.get_poster()
    
    def get_tags_list(self, obj):
        """Return tags as a list"""
        return obj.get_tags_list()


class MovieListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for movie lists"""
    poster = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'name', 'year', 'poster', 'rating', 
            'watch_again', 'date_added'
        ]
    
    def get_poster(self, obj):
        return obj.get_poster()


class MovieStatsSerializer(serializers.Serializer):
    """Serializer for movie statistics"""
    total_movies = serializers.IntegerField()
    watch_again_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    total_genres = serializers.IntegerField()
    movies_by_year = serializers.DictField()
    top_rated_movies = MovieListSerializer(many=True)
