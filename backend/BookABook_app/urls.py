from django.urls import path, include
from .views import register_user, BookListView, get_recommendations, login, get_all_book_names, get_all_genres, \
    save_favorite_books_and_genres, save_rating, get_mood_recommendations,analyze_sentiment,analyze_mood, update_user_moods

urlpatterns = [
    path('register/', register_user, name='register'),
    path('book/', BookListView.as_view(), name='book_list'),
    path('get_recommendations/', get_recommendations, name='get_recommendations'),
    path('login/', login, name='login'),
    path('get_all_books/', get_all_book_names, name='get_all_book_names'),
    path('get_all_genres/', get_all_genres, name='get_all_genres'),
    path('save_rating/', save_rating, name='save_rating'),
    path('save_favorite_books_and_genres/', save_favorite_books_and_genres, name='save_favorite_books_and_genres'),
    path('get_mood_recommendations/', get_mood_recommendations, name='get_based_recommendations'),
    path('analyzesentiment/', analyze_sentiment, name='analyze_sentiment'),
    path('analyze_mood/', analyze_mood, name='analyze_mood'),
    path('update_user_moods/', update_user_moods, name='update_user_moods'),

]
