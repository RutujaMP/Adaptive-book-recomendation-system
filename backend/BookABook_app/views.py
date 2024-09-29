from rest_framework import generics
from .models import User, Book, Genre, Rating, UserMoods
from .recommenders.ibcf_recommender import get_ibcf_recommendation
from .serializer import BookSerializer
from .recommenders.cbf_recommender import get_cbf_recommendation
from django.contrib.auth import authenticate, login
from django.db import DatabaseError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login as auth_login
from .recommenders.mood_recommender import get_mood_based_recommendation
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.decorators import api_view
from transformers import pipeline
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline
from textblob import TextBlob

def set_cors_headers(function):
    def wrap(request, *args, **kwargs):
        response = function(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"  # Allow credentials (cookies)
        
        # Handle Cookie header
        if "HTTP_COOKIE" in request.META:
            response["Set-Cookie"] = request.META["HTTP_COOKIE"]
        
        return response
    return wrap




@set_cors_headers
@api_view(['GET'])
def get_recommendations(request):
    # print(request.META.get('HTTP_COOKIE'))  # Print the cookies from the request header

    # if not request.user.is_authenticated:
    #     print("not authenticated")
    #     return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    user_id = request.GET.get('user_id')

    try:
        user = User.objects.get(id=user_id)
        favorite_books_titles = list(user.favorite_books.values_list('title', flat=True))
        print("favorite book is ", favorite_books_titles)

        # if don't have favorite books, set a random book
        if len(favorite_books_titles) == 0:
            favorite_books_titles = ['The Catcher in the Rye', 'The Great Gatsby', 'To Kill a Mockingbird', 'The Hobbit']
            print("favorite book is ", favorite_books_titles)

        # hybrid_recommendations = algo.get_hybrid_recommendation(favorite_books_titles, user_id)

        cbf_recommendations = get_cbf_recommendation(favorite_books_titles)
        print("cbf recommend book ", cbf_recommendations)
        try:
            ibcf_recommendations = get_ibcf_recommendation(user_id)
        except Exception as e:
            print("ibcf error ", e)
            ibcf_recommendations = []

        print("ibcf recommend book ", ibcf_recommendations)

        # Combine the two recommendation lists, removing duplicates, select top 3 of each
        combined_recommendations = cbf_recommendations[:3]
        for ibcf_recommendations in ibcf_recommendations:
            if ibcf_recommendations not in combined_recommendations:
                combined_recommendations.append(ibcf_recommendations)
            if len(combined_recommendations) == 6:
                break
        # if less than 6 recommendations, add more from the CBF recommendations
        if len(combined_recommendations) < 6:
            for cbf_recommendation in cbf_recommendations:
                if cbf_recommendation not in combined_recommendations:
                    combined_recommendations.append(cbf_recommendation)
                if len(combined_recommendations) == 6:
                    break

        print("combined recommend book ", combined_recommendations)

        # get book details from book id
        book_details = []
        for book_id in combined_recommendations:
            book = Book.objects.get(id=book_id)
            book_details.append({
                'id' : book_id,
                'title': book.title,
                'author': book.author,
                'genres': [genre.name for genre in book.genres.all()]
            })

        return Response({'recommendations': book_details}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @api_view(['POST'])
# def register_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': 'Registration successful'}, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def save_rating(request):
    # if not request.user.is_authenticated:
    #     return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    user_id = request.GET.get('user_id')
    book_id = request.data.get('book_id')
    rating = request.data.get('rating')

    if not book_id or not rating:
        return Response({'error': 'Book ID and rating are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user has already rated the book
    if Rating.objects.filter(user_id=user_id, book_id=book_id).exists():
        return Response({'error': 'You have already rated this book'}, status=status.HTTP_400_BAD_REQUEST)

    Rating.objects.create(user_id=user_id, book_id=book_id, rating=rating)
    print(f'user_id: {user_id}, book_id: {book_id}, rating: {rating}')
    return Response({'message': f'Rating saved successfully'}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    name = request.data.get('name')
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    User.objects.create_user(username=username, password=password, email=email)
    user = authenticate(request=request, username=username, password=password)
    auth_login(request, user)  # This sets the user in the session
    print(f'user_id: {user.id} logged in')
    return Response({'message': 'Registration successful','userid':user.id}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request=request, username=username, password=password)
    if user is not None:
        # User authenticated, now log them in
        auth_login(request, user)  # This sets the user in the session
        print(f'user_id: {user.id} logged in')
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        # Authentication failed
        return Response({'error': 'Invalid username or password','userid':user.id}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_book_names(request):
    books = Book.objects.all()
    book_names = [book.title for book in books]
    return Response({'books': book_names}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_genres(request):
    genres = Genre.objects.all()
    genre_names = [genre.name for genre in genres]
    # print(genre_names)
    return Response({'genres': genre_names}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def save_favorite_books_and_genres(request):
    # if not request.user.is_authenticated:
    #     return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    # # print(request)
    user_id = request.GET.get('user_id')
    print(f'user_id: {user_id}')
    user = User.objects.get(id=user_id)

    favorite_books = request.data.get('favorite_books')
    print(f'favorite_books: {favorite_books}')
    favorite_genres = request.data.get('favorite_genres')
    print(f'favorite_genres: {favorite_genres}')

    if not favorite_books or not favorite_genres:
        return Response({'error': 'Favorite books and genres are required'}, status=status.HTTP_400_BAD_REQUEST)

    # favorite_books = ['Cosmos', 'Rebecca']
    # convert favorite_books and favorite_genres to lists
    favorite_books = favorite_books.split(';')
    favorite_genres = favorite_genres.split(';')

    print(f'favorite_books: {favorite_books}')
    print(f'favorite_genres: {favorite_genres}')

    if favorite_books:
        book_instances = Book.objects.filter(title__in=favorite_books)
        for book in book_instances:
            print(f'book: {book}')
            user.favorite_books.add(book)


    if favorite_genres:
        genre_instances = Genre.objects.filter(name__in=favorite_genres)
        for genre in genre_instances:
            print(f'genre: {genre}')
            user.favorite_genres.add(genre)

    print(f'favorite_genres: {user.favorite_genres}')

    # save the user object
    user.save()

    return Response({'message': 'Favorite books and genres saved successfully'}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def get_mood_recommendations(request):
    mood_keywords = request.data.get('mood_keywords')
    if not mood_keywords:
        return Response({'error': 'Mood keyword is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        recommendations = get_mood_based_recommendation(mood_keywords)
        book_details = []
        for book_id in recommendations:
            book = Book.objects.get(id=book_id + 1)
            book_details.append({
                'id' : book_id,
                'title': book.title,
                'author': book.author,
                'genres': [genre.name for genre in book.genres.all()]
            })
        return Response({'recommendations': book_details}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Book.objects.all()
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        genre_name = self.request.query_params.get('genre', None)

        # Filter by title if title param is provided
        if title is not None:
            queryset = queryset.filter(title__icontains=title)

        # Filter by author if author param is provided
        if author is not None:
            queryset = queryset.filter(author__icontains=author)

        # Filter by genre if genre param is provided
        if genre_name is not None:
            queryset = queryset.filter(genres__name__icontains=genre_name)

        return queryset
    
@method_decorator(csrf_exempt, name='dispatch')
@api_view(['POST'])
def analyze_sentiment(request):
    try:
        data = request.data
        text = data.get('text', '')
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity  # -1 (negative) to 1 (positive)

        # Simplified mapping of polarity to mood
        if sentiment > 0.1:  # adjust thresholds as needed
            mood = 'happy'
        elif sentiment < -0.1:
            mood = 'sad'
        else:
            mood = 'neutral'

        # Map mood to genre (adjust mapping as needed)
        genre_map = {
            'happy': 'Comedy',
            'sad': 'Drama',
            'neutral': 'Non-Fiction'
        }
        
        genre = genre_map.get(mood)

        return JsonResponse({'mood': mood, 'genre': genre})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        

# Initialize the classifier globally to load it once
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

@api_view(['POST'])
def analyze_mood(request):
    text = request.data.get('text', '')
    candidate_labels = ["Happy", "Sad", "Mysterious", "Adventurous", "Thought-provoking", "Romance", "Cozy", "Fun"]
    results = classifier(text, candidate_labels)
    mood = results['labels'][0]  # Assuming the highest scoring label is the predicted mood

    # Mood to Genre mapping
    mood_to_genre = {
        "Happy": ["Children's Fiction", "Fairy Tales", "Christian Life"],
        "Sad": ["Memoir", "Biography", "Poetry"],
        "Mysterious": ["Mystery", "Detective", "Thriller"],
        "Adventurous": ["Adventure", "Travel", "Science Fiction"],
        "Thought-provoking": ["Philosophy", "Psychology", "Self-Help"],
        "Romance": ["Romance", "Coming-of-Age", "Classic"],
        "Cozy": ["Family Saga", "Christian Literature", "Classic"],
        "Fun": ["Satire", "Art", "Classic"]
    }

    # Select the genre based on the mood
    suggested_genre = mood_to_genre.get(mood, "General")
    print("suggested_genre",suggested_genre)

    # Fetch books for the suggested genre
    book_details = get_books_by_genre(suggested_genre)
    print("book_details",book_details)


    return JsonResponse({
        'text': text,
        'mood': mood,
        'suggested_genre': suggested_genre,
        'recommended_books': book_details
    })

def get_books_by_genre(genre):
    books = Book.objects.filter(genres__name__icontains=genre)
    return [
        {'title': book.title, 'author': book.author, 'genres': [genre.name for genre in book.genres.all()]}
        for book in books
    ]

@api_view(['GET'])
def get_all_genres(request):
    genres = Genre.objects.all()
    genre_names = [genre.name for genre in genres]
    return Response({'genres': genre_names}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_user_moods(request):
    # if not request.user.is_authenticated:
    #     return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    # Assuming user_id is coming from the request
    user_id = request.data.get('user_id')
    mood = request.data.get('mood')

    if not mood:
        return Response({'error': 'Mood value is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if the user has existing mood records
        user_moods = UserMoods.objects.filter(user_id=user_id)

        if user_moods.exists():
            # Update existing mood records
            user_moods = user_moods.first()
            # Shift the mood values to their respective columns
            user_moods.mood1, user_moods.mood2, user_moods.mood3, user_moods.mood4, user_moods.mood5 = (
                mood, user_moods.mood1, user_moods.mood2, user_moods.mood3, user_moods.mood4
            )
            # Save the updated mood records
            user_moods.save()
        else:
            # Create new mood records
            UserMoods.objects.create(user_id=user_id, mood1=mood)

        return Response({'message': 'User moods updated successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
