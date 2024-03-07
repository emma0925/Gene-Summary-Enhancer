#!/bin/bash

# Configuration
API_URL="https://connectome.plant.tools/api/alias/"
GENE_ID_FILE="./gene_ids_full.txt"
BATCH_SIZE=2500
SCRIPT="./generate_connectome_output.py"
OUTPUT_DIR="./outputs" # change line 10 if you changed here


mkdir -p ./outputs #if you changed line 8, make sure to change here
mkdir -p ./gene_ids # the folder where the divided gene_ids txt file will be, make sure to change line 14

# Split gene ID file into batches
split -l $BATCH_SIZE "$GENE_ID_FILE" ./gene_ids/batch_

# Counter for batch file script naming
batch_counter=1

# Assuming variables are already set
for batch_file in ./gene_ids/batch_*; do
    mkdir -p ${OUTPUT_DIR}/batch_${batch_counter}
    output_file="${OUTPUT_DIR}/batch_${batch_counter}/output_$(basename "${batch_file}").json"
    sbatch_file="${OUTPUT_DIR}/batch_${batch_counter}/sbatch_script_${batch_counter}.sh"

    # Create the sbatch script for the current batch
    echo "#!/bin/bash" > "$sbatch_file"
    echo "#SBATCH --time=20:00:00" >> "$sbatch_file"
    echo "#SBATCH --account=def-nprovart" >> "$sbatch_file"
    echo "#SBATCH --mail-user=jianyun.zhuang@mail.utoronto.ca" >> "$sbatch_file"
    echo "#SBATCH --mail-type=ALL" >> "$sbatch_file"
    echo "#SBATCH --output ${OUTPUT_DIR}/batch_${batch_counter}/slurm-%A_%a.out"  >> "$sbatch_file"
    echo "" >> "$sbatch_file"
    echo "module load python/3.8" >> "$sbatch_file"
    echo "SLURM_TMPDIR='/home/emma0925/scratch/generate_new'" >> "$sbatch_file"
    echo "virtualenv --no-download \$SLURM_TMPDIR/env" >> "$sbatch_file"
    echo "source \$SLURM_TMPDIR/env/bin/activate" >> "$sbatch_file"
    echo "" >> "$sbatch_file"
    echo "pip install requests" >> "$sbatch_file"
    echo "" >> "$sbatch_file"
    echo "python3 $SCRIPT $API_URL $batch_file $output_file" >> "$sbatch_file"

    # Make the sbatch script executable
    chmod +x "$sbatch_file"

    # Submit the sbatch script
    sbatch "$sbatch_file" 

    # Increment the batch counter for the next script
    batch_counter=$((batch_counter+1))
done

echo "All sbatch scripts have been created and submitted."

