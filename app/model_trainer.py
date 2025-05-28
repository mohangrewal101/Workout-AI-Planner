# model_trainer.py
# This script trains a language model to generate detailed descriptions for exercises.

from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
from transformers import pipeline
import os

# Define model and tokenizer
model_name = "distilgpt2"  # Starting with a small, efficient model
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load the dataset (high-quality descriptions)
data_path = "../data/workout_descriptions.txt"
assert os.path.exists(data_path), "Dataset file not found. Please ensure the file is in the 'data' directory."

# Prepare the dataset for training
train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=data_path,
        block_size=128
    )
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Set up training arguments
training_args = TrainingArguments(
    output_dir="./models/exercise_description_model",
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=4,
    save_steps=1000,
    save_total_limit=2,
    logging_steps=200,
)

# Set up the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset
)

# Train the model
trainer.train()

# Save the trained model
trainer.save_model("./models/exercise_description_model")