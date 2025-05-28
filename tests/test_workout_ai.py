# test_workout_ai.py
# Test cases for the workout recommendation system

import pandas as pd
import pytest
from app.workout_ai import recommend_workouts
from app.data_loader import load_data

@pytest.fixture(scope="module")
def workout_data():
    df, encoders = load_data("data/workout_data.csv")
    return df, encoders

# Ensure that exact matches are returned in the recommendations
def test_exact_match(workout_data):
    df, encoders = workout_data
    result = recommend_workouts(df, encoders, "Chest", "Beginner", "Strength", num_neighbors=3)
    
    exercise_names = result["exercise_name"].tolist()
    assert "Cable Pec Deck" in exercise_names

# Ensure that the number of recommendations is correct
def test_number_of_recommendations(workout_data):
    df, encoders = workout_data
    result = recommend_workouts(df, encoders, "Chest", "Beginner", "Strength", num_neighbors=5)
    
    assert len(result) == 5
    

# Ensure that no crash on unknown input
def test_unknown_input(workout_data):
    df, encoders = workout_data
    result = recommend_workouts(df, encoders, "Unknown", "Unknown", "Unknown", num_neighbors=3)
    
    assert result.empty  # Expecting an empty DataFrame as output for unknown input
    
# Ensure that the function handles partial matches correctly (when there is no exact match)
def test_partial_match_with_knn(workout_data):
    df, encoders = workout_data
    result = recommend_workouts(df, encoders, "Shoulders", "Intermediate", "Strength", num_neighbors=3)
    
    # Check if the recommended exercises are similar to the input
    assert not result.empty  # Ensure that we get some recommendations
    assert len(result) == 3
    
    
# Ensure that all the exercises have an exercise name and are not null
def test_output_exercise_name_not_null(workout_data):
    df, encoders = workout_data
    result = recommend_workouts(df, encoders, "Legs", "Beginner", "Hypertrophy", num_neighbors=5)
    assert not result.empty
    assert result["exercise_name"].notnull().all()
