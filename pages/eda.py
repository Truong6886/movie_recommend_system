import streamlit as st
import matplotlib.pyplot as plt
from process_data import *
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

ratings,movies,user_ids,user_ids_set = load_data()

@st.cache_data
def prepare_data():
    df=movies.copy()
    df['genres']=df['genres'].str.split('|')
    df=df.explode('genres')
    movies_df=movies.copy()
    movies_df["num_genres"] = movies_df["genres"].apply(lambda x: len(x.split('|')))
    return df,movies_df

df,movies_df = prepare_data()

@st.cache_data
def rating_hist(ratings):
    fig = px.histogram(ratings, x='rating', nbins=20, title="Phân phối Rating", 
                       labels={'rating': 'Ratings', 'count': 'Frequency'})
    fig.update_xaxes(title_text='Ratings')  
    fig.update_yaxes(title_text='Frequency')
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1),width=1000, height=600,yaxis_tickformat='d',template='plotly_white') 
    st.plotly_chart(fig)

@st.cache_data
def plot_genre_count(df):
    genre_counts = df['genres'].value_counts().reset_index()
    genre_counts.columns = ['genres', 'count']
    
    fig = px.bar(genre_counts, x='genres', y='count', 
                 title='The distribution of Genres', 
                 labels={'genres': 'Genres', 'count': 'Count'},
                 color='genres')
    fig.update_layout(
        xaxis_title='Genres', 
        yaxis_title='Count', 
        xaxis={'categoryorder':'total descending'},
        width=900, 
        height=600,
        plot_bgcolor='white'  
    )
    st.plotly_chart(fig)

@st.cache_data
def plot_genre_distribution(movies_df):
    # Create histogram
    fig = px.histogram(movies_df, x='num_genres', title='The distribution of Movies by Number of Genres')

    # Set axis and title parameters
    fig.update_layout(xaxis_title='Number of genres', yaxis_title='Number of movies', bargap=0.1, showlegend=False, plot_bgcolor='white')
    fig.update_traces(marker_color='green')
    # Display the plot
    st.plotly_chart(fig)

def plot_rating_by_user(ratings):
    user_counts = ratings['userId'].value_counts()

    # Lấy 10 người dùng có số lượng đánh giá cao nhất và thấp nhất
    top_users = user_counts.head(10)
    bottom_users = user_counts.tail(10)

    # Gộp dữ liệu của top và bottom users
    merged_data = pd.concat([top_users, bottom_users])

    # Tạo DataFrame từ dữ liệu gộp
    df = merged_data.reset_index()
    df.columns = ['userId', 'Number of Ratings']

    # Vẽ biểu đồ bằng Plotly
    fig = px.bar(df, x='userId', y='Number of Ratings', 
                 text='Number of Ratings', color='Number of Ratings',
                 labels={'Number of Ratings': 'Number of Ratings', 'UserID': 'UserID'})
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(title='Number of Ratings per User',
                      xaxis_title='UserID',
                      yaxis_title='Number of Ratings',
                      xaxis=dict(type='category', tickangle=0),width=900,  # Chiều rộng của biểu đồ
                      height=500, plot_bgcolor='white')
    st.plotly_chart(fig)

def plot_rating_by_movie():
    ratings_per_movie = ratings['movieId'].value_counts()
    top_users = ratings_per_movie.head(10)
    bottom_users = ratings_per_movie.tail(10)

    # Gộp dữ liệu của top và bottom users
    merged_data = pd.concat([top_users, bottom_users])

    # Tạo DataFrame từ dữ liệu gộp
    df = merged_data.reset_index()
    df.columns = ['userId', 'Number of Movies']

    # Vẽ biểu đồ bằng Plotly
    fig = px.bar(df, x='userId', y='Number of Movies', 
                 text='Number of Movies', color='Number of Movies',
                 labels={'Number of Movies': 'Number of Movies', 'UserID': 'UserID'},color_continuous_scale='Purples')
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(title='Number of Movies per User',
                      xaxis_title='UserID',
                      yaxis_title='Number of Movies',
                      xaxis=dict(type='category', tickangle=0),width=900,  
                      height=500, plot_bgcolor='white')
    
    st.plotly_chart(fig)

def genres_per_user(ratings, movies):
    # Merge ratings and movies on 'movieId'
    data = pd.merge(ratings, movies, on='movieId')
    
    # Group by 'userId' and count unique genres
    genres_per_user = data.groupby('userId')['genres'].nunique()
    
    # Sort values in descending order
    sorted_genres_per_user = genres_per_user.sort_values(ascending=False)
    
    # Get the top 10 and bottom 10 users
    top_users = sorted_genres_per_user.head(10)
    bottom_users = sorted_genres_per_user.tail(10)
    
    # Combine top and bottom users
    merged_data = pd.concat([top_users, bottom_users])
    
    # Create DataFrame from merged data
    df1 = merged_data.reset_index()
    df1.columns = ['userId', 'Number of Genres']
    
    # Sort DataFrame by 'Number of Genres' in descending order
    df1 = df1.sort_values(by='Number of Genres', ascending=False)
    
    # Plot bar chart with Plotly
    fig = px.bar(df1, x='userId', y='Number of Genres', 
                 text='Number of Genres', color='Number of Genres',
                 labels={'Number of Genres': 'Number of Genres', 'userId': 'UserID'},
                 color_continuous_scale='gnbu')
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(title='Number of Genres per User',
                      xaxis_title='UserID',
                      yaxis_title='Number of Genres',
                      xaxis=dict(type='category', tickangle=0),
                      width=900,
                      height=500, plot_bgcolor='white')
    
    st.plotly_chart(fig)

def top_10_most_rated_movies(ratings, movies):
    # Tính số lượng xếp hạng cho mỗi bộ phim từ dữ liệu ratings
    ratings_count_per_movie = ratings['movieId'].value_counts()

    # Ghép thông tin về số lượng xếp hạng vào DataFrame movies
    movies['ratings_count'] = ratings_count_per_movie

    # Sắp xếp các bộ phim theo số lượng xếp hạng giảm dần
    top_movies = movies.sort_values(by='ratings_count', ascending=False).head(10)

    # Tạo biểu đồ bằng Plotly
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Bar(x=top_movies['title'], y=top_movies['ratings_count'], marker_color='green'), row=1, col=1)

    # Cập nhật layout và kích thước biểu đồ
    fig.update_layout(title_text='Top 10 Most Rated Movies', xaxis_title='Movie Title', yaxis_title='Number of Ratings', height=500, width=700, plot_bgcolor='white')

    # Hiển thị biểu đồ
    st.plotly_chart(fig)

def show_EDA():
    select_eda = st.selectbox("Chọn thuộc tính phân phối",["","Phân phối Rating(The distribution of Rating)","Phân phối thể loại phim(The distribution of Genres)","Phân phối phim theo số lượng thể loại(The distribution of Movies by Number of Genres)",
                                                           "Số lượng đánh giá của mỗi người dùng(Number of Ratings per User)",
                                                         "Số lượng bộ phim mà mỗi người dùng đã đánh giá(Number of Movies per User)",
                                                         "Số lượng thể loại phim mỗi người dùng đã xem(Number of Genres per User)","Top 10 bộ phim được đánh giá nhiều nhất(Top 10 Most Rated Movies)"])

    if select_eda =="Phân phối Rating(The distribution of Rating)":
        rating_hist(ratings)
    elif select_eda == "Phân phối thể loại phim(The distribution of Genres)":
        plot_genre_count(df)
    elif select_eda == "Phân phối phim theo số lượng thể loại(The distribution of Movies by Number of Genres)":
        plot_genre_distribution(movies_df) 
    elif select_eda == "Số lượng đánh giá của mỗi người dùng(Number of Ratings per User)":
        plot_rating_by_user(ratings)
    elif select_eda == "Số lượng bộ phim mà mỗi người dùng đã đánh giá(Number of Movies per User)":
        plot_rating_by_movie()
    elif select_eda == "Số lượng thể loại phim mỗi người dùng đã xem(Number of Genres per User)":
        genres_per_user(ratings,movies)
    elif select_eda == "Top 10 bộ phim được đánh giá nhiều nhất(Top 10 Most Rated Movies)":
        top_10_most_rated_movies(ratings, movies)
