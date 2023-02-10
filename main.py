# Modules checker
import os
try:
    import requests, colorama, pystyle
except ModuleNotFoundError:
    os.system("pip install requests colorama pystyle")

# Main
import requests, pystyle, yaml, time, threading, ctypes
from colorama import Fore, init
init(convert=True)

valid_tokens = 0
locked_tokens = 0
print_lock = threading.Lock()
def info(text):
    print(f"({Fore.LIGHTYELLOW_EX}#{Fore.RESET}) {Fore.LIGHTYELLOW_EX}{text}{Fore.RESET}")
def error(text):
    print(f"({Fore.LIGHTRED_EX}ERR{Fore.RESET}) {Fore.RED}{text}{Fore.RESET}")
def cinput(text):
    content = input(
        f"({Fore.LIGHTCYAN_EX}~{Fore.RESET}) {text}{Fore.CYAN} >>{Fore.RESET} ")
    return content
def main():
    os.system("cls")
    info("Loading config...")
    config = yaml.safe_load(open("config.yml"))["settings"]
    # Tokens
    info("Loading tokens...")
    if open("tokens.txt").read() == "":
        error("No tokens found in tokens.txt")
        time.sleep(3)
        exit(0)
    else:
        tokens = open("tokens.txt").read().splitlines()
        for i in tokens:
            if ":" in i:
                tokens[tokens.index(i)] = i.split(":")[2]
    os.system("cls")
    title()
    # Proxy
    proxyless = cinput("Proxyless? (N/Y)")
    if proxyless.lower() == "n":
        if config["rotating-proxy"] != "":
            proxy = config["rotating-proxy"]
        else:
            proxy = cinput("Rotating proxy (user:pass@host:port)")
            try:
                proxies = {
                    "http": "http://"+proxy,
                    "https": "http://"+proxy
                }
                requests.get("https://google.com/",proxies=proxies)
            except:
                error("Invalid proxy")
                time.sleep(3)
                main()
    elif proxyless.lower() == "y":
        proxy = None
    else:
        error("Invalid input")
        time.sleep(2)
        main()

    # Threads
    num_threads = cinput("Threads (number)")
    try:
        num_threads = int(num_threads)
    except:
        error("Invalid input")
        time.sleep(3)
        main()
    os.system("cls")
    title()
    threading.Thread(target=update_title, args=(tokens,)).start()
    # Checking tokens
    if num_threads == 1:
        check_tokens(tokens,proxy)
    else:
        tokens_per_thread = [tokens[i::num_threads] for i in range(num_threads)]
        for tokens in tokens_per_thread:
            thread = threading.Thread(target=check_tokens, args=(tokens,proxy))
            thread.start()
    input(f"({Fore.LIGHTYELLOW_EX}#{Fore.RESET}) {Fore.LIGHTYELLOW_EX}Press ENTER to exit.{Fore.RESET}\n")
    exit()
def update_title(tokens):
    while True:
        global locked_tokens
        global valid_tokens
        ctypes.windll.kernel32.SetConsoleTitleW(f"Tokens: {len(tokens)} | Valid: {valid_tokens} | Locked: {locked_tokens}")
        time.sleep(0.1)
def title():
    print(pystyle.Center.XCenter(Fore.CYAN+
f'''$$\   $$\  $$$$$$\  $$\    $$\  $$$$$$\  
$$$\  $$ |$$  __$$\ $$ |   $$ |$$  __$$\ 
$$$$\ $$ |$$ /  $$ |$$ |   $$ |$$ /  $$ |
$$ $$\$$ |$$ |  $$ |\$$\  $$  |$$$$$$$$ |
$$ \$$$$ |$$ |  $$ | \$$\$$  / $$  __$$ |
$$ |\$$$ |$$ |  $$ |  \$$$  /  $$ |  $$ |
$$ | \$$ | $$$$$$  |   \$  /   $$ |  $$ |
\__|  \__| \______/     \_/    \__|  \__|
                        {Fore.LIGHTCYAN_EX}Made by Mouad#9475{Fore.RESET}'''
    +Fore.RESET))

def print_token(token, isvalid):
    config = yaml.safe_load(open("config.yml"))
    if config["settings"]["censor-tokens"] == True:
        token = f"{token.split('.')[0]}.######.######################################"
    if isvalid == True:
        with print_lock:
            print(f"({Fore.LIGHTGREEN_EX}+{Fore.RESET}) Valid token: {Fore.GREEN}{token}{Fore.RESET}")
    else:
        with print_lock:
            print(f"({Fore.LIGHTGREEN_EX}+{Fore.RESET}) Locked token: {Fore.GREEN}{token}{Fore.RESET}")
def check_tokens(tokens, proxy):
    global locked_tokens
    global valid_tokens
    for token in tokens:
        session = requests.Session()
        if proxy != None:
            session.proxies = {
                "http": "http://"+proxy,
                "https": "http://"+proxy
            }
        headers = {
            "authorization": token
        }
        r = session.get("https://discord.com/api/v9/users/@me/library",headers=headers)
        try:
            if r.json() == []:  
                with open("output/valid_tokens.txt","a+") as f:
                    if len(f.read()) == 0:
                        f.write(token)
                    else:
                        f.write(token+"\n")
                valid_tokens += 1
                print_token(token, True)
            else:
                with open("output/locked_tokens.txt","a+") as f:
                    if len(f.read()) == 0:
                        f.write(token)
                    else:
                        f.write(token+"\n")
                locked_tokens += 1
                print_token(token, False)
        except:
            with open("output/unknown_tokens.txt","a+") as f:
                if len(f.read()) == 0:
                    f.write(token)
                else:
                    f.write(token+"\n")
            locked_tokens += 1
            print_token(token, False)

if __name__ == "__main__":   
    main()