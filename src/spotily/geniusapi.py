#!/bin/python3.9


import requests
import webbrowser
import json
import main
import os
song = main.main()

client_id = "hssdkAioHJca8N9wG5f46-2uAt3QS8jiAPqBiOfRuPDYNHsZbloFZnt0jndal82H"
client_secret = "CXhGMlSZXvHl2N-NSehY-roBmkfKQFFA4sm1WaVJipHWW_wjQ9HEA6kzzowkVBuAwKhB_nsyaBaEZKmN5wBb7Q"

def authoriza(cid, csec):
    redirect_url = "http://localhost/"
    url = "https://api.genius.com/oauth/authorize"
#    webbrowser.open(url + f"?client_id={client_id}&scope=create_annotation&response_type=code&redirect_uri={redirect_url}")

    webbrowser.open(url + f"?client_id={client_id}&response_type=code&redirect_uri={redirect_url}")
    authcode = input("Enter the link :")[23:]
    return authcode

def access_token_genius():

    x = authoriza(client_id, client_secret)

    payloads = {
        "code": x,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "http://localhost/",
        "response_type": "code",
        "grant_type": "authorization_code"
    }

    x = requests.post("https://api.genius.com/oauth/token", data=payloads)
    with open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/gtokens.json", 'w') as outfile:
        json.dump(x.json(), outfile)
    getlyrics()


def getsongid():
    file = open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/gtokens.json", "r")
    x = json.loads(file.read())
    file.close()
    access_token = x['access_token']

    header = {
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "q": song
    }
    l = requests.get("https://api.genius.com/search",data=payload ,headers=header)
    apipath = l.json()['response']['hits'][0]['result']['api_path']
    return apipath
  # with open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/temp.html", 'w') as outfile:
   #     json.dump(html, outfile)
 #access_token()

def getlyrics():
   apipath = getsongid()
 #  x = int(input("1 or 2 :"))
   # if x == 1 :
   #     trial = requests.get(f"https://genius.com{apipath}")
   #     html = BeautifulSoup(trial.text, "html.parser")
   #     lyrics = html.find("div", class_="lyrics").get_text()
   #     print(lyrics)
   # if x == 2:
   #     webbrowser.open(f"https://genius.com{apipath}")

#   webbrowser.open(f"https://genius.com{apipath}")
   os.system(f"firefox-developer-edition https://genius.com{apipath}")


#access_token_genius()
getlyrics()
