#!/bin/bash

# Configuration
SLURM_TMPDIR='/home/emma0925/scratch/llama' # The dir for the virtual env, MUST CHANGE THIS

SCRIPT="./generate_llama_summary.py"  # Update this path to your Python script
INPUT_DIR="../outputs" # The directory that you saved the connectome outputs
OUTPUT_DIR="../outputs/slurm_out_fils" # The directory that you want to save your slurm-.out file
EXEMPT_DIR="../outputs/exempt_genes" # the place you want to save the exempt_genes


# Make sure exempt directory exists
mkdir -p "$EXEMPT_DIR"

# Loop through each batch folder in OUTPUT_DIR
for batch_folder in "$INPUT_DIR"/batch_*; do
    batch_name=$(basename "$batch_folder")
    input_file=$(find "${batch_folder}" -type f -name "*.json" | head -n 1)
    exempt_file_path="${EXEMPT_DIR}/exempt_${batch_name}.txt"
    sbatch_file="${batch_folder}/sbatch_llama_${batch_name}.sh"

    # Check if the input JSON file exists
    if [[ -f "$input_file" ]]; then
        # Create the sbatch script for the current batch
        echo "#!/bin/bash" > "$sbatch_file"
        echo "#SBATCH --time=60:00:00" >> "$sbatch_file"
        echo "#SBATCH --account=def-nprovart" >> "$sbatch_file"
        echo "#SBATCH --gpus-per-node=v100l:2" >> "$sbatch_file"
        echo "#SBATCH --mem=125G" >> "$sbatch_file"
        echo "#SBATCH --mail-user=jianyun.zhuang@mail.utoronto.ca" >> "$sbatch_file"
        echo "#SBATCH --mail-type=ALL" >> "$sbatch_file"
        echo "#SBATCH --output ${OUTPUT_DIR}/slurm-llama-${batch_name}-%A_%a.out"  >> "$sbatch_file" # %A_%a is the job_id 
        echo "" >> "$sbatch_file"
        echo "module load python/3.6" >> "$sbatch_file"
        echo "SLURM_TMPDIR=${SLURM_TMPDIR}" >> "$sbatch_file" # need to change to the correct PATH
        echo "virtualenv --no-download \$SLURM_TMPDIR/env" >> "$sbatch_file"
        echo "source \$SLURM_TMPDIR/env/bin/activate" >> "$sbatch_file"
        echo "" >> "$sbatch_file"
        echo "pip install -e ." >> "$sbatch_file"  # Make sure to install any dependencies your script might need
        echo "pip install torch --no-index" >> "$sbatch_file" 
        echo "" >> "$sbatch_file"
        echo "module purge" >> "$sbatch_file" 
        echo "module load gcc/9.3.0" >> "$sbatch_file" 
        echo "module load openmpi/4.0.3" >> "$sbatch_file" 
        echo "module load PyTorch/1.13.1" >> "$sbatch_file" 
        echo "" >> "$sbatch_file"
        echo "torchrun --nproc_per_node 2 $SCRIPT $input_file $exempt_file_path \\" >> "$sbatch_file"
        echo "    --ckpt_dir ../codellama/CodeLlama-13b-Instruct/ \\" >> "$sbatch_file" # You might need to change this part
        echo "    --tokenizer_path ../codellama/CodeLlama-13b-Instruct/tokenizer.model \\" >> "$sbatch_file"  # You might need to change this part
        echo "    --max_seq_len 6000 --max_batch_size 4" >> "$sbatch_file"

        # Make the sbatch script executable
        chmod +x "$sbatch_file"

        # Submit the sbatch script
        sbatch "$sbatch_file" 
    else
        echo "Input file not found for batch: $batch_name"
    fi
done

echo "All sbatch scripts have been created and submitted."
