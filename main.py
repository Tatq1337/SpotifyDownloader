from __future__ import unicode_literals
import youtube_dl
import requests
import pywhatkit as pwt
playlist_id = '0jJV1X0DM2agvFxf93CyuD'  # changeable

cid = ''
secret = ''
AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': cid,
    'client_secret': secret,
})

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']


def getPlaylistTracks(token, playlistID) -> dict:
    endPoint = f'https://api.spotify.com/v1/playlists/{playlist_id}'

    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    res = requests.get(endPoint, headers=headers)

    playlistObject = res.json()
    return playlistObject



trackList = getPlaylistTracks(access_token, playlist_id)
songs = []


for track in trackList['tracks']['items']:
    artists = ''
    for artist in track['track']['artists']:
        artists += str(artist['name']) + ' '

    songName = track['track']['name']
    songs.append(artists + songName)
    artist = ''


def get_link(songs) -> list:
    data = []
    for x in songs:
        link = pwt.playonyt(x, open_video=False)
        data.append(link)

    return data


def download_songs(data) -> bool:
    for song in data:
        print(song)
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song])
        print("Downloading successful")



data = get_link(songs)
download_songs(data)

