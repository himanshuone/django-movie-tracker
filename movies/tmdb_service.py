import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class TMDBService:
    """Service for interacting with The Movie Database API"""
    
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.read_access_token = settings.TMDB_READ_ACCESS_TOKEN
        self.base_url = settings.TMDB_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL
        
    def get_headers(self):
        """Get headers for TMDB API requests using Read Access Token"""
        return {
            'Authorization': f'Bearer {self.read_access_token}',
            'Content-Type': 'application/json;charset=utf-8'
        }
    
    def search_movie(self, title, year=None):
        """
        Search for a movie by title and optionally year
        Returns the best match or None
        """
        try:
            url = f"{self.base_url}/search/movie"
            params = {
                'query': title,
                'include_adult': 'false',
                'language': 'en-US',
                'page': 1
            }
            
            if year:
                params['year'] = year
            
            response = requests.get(url, headers=self.get_headers(), params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            if results:
                # If year is provided, try to find exact year match first
                if year:
                    for movie in results:
                        release_date = movie.get('release_date', '')
                        if release_date and release_date.startswith(str(year)):
                            return movie
                
                # Return the first result (usually most relevant)
                return results[0]
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDB API error searching for movie '{title}': {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error searching for movie '{title}': {e}")
            return None
    
    def get_movie_details(self, tmdb_id):
        """
        Get detailed information about a movie by TMDB ID
        """
        try:
            url = f"{self.base_url}/movie/{tmdb_id}"
            params = {
                'language': 'en-US',
                'append_to_response': 'images,videos'
            }
            
            response = requests.get(url, headers=self.get_headers(), params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDB API error getting movie details for ID '{tmdb_id}': {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting movie details for ID '{tmdb_id}': {e}")
            return None
    
    def get_poster_url(self, poster_path, size='w500'):
        """
        Generate full poster URL from TMDB poster path
        Available sizes: w92, w154, w185, w342, w500, w780, original
        """
        if not poster_path:
            return None
        
        return f"https://image.tmdb.org/t/p/{size}{poster_path}"
    
    def find_movie_poster(self, title, year=None):
        """
        Find and return the poster URL for a movie
        This is the main method to use for getting posters
        """
        try:
            # Search for the movie
            movie_data = self.search_movie(title, year)
            
            if not movie_data:
                logger.info(f"No TMDB results found for movie: {title} ({year})")
                return None
            
            # Get poster path
            poster_path = movie_data.get('poster_path')
            
            if not poster_path:
                logger.info(f"No poster found for movie: {title} ({year})")
                return None
            
            # Generate full poster URL
            poster_url = self.get_poster_url(poster_path)
            
            logger.info(f"Found poster for '{title}' ({year}): {poster_url}")
            return poster_url
            
        except Exception as e:
            logger.error(f"Error finding poster for '{title}': {e}")
            return None
    
    def get_movie_info(self, title, year=None):
        """
        Get comprehensive movie information including poster, rating, overview, etc.
        """
        try:
            movie_data = self.search_movie(title, year)
            
            if not movie_data:
                return None
            
            # Extract useful information
            info = {
                'tmdb_id': movie_data.get('id'),
                'title': movie_data.get('title'),
                'original_title': movie_data.get('original_title'),
                'release_date': movie_data.get('release_date'),
                'overview': movie_data.get('overview'),
                'poster_path': movie_data.get('poster_path'),
                'poster_url': self.get_poster_url(movie_data.get('poster_path')) if movie_data.get('poster_path') else None,
                'backdrop_path': movie_data.get('backdrop_path'),
                'vote_average': movie_data.get('vote_average'),
                'vote_count': movie_data.get('vote_count'),
                'popularity': movie_data.get('popularity'),
                'genre_ids': movie_data.get('genre_ids', []),
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting movie info for '{title}': {e}")
            return None


# Global instance
tmdb_service = TMDBService()
