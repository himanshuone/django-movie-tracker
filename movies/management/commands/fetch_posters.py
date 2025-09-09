from django.core.management.base import BaseCommand
from movies.models import Movie
from movies.tmdb_service import tmdb_service
import time

class Command(BaseCommand):
    help = 'Fetch movie posters from TMDB API for existing movies without posters'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update posters even if they already exist',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Maximum number of movies to process (default: 50)',
        )

    def handle(self, *args, **options):
        force = options['force']
        limit = options['limit']
        
        # Get movies without posters or all movies if force is True
        if force:
            movies = Movie.objects.all()[:limit]
            self.stdout.write(f"Processing {movies.count()} movies (force mode)...")
        else:
            movies = Movie.objects.filter(
                poster_url__isnull=True,
                poster_image__isnull=True
            )[:limit]
            self.stdout.write(f"Processing {movies.count()} movies without posters...")
        
        updated_count = 0
        failed_count = 0
        
        for i, movie in enumerate(movies, 1):
            self.stdout.write(f"[{i}/{movies.count()}] Processing: {movie.name} ({movie.year})")
            
            try:
                # Get movie info from TMDB
                movie_info = tmdb_service.get_movie_info(movie.name, movie.year)
                
                if movie_info and movie_info.get('poster_url'):
                    # Update movie with TMDB data
                    movie.poster_url = movie_info['poster_url']
                    if movie_info.get('tmdb_id'):
                        movie.tmdb_id = movie_info['tmdb_id']
                    
                    movie.save(update_fields=['poster_url', 'tmdb_id'])
                    
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ Found poster: {movie_info['poster_url']}")
                    )
                else:
                    failed_count += 1
                    self.stdout.write(
                        self.style.WARNING(f"  ✗ No poster found for {movie.name}")
                    )
                
                # Be nice to the API - small delay between requests
                time.sleep(0.2)
                
            except Exception as e:
                failed_count += 1
                self.stdout.write(
                    self.style.ERROR(f"  ✗ Error processing {movie.name}: {e}")
                )
        
        # Summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS(f"Poster fetch completed!")
        )
        self.stdout.write(f"Updated: {updated_count} movies")
        self.stdout.write(f"Failed: {failed_count} movies")
        self.stdout.write(f"Total processed: {updated_count + failed_count} movies")
