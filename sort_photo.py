#  utility script to organize photos

#  In my photo folders, where this script will go
#  folders come in pairs: YYYYMMDD_RAW & YYYYMMDD_JPG
#  both contain symmetrical sets of files with matching names
#  Raw are IMG_DDDD.cr2, jpegs are same but .jpeg
#  Crawl folder, Find JPEG folder, collect names
#  find matching RAW folder, delete all that are not in the names
#  v.2023-12-13 added skip logic for already processed raw files
#  ...
#  profit


import os
import shutil


def collect_jpg_file_names(directory_path):

    jpg_files = set()

    for root, _, files in os.walk(directory_path):
        if "_JPG" in root:
            for file in files:
                if file.lower().endswith('.jpg'):
                    jpg_files.add(file.lower().replace('.jpg', ''))

    return jpg_files


def delete_non_matching_raw_files(directory_path, jpeg_files):

    for root, _, files in os.walk(directory_path):
        if "_RAW" in root:

            skip_list = set()

            for file in files:  # add skip logic for already processed raw files.
                if file.lower().endswith('.pp3'):
                    skip_list.add(file.lower().replace('.cr2.pp3', ''))

            for file in files:
                if file.lower().endswith('.cr2'):
                    raw_file_name = file.lower().replace('.cr2', '')
                    if raw_file_name not in jpeg_files and raw_file_name not in skip_list:
                        os.remove(os.path.join(root, file))


def delete_remaining_jpeg_folders(directory_path):
    for root, dirs, _ in os.walk(directory_path):
        for directory in dirs:
            if directory.endswith('_JPG'):
                folder_path = os.path.join(root, directory)
                shutil.rmtree(folder_path)


def move_remaining_cr2_files(directory_path):
    sorted_folder = os.path.join(directory_path, 'SORTED')
    os.makedirs(sorted_folder, exist_ok=True)
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.cr2') or file.lower().endswith('.pp3'):
                file_path = os.path.join(root, file)
                shutil.move(file_path, os.path.join(sorted_folder, file))


def delete_remaining_empty_raw_folders(directory_path):
    for root, dirs, _ in os.walk(directory_path):
        for directory in dirs:
            if directory.endswith('_RAW'):
                folder_path = os.path.join(root, directory)
                if not os.listdir(folder_path):  # Check if the folder is empty
                    os.rmdir(folder_path)  # Remove the empty folder


# Path to the parent directory containing '_JPG' and '_RAW' folders


if __name__ == '__main__':
    path = os.getcwd()
    jpgs = collect_jpg_file_names(path)
    delete_non_matching_raw_files(path, jpgs)
    delete_remaining_jpeg_folders(path)
    # Move .cr2 files to SORTED folder
    move_remaining_cr2_files(path)
    delete_remaining_empty_raw_folders(path)
    input("Done, press any key to exit...")
