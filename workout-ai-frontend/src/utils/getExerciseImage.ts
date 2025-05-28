// This file contains utility functions to generate image paths for exercises.
// It includes a slugify helper function to format exercise names into a URL-friendly format.

export function slugify(text: string): string {
    return text
      .toLowerCase()
      .replace(/[^\w\s-]/g, "") // remove special characters
      .trim()
      .replace(/\s+/g, "-");
  }
  
  export function getExerciseImagePath(exerciseName: string): string {
    const slug = slugify(exerciseName);
    return `/exercise_images/${slug}.jpg`;
  }
  