import os
import time
import aiohttp
import asyncio
from dotenv import load_dotenv
from colorama import Fore, Style


def clear_screen():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def def_leppard_banner():
    return f"""{Fore.RED}
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


load_dotenv()

token = os.getenv("TOKEN")
proxy_url = os.getenv("PROXY")


async def check_username_availability(username, session):
    headers = {
        "authority": "discord.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,en;q=0.8",
        "authorization": f"{token}",
    }

    url = "https://discord.com/api/v9/users/@me/pomelo-attempt"

    data = {"username": username}

    retries = 3
    for attempt in range(retries):
        async with session.post(
            url, headers=headers, json=data, proxy=proxy_url
        ) as response:
            if response.status == 200:
                result = await response.json()
                if not result.get("taken"):
                    print(f"{Fore.GREEN}[Available] {username}{Style.RESET_ALL}")
                break
            elif response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                print(
                    f"\n{Fore.RED}[Rate limited] Waiting for {retry_after} seconds.{Style.RESET_ALL}"
                )
                await asyncio.sleep(retry_after)
            else:
                print(
                    f"\n{Fore.RED}[Check Failed For: '{username}'] Status code: {response.status}.{Style.RESET_ALL}"
                )


with open("words.txt", "r") as file:
    usernames = file.read().splitlines()

requests_per_minute = 10
tokens_per_request = 1
max_tokens = requests_per_minute


async def process_usernames(usernames):
    async with aiohttp.ClientSession() as session:
        tokens_available = max_tokens
        last_request_time = time.time()

        for username in usernames:
            current_time = time.time()
            elapsed_time_since_last_request = current_time - last_request_time

            tokens_to_add = elapsed_time_since_last_request * (requests_per_minute / 60)
            tokens_available = min(tokens_available + tokens_to_add, max_tokens)

            if tokens_available >= tokens_per_request:
                await check_username_availability(username, session)
                last_request_time = time.time()
                tokens_available -= tokens_per_request

            else:
                sleep_duration = (tokens_per_request - tokens_available) / (
                    requests_per_minute / 60
                )
                await asyncio.sleep(sleep_duration)


async def main():
    clear_screen()
    print(def_leppard_banner())  # Display the Def Leppard ASCII banner
    await process_usernames(usernames)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
