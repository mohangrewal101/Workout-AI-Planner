# tips_ai.py
# Uses AI to recommend workout tips based on user muscle groups

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, TransformerMixin
import joblib
import os

TRAINING_DATA_PATH = "data/tips_training_data.csv"
MODEL_FEATURES_PATH = "models/features.pkl"
MODEL_MODEL_PATH = "models/model.pkl"

# Custom transformer to vectorize muscle groups as multi-hot vector
class MuscleGroupEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.mlb = MultiLabelBinarizer(classes=["triceps", "biceps", "shoulders", "chest", "back", "legs"])
    def fit(self, X, y=None):
        # X is list of muscle_group lists
        self.mlb.fit(X)
        return self
    def transform(self, X):
        return self.mlb.transform(X)

# Combine tip text vectorizer and muscle group encoder into one feature set
class CombinedFeatures(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.text_vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1,2))
        self.muscle_encoder = MuscleGroupEncoder()
    def fit(self, X, y=None):
        tips = [x[0] for x in X]
        muscles = [x[1] for x in X]
        self.text_vectorizer.fit(tips)
        self.muscle_encoder.fit(muscles)
        return self
    def transform(self, X):
        tips = [x[0] for x in X]
        muscles = [x[1] for x in X]
        text_features = self.text_vectorizer.transform(tips)
        muscle_features = self.muscle_encoder.transform(muscles)
        # concatenate sparse and dense arrays horizontally
        from scipy.sparse import hstack
        return hstack([text_features, muscle_features])

# Load dataset CSV
def load_data(filepath):
    df = pd.read_csv(filepath)
    df['muscle_groups'] = df['muscle_groups'].str.split()
    X = list(zip(df['tip'], df['muscle_groups']))
    y = df['label']
    return X, y

def load_app_tips(filepath):
    df = pd.read_csv(filepath)
    df['muscle_groups'] = df['muscle_groups'].str.split()
    return df

# Train model
def train_model(X, y):
    features = CombinedFeatures()
    X_feat = features.fit_transform(X)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_feat, y)
    return features, model

# Predict relevance score for tip given user muscle groups
def predict_tip_relevance(features, model, tip_text, user_muscle_groups):
    X_test = [(tip_text, user_muscle_groups)]
    X_feat = features.transform(X_test)
    proba = model.predict_proba(X_feat)[:,1][0]
    return proba

# Load or train the model at import time (runs on startup of the app)
if os.path.exists(MODEL_FEATURES_PATH) and os.path.exists(MODEL_MODEL_PATH):
    features = joblib.load(MODEL_FEATURES_PATH)
    model = joblib.load(MODEL_MODEL_PATH)
else:
    print("Training tips model...")
    X_train, y_train = load_data(TRAINING_DATA_PATH)
    features, model = train_model(X_train, y_train)
    os.makedirs(os.path.dirname(MODEL_FEATURES_PATH), exist_ok=True)
    joblib.dump(features, MODEL_FEATURES_PATH)
    joblib.dump(model, MODEL_MODEL_PATH)
    print("Model trained and saved.")