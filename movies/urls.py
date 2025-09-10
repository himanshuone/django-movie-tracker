from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('add/', views.add_movie, name='add_movie'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('stats/', views.stats, name='stats'),
    path('export/', views.export_backup, name='export_backup'),
    path('permission-denied/', views.permission_denied_view, name='permission_denied'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    path('movie/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
]
