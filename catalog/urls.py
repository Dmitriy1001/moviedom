from django.urls import path
from . import views


urlpatterns = [
    path('', views.MovieList.as_view(), name='index'),
    path('categories/<slug:category_url>/', views.CategoryMovieList.as_view(), name='category_movies_list'),
    path('movies/<slug:movie_url>/', views.MovieDetail.as_view(), name='movie_detail'),
]