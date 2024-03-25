#!/bin/bash
#SBATCH --time=100:00:00
#SBATCH --account=def-nprovart
#SBATCH --gpus-per-node=v100l:2
#SBATCH --mem=125G
#SBATCH --mail-user=jianyun.zhuang@mail.utoronto.ca
#SBATCH --mail-type=ALL
#SBATCH --output ../outputs/llama_rerun_%A.out

module load python/3.6
SLURM_TMPDIR='/home/emma0925/scratch/llama'
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate

pip install -e .
pip install torch --no-index

module purge
module load gcc/9.3.0
module load openmpi/4.0.3
module load PyTorch/1.13.1

torchrun --nproc_per_node 2 /home/emma0925/scratch/new_llama/codellama/Gene-Summary-Enhancer/scripts/generate_llama_specific.py /home/emma0925/scratch/new_llama/codellama/Gene-Summary-Enhancer/outputs/combined/combined_connectome.json /home/emma0925/scratch/new_llama/codellama/Gene-Summary-Enhancer/outputs/combined/combined_rerun.txt \
    --ckpt_dir ../../CodeLlama-13b-Instruct/ \
    --tokenizer_path ../../CodeLlama-13b-Instruct/tokenizer.model \
    --max_seq_len 6000 --max_batch_size 4
