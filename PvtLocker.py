# Make sure that the file you want to upload is in the same directory as this program file
# Any Downloaded file will be found where the program file is kept
# I tried to create a executable but failed as pyrebase4 is showing error with pyinstaller
# would be very helpfull if someone can find a way to create a executable for this program.
import pyrebase
import time
import sys
import os


logo = '''
 ____        _      _               _             
|  _ \__   _| |_   | |    ___   ___| | _____ _ __ 
| |_) \ \ / / __|  | |   / _ \ / __| |/ / _ \ '__|
|  __/ \ V /| |_   | |__| (_) | (__|   <  __/ |   
|_|     \_/  \__|  |_____\___/ \___|_|\_\___|_|   
                                                  
'''

PvtServiceJson = {} #should contain the data of your firebase service account json file

'''

Include PvtServiceJson inside the config also
stating:
"serviceAccount": PvtServiceJson

'''
firebaseConfig = {} #Should contain your firebase config

class fcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'


fire = pyrebase.initialize_app(firebaseConfig)
authentication = fire.auth()
storage = fire.storage()

class Storage():
    email_id = ""
    sign_check = False
    token = ""

def sigin():
    email = input(f"\n{fcolors.GREEN + '[*]' + fcolors.ENDC} Enter your email ID >> ")
    password = input(f"{fcolors.GREEN + '[*]' + fcolors.ENDC} Enter you password >> ")
    try:
        user = authentication.sign_in_with_email_and_password(email, password)
        Storage.sign_check = True
        Storage.email_id = email
        Storage.token = user['idToken']

    except Exception as e:
        print(e)

def signup():
    email = input(f"\n{fcolors.GREEN + '[*]' + fcolors.ENDC} Enter your email ID >> ")
    password = input(f"{fcolors.GREEN + '[*]' + fcolors.ENDC} Enter you password >> ")

    if len(password) < 6:
        print("Too Weak Password! Try Again")
        sys.exit()

    user = authentication.create_user_with_email_and_password(email, password)
    token = user['idToken']
    try:
        authentication.send_email_verification(token)

    except Exception:
        authentication.delete_user_account(token)
        print(fcolors.RED + "\n[ERROR] Check connectivity; Make sure u are using a valid email; Please check if u already have a account or not" + fcolors.ENDC)
    
    print(fcolors.RED + "You have 60 seconds to verify your account\n" + fcolors.ENDC)
    
    cnt = 60
    check = False
    now = time.time()
    final = 0

    while final != now + 60:
        final = time.time()
        data = authentication.get_account_info(user['idToken'])
        verify = data['users'][0]['emailVerified']

        if verify == True:
            check = True
            break

        else:
            if cnt != 0:
                print(fcolors.BLUE +"Waiting for verification... \r" + fcolors.ENDC, end="")
                cnt = cnt - 1
            
            elif cnt == 0:
                check = False
                break
                
            now += 1
    
    if check == True:
        print(fcolors.GREEN+"Sign Up completed; you can sign in now :)"+fcolors.ENDC)
        print()
    
    else:
        print(fcolors.GREEN+"Please sign up again and verify your account this time"+fcolors.ENDC)
        authentication.delete_user_account(token)


# ------- Main Body --------
print(fcolors.RED + logo + fcolors.ENDC)
print(fcolors.YELLOW + "\nChoices Available\n" + fcolors.ENDC)
print(f"{fcolors.GREEN + '[1]' + fcolors.ENDC} Sign In")
print(f"{fcolors.GREEN + '[2]' + fcolors.ENDC} Sign Up\n")

choice = int(input(f"{fcolors.YELLOW + '[*]' + fcolors.ENDC} Please enter your choice >> "))
if choice == 1:
    sigin()

    if Storage.sign_check == True:
        task = input(fcolors.YELLOW + "\nDo you want to upload a file or download a file ?[u/d] >> " + fcolors.ENDC)

        if task == "u" or task == "U":
            filename = input(f"\n{fcolors.BLUE + '[*]' + fcolors.ENDC} Enter the path of the file >> ")
            
            if os.path.exists(filename):
                try:
                    print("\nUploading...")
                    storage.child(Storage.email_id.replace(".", "_")).child(filename).put(filename, Storage.token)
                    print(f"{fcolors.RED+'[*]'+fcolors.ENDC} Uploaded successfully\n")

                except Exception as e:
                    print(e)

        elif task == "d" or task == "D":
            dat = storage.child(f'{Storage.email_id.replace(".", "_")}').list_files()
            print(fcolors.BLUE + "\nFiles Available for Download\n" + fcolors.ENDC)

            for i in dat:
                lst = str(i).split(" ")[2].split("/")
                if lst[0] == Storage.email_id.replace(".", "_"):
                    print(fcolors.GREEN + lst[1].rstrip(">") + fcolors.ENDC)
            
            fl = input(f"\n{fcolors.BLUE + '[*]' + fcolors.ENDC} Enter the file you want to download >> ")
            print("\nDownloading...")
            storage.download(filename=fl, path=f"{Storage.email_id.replace('.', '_')}/{fl}")
            print(f"{fcolors.RED+'[*]'+fcolors.ENDC} Downloaded successfully\n")

elif choice == 2:
    signup()

else:
    print("\nInvalid Choice!")
