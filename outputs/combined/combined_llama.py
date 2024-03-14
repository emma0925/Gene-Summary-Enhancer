import os

def extract_and_combine_sections(folder_path, output_file_name):
    all_sections = []  # Store all extracted sections

    # Iterate over each file in the given folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.out'):
            file_path = os.path.join(folder_path, filename)

            # Open and read the file
            with open(file_path, 'r') as file:
                user_count = 0  # Track "User:" occurrences
                section = []
                capture_section = False  # Flag to start capturing lines

                # Read the file line by line
                for line in file:
                    if '==================================' in line.strip():
                        if capture_section and not 'References:' in ''.join(section):  # End of a relevant section
                            all_sections.append(''.join(section))  # Add the complete section
                            section = []  # Reset for the next section
                        user_count = 0  # Reset "User:" count
                        capture_section = False  # Reset capture flag until next relevant section
                    elif 'User:' in line:
                        user_count += 1
                        if user_count == 2:  # Start capturing from the second "User:"
                            capture_section = True
                            section = [line]  # Start new section
                        elif user_count > 2:
                            section.append(line)  # Append subsequent lines
                    elif capture_section:  # Inside a section to be captured
                        section.append(line)

                if capture_section and section:  # Ensure the last section in file is added
                    all_sections.append(''.join(section))

    # Write all extracted sections to the specified output file
    with open(output_file_name, 'w') as output_file:
        output_file.write('\n==================================\n'.join(all_sections))


# Specify the name of the output file where all sections will be saved
extract_and_combine_sections('../llama_outputs', 'combined_llama.out')
