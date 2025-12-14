import json
from pathlib import Path
import ollama

# Load input text
text = Path("data/example_report.txt").read_text()

# Load prompt template
prompt_template = Path("prompts/pathology_extraction.txt").read_text()
prompt = prompt_template.replace("{{TEXT}}", text)

# Run inference
response = ollama.chat(
    model="codellama:7b",
    messages=[{"role": "user", "content": prompt}],
    options={"temperature": 0.0}
)

output_text = response["message"]["content"]

# Extract JSON safely
start = output_text.find("{")
end = output_text.rfind("}") + 1
json_output = json.loads(output_text[start:end])

# Save output
Path("outputs").mkdir(exist_ok=True)
with open("outputs/example_report.json", "w") as f:
    json.dump(json_output, f, indent=2)

print("Inference complete. Output saved to outputs/example_report.json")
