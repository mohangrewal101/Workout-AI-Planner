import { useState } from 'react';
import './index.css';
import './App.css';
import { getExerciseImagePath } from './utils/getExerciseImage';
import { Dumbbell } from 'lucide-react';

function App() {
  const [formData, setFormData] = useState({
    muscle_group: "",
    difficulty: "",
    workout_type: "",
  });

  const [recommendations, setRecommendations] = useState([]);
  const [currentTip, setCurrentTip] = useState("");
  const [tipIndex, setTipIndex] = useState(0);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const getRecommendations = async () => {
    const { muscle_group, difficulty, workout_type } = formData;
    if (!muscle_group || !difficulty || !workout_type) {
      alert("🔥 Please complete all workout criteria before proceeding!");
      return;
    }

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/recommend_workouts/`,{
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      const recommendationsWithImages = data.recommendations.map((rec) => ({
        ...rec,
        imageUrl: getExerciseImagePath(rec.exercise_name),
      }));

      setRecommendations(recommendationsWithImages);
      setCurrentTip(data.tip);
      setTipIndex(data.tip_index);

    } catch (err) {
      console.error("Error fetching recommendations:", err);
    }
  };

  const getNextTip = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/next_tip/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          muscle_group: formData.muscle_group,
          tip_index: tipIndex + 1,
        }),
      });

      const data = await response.json();
      setCurrentTip(data.tip);
      setTipIndex(data.tip_index);
    } catch (err) {
      console.error("Error fetching next tip:", err);
    }
  };

  return (
    <div className="relative min-h-screen text-white font-sans">
      {/* Fixed background image */}
      <div
        className="fixed top-0 left-0 w-full h-full bg-cover bg-center -z-10"
        style={{ backgroundImage: `url('/ui_background_images/gym-background.jpg')` }}
      />
  
      {/* Dark overlay */}
      <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-70 -z-10" />
  
      {/* Page content */}
      <div className="relative z-10 flex justify-center items-start py-12 px-4 min-h-screen">
        <div className="bg-neutral-900 p-8 rounded-3xl shadow-2xl w-full max-w-3xl">
          <div className="text-4xl font-extrabold tracking-wide text-red-600 flex items-center justify-center mb-8 font-['Anton']">
            <Dumbbell className="mr-3" size={36} /> PowerUp Workout Planner
          </div>
  
          {/* Inputs */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <input
              className="p-4 rounded-lg bg-gray-800 placeholder-gray-400 text-white text-lg font-semibold"
              placeholder="Target Muscle Group (e.g., Chest, Legs)"
              name="muscle_group"
              onChange={handleChange}
              spellCheck={false}
            />
            <input
              className="p-4 rounded-lg bg-gray-800 placeholder-gray-400 text-white text-lg font-semibold"
              placeholder="Workout Difficulty (Beginner, Intermediate, Advanced)"
              name="difficulty"
              onChange={handleChange}
              spellCheck={false}
            />
            <input
              className="p-4 rounded-lg bg-gray-800 placeholder-gray-400 text-white text-lg font-semibold"
              placeholder="Workout Type (Strength, Cardio, HIIT)"
              name="workout_type"
              onChange={handleChange}
              spellCheck={false}
            />
          </div>
  
          <button
            onClick={getRecommendations}
            className="w-full bg-red-700 hover:bg-red-800 text-white font-bold text-xl py-4 rounded-2xl transition-all duration-300 tracking-wider"
          >
            Generate My Workout Plan
          </button>
  
          {/* Recommendations */}
          {recommendations.length > 0 && (
            <div className="mt-10">
              <h2 className="text-3xl font-bold mb-5 border-b-4 border-red-600 pb-2 font-['Montserrat']">
                Your Custom Workout Routine
              </h2>
              <ul className="space-y-6">
                {recommendations.map((rec, index) => (
                  <li key={index} className="bg-gray-900 rounded-2xl p-6 shadow-lg">
                    <div className="text-2xl font-semibold text-red-500 mb-1 tracking-tight font-['Poppins']">
                      {rec.exercise_name}
                    </div>
                    <div className="text-sm text-gray-300 mb-3 italic">
                      Muscle Group: {rec.muscle_group} • Level: {rec.difficulty} • Mode: {rec.workout_type}
                    </div>
                    <div className="w-full h-80 flex justify-center items-center bg-gray-200 rounded-2xl overflow-hidden">
                      <img
                        src={rec.imageUrl}
                        alt={rec.exercise_name}
                        className="object-contain w-full h-full"
                      />
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
  
          {/* Tips */}
          {currentTip && (
            <div className="mt-10">
              <h2 className="text-3xl font-bold mb-3 border-b-4 border-yellow-400 pb-2 font-['Montserrat'] flex items-center gap-2">
                💪 Pro Tips For Maximizing Gains
              </h2>
              <div className="p-5 bg-yellow-200 text-black rounded-xl shadow-md text-base font-medium leading-relaxed font-['Open_Sans']">
                {currentTip}
              </div>
              <button
                onClick={getNextTip}
                className="mt-5 bg-red-600 hover:bg-red-700 text-white px-5 py-3 rounded-xl text-lg font-semibold tracking-wide transition-colors duration-300"
              >
                Next Tip
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
