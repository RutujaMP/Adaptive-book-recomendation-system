import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import os
import django
from .models import Book, Genre  # 确保同时导入了Book和Genre模型

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookABook_project.settings')
django.setup()


class algorithm:
    def get_cbf_Matrix(self, file):
        if os.path.isfile('data/cbf_matrix.csv'):
            df_features = pd.read_csv('data/cbf_matrix.csv')
        else:
            df_features = self.calculate_cbf_matrix()
        return df_features

    def calculate_cbf_matrix(self):
        conn = sqlite3.connect('../db_test.sqlite3')
        data = pd.read_sql_query("SELECT * from books", conn)
        book_genres = []
        for index, row in data.iterrows():
            genres = Genre.objects.filter(books__id=row['id'])
            genre_names = ', '.join(genre.name for genre in genres)
            book_genres.append(genre_names)

        data['genre'] = book_genres
        count = CountVectorizer(token_pattern='[a-zA-Z0-9\s]+')
        count_matrix = count.fit_transform(data['genre'])
        df_count_matrix = pd.DataFrame(count_matrix.toarray(), columns=count.get_feature_names_out())
        df_pages = pd.DataFrame()
        df_pages['short'] = (data['num_pages'] <= 150).astype(int)
        df_pages['long'] = (data['num_pages'] > 150).astype(int)
        df_features = pd.concat([df_pages, df_count_matrix], axis=1)
        df_features.to_csv('data/cbf_matrix.csv', index=False)
        conn.close()
        return df_features

    def get_ibcf_matrix(self, file):
        df_features = pd.read_csv(file)
        return df_features

    def updata_ibcf_matrix(self):
        conn = sqlite3.connect('../db_test.sqlite3')
        data = pd.read_sql_query("SELECT * from ratings", conn)
        ratings_matrix = data.pivot_table(index='user_id', columns='book_id', values='rating')
        ratings_matrix.fillna(0, inplace=True)
        ratings_matrix.to_csv('data/ibcf_matrix.csv')
        conn.close()

    def get_cbf_recommendation(self, book_names):
        # Load the features matrix
        df_features = pd.read_csv('data/cbf_matrix.csv')
        # Load the book_ids and names
        df_books = pd.DataFrame(list(Book.objects.all().values('id', 'title')))

        # 使用书名获取相应的书籍ID
        book_ids = df_books[df_books['title'].isin(book_names)]['id'].tolist()
        # Calculate the cosine similarity
        similarity = cosine_similarity(df_features)
        # Initialize an empty list to store recommendations
        recommendations = []
        # Iterate over each book_id in the input list
        for book_id in book_ids:
            book_index = df_books.index[df_books['id'] == book_id].tolist()[0] if df_books[
                df_books['id'] == book_id].index.tolist() else None
            if book_index is not None:
                similar_books = np.argsort(-similarity[book_index])[1:11]
                recommendations.extend(similar_books.tolist())
            # Add the similar books to the recommendations list

        # Remove duplicates from the recommendations list
        recommendations = list(set(recommendations))
        # If more than 10 recommendations, keep only the top 10
        if len(recommendations) > 10:
            recommendations = recommendations[:10]
        print("cbf recommend book ", recommendations)
        return recommendations

    def get_ibcf_recommendation(self, user_id):
        # Load the ratings matrix
        ratings_matrix = pd.read_csv('data/ibcf_matrix.csv', index_col='user_id')
        print("ratings_matrix index is", ratings_matrix.index)
        # 检查提供的user_id是否存在于ratings_matrix的索引中
        if user_id not in ratings_matrix.index:
            raise ValueError("User ID not found in ratings matrix.")

        # 计算所有用户的余弦相似度
        similarity = cosine_similarity(ratings_matrix, ratings_matrix.loc[[user_id]])

        # 获取除自身外的相似度分数
        similarity_scores = similarity.flatten()
        similarity_scores = np.delete(similarity_scores, np.where(ratings_matrix.index == user_id))

        # 获取最相似用户的索引；注意，如果用户总数少于10，则获取所有用户
        num_users = len(ratings_matrix.index) - 1  # 排除自己
        num_similar_users = min(num_users, 10)  # 选择最多10个或实际用户数
        similar_users_indices = np.argsort(-similarity_scores)[:num_similar_users]

        # 获取这些相似用户的用户ID
        similar_users_ids = ratings_matrix.index[similar_users_indices]

        # 从相似用户中获取最高评分的书籍
        recommendations = ratings_matrix.loc[similar_users_ids].max().sort_values(ascending=False).index[:10]

        return recommendations.tolist()

    def get_hybrid_recommendation(self, book_names, user_id):
        # 获取基于内容的推荐
        cbf_recommendations = self.get_cbf_recommendation(book_names)

        # 获取基于物品的协同过滤推荐
        ibcf_recommendations = self.get_ibcf_recommendation(user_id)

        # 结合两种推荐
        # 这里我们使用简单的并集合并两者推荐，但可以根据需要进行加权或排序
        combined_recommendations = list(set(cbf_recommendations + ibcf_recommendations))

        # 如果结果列表太长，你可以在这里实现一种截断策略
        # 例如，随机选择，根据另一种度量来排序，或者保留更靠前的推荐
        if len(combined_recommendations) > 10:
            combined_recommendations = combined_recommendations[:10]

        # 转换ID为书籍标题
        recommended_titles = Book.objects.filter(id__in=combined_recommendations).values_list('title', flat=True)

        return list(recommended_titles)
