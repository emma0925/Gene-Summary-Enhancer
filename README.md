# Connectome Gene Summary Enhancer Using Llama 2

## Introduction

The Connectome Gene Summary Enhancer is a specialized tool aimed at transforming the dense and note-like outputs from the Connectome database into coherent, easily readable paragraphs. Connectome's data, rich with genetic insights and findings from pubmed, often comes in a format that's challenging for quick consumption, as shown in gene-specific notes filled with technical details and references. By inputting gene IDs, this tool extracts these complex summaries and employs natural lanaguage processing, facilitated by Facebook's Llama 2, to restructure and refine the information into a narrative that's more accessible to researchers.

## Objective

The aim of this project is to enhance the comprehension and accessibility of genetic research data by converting the technical and note-formatted output from the Connectome database into reader-friendly paragraphs. These transformed summaries are intended to support the General Agricultural Intelligent Agent (GAIA) platform at the University of Toronto, facilitating the integration of complex genetic information into GAIA's agricultural and biological sciences knowledge base.

## Set Up & Installation
1. ssh to your **cedar.computecanada.ca** account
2. clone the github repo for llama2
   ```
   git clone https://github.com/meta-llama/llama
   ```
3. Follow the instruction for llama 2, visit the Meta website https://llama.meta.com/llama-downloads/ and register to download the **codellama 17b mode**
4. Clone this repo, move the scipt folder parallal to the `example_chat_completion.py`
   ```bash
   # Clone the repository
   git clone https://github.com/emma0925/Gene-Summary-Enhancer.git
   
   # Navigate to the project's scripts directory
   cd Gene-Symmary-Enhancer/scripts
   ```
## Example Use Case

**Input Text Summary from Connectome:**
"text_summary": "MEKK2 INTERACTS WITH CRCK3 (32165446). MEKK2 DEPENDS ON CRCK3 (32165446). MEKK2 STRUCTURALLY REGULATES CRCK3 (32165446). CRCK3 ENHANCES MEKK2-INDUCED CELL DEATH (32165446). CRCK3 DEPENDS ON SUMM2 (32165446). MDS1 RELATED TO CRCK3 (32497412). MDS1 PHOSPHORYLATES CRCK3 (32497412). SUMM2 MAINTAINS CRCK3 (32497412).",

**Outout from llama:**
"The gene AT2G11520, also known as MEKK2, interacts with CRCK3, a protein that is essential for cell death and is involved in various cellular processes, including cell signaling and protein synthesis. MEKK2 depends on CRCK3 for its proper functioning, and CRCK3 regulates MEKK2's structural properties. CRCK3 enhances MEKK2-induced cell death, and it is also dependent on SUMM2, a protein that is involved in various cellular processes, including cell signaling and protein synthesis. MDS1, a protein that is related to CRCK3, phosphorylates CRCK3, and SUMM2 maintains CRCK3. These findings suggest that CRCK3 plays a crucial role in regulating MEKK2 and its function in cell death."


## Features

### 1. Gene ID Input Cleaning:
Cleans a table of gene IDs that contains TAIR_OBJECT_ID to a gene id only txt files that does not contain any duplicates.
#### Process Overview

1. **Extraction of Gene IDs:** Initially, the process begins by reading through a raw input file to extract gene IDs of interest. This is achieved by identifying and isolating the precise parts of the data that correspond to gene IDs, while disregarding extraneous information.

2. **Edge Case Handling:** The procedure also involves a examination to capture and include gene IDs that might not follow the standard formatting (e.g., lacking a version number like `.1` or `.2`). These edge cases are essential to ensure no relevant gene ID is overlooked.

3. **Deduplication:** Finally, the process eliminates any duplicates within the extracted list of gene IDs. This step is crucial to maintain the integrity of the dataset, ensuring that each gene ID is represented uniquely.

#### Script Functions

- `extract_and_save_ids(input_file, output_file)`: Parses the raw input file to extract gene IDs and saves them to an output file. This function specifically targets IDs following a standard format with version numbers.

- `check_and_save_edge_cases(input_file, output_file)`: Identifies and preserves gene IDs that do not conform to the standard formatting, ensuring comprehensive coverage of all potential gene IDs in the dataset.

- `remove_duplicates(input_file, output_file)`: Scans the list of gene IDs for duplicates and retains only unique entries, thereby cleansing the dataset of any redundancies.

#### Execution
To run it, you might need to modify the file path in line 44 and 45 in clean_raw.py
```
input_file_path = '../gene_ids/raw_genes_id.txt' # Change it to your path of raw genes_id if needed
output_file_path = '../gene_ids/gene_ids_full.txt' # The output file name as you like
```
Then, you can run
```
python3 clean_raw.py
```
The cleaned gene_id list will be in the output_file_path that you modified. If you didn't miodify it, it will be in the current directory and name as "test_raw.txt".

### 2. Automated Data Extraction:
Utilizes Connectome endpoints to automatically retrieve detailed notes and publication information for specified genes that is suitable for compute canada environment.

#### Process Overview

1. **Batch Processing:** Gene IDs are divided into manageable batches to optimize the data retrieval process. This approach ensures that the extraction process is not too long (takes approximately 20 hour to process 5000 genes ID) and multiple gene_id outputs can be extracted at the same time. (Compute canda has multiple IP address, this can help to avoid IP ban)
   
2. **Parallel Execution:** Each batch of gene IDs is processed in parallel using Compute Canada's scheduling system, significantly reducing the overall time required for data extraction. It takes approximately 20 hour to process 5000 genes IDs. Also, Compute canda has different IP address, separating them to different jobs can avoid IP ban.

3. **Data Retrieval and Handling:** Detailed notes and publication information for each gene ID are fetched using a custom Python script. This script handles API communication, response validation, and data storage, ensuring that the extracted data is accurate and ready for subsequent processing.

#### Script Functions

- **Shell Script (`submit_all_batch.sh`):** Divides all gene IDs into different batches and prepares sbatch scripts for submission to Compute Canada's scheduling system. This script automates the setup for parallel data extraction, including the creation of necessary directories for organized storage of outputs.

- **Python Script (`generate_connectome_output.py`):** Fetches data for each gene ID by making requests to the Connectome API, processes the response to ensure data integrity, and saves the results in a structured JSON format. The script is designed to handle API rate limits gracefully and includes error handling to manage any issues that may arise during data retrieval.

#### Configuration and Usage

Users must update certain paths in the `submit_all_batch.sh` script to match their environment and project structure, including directories for the virtual environment, input and output data, and the Python script path.

#### Execution

To initiate the Automated Data Extraction process, follow these steps:

1. **Prepare the Gene ID List:** Use the output file generated from the 'Gene ID Input Cleaning' process as the input for this stage.

2. **Adjustions:** the batch size, job email recipient, output_directory

    In line 29 of the `submit_all_batch.sh`, change the email address for getting the job status (**Highly Recommended**)
    ```
    echo "#SBATCH --mail-user=<your_email>" >> "$sbatch_file" # Replace <your_email>
    ```
    You can remove this line if you don't want to get email of the job status.

    **Below are optiaonal:**
   
    If you want to change the batch size, it is in line 6 of the `submit_all_batch.sh`
    ```
    BATCH_SIZE=2500 # Changed the number to the number of genes you want to have in each batch
    ```
    Note: it takes around 20 hours to access the endpoint for 5000 genes

    If you want to change the output directory you can change line 8-15 of the `submit_all_batch.sh`
    ```
    OUTPUT_DIR="./outputs" # change line 10 if you changed here

    mkdir -p ./outputs #if you changed the output directory, make sure to change here
    mkdir -p ./gene_ids # the folder where the divided gene_ids txt file will be, make sure to change the next line too if you changed here

    # Split gene ID file into batches
    split -l $BATCH_SIZE "$GENE_ID_FILE" ./gene_ids/batch_ # ./gene_ids/batch_ is the default folder where the divided gene_ids txt file will be
    ```

4. **Run the Shell Script:** Execute the `batch_data_retrieval.sh` script. This will split the gene ID list into batches, create sbatch scripts for each batch, and submit them for processing.

    ```bash
    ./submit_all_batch.sh
    ```

3. **Monitor the Process:** Once submitted, the jobs will run independently on Compute Canada. The script outputs and data retrieval status can be monitored through Compute Canada's job management tools.

4. **Data Collection:** Upon completion, the extracted data will be available in the specified output directory(default: `./outputs`), organized by batch, and ready for further analysis or processing.
### 3. Summary Generation Process

#### Overview

Following data extraction, the script employs Llama2 to transform the dense connectome notes into coherent and comprehensive paragraphs. This process involves two key components:

- **Python Script (`generate_llama_summary.py`):** Reads the JSON-formatted connectome outputs, utilizes Llama2 to generate readable summaries for each gene, and exempts genes with summaries that are too long, potentially causing memory issues.

- **Shell Script (`get_llama_for_all.sh`):** Facilitates batch processing of connectome output directories, generating sbatch scripts for submission to Compute Canada's SLURM job scheduling system. This ensures efficient processing of each batch on the cluster.

#### Configuration and Usage

Users must update certain paths in the `get_llama_for_all.sh` script to match their environment and project structure, including directories for the virtual environment, input and output data, and the Python script path.

#### Execution

To initiate the Summary Generation Process, follow these steps:

1. **Prepare the Connectome Output Files**: Ensure that the connectome output files are in JSON format and the path of the directory is the same as the **Input Directory** variable (line 7) in the `get_llama_for_all.sh`. These files should be the result of the Automated Data Extraction process.

2. **Adjustments**:
   - **Job Email Recipient**: To receive job status notifications via email, find and modify the following line in your sbatch script template within `get_llama_for_all.sh`:
     ```bash
     echo "#SBATCH --mail-user=<your_email>" >> "$sbatch_file" # Replace <your_email> with your actual email address
     ```
     You may remove or comment out this line if you do not wish to receive email notifications.

   - **Output Directory**: If you want to change the directory where the slurm output files are saved, adjust the following line in `get_llama_for_all.sh`:
     ```bash
     OUTPUT_DIR="../outputs/slurm_out_files" # Example: Change this to your desired output directory path
     ```

3. **Run the Shell Script**:
   Execute the `get_llama_for_all.sh` script to start processing. This will:
   - Check for the existence of the exempt directory and create it if missing.
   - Loop through each batch of connectome outputs.
   - Create an sbatch script for each batch. These sbatch script will be using the `generate_llama_summary.py`
   - Submit each sbatch script for processing on Compute Canada.

   ```bash
   ./get_llama_for_all.sh

## License (To be determined)

## Acknowledgements

This repository was created by Jian Yun Zhuang (@emma0925), under the supervision of Professor Nicholas Provart(@nprovart) and with guidance from Vincent Lau(@vinlau) at the University of Toronto. The project benefits from their extensive knowledge, support, and insights in the field of bioinformatics and computer science. 

Special thanks are extended to Professor Marek Mutwil and his team at the Plants Systems Biology and Evolution Lab, Nanyang Technological University, for their development of the Plant Connectome endpoint. Their contributions to plant systems biology significantly enhance the capabilities of this tool by providing comprehensive data access and facilitating advanced gene analysis.

We are grateful for the contributions and mentorship from all parties involved throughout the development of this tool.


