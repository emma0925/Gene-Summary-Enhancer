import glob

# Assuming all your text files are in the folder 'path/to/your/folder' and have a '.txt' extension
file_paths = glob.glob('/home/emma0925/scratch/new_llama/codellama/final_final_run/llama_outputs/exempt_genes/*.txt')
combined_content = ""

for file_path in file_paths:
    with open(file_path, 'r') as file:
        content = file.readline().strip()  # Reads the single line and removes any leading/trailing whitespace
        # Splits the line at each 'AT', filters out any empty strings, and then rejoins them with 'AT' at the start and '\n' between IDs
        processed_content = '\n'.join(['AT' + part for part in content.split('AT') if part])
        combined_content += processed_content + "\n"  # Adds a newline to separate content from different files

# Remove the last unnecessary newline
combined_content = combined_content.rstrip()

# Writing the processed content to a new file
with open('../outputs/combined_exempt.txt', 'w') as combined_file:
    combined_file.write(combined_content)

print("Done. The IDs have been combined and processed into combined.txt.")