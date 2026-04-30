# This script is entirely created by ChatGPT
import os
import shutil
import sys
from tqdm import tqdm


def get_sorted_files(main_folder, script_name, sort_mode="name"):
    # Get all files except this script
    files = [
        f for f in os.listdir(main_folder)
        if os.path.isfile(os.path.join(main_folder, f)) and f != script_name
    ]

    # Sort based on selected mode
    if sort_mode == "name":
        files.sort()  # alphabetical (good for YYYYMMDD_HHMMSS filenames)

    elif sort_mode == "created":
        files.sort(
            key=lambda f: os.path.getctime(os.path.join(main_folder, f))
        )

    elif sort_mode == "modified":
        files.sort(
            key=lambda f: os.path.getmtime(os.path.join(main_folder, f))
        )

    else:
        raise ValueError("Invalid sort mode. Use: name, created, modified")

    return files


def organize_files_into_chunks(main_folder, chunk_size, script_name, sort_mode):
    chunk_size = int(chunk_size)

    # Get sorted files
    files = get_sorted_files(main_folder, script_name, sort_mode)

    num_chunks = (len(files) + chunk_size - 1) // chunk_size

    with tqdm(total=len(files), desc="Organizing Files", unit="file") as pbar:
        for chunk_index in range(num_chunks):
            # Zero-padded chunk names
            chunk_folder = os.path.join(
                main_folder,
                f"chunk_{chunk_index + 1:03d}"
            )
            os.makedirs(chunk_folder, exist_ok=True)

            start_index = chunk_index * chunk_size
            end_index = min(start_index + chunk_size, len(files))

            for file_index in range(start_index, end_index):
                file_path = os.path.join(main_folder, files[file_index])
                shutil.move(file_path, chunk_folder)
                pbar.update(1)

            print(
                f"Created {chunk_folder} with "
                f"{end_index - start_index} files."
            )


def unchunk_files(main_folder):
    # Sort chunk folders so chunk_001, chunk_002... stay ordered
    chunk_folders = sorted(
        [
            f for f in os.listdir(main_folder)
            if os.path.isdir(os.path.join(main_folder, f))
            and f.startswith("chunk_")
        ]
    )

    all_files = []

    for chunk_folder in chunk_folders:
        chunk_folder_path = os.path.join(main_folder, chunk_folder)

        files = [
            f for f in os.listdir(chunk_folder_path)
            if os.path.isfile(os.path.join(chunk_folder_path, f))
        ]

        for file in files:
            all_files.append(os.path.join(chunk_folder_path, file))

    with tqdm(total=len(all_files), desc="Unchunking Files", unit="file") as pbar:
        for file_path in all_files:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(main_folder, file_name)

            shutil.move(file_path, dest_path)
            pbar.update(1)

    print(f"Unchunked {len(all_files)} files back to the main folder.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage:\n"
            "  py organize_files_into_chunks.py <main_folder> chunk <chunk_size> --sort <name|created|modified>\n"
            "  py organize_files_into_chunks.py <main_folder> unchunk"
        )
        sys.exit(1)

    main_folder = sys.argv[1]
    mode = sys.argv[2].lower()
    script_name = os.path.basename(__file__)

    if mode == "chunk":
        if len(sys.argv) < 4:
            print("Chunk size required.")
            sys.exit(1)

        chunk_size = int(sys.argv[3])

        # Default sort mode
        sort_mode = "name"

        if "--sort" in sys.argv:
            sort_index = sys.argv.index("--sort")
            if sort_index + 1 < len(sys.argv):
                sort_mode = sys.argv[sort_index + 1]

        organize_files_into_chunks(
            main_folder,
            chunk_size,
            script_name,
            sort_mode
        )

    elif mode == "unchunk":
        unchunk_files(main_folder)

    else:
        print("Invalid mode. Use 'chunk' or 'unchunk'.")
        sys.exit(1)