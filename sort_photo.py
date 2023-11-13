#  utility script to organize photos

#  In my photo folders, where this script will go
#  folders come in pairs: YYYYMMDD_RAW & YYYYMMDD_JPEG
#  both contain symmetrical sets of files with matching names
#  Raw are IMG_DDDD.cr2, jpegs are same but .jpeg
#  Crawl folder, Find JPEG folder, collect names
#  find matching RAW folder, delete all that are not in the names
#  ...
#  profit


import os
import shutil


def collect_jpg_file_names(directory_path):

    jpg_files = set()
    for root, _, files in os.walk(directory_path):
        if "_JPEG" in root:
            for file in files:
                if file.lower().endswith('.jpg'):
                    jpg_files.add(file.lower().replace('.jpg', ''))

    return jpg_files


def delete_non_matching_raw_files(directory_path, jpeg_files):
    for root, _, files in os.walk(directory_path):
        if "_RAW" in root:
            for file in files:
                if file.lower().endswith('.cr2'):
                    raw_file_name = file.lower().replace('.cr2', '')
                    if raw_file_name not in jpeg_files:
                        os.remove(os.path.join(root, file))


def delete_remaining_jpeg_folders(directory_path):
    for root, dirs, _ in os.walk(directory_path):
        for directory in dirs:
            if directory.endswith('_JPEG'):
                folder_path = os.path.join(root, directory)
                shutil.rmtree(folder_path)


def move_remaining_cr2_files(directory_path):
    sorted_folder = os.path.join(directory_path, 'SORTED')
    os.makedirs(sorted_folder, exist_ok=True)
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.cr2'):
                file_path = os.path.join(root, file)
                shutil.move(file_path, os.path.join(sorted_folder, file))


def delete_remaining_empty_raw_folders(directory_path):
    for root, dirs, _ in os.walk(directory_path):
        for directory in dirs:
            if directory.endswith('_RAW'):
                folder_path = os.path.join(root, directory)
                if not os.listdir(folder_path):  # Check if the folder is empty
                    os.rmdir(folder_path)  # Remove the empty folder


# Path to the parent directory containing '_JPEG' and '_RAW' folders
# PATH = 'c:\\Walbrzych_photo' DEPRECATED


if __name__ == '__main__':
    path = os.getcwd()
    jpgs = collect_jpg_file_names(path)
    delete_non_matching_raw_files(path, jpgs)
    delete_remaining_jpeg_folders(path)
    # Move .cr2 files to SORTED folder
    move_remaining_cr2_files(path)
    delete_remaining_empty_raw_folders(path)