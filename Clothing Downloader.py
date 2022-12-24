try:
    import requests
    import requests, re, time, random, os
    from colorama import init, Fore
    import emoji
    import configparser
    from PIL import Image
    config = configparser.ConfigParser()
    config.read_file(open(r"Config.ini"))
    init()
except:
    print("Run Requirements.bat to install all required modules.")
    input()

path = os.getcwd()
try:
    os.remove(f"{path}\\Storage\\Clothes\\Shirts\\deleteme.png")
    os.remove(f"{path}\\Storage\\Clothes\\Pants\\deleteme.png")
except:
    pass

cookie = str(config.get("auth","cookie"))
templatechanger = config.getboolean('optional', 'templatechanger') 
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

print("Choose what type of clothing you would like to download\n")
print("Clothing\n- Shirts (s)\n- Pants (p)")
b = input("Enter type (s/p): ")
cltype = ""
if b.lower() == "shirts" or b.lower() == "shirt" or b.lower() == "s":
    cltype = "Shirts"
elif b.lower() == "pants" or  b.lower() == "pant" or b.lower() == "p":
    cltype = "Pants"
else:
    print("Invalid input, restart program.")
    input()
print(f"Selected: {cltype}")

print("\n")
print("Keywords example\n- emo goth y2k\n- slender black dark")
ab = input("Enter keywords: ")
ab = ab.strip()
ab = ab.replace(" ","+")
ab = ab.lower()

print("\n")
friendslist = []
nextpagecursor = ""
relevance = f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={ab}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&subcategory=Classic{cltype}"

favouritedalltime = f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={ab}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&sortAggregation=5&sortType=1&subcategory=Classic{cltype}"
favouritedallweek = f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={ab}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&sortAggregation=3&sortType=1&subcategory=Classic{cltype}"
favouritedallday = f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={ab}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&sortAggregation=5&sortType=1&subcategory=Classic{cltype}"

bestsellingalltime = f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={ab}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&sortAggregation=5&sortType=2&subcategory=Classic{cltype}"
bestsellingweek= f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={ab}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&sortAggregation=3&sortType=2&subcategory=Classic{cltype}"
bestsellingday = f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={ab}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&sortAggregation=1&sortType=1&subcategory=Classic{cltype}"

recentlyupdated = f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={ab}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&sortType=3&subcategory=Classic{cltype}"



print("Catalog Sorts\n-[1] Relevance\n\n-[2] Most Favourited (all time)\n-[3] Most Favourited (past week)\n-[4] Most Favourited (past day)\n\n-[5] Bestselling (all time)\n-[6] Bestselling (weekly)\n-[7] Bestselling (past day)\n\n-[8] Recently Updated")
sortby = input("Sort by: ")
if sortby == "1":
    a = relevance
    
elif sortby == "2":
    a = favouritedalltime
elif sortby == "3":
    a = favouritedallweek
elif sortby == "4":
    a = favouritedallday
    
elif sortby == "5":
    a = bestsellingalltime
elif sortby == "6":
    a = bestsellingweek
elif sortby == "7":
    a = bestsellingday
elif sortby == "8":
    a = recentlyupdated
else:
    print("Invalid input, restart program")
    input()
    
abx = a.split("&limit=120")

new1 = abx[1]
print("\nGathering clothes")

pagecurrent = 0
a = requests.get(a)
nextpagecursor = a.json()


try:
    nextpagecursor = nextpagecursor["nextPageCursor"]
except:
    print("Issue getting next page, try different key words/different sort - restart program")
    input()
    
   
abx = f"https://catalog.roblox.com/v1/search/items?category=Clothing&cursor={nextpagecursor}&keyword={ab}&limit=120{new1}"
ids_and_item_types = a.json()["data"]
if len(ids_and_item_types) == 0:
    print("No items found (bad keywords)")
    input()
friendslist = [datum["id"] for datum in ids_and_item_types]
pagecurrent+=1



while True:
    pagecurrent+=1
    abx = f"https://catalog.roblox.com/v1/search/items?category=Clothing&cursor={nextpagecursor}&keyword={ab}&limit=120{new1}"
    thelinks = abx

    a = requests.get(thelinks)
    nextpagecursor = a.json()
    
    try:
        
        nextpagecursor = nextpagecursor["nextPageCursor"]
    except:
        print(f"Max page limit of {pagecurrent} has been reached")
        break
    
    ids_and_item_types = a.json()["data"]
    haha = [datum["id"] for datum in ids_and_item_types]
    friendslist.extend(haha)
    
    

print(friendslist)

print("\nYou may close the program once you have enough, or program will continue till limit.")
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
        b=a
        b = remove_emoji(b)
        if len(r) >= 7500:
            print(f'Downloaded: {amount}')
            if cltype == "Shirts" and templatechanger == True:
                with open(f'Storage/Clothes/Shirts/{i}.png', 'wb') as f:
                    f.write(r)

                img1 = Image.open(fr"Storage/Clothes/Shirts/{i}.png")
                img2 = Image.open(r"Storage/Json/shirt.png")
                img1.paste(img2, (0,0), mask = img2)
                img1.save(f"Storage/Clothes/Shirts/{b}.png")
                pathz = f"{path}/Storage/Clothes/Shirts" 
                os.remove(fr"{pathz}/{i}.png")
                
                    
            elif cltype == "Pants" and templatechanger == True:
                with open(f'Storage/Clothes/Pants/{i}.png', 'wb') as f:
                    f.write(r)
                img1 = Image.open(fr"Storage/Clothes/Pants/{i}.png")
                img2 = Image.open(r"Storage/Json/pants.png")
                img1.paste(img2, (0,0), mask = img2)
                img1.save(f"Storage/Clothes/Pants/{b}.png")
                pathz = f"{path}/Storage/Clothes/Pants" 
                os.remove(fr"{pathz}/{i}.png")

            # If template changer off

            elif cltype == "Shirts" and templatechanger == False:
                with open(f'Storage/Clothes/Shirts/{b}.png', 'wb') as f:
                    f.write(r)
                    
            elif cltype == "Pants" and templatechanger == False:
                with open(f'Storage/Clothes/Pants/{b}.png', 'wb') as f:
                    f.write(r)
                
            
            amount+=1
                
        else:
            print(f'Unable to download asset')
   except:
        print(f'Unable to download asset')
        pass
print(f"Completed, downloaded {amount} clothes")
