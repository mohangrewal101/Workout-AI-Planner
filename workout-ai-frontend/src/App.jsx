import { useState } from 'react'
import "./index.css";
import './App.css';
import { getExerciseImagePath } from './utils/getExerciseImage';



function App() {
  const [formData, setFormData] = useState({
    muscle_group:"",
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
      alert("Please fill out all fields.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/recommend_workouts/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      console.log("Raw Recommendations:", data);

      // Fetch images from ExerciseDB
      const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

      const recommendationsWithImages = data.recommendations.map((rec) => {
        const imageUrl = getExerciseImagePath(rec.exercise_name);
        return { ...rec, imageUrl };
      });
      console.log("Recommendations with images:", recommendationsWithImages);

      // Set the recommendations and current tip
      setRecommendations(recommendationsWithImages);
      setCurrentTip(data.tip);
      setTipIndex(data.tip_index);

    } catch (err) {
      console.error("Error fetching recommendations:", err);
    }
  };

  const getNextTip = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/next_tip/", {
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
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md w-full">
        <h1 className="text-2xl font-bold mb-6 text-center">Workout Recommender</h1>

        <div className="space-y-4">
          <input
            className="w-full p-2 border rounded"
            placeholder="Muscle Group"
            name="muscle_group"
            onChange={handleChange}
          />
          <input
            className="w-full p-2 border rounded"
            placeholder="Difficulty"
            name="difficulty"
            onChange={handleChange}
          />
          <input
            className="w-full p-2 border rounded"
            placeholder="Workout Type"
            name="workout_type"
            onChange={handleChange}
          />
          <button
            onClick={getRecommendations}
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          >
            Get Recommendations
          </button>
        </div>

        {recommendations.length > 0 && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-2">Recommendations:</h2>
            <ul className="list-disc pl-5 space-y-1">
              {recommendations.map((rec, index) => (
                <li key={index} className="p-4 bg-gray-50 rounded shadow">
                  <div className="text-lg font-bold text-black">{rec.exercise_name}</div>
                  <div className="text-sm text-gray-700">
                    Muscle: {rec.muscle_group} • Difficulty: {rec.difficulty} • Type: {rec.workout_type}
                  </div>
                  <img
                    src={rec.imageUrl}
                    alt={rec.exercise_name}
                    className="mt-2 rounded w-full h-48 object-cover"
                  />
                </li>
              ))}
            </ul>
          </div>
        )}

        {currentTip && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-2"> Tip:</h2>
            <div className="p-4 bg-yellow-100 rounded text-gray-900">{currentTip}</div>
            <button
              onClick={getNextTip}
              className="mt-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Next Tip
            </button>
          </div>
        )}
      </div>
    </div>
  );
}


export default App;