import pickle
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
        page_title="Movie Recommendation System ",
        page_icon="🎬",
        layout="wide",
    )

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=9fe63ff93677fdb4830b4c8cb4b6a897&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters



st.header('🎬 Movie Recommendation System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb')) 

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)


def selected_title(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=9fe63ff93677fdb4830b4c8cb4b6a897&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    title=data['original_title']
    return title

def selected_genres(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=9fe63ff93677fdb4830b4c8cb4b6a897&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    genre = "Genre : "
    for i in data['genres']:
        genre+=i['name']+" | "
    return genre[:len(genre)-2]

def selected_runtime(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=9fe63ff93677fdb4830b4c8cb4b6a897&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    ans = "Run-time : "
    runtime = data['runtime']
    ans+=str(runtime)
    return ans + " mins"

def selected_cast(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=9fe63ff93677fdb4830b4c8cb4b6a897&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    cast = "Cast : "
    castList = data['cast']
    for j in range(3):
        cast += castList[j]['original_name'] + " | "
    return cast[:len(cast)-2]

def selected_director(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=9fe63ff93677fdb4830b4c8cb4b6a897&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    director = "Director : "
    directorList = data['crew']
    for i in directorList:
        if i['job']=="Director":
            return director + i['original_name']
    return None

def selected_release(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/release_dates?api_key=9fe63ff93677fdb4830b4c8cb4b6a897&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    date = data['results'][0]['release_dates'][0]['release_date']
    
    return date[:4]

def selected_reviews(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/reviews?api_key=9fe63ff93677fdb4830b4c8cb4b6a897&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    reviews = []
    for review in data.get("results", []):
        content = review.get("content", "")
        reviews.append(content)
    return reviews

def selected_overview(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=9fe63ff93677fdb4830b4c8cb4b6a897&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    overview = "Overview : "
    overview += data['overview']
    return overview

def selected_rating(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=9fe63ff93677fdb4830b4c8cb4b6a897&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    li=[]
    li.append(data['vote_average'])
    li.append(data['vote_count'])
    return li

model=pickle.load(open('sentiment_analysis.pkl','rb'))

def sentiment(reviews):
    # Ensure that reviews is a list of text documents
    if not isinstance(reviews, list):
        raise ValueError("Input 'reviews' must be a list of text documents.")
    
    # Predict sentiments for the entire list of reviews
    sentiments = model.predict(reviews)
    return sentiments



if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    st.markdown("<p style='font-size:32px';'font-weight':bold>{}</p>".format("Movie Details"),unsafe_allow_html=True)
    coll1,coll2,coll3=st.columns(3, gap = "large")
    selected_movie_row = movies.loc[movies['title'] == selected_movie]
    selected_movie_id = selected_movie_row.iloc[0]['movie_id']
    st.markdown("---")
    st.markdown("<p style='font-size:32px';'font-weight':bold;>{}</p>".format("Movie Reviews Sentiments"),unsafe_allow_html=True)
    if len(selected_reviews(selected_movie_id))!=0:
        review_table={'Review' : selected_reviews(selected_movie_id),
                'sentiment' : sentiment(selected_reviews(selected_movie_id))}
        df = pd.DataFrame(review_table)
        st.table(df)
    else:
        st.write("<p style='font-size:20px';>{}</p>".format("No reviews found!"),unsafe_allow_html=True)
        # st.dataframe(df,width=800,height=400)
    st.markdown("---")
    st.markdown("<p style='font-size:32px';'font-weight':bold>{}</p>".format("🍿 Movie Recommendations"),unsafe_allow_html=True)
 
    col1, col2, col3, col4, col5 = st.columns(5,gap = "large")
    
    

    with coll1:
        # st.image(fetch_poster(movies[movies['title'][selected_movie]].movie_id))
        selected_movie_row = movies.loc[movies['title'] == selected_movie]
        selected_movie_id = selected_movie_row.iloc[0]['movie_id']
        st.image(fetch_poster(selected_movie_id))

    with coll2:
        selected_movie_row = movies.loc[movies['title'] == selected_movie]
        selected_movie_id = selected_movie_row.iloc[0]['movie_id']
        # st.markdown(selected_title(selected_movie_id))
        st.markdown("<p style='font-size:30px';'font-weight':700>{} ({})</p>".format(selected_title(selected_movie_id),selected_release(selected_movie_id)), unsafe_allow_html=True)
        st.markdown(selected_genres(selected_movie_id))
        st.markdown(selected_runtime(selected_movie_id))
        st.markdown(selected_cast(selected_movie_id))
        st.markdown(selected_director(selected_movie_id))
        st.markdown(selected_overview(selected_movie_id))
    with coll3:
        c1,c2 = st.columns([1,4])
        with c1:
            st.markdown("<p style='font-size:50px'>{}</p>".format("⭐"), unsafe_allow_html=True)
        with c2:
            st.markdown("<p style='margin-top:18px;margin-bottom:0px'>{} / 10</p>".format(selected_rating(selected_movie_id)[0]), unsafe_allow_html=True)
            st.markdown("<p style='color:grey; margin-bottom:20px'>{} Votes</p>".format(selected_rating(selected_movie_id)[1]), unsafe_allow_html=True)

    with col1:
        st.image(recommended_movie_posters[0])
        st.markdown(recommended_movie_names[0])
    with col2:
        st.image(recommended_movie_posters[1])
        st.markdown(recommended_movie_names[1])
    with col3:
        st.image(recommended_movie_posters[2])
        st.markdown(recommended_movie_names[2])
    with col4:
        st.image(recommended_movie_posters[3])
        st.markdown(recommended_movie_names[3])
    with col5:
        st.image(recommended_movie_posters[4])
        st.markdown(recommended_movie_names[4])