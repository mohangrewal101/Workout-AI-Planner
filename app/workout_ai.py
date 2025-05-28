# workout_ai.py
# AI Logic for Workout Recommendations

import pandas as pd
import numpy as np
from scipy.spatial import distance
    
def recommend_workouts(df, encoders, muscle_group, difficulty, workout_type, num_neighbors=3, weights=(3, 1, 2)):
    try:
        muscle_encoded = encoders["muscle_group"].transform([muscle_group])[0]
        difficulty_encoded = encoders["difficulty"].transform([difficulty])[0]
        workout_type_encoded = encoders["workout_type"].transform([workout_type])[0]
    except ValueError as e:
        print(f"Unknown input value: {e}")
        return pd.DataFrame() # Return empty DataFrame if input is invalid/unknown
    
    input_data = np.array([muscle_encoded, difficulty_encoded, workout_type_encoded])

    distances = []
    for i, row in df.iterrows():
        row_vector = [
            row["muscle_group_encoded"],
            row["difficulty_encoded"],
            row["workout_type_encoded"]
        ]
        weighted_distance = distance.euclidean(
            [x * w for x, w in zip(input_data, weights)],
            [x * w for x, w in zip(row_vector, weights)]
        )
        distances.append((weighted_distance, i))

    distances.sort()
    nearest_indices = [i for _, i in distances[:num_neighbors]]

    result = df.iloc[nearest_indices][["exercise_name", "muscle_group", "difficulty", "workout_type"]]
    
    return result.to_dict(orient="records")

