import pandas as pd 
import streamlit as st
from sklearn.decomposition import NMF
from joblib import dump, load
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import imdb
@st.cache_data
def load_data():
    file_path = "ml-1m/ratings.dat"
    ratings = pd.read_csv(file_path, sep="::", header=None, names=["userId", "movieId", "rating", "timestamp"])
    file_path = "ml-1m/movies.dat" 

    movies = pd.read_csv(file_path, sep="::", header=None, names=["movieId", "title", "genres"], encoding="latin1")
    user_ids = sorted(map(str, ratings["userId"].unique()))
    user_ids_set = set(user_ids)

    return ratings,movies,user_ids,user_ids_set
def plot_genre_counts(genre_counts, user_id):
    # Tạo biểu đồ bằng Plotly
    fig = px.bar(
        genre_counts,
        x=genre_counts.index,
        y=genre_counts.values,
        labels={'index': 'Thể loại phim', 'y': 'Số lần xem'},
        title=f'Các thể loại phim của UserID {user_id} hay xem'
    )
    
    # Tùy chỉnh giao diện biểu đồ
    fig.update_layout(
        xaxis_title="Thể loại phim",
        yaxis_title="Số lần xem",
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig)

# #@st.cache_data
# def algorithm_nmf():
#     R = load('matrix_R.pkl')
#     nmf = NMF(n_components=5,init='random',solver="mu")
#     nmf.fit(R.values)

#     W_nmf = nmf.transform(R.values)  # Hệ số người dùng
#     H_nmf = nmf.components_  # Hệ số phim


#     # Tạo ma trận dự đoán
#     #X_nmf = np.dot(H_nmf, W_nmf)

#     # Tạo dataframe từ ma trận dự đoán
    

#     # Save the model to a file
#     dump((W_nmf, H_nmf), 'nmf_algorithm.pkl')
#     return W_nmf,H_nmf,R


# def get_movie_poster_url(movie_title):
#     ia = imdb.IMDb()
#     # Sử dụng phương thức search_movie để tìm kiếm thông tin về phim
#     movies = ia.search_movie(movie_title)
#     if movies:
#         # Lấy thông tin của phim đầu tiên trong kết quả tìm kiếm
#         movie = ia.get_movie(movies[0].movieID)
        
#         if 'full-size cover url' in movie.keys():
#             # Lấy URL của poster (nếu có)
#             poster_url = movie.get('full-size cover url')
#             return poster_url
#         else:
#             return None
 

# def lee_seung_algorithm(R, n_components=30, max_iter=40, epsilon=1e-6):

#     # Kích thước của ma trận R
#     num_users, num_movies = R.shape

#     # Khởi tạo ma trận W_ và H không âm
#     W_ = np.abs(np.random.randn(num_users, n_components))
#     H_ = np.abs(np.random.randn(n_components, num_movies))

#     for i in range(max_iter):
#         # Lưu lại W_ và H_ để kiểm tra điều kiện dừng
#         W_prev = W_.copy()
#         H_prev = H_.copy()

#         # Cập nhật ma trận W
#         numerator = np.dot(R, H_.T)
#         denominator = np.dot(np.dot(W_, H_), H_.T)
#         W_ *= numerator / denominator

#         # Cập nhật ma trận H_
#         numerator = np.dot(W_.T, R)
#         denominator = np.dot(np.dot(W_.T, W_), H_)
#         H_ *= numerator / denominator

#         # Kiểm tra điều kiện dừng
#         diff_W = np.linalg.norm(W_ - W_prev)
#         diff_H = np.linalg.norm(H_ - H_prev)
#         if diff_W < epsilon and diff_H < epsilon:
#             print("Convergence reached after {} iterations".format(i+1))
#             break

#     dump((W_, H_),'lee_seung_algorithm.pkl')
#     return W_, H_