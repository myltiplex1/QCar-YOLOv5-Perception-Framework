import os
import random
import uuid

def rename_and_shuffle(folder_path):
    # 1. Setup
    # valid image extensions to look for
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    
    # Get list of all files in the folder
    try:
        all_files = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"Error: The folder '{folder_path}' was not found.")
        return

    # Filter only for image files
    images = [f for f in all_files if os.path.splitext(f)[1].lower() in extensions]
    
    if not images:
        print("No images found in the folder!")
        return

    print(f"Found {len(images)} images. Shuffling and renaming...")

    # 2. Shuffle the list randomly
    random.shuffle(images)

    # 3. Rename to temporary unique names first
    # This prevents errors if a file named '000001.jpg' already exists in the folder
    temp_map = []
    print("Step 1: Applying temporary names to avoid conflicts...")
    
    for filename in images:
        old_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()
        
        # Create a random temporary name
        temp_name = f"temp_{uuid.uuid4().hex}{ext}"
        temp_path = os.path.join(folder_path, temp_name)
        
        os.rename(old_path, temp_path)
        temp_map.append(temp_path)

    # 4. Rename to final sequence (000001, 000002, etc.)
    print("Step 2: Applying final sequential names...")
    
    count = 0
    for index, temp_path in enumerate(temp_map, start=1):
        # Get extension from the temp file
        ext = os.path.splitext(temp_path)[1]
        
        # Format: 000001.jpg, 000002.jpg ...
        new_filename = f"{index:06d}{ext}"
        new_path = os.path.join(folder_path, new_filename)
        
        os.rename(temp_path, new_path)
        count += 1

    print(f"✅ Success! {count} images have been shuffled and renamed.")
    print(f"Example: {os.path.join(folder_path, '000001.jpg')}")

# --- CONFIGURATION ---
# Change this to match your folder name strictly
target_folder = "qlabs_datasets" 

# Run the function
if __name__ == "__main__":
    # Check if path is absolute or relative
    if not os.path.exists(target_folder):
        # Try finding it in the current directory
        current_dir = os.getcwd()
        full_path = os.path.join(current_dir, target_folder)
    else:
        full_path = target_folder
        
    rename_and_shuffle(full_path)