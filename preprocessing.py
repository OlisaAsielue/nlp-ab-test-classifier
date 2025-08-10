import pandas as pd
import nltk
import re # The regular expression module, for removing punctuation
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# --- NLTK Data Download ---

# nltk.download('punkt')      # For tokenization
# nltk.download('stopwords')  # For stopword removal
# nltk.download('wordnet')    # For lemmatization
# nltk.download('punkt_tab')

# --- Load the Dataset ---
print("Loading the dataset from vwo_corpus.csv...")
try:
    df = pd.read_csv('vwo_corpus.csv')
except FileNotFoundError:
    print("Error: vwo_corpus.csv not found. Make sure the orchestrator script ran successfully.")
    exit()

# --- Preprocessing Function ---
# It's a best practice to wrap the cleaning steps in a single function.
def preprocess_text(text):
    """
    Cleans and preprocesses a single text string by lowercasing,
    removing punctuation, tokenizing, removing stopwords, and lemmatizing.
    """
    # Ensure text is a string
    if not isinstance(text, str):
        return []

    # 1. Convert to lowercase
    text = text.lower()
    
    # 2. Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # 3. Tokenize (split text into words)
    tokens = word_tokenize(text)
    
    # 4. Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # 5. Lemmatize
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    
    return lemmatized_tokens

# --- Apply the Pipeline ---
print("Starting text preprocessing...")

# Drop rows where 'body_text' is missing, to prevent errors
df.dropna(subset=['body_text'], inplace=True)

# This creates a new column containing a list of clean tokens for each case study.
df['cleaned_tokens'] = df['body_text'].apply(preprocess_text)

# Create another column with the cleaned text as a single string
df['cleaned_text'] = df['cleaned_tokens'].apply(lambda tokens: ' '.join(tokens))


print("Preprocessing complete.")
print("Here's a sample of the processed data:")
# Display the original text and the new cleaned columns for comparison
print(df[['body_text', 'cleaned_text']].head())


# --- Save the Cleaned Data ---
OUTPUT_FILE = 'vwo_corpus_cleaned.csv'
df.to_csv(OUTPUT_FILE, index=False)
print(f"\nCleaned data has been saved to '{OUTPUT_FILE}'")