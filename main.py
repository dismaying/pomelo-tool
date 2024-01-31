"""
End-User License Agreement (EULA)

1. This script is provided as-is, without any warranties or guarantees.
2. You may use, modify, and distribute this script for personal or educational purposes.
3. Commercial use or distribution without explicit permission is prohibited.
4. The author is not responsible for any damages or liabilities resulting from the use of this script.

By using this script, you agree to abide by the terms of this license.

"""

"""
End-User License Agreement (EULA)

1. This script is provided as-is, without any warranties or guarantees.
2. You may use, modify, and distribute this script for personal or educational purposes.
3. Commercial use or distribution without explicit permission is prohibited.
4. The author is not responsible for any damages or liabilities resulting from the use of this script.

By using this script, you agree to abide by the terms of this license.

"""
import os
import time
import asyncio
import aiohttp
from dotenv import load_dotenv
from colorama import Fore, Style

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")
PROXY_URL = os.getenv("PROXY")

# Clear screen function
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Banner display function
def display_banner():
    banner = f"""{Fore.RED}
     ,
     Et           :                                 :                              
     E#t         t#,                               t#,               L.            
     E##t       ;##W.   j.                    i   ;##W.   j.         EW:        ,ft
     E#W#t     :#L:WE   EW,                  LE  :#L:WE   EW,        E##;       t#E
     E#tfL.   .KG  ,#D  E##j                L#E .KG  ,#D  E##j       E###t      t#E
     E#t      EE    ;#f E###D.             G#W. EE    ;#f E###D.     E#fE#f     t#E
  ,ffW#Dffj. f#.     t#iE#jG#W;           D#K. f#.     t#iE#jG#W;    E#t D#G    t#E
   ;LW#ELLLf.:#G     GK E#t t##f         E#K.  :#G     GK E#t t##f   E#t  f#E.  t#E
     E#t      ;#L   LW. E#t  :K#E:     .E#E.    ;#L   LW. E#t  :K#E: E#t   t#K: t#E
     E#t       t#f f#:  E#KDDDD###i   .K#E       t#f f#:  E#KDDDD###iE#t    ;#W,t#E
     E#t        f#D#;   E#f,t#Wi,,,  .K#D         f#D#;   E#f,t#Wi,,,E#t     :K#D#E
     E#t         G#t    E#t  ;#W:   .W#G           G#t    E#t  ;#W:  E#t      .E##E
     E#t          t     DWi   ,KK: :W##########Wt   t     DWi   ,KK: ..         G#E
     ;#t                           :,,,,,,,,,,,,,.                               fE
      :;                                                                          ,
{Style.RESET_ALL}
			┌─────────────────────────────┐
  	                   {time.strftime("%d/%m/%Y"):^11} |  Pomelo Tool
			└─────────────────────────────┘
"""
    print(banner)


# Function to check username availability
async def check_username_availability(username, session):
    headers = {
        "authority": "discord.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": TOKEN,
    }
    url = "https://discord.com/api/v9/users/@me/pomelo-attempt"
    data = {"username": username}

    async with session.post(url, headers=headers, json=data, proxy=PROXY_URL) as response:
        if response.status == 200:
            result = await response.json()
            if not result.get("taken"):
                print(f"{Fore.GREEN}[Available] {username}{Style.RESET_ALL}")
        elif response.status in [401, 403]:
            print(f"{Fore.YELLOW}[Access Denied] {username} - Status: {response.status}{Style.RESET_ALL}")
            # Stop further requests if token is invalid or access is forbidden
            return False
        elif response.status == 429:
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"{Fore.RED}[Rate limited] Seconds Remaining: {retry_after} {Style.RESET_ALL}")
            await asyncio.sleep(retry_after)
        else:
            print(f"{Fore.RED}[Check Failed] {username} - Status: {response.status}{Style.RESET_ALL}")
        return True

# Function to process usernames
async def process_usernames(usernames):
    async with aiohttp.ClientSession() as session:
        for username in usernames:
            success = await check_username_availability(username, session)
            if not success:
                break  # Stop processing if a 401 or 403 error occurs

# Main function
async def main():
    clear_screen()
    display_banner()
    with open("words.txt", "r") as file:
        usernames = file.read().splitlines()
    await process_usernames(usernames)

# Run the main function
asyncio.run(main())
