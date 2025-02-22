import os
import json
from data import write_jsonl, read_problems
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from config import MODIFIED_MODEL_PATH, BASE_GENERATED_CODE_OUTPUT_PATH, HUMANEVAL_DATA_PATH

# GPU-Nutzung optimieren
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Liste aller Modellpfade
model_paths = MODIFIED_MODEL_PATH

# HumanEval-Aufgaben laden
problems = read_problems(HUMANEVAL_DATA_PATH)

# Durchlaufe alle Modellpfade
for model_path in model_paths:
    print(f"\n Starte Generierung mit Modell: {model_path}")

    # Modell und Tokenizer laden
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch_dtype,
        device_map="auto"
    )

    # Funktion zur Generierung einer Lösung mit dem LLM
    def generate_completion(prompt):
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_length=512,
                temperature=0.2,
                top_p=0.95,
                do_sample=True
            )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    samples = []
    for task_id, problem in problems.items():
        prompt = problem["prompt"]
        print(f" Processing task: {task_id} mit {model_path}")

        # LLM generiert den Code
        completion = generate_completion(prompt)

        # Speichere den Code als Sample
        samples.append({"task_id": task_id, "completion": completion})

    # Speichere Ergebnisse mit entsprechendem Dateinamen
    round_name = model_path.split("/")[-2]  # "round_X"
    percent_name = model_path.split("/")[-3]  # "CodeLlama0Percent", etc.
    output_file = f"{BASE_GENERATED_CODE_OUTPUT_PATH}human-eval/generated_code_used_for_analysis/samples_{percent_name}_{round_name}.jsonl"
    
    write_jsonl(output_file, samples)
    print(f" Ergebnisse gespeichert: {output_file}")
