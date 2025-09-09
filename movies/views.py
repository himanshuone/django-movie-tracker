from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Movie
from .forms import MovieForm, CSVUploadForm
import csv
import io
import requests
from django.db.models import Count, Avg
from collections import Counter
from datetime import datetime


def is_admin(user):
    """Check if user is admin (staff or superuser)"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def permission_denied_view(request):
    """Show permission denied page with LinkedIn redirect"""
    return render(request, 'permission_denied.html')


def movie_list(request):
    """Display list of movies with search and filter functionality"""
    movies = Movie.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        movies = movies.filter(
            Q(name__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Filter by year
    year_filter = request.GET.get('year', '')
    if year_filter:
        movies = movies.filter(year=year_filter)
    
    # Filter by tags
    tag_filter = request.GET.get('tag', '')
    if tag_filter:
        movies = movies.filter(tags__icontains=tag_filter)
    
    # Sorting
    sort_by = request.GET.get('sort', 'date_added')
    if sort_by == 'name':
        movies = movies.order_by('name')
    elif sort_by == 'year':
        movies = movies.order_by('-year')
    elif sort_by == 'rating':
        movies = movies.order_by('-rating')
    else:  # default: date_added
        movies = movies.order_by('-date_added')
    
    # Pagination
    paginator = Paginator(movies, 12)  # Show 12 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique years and tags for filters
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('-year')
    all_tags = []
    for movie in Movie.objects.exclude(tags__isnull=True).exclude(tags=''):
        all_tags.extend(movie.get_tags_list())
    unique_tags = sorted(list(set(all_tags)))
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'year_filter': year_filter,
        'tag_filter': tag_filter,
        'sort_by': sort_by,
        'years': years,
        'tags': unique_tags,
        'total_movies': Movie.objects.count(),
        'watch_again_count': Movie.objects.filter(watch_again=True).count(),
    }
    return render(request, 'movies/movie_list.html', context)


def movie_detail(request, movie_id):
    """Display movie detail page"""
    movie = get_object_or_404(Movie, id=movie_id)
    context = {'movie': movie}
    return render(request, 'movies/movie_detail.html', context)


@user_passes_test(is_admin, login_url='/permission-denied/')
def add_movie(request):
    """Add a new movie"""
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            
            # Try to fetch poster from TMDB if no poster provided
            if not movie.poster_url and not movie.poster_image:
                try:
                    from .tmdb_service import tmdb_service
                    tmdb_poster = tmdb_service.find_movie_poster(movie.name, movie.year)
                    if tmdb_poster:
                        movie.poster_url = tmdb_poster
                        movie.save(update_fields=['poster_url'])
                        messages.info(request, f'✨ Auto-fetched poster from TMDB!')
                except Exception:
                    pass  # Silently fail if TMDB fetch fails
            
            messages.success(request, f'Movie "{movie.name}" added successfully!')
            return redirect('movie_list')
    else:
        form = MovieForm()
    
    context = {'form': form}
    return render(request, 'movies/add_movie.html', context)


@user_passes_test(is_admin, login_url='/permission-denied/')
def edit_movie(request, movie_id):
    """Edit an existing movie"""
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save()
            messages.success(request, f'Movie "{movie.name}" updated successfully!')
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    
    context = {'form': form, 'movie': movie}
    return render(request, 'movies/edit_movie.html', context)


@user_passes_test(is_admin, login_url='/permission-denied/')
def upload_csv(request):
    """Upload movies from CSV file"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            try:
                # Read CSV file
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                csv_reader = csv.DictReader(io_string)
                
                # Get the header row for debugging
                fieldnames = csv_reader.fieldnames
                print(f'CSV Headers found: {fieldnames}')
                
                added_count = 0
                error_count = 0
                errors = []
                
                for row_num, row in enumerate(csv_reader, start=2):
                    try:
                        # Clean and validate data - handle different column name variations
                        name = (row.get('Name') or row.get('name') or row.get('Movie Name') or row.get('Title') or '').strip()
                        year = (row.get('Year') or row.get('year') or row.get('Release Year') or '').strip()
                        imdb_link = (row.get('IMDb') or row.get('imdb') or row.get('IMDb Link') or row.get('imdb_link') or '').strip()
                        poster_url = (row.get('Poster') or row.get('poster') or row.get('Poster URL') or row.get('poster_url') or '').strip()
                        rating = (row.get('Rating') or row.get('rating') or row.get('My Rating') or '').strip()
                        notes = (row.get('Notes') or row.get('notes') or row.get('Comments') or '').strip()
                        tags = (row.get('Tags') or row.get('tags') or row.get('Genres') or row.get('Genre') or '').strip()
                        watch_again = (row.get('Watch Again') or row.get('watch_again') or row.get('Worth Watching Again') or '').strip()
                        
                        if not name or not year or not imdb_link:
                            errors.append(f'Row {row_num}: Missing required fields (Name, Year, or IMDb)')
                            error_count += 1
                            continue
                        
                        # Check if movie already exists
                        if Movie.objects.filter(name=name, year=int(year)).exists():
                            errors.append(f'Row {row_num}: Movie "{name} ({year})" already exists')
                            error_count += 1
                            continue
                        
                        # Create movie
                        movie_data = {
                            'name': name,
                            'year': int(year),
                            'imdb_link': imdb_link,
                            'notes': notes if notes else None,
                        }
                        
                        if poster_url:
                            movie_data['poster_url'] = poster_url
                        
                        if rating:
                            try:
                                movie_data['rating'] = float(rating)
                            except ValueError:
                                pass
                        
                        if tags:
                            movie_data['tags'] = tags
                        
                        # Handle watch_again field
                        if watch_again:
                            movie_data['watch_again'] = watch_again.lower() in ['yes', 'true', '1', 'y']
                        
                        # Create the movie
                        movie = Movie.objects.create(**movie_data)
                        
                        # Try to fetch poster from TMDB if no poster provided or if it's a placeholder
                        if not poster_url or poster_url in ['https://image.url', 'image.url', 'placeholder']:
                            try:
                                from .tmdb_service import tmdb_service
                                tmdb_poster = tmdb_service.find_movie_poster(name, int(year))
                                if tmdb_poster:
                                    movie.poster_url = tmdb_poster
                                    movie.save(update_fields=['poster_url'])
                                    print(f'✓ Auto-fetched poster for {name}: {tmdb_poster}')
                            except Exception as e:
                                print(f'✗ Failed to fetch poster for {name}: {e}')
                                pass  # Silently fail if TMDB fetch fails
                        added_count += 1
                        
                    except Exception as e:
                        errors.append(f'Row {row_num}: {str(e)}')
                        error_count += 1
                
                # Show results
                if added_count > 0:
                    messages.success(request, f'Successfully added {added_count} movies!')
                
                if error_count > 0:
                    error_msg = f'{error_count} errors occurred:\n' + '\n'.join(errors[:5])
                    if len(errors) > 5:
                        error_msg += f'\n... and {len(errors) - 5} more errors'
                    messages.warning(request, error_msg)
                
                return redirect('movie_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
    else:
        form = CSVUploadForm()
    
    context = {'form': form}
    return render(request, 'movies/upload_csv.html', context)


def stats(request):
    """Display movie statistics"""
    total_movies = Movie.objects.count()
    
    if total_movies == 0:
        context = {
            'total_movies': 0,
            'movies_by_year': [],
            'tag_counts': [],
            'avg_rating': None,
            'top_rated': [],
        }
        return render(request, 'movies/stats.html', context)
    
    # Movies by year with percentages
    movies_by_year_raw = Movie.objects.values('year').annotate(
        count=Count('id')
    ).order_by('-year')[:10]  # Top 10 years
    
    movies_by_year = []
    for item in movies_by_year_raw:
        percentage = round((item['count'] * 100) / total_movies)
        movies_by_year.append({
            'year': item['year'],
            'count': item['count'],
            'percentage': percentage
        })
    
    # Get all tags and count them
    all_tags = []
    for movie in Movie.objects.exclude(tags__isnull=True).exclude(tags=''):
        all_tags.extend(movie.get_tags_list())
    
    tag_counts_raw = Counter(all_tags).most_common(10)  # Top 10 tags
    
    tag_counts = []
    for tag, count in tag_counts_raw:
        percentage = round((count * 100) / total_movies)
        tag_counts.append({
            'tag': tag,
            'count': count,
            'percentage': percentage
        })
    
    # Average rating
    avg_rating = Movie.objects.exclude(rating__isnull=True).aggregate(
        avg_rating=Avg('rating')
    )['avg_rating']
    
    # Highest rated movies
    top_rated = Movie.objects.exclude(rating__isnull=True).order_by('-rating')[:5]
    
    context = {
        'total_movies': total_movies,
        'movies_by_year': movies_by_year,
        'tag_counts': tag_counts,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
        'top_rated': top_rated,
    }
    return render(request, 'movies/stats.html', context)


def export_backup(request):
    """Export all movie data to CSV file"""
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'iseethrough_movies_backup_{timestamp}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write CSV header
    writer.writerow([
        'Name',
        'Year', 
        'IMDb Link',
        'Poster URL',
        'Rating',
        'Notes',
        'Tags',
        'Watch Again',
        'Date Added'
    ])
    
    # Get all movies and write data
    movies = Movie.objects.all().order_by('-date_added')
    
    for movie in movies:
        writer.writerow([
            movie.name,
            movie.year,
            movie.imdb_link,
            movie.poster_url or '',
            movie.rating or '',
            movie.notes or '',
            movie.tags or '',
            'Yes' if movie.watch_again else 'No',
            movie.date_added.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response
