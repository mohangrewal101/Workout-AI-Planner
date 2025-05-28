# data_loader.py
# Loads and encodes the workout data

import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def preprocess_data(df):
    encoders = {}
    scaler = MinMaxScaler()
    
    for column in ["muscle_group", "difficulty", "workout_type"]:
        encoder = LabelEncoder()
        df[column + "_encoded"] = encoder.fit_transform(df[column])
        encoders[column] = encoder
        
    # Scale the features to [0, 1] range so we can add weight
    features = df[["muscle_group_encoded", "difficulty_encoded", "workout_type_encoded"]]
    features_scaled = scaler.fit_transform(features)
    
    # Add scaled features to DataFrame for tracking
    df_scaled = df.copy()
    df_scaled[["muscle_group_scaled", "difficulty_scaled", "workout_type_scaled"]] = features_scaled
    
    return df_scaled, encoders

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return preprocess_data(df)
