import os, requests, urllib3, concurrent.futures, colorama, json, pathlib, threading, random, math, time
from time import sleep
from bs4 import BeautifulSoup
from termcolor import colored as cld

''' START INIT GLOBAL CLASSES '''
colorama.init()
urllib3.disable_warnings()
''' END INIT GLOBAL CLASSES '''

''' START SETTINGS '''
class AppSettings:
    # CONVERT TEXT FILE TO LIST
    def convert_file_to_list(path,cleaned):
        filelist_ = []
        mypath = pathlib.Path(path)
        with open(path,'r',encoding='utf-8',errors='ignore') as file :
            fileexists = True
            fileexists = mypath.stat().st_size
            if (fileexists) :
                for i in file : 
                    i = i.replace('\n','')
                    filelist_.append(i)
            else: 
                print("file doesn't exist",path)
        if cleaned == True :
            return [*set(filelist_)]
        if cleaned == False :
            return filelist_
    # SAVE TEXT ON PATH
    def save_text(pt, nm, tp, ln):
        f = open(f"{FOLDER_PATH}\\{pt}\\{nm}.{tp}", "a+", encoding="utf-8", errors="ignore")
        f.write(ln)
        f.close()
        return "SAVED"
    # CREATE FOLDER
    def create_folder(after_f_path):
        return pathlib.Path(f'{FOLDER_PATH}\\{after_f_path}').mkdir(parents=True, exist_ok=True)
    # Send Telegram Message
    def send_telegram_message(message, telegramToken, telegramChatId):
        url = f'https://api.telegram.org/bot{telegramToken}/sendMessage?chat_id={telegramChatId}&text={message}'
        return requests.get(url)
''' END SETTINGS '''

''' START MAIN VARIABLES '''
FOLDER_PATH = str(pathlib.Path(__file__).parents[0])
''' END MAIN VARIABLES '''


''' START MAIN FUNCTIONS '''
def prepareFiles():
    rezults_folder = None
    if not os.path.exists(f'{FOLDER_PATH}\\conf'):
        AppSettings.create_folder('conf')
        print(cld("Please add links and emails to _links.txt and _emails.txt files on conf Folder","red"))
    if not os.path.exists(f'{FOLDER_PATH}\\tracker'):
        AppSettings.create_folder('tracker')   
    if not os.path.exists(f'{FOLDER_PATH}\\conf\\_links.txt'):
        print(cld("Please add links to _links.txt file","red"))
    if not os.path.exists(f'{FOLDER_PATH}\\conf\\_emails.txt'):
        print(cld("Please add emails to _emails.txt file","red"))
    rezults_folder = "track_" + str(random.randint(1000000000,9999999999))
    try:
        AppSettings.create_folder("tracker\\"  + rezults_folder)
        AppSettings.save_text(f"tracker\\{rezults_folder}", "SENT", "csv", "Email,FormID\n")
        AppSettings.save_text(f"tracker\\{rezults_folder}", "NOT_SENT", "csv", "Email,FormID\n")
    except Exception as e:
        print(cld(f"[ERROR] : Cant Create Rezult Folder ==> {e}","red"))
    return rezults_folder

def parseJsonSettings():
    with open(f"{FOLDER_PATH}\\settings.json", "r", encoding="utf-8", errors="ignore") as f:
        json_str = f.read()
    userSettings = json.loads(json_str)
    threadsNum = userSettings['Threads'] # 1 - 100
    telegramData = userSettings['SendTelegramData']  # True or False
    telegramToken = userSettings['TelegramToken'] # telegram bot token
    telegramChatId = userSettings['TelegramChatID'] # telegram chat id
    sendDublicatedEmails = userSettings['SendDublicatedEmails'] # True or False
    maxDataErrorsCount = userSettings['MaxDataErrorsCount'] # 1 - 100
    timeBetweenRequests = userSettings['TimeBetweenRequests'] # 100 ms
    maxEmailRetries = userSettings['MaxEmailRetries'] # 1 - 100
    updateFormsEach = userSettings['UpdateFormsEach'] # 1 - 100
    return threadsNum, telegramData, telegramToken, telegramChatId, sendDublicatedEmails, maxDataErrorsCount, timeBetweenRequests, maxEmailRetries, updateFormsEach

''' End MAIN FUNCTIONS '''

'''  START MAIN CLASSES'''


class Sender:
    def __init__(self,tempObj):
        global formsObjects
        self.random_index = random.randint(0, len(formsObjects)-1)
        self.form_object = formsObjects[self.random_index]
        self.email = tempObj['Email']
        self.sent = tempObj['Sent']
        self.retried = tempObj['Retried']
        self.status = False
        
        self.send()

        if self.sent == False:
            if self.retried < maxEmailRetries:
                # retry with another form
                self.random_index = random.randint(0, len(formsObjects)-1)
                self.form_object = formsObjects[self.random_index]
                self.send()

        if self.status == True:
            self.sent = True


    def send(self):
        self.retried += 1
        try:
            response = requests.get(f'https://www.tfaforms.com/{self.form_object["Id"]}')
            if response.status_code == 200:
                html = response.content
                soup = BeautifulSoup(html, 'html.parser')
                tfa_dbCounters = soup.find('input', {'name': 'tfa_dbCounters'}).get('value')
                tfa_dbFormId = soup.find('input', {'name': 'tfa_dbFormId'}).get('value')
                tfa_dbResponseId = soup.find('input', {'name': 'tfa_dbResponseId'}).get('value')
                tfa_dbControl = soup.find('input', {'name': 'tfa_dbControl'}).get('value')
                tfa_dbWorkflowSessionUuid = soup.find('input', {'name': 'tfa_dbWorkflowSessionUuid'}).get('value')
                tfa_dbTimeStarted = soup.find('input', {'name': 'tfa_dbTimeStarted'}).get('value')
                tfa_dbVersionId = soup.find('input', {'name': 'tfa_dbVersionId'}).get('value')
                meta_list = {
                    'tfa_1873': self.email,
                    'tfa_dbCounters': tfa_dbCounters,
                    'tfa_dbFormId': tfa_dbFormId,
                    'tfa_dbResponseId': tfa_dbResponseId,
                    'tfa_dbControl': tfa_dbControl,
                    'tfa_dbWorkflowSessionUuid': tfa_dbWorkflowSessionUuid,
                    'tfa_dbTimeStarted': tfa_dbTimeStarted,
                    'tfa_dbVersionId': tfa_dbVersionId
                    }
                res = requests.post(
                'https://www.tfaforms.com/api_v2/workflow/processor',
                data=meta_list,
                verify=False,
                timeout=10
                )
                if res.status_code == 200:
                    self.status = True
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(cld(f"[EXPTION] : Cant Send Email ==> {e}","cyan"))
            return False




def forceSendEmailSingleEmail(tempObj):
    global sentCounter, totalListCount, failCounter, formsObjects, badFormsCounter
    senderObj = Sender(tempObj)
    if senderObj.status == True:
        print(cld(f"[{sentCounter}/{totalListCount}][SENT({sentCounter})] : {senderObj.email} = FROM => {senderObj.form_object['Id']}","green"))
        formsObjects[senderObj.random_index]['Sent'] += True
        sentCounter += 1
        AppSettings.save_text(f"tracker\\{rezults_folder}", "SENT", "csv", f"{senderObj.email},{senderObj.form_object['Id']}\n")
        return True
    else:
        try:
            print(cld(f"[{sentCounter} / {totalListCount}][RETRIING({senderObj.retried})] : {senderObj.email} = FROM => {senderObj.form_object['Id']}","red")) 
            if formsObjects[senderObj.random_index]['ErrorsNum'] < maxDataErrorsCount:
                formsObjects[senderObj.random_index]['ErrorsNum'] += 1
                forceSendEmailSingleEmail(tempObj)
            else:
                print(cld(f"[BADFORMS] : {senderObj.email} = FROM => {senderObj.form_object['Id']}","blue"))
                # save bad form to bad forms list
                try:
                    if requests.get(f'https://www.tfaforms.com/{senderObj.form_object["Id"]}').status_code != 200:
                        # try to delete not working form from original list of forms
                        try:
                            formsObjects.remove(senderObj.form_object)
                        except Exception as e:
                            print(cld(f"[EXPTION] : Cant Remove Form ==> {e}","cyan"))
                        AppSettings.send_telegram_message(f"FORMERROR : {rezults_folder}\nID: {senderObj.form_object['Id']}", telegramToken, telegramChatId)
                        badFormsCounter += 1
                except Exception as e:
                    print(cld(f"[EXPTION] : Cant Save Form Error ==> {e}","cyan"))
        except Exception as e:
            print(cld(f"[EXPTION] : Cant Send Email ==> {e}","cyan"))
    if senderObj.sent == False:
        failCounter += 1
        AppSettings.save_text(f"tracker\\{rezults_folder}", "NOT_SENT", "csv", f"{senderObj.email},{senderObj.form_object['Id']}\n")
        print(cld(f"[{sentCounter}/{totalListCount}][NOT_SENT({failCounter})] : {senderObj.email} = FROM => {senderObj.form_object['Id']}","red"))
        return False
    else:
        return True

def updateFormsObjects():
    global updateFormsEach
    while formUpdator:
        # code to update formsObjects list
        print(cld(f"[INFO] : Updating Forms List","yellow"))
        for form in  formsObjects:
            if requests.get(f'https://www.tfaforms.com/{form["Id"]}').status_code != 200:
                # try to delete not working form from original list of forms
                try:
                    formsObjects.remove(form)
                except Exception as e:
                    print(cld(f"[EXPTION] : Cant Remove Form ==> {e}","cyan"))
        time.sleep(updateFormsEach) # sleep for updateFormsEach Seconds


if __name__ == "__main__":
    badFormsCounter = 0
    # parse json string
    threadsNum, telegramData, telegramToken, telegramChatId, sendDublicatedEmails, maxDataErrorsCount, timeBetweenRequests, maxEmailRetries, updateFormsEach = parseJsonSettings()
    # prepare files
    rezults_folder = prepareFiles()
    if rezults_folder != None:
        print(cld(f"[INFO] : Results Folder ==> {rezults_folder} Created","yellow"))
    # get required text files and convert them to lists
    emailsList = AppSettings.convert_file_to_list(f'{FOLDER_PATH}\\conf\\_emails.txt',cleaned=(False if sendDublicatedEmails == "True" else True)) # emails list
    formsList = AppSettings.convert_file_to_list(f'{FOLDER_PATH}\\conf\\_links.txt',cleaned=True) # forms list
    # convert list ti objects {form_id, errorsNum, status}
    formsObjects = []
    for form in formsList:
        if requests.get(f'https://www.tfaforms.com/{form}').status_code == 200:
            formsObjects.append({
                "Id" : form, 
                "ErrorsNum" : 0,
                "Sent" : 0,
                "Status" : True
                })
        else:
            badFormsCounter += 1
            print(cld(f"[BADFORMS] : {form}","blue"))
            AppSettings.save_text(f"tracker\\{rezults_folder}", "BAD_FORMS", "csv", f"{form}\n")
            AppSettings.send_telegram_message(f"FORMERROR : {rezults_folder}\nID{form}", telegramToken, telegramChatId)

    # convert list to objects {email, sent, retried}
    emailsObjects = []
    for email in emailsList:
        emailsObjects.append({
            "Email" : email,
            "Sent" : False,
            "Retried" : 0
            })
    # counters
    sentCounter = 1
    failCounter = 0
    totalListCount = len(emailsObjects)
    formUpdator = True

    update_thread = threading.Thread(target=updateFormsObjects)
    update_thread.start()

    # start sending emails with concurrent threads and moniroting as header of terminal
    with concurrent.futures.ThreadPoolExecutor(max_workers=threadsNum) as executor:
        rezults = executor.map(forceSendEmailSingleEmail, emailsObjects)
                
    good_forms_still = []
    for obj in formsObjects:
        if requests.get(f'https://www.tfaforms.com/{obj["Id"]}').status_code == 200:
            good_forms_still.append(obj)
            AppSettings.save_text(f"tracker\\{rezults_folder}", "GOOD_FORMS", "csv", f"{obj['Id']}\n")
    
    print(cld(f"[INFO] : Sent Emails ==> {sentCounter-1}","yellow"))
    print(cld(f"[INFO] : Failed Emails ==> {failCounter}","yellow"))
    print(cld(f"[INFO] : Total Emails ==> {totalListCount}","yellow"))
    print(cld(f"[INFO] : Good Forms ==> {len(good_forms_still)}","yellow"))
    print(cld(f"[INFO] : Bad Forms ==> {badFormsCounter}","yellow"))
    print(cld(f"[INFO] : Results Folder ==> {rezults_folder}","yellow"))
    print(cld(f"[INFO] : Done","yellow"))
    time.sleep(5)
    # stop formUpdator
    formUpdator = False
    # send telegram message
    AppSettings.send_telegram_message(f"Done : {rezults_folder}\nSent Emails ==> {sentCounter-1}\nFailed Emails ==> {failCounter}\nTotal Emails ==> {totalListCount}\nGood Forms ==> {len(good_forms_still)}\nBad Forms ==> {badFormsCounter}", telegramToken, telegramChatId)
    # send files to telegram
    send_telegram_file = requests.post(f'https://api.telegram.org/bot{telegramToken}/sendDocument?chat_id={telegramChatId}', files={'document': open(f'{FOLDER_PATH}\\tracker\\{rezults_folder}\\NOT_SENT.csv', 'rb')})
    send_telegram_file = requests.post(f'https://api.telegram.org/bot{telegramToken}/sendDocument?chat_id={telegramChatId}', files={'document': open(f'{FOLDER_PATH}\\tracker\\{rezults_folder}\\GOOD_FORMS.csv', 'rb')})
    # ask user to open results folder
    if input(cld(f"[INFO] : Open Results Folder ? (y/n) : ","blue")).lower() == "y":
        os.startfile(f"{FOLDER_PATH}\\tracker\\{rezults_folder}")
    # ask user if need to exit
    if input(cld(f"[INFO] : Exit ? (y/n) : ","red")).lower() == "y":
        exit()