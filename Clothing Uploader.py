try:
    import time
    import colorama
    import requests
    import time
    import re
    import configparser
    from cleantext import clean
    config = configparser.ConfigParser()
    config.read_file(open(r"Config.ini"))
    import os
    from colorama import init, Fore, Back, Style
    init()
# If user doesn't have one of the modules, it will tell them to install all of the required
except ImportError:
    print("[ERROR] Failed to import some modules, make sure to run requirements.bat, delete all other python versions and install python 3.10.0 installed with add to path option checked during installation")
    input()

cookie = str(config.get("auth","cookie"))
group = str(config.get("clothing","group"))
description = str(config.get("clothing","description"))
priceconfig = int(config.get("clothing","price"))
ratelimz = int(config.get("optional","ratelimitwaitseconds"))
maxrobux = int(config.get("optional","maxrobuxtospend"))
debugmode = config.getboolean('optional', 'debugmode') 


path = os.getcwd()
try:
    os.remove(f"{path}\\Storage\\Clothes\\Shirts\\deleteme.png")
    os.remove(f"{path}\\Storage\\Clothes\\Pants\\deleteme.png")
except:
    pass

# Authentication into roblox account
session = requests.Session()
session.cookies[".ROBLOSECURITY"] = cookie
req = session.post(url="https://auth.roblox.com/")
if "X-CSRF-Token" in req.headers: 
    session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]  
req2 = session.post(url="https://auth.roblox.com/")
try:
    getuser = session.get("https://users.roblox.com/v1/users/authenticated")
    getuser2 = getuser.json()
    getuser3 = getuser2['id']
    getuser4 = getuser2['name']
    print(f"{Back.CYAN}{Fore.BLACK}[Authentication]{Back.BLACK}{Fore.WHITE} Logged in as {getuser4}")
except:
    print(f"{Back.RED}{Fore.BLACK}[Error]{Back.BLACK}{Fore.WHITE} Your cookie is invalid")
    print(f"{Back.YELLOW}{Fore.BLACK}[Info]{Back.BLACK}{Fore.WHITE} Please restart the program, with a valid cookie")
    input()

# Main program
brokie = session.get("https://economy.roblox.com/v1/user/currency")
brokie = brokie.json()
brokie=brokie["robux"]
print(f"{Back.CYAN}{Fore.BLACK}[Robux]{Back.BLACK}{Fore.WHITE} Remaining: R$ {brokie}")
print("\n")
pants = False
assetid = "1"
robuxspent = 0


def shirts():
    global group,description,priceconfig, name,creator,creatortype, pants,assetid, robuxspent, maxrobux

    if robuxspent >= maxrobux:
        print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Max robux spent reached, stopping program")
        input()
        return

    try:
        path = os.getcwd()
        if pants == False:
            pathz = f"{path}\\Storage\\Clothes\\Shirts"
        else:
            pathz = f"{path}\\Storage\\Clothes\\Pants"
        name = os.listdir(pathz)[0]
        name = name.split(".")
        name = name[0]
        creator = group
        creatortype = "Group"
        name = clean(name, no_emoji=True)
    except:
        if pants == False:
            
            print(f"{Back.MAGENTA}{Fore.BLACK}[Shirts]{Back.BLACK}{Fore.WHITE} All shirts have been uploaded, moving to pants\n")
            pants = True
            shirts()
            return
            
        else:
            print(f"{Back.MAGENTA}{Fore.BLACK}[Pants]{Back.BLACK}{Fore.WHITE} All pants have been uploaded, you may close the program")
            input()
            return
        return "hey"
        pants = True
        shirts()
        
    json = open("Storage\Json\config.json","w")
    json.write(f"""{{"name":"{name}","description":"{description}","creatorTargetId":"{creator}","creatorType":"{creatortype}"}}""")
    json.close()

    path = os.getcwd()
    if pants == False:
        
        link = "https://itemconfiguration.roblox.com/v1/avatar-assets/11/upload"
    if pants == True:
        link = "https://itemconfiguration.roblox.com/v1/avatar-assets/12/upload"
    
    files = {
        'media': open(fr"{pathz}\\{os.listdir(pathz)[0]}", 'rb'),
        'config': open('Storage\Json\config.json', 'rb')
        }
    s = session.post(link,files=files)
    if debugmode == True:
        print(f"Status: {s.status_code}\nResponse: {s.text}"
    files["media"].close()

    sd = s.json()
   
    try:
        assetid = sd['assetId']
    except:
        #files["media"].close()
        #os.remove(fr"{pathz}\\{os.listdir(pathz)[0]}")
        #print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Invalid template: {name}\n")
        code = sd['errors'][0]['code']
        if code == 16:
            print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Clothing name not allowed or invalid description, removing from list: {name}")
            files["media"].close()
            os.remove(fr"{pathz}\\{os.listdir(pathz)[0]}")
            shirts()
            return
        elif code == 0:
            print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Ratelimited, failed to upload (waiting {ratelimz}s): {name}\n")
            time.sleep(ratelimz)
            shirts()
            return
        elif code == 6:
            print(f"{Back.RED}{Fore.BLACK}[Robux]{Back.BLACK}{Fore.WHITE} You don't have 10 robux to upload: {name}")
            input()
        elif code == 7:
            print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Invalid template, removing from list: {name}")
            files["media"].close()
            os.remove(fr"{pathz}\\{os.listdir(pathz)[0]}")
            shirts()
            return
        elif code == 9:
            print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} You do not have permission to upload to the group")
            shirts()
            return
            

    pricefiles = {"price":priceconfig,"priceConfiguration":{"priceInRobux":priceconfig},"saleStatus":"OnSale"}
    priceupdate = f"https://itemconfiguration.roblox.com/v1/assets/{assetid}/release"
    price = session.post(priceupdate,json=pricefiles)

    if pants == False:
        if s.status_code == 200:
            print(f"{Back.GREEN}{Fore.BLACK}[Upload]{Back.BLACK}{Fore.WHITE} Successfully uploaded a shirt: {name}")
            robuxspent+=10
            os.remove(fr"{pathz}\\{os.listdir(pathz)[0]}")
        else:
            print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Failed to upload a shirt: {name}")
    else:
        if s.status_code == 200:
            print(f"{Back.GREEN}{Fore.BLACK}[Upload]{Back.BLACK}{Fore.WHITE} Successfully uploaded pants: {name}")
            robuxspent+=10
            os.remove(fr"{pathz}\\{os.listdir(pathz)[0]}")
        else:
            print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Failed to upload pants: {name}")

    if price.status_code == 200:
        print(f"{Back.GREEN}{Fore.BLACK}[Upload]{Back.BLACK}{Fore.WHITE} Successfully set price to R$ {priceconfig}")
    else:
        print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Failed to set a price: {name}")
    print("\n")
    brokie = session.get("https://economy.roblox.com/v1/user/currency")
    brokie = brokie.json()
    brokie=brokie["robux"]
    print(f"{Back.CYAN}{Fore.BLACK}[Robux]{Back.BLACK}{Fore.WHITE} Remaining: R$ {brokie}")
    print("\n")

    shirts()
if pants == False:
    a = shirts()
    if a == "hey":
        pants = True
        shirts()
