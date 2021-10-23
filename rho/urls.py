from django.urls import path
from . import views

app_name='rho'
urlpatterns=[
    path('',views.index,name="index"),
    path('actor/<int:actor_id>',views.actor_page,name="actor_page"),
    path('movie/<int:movie_id>',views.movie_page,name="movie_page"),
    path('actor/',views.index_actor,name="index_actor"),
    path('search/',views.search,name="search"),
    # path('search_movie/',views.search_movie,name="search_movie")),
    # path('search_actor/',views.search_actor,name="search_actor")),
    # path('search_comment/',views.search_comment,name="search_comment")),
]