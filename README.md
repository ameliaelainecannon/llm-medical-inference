# LLM Medical Inference

This self-study project provides Python scripts to automatically extract structured information from made-up/practice pathology reports using a large language model (LLM) via the `ollama` library. The scripts process text reports, apply a custom prompt template, and output JSON files containing inferred TNM staging and ICD codes.

## Features

- Reads `.txt` pathology reports from the `data/` folder.
- Uses a prompt template to instruct the LLM to output **only valid JSON**.
- Infers TNM staging and ICD codes even if not explicitly mentioned.
- Handles multiple tumors per report.
- Saves structured JSON outputs in the `outputs/` folder.
- Supports multiple malignancy report (`run_inference.py`) and single malignancy report (`single_run_inference.py`) processing.

## Folder Structure

```text
LLM-MEDICAL-INFERENCE/
│
├─ .venv/ # Python virtual environment
├─ config/ # Configuration files (optional)
├─ data/ # Input pathology reports (.txt)
├─ outputs/ # Generated JSON outputs
├─ prompts/
│ └─ pathology_extraction.txt # Prompt template for the LLM
├─ run_inference.py # Script for batch inference
├─ single_run_inference.py # Script for single report inference
├─ requirements.txt # Python dependencies
├─ README.md # Project documentation
└─ .gitignore
```

## Requirements

- Python 3.10+
- Use the virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
Install required packages inside the virtual environment:
```bash
pip install -r requirements.txt
```

## Usage
### Batch Inference
Activate your virtual environment:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
Place your pathology reports in the data/ folder as .txt files.
Customize the prompt in prompts/pathology_extraction.txt if needed.

Run the batch inference script:
```bash
python run_inference.py
```
JSON outputs will be saved in the outputs/ folder, named according to the input report files.

Single Report Inference
```bash
python single_run_inference.py --input data/example_report.txt --output outputs/example_report.json
```

## How It Works
1. The script reads .txt files from data/.
2. Inserts the report text into a prompt template (prompts/pathology_extraction.txt).
3. Sends the prompt to the LLM (codellama:7b) with a system message enforcing JSON-only output.
4. Parses the model response to extract JSON objects.
5. Handles single or multiple tumors per report.
6. Saves the resulting JSON to outputs/.

### Error Handling
If the model output is not valid JSON, an error message is printed along with the raw output.
The script continues processing other reports even if one fails.

### Notes
Ensure your LLM model (codellama:7b) is accessible via ollama.
Adjust temperature in options to control randomness (currently set to 0.0 for deterministic output).
The JSON structure depends on your prompt template and LLM instructions.