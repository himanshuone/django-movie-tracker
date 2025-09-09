from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Movie
from .serializers import MovieSerializer, MovieListSerializer, MovieStatsSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for movies
    Provides: GET, POST, PUT, PATCH, DELETE
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieSerializer
    
    def get_queryset(self):
        queryset = Movie.objects.all()
        
        # Filter by search query
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Filter by year
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(year=year)
        
        # Filter by watch_again
        watch_again = self.request.query_params.get('watch_again', None)
        if watch_again:
            queryset = queryset.filter(watch_again=True)
        
        # Filter by rating
        min_rating = self.request.query_params.get('min_rating', None)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        
        # Order by
        ordering = self.request.query_params.get('ordering', '-date_added')
        if ordering in ['name', 'year', 'rating', 'date_added', '-name', '-year', '-rating', '-date_added']:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get movie collection statistics"""
        movies = Movie.objects.all()
        
        stats_data = {
            'total_movies': movies.count(),
            'watch_again_count': movies.filter(watch_again=True).count(),
            'average_rating': movies.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,
            'total_genres': len(set([tag.strip() for movie in movies for tag in movie.get_tags_list()])),
            'movies_by_year': dict(movies.values('year').annotate(count=Count('year')).values_list('year', 'count')),
            'top_rated_movies': movies.filter(rating__isnull=False).order_by('-rating')[:5]
        }
        
        serializer = MovieStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get recommended movies (watch_again=True, high ratings)"""
        recommended = Movie.objects.filter(
            watch_again=True, 
            rating__gte=7.0
        ).order_by('-rating')[:10]
        
        serializer = MovieListSerializer(recommended, many=True)
        return Response(serializer.data)
