def extract_and_save_ids(input_file, output_file):
    """
    Reads raw gene IDs from the input_file, extracts the part of interest(the actual gene ids),
    and saves it to the output_file.
    """
    with open(input_file, 'r') as infile:
        # Read lines and split to extract the needed part
        extracted_ids = []
        for line in infile.readlines():
            if len(line.split()[1].split('.')) == 2 and line.split()[1].split('.')[1] ==  '1':
                extracted_ids.append(line.split()[1].split('.')[0])

    with open(output_file, 'w') as outfile:
        # Join the extracted IDs with a newline and write to the output file
        outfile.write("\n".join(extracted_ids))

def check_and_save_edge_cases(input_file, output_file):
    """
    Reads raw gene IDs from the input_file, extracts gene ids that does not have .1 .2 ...
    If its not saved, saved to the output file. 
    """
    with open(input_file, 'r') as infile:
        extracted_ids  = []
        for line in infile.readlines():
            if (line.split()[1].find('.') == -1 ) :
                extracted_ids.append(line.split()[1])
    with open(output_file, 'r+') as outfile:
        existing_ids = [line.strip() for line in outfile.readlines()]  # Read and strip lines
        for i in extracted_ids:
            if i not in existing_ids:  # Check if ID is not in existing_ids
                outfile.write(i + '\n')

def remove_duplicates(input_file, output_file):
    # Read the input file and remove duplicates by converting to a set
    with open(input_file, 'r') as file:
        unique_lines = set(file.readlines())

    # Write the unique lines back to a new file
    with open(output_file, 'w') as file:
        for line in sorted(unique_lines):
            file.write(line)

# Specify the path to your input and output files
input_file_path = 'raw_genes_id.txt'
output_file_path = 'test_raw.txt'

# Call the function with the file paths
extract_and_save_ids(input_file_path, output_file_path)
check_and_save_edge_cases(input_file_path, output_file_path)
remove_duplicates(output_file_path, output_file_path) #Remove all possible duplicates, there are duplicates in the first step, e.g .1 are not distinct

print(f"IDs have been extracted and saved to {output_file_path}")