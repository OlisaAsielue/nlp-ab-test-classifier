# A/B Test Classifier: A Behavioral Science NLP Project

This project uses Natural Language Processing (NLP) and machine learning to analyze and classify A/B test case studies according to established behavioral science principles. It features a complete data science pipeline, from web scraping and data curation to model training and deployment as an interactive web application.

**Live Demo:** https://nlp-ab-test-classifier-wyq6eqf9aoj3t8yhtovjsx.streamlit.app/

---

## Key Features

* **Dynamic Web Scraper:** A multi-stage Python scraper that navigates a dynamic website's hidden API to collect over 200 case studies.
* **Data Quality Scoring:** A "feasibility scorer" to programmatically identify high-quality documents from a noisy dataset, enabling a pivot to a curated "gold standard" corpus.
* **Machine Learning Model:** A `LinearSVC` classifier trained to predict one of eight behavioral principles from the text of a case study.
* **Interactive Application:** A web app built with Streamlit that allows users to get real-time predictions from the trained model.

---

## Methodology Overview

The project followed a rigorous, multi-stage methodology that adapted to real-world data quality challenges.

1.  **Broad Scraping:** Initially scraped 232 case study summaries from vwo.com.
2.  **Problem Discovery:** Manual labeling revealed that over 60% of the initial data was too vague for classification.
3.  **Methodological Pivot:** Developed a keyword-based scoring system to rank all documents by their likely level of detail.
4.  **Targeted Enrichment:** Created a 50-item "gold standard" corpus by re-scraping the top 50 most promising articles.
5.  **Modeling & Evaluation:** Trained a `LinearSVC` model on the curated corpus, achieving 78% accuracy and gaining insights into the model's performance with a confusion matrix.

---

## Repository Structure

├── app.py                  # The Streamlit web application
├── eda.ipynb               # Jupyter Notebook with EDA, model training, and evaluation
├── orchestrator.py         # Main script to run the full scraping pipeline
├── detail_scraper.py       # Module with the function to scrape a single page
├── feasibility_scorer.py   # Script to score data quality
├── preprocessing.py        # Script for the NLP text cleaning pipeline
├── gold_corpus.csv         # The final, curated, and manually labeled dataset
├── model.joblib            # The saved, trained classification model
├── vectorizer.joblib       # The saved, trained TF-IDF vectorizer
├── LABELLING_GUIDE.md      # Documentation for the manual labeling schema
├── requirements.txt        # All Python dependencies for the project
└── README.md               # This file

---

---

## Setup and Installation

To run this project locally, please follow these steps.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/OlisaAsielue/nlp-ab-test-classifier

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv nlp_env
    # On Windows:
    # .\nlp_env\Scripts\activate
    # On macOS/Linux:
    source nlp_env/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLTK data:**
    Run the following command in your terminal to open the Python interpreter, then enter the commands to download the necessary NLTK packages.
    ```bash
    python
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    exit()
    ```

---

## How to Use This Project

There are two main ways to interact with this project: launching the interactive web application or exploring the analysis notebook.

### Option 1: Launch the Streamlit Application (Recommended)

This is the quickest way to see the final model in action. The app uses the pre-trained model (`model.joblib`) and vectorizer (`vectorizer.joblib`) included in this repository.

From your activated terminal, simply run:
```bash
streamlit run app.py
```
Your web browser will open with the live application.

### Option 2: Explore the Analysis Notebook

If you want to understand the full data analysis and model training process, open and run the cells in the `eda.ipynb` Jupyter Notebook. This notebook covers:

* Exploratory Data Analysis (EDA) of the corpus.
* The complete model training and evaluation pipeline.
* Generation of the final classification report and confusion matrix.

---

## Advanced: Re-generating the Corpus

The `gold_corpus.csv` file is included in this repository so you can run the analysis and app without needing to perform the scraping yourself. However, if you wish to re-create the entire dataset from scratch, you can run the original scripts in sequence. Note that this will take 5-10 minutes.

1.  **Run the orchestrator to collect all URLs and raw data:**
    ```bash
    python orchestrator.py
    ```
    *(This will re-create the `vwo_urls.txt` and other intermediate files)*

2.  **Run the feasibility scorer and other scripts as needed.**
