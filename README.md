# Connectome Gene Summary Enhancer Using Llama 2

## Introduction

The Connectome Gene Summary Enhancer is a specialized tool aimed at transforming the dense and note-like outputs from the Connectome database into coherent, easily readable paragraphs. Connectome's data, rich with genetic insights and findings from pubmed, often comes in a format that's challenging for quick consumption, as shown in gene-specific notes filled with technical details and references. By inputting gene IDs, this tool extracts these complex summaries and employs natural lanaguage processing, facilitated by Facebook's Llama 2, to restructure and refine the information into a narrative that's more accessible to researchers.

## Objective

The aim of this project is to enhance the comprehension and accessibility of genetic research data by converting the technical and note-formatted output from the Connectome database into reader-friendly paragraphs. These transformed summaries are intended to support the General Agricultural Intelligent Agent (GAIA) platform at the University of Toronto, facilitating the integration of complex genetic information into GAIA's agricultural and biological sciences knowledge base.

## Installation (Draft)
1. Sign in to your cedar.computecanada.ca account
2. clone the github repo for llama2
   ```
   git clone https://github.com/meta-llama/llama
   ```
3. Follow the instruction for llama 2, visit the Meta website https://llama.meta.com/llama-downloads/ and register to download the codellama 17b mode
4. Clone this repo, move the scipt folder parallal to the `example_chat_completion.py`
   ```bash
   # Clone the repository
   git clone https://github.com/emma0925/Gene-Summary-Enhancer.git
   
   # Navigate to the project directory
   cd connectome-gene-summary-enhancer
   
   # Install the required dependencies
   pip install -r requirements.txt
   ```
## Prerequisites  (Draft)


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
input_file_path = 'raw_genes_id.txt' # Change it to your path of raw genes_id
output_file_path = 'test_raw.txt'    # The output file name as you like
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

