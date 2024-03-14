import requests
import json
import time
import random
import argparse

# Function to write a single dictionary to an already open file as a JSON object.
def write_to_json(file, data):
    """
    Writes a dictionary to an already open file as a JSON object.

    :file: File object to write the data into.
    :data: Dictionary to be written to the file.
    """
    json_string = json.dumps(data)
    file.write(json_string + '\n')

def is_response_empty(response_data):
    """
    Checks if the response data is empty based on specific fields.

    :response_data: Dictionary representing the JSON response.
    :return: Boolean indicating whether the data is considered empty.
    """
    empty_structure = {"abbreviations": {}, "cytoscape_elements": [], "functional_annotations": {}, "publications": [], "text_summary": ""}
    return response_data == empty_structure


def save_connectome_output(api_url, gene_id_file, output_file):
    with open(gene_id_file, 'r') as file:
        gene_ids = file.readlines()
    
    with open(output_file, 'w') as output_file:
        output_file.write('[')
        first_entry = True

        for gene_id in gene_ids:
            try:
                full_url = api_url + gene_id.strip()
                response = requests.get(full_url)
                time.sleep(random.uniform(1, 5))

                if response.status_code == 200:
                    response_json = response.json()
                    
                    if not is_response_empty(response_json):
                        response_json["gene_id"] = gene_id.strip()
                        print("Success gene ID: " +  gene_id)
                        if not first_entry:
                            output_file.write(',')
                        else:
                            first_entry = False

                        write_to_json(output_file, response_json)
                else:
                    print(f"Failed to retrieve data for gene ID: {gene_id.strip()}\n")
            except Exception as e:
                print("Request Failed!!!"+gene_id)
        output_file.write(']')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch gene data and save to a JSON file.")
    parser.add_argument("api_url", help="API URL")
    parser.add_argument("gene_id_file", help="File path for the gene IDs")
    parser.add_argument("output_file", help="File path for the output JSON")
    
    args = parser.parse_args()
    save_connectome_output(args.api_url, args.gene_id_file, args.output_file)
