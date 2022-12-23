import requests
import requests, re, time, random, os
from colorama import init, Fore
import emoji
import configparser
config = configparser.ConfigParser()
config.read_file(open(r"Config.ini"))
init()

path = os.getcwd()
try:
    os.remove(f"{path}\\Storage\\Clothes\\Shirts\\deleteme.png")
    os.remove(f"{path}\\Storage\\Clothes\\Pants\\deleteme.png")
except:
    pass

cookie = str(config.get("auth","cookie"))
session = requests.Session()
session.cookies[".ROBLOSECURITY"] = cookie

# send first request
req = session.post(
    url="https://auth.roblox.com/"
)

if "X-CSRF-Token" in req.headers:  # check if token is in response headers
    session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]  # store the response header in the session

# send second request
req2 = session.post(
    url="https://auth.roblox.com/"
)

# Attempt to get player user
try:
    getuser = session.get("https://users.roblox.com/v1/users/authenticated")
    getuser2 = getuser.json()
    getuser3 = getuser2['id']
    getuser4 = getuser2['name']
    print(f"Logged in as {getuser4}\n")

# If failed, it means the cookie is invalid, so the user will be told that
except:
    print(f"Your cookie is invalid")
    input()


print("Clothing\n- Shirts (s)\n- Pants (p)")
b = input("Enter type (s/p): ")
cltype = ""
if b.lower() == "shirts" or b.lower() == "shirt" or b.lower() == "s":
    cltype = "Shirts"
elif b.lower() == "pants" or  b.lower() == "pant" or b.lower() == "p":
    cltype = "Pants"
print(f"Selected: {cltype}")

print("\n")
print("Keywords example\n- emo goth y2k\n- slender black dark")
ab = input("Enter keywords: ")
ab = ab.strip()
ab = ab.replace(" ","+")
ab = ab.lower()

print("\n")
thelink = f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={ab}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&subcategory=Classic{cltype}"
thelinkweek= f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={ab}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&sortAggregation=3&sortType=2&subcategory=Classic{cltype}"

print("Sorts\n- [1] Bestseller (weekly)\n- [2] Relevance")
sortby = input("Sort by: ")
if sortby == "1":
    a = requests.get(thelinkweek)
elif sortby == "2":
    a = requests.get(thelink)
else:
    print("Wrong input, restart program")
    
ids_and_item_types = a.json()["data"]
friendslist = [datum["id"] for datum in ids_and_item_types]
print(friendslist)
print("\n")

def remove_emoji(string):
    return emoji.get_emoji_regexp().sub(u'', string)
        
amount = 0      
for i in friendslist:
   try:
        r = requests.get(re.findall(r'<url>(.+?)(?=</url>)', requests.get(f'https://assetdelivery.roblox.com/v1/asset?id={i}').text.replace('http://www.roblox.com/asset/?id=', 'https://assetdelivery.roblox.com/v1/asset?id='))[0]).content
        data = {
          "items": [
            {
              "itemType": "Asset",
              "id": i
            }
          ]
        }

                
        a = session.post("https://catalog.roblox.com/v1/catalog/items/details",json=data)
        a=a.json()
        a=a['data'][0]['name']
        i=a
        i = remove_emoji(i)
        if len(r) >= 7500:
            print(f'Downloaded')
            if cltype == "Shirts":
                with open(f'Storage/Clothes/Shirts/{i}.png', 'wb') as f:
                    f.write(r)
            elif cltype == "Pants":
                with open(f'Storage/Clothes/Pants/{i}.png', 'wb') as f:
                    f.write(r)
            amount+=1
                
        else:
            print(f'Unable to download asset')
   except:
        print(f'Unable to download asset')
        pass
print(f"Completed, downloaded {amount} clothes")
