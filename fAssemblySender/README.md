# formAssemblyEmailSender
### https://www.formassembly.com/
## Using forms ids

## Overview
This program is a notification sender that uses emails and links stored in text files to send notifications to subscribers. It also uses a Telegram token and chat ID for sending data via Telegram and uses a folder named 'tracker' to keep track of the program's progress.

## File Structure
 * conf: contains _links.txt and _emails.txt files where you add your links and emails respectively
 * tracker: folder created automatically with the program to keep track of the program's progress
 * installer.py: script to install the program's dependencies
 * launcher.py: script to start the program
 * settings.json: file that contains the program's settings

## Dependencies
 * psutil
 * urllib3
 * requests
 * colorama
 * termcolor
 * bs4

## Usage
 * Run the installer script to install the dependencies.
 **``` python installer.py```
 * Create _emails.txt and _links.txt files in the conf folder and add your emails and links respectively.
 * Run the launcher script to start the program.
 * You can customize the program's settings by editing the settings.json file.
 **``` python launcher.py```
 
## Classes and functions

***AppSettings:
 * convert_file_to_list(path, cleaned): takes a file path and returns a list of the file's content.
 * save_text(pt, nm, tp, ln): saves a text on a specific path.
 * create_folder(after_f_path): creates a folder in a specific path.
 * send_telegram_message(message, telegramToken, telegramChatId): sends telegram message.
 * prepareFiles(): function that creates necessary folders and files.

## Additional notes
 * The program uses a global variable called FOLDER_PATH which gets the current directory of the script and it's used to locate files.
 * The program is designed to be run from the command line and that it expects certain files and folders to be present in the program's directory.
 * The program uses multi-threading to increase performance and the number of threads can be configured in the settings.json file.
 * The program also uses a Telegram token and chat ID to send data via Telegram, this can also be configured in the settings.json file.
 * The program uses an 'tracker' folder to keep track of the program's progress, this folder is created automatically when the program starts.
 * The program has a built-in error handling mechanism that allows it to handle errors and continue running.

## Potential improvements
 * Adding more features like sending notifications through different platforms.
 * Adding more options to customize the program's behavior.
 * Improving the program's error handling mechanism.
 * Optimizing the program's performance.

