import numpy as np
from process_data import *
from joblib import load
import streamlit as st
import pickle
import zipfile
import joblib
ratings, movies, user_ids, user_ids_set = load_data()


zip_file = '/mount/src/movie_recommend_system/pages/matrix_R.zip'

with zipfile.ZipFile(zip_file, 'r') as z:
    with z.open('matrix_R.pkl') as f:
        R = joblib.load(f)
# Load data from CSV file
# W_nmf, H_nmf, R = algorithm_nmf()
film_poster = pd.read_csv('film_poster.csv')

# Merge movie and film_poster DataFrames on MovieID
merged_df = pd.merge(movies, film_poster, on="movieId")
merged_df = pd.merge(movies, film_poster, on="movieId").drop(columns=["genres_y", "title_y"])
merged_df = merged_df.rename(columns={"title_x": "title", "genres_x": "genres"})

def show_home():
    
    st.title("Hệ thống gợi ý phim")
    user_id = st.text_input('Nhập UserID', key='user_input', value="", type="default")

    # Check if the entered user ID is valid
    if user_id:
        user_id_str = str(user_id)
        if user_id_str.isdigit() and user_id_str in user_ids_set:
            st.write(f"Bạn đã nhập UserID: {user_id_str}")
            user_ratings = ratings[ratings['userId'] == int(user_id_str)]
            
            # Merge ratings with movies to get movie genres
            user_movies = pd.merge(user_ratings, movies, on='movieId')
            
            # Split genres and count occurrences
            genre_counts = user_movies['genres'].str.split('|', expand=True).stack().value_counts()
            
            # Plot genre counts
            plot_genre_counts(genre_counts, user_id_str)
            num_recommendations = st.selectbox('Chọn số lượng đề xuất phim', [5, 10], key='num_rec')
            algorithm = st.selectbox("Chọn thuật toán", ["Thuật toán NMF", "Thuật toán Lee-Seung(Khoảng cách Euclid)","Thuật toán Lee-Seung(Độ phân kỳ Kullback-Leibler)"])
            if algorithm == "Thuật toán NMF":
                if st.button(':red[Đề xuất]'):
                    if not user_ids:
                        st.write("Không có đánh giá của người dùng này.")
                    else:
                        W_nmf, H_nmf = load('nmf_algorithm.pkl') 
                        X_nmf = np.dot(W_nmf, H_nmf)
                        user_index = user_ids.index(user_id_str)
                        user_ratings_pred = X_nmf[user_index]
                        predicted_ratings = pd.DataFrame(user_ratings_pred, index=R.columns, columns=['predicted_rating'])
                        predicted_ratings = predicted_ratings.join(merged_df.set_index('movieId'))
                        
                        # Filter movies by user's favorite genres
                        user_favorite_genres = genre_counts.index[:3]  # Choose top 3 genres
                        recommended_movies = predicted_ratings[predicted_ratings['genres'].str.contains('|'.join(user_favorite_genres), na=False)].nlargest(num_recommendations, 'predicted_rating')
                        
                        st.write(f"Top {num_recommendations} bộ phim được đề xuất:")
                        cols = st.columns(num_recommendations)
                        if num_recommendations == 5:
                            cols = st.columns(5)
                        elif num_recommendations == 10:
                            cols = [st.columns(5), st.columns(5)]

                        for i, (_, row) in enumerate(recommended_movies.iterrows(), 1):
                            movie_title = row['title']
                            genres = row['genres']
                            poster_url = row['poster_url']
                            if num_recommendations == 5:
                                with cols[i - 1]:
                                    if poster_url:
                                        st.markdown(f'<div style="text-align:center;"><img src="{poster_url}" width="200" height="300"></div>', unsafe_allow_html=True)  # Fixed width and height for the images
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4>", unsafe_allow_html=True)
                                        st.markdown(f"<p style='text-align: center;'>Thể loại</p>", unsafe_allow_html=True)
                                        st.markdown(f"<p style='text-align: center;'>{genres}</p>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4>", unsafe_allow_html=True)
                                        st.markdown(f"<p style='text-align: center;'>Thể loại</p>", unsafe_allow_html=True)
                                        st.markdown(f"<p style='text-align: center;'>{genres}</p>", unsafe_allow_html=True)
                            elif num_recommendations == 10:
                                row = (i - 1) // 5
                                col = (i - 1) % 5
                                with cols[row][col]:
                                    if poster_url:
                                        st.markdown(f'<div style="text-align:center;"><img src="{poster_url}" width="200" height="300"></div>', unsafe_allow_html=True)  # Fixed width and height for the images
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4>", unsafe_allow_html=True)
                                        st.markdown(f"<p style='text-align: center;'>Thể loại: {genres}</p>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4>", unsafe_allow_html=True)
                                        st.markdown(f"<p style='text-align: center;'>Thể loại: {genres}</p>", unsafe_allow_html=True)
            elif algorithm == "Thuật toán Lee-Seung(Khoảng cách Eculid)":
                if st.button(':red[Đề xuất]'):
                    if not user_ids:
                        st.write("Không có đánh giá của người dùng này.")
                    else:
                        W_ls, H_ls = load('lee_seung_algorithm.pkl')
                        R_ls = np.dot(W_ls, H_ls)
                        user_index = user_ids.index(user_id_str)
                        user_ratings_pred = R_ls[user_index]
                        predicted_ratings = pd.DataFrame(user_ratings_pred, index=R.columns, columns=['predicted_rating'])
                        predicted_ratings = predicted_ratings.join(merged_df.set_index('movieId'))
                        
                        # Filter movies by user's favorite genres
                        user_favorite_genres = genre_counts.index[:3]  # Choose top 3 genres
                        recommended_movies = predicted_ratings[predicted_ratings['genres'].str.contains('|'.join(user_favorite_genres), na=False)].nlargest(num_recommendations, 'predicted_rating')
                        
                        st.write(f"Top {num_recommendations} recommended movies:")
                        cols = st.columns(num_recommendations)
                        if num_recommendations == 5:
                            cols = st.columns(5)
                        elif num_recommendations == 10:
                            cols = [st.columns(5), st.columns(5)]

                        for i, (_, row) in enumerate(recommended_movies.iterrows(), 1):
                            movie_title = row['title']
                            genres = row['genres']
                            poster_url = row['poster_url']
                            if num_recommendations == 5:
                                with cols[i - 1]:
                                    if poster_url:
                                        st.markdown(f'<div style="text-align:center;"><img src="{poster_url}" width="200" height="300"></div>', unsafe_allow_html=True)  # Fixed width and height for the images
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4><p style='text-align: center;'>Thể loại: {genres}</p>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4><p style='text-align: center;'>Thể loại: {genres}</p>", unsafe_allow_html=True)
                            elif num_recommendations == 10:
                                row = (i - 1) // 5
                                col = (i - 1) % 5
                                with cols[row][col]:
                                    if poster_url:
                                        st.markdown(f'<div style="text-align:center;"><img src="{poster_url}" width="200" height="300"></div>', unsafe_allow_html=True)  # Fixed width and height for the images
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4><p style='text-align: center;'>Thể loại: {genres}</p>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4><p style='text-align: center;'>Thể loại: {genres}</p>", unsafe_allow_html=True)

            else:
                if st.button(':red[Đề xuất]'):
                    if not user_ids:
                        st.write("Không có đánh giá của người dùng này.")
                    else:
                        W_lskld, H_lskld = load('lee_seung_kld_algorithm.pkl')
                        R_lskld = np.dot(W_lskld, H_lskld)
                        user_index = user_ids.index(user_id_str)
                        user_ratings_pred = R_lskld[user_index]
                        predicted_ratings = pd.DataFrame(user_ratings_pred, index=R.columns, columns=['predicted_rating'])
                        predicted_ratings = predicted_ratings.join(merged_df.set_index('movieId'))
                        
                        # Filter movies by user's favorite genres
                        user_favorite_genres = genre_counts.index[:3]  # Choose top 3 genres
                        recommended_movies = predicted_ratings[predicted_ratings['genres'].str.contains('|'.join(user_favorite_genres), na=False)].nlargest(num_recommendations, 'predicted_rating')
                        
                        st.write(f"Top {num_recommendations} recommended movies:")
                        cols = st.columns(num_recommendations)
                        if num_recommendations == 5:
                            cols = st.columns(5)
                        elif num_recommendations == 10:
                            cols = [st.columns(5), st.columns(5)]

                        for i, (_, row) in enumerate(recommended_movies.iterrows(), 1):
                            movie_title = row['title']
                            genres = row['genres']
                            poster_url = row['poster_url']
                            if num_recommendations == 5:
                                with cols[i - 1]:
                                    if poster_url:
                                        st.markdown(f'<div style="text-align:center;"><img src="{poster_url}" width="200" height="300"></div>', unsafe_allow_html=True)  # Fixed width and height for the images
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4><p style='text-align: center;'>Thể loại: {genres}</p>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4><p style='text-align: center;'>Thể loại: {genres}</p>", unsafe_allow_html=True)
                            elif num_recommendations == 10:
                                row = (i - 1) // 5
                                col = (i - 1) % 5
                                with cols[row][col]:
                                    if poster_url:
                                        st.markdown(f'<div style="text-align:center;"><img src="{poster_url}" width="200" height="300"></div>', unsafe_allow_html=True)  # Fixed width and height for the images
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4><p style='text-align: center;'>Thể loại: {genres}</p>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<h4 style='text-align: center;'> {movie_title}</h4><p style='text-align: center;'>Thể loại: {genres}</p>", unsafe_allow_html=True)

        else:
            st.warning("Vui lòng nhập UserID hợp lệ.")
