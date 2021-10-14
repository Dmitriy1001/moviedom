from django.urls import path
from . import views


urlpatterns = [
    path('', views.MovieList.as_view(), name='index'),
    path('filter/<str:model>/<slug:model_url>/', views.FilterMovieList.as_view(), name='filter_movies_list'),
    path('multiple_filter/', views.MultipleFilterMovieList.as_view(), name='multiple_filter_movies_list'),
    path('search/', views.SearchMovieList.as_view(), name='search_movies_list'),
    path('movie_detail/<slug:movie_url>/', views.MovieDetail.as_view(), name='movie_detail'),
]