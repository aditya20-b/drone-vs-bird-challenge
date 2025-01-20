import os

def combine_yolo_files(input_dir, output_file):
    # Open the output file
    with open(output_file, 'w') as outfile:
        # Iterate through all text files in the input directory
        for txt_file in sorted(os.listdir(input_dir)):
            if txt_file.endswith('.txt'):
                txt_file_path = os.path.join(input_dir, txt_file)
                with open(txt_file_path, 'r') as infile:
                    # Read contents of the YOLO file and append to the output
                    contents = infile.read()
                    outfile.write(contents)
                    # Add a newline after each file's content
                    outfile.write('\n')
    
    print(f"All YOLO files in '{input_dir}' have been combined into '{output_file}'.")

# Example usage
input_dir = 'yolo_labels'  # Directory containing YOLO .txt files for the video
output_file = 'combined_yolo_labels.txt'  # Path to save the combined file
combine_yolo_files(input_dir, output_file)
