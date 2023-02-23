import os, csv, time, random, shutil, ctypes, sys, math, threading, concurrent.futures, progressbar
from tqdm import tqdm

''' Main classes '''
class TrackFiles:
    def __init__(self):
        self.expected_filtered_count_headers = [
            "id", "ln_count", "ln_finished", "fi_done", "fi_name"]
        self.expected_splitted_files_headers = [
            "id", "lines_count", "cfo_path", "cfo_name"]
        self.track_files_dir = os.path.join(programDir, "_track_files")
        self.filtered_files_dir = os.path.join(programDir, "_filtered")
        self.filtered_count_path = os.path.join(
            self.track_files_dir, "_filtered_count.csv")
        self.orignal_files_path = os.path.join(
            self.track_files_dir, "_splitted_files.csv")
        self.filtered_path = "_filtered"
    
    # Create a csv file if it does not exist or if it has the wrong headers
    def create_csv_if_not_exists(self, file_path, expected_headers):
        finame = os.path.basename(file_path)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding="UTF-8", errors="ignore") as file:
                    reader = csv.reader(file)
                    header = next(reader)
                    if header != expected_headers:
                        os.remove(file_path)
                        with open(file_path, 'w', newline='', encoding="UTF-8", errors="ignore") as file:
                            writer = csv.writer(file)
                            writer.writerow(expected_headers)
                        print(f"[INFO] : {finame} was deleted and re-created with the correct headers.")
                    else:
                        print(f"[READY] : {finame} has the correct headers.")
            except StopIteration:
                os.remove(file_path)
                with open(file_path, 'w', newline='', encoding="UTF-8", errors="ignore") as file:
                    writer = csv.writer(file)
                    writer.writerow(expected_headers)
                print(f"[INFO] : {finame} was deleted and re-created with the correct headers.")
        else:
            with open(file_path, 'w', newline='', encoding="UTF-8", errors="ignore") as file:
                writer = csv.writer(file)
                writer.writerow(expected_headers)
            print(f"[READY] : {finame} has been created.")

    # Get the next result folder name
    def get_next_result_folder_name(self):
        base_full_path = os.path.join(programDir, self.filtered_path)
        date_string = time.strftime("%Y_%m_%d")
        existing_folders = [f for f in os.listdir(base_full_path) if os.path.isdir(os.path.join(base_full_path, f)) and date_string in f]
        # existing_folders = [f for f in os.listdir(base_full_path) if date_string in f]
        max_num = 0
        for folder in existing_folders:
            try:
                folder_num = int(folder.split(date_string + "-")[1])
                max_num = max(max_num, folder_num)
            except ValueError:
                pass
        next_num = max_num + 1
        return os.path.join(self.filtered_path, date_string + "-" + str(next_num))
    
    # Sort and rename the text files in the given directory  from file_0.txt to file_n.txt sorted by their size from largest to smallest 
    def sort_and_rename_text_files(self):
        texts_dir = os.path.join(programDir, base_texts_dir)
        texts = [f for f in os.listdir(texts_dir) if os.path.isfile(os.path.join(texts_dir, f)) and f.endswith(".txt")]
        texts.sort(key=lambda x: os.path.getsize(os.path.join(texts_dir, x)), reverse=True)
        for i, text in enumerate(texts):
            try:
                os.rename(os.path.join(texts_dir, text), os.path.join(texts_dir, "sorted_file_" + str(i) + ".txt"))
            except:
                pass
        print("[INFO] : The text files in {} have been sorted and renamed.".format(texts_dir.split("/")[-1]))
        return

    # Sort and rename the text files in the given directory  from file_0.txt to file_n.txt sorted by their size from largest to smallest
    def prepare(self):
        # STEP 1 : CREATE THE `_track_files` directory if it does not exist
        if not os.path.exists(self.track_files_dir):
            os.makedirs(self.track_files_dir)
            print("[INFO] : The `_track_files` directory has been created.")
        if not os.path.exists(self.filtered_files_dir):
            os.makedirs(self.filtered_files_dir)
            print("[INFO] : The `_filtered` directory has been created.")
        # STEP 2 : CREATE THE CSV FILES IF THEY DO NOT EXIST ==> _filtered_count.csv and _splitted_files.csv in the `_track_files` directory
        self.create_csv_if_not_exists(
            self.filtered_count_path, self.expected_filtered_count_headers)
        self.create_csv_if_not_exists(
            self.orignal_files_path, self.expected_splitted_files_headers)
        # STEP 3 : CREATE THE FILTERED FOLDER    
        self.result_folder = self.get_next_result_folder_name()
        os.makedirs(self.result_folder)
        print("[INFO] : The result folder {} has been created.".format(self.result_folder.split("/")[-1]))
        # STEP 4 : SORT AND RENAME THE TEXT FILES
        try:
            self.sort_and_rename_text_files()
        except FileNotFoundError as e:
            print("[ERROR] : The text files in {} could not be sorted and renamed.".format(base_texts_dir))
            pass


class FileSplit:
    def __init__(self, text_dir, chunk_size=50 * 1024 * 1024):
        self.text_dir = text_dir
        self.chunk_size = chunk_size
        self.splitted_folder = "_splitted_" + str(int(time.time()))
        



    def split_file(self, filename):
        if not filename.endswith('.txt'):
            return
        with open(os.path.join(self.text_dir, filename), "rb") as f:
            content = f.read()
            chunk_count = int(math.ceil(len(content) / float(self.chunk_size)))
            for i in range(chunk_count):
                chunk = content[i * self.chunk_size : (i + 1) * self.chunk_size]
                chunk_filename = "{}_{}".format(i, filename)
                new_file_path = os.path.join(self.text_dir, self.splitted_folder, chunk_filename)
                try:
                    with open(new_file_path, "wb") as chunk_file:
                        chunk_file.write(chunk)
                except Exception as e:
                    # print("PermsError: {}".format(e))
                    pass
        if deleteOrignalFiles:
            os.remove(os.path.join(self.text_dir, filename))

    def split_all_files(self):
        splitted_dir = os.path.join(self.text_dir, self.splitted_folder)
        if not os.path.exists(splitted_dir):
            os.makedirs(splitted_dir)

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            filenames = os.listdir(self.text_dir)
            widgets = [
                progressbar.Percentage(),
                ' ', progressbar.Bar(),
                ' ', progressbar.ETA(),
                ' ', progressbar.DynamicMessage('file')
            ]
            bar = progressbar.ProgressBar(
                widgets=widgets, max_value=len(filenames), redirect_stdout=True
            ).start()
            for i, future in enumerate(concurrent.futures.as_completed(
                executor.submit(self.split_file, filename)
                for filename in filenames
            )):
                bar.update(i + 1, file=os.path.basename(filenames[i]))
                future.result()
            bar.finish()

    def get_splitted_files(self):
        # GET EACH SPLITTED FILE TO FILL THIS INFO IN CSV FILE
        self.all_splitted_files_dirs =  [f for f in os.listdir(os.path.join(self.text_dir, self.splitted_folder)) if os.path.isfile(os.path.join(self.text_dir, self.splitted_folder, f)) and f.endswith(".txt")]
        return

    def write_splitted_files_info(self):
        # track files info /_track_files/_splitted_files.csv
        self.splitted_files_path = os.path.join(programDir, "_track_files", "_splitted_files.csv")
        self.filtered_count_path = os.path.join(programDir, "_track_files", "_filtered_count.csv")

        def write_file_info(file_path, header, writer_func):
            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for i, file in enumerate(self.all_splitted_files_dirs):
                    # 'charmap' codec can't decode byte 0x8f in position 110: character maps to <undefined>
                    with open(os.path.join(self.text_dir, self.splitted_folder, file), "r", encoding="utf-8", errors="ignore") as f:
                        lines_count = len(f.readlines())
                    writer_func(writer, i, lines_count, file)

        def write_splitted_file_info(writer, i, lines_count, file):
            writer.writerow([i, lines_count, self.splitted_folder, file])

        def write_filtered_count_info(writer, i, lines_count, file):
            writer.writerow([i, lines_count, 0, "False", file])

        write_file_info(self.splitted_files_path, ["id", "lines_count", "cfo_path", "cfo_name"], write_splitted_file_info)
        write_file_info(self.filtered_count_path, ["id", "ln_count", "ln_finished", "fi_done", "fi_name"], write_filtered_count_info)
        return


''' Main functions '''



if __name__ == "__main__":
    # global variables    
    base_texts_dir = r"D:\agtests"
    programDir = os.path.dirname(os.path.realpath(__file__))
    deleteOrignalFiles = False
    # ask user for access program as admin
    # if not ctypes.windll.shell32.IsUserAnAdmin():
    #     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

    # print the start time HH:MM:SS in 12h format
    start_time = time.time()
    print("[STARTED] : SORTER STARTED AT {}. ".format(time.strftime("%I:%M:%S %p", time.localtime(start_time))))

    # STEP 1 : PREPARE THE TRACK FILES AND SORT THE TEXT FILES
    track_files = TrackFiles()
    track_files.prepare()
    
    # STEP 2 : SPLIT THE TEXT FILES
    splitter = FileSplit(base_texts_dir)
    splitter.split_all_files()

    # STEP 3 : READ ALL THE SPLITTED FILES TO ADD INFO TO THE CSV FILES
    splitter.get_splitted_files()
    splitter.write_splitted_files_info()


    # print the end time HH:MM:SS in 12h format
    end_time = time.time()
    execution_time = end_time - start_time
    print("[FINISHED] : SORTER FINISHED AT {} || EXECUTION TIME : {} seconds.".format(time.strftime("%I:%M:%S %p", time.localtime(end_time)), execution_time))

