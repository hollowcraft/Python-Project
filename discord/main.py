import os
from datetime import datetime
import json
import discord
import sys
import pyttsx3
import urllib.request
import pygame
import time

# --- Lecture du token depuis token.txt ---
with open(r"C:\Users\Adam\Desktop\Shortcut\Tools\autre\token.txt", "r", encoding="utf-8") as f:
    BOT_TOKEN = f.read().strip()

# --- Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

client = discord.Client(intents=intents)



Admin = {
    "hollow_craft",
    "basil_lique"
}
#Number to letter
def ascii(n):
    return chr(ord('a') + n - 1)
#OnStartup
@client.event
async def on_ready():
    # Emoji retiré pour éviter UnicodeEncodeError
    print(f"Connected to {client.user}")
    print("-----")
    engine = pyttsx3.init()
    engine.setProperty("volume", 1.0) # volume (0.0 à 1.0)
    engine.say("Discord Bot Ready")
    engine.runAndWait()

@client.event
async def on_message(message):
    if message.content.startswith("/"):
        message.content = message.content[1:]
    split_message = message.content.split()
    if message.author == client.user:
        return
    # Debug : affiche tous les messages reçus
    print(f"{message.author}: {message.content}")
    #enlève les curse du deuxième joueur
    if message.content == "remove curse":
        #enlève les curse du deuxième joueur
        if message.guild is None:
            save_file = r"C:\Users\Adam\AppData\LocalLow\Hopoo Games, LLC\Risk of Rain 2\ProperSave\Saves\9bd28171-08b2-473c-bd8e-0df603743fef.json"
            with open(save_file, "r", encoding="utf-8") as f:
                save_content = json.load(f)
            for i in range(len(save_content["p"][1]["m"]["i"]["i"])):
                if save_content["p"][1]["m"]["i"]["i"][i]["i"] == 216:
                    if save_content["p"][1]["m"]["i"]["i"][i]["c"] < 0:
                        print(save_content["p"][1]["m"]["i"]["i"][i]["c"])
                        text = "Curse already removed"
                    else:
                        text = f"{save_content["p"][1]["m"]["i"]["i"][i]["c"]} Curse removed!"
                        save_content["p"][1]["m"]["i"]["i"][i]["c"] = -1000
                        print(save_content["p"][1]["m"]["i"]["i"][i]["c"])
            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(save_content, f, ensure_ascii=False, indent=4)    
    #JUST DONT TYPE THIS
    elif message.content == "save nuke":
            with open(save_file, "r", encoding="utf-8") as f:
                text = str(json.load(f))
                a = 2000
                result = [text[i:i+a] for i in range(0, len(text), a)]
                for i in result:
                    await message.channel.send(i)
                print(result)
                text = "done"
    #Start Steam game
    elif split_message[0] == "steam":
        if message.author.name in Admin:
            with open(r"C:\Users\Adam\Desktop\Mes Projects\python\discord\steam_game.json", "r", encoding="utf-8") as f:
                steam_game = json.load(f)
            if split_message[1] in steam_game:
                split_message[1] = steam_game[split_message[1]]
            print("Launching game id: "+split_message[1])
            try:
                os.startfile("steam://rungameid/"+split_message[1])
                text = "Launching game..."
            except:
                text = "Error launching game."
            
        else:
            text = "You don't have permission to use this command."
    #Start server
    elif split_message[0] == "server":
        if split_message[1] == "help" or split_message[1] == "?" or split_message[1] == None:
            text = "Available servers: \n- Portal Knights"
        elif split_message[1] == "portal":
            os.startfile(r"C:\Program Files (x86)\Steam\steamapps\common\Portal Knights\dedicated_server\pk_dedicated_server.exe")
            text = "Starting PK server..."
    #Request command
    elif split_message[0] == "request":
        name = f"{message.author.name} │ {datetime.now().strftime('%Y-%m-%d')}"
        with open(r"C:\Users\Adam\Desktop\Mes Projects\python\discord\request\\"+name, "a", encoding="utf-8") as f:
            f.write(f"{message.content}\n")
        text = "Thanks for your request :D"
        print(f"Request from {message.author.name} saved at {name}")
    #Help command
    elif split_message[0] == "help":
        text = open(r"C:\Users\Adam\Desktop\Mes Projects\python\discord\help.txt", "r", encoding="utf-8").read()
    #Ping the bot
    elif split_message[0] == "ping":
        text = "Pong!"
    #Text To Speech
    elif split_message[0] == "tts":
        text = ""
        engine = pyttsx3.init()
        engine.setProperty("volume", 1.0) # volume (0.0 à 1.0)
        engine.say(message.content[4:])
        engine.runAndWait()
    #Play audio 
    elif split_message[0] == "play":
        if split_message[1] != ".":
            urllib.request.urlretrieve(split_message[1], "audio.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("audio.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    #send to hugo
    elif split_message[0] == "send":
        if message.author.name in Admin:
            text = message.content[5:]
            message.channel.id = 1450942801175908434
    #Else HYPIIIE!!! 
    elif message.guild is None:
        text = "HYPIIIIE!!!"
    #Send response
    if text != "":
        print("boaternos: "+text)
        await message.channel.send(text)
        #print (message)
# --- Lancement du bot ---
client.run(BOT_TOKEN)