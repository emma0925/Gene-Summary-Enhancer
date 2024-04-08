# Connectome Gene Summary Enhancer Using Llama 2

## Introduction

The Connectome Gene Summary Enhancer is a specialized tool aimed at transforming the dense and note-like outputs from the Connectome database into coherent, easily readable paragraphs. Connectome's data, rich with genetic insights and findings from pubmed, often comes in a format that's challenging for quick consumption, as shown in gene-specific notes filled with technical details and references. By inputting gene IDs, this tool extracts these complex summaries and employs natural lanaguage processing, facilitated by Facebook's Llama 2, to restructure and refine the information into a narrative that's more accessible to researchers.

## Objective

The aim of this project is to enhance the comprehension and accessibility of genetic research data by converting the technical and note-formatted output from the Connectome database into reader-friendly paragraphs. These transformed summaries are intended to support the General Agricultural Intelligent Agent (GAIA) platform at the University of Toronto, facilitating the integration of complex genetic information into GAIA's agricultural and biological sciences knowledge base.

## Example Use Case

**Input Text Summary from Connectome:**
"text_summary": "NAD-ME1 AFFECTS PLANT METABOLISM (33523525). NAD-ME1 LOCALIZES TO MET.II.15 QTL (33523525). NAD-ME1 INTERACTS WITH CIRCADIAN CIS-ELEMENT BINDING SITE (33523525). NAD-ME1 ENHANCES TRICARBOXYLIC ACID CYCLE INTERMEDIATES (33523525). NAD-ME1 REPRESSES GSL BIOSYNTHESIS PATHWAY GENES (33523525). NAD-ME1 PRODUCES PRIMARY AND SECONDARY METABOLITES (33523525)."<br>

**Outout from llama:**
The gene AT2G13560, also known as NAD-ME1, plays a crucial role in plant metabolism. Studies have shown that NAD-ME1 localizes to the metabolic pathway II.15 QTL (PubMed ID: 33523525) and interacts with the circadian cis-element binding site (PubMed ID: 33523525). NAD-ME1 enhances the production of tricarboxylic acid cycle intermediates (PubMed ID: 33523525) and represses the expression of genes involved in the glycolysis and starch synthesis pathways (PubMed ID: 33523525). Additionally, NAD-ME1 produces primary and secondary metabolites, such as flavonoids and phenolic acids, which are important for plant defense and stress responses (PubMed ID: 33523525). Overall, the function of NAD-ME1 in plant metabolism is to regulate the balance between different metabolic pathways and to produce metabolites that are essential for plant growth and development.

## Final Prompt
```
mini_ins = []
pro = "Please convert the following notes about the gene " + gene_id + " into a more readable and comprehensive paragraph like the given example. Remember to include all numbers in the brackets, as these PubMed IDs are essential for referencing the studies. Also include all given details. Here are the notes: " + text_summary
mini_dict = {"role": "user",}
mini_dict["content"] = pro
mini_ins.append({
"role": "user",
"content": "Please convert the following notes about the gene ABI3 into a coherent, comprehensive and readable paragraph. It's crucial to include the PubMed IDs, which are the numbers in the brackets, within the paragraph. These IDs provide essential references and should not be omitted. For example, you can mention studies or findings followed by their respective PubMed ID. Here are the notes: ABI3 MAINTAINS EMBRYO DEVELOPMENT (10743655), SSP ACCUMULATION (15695450), AT2S3 (15695463), CRC (15695463), PLANT EMBRYO DEVELOPMENT (17158584), MIR159 (17217461), HSFA9 (17220197), ABA-INDUCED ARREST (18278579), STORAGE PROTEIN SYNTHESIS (18701524), WRKY2 (19622176), TWO MAJOR STAGES IN EMBRYO MATURATION (19659659), LEA PROTEINS (24043848), SEED DEVELOPMENT (24388521, 29475938), SEED MATURATION (24473899, 28346448, 35318532), PROTEIN RESERVES (25840088), ABA SIGNALING (26496910)."
})
mini_ins.append(
{
"role": "assistant",
"content": "The gene ABI3 plays a pivotal role in maintaining embryo development, as evidenced by research documented in PubMed ID 10743655. It is also involved in the accumulation of SSP (PubMed ID 15695450) and influences various processes such as AT2S3 and CRC (PubMed IDs 15695463), plant embryo development (PubMed ID 17158584), and the regulation of MIR159 (PubMed ID 17217461). Further, ABI3 is integral to HSFA9 mechanisms (PubMed ID 17220197), ABA-induced arrest (PubMed ID 18278579), and storage protein synthesis (PubMed ID 18701524). It interacts with WRKY2 (PubMed ID 19622176) and is crucial in two major stages of embryo maturation (PubMed ID 19659659), LEA protein production (PubMed ID 24043848), and seed development (PubMed IDs 24388521, 29475938). The gene's role extends to seed maturation (PubMed IDs 24473899, 28346448, 35318532), protein reserve synthesis (PubMed ID 25840088), and ABA signaling pathways (PubMed ID 26496910)."
})
mini_ins.append(mini_dict)
instruction.append(mini_ins)
```
## Set Up & Installation
1. ssh to your **cedar.computecanada.ca** account
2. clone the github repo for llama2-codellama
   ```
   git clone https://github.com/meta-llama/codellama.git
   ```
3. Follow the instruction for Codellama, visit the Meta website https://llama.meta.com/llama-downloads/ and register to download the **codellama 13b model**
4. Clone this repo, move the scipt folder parallal to the `example_chat_completion.py` (You don't need to worry about the dependices for the llama model, the setup is already included in the script)
   ```bash
   # Clone the repository
   git clone https://github.com/emma0925/Gene-Summary-Enhancer.git
   
   # Navigate to the project's scripts directory
   cd Gene-Symmary-Enhancer/scripts
   ```
## Overview on how to run?
If you want to run from very begining (cleaning out the gene id) to generation the llama summary, forllow the following steps. Please make sure to change all the file path and email for sbatch job before running, for more details read through Features section. 
1. Clean Gene ids (Most likely, you don't need to run this step, the cleaned gene list is saved in `gene_ids/gene_ids_full.txt`)
```
python3 clean_raw.py
```
2. Extract from Plant Connectome: If first time run, you need to change the emails and the file path, details in Features section
```
./get_connectome_for_all.sh
```
3. Summary Generation using llama (the script includes setting up a new virtual env and download all the dependency for llama)
```
./get_llama_for_all.sh
```
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

- **Shell Script (`get_connectome_for_all.sh`):** Divides all gene IDs into different batches and prepares sbatch scripts for submission to Compute Canada's scheduling system. This script automates the setup for parallel data extraction, including the creation of necessary directories for organized storage of outputs.

- **Python Script (`generate_connectome_output.py`):** Fetches data for each gene ID by making requests to the Connectome API, processes the response to ensure data integrity, and saves the results in a structured JSON format. The script is designed to handle API rate limits gracefully and includes error handling to manage any issues that may arise during data retrieval.

#### Configuration and Usage

Users must update certain paths in the `get_connectome_for_all.sh` script to match their environment and project structure, including directories for the virtual environment, input and output data, and the Python script path.

#### Execution

To initiate the Automated Data Extraction process, follow these steps:

1. **Prepare the Gene ID List:** Use the output file generated from the 'Gene ID Input Cleaning' process as the input for this stage.

2. **Adjustions:** the batch size, job email recipient, output_directory

    In line 29 of the `get_connectome_for_all.sh`, change the email address for getting the job status (**Highly Recommended**)
    ```
    echo "#SBATCH --mail-user=<your_email>" >> "$sbatch_file" # Replace <your_email>
    ```
    You can remove this line if you don't want to get email of the job status.

    **Below are optiaonal:**
   
    If you want to change the batch size, it is in line 6 of the `get_connectome_for_all.sh`
    ```
    BATCH_SIZE=2500 # Changed the number to the number of genes you want to have in each batch
    ```
    Note: it takes around 20 hours to access the endpoint for 5000 genes

    If you want to change the output directory you can change line 8-15 of the `get_connectome_for_all.sh`
    ```
    OUTPUT_DIR="./outputs" # change line 10 if you changed here

    mkdir -p ./outputs #if you changed the output directory, make sure to change here
    mkdir -p ./gene_ids # the folder where the divided gene_ids txt file will be, make sure to change the next line too if you changed here

    # Split gene ID file into batches
    split -l $BATCH_SIZE "$GENE_ID_FILE" ./gene_ids/batch_ # ./gene_ids/batch_ is the default folder where the divided gene_ids txt file will be
    ```

4. **Run the Shell Script:** Execute the `batch_data_retrieval.sh` script. This will split the gene ID list into batches, create sbatch scripts for each batch, and submit them for processing.

    ```bash
    ./get_connectome_for_all.sh
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

## Questions
If you have any questions regarding this repo, feel free to email me through jianyun.zhuang@mail.utronto.ca. 
## License (To be determined)

## Acknowledgements

This repository was created by Jian Yun Zhuang (@emma0925), under the supervision of Professor Nicholas Provart(@nprovart) and with guidance from Vincent Lau(@vinlau) at the University of Toronto. The project benefits from their extensive knowledge, support, and insights in the field of bioinformatics and computer science. 

Special thanks are extended to Professor Marek Mutwil and his team at the Plants Systems Biology and Evolution Lab, Nanyang Technological University, for their development of the Plant Connectome endpoint. Their contributions to plant systems biology significantly enhance the capabilities of this tool by providing comprehensive data access and facilitating advanced gene analysis.

We are grateful for the contributions and mentorship from all parties involved throughout the development of this tool.


