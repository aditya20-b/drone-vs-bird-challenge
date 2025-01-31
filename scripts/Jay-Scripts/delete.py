import os

def delete_files_with_prefix(directory, prefix):
    try:
        # Get a list of files in the specified directory
        files = os.listdir(directory)
        
        # Iterate through the files
        for file in files:
            # Check if the file name starts with the given prefix
            if file.startswith(prefix):
                # Construct the full file path
                file_path = os.path.join(directory, file)
                
                # Check if it's a file (not a directory)
                if os.path.isfile(file_path):
                    # Delete the file
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                    
        print("Operation completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the directory and prefix
#directory = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data/labels"
directory = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/annotated_images"
#directory = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/checker_dummy/annotated"
prefix = "two_parrot_disco_1"

# Call the function to delete files
delete_files_with_prefix(directory, prefix)

