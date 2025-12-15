import json
from pathlib import Path
import ollama

# Paths
data_dir = Path("data")
print(data_dir)
prompt_file = Path("prompts/pathology_extraction.txt")
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# Load prompt template
prompt_template = prompt_file.read_text()

# Iterate over all .txt reports in data folder
for report_path in data_dir.glob("*.txt"): #List files matching pattern
    print(data_dir.glob("*.txt").name())
    text = report_path.read_text() #gets the path of the file, reads it as a string, saves that string in "text"
    prompt = prompt_template.replace("{{TEXT}}", text) #replace TEXT in the prompt template with the example_report

    # Messages with system role to enforce JSON-only output
    messages = [
        {"role": "system", "content": "You are a medical assistant that outputs ONLY valid JSON. No explanations. Use medical reasoning to infer TNM staging and ICD codes when not explicitly stated."},
        {"role": "user", "content": prompt}
    ]

    # Run inference
    response = ollama.chat(
        model="codellama:7b",
        messages=messages,
        options={"temperature": 0.0}
    )

    output_text = response["message"]["content"]

    # Extract JSON safely
    try:
        start = output_text.find("{")
        end = output_text.rfind("}") + 1
        json_output = json.loads(output_text[start:end])
    except Exception as e:
        print(f"Error parsing JSON for {report_path.name}: {e}")
        print(f"the json error file:", json_output)
        continue

    # Save output
    output_file = output_dir / f"{report_path.stem}.json"
    with open(output_file, "w") as f:
        json.dump(json_output, f, indent=2)

    print(f"Inference complete for {report_path.name}. Saved to {output_file}")
