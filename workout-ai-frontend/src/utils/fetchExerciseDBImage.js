// fetchExerciseDBImage.js
// This function fetches an exercise image from the ExerciseDB API using the exercise name.
let cachedExercises = [];

function normalizeName(name) {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]/gi, '') // remove special characters/spaces
      .trim();
  }


export async function fetchExerciseDBImage(exerciseName) {
  if (cachedExercises.length === 0) {
    try {
      const res = await fetch("https://exercisedb.p.rapidapi.com/exercises", {
        method: "GET",
        headers: {
          "X-RapidAPI-Key": import.meta.env.VITE_RAPIDAPI_KEY,
          "X-RapidAPI-Host": "exercisedb.p.rapidapi.com",
        },
      });
      const data = await res.json();
      cachedExercises = data;
    } catch (err) {
      console.error("Error fetching ExerciseDB data:", err);
      return null;
    }
  }

  const normalizedInput = normalizeName(exerciseName);

   // Exact match (normalized)
   let match = cachedExercises.find(
    (ex) => normalizeName(ex.name) === normalizedInput
  );

  // Fuzzy match (normalized)
  if (!match) {
    match = cachedExercises.find((ex) =>
      normalizeName(ex.name).includes(normalizedInput)
    );
  }

  return match?.gifUrl || null;
}
