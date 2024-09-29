import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import django
import os
from ..models import Genre, Book

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookABook_project.settings')
django.setup()

from sklearn.feature_extraction.text import CountVectorizer
from ..models import Genre, Book

def get_cbf_matrix():
    # Get all books
    books = Book.objects.all()

    # Preprocess the 'genre' column
    book_genres = []
    for book in books:
        # Get all genres of the current book
        genres = book.genres.all()
        genre_names = ', '.join(genre.name for genre in genres)
        book_genres.append(genre_names)

    # Create a DataFrame from the books QuerySet
    data = pd.DataFrame.from_records(books.values())

    # Add the 'genre' column to the DataFrame
    data['genre'] = book_genres

    # Create a CountVectorizer object
    count = CountVectorizer(token_pattern='[a-zA-Z0-9\s]+')

    # Create the count matrix
    count_matrix = count.fit_transform(data['genre'])

    # Convert the count matrix to a DataFrame for better visualization
    df_count_matrix = pd.DataFrame(count_matrix.toarray(), columns=count.get_feature_names_out())

    # Create a DataFrame for the 'short' and 'long' features
    df_pages = pd.DataFrame()

    # Set 'short' to 1 for books less than or equal to 150 pages, 0 otherwise
    df_pages['short'] = (data['num_pages'] <= 150).astype(int)

    # Set 'long' to 1 for books more than 150 pages, 0 otherwise
    df_pages['long'] = (data['num_pages'] > 150).astype(int)

    # Concatenate the count matrix and the pages DataFrame
    df_features = pd.concat([df_pages, df_count_matrix], axis=1)

    return df_features

if __name__ == '__main__':
    df_features = get_cbf_matrix()
    # save the matrix to a file
    df_features.to_csv('../../data/cbf_matrix.csv', index=False)