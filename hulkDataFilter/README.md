# Text Sorter

## Description

This script sorts text files in a specified directory by their size and splits large files into smaller chunks. The script creates a folder to hold the filtered files and tracks the progress of the filtering process using CSV files. 

The script is divided into two main classes: `TrackFiles` and `FileSplit`.

### `TrackFiles`

The `TrackFiles` class is responsible for creating and managing the CSV files that track the progress of the filtering process. The class has the following methods:

- `create_csv_if_not_exists(file_path, expected_headers)`: This method creates a CSV file if it does not exist or if it has the wrong headers. It takes two arguments: `file_path`, which is the path to the CSV file, and `expected_headers`, which is a list of strings representing the expected header row for the CSV file.

- `get_next_result_folder_name()`: This method returns the name of the next folder to hold the filtered files.

- `sort_and_rename_text_files()`: This method sorts and renames the text files in the given directory from `file_0.txt` to `file_n.txt`, sorted by their size from largest to smallest.

- `prepare()`: This method prepares the track files, creates the filtered folder, and sorts the text files.

### `FileSplit`

The `FileSplit` class is responsible for splitting the text files into smaller chunks. The class has the following methods:

- `split_file(filename)`: This method splits a single text file into smaller chunks. It takes one argument: `filename`, which is the name of the file to split.

- `split_all_files()`: This method splits all the text files in the directory.

- `get_splitted_files()`: This method gets the names of all the split files.

- `write_splitted_files_info()`: This method writes the information about the split files to the CSV files.

## Usage

To use the script, you need to provide a directory containing the text files to sort. You can modify some of the parameters in the script, such as the chunk size and whether to delete the original files after they have been split.

base_texts_dir = r"D:\agtests"
deleteOrignalFiles = False

To run the script, simply run the `main` function.

## Dependencies

The script uses the following libraries:

- `os`
- `csv`
- `time`
- `random`
- `shutil`
- `ctypes`
- `sys`
- `math`
- `threading`
- `concurrent.futures`
- `progressbar`
- `tqdm`

Make sure to install these libraries before running the script.
