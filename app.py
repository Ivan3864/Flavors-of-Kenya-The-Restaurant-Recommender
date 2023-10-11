from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

# Load your dataset (replace 'your_data.csv' with your dataset file)
final_data = pd.read_csv('final.csv')

# Combine relevant features into a single column for TF-IDF vectorization
final_data['combined_features'] = final_data['features'] + ' ' + final_data['cuisine'] + ' ' + final_data['town'] + ' ' + final_data['name'] + ' ' + final_data['category']

# Fill missing values in the 'combined_features' column with an empty string
final_data['combined_features'] = final_data['combined_features'].fillna('')

# Create a TF-IDF vectorizer for the 'combined_features' column
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(final_data['combined_features'])

# Create a NearestNeighbors model
n_neighbors = 10  # Number of similar hotels to recommend
knn_model = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
knn_model.fit(tfidf_matrix)

# Function to get hotel recommendations
def recommend_hotels_restaurants(input_features, n_recommendations=5):
    print("Input features:", input_features)

    # Transform input_features into a TF-IDF vector
    input_vector = tfidf_vectorizer.transform([input_features])
    
    print("Input vector shape:", input_vector.shape)  # Add this line for debugging

    # Find the most similar hotels
    _, indices = knn_model.kneighbors(input_vector, n_neighbors=n_recommendations)

    print("Indices:", indices)  # Add this line for debugging

    # Return the recommended hotels with relevant information
    recommended_hotels = final_data.iloc[indices[0]][['name', 'town', 'category', 'combined_features', 'locationString', 'average_price']]
    print("Recommended hotels:", recommended_hotels)  # Add this line for debugging

    return recommended_hotels


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommendations', methods=['POST'])
def recommendations():
    user_input = request.form['user_input']
    recommended_hotels = recommend_hotels_restaurants(user_input, n_recommendations=5)
    print("Recommendations:", recommended_hotels)  # Add this line for debugging
    return render_template('recommendations.html', recommendations=recommended_hotels)



if __name__ == '__main__':
    app.run(debug=True)







