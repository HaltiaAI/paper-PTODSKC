import argparse
import json
import re
import subprocess
import sys

if __name__ == "__main__":

    # Create the parser
    parser = argparse.ArgumentParser(description="Run the benchmarks for the provided model and adapter.")

    # Add the arguments
    parser.add_argument('--model-path', type=str, required=True, help='The path of the model to use')
    parser.add_argument('--adapter-path', type=str, required=True, help='The path of the adapter to use')
    # Parse the arguments
    args = parser.parse_args()

    model_path = args.model_path
    qlora_adapter_path = args.adapter_path
    test_file = 'data/test.jsonl'
    results_file_fineTuned_shot = 'results/test_evaluation_output/'

    # The instruction bases for the proposed methods
    prompt_base_fineTuned_shot = '[INST]'

    # Run fine-tuned benchmark on model
    command = ['/usr/bin/python3', 'scripts/fineTunedShot.py', model_path, prompt_base_fineTuned_shot, test_file, results_file_fineTuned_shot, qlora_adapter_path]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in fine-tuning script execution: {result.stderr}")
        sys.exit(3)

    print("Benchmarks completed. Please check 'results/' directory for benchmark results")

