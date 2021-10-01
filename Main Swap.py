import subprocess, requests, time, os
import os
import datetime
import sys
import json
import time
import ctypes
import socket
import smtplib
import random
import requests
import threading
from colorama import init
from colorama import Fore, Back, Style
from discord_webhook import DiscordWebhook, DiscordEmbed
from threading import Thread
init()

benner = '[\x1b[36m?\x1b[39m]'
benner1 = '[\x1b[32m+\x1b[39m]'

  

class XTG:
    def __init__(self):
        self.Threading()


    with open('tokens.txt', 'r') as file:
        xbox_user_tokens = file.read().splitlines()
        if len(xbox_user_tokens) < 1:
            Clear()
            print('No Tokens Found In tokens.txt')
            time.sleep(5)
            os._exit(0)


    def Grab_Tokens(self, token):
        global xbox_grabbed

        try:
            json = {'RelyingParty': 'http://xboxlive.com', 'TokenType': 'JWT', 'Properties': {'UserTokens': [token], 'SandboxId': 'RETAIL'}}
            response = requests.post('https://xsts.auth.xboxlive.com/xsts/authorize', json=json)

            if response.status_code == 200:
                token = 'XBL3.0 x={};{}'.format(response.json()['DisplayClaims']['xui'][0]['uhs'], response.json()['Token'])

                headers = {'Authorization': token}
                response = requests.get('https://accounts.xboxlive.com/users/current/profile', headers=headers)

                if '"gamerTag":null' not in response.text:
                    xbox_tokens.append(token)
                    xbox_grabbed += 1
                else:
                    pass
            else:
                pass
        except:
            pass



    def Threading(self):
        for token in self.xbox_user_tokens:
            thread = Thread(target=self.Grab_Tokens, args=(token,))
            thread.setDaemon(True)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


class MS:
    def __init__(self):
        self.printed = 0
        self.attempts = 0
        self.other = 0
        self.rl = 0
        self.rs = 0
        
        

    def Reserve(self):
        while True:
            for token in xbox_tokens:
                json = {'classicGamertag': gamertag, 'reservationId': xuid, 'targetGamertagFields': 'classicGamertag'}
                headers = {'x-xbl-contract-version': '1', 'Authorization': token}

                response = requests.post('https://gamertag.xboxlive.com/gamertags/reserve', json=json, headers=headers)

                if response.status_code == 409:
                    self.attempts += 1
                    print('{} attempts - [\x1b[32m{}\x1b[39m] | RL - [\x1b[31m{}\x1b[39m] | r/s - [\x1b[36m{}\x1b[39m]'.format(benner1, self.attempts, self.rl, self.rs), end='\r')                   
                    self.RPS_Threading()
                elif response.status_code == 200:
                    if self.printed == 0:
                        self.printed += 1
                        print('\n[\x1b[31m!\x1b[39m] {} is avivable\n'.format(gamertag))
                        time.sleep(1)
                        print('{} {} Has Been reserved to {}'.format(benner1, gamertag, xuid))
                        print('{} Attempts Taken To Reserve - {}'.format(benner1, self.attempts))
                        self.SendHook(gamertag, self.attempts)
                elif response.status_code == 429:
                    self.rl += 1
                else:
                    self.other += 1

                
 

    def RPS(self):
        while True:
            before = self.attempts
            time.sleep(1)
            self.rs = self.attempts - before
        

    def Threading(self):
        for _ in range(thread_count):
            thread = Thread(target=self.Reserve)
            thread.start()
                        
    
    def SendHook(self, gamertag, elapsed):
        webhook = DiscordWebhook(url='discord Webhook', username="Claimed!")
        embed = DiscordEmbed(title='Main Swap!', color='ffffff')
        embed.set_footer(text='Made By doomed#8348')
        embed.add_embed_field(name="𝙂𝙖𝙢𝙚𝙧𝙩𝙖𝙜", value="`{}`".format(gamertag), inline=False)
        embed.add_embed_field(name="𝘼𝙩𝙩𝙚𝙢𝙥𝙩𝙨", value="`{}`".format(elapsed), inline=False)
        embed.set_thumbnail(url='')
        webhook.add_embed(embed)
        response = webhook.execute()      
        

    def RPS_Threading(self):
        thread = Thread(target=self.RPS)
        thread.setDaemon(True)
        thread.start()
 

if __name__ == '__main__':
    threads = []
    xbox_tokens = []
    ms_tokens = []
    xbox_grabbed = 0
    XTG()
print('{} Tokens Authd - {}'.format(benner, xbox_grabbed))
print('\n{}'.format(benner), end='');gamertag = input(' gamertag: ')
print('{}'.format(benner1), end='');xuid = input(' XUID: ')
print('{}'.format(benner1), end='');thread_count = int(input(' Thread Count: '));print()
MS().Threading()
