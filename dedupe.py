import os
import csv
import hashlib
from tqdm import tqdm

VERSION_STRING: str = "1.1.1"


def get_dir() -> str:
    """Get the working directory from user input.

    :return: Directory path
    :rtype: str
    """
    print("Enter or paste the directory you would like to work on below.")
    directory: str = input("Directory: ")
    if not os.path.exists(directory):
        print(f"{directory} does not exist. Please try again.")
        return ""
    return directory


def read_files(working_directory: str) -> list:
    """Read all files in the working directory. Add files and their MD5 hash to a list.

    :param working_directory: String of the directory to scan.
    :type working_directory: str
    :return: List of files and their hashes, in the form of [[file, hash]].
    :rtype: list
    """
    hash_list: list = []
    for root, dirs, file in tqdm(os.walk(working_directory)):
        for f in file:
            # print(os.path.join(root, f))
            file_path: str = os.path.join(root, f)

            with open(file_path, "rb") as file_to_check:
                file_binary = file_to_check.read()
                md5_hash = hashlib.md5(file_binary).hexdigest()

            hash_list.append([file_path, md5_hash])

    return hash_list


def find_duplicates(hash_list: list) -> list:
    """Search through the list of files for duplicates.

    :param hash_list: List of files and their hashes, in the form of [[file, hash]].
    :type hash_list: list
    :return: List of duplicated files, in the form of [[file, hash]].
    :rtype: list
    """
    seen: dict = {}
    duplicated: dict = {}

    for file in hash_list:
        if file[1] in seen:
            duplicated[file[0]] = file[1]
            if seen[file[1]] not in duplicated.values():
                duplicated[seen[file[1]]] = file[1]

        else:
            seen[file[1]] = file[0]

    duplicated_files: list = []
    for file in duplicated.keys():
        duplicated_files.append([file, duplicated[file]])
    return duplicated_files


def make_report(directory: str, duplicated_files: list) -> bool:
    """Creates a .csv file in the root working directory containing the list of duplicated files and their hashes.

    :param directory: Root of working directory.
    :type directory: str
    :param duplicated_files: List of duplicated files, in the in the form of [[file, hash]].
    :type duplicated_files: list
    :return: Returns True or False based on the success of writing the file.
    :rtype: bool
    """
    title_row: list = ["Filename", "Checksum"]
    filename: str = os.path.join(directory, "duplicated_hash_list.csv")

    try:
        with open(filename, "w") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(title_row)
            csvwriter.writerows(duplicated_files)
        return True
    except IOError:
        return False


if __name__ == "__main__":
    print(f"Welcome to JMDM Dedupe v{VERSION_STRING}!")
    working_directory: str = ""
    while working_directory == "":
        working_directory = get_dir()
    hash_list: list = read_files(working_directory)
    duplicated_files: list = find_duplicates(hash_list)
    if make_report(working_directory, duplicated_files):
        print(f"Successfully created list of duplicates in ${working_directory}.")
    else:
        print("There was an error. Please try again.")
