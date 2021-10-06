from django.urls import path
from . import views


urlpatterns = [
    path('', views.MovieList.as_view(), name='index'),
    path('categories/<slug:category_url>/', views.CategoryMovieListMixin.as_view(), name='category_movies_list'),
    path('genres/<slug:genre_url>/', views.GenreMovieList.as_view(), name='genre_movies_list'),
    path('countries/<slug:country_url>/', views.CountryMovieList.as_view(), name='country_movies_list'),
    path('directors/<slug:director_url>/', views.DirectorMovieList.as_view(), name='director_movies_list'),
    path('actors/<slug:actor_url>/', views.ActorMovieList.as_view(), name='actor_movies_list'),
    path('search/', views.SearchMovieList.as_view(), name='search'),
    path('movies/<slug:movie_url>/', views.MovieDetail.as_view(), name='movie_detail'),

]