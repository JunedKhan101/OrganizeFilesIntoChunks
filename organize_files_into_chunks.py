import os
import shutil
import sys
from tqdm import tqdm

def organize_files_into_chunks(main_folder, chunk_size, script_name):
    # Ensure the chunk size is an integer
    chunk_size = int(chunk_size)

    # Create a list of all files in the main directory excluding the script file itself
    files = [f for f in os.listdir(main_folder) if os.path.isfile(os.path.join(main_folder, f)) and f != script_name]

    # Calculate the number of chunk folders needed
    num_chunks = (len(files) + chunk_size - 1) // chunk_size

    with tqdm(total=len(files), desc="Organizing Files", unit="file") as pbar:
        # Create chunk folders and move files into them
        for chunk_index in range(num_chunks):
            chunk_folder = os.path.join(main_folder, f'chunk_{chunk_index + 1}')
            os.makedirs(chunk_folder, exist_ok=True)

            # Determine the start and end index for the files in this chunk
            start_index = chunk_index * chunk_size
            end_index = min(start_index + chunk_size, len(files))

            # Move the files to the chunk folder
            for file_index in range(start_index, end_index):
                file_path = os.path.join(main_folder, files[file_index])
                shutil.move(file_path, chunk_folder)
                pbar.update(1)
            print(f'Created {chunk_folder} with {end_index - start_index} files.')

def unchunk_files(main_folder, script_name):
    # List all directories in the main folder matching the pattern 'chunk_#'
    chunk_folders = [f for f in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, f)) and f.startswith('chunk_')]
    # Initialize a list to store all files to be moved back
    all_files = []
    # Collect all files from chunk folders
    for chunk_folder in chunk_folders:
        chunk_folder_path = os.path.join(main_folder, chunk_folder)
        files = [f for f in os.listdir(chunk_folder_path) if os.path.isfile(os.path.join(chunk_folder_path, f))]
        # Append file paths to the list
        for file in files:
            all_files.append(os.path.join(chunk_folder_path, file))

    with tqdm(total=len(all_files), desc="Unchunking Files", unit="file") as pbar:
        # Move files back to the main folder
        for file_path in all_files:
            # Determine the destination path
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(main_folder, file_name)
            shutil.move(file_path, dest_path)
            pbar.update(1)

    print(f'Unchunked {len(all_files)} files back to the main folder.')

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python organize_files_into_chunks.py <main_folder> <mode> <chunk_size>")
        print("Mode should be 'chunk' or 'unchunk'.")
        sys.exit(1)

    main_folder = sys.argv[1]
    mode = sys.argv[2].lower()
    script_name = os.path.basename(__file__)  # Get the name of this script

    if mode == 'chunk':
        chunk_size = int(sys.argv[3])
        organize_files_into_chunks(main_folder, chunk_size, script_name)
    elif mode == 'unchunk':
        unchunk_files(main_folder, script_name)
    else:
        print("Invalid mode. Please use 'chunk' or 'unchunk'.")
        sys.exit(1)

