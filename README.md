# 🏋️‍♂️ Workout AI Planner

Workout AI Planner is a full-stack web app that intelligently recommends workouts tailored to your fitness goals. Whether you're a beginner or advanced lifter, this app curates exercises based on **muscle group**, **difficulty level**, and **workout type** (e.g., Hypertrophy or Strength). It also offers **AI-powered tips** to help you train more effectively.

This project was built to simplify fitness planning and personalize training recommendations using a combination of machine learning and user input.

---

## ❔ How to Use

List out the following:

- **Muscle Group:** Biceps, Triceps, Legs, Chest, Back, Shoulders (Must be one of these muscles and EXACTLY AS WRITTEN)

- **Difficulty Level:** Beginner, Intermediate, Advanced (Must be one of these levels and EXACTLY AS WRITTEN)

- **Workout Type:** Hypertrophy, Strength (Must be one of these types and EXACTLY AS WRITTEN)

Then click **Generate My Workout Plan** and ENJOY! 💪

---

## 🚀 Features

- 🎯 **Smart Workout Recommendations**  
  Get personalized workouts based on your inputs — just pure results.

- 🧠 **AI-Powered Training Tips**  
  Helpful insights tailored to your target muscle group, with the ability to cycle through tips.

- 📸 **Exercise Visuals**  
  Each workout is displayed with an accompanying image.

- ⚡ **Fast and Responsive UI**  
  Built with React and Tailwind CSS for a smooth user experience.

---

## 🛠️ Tech Stack

**Frontend:**  
- React + Vite
- Javascript  
- Tailwind CSS  
- Lucide Icons  
- Hosted on Vercel

**Backend:**  
- FastAPI  
- Python (pandas, scikit-learn)  
- Machine Learning: KNN-based recommender + Tip relevance ranker
- Hosted on Render

**Other:**  
- Exercise images downloaded through Google images 
- AI-generated tips and classes used for future GPT-based integrations for descriptions

---

## 📅 Planned Features

### Short-Term

- 🔢 Let users choose the number of exercises they want  
- 🎨 UI improvements and animations  
- 📸 Add more exercises with visual coverage
- 🛠️ Add more testing
- ❔ Add multiple muscle groups in one search

### Long-Term

- 👤 User accounts and saved preferences  
- 🗓️ Calendar system for tracking workouts  
- 🤖 Fully AI-generated workout descriptions  
- 🛠️ Ability to add custom exercises

---

## 💻 Running Locally

**Clone the repo:**

```bash
git clone https://github.com/mohangrewal101/Workout-AI-Planner.git
cd Workout-AI-Planner
```

**Backend Setup:**
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```
Be sure to look through errors to see you have all the requirements for the project!

📎 Project Purpose

This project showcases my skills across frontend and backend development, machine learning integration, and REST API architecture. I designed Workout AI Planner to help users make faster, smarter training decisions — and to demonstrate how AI can improve daily routines like fitness.

🔗 Live Demo

👉 https://workout-ai-planner-one.vercel.app

📬 Contact

Made by Mohan Grewal

Contact me on LinkedIn: https://www.linkedin.com/in/mohan-grewal-18605a211/






