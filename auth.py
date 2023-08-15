import requests
from urllib.parse import urlencode
import base64
import webbrowser
import argparse

def authorize(client_id, client_secret, redirect_uri):
    auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    } #This is the Oauth header that we need to provide for spotify

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))
    #This will open up your web browser. You will need to copy and paste all of the url AFTER the 'code=' flag in the url

    code = input("Please enter all of the url after 'code='")

    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")
    #This creates the encoded credentials of the users client id and secret

    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    } #This is the header we will pass to create a token

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    } #This is the data we will pass to the post request to get our token

    response = requests.post(
        url="https://accounts.spotify.com/api/token", 
        data=token_data, 
        headers=token_headers
        )
    token = response.json()["access_token"] #This is the actual access token that will be needed for the weekly_adder.py script

    print(f"This is your authorization token:\n\n{token}\n\nPlease store this somewhere safe you will need it for the weekly_adder.py script")
    print("This token will only need to be generated once unless you need to generate a new token")
    #These two print statements inform the user of their token


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--client-id',
        dest="client_id",
        help="This is the client id from the spotify developer dashboard"
    )
    parser.add_argument(
        '--client-secret',
        dest="client_secret",
        help="This is the client secret from the spotify developer dashboard"
    )
    parser.add_argument(
        '--redirect-uri',
        dest="redirect_uri",
        help="This is the redirect uri that was setup in the spotify developer dashboard"
    )
    args = parser.parse_args()
    #These are all of the arguments that are needed to run this script
    return args


if __name__ == "__main__":
    args = parse_args() #gets command line arguments
    authorize(args.client_id, args.client_secret, args.redirect_uri) #this calls the authorize function

   