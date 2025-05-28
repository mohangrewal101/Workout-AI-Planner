# tips_ai.py
# Uses AI to recommend workout tips based on user muscle groups

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

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

# Pre-filter by checking overlap
def filter_tips_by_muscle_group(tips, user_muscles):
    def matches(tip_muscles):
        return any(m in tip_muscles for m in user_muscles)
    return [tip for tip in tips if matches(tip[1])]

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

if __name__ == "__main__":
    # Step 1: Load and train on the training dataset
    X_train, y_train = load_data("../data/tips_training_data.csv")
    features, model = train_model(X_train, y_train)

    # Step 2: Load tips for testing (app use case)
    df_app = load_app_tips("../data/tips_for_app.csv")

    # Step 3: Define your target muscle group(s)
    user_muscles = ["legs"]  # You can change this dynamically

    # Step 4: Filter for relevant muscle groups
    filtered = df_app[df_app['muscle_groups'].apply(lambda mg: any(m in mg for m in user_muscles))]

    # Step 5: Score and sort tips using the model
    scored_tips = []
    for _, row in filtered.iterrows():
        score = predict_tip_relevance(features, model, row['tip_text'], user_muscles)
        scored_tips.append((score, row['tip_text']))

    scored_tips.sort(reverse=True)

    # Step 6: Display top tips
    print("\nTop Recommended Tips:")
    for score, tip in scored_tips[:10]:
        print(f"Score: {score:.3f} | Tip: {tip}")
