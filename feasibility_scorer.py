import pandas as pd
import ast

# --- CONFIGURATION ---
INPUT_FILE = 'vwo_corpus_cleaned.csv'
OUTPUT_FILE = 'vwo_corpus_scored.csv'

# Define keywords that indicate a detailed A/B test description.
# These words suggest the text describes the 'how' and not just the 'what'.
DETAIL_KEYWORDS = [
    'variation', 'control', 'hypothesis', 'button', 'headline', 'form',
    'design', 'image', 'text', 'copy', 'color', 'layout', 'price', 'cta',
    'page', 'element', 'change', 'test', 'version'
]

# --- SCRIPT ---

# Function to calculate the detail score for a list of tokens
def calculate_detail_score(token_list):
    """Counts how many unique detail-oriented keywords are present in a list of tokens."""
    # Using a set for efficiency to find unique words present in both lists
    found_keywords = set(token_list) & set(DETAIL_KEYWORDS)
    return len(found_keywords)

print(f"Loading cleaned data from '{INPUT_FILE}'...")
df = pd.read_csv(INPUT_FILE)

# Safely convert the 'cleaned_tokens' string back into a list
df['cleaned_tokens'] = df['cleaned_tokens'].apply(ast.literal_eval)

print("Calculating detail scores for each case study...")
# Apply the scoring function to create our new column
df['detail_score'] = df['cleaned_tokens'].apply(calculate_detail_score)

# Sort the DataFrame to see the highest-scoring (most promising) articles first
df_sorted = df.sort_values(by='detail_score', ascending=False)

print("\n--- Top 5 Most Detailed Case Studies ---")
print(df_sorted[['title', 'detail_score', 'url']].head())

print("\n--- Top 5 Least Detailed Case Studies ---")
print(df_sorted[['title', 'detail_score', 'url']].tail())

# Save the entire scored DataFrame to a new file
df_sorted.to_csv(OUTPUT_FILE, index=False)
print(f"\nScored data has been saved to '{OUTPUT_FILE}'")