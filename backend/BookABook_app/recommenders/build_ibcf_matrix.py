import pandas as pd
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookABook.settings')
django.setup()
from BookABook_app.models import Rating

def get_ibcf_matrix():
    # Get all ratings
    ratings = Rating.objects.all()

    # Create a DataFrame from the ratings QuerySet
    data = pd.DataFrame.from_records(ratings.values())

    # Pivot the data to get a matrix where rows represent users, columns represent books, and values represent ratings
    ratings_matrix = data.pivot_table(index='user_id', columns='book_id', values='rating')

    # Fill the NaN values with 0
    ratings_matrix.fillna(0, inplace=True)

    return ratings_matrix

if __name__ == '__main__':
    ratings_matrix = get_ibcf_matrix()
    # Save the matrix to a file
    ratings_matrix.to_csv('../../data/ibcf_matrix.csv')