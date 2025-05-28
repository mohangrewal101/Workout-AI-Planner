# main.py
# FastAPI entry point
# TODO: Remember to figure out how to private the OpenAI API key and other sensitive data

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.workout_ai import recommend_workouts
from app.data_loader import load_data
from app.data_loader import load_data
from app.description_generator import generate_description 

# Description cache
description_cache = {}

df, encoders = load_data("data/workout_data.csv")
    
app = FastAPI()

# Allow requests from your frontend (e.g., Vite dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body
class WorkoutRequest(BaseModel):
    muscle_group: str
    difficulty: str
    workout_type: str
    num_neighbors: int = 3
    weights: tuple = (3, 1, 2)  # Default weights for features

    
@app.get("/")
def read_root():
    return {"message": "Welcome to the Workout Recommendation API!"}

   
@app.post("/recommend_workouts/")
async def get_recommendations(request: WorkoutRequest):
    # Call the recommend_workouts function
    recommendations = recommend_workouts(
        df,
        encoders,
        request.muscle_group,
        request.difficulty,
        request.workout_type,
        num_neighbors=request.num_neighbors,
        weights=request.weights
    )
    
     # Add AI-generated descriptions
    for exercise in recommendations:
        exercise_name = exercise.get("exercise_name", "")
        if exercise_name:
            if exercise_name in description_cache:
                exercise["description"] = description_cache[exercise_name]
            else:
                desc = generate_description(exercise_name)
                description_cache[exercise_name] = desc
                exercise["description"] = desc
        else:
            exercise["description"] = "No name provided for description."

    return {"recommendations": recommendations}