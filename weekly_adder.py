import argparse 
import requests 
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

BASE_URL = "https://api.spotify.com/v1" #The base URL for all the APi calls


def authorize(client_id, client_secret):
    redirect_uri = 'https://example.org/callback'
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private" #all of the authorization scopes we need
    sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)

    #auth_url = sp_oauth.get_authorize_url()
    #print(f"Please authorize the application by clicking the following link:\n{auth_url}")
    
    redirected_url = ""
    code = sp_oauth.parse_response_code(redirected_url)
    token = sp_oauth.get_access_token(code)

    return token['access_token']


def get_user_id(header):
    response = requests.get(
        url=f"{BASE_URL}/me",
        headers=header
    )#sends a request to get the user id
    user_id = response.json().get('id')

    return user_id


def get_saved_playlist(header, user_id):
    response = requests.get(
        url=f"{BASE_URL}/users/{user_id}/playlists?limit=50&offset=0",
        headers=header,
    )#sends a request to get a users saved plalists. Builds up the URL with an f string. Also gets a limit of 50 playlists
    playlists = response.json().get('items')#gets a list of playlist items (dict format)

    return playlists

def get_source_tracks(playlist):
    playlist_id = playlist['id'] #gets ID of our discover weekly playlist so it can be used in the next API call
    response = requests.get(
        url=f"{BASE_URL}/playlists/{playlist_id}/tracks",
        headers=header,
    ) 
    playlist_tracks = response.json().get('items') #returns an array of track objects

    uris_for_tracks = []
    for track in playlist_tracks:
        uris_for_tracks.append(track['track']['uri'])

    return uris_for_tracks #This is a list of the uri's we can then add to our saved playlist


def add_to_save_playlist(uri_list):
    target_playlist_id = target_playlist['id'] #gets ID of our playlist we will add the songs to
    response = requests.post(
            url=f"{BASE_URL}/playlists/{target_playlist_id}/tracks",
            headers=header,
            data = {
                "uris": f"{uri_list}"
            })#This adds the songs to the new playlist
    if response['status_code'] == 201:
        print("successfully saved Discover Weekly playlist!!")



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--client-id',
        dest="client_id",
        default=""
    )
    parser.add_argument(
        '--client-secret',
        dest="client_secret",
        default=""
    )
    parser.add_argument(
        '--playlist-name',
        dest="playlist_name",
        default=""
    )
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args() #gets command line arguments
    token = authorize(args.client_id, args.client_secret) #passes the clientID and the client secret which is generated by spotify to the token generator


    header = {
        'Authorization': f"Bearer {token}"
    } #Creates the header that will be sent in all requests

    user_id = get_user_id(header)
    saved_playlists = get_saved_playlist(header, user_id) #Gets a list of all the saved playlist

    source_playlist = None
    target_playlist = None
    #This is initializing the variables

    for playlist in saved_playlists:
        if playlist['name'] == args.playlist_name:
            target_playlist = playlist
        if playlist['name'] == "Discover Weekly":
            source_playlist = playlist
        if source_playlist and target_playlist:
            #check to see if we found both playlist
            #If we did we can break out of this loop
            break
    #This for loop loops through all of the returned playlists until it finds the correct one

    if not target_playlist:
        logging.warning("Your playlist was not found...\nTerminating script")
        exit()
    if not source_playlist:
        logging.warning("Your Discover weekly playlist was not found...\nEnsure it is added to your library\nTerminating script")
        exit()
    #These two if check will ensure we have found both a target and source playlist. We need both of these so if we are missing one then quit the scrip

    track_uris_from_source = get_source_tracks(source_playlist) #Gets the tracks from the discover weekly playlist
    add_to_save_playlist(track_uris_from_source)

#TODO:
#Look into Oauth so token doesn't expire every hour (for automation)