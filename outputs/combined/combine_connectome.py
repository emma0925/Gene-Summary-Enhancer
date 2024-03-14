import json
import os

def merge_json_files(folder_path):
    combined_dict = {}
    
    # List all files in the given folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)
            
            # Open and read the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Merge the current dictionary with the combined dictionary
                combined_dict.update(data)
    
    # Write the combined dictionary to a new JSON file
    with open('combined_connectome.json', 'w') as combined_file:
        json.dump(combined_dict, combined_file, indent=4)

# Replace '/path/to/your/json_folder' with the actual path to your folder of JSON files
merge_json_files('../connectome_outputs')
