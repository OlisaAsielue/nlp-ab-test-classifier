import streamlit as st
import joblib
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# --- Text Preprocessing Function ---
# We need the same preprocessing function from our notebook to clean the user's input.
def preprocess_text(text):
    """Cleans and preprocesses a single text string."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return " ".join(lemmatized_tokens)

# --- Load the Trained Model and Vectorizer ---
# Load the objects we saved from our notebook.
try:
    vectorizer = joblib.load('vectorizer.joblib')
    model = joblib.load('model.joblib')
except FileNotFoundError:
    st.error("Model files not found. Please run the training notebook to generate them.")
    st.stop() # Stop the app if files are missing

# --- Streamlit App Interface ---
st.title('A/B Test Behavioral Principle Classifier')
st.write(
    "This app uses a trained NLP model to predict the primary behavioral principle "
    "behind an A/B test. Enter the text from a case study below to classify it."
)

# Create a text area for user input
user_input = st.text_area("Paste the case study text here:", height=150)

# Create a button to trigger the classification
if st.button('Classify Text'):
    if user_input:
        # 1. Preprocess the user's input
        cleaned_input = preprocess_text(user_input)
        
        # 2. Vectorize the cleaned input using our loaded vectorizer
        vectorized_input = vectorizer.transform([cleaned_input])
        
        # 3. Make a prediction using our loaded model
        prediction = model.predict(vectorized_input)
        
        # Display the result
        st.success(f"Predicted Behavioral Principle: {prediction[0]}")
    else:
        st.warning("Please enter some text to classify.")