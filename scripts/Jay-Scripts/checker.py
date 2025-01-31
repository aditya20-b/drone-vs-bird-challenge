import os

def count_matching_images(image_directory, json_directory):
    if not (os.path.exists(image_directory) and os.path.isdir(image_directory)):
        print(f"Warning: {image_directory} is not a valid directory.")
        return {}
    if not (os.path.exists(json_directory) and os.path.isdir(json_directory)):
        print(f"Warning: {json_directory} is not a valid directory.")
        return {}
    
    image_files = set(f for f in os.listdir(image_directory) if not f.endswith(".json"))
    json_files = sorted([os.path.splitext(f)[0] for f in os.listdir(json_directory) if f.endswith(".json")])
    
    counts = {}
    for json_file in json_files:
        count = sum(1 for img in image_files if img.startswith(json_file))
        counts[json_file] = count
    
    return counts

# Example usage
image_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data/images"  # Replace with actual path
json_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/output_json"  # Replace with actual path

result = count_matching_images(image_dir, json_dir)
for json_file, count in result.items():
    print(f"Count of matching images for {json_file}: {count}")
