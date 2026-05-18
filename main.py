import pandas as pd

# Load dataset
df = pd.read_csv("FA-KES-Dataset.csv", encoding='latin1')

# Keep useful columns
df = df[['article_title', 'article_content', 'labels']]

# Remove missing values
df.dropna(inplace=True)

# Combine title + content
df['content'] = df['article_title'] + " " + df['article_content']

# Features and labels
X = df['content']
y = df['labels']

# Convert text into numbers
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

X_vectorized = vectorizer.fit_transform(X)

# Train/Test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

model.fit(X_train, y_train)

# Accuracy
from sklearn.metrics import accuracy_score

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

# Save model + vectorizer
import pickle

pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))

print("Model and vectorizer saved successfully.")