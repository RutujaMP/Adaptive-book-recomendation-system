import sqlite3
import pandas as pd
import numpy as np

# 假设变量 n_ratings, n_users, n_books 已经定义
n_ratings = 1000  # 示例：100个评分
n_users = 50  # 示例：50个用户
n_books = 301  # 示例：20本书

# 生成随机评分数据
data = {
    'id': range(1, n_ratings + 1),
    'user_id': np.random.randint(1, n_users + 1, size=n_ratings),
    'book_id': np.random.randint(1, n_books + 1, size=n_ratings),
    'rating': np.random.randint(1, 6, size=n_ratings),  # 假设评分范围是1-5
}

df = pd.DataFrame(data)

# 连接到SQLite数据库
conn = sqlite3.connect('db_test.sqlite3')

# 创建一个查询已存在的用户ID的临时DataFrame
query = "SELECT user_id FROM users"
existing_users = pd.read_sql(query, conn)

# 筛选出存在于用户表中的评分数据
filtered_df = df[df['user_id'].isin(existing_users['user_id'])]

# 将筛选后的数据存储到数据库
filtered_df.to_sql('ratings', conn, if_exists='replace', index=False)

# 关闭数据库连接
conn.close()
