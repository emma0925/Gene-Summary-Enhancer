import csv

def extract_data_and_write_csv(input_file, output_csv):

    with open(input_file, 'r') as infile:
        # Read the entire content of the file
        content = infile.read()
        
    # Split the content by the '==================================' separator
    sections = content.split('==================================')
    
    # Prepare data for CSV
    data_for_csv = []
    for section in sections:
        if section.strip():  # Ensure the section is not empty
            # Find the gene ID and content
            start_idx = section.find('User: Please convert the following notes about the gene')
            if start_idx != -1:
                # Extract the gene ID
                gene_id_start = start_idx + len('User: Please convert the following notes about the gene ')
                gene_id_end = gene_id_start +9
                gene_id = section[gene_id_start:gene_id_end].strip()
                
                # Extract the content
                content_start_idx = section.find('> Assistant:') + len('> Assistant:')
                content = section[content_start_idx:].strip().replace('\n', ' ')
                
                # Append the extracted data to the list
                data_for_csv.append([gene_id, content])
            else:
                # For sections without a gene ID in the specific format
                content = section.strip().replace('\n', ' ')
                data_for_csv.append(["", content])
    
    # Write data to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Gene ID', 'Content'])
        # Write data rows
        writer.writerows(data_for_csv)

# Replace 'input_file.out' with the path to your .out file
# Specify the name of the CSV file you want to create
extract_data_and_write_csv('./combined_llama.out', 'genes_content.csv')
