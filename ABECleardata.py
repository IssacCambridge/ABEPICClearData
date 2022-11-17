from sys import exit
import subprocess
import xmltodict
import shutil
from os import system, rename, remove, path, mkdir
from english_words import english_words_lower_set
from random import choice
from colorama import Fore, init
from time import sleep

file_paths = {
    "decodedplayerdata": f"{path.dirname(path.realpath(__file__))}/DecodedPlayerData",
    "newplayerdata": f"{path.dirname(path.realpath(__file__))}/NewPlayerData",
    "wipedplayerdata": f"{path.dirname(path.realpath(__file__))}/WipedPlayerData",
    "oldplayerdata": f"{path.dirname(path.realpath(__file__))}/OldPlayerData",
    "basepath": f"{path.dirname(path.realpath(__file__))}"
}
init(autoreset=True)

def clear_data():
    try:
        with open("com.rovio.gold.v2.playerprefs.xml", "r") as angrybirdsepic, open("template.xml", "r") as template:
            clear_data = "CgZwbGF5ZXIQARpGCgxwaWdneV9pc2xhbmQSGgoQaG90c3BvdF8wMDFfY2FtcBABIgQIARAPGhoKEGhvdHNwb3RfMDAxX2NhbXAQASIECAEQDyLOBgoQcGxheWVyX2ludmVudG9yeRIQCgpzdG9yeV9zaG9wEAEYARITCg1zdG9yeV9tYWlsYm94EAEYARIZChFjb21pY19jdXRzY2VuZV8wMRABGAEoARoQCgpleHBlcmllbmNlEAEYARoPCgRnb2xkEAEYutGLXTABGhUKCmx1Y2t5X2NvaW4QARiw0YtdMAEaHQoSZnJpZW5kc2hpcF9lc3NlbmNlEAEYv9GLXTABIhIKDGNsYXNzX2tuaWdodBABGAEqIwobYmlyZF93ZWFwb25fcmVkX3N3b3JkXzBzdGFyEAEYATgEMiUKHWJpcmRfb2ZmaGFuZF9yZWRfc2hpZWxkX3N0YXJ0EAEYATgEOhYKEHJlc291cmNlX2Zsb3RzYW0QARgEOhMKDXJlc291cmNlX3dvb2QQARgGOhcKEXJlc291cmNlX3NlYXNoZWxsEAEYBDoUCg5yZXNvdXJjZV9zdG9uZRABGANCFwoRaW5ncmVkaWVudF9iYW5hbmEQARgMQhYKEGluZ3JlZGllbnRfd2F0ZXIQARgIQhUKD2luZ3JlZGllbnRfdmlhbBABGAhSFgoOcmVjaXBlX2Zsb3RzYW0QARgBIAFSEwoLcmVjaXBlX3dvb2QQARgBIAFSFwoPcmVjaXBlX3NlYXNoZWxsEAEYASABUhQKDHJlY2lwZV9zdG9uZRABGAEgAVIVCg1yZWNpcGVfYmFuYW5hEAEYASABUhQKDHJlY2lwZV9zZWVkcxABGAEgAVIUCgxyZWNpcGVfd2F0ZXIQARgBIAFSEwoLcmVjaXBlX3ZpYWwQARgBIAFSGQoRcmVjaXBlX3NoaW55X3NhbmQQARgBIAFSIAoacmVjaXBlX3dlYXBvbl9yZWRfbGFuY2VfMDEQAhgBUh4KGHJlY2lwZV9wb3Rpb25faGVhbGluZ18wMBABGAFSFwoRcmVjaXBlX2hvdF90b21hdG8QARgBch0KE2Jhbm5lcl90aXBfbDFfcTFfczEQARgBIAYwBHIgChZiYW5uZXJfYmFubmVyX2wxX3ExX3MxEAEYASAGMARyGgoQYmFubmVyX2VtYmxlbV8wOBABGAEgBjAEigETCgtza2luX2tuaWdodBABGAEgASqVAQoIYmlyZF9yZWQQARqGAQoOcmVkX2JpcmRfc3RhcnQiEgoMY2xhc3Nfa25pZ2h0EAEYASojChtiaXJkX3dlYXBvbl9yZWRfc3dvcmRfMHN0YXIQARgBOAQyJQodYmlyZF9vZmZoYW5kX3JlZF9zaGllbGRfc3RhcnQQARgBOASKARMKC3NraW5fa25pZ2h0EAEYAiABMghwcm90b2J1ZjjY2NXyBboB4QcKB2RlZmF1bHQiCU5QQ19Qb3JreSIOTlBDX0FkdmVudHVyZXIiB05QQ19Mb3ciCE5QQ19IaWdoKg0KCU5QQ19Qb3JreRAAKhIKDk5QQ19BZHZlbnR1cmVyEAAqCwoHTlBDX0xvdxAAKgwKCE5QQ19IaWdoEABK0QEKCU5QQ19Qb3JreRIAKgQIABAAKgQIARAAMNfY1fIFOAJCEW5wY19mcmllbmRfcHJpbmNlSgBaiAEKEWJpcmRfYmFubmVyX3Bvcmt5EAIacQoSYmlyZF9iYW5uZXJfbWNjb29sch4KEmJhbm5lcl9mbGFnX3NldF8wNBACGAEgBigBMARyHAoQYmFubmVyX2VtYmxlbV8yMxACGAEgBigBMARyHQoRYmFubmVyX3RpcF9zZXRfMDQQAhgBIAYoATAEYABgAWACaAVwBY0B31gtfUraAQoOTlBDX0FkdmVudHVyZXISACoECAAQACoECAEQADDY2NXyBTgBQhVucGNfZnJpZW5kX2FkdmVudHVyZXJKAFqIAQoRYmlyZF9iYW5uZXJfcG9ya3kQARpxChJiaXJkX2Jhbm5lcl9tY2Nvb2xyHgoSYmFubmVyX2ZsYWdfc2V0XzA0EAEYASAGKAEwBHIcChBiYW5uZXJfZW1ibGVtXzIzEAEYASAGKAEwBHIdChFiYW5uZXJfdGlwX3NldF8wNBABGAEgBigBMARgAGABYAJoBXAFjQFs8x5/StEBCgdOUENfTG93EgAqBAgAEAAqBAgBEAAw2NjV8gU4AUITbnBjX2ZyaWVuZF9tZXJjaGFudEoAWogBChFiaXJkX2Jhbm5lcl9wb3JreRABGnEKEmJpcmRfYmFubmVyX21jY29vbHIeChJiYW5uZXJfZmxhZ19zZXRfMDQQARgBIAYoATAEchwKEGJhbm5lcl9lbWJsZW1fMjMQARgBIAYoATAEch0KEWJhbm5lcl90aXBfc2V0XzA0EAEYASAGKAEwBGAAYAFgAmgFcAWNAVNkZH9KzwEKCE5QQ19IaWdoEgAqBAgAEAAqBAgBEAAw2NjV8gU4BkIQbnBjX2ZyaWVuZF9lYWdsZUoAWogBChFiaXJkX2Jhbm5lcl9wb3JreRAGGnEKEmJpcmRfYmFubmVyX21jY29vbHIeChJiYW5uZXJfZmxhZ19zZXRfMDQQBhgBIAYoATAEchwKEGJhbm5lcl9lbWJsZW1fMjMQBhgBIAYoATAEch0KEWJhbm5lcl90aXBfc2V0XzA0EAYYASAGKAEwBGAAYAFgAmgFcAWNAb8sJX9iBAgAEAFiBAgBEAB6AIIBATGaAQDKAQUzLjAuMdIBATD4AQGgAtjY1fIF0gN7CgtiaXJkX2Jhbm5lchABGmoKC2JpcmRfYmFubmVyciAKFmJhbm5lcl9iYW5uZXJfbDFfcTFfczEQARgBIAYwBHIaChBiYW5uZXJfZW1ibGVtXzA4EAEYASAGMARyHQoTYmFubmVyX3RpcF9sMV9xMV9zMRABGAEgBjAEogQA9QUR8jJ/gAYJugYbCgxjbGFzc19rbmlnaHQSC3NraW5fa25pZ2h0+AYBmAcBgggCEAA="
            lines = template.readlines()
            lines[-2] = f"""    <string name="player">{clear_data}</string>\n"""
            
        rename("com.rovio.gold.v2.playerprefs.xml", file_name := "oldplayerdata.xml")

        if path.exists(f"{file_paths['oldplayerdata']}/{file_name}"):
            rename(f"{file_name}", file_name := f"ABE{choice(list(english_words_lower_set))}.xml")
            print(f"{Fore.LIGHTRED_EX}Renamed file to {file_name} due to 'oldplayerdata.xml' already exsisting.")
            

        shutil.move(f"{path.dirname(path.realpath(__file__))}/{file_name}", file_paths['oldplayerdata'])
    except FileNotFoundError:
        print(f"{Fore.LIGHTRED_EX}You must add your playdata in the same folder as this program. (com.rovio.gold.v2.playerprefs.xml)")
        return False
        
    with open(path.join(file_paths['wipedplayerdata'], 'com.rovio.gold.v2.playerprefs.xml'), "w") as f:
        f.writelines(lines)
    
    print(f"{Fore.LIGHTGREEN_EX}Back-uped your old playerdata file and named it {file_name} in the folder OldPlayerData!")
    sleep(1)    
    print(f"{Fore.LIGHTGREEN_EX}Data has been wiped! - please check your folder for the new file.")

def decode():
    try: 
        with open("com.rovio.gold.v2.playerprefs.xml", "r") as file, open("player_base64.json", "w+") as player_data:
            parsed = xmltodict.parse(file.read())
            old_data = parsed['map']['string'][7]['#text']
            player_data.write(old_data)
    except FileNotFoundError:
        print(f"{Fore.LIGHTRED_EX}You must add your playdata in the same folder as this program. (com.rovio.gold.v2.playerprefs.xml)")
        return False
        
    
    subprocess.run(['ABEpicPlayerDecoder', "decode", "player_base64.json", file_name := "decoded_data.json"])
    if path.exists(f"{file_paths['decodedplayerdata']}/{file_name}"):
        remove(f"{file_paths['decodedplayerdata']}/{file_name}")
    shutil.move(f"{path.dirname(path.realpath(__file__))}/{file_name}", file_paths['decodedplayerdata'])
    remove('player_base64.json')
    print(f"{Fore.LIGHTGREEN_EX}Success! the decoded data has been written to decoded_data.json")

def checkforFile() -> bool:
    if path.exists(f"{file_paths['decodedplayerdata']}/decoded_data.json"):
        pass
    else:
        print(f"{Fore.LIGHTRED_EX}You have not decoded your playerdata.")
        return False

    if path.exists("template.xml"):
        pass
    else:
        print(f"{Fore.LIGHTRED_EX}You do not have a template.xml")
        return False
    
    return True
    

        
def encode():
    if checkforFile():
        shutil.move(f"{path.dirname(path.realpath(__file__))}/DecodedPlayerData/decoded_data.json", file_paths['basepath'])
        subprocess.run(['ABEpicPlayerDecoder', 'encode', 'decoded_data.json', 'encoded_data.json'])
        with open('encoded_data.json', "r") as file, open('template.xml', "r") as template:
            base64data = "".join(x for x in file.readlines())
            template_lines = template.readlines()
            template_lines[-2] = f"""    <string name="player">{base64data}</string>\n"""
            
        with open(file_name := "com.rovio.gold.v2.playerprefs.xml", "w+") as file:
            file.writelines(template_lines)
        
        if path.exists(f"{file_paths['newplayerdata']}/{file_name}"):
            remove(f"{file_paths['newplayerdata']}/{file_name}")
        shutil.move(f"{path.dirname(path.realpath(__file__))}/{file_name}", file_paths['newplayerdata'])
        remove("decoded_data.json")
        remove('encoded_data.json')

        print(f"{Fore.LIGHTGREEN_EX}Success! the encoded data has been written to the playerdata file (com.rovio.gold.v2.playerprefs.xml) in the folder 'NewPlayerData'")

    
def main():
    user = input(f"{Fore.CYAN}~ ").lower()
    
    if user == "help":
        print(f"\n{Fore.MAGENTA}Decode - decodes the base64 in playdata.\n{Fore.LIGHTGREEN_EX}Encode - Changes the decoded file back to a normal file\n{Fore.LIGHTRED_EX}Cleardata - wipes the data\n{Fore.MAGENTA}Help - does this\n{Fore.RED}You {Fore.LIGHTGREEN_EX}MUST {Fore.RED}Put the playerprefs file in the same folder as this program\n")
        main()
        
    elif user == "cleardata":
        clear_data()
        main()
        
    elif user == "decode":
        decode()
        main()
        
    elif user == "encode":
        encode()
        main()
        
    else:
        print(f"{Fore.LIGHTRED_EX}Invalid command - use 'help'")
        sleep(1)
        system('cls')
        main()
            

if __name__ == "__main__":
    system('cls')
    system('title ABEClearData')
    for key, value in file_paths.items():
        if not path.exists(value):
            mkdir(value)
    main()