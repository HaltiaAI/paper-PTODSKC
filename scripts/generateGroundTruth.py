import json
import os
import re

# Path to your JSONL file
input_file_path = 'data/test.jsonl'
output_file_path = 'results/test_ground_truth_output/'

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

def format_and_generate_ttl(line, line_num):
    # Parse the JSON content from the line
    data = json.loads(line)

    # Extract text field
    text_field = data.get('text', '')

    # Extract turtle part from the string
    tmp = text_field.split("[/INST]")[1]
    generated_output = tmp.split("</s>")[0]

    try:
        with open(output_file_path + str(line_num) + ".ttl" , 'w') as file:
            file.write(generated_output)
    except FileNotFoundError:
        print(f"Error: The file '{output_file_path}\{str(line_num)}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Clear all the output fiels under the resulsts path 
    delete_files_in_directory(output_file_path)

    try:
        with open(input_file_path, 'r') as input_file:
            line_num = 0
            for line in input_file:
                # Read each line and create a new .ttl file using the ground truth response 
                line_num+= 1
                format_and_generate_ttl(line,line_num)

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    print("Processing completed. test_ground_truth_output file generated.")