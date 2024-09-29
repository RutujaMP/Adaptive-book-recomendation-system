import random

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


def mood_to_vector(moods, mood_keywords):
    return [1 if mood in mood_keywords else 0 for mood in moods]


def get_mood_based_recommendation(mood_keywords):
    # Load the mood_matrix
    mood_matrix = pd.read_csv('data/mood_matrix.csv')

    mood_vector = mood_to_vector(mood_matrix.columns, mood_keywords)

    # print(f'mood_vector: {mood_vector}')

    # Calculate the cosine similarity
    similarities = cosine_similarity(mood_matrix, [mood_vector])

    # print(f'similarities: {similarities}')

    # Get the 5 most similar books, excluding the book itself
    recommended_books = np.argsort(-similarities.flatten())[:5]

    return recommended_books


if __name__ == "__main__":
    mood_keywords = ['happy', 'spring', 'romance']
    recommendations = get_mood_based_recommendation(mood_keywords)
    print(f'mood: {mood_keywords}, recommendations: {recommendations}')

    mood_keywords = ['happy', 'spring', 'misterious']
    recommendations = get_mood_based_recommendation(mood_keywords)
    print(f'mood: {mood_keywords}, recommendations: {recommendations}')

    mood_keywords = ['sad', 'spring', 'misterious']
    recommendations = get_mood_based_recommendation(mood_keywords)
    print(f'mood: {mood_keywords}, recommendations: {recommendations}')

    mood_keywords = ['sad', 'adventurous', 'misterious']
    recommendations = get_mood_based_recommendation(mood_keywords)
    print(f'mood: {mood_keywords}, recommendations: {recommendations}')

