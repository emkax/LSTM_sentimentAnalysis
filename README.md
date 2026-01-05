# 📦 Sentiment Analysis for E-Commerce Reviews

This project implements an **end-to-end sentiment analysis pipeline** for e-commerce product reviews.  
It includes **web scraping**, **text preprocessing**, **sentiment labeling**, **model training**, and **result export**.

The goal is to classify customer reviews into:
- **Positive**
- **Neutral**
- **Negative**

based on review text and rating scores.

---

## 🧠 Project Overview

Customer reviews contain valuable insights about product quality and user satisfaction.  
This project extracts review data from e-commerce platforms and applies **Natural Language Processing (NLP)** techniques to analyze sentiment automatically.

The workflow consists of:
1. Scraping review text and ratings
2. Cleaning and preprocessing text data
3. Assigning sentiment labels
4. Training a sentiment classification model
5. Exporting predictions for analysis

---

## ⚙️ Features

- Automated e-commerce review scraping
- Dynamic page handling with Selenium
- Comment expansion handling ("Read more")
- Rating extraction via aria-label parsing
- Text cleaning & normalization
- Sentiment classification using ratings
- Imbalanced dataset handling
- Exportable CSV results

---

## 🛠️ Installation

Clone the repository:

git clone https://github.com/emkax/sentiment_analysis_ecommerce.git  
cd sentiment_analysis_ecommerce  

Install dependencies:

pip install -r requirements.txt  

---

## 📌 Scraping Process Explanation (scraper.py)

The scraping system is built using **Selenium + BeautifulSoup** to handle dynamic e-commerce pages.

### 1. URL Input
Target product review URLs are stored in:

link_toko.txt  

Each URL is loaded sequentially by Selenium.

---

### 2. Page Loading & Dynamic Scrolling
Because reviews are dynamically loaded, the scraper:
- Waits for review elements to appear
- Scrolls the page to trigger lazy loading

This ensures all reviews are fetched correctly.

---

### 3. Rating Extraction
Ratings are extracted from the `aria-label` attribute of review elements using regular expressions.

This approach:
- Avoids dependency on UI layout
- Works even if visible rating text changes

---

### 4. Comment Expansion
Some reviews are truncated with a **“Read More”** button.

The scraper:
- Detects expandable comments
- Clicks the button using JavaScript execution
- Waits briefly to allow full text to load

---

### 5. Comment Parsing
After expansion:
- Review HTML is extracted
- Parsed using BeautifulSoup
- Comment text is selected via CSS selectors

Only valid comments with at least 5 characters are stored.

---

### 6. Pagination Handling
The scraper:
- Detects the **Next** button
- Checks whether it is disabled
- Stops scraping automatically when the last page is reached

This prevents infinite scrolling loops.

---

### 7. Data Storage
Scraped data is appended to:

result.csv  

Each row contains:
- comment
- rating

---

## 🧪 Training & Sentiment Classification (train.ipynb)

The training notebook performs the following steps:

---

### 1. Data Cleaning
Text preprocessing includes:
- Lowercasing
- Removing punctuation and numbers
- Removing extra whitespace
- Stopword removal

---

### 2. Sentiment Labeling Strategy

Sentiment labels are derived directly from ratings:

Rating 1–2 → Negative  
Rating 3 → Neutral  
Rating 4–5 → Positive  

This enables supervised learning without manual labeling.

---

### 3. Text Vectorization
Review text is converted into numerical form using:
- Tokenization
- Padding / sequence alignment
- TF-IDF or word embeddings (depending on configuration)

---

### 4. Model Training
The model learns to map text features to sentiment classes.

Training includes:
- Splitting data into train/test sets
- Optimizing loss function
- Evaluating accuracy and class performance

---

### 5. Imbalanced Dataset Handling
Since positive reviews dominate e-commerce data:
- Class distribution is analyzed
- Techniques such as weighting or resampling are applied
- Model performance is evaluated per sentiment class

---

### 6. Result Export
Final predictions are saved back to:

result.csv  

This file can be used for further analysis or visualization.

---

## 📊 Output Example

"Great product!", 5, Positive  
"Average quality", 3, Neutral  
"Very disappointed", 1, Negative  

---

## 📖 Use Case

This project can be used for:
- Product sentiment monitoring
- Brand reputation analysis
- Customer feedback automation
- Market research insights
