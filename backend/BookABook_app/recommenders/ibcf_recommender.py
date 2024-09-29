import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .build_ibcf_matrix import get_ibcf_matrix


def get_ibcf_recommendation(user_id):
    # Load the ratings matrix
    # ratings_matrix = pd.read_csv('../../data/ibcf_matrix.csv', index_col='user_id')
    ratings_matrix = get_ibcf_matrix()
    #print("ratings_matrix size is ",ratings_matrix.shape)
    # Calculate the cosine similarity
    similarity = cosine_similarity(ratings_matrix)
    #print("similarity size is ",similarity.shape)
    #print("user id type is ",type(user_id))
    user_id = int(user_id)
    # Get the 10 most similar users, excluding the user itself
    similar_users = np.argsort(-similarity[user_id])[1:11]
    
    #print("similar_users1 is ",similar_users)
    # Ensure the user IDs exist in the index of the ratings_matrix DataFrame
    similar_users = np.intersect1d(similar_users, ratings_matrix.index)
    #print("similar_users2 size is ",similar_users.shape)
    # Get the books that the similar users have rated the highest
    recommendations = ratings_matrix.loc[similar_users].max().sort_values(ascending=False).index[:10]
    #print("recommendations is ",recommendations)
    return recommendations.tolist()


if __name__ == '__main__':
    user_id = input('Input user_id: ')
    recommendations = get_ibcf_recommendation(int(user_id))
    print(recommendations)
