# description_generator.py
# Generate detailed descriptions for exercises using a pre-trained model

import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), "models", "exercise_description_model")
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True, use_safetensors=True)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

def clean_description(text: str) -> str:
    # Deduplicate lines and normalize spacing
    seen = set()
    cleaned = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped and stripped not in seen:
            cleaned.append(stripped)
            seen.add(stripped)
    return "\n".join(cleaned)

def is_valid_output(output: str) -> bool:
    # Check if all required sections are present
    required_sections = [
        "Muscles Targeted:", 
        "Step-by-Step Instructions:", 
        "Key Form Tips:", 
        "Common Mistakes:", 
        "Breathing and Tempo:"
    ]
    return all(section in output for section in required_sections)

def generate_description(exercise_name: str) -> str:
    # Structured and anchored prompt
    prompt = (
        f"### Exercise: {exercise_name}\n"
    f"Muscles Targeted:\n- \n\n"
    "Step-by-Step Instructions:\n"
    "1. \n2. \n3. \n\n"
    "Key Form Tips:\n- \n\n"
    "Common Mistakes:\n- \n\n"
    "Breathing and Tempo:\n- \n\n"
    "End of description."
    )

    try:
        result = generator(
            prompt,
            max_length=250,
            temperature=0.5,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            truncation=True,
            pad_token_id=tokenizer.eos_token_id
        )
        raw_output = result[0]['generated_text'].replace(prompt, "").strip()
        final_output = clean_description(raw_output)

        if not is_valid_output(final_output):
            return f"[Warning] Incomplete description generated for {exercise_name}. Output:\n\n{final_output}"

        print(f"Generated description for {exercise_name}:\n{final_output}\n")
        return final_output

    except Exception as e:
        return f"[Error] Failed to generate description for {exercise_name}: {str(e)}"
