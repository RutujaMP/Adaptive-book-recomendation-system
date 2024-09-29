from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from django.shortcuts import get_object_or_404
from ..models import Book
from .build_cbf_matrix import get_cbf_matrix


def get_cbf_recommendation(book_names):
    df_features = get_cbf_matrix()
    df_books = pd.DataFrame(list(Book.objects.all().values('id', 'title')))
    book_ids = df_books[df_books['title'].isin(book_names)]['id'].tolist()
    similarity = cosine_similarity(df_features)
    recommendations = []
    for book_id in book_ids:
        similar_books = np.argsort(-similarity[book_id-1])[1:11]  # Subtract 1 from book_id to match zero-based indexing
        recommendations.extend((similar_books+1).tolist())  # Add 1 to match one-based book IDs
    recommendations = list(set(recommendations))
    if len(recommendations) > 10:
        recommendations = recommendations[:10]
    return recommendations


if __name__ == '__main__':
    book_id = int(input('Input book_id: '))
    recommendations = get_cbf_recommendation(book_id)
    print(recommendations)
