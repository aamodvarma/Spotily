#!/bin/python3.9
import requests
import webbrowser
import base64
import json
from datetime import datetime

# Declarationof important variables

client_id = ""
client_secret = ""
clientc = f"{client_id}:{client_secret}"
b64 = base64.b64encode(clientc.encode()).decode()
redirect_uri = "http://localhost/"


def auth(client_id, redirect_uri):
    url = "https://accounts.spotify.com/authorize"
    # getting code after opening webbrowser
    webbrowser.open(
        url + f"?client_id={client_id}&scope=user-read-currently-playing user-read-playback-state&response_type=code&redirect_uri={redirect_uri}")
    code = input("Enter the code : ")[23:]
    return code


def check_time():
    f = open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/tokens.json", 'r')
    x = f.read()
    print(type(x))
    print(x)


def refresh_token():
    f = open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/refresh.txt", 'r')
    x = (f.read())
    if (x):
        f.close()
        return x
    else:
        f.close()
        return 0


def access_token(corno):
    if corno == 0:
        code = auth(client_id, redirect_uri)
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri
        }


    else:
        file = open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/time.txt", 'r')
        t = int(file.read())
        file.close()
        now = int(datetime.now().strftime("%H%M"))

        print("The access token has expired.\nUsing refresh token to generate new access token.")
        code = refresh_token()
        if code == 0:
            print("Refresh token not present, opening it up.")
            access_token(0)
            return 0
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": code,
        }
    # API TOKEN
    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {b64}"
    }
    x = requests.post(url, data=payload, headers=headers)

    with open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/tokens.json", 'w') as outfile:
        json.dump(x.json(), outfile)
    with open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/refresh.txt", 'r+') as outfile:
        y = outfile.read()
        if y:
            pass
        else:
            z = x.json()['refresh_token']
            outfile.write(z)
    with open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/time.txt", 'w') as outfile:
        y = str(int(datetime.now().strftime("%H%M")) + 100)
        outfile.write(y)


def getsong():
    file = open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/tokens.json", "r")
    x = json.loads(file.read())
    file.close()
    access_token = x['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    r = requests.get(url, headers=headers)
    if (str((r)) == "<Response [204]>"):
        print("No current playing track")
        return 0
    elif (str(r)) != "<Response [200]>":
        print("Error")
        print(str(r))
        return 0
    else:
        js = r.json()
        artist_name = js['item']['album']['artists'][0]['name']

        song_name = js['item']['name']
        return (song_name + " " + artist_name)


def file_empty_exists():
    file = open("/home/ajrv/PycharmProjects/SpotifyLyricsLatest/tokens.json", 'r')
    read = file.read()
    try:
        if not read or json.loads(read)['error']:
            return 0
        else:
            return 1
    except:
        return 1


def main():
    file_exists = file_empty_exists()
    if (file_exists == 0):
        access_token(0)
    else:
        access_token(1)
    song = getsong()
    if song:
        return song

    else:

        print("Error")
        return None
if __name__ == '__main__':
    y = main()
    if y:
        print(y.split())
