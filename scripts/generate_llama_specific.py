import json
import time
import random
import ast
import fire

from typing import Optional
from llama import Llama

def divide_to_two(text_summary):
    # Split the text into sentences
    sentences = text_summary.split('. ')
    total_length = len(text_summary)
    half_length = total_length / 2

    # Initialize variables to keep track of the split
    first_half = ""
    second_half = ""
    current_length = 0

    # Iterate over sentences to find the split point
    for sentence in sentences:
        if current_length + len(sentence) < half_length:
            first_half += sentence + ". "
            current_length += len(sentence) + 2  # Adding 2 for the period and space
        else:
            second_half += sentence + ". "
            continue

    # Remove the extra space and period from the end of the first half and start of the second half
    first_half = first_half.rstrip('. ')
    second_half = second_half.rstrip('. ')
    return [first_half, second_half]

def prepare_mini_instruct(text_summary, gene_id, instruction):
    char_count=len(text_summary)
    mini_ins = []
    if char_count <= 2000:
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
    else:
        temp = divide_to_two(text_summary)
        prepare_mini_instruct(temp[0], gene_id, instruction)
        prepare_mini_instruct(temp[1], gene_id, instruction)
    
    return instruction

def read_and_prepare_instructions(input_file_path, gene_id_path):
    instruction = []

    with open(input_file_path, 'r') as file:
        data = json.load(file)  # Assuming the entire file is a valid JSON object

        with open(gene_id_path, 'r') as exempt_file:
            for line in exempt_file:
                try: 
                    gene_id = line.replace('\n', '')
                    text_summary = data[gene_id].get('text_summary', '')
                    if text_summary:
                        instruction = prepare_mini_instruct(text_summary, gene_id, instruction)
                except:
                    print(gene_id)
    return instruction

import fire
from typing import Optional

# Assuming Llama and other necessary imports are already included

def main(input_file_path: str, gene_id_path: str, ckpt_dir: str, tokenizer_path: str, temperature: float = 0.2, top_p: float = 0.95, max_seq_len: int = 512, max_batch_size: int = 8, max_gen_len: Optional[int] = None):
    # Now the function directly takes all required arguments, including those for file paths and model configuration
    
    # Load and prepare instructions based on the given input file path and exempt file path
    instructions = read_and_prepare_instructions(input_file_path, gene_id_path)
    
    # Initialize the generator with the provided configuration
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )
    
    # Processing instructions with the generator
    for instruction_set in instructions:
        try:
            result = generator.chat_completion(
                [instruction_set],  # Sending one instruction set at a time
                max_gen_len=max_gen_len,
                temperature=temperature,
                top_p=top_p,
            )

            for msg in instruction_set:
                print(f"{msg['role'].capitalize()}: {msg['content']}\n")
            print(f"> {result[0]['generation']['role'].capitalize()}: {result[0]['generation']['content']}")
            print("\n==================================\n")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    fire.Fire(main)
