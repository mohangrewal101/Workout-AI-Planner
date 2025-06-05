# main.py
# FastAPI entry point

from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.workout_ai import recommend_workouts
from app.data_loader import load_data

# Import your tips_ai functions
from app.tips_ai import load_app_tips, predict_tip_relevance, features, model


df, encoders = load_data("data/workout_data.csv")
# Load tips for app
df_tips = load_app_tips("data/tips_for_app.csv")
print("Loaded tips:", df_tips.shape) 
    
app = FastAPI()

# Allow your frontend origin
origins = [
    "https://workout-ai-planner-one.vercel.app",
    "http://localhost:5173"  # for local dev
]

# Allow requests from your frontend (e.g., Vite dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for WorkoutRequest POST body
class WorkoutRequest(BaseModel):
    muscle_group: str
    difficulty: str
    workout_type: str
    num_neighbors: int = 3
    weights: tuple = (3, 1, 2)  # Default weights for features
    
# Pydantic model for TipRequest POST body
class TipRequest(BaseModel):
    muscle_group: str
    tip_index: int

    
@app.get("/")
def read_root():
    return {"message": "Welcome to the Workout Recommendation API!"}

@app.post("/next_tip/")
async def next_tip(request: TipRequest):
    user_muscles = [request.muscle_group]
    sorted_tips = get_sorted_tips(user_muscles)
    
    if not sorted_tips:
        return {
            "tip": "No tips available.",
            "tip_index": 0
        }
        
    next_index = (request.tip_index + 1) % len(sorted_tips)
    next_tip_text = sorted_tips[next_index]
    
    return {
        "tip": next_tip_text,
        "tip_index": next_index
    }
   
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
    
    # Get tips list
    user_muscles = [request.muscle_group]
    sorted_tips = get_sorted_tips(user_muscles)
    first_tip = sorted_tips[0] if sorted_tips else "No tips available."

    return {
        "recommendations": recommendations,
        "tip": first_tip,
        "tip_index": 0  # to track current tip for cycling
    }

# Helper: Get sorted tips based on user muscle groups
def get_sorted_tips(user_muscles):
    user_muscles = [m.lower() for m in user_muscles]
    
    filtered = df_tips[df_tips['muscle_groups'].apply(
        lambda mg: any(m in parse_groups(mg) for m in user_muscles)
    )]
    print("Filtered tips:", len(filtered))
    scored_tips = []
    for _, row in filtered.iterrows():
        score = predict_tip_relevance(features, model, row['tip_text'], user_muscles)
        scored_tips.append((score, row['tip_text']))
    
    scored_tips.sort(reverse=True)
    return [tip for score, tip in scored_tips]

# Helper function to parse muscle groups from string or list
def parse_groups(mg):
    if isinstance(mg, str):
        return [m.strip().lower() for m in mg.split()]
    elif isinstance(mg, list):
        return [m.strip().lower() for m in mg]
    else:
        return []
