import json
import os
import re
import subprocess
import sys

def delete_files_in_directory(directory_path):
    """
    Deletes all files in the specified directory.

    :param directory_path: The path to the directory whose files are to be deleted.
    """
    # Check if the specified path is indeed a directory
    if not os.path.isdir(directory_path):
        print(f"The path {directory_path} is not a valid directory.")
        return

    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            # Check if it is a file and not a directory
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file
                # print(f"Deleted {file_path}")
            else:
                print(f"Skipped {file_path}, not a file.")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def do_inference_and_log_result(model_path, prompt, results_file_path, adapter_file, line_num):
    # Construct the command to call the script with arguments
    command = ['venv/bin/python3', '-m','mlx_lm.generate', '--temp', '0', '-m', '500', '--model', model_path, '--adapter-path', adapter_file,'--prompt', prompt]

    # Call the script and capture its output
    result = subprocess.run(command, capture_output=True, text=True)

    try:
        with open(results_file_path + str(line_num) + ".ttl" , 'w') as file:
            # Check for errors
            if result.returncode != 0:
                file.write("ERROR_1: "+ result.stderr)
                print(f"Error in script execution: {result.stderr}")
            else:
                text_input = result.stdout

                tmp = text_input.split("[/INST]")[1]
                generated_output = tmp.split("==========")[0]
                file.write(generated_output)
    except FileNotFoundError:
        print(f"Error: The file '{results_file_path}\{str(line_num)}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main (model_file, testset_path, results_file_path, adapter_file):
    # Clear all the output fiels under the resulsts path 
    delete_files_in_directory(results_file_path)

    prompt = None
    with open(testset_path, 'r') as testFile:
        line_num = 0
        for line in testFile:
            line_num += 1
            # Parse the JSON line
            json_obj = json.loads(line)

            # The instructions are in the 'text 'field
            text = json_obj.get('text', '')

            # Regular expression to find text between [INST] and [/INST]
            match = re.search(r'\[INST\](.*?)\[/INST\]', text, re.IGNORECASE)
            if match:
                prompt = match.group(1).strip()
                do_inference_and_log_result(model_file, prompt, results_file_path, adapter_file, line_num)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Fine-tuned benchmark requires 4 arguments.")
    sys.exit(0)
