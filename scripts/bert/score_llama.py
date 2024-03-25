import csv
import json
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def evaluate_paragraph(paragraph, hypothesis):
    model_name = "microsoft/deberta-xlarge-mnli"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    inputs = tokenizer(paragraph, hypothesis, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)

    scores = outputs.logits
    probabilities = torch.softmax(scores, dim=1)
    return probabilities

def process_csv_and_json(csv_file, json_file, output_json_file):
    with open(json_file, 'r') as jf:
        json_data = json.load(jf)

    results = {}

    with open(csv_file, 'r') as cf:
        reader = csv.reader(cf)
        next(reader)  # Assuming the first row is a header
        for row in reader:
            gene_id = row[0]
            paragraph = row[1]
            
            # Check if gene_id exists in the JSON data
            if gene_id in json_data and 'text_summary' in json_data[gene_id]:
                hypothesis = json_data[gene_id]['text_summary']
                probabilities = evaluate_paragraph(paragraph, hypothesis)
                
                # Convert tensor to list for JSON serialization
                prob_list = probabilities.tolist()
                
                # Save the probabilities list for each gene_id
                print(gene_id)
                results[gene_id] = prob_list

    # Save results to a JSON file
    with open(output_json_file, 'w') as of:
        json.dump(results, of, indent=4)

# Example usage
csv_file = 'genes_content_small.csv'
json_file = 'combined_connectome.json'
output_json_file = './scoring_results_small.json'
evaluation_results = process_csv_and_json(csv_file, json_file, output_json_file)
