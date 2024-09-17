from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd 
import gzip

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])

    recommended_movies = []
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

def get_similar_titles(query):
    titles = movies['title'].tolist()
    similar_titles = [title for title in titles if query.lower() in title.lower()]
    return similar_titles[:10]

# Load the trained model
model_path = 'movie_dict.pkl'
with open(model_path, 'rb') as file:
    movie = pickle.load(file)

movies = pd.DataFrame(movie)

with gzip.open('model_compressed.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommender():
     user_input = request.form['userInput']
     recommendations = recommend(user_input)
     return jsonify({'recommendations': recommendations}) 

@app.route('/suggest', methods=['GET'])
def suggest():
    query = request.args.get('query')
    similar_titles = get_similar_titles(query)
    return jsonify({'suggestions': similar_titles})

if __name__ == "__main__":
    app.run(debug=True)